#!/usr/bin/env bash
set -euo pipefail

# Installation locale OmniVoice CPU-first, sans CUDA requis.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python 3 est requis (Python 3.10+ recommandé)." >&2
  exit 1
fi

"$PYTHON_BIN" -m venv .venv
.venv/bin/python -m pip install --upgrade pip wheel

# Installer d'abord PyTorch CPU. Sur Mac Apple Silicon, PyTorch peut utiliser MPS
# si disponible ; le script de génération choisira automatiquement le périphérique.
.venv/bin/python - <<'PY'
import platform, subprocess, sys
if platform.system() == "Darwin":
    # Official macOS PyTorch wheel enables MPS on supported Apple Silicon machines.
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "torch"]
else:
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "--index-url", "https://download.pytorch.org/whl/cpu", "torch"]
subprocess.run(cmd, check=True)
PY

.venv/bin/python -m pip install --upgrade soundfile numpy
if ! .venv/bin/python -m pip install --upgrade omnivoice; then
  echo "PyPI install failed; trying the official OmniVoice Git repository..."
  .venv/bin/python -m pip install --upgrade "git+https://github.com/k2-fsa/OmniVoice.git"
fi

.venv/bin/python - <<'PY'
import sys, torch
print("Python :", sys.version.split()[0])
print("PyTorch :", torch.__version__)
print("CUDA disponible :", torch.cuda.is_available())
print("MPS disponible :", bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available()))
try:
    from omnivoice import OmniVoice
    print("Import OmniVoice réussi.")
except Exception as exc:
    raise SystemExit(f"Échec de l'import OmniVoice dans {sys.executable}: {type(exc).__name__}: {exc}")
PY

echo
echo "Installation terminée. Vérifie la présence de audio/snk-00054.wav et audio/snk-00258.wav."
echo "Puis lance : .venv/bin/python scripts/generate_voice.py --generate --device cpu --limit 20"
