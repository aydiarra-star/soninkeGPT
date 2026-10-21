# Asawan Soninke–French–English lexicon: ingestion note

## Source identified

- Source page (French): https://www.asawan.org/fr/lexique_soninke
- Source page (English): https://www.asawan.org/en/Soninke_lexicon
- Online lexicon app: https://media.ipsapps.org/snk/oda/
- Download advertised by Asawan: `Lexique Soninke-Francais-English (17.25 Mo)`
- Direct download URL exposed by the page:
  https://www.asawan.org/sites/www.asawan.org/files/uploads/Lexique%20Soninke-Francais-English%2006-2016.exe

Asawan describes this as a trilingual Soninke–French–English lexicon. SIL's published-lexicons page also lists the Soninke–French–English dictionary as available through Asawan.

## Status of this ingestion attempt

The source has been located, but the downloadable `.exe` was not retrievable through the current tool environment (the browser rejects the binary content type and the direct download attempt failed). The online app opens as an embedded application but exposes no lexicon entries as readable page text through the current retrieval tools.

**No lexical entries have been copied from this source, no new candidate batch has been claimed, and no production files have been modified.** This prevents accidental invention of entries or presenting guessed content as source-derived data.

## Next ingestion procedure

1. Obtain the official `.exe` file or a machine-readable export from the source.
2. Inspect the executable safely without running it; determine whether it is a self-extracting archive or contains a database/text resource.
3. Extract only the dictionary data, preserve original Soninke spelling and each French/English sense, and record source attribution.
4. Compare forms with `data/source/lexique-soninke-fr-base.csv` and `data/audio/new-lexicon-candidates-production-queue.csv` using Unicode NFC and exact normalized form matching first.
5. Keep variants and homographs separate; do not auto-merge approximate matches.
6. Add candidates to a source-specific staging CSV, mark them `a_verifier`, and do not add them to the production audio queue until reviewed.

## Attribution and caveat

Asawan's lexicon is a source for candidate discovery, not automatic linguistic validation. The displayed download is dated 06-2016; verify the source's terms and attribution before redistributing extracted data.
