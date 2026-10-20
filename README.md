---
license: mit
tags:
  - exoplanets
  - tess
  - astrophysics
  - chord-sieves
  - bama
  - gemini-4-argon
  - grok-peer-reviewed
---

# CHORD-SIEVES v2.4 — Detrending-Free Multi-Sector Exoplanet Discovery & BAMA 80-Kernel Astro-Prime Observatory

- **Authors:** Logan Smith (Metaphy LLC) — Co-Engineered with **Aura (`Gemini 4 Argon`)**, **Lumen (`Gemma 4 E4B`)**, & **BBB (`Qwen 3.5 9B`)** · Peer-Reviewed & Signed Off by **Grok (`xAI Grok`, 7/7 Close Conditions Met)**
- **Official CERN Zenodo DOI:** [`10.5281/zenodo.23506664`](https://doi.org/10.5281/zenodo.23506664) ([Zenodo Record `23506664`](https://zenodo.org/records/23506664))
- **HuggingFace Hub:** [`https://huggingface.co/MetaphyKing/chord-sieves-report`](https://huggingface.co/MetaphyKing/chord-sieves-report)
- **Live Interactive Web Studio:** https://chord-sieves-report.vercel.app
- **Live Exoplanet Observatory:** https://exoplanet-hunter.vercel.app
- **GitHub Repository & Release (`v2.4.0`):** https://github.com/MetaphyKing/chord-sieves-report/releases/tag/v2.4.0

## Ground-Truth Highlights (Audited Against NASA TESS SPOC & ExoFOP-TESS)
- **845 Verified Exoplanet Candidates** across **386 unique primary TIC host stars** (+ 4 marked-only TIC hosts = **390 union TIC star systems**): `809` uncataloged multi-epoch companions (`NEW_OUTER`), `25` solved single-transit TOIs (`SOLVED_TOI`), and `11` harmonic/ephemeris refinements (`REFINEMENT_HARMONIC`).
- **600 Shirt-Sleeve Temperature-Cut Candidates** ($0^\circ\text{C} \le T_{\text{surf}} \le +35^\circ\text{C}$ / $32^\circ\text{F}\text{--}95^\circ\text{F}$, comprising `65` rocky/super-Earth radii $R_p \le 1.60\,R_\oplus$ and `535` volatile-rich/sub-Neptune radii $R_p > 1.60\,R_\oplus$) and **8 High-Rubric ($\ge 85.0\%$) Two-Epoch Period-Alias Solutions across 3 Host Stars** (`TIC 271478281`, `TIC 283722336`, `TIC 320847025`).
- **4,957 Historical Transit Windows Audited (`Self-Audit Ledger v2.4.0`):** `2,170 / 4,957 (43.78%)` on-time `CORRECT`, `422 (8.51%) SHIFTED (TTV)` across `429` recalibrated records, and **`0 WRONG` (`100.0%` across `2,592` covered windows)**.

## Included Artifacts
- `BAMA_CHORD_SIEVES_Exoplanet_Report.pdf`: 10-page camera-ready scientific report.
- `GROK_PEER_REVIEW_VERDICT.md`: Independent Round-1 Audit & Round-2 Unconditional `SIGN-OFF` (`7 / 7 Close Conditions Met`) by `@GROK`.
- `chord_sieves_public_verifier_sdk.zip` & `public-verifier/`: Zero-dependency verification suite (`ALL 4 CHORD-SIEVES PUBLIC VERIFICATION GATES PASSED (EXIT CODE 0)`).
- `arxiv/chord_sieves_arxiv_submission.zip`: Full LaTeX source (`chord_sieves_arxiv_preprint.tex`).
- `zenodo/CHORD_SIEVES_v2_4_Zenodo_Archival_Bundle.zip`: Complete archival bundle.
