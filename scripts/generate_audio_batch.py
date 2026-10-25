#!/usr/bin/env python3
"""Generate exactly the reviewed 100-word Soninke batch from its committed CSV."""
import argparse, csv, wave
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BATCH = ROOT / "data/source/audio-batch-100-2026-10-25.csv"
PROGRESS = ROOT / "data/source/audio-batch-100-progress.csv"
ERRORS = ROOT / "data/voice-generation-errors.csv"
def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f: return list(csv.DictReader(f))
def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True); tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    tmp.replace(path)
def valid_wav(path):
    try:
        with wave.open(str(path), "rb") as w: return w.getnframes()>0 and w.getframerate()>0 and w.getnchannels()>0
    except (wave.Error, EOFError, OSError): return False
def main():
    p=argparse.ArgumentParser(); p.add_argument("--batch",default=str(DEFAULT_BATCH)); p.add_argument("--limit",type=int,default=100); p.add_argument("--device",choices=("auto","cpu","cuda","mps"),default="auto"); args=p.parse_args()
    rows=read_csv(Path(args.batch))
    if len(rows)!=100: raise SystemExit(f"Arrêt sécurité : 100 lignes exigées, trouvé {len(rows)}.")
    required=("id","soninke","francais","source","audio_path")
    for n,r in enumerate(rows,1):
        missing=[k for k in required if not str(r.get(k,"")).strip()]
        if missing: raise SystemExit(f"Ligne {n}, champs manquants : {', '.join(missing)}.")
    ids=[r["id"] for r in rows]; forms=[r["soninke"] for r in rows]
    if len(set(ids))!=100 or len(set(forms))!=100: raise SystemExit("Identifiants ou formes soninké dupliqués.")
    limit=max(1,min(args.limit,100)); fields=list(rows[0].keys())+["generation_status","pronunciation_validation","audio_file_created","error"]
    if PROGRESS.exists():
        state=read_csv(PROGRESS)
        if len(state)!=100 or [r.get("id") for r in state]!=ids: raise SystemExit("Le suivi existant ne correspond pas au lot.")
        for old,src in zip(state,rows):
            for k in required:
                if old.get(k,"")!=src.get(k,""): raise SystemExit(f"{k} modifié pour {src['soninke']}.")
    else:
        state=[{**r,"generation_status":"en_attente_generation","pronunciation_validation":"en_attente_ecoute_referent","audio_file_created":"","error":""} for r in rows]
        write_csv(PROGRESS,state,fields)
    import numpy as np, soundfile as sf, torch
    from omnivoice import OmniVoice
    if args.device=="auto":
        device="cuda:0" if torch.cuda.is_available() else ("mps" if getattr(torch.backends,"mps",None) and torch.backends.mps.is_available() else "cpu")
    else: device=args.device
    if device.startswith("cuda") and not torch.cuda.is_available(): raise SystemExit("CUDA demandé mais indisponible.")
    if device=="mps" and not (getattr(torch.backends,"mps",None) and torch.backends.mps.is_available()): raise SystemExit("MPS indisponible.")
    dtype=torch.float16 if device.startswith("cuda") else torch.float32
    print(f"Chargement OmniVoice sur {device} ({dtype}); lot cible : {limit}.")
    model=OmniVoice.from_pretrained("k2-fsa/OmniVoice",device_map=device,dtype=dtype)
    names={str(x).casefold() for x in model.supported_language_names()}; langs={str(x).casefold() for x in model.supported_language_ids()}
    if not (any("sonink" in x for x in names) or "snk" in langs): raise SystemExit("Le modèle ne confirme pas la prise en charge du soninké. Pas de substitution.")
    refs=[ROOT/"audio/snk-00054.wav",ROOT/"audio/snk-00258.wav"]
    for r in refs:
        if not valid_wav(r): raise SystemExit(f"Référence vocale absente/invalide : {r}")
    a,sr=sf.read(refs[0]); b,sr_b=sf.read(refs[1])
    if sr!=sr_b: raise SystemExit("Fréquences de référence incompatibles.")
    if a.ndim>1: a=a.mean(axis=1)
    if b.ndim>1: b=b.mean(axis=1)
    ref=ROOT/"audio/generated/reference.wav"; ref.parent.mkdir(parents=True,exist_ok=True)
    sf.write(ref,np.concatenate([a,np.zeros(int(.4*sr)),b]),sr)
    failures=[]; done=0
    for i,row in enumerate(state[:limit]):
        out=ROOT/row["audio_path"]; out.parent.mkdir(parents=True,exist_ok=True)
        if valid_wav(out):
            row["generation_status"]="wav_present_controle_technique_ok"; row["audio_file_created"]=row["audio_path"]; row["error"]=""; done+=1; continue
        row["generation_status"]="generation_en_cours"; row["error"]=""; write_csv(PROGRESS,state,fields)
        try:
            result=model.generate(text=row["soninke"],language="snk",ref_audio=str(ref),ref_text="Daga goli. Li taxu.",num_step=32)
            samples=np.asarray(result[0]).squeeze()
            if samples.ndim!=1 or not samples.size or not np.isfinite(samples).all(): raise ValueError("Sortie audio vide/invalide.")
            tmp=out.with_suffix(".tmp.wav"); sf.write(tmp,samples,int(model.sampling_rate),subtype="PCM_16")
            if not valid_wav(tmp): tmp.unlink(missing_ok=True); raise ValueError("WAV invalide après écriture.")
            tmp.replace(out); row["generation_status"]="wav_genere_a_ecouter"; row["audio_file_created"]=row["audio_path"]; row["pronunciation_validation"]="en_attente_ecoute_referent"; done+=1
            print(f"[{i+1}/{limit}] WAV créé : {row['soninke']}")
        except Exception as exc:
            row["generation_status"]="echec_generation"; row["error"]=str(exc); failures.append({"soninke":row["soninke"],"francais":row["francais"],"audio_path":row["audio_path"],"erreur":str(exc)})
            print(f"[{i+1}/{limit}] ÉCHEC : {row['soninke']}: {exc}")
        write_csv(PROGRESS,state,fields)
    write_csv(PROGRESS,state,fields)
    if failures: write_csv(ERRORS,failures,["soninke","francais","audio_path","erreur"])
    elif ERRORS.exists(): ERRORS.unlink()
    ref.unlink(missing_ok=True)
    check=read_csv(PROGRESS)
    assert len(check)==100 and [r["soninke"] for r in check]==forms and [r["francais"] for r in check]==[r["francais"] for r in rows]
    print(f"Fin : {done}/{limit} WAV présents ou générés; {len(failures)} erreurs. Les 100 traductions restent conservées.")
if __name__=="__main__": main()
