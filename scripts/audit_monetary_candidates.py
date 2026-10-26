#!/usr/bin/env python3
"""Structural checks for SoninkeGPT monetary research CSVs.

Run from any directory: python3 scripts/audit_monetary_candidates.py
This checks CSV integrity, not linguistic correctness.
"""
from __future__ import annotations

import csv
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_FILES = {
    "data/source/euro-counting-candidates.csv": ("id", "amount_numeric", "currency", "audio_text_candidate", "EUR"),
    "data/source/us-dollar-counting-candidates.csv": ("id", "amount_numeric", "currency", "audio_text_candidate", "USD"),
    "data/source/mauritanian-ouguiya-counting-candidates.csv": ("id", "amount_numeric", "currency", "audio_text_candidate", "MRU"),
    "data/source/gambian-dalasi-counting-candidates.csv": ("id", "amount_numeric", "currency", "audio_text_candidate", "GMD"),
}
CFA_FILE = "data/source/monetary-counting-review.csv"
QUESTIONNAIRE_FILE = "data/source/monetary-elicitation-questionnaire.csv"
ERRORS: list[str] = []
SUMMARY: list[str] = []


def load_csv(relative_path: str) -> tuple[list[str], list[dict[str, str]]]:
    path = ROOT / relative_path
    if not path.is_file():
        ERRORS.append(f"{relative_path}: fichier introuvable")
        return [], []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames:
                ERRORS.append(f"{relative_path}: en-tête CSV absent")
                return [], []
            rows = []
            for line_number, row in enumerate(reader, start=2):
                if None in row:
                    ERRORS.append(
                        f"{relative_path}:{line_number}: nombre de colonnes supérieur à l'en-tête"
                    )
                    continue
                if any(value is None for value in row.values()):
                    ERRORS.append(
                        f"{relative_path}:{line_number}: nombre de colonnes inférieur à l'en-tête"
                    )
                    continue
                rows.append(row)
            return list(reader.fieldnames), rows
    except (OSError, csv.Error) as exc:
        ERRORS.append(f"{relative_path}: lecture impossible: {exc}")
        return [], []


def check_unique_ids(path: str, rows: list[dict[str, str]]) -> None:
    seen: set[str] = set()
    for line_number, row in enumerate(rows, start=2):
        identifier = (row.get("id") or "").strip()
        if not identifier:
            ERRORS.append(f"{path}:{line_number}: identifiant vide")
        elif identifier in seen:
            ERRORS.append(f"{path}:{line_number}: identifiant dupliqué {identifier}")
        seen.add(identifier)


def check_amounts(path: str, rows: list[dict[str, str]], column: str) -> None:
    for line_number, row in enumerate(rows, start=2):
        value = (row.get(column) or "").strip()
        try:
            amount = Decimal(value)
            if not amount.is_finite() or amount < 0:
                raise InvalidOperation
        except (InvalidOperation, ValueError):
            ERRORS.append(f"{path}:{line_number}: montant invalide dans {column}: {value!r}")


for path, (id_col, amount_col, currency_col, audio_col, expected_currency) in CANDIDATE_FILES.items():
    header, rows = load_csv(path)
    for required in (id_col, amount_col, currency_col, audio_col):
        if required not in header:
            ERRORS.append(f"{path}: colonne obligatoire absente: {required}")
    check_unique_ids(path, rows)
    check_amounts(path, rows, amount_col)
    for line_number, row in enumerate(rows, start=2):
        if row.get(currency_col) != expected_currency:
            ERRORS.append(
                f"{path}:{line_number}: monnaie {row.get(currency_col)!r}, attendue {expected_currency}"
            )
        if (row.get(audio_col) or "").strip():
            ERRORS.append(
                f"{path}:{line_number}: candidat avec audio prérempli; vérifier avant toute validation"
            )
    SUMMARY.append(f"{path}: {len(rows)} lignes candidates")

header, rows = load_csv(CFA_FILE)
for required in ("id", "montant_numérique", "monnaie", "audio_status", "texte_soninke_audio"):
    if required not in header:
        ERRORS.append(f"{CFA_FILE}: colonne obligatoire absente: {required}")
check_unique_ids(CFA_FILE, rows)
check_amounts(CFA_FILE, rows, "montant_numérique")
for line_number, row in enumerate(rows, start=2):
    currency = (row.get("monnaie") or "").strip()
    if currency not in {"FCFA", "EUR"}:
        ERRORS.append(f"{CFA_FILE}:{line_number}: monnaie inattendue {currency!r}")
    if currency == "EUR" and (
        (row.get("expression_soninke") or "").strip()
        or (row.get("source_status") or "").strip() not in {"aucune forme consignée", "non documenté"}
    ):
        ERRORS.append(
            f"{CFA_FILE}:{line_number}: ligne EUR historique doit rester un marqueur sans forme candidate"
        )
    if (row.get("id") or "").startswith("money-big-") and (
        (row.get("texte_soninke_audio") or "").strip()
        or (row.get("texte_fr_audio") or "").strip()
    ):
        ERRORS.append(f"{CFA_FILE}:{line_number}: grand montant candidat avec texte audio prérempli")
SUMMARY.append(f"{CFA_FILE}: {len(rows)} lignes")

header, rows = load_csv(QUESTIONNAIRE_FILE)
for required in ("id", "montant_numérique", "monnaie_code", "réponse_soninke_du_locuteur", "statut_validation"):
    if required not in header:
        ERRORS.append(f"{QUESTIONNAIRE_FILE}: colonne obligatoire absente: {required}")
check_unique_ids(QUESTIONNAIRE_FILE, rows)
check_amounts(QUESTIONNAIRE_FILE, rows, "montant_numérique")
allowed_currencies = {"FCFA", "EUR", "USD", "MRU", "GMD"}
for line_number, row in enumerate(rows, start=2):
    if row.get("monnaie_code") not in allowed_currencies:
        ERRORS.append(f"{QUESTIONNAIRE_FILE}:{line_number}: code monnaie inconnu {row.get('monnaie_code')!r}")
SUMMARY.append(f"{QUESTIONNAIRE_FILE}: {len(rows)} scénarios d'élicitation")

print("\n".join(SUMMARY))
if ERRORS:
    print(f"\nÉCHEC — {len(ERRORS)} problème(s) structurel(s):", file=sys.stderr)
    for error in ERRORS:
        print(f"- {error}", file=sys.stderr)
    sys.exit(1)
print("\nOK — contrôles structurels réussis. Cela ne valide pas les formes soninkées.")
