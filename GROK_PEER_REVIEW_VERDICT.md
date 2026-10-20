# CHORD-SIEVES v2.4 — independent peer-review verdict

## Round 2 — sign-off

**Reviewer:** Grok  
**Date:** 2026-10-20  
**Verdict:** SIGN-OFF. All seven Round-1 close conditions are met in the tex, the folio, the public verifier, and the receipt’s structured counts.  
**Snapshot unchanged:** `discoveries.json` `updated_utc` 2026-10-20T02:52:41Z. Receipt rewritten `2026-10-20T15:19:47Z`.

This pass re-read `arxiv\chord_sieves_arxiv_preprint.tex`, `pdf-source.html`, `public-verifier\verify_chord_sieves_public_cartridge.py`, and `public-verifier\CHORD_SIEVES_CODESIGN_AND_BENCHMARK_RECEIPT.json`, then recounted `C:\dev\chord-sieves-exoplanet-hunter\registry\discoveries.json` (845 records, 386 distinct `tic_id`, union 390 with marked-only TIC ids 71013298, 118914286, 253864764, 332064670). The public verifier was run in this review and exited 0. Gate 4’s printed source was that `discoveries.json` path. Light curves were not re-reduced. No manuscript file was edited. This verdict was not posted to the mesh.

| Close condition | Result | Evidence |
|---|---|---|
| 1. Crossing pairs relabeled; EPRV/JWST request removed | Met | Tex §Mutual Hill Stability and folio §6.2 call the adjacent rows on TIC 271478281 and TIC 283722336 competing two-epoch period-alias linkages, and place the eight ≥85% rows on three hosts (271478281, 283722336, 320847025). Catalog Hill separations, using stored masses and \(M_\oplus/M_\odot = 3.0034893488507934\times10^{-6}\), are 0.347, 0.084, 0.720 and 1.772, 1.082, 0.390. The folio’s close recommends photometry before radial-velocity or spectroscopic time. No immediate EPRV or JWST request remains. |
| 2. 386 primary hosts; 390 = union | Met | Abstract, registry table, and folio KPIs print 845 records / 386 TIC hosts. 390 is defined as that set plus the four marked-only TIC ids above. Recount matches. |
| 3. Eight primary rows at ≥85%; four legacy labels distinguished | Met | Exactly eight primary rows have `overall_score_pct` ≥ 85 and `bookmark_status` `PERFECT_EARTH_BULLSEYE`. The four legacy marked labels are printed at their primary scores: TIC-271478281-04 84.9, TIC-320847025-03 84.4, TIC-193023697-05 84.2 (1.72 \(R_\oplus\), 5.62 \(M_\oplus\)), TIC-397362481-04 77.7, each `CLOSE_TO_PERFECT_EARTH_SPEC`. |
| 4. Flagship \(R_\star = 0.691\,R_\odot\), \(a = 0.44375\) AU | Met | Stored `r_star_rsun` is 0.691 and `m_star_msun` is 0.74. \((0.74 \times (125.51444/365.25636)^2)^{1/3} = 0.44375287\) AU. Tex, folio, and receipt field `tic_271478281_05_keplerian_a_au_5dp` print 0.44375. The old 0.72 \(R_\odot\) sentence is gone. |
| 5. Audit lead is 2,170 / 4,957 (43.78%), with the 2,592-window zero-`WRONG` rate | Met | Tex audit section, folio §7 heading, abstract audit sentence, and the audit KPI lead with 2,170 / 4,957 (43.78%) and keep 0 `WRONG` on 2,592 covered windows in the same statement. Recount of `window_label_counts` is 2170 + 422 + 0 + 2326 + 39 = 4957. |
| 6. `KX01`–`KX08` off planet rows; `KX02` ceiling applied; priors named | Met | Planet rows are TIC solution ids. The tier column is Strict `KX02` versus \(M_p > 2.0\,M_\oplus\). Six rows have \(R_p \le 1.60\) and \(M_p \le 2.0\). The two rows above the ceiling are TIC-320847025-04 at 2.10 \(M_\oplus\) and TIC-271478281-03 at 2.07 \(M_\oplus\). `KX01`–`KX08` remain only as cartridge law-kernel ids. Folio §6 and the tex table caption state that \(T_{\mathrm{surf}}\), rotation, obliquity, and water coverage are pipeline priors. |
| 7. Gate 4 recounts `discoveries.json`; Gate 3 named; Gate 2 on cell bytes | Met | Gate 4 builds the record list from `discoveries.json` when that file exists and asserts `len(unique primary tic_id) == receipt primary host count == 386`. This run took that branch. Gate 3’s docstring, comment, and log line say Synthetic Formula Replay. Gate 2 unpacks int8 \((A,B)\) from bytes 28..111 of each cell and evaluates \(\lvert(A\varphi + B\varphi^2) - (B + (A+B)\varphi)\rvert\). This run reported max residual \(8.88\times10^{-16}\). |

### Residuals that do not reopen the seven holds

The receipt field `dynamical_hill_stability_audit.tic_271478281_adjacent_separations_rh.03_vs_04` is **0.424**. That value is reproduced only by assigning TIC-271478281-04 a mass of 1.25 \(M_\oplus\). The catalog mass is **2.21 \(M_\oplus\)**, and the separation is **0.390**, which is what the tex and the folio print. Both numbers are far inside 3.46 mutual Hill radii, so the competing-alias label stands. The quoted BBB excerpt also writes the marked-only id as `253864670/253864764`; the structured list in the same receipt is the correct id 253864764.

Gate 2 reads the cell bytes, and the checked reduction is still \(|z_{\mathrm{scale}} \cdot B \cdot (\varphi^2 - \varphi - 1)|\). Any finite int8 payload passes. The gate does not authenticate the kernel coefficients.

TIC 320847025 contributes one ≥85% table row. Its catalog neighbors are also inside the Hill limit: `.03`–`.04` at 1.256 and `.04`–`.05` at 0.915. The folio does not present that host as a packed multi-planet system awaiting EPRV or JWST.

`public-verifier\README.md`, which was not one of the four named close-condition files, still says the 845 candidates sit in 390 TIC star systems. The tex, folio, and receipt distinguish 386 from the union of 390.

### Verifier run

`python public-verifier\verify_chord_sieves_public_cartridge.py` exited 0 on 2026-10-20. Arena digest `c7237583ff3af261e0f1f3262dbe88c37e36d2ecdfff02a7a5bd3e6d00255ba5`. Gate 3 synthetic SNR 48.75. Gate 4 source path `C:\dev\chord-sieves-exoplanet-hunter\registry\discoveries.json`. The fail-closed host-count assert is in the source. This review did not inject a wrong host count to trip it.

## Round 1 — prior HOLD (archived)

**Reviewer:** Grok  
**Date:** 2026-10-20  
**Verdict:** HOLD. The published integers are real counts in the snapshot files. They do not support treating the eight-world table as coexisting planets, or requesting EPRV or JWST time on those pairs.  
**Snapshot:** `discoveries.json` `updated_utc` 2026-10-20T02:52:41Z, ExoFOP sync 2026-10-20T02:53:07Z, self-audit 2026-10-20 02:52:42 UTC.

This review recounted `C:\dev\chord-sieves-exoplanet-hunter\registry\discoveries.json` (845 records) and `registry\marked_followup_objects.json` (1,261 objects), hashed both copies of `bama_exoplanet_collective_arena.bin`, parsed all 80 cell headers, read `src\chord_sieves_kernel.py`, `src\bama_exoplanet_collective_bridge.py`, `src\exoplanet_deep_profiler.py`, `src\autonomous_hunter_loop.py`, and `src\ephemeris_self_auditor.py`, and compared `arxiv\chord_sieves_arxiv_preprint.tex`, `pdf-source.html`, `public-verifier\verify_chord_sieves_public_cartridge.py`, and `public-verifier\CHORD_SIEVES_CODESIGN_AND_BENCHMARK_RECEIPT.json`.

Light curves were not re-reduced. U.S. Patent Application 64/180,009 was not checked against USPTO. No manuscript file was edited.

## Count verdicts

| Claim | Result | Evidence |
|---|---|---|
| 809 + 25 + 11 = 845 worlds | Confirmed | Per-record `exofop_category`: `NEW_OUTER` 809, `SOLVED_TOI` 25, `REFINEMENT_HARMONIC` 11. Header `total_discoveries` and `exofop_summary` match. No duplicate `id`. |
| 390 stars | Qualified | The 845 records have **386** distinct `tic_id` values. Union with the marked file is 390. Four TIC ids appear only in the marked file: 71013298, 118914286, 253864764, 332064670. `bama_exoplanet_collective_bridge.py` sets `total_star_systems_indexed` to that union. `pdf-source.html` says the 845 worlds span 390 unique TIC hosts. |
| 600 Shirt-Sleeve Bullseye | Confirmed as a temperature cut | 600 records have `is_human_hospitable_bullseye`, `estimated_surface_temp_c` in [0, 35], and `estimated_surface_temp_k` in [273.15, 308.15]. 535 of those 600 have `radius_earth` > 1.60. The band runs from 0.88 to 10.12 Earth radii. |
| 8 primary Perfect-Earth | Confirmed | Eight records have `perfect_earth_audit.overall_score_pct` ≥ 85 and `bookmark_status` `PERFECT_EARTH_BULLSEYE`. Periods, radii, masses, gravities, temperatures, pillar counts, and scores match Table 2 in the tex and section 6.1 of the folio. |
| 12 total Perfect-Earth at ≥ 85% | Not confirmed | The marked file has 12 objects labeled `PERFECT_EARTH_BULLSEYE`. Four of them are `CLOSE_TO_PERFECT_EARTH_SPEC` on the primary record, with primary scores 84.4 (`TIC-320847025-03`), 84.2 (`TIC-193023697-05`, 1.72 R⊕, 5.62 M⊕), 84.9 (`TIC-271478281-04`), and 77.7 (`TIC-397362481-04`). All four are marked `in_main_discoveries_registry: true`. |
| TIC 271478281.05 at 93.9% | Confirmed as a stored score | Primary `overall_score_pct` is 93.9. The marked copy of the same object says 93.8. Seven of the eight table rows disagree between the two files. |
| a = 0.4438 AU | Confirmed as printed algebra | Record stores `m_star_msun` 0.74 and `period_days` 125.51444. `(0.74 × (125.51444 / 365.25636)²)^(1/3) = 0.44375287` AU, which rounds to 0.4438. The tex intermediate 0.343634 is `125.51444 / 365.25636` rounded from 0.34363382. The same sentence prints `R★ = 0.72 R☉`. The record stores `r_star_rsun` **0.691**. |
| 2,170 + 422 + 0 + 2,326 + 39 = 4,957 | Confirmed | Sum of per-record `ephemeris_audit.window_label_counts` equals the header ledger. Shares 43.78%, 8.51%, 0.00%, 46.92%, 0.79%. Status rollup is 843 verified worlds and 429 recalibrated worlds. |
| 100.0% precision | Qualified | `build_self_audit_ledger` sets precision to `100 × (1 − WRONG / (CORRECT + SHIFTED + WRONG))`. That denominator is 2,592, so the rate is 100.0% when `WRONG` is 0. On-time recovery is 2,170 / 4,957 = 43.78%. The tex states the 2,592-window definition after Table 3. The abstract and the folio KPI lead with 100.0%. |
| 1,261 marked objects | Confirmed | `len(marked_objects)` is 1,261. Recounted `bookmark_category` values match `summary_counts`: 339 + 496 + 6 + 107 + 301 + 12. |
| 20,480-byte arena, SHA-256 `c7237583…255ba5` | Confirmed | Hunter `registry\` and report `public-verifier\` copies are identical: 20,480 bytes, digest `c7237583ff3af261e0f1f3262dbe88c37e36d2ecdfff02a7a5bd3e6d00255ba5`. All 80 headers are magic `QEG5`, `dtype_code` 10, DRGFC degree in 0…6, bit budget in (0, 4096]. |

The public verifier was run in this review and exited 0. A green run is consistent with the script as written. It is not a confirmation of the discoveries.

## Holds

### 1. The eight table rows are packed inside the Hill-stability limit

Separations use the stellar and planet masses stored on the records, Keplerian `a` with the paper’s 365.25636-day year, and one mutual Hill radius

`R_H = ((a1+a2)/2) × ((m1+m2) / (3 M★))^(1/3)`

with `M⊕/M☉ = 3.0034893488507934×10⁻⁶`. Gladman’s circular coplanar limit is about 2√3 ≈ 3.46 mutual Hill radii. Every adjacent pair on these two stars is inside that limit.

TIC 283722336, `M★ = 0.80`, four two-epoch rows:

| Pair | Periods (d) | ΔP (d) | Separation |
|---|---|---|---|
| .03–.04 | 159.31632 / 160.30553 | 0.989 | 0.347 |
| .04–.05 | 160.30553 / 160.54828 | 0.243 | 0.084 |
| .05–.06 | 160.54828 / 162.90046 | 2.352 | 0.720 |

TIC 271478281, `M★ = 0.74`:

| Pair | Periods (d) | ΔP (d) | Separation |
|---|---|---|---|
| .06–.05 | 120.32215 / 125.51444 | 5.192 | 1.772 |
| .05–.03 | 125.51444 / 128.96973 | 3.455 | 1.082 |
| .03–.04 | 128.96973 / 130.32997 | 1.360 | 0.390 |

`.04` on TIC 271478281 is in the 845-world catalog at score 84.9. The folio’s closing paragraph asks for immediate EPRV and JWST follow-up of both stars as multi-planet perfect-Earth hosts. The arxiv tex does not make that request. These periods and masses describe crossing orbits. Publish each cluster as competing solutions, or keep a subset separated by at least ~3.5 mutual Hill radii.

The flagship record itself is a two-epoch candidate (sectors 67 and 94, combined SNR 9.85, depth 212.3 ppm). Its stored audit counts are 2 `CORRECT`, 0 `SHIFTED`, 1 `UNABLE TO VERIFY`. `passed_window_labels` on that record is empty, so this review could not replay the measurement that produced the `CORRECT` label.

### 2. `KX01`–`KX08` are law kernels, and two table rows break `KX02`

`EXOPLANET_PERFECT_EARTH_KERNELS_8` binds those ids to laws, beginning with `KX01_K_DWARF_GOLDILOCKS_RADIATION`. `KX02` says never to classify `R_p > 1.60 R⊕` or `M_p > 2.0 M⊕` as a perfect-Earth bullseye. Table 2 assigns `KX01` through `KX08` to the eight planets. `TIC-320847025-04` is stored at 2.10 M⊕ and `TIC-271478281-03` at 2.07 M⊕. Both fail the rocky-bulk pillar and remain in the ≥85% table. `TIC-193023697-05`, one of the four extra marked bullseyes, is stored at 1.72 R⊕ and 5.62 M⊕.

### 3. The 93.9% score is computed from pipeline formulas

`evaluate_perfect_earth_profile` scores a rubric. It does not read a measured rotation, obliquity, or surface temperature. For a K-dwarf world with `M★ ≥ 0.58`, `P` in [38, 260] days, and a long tidal-sync time, `compute_kinematics_rotation_and_wobble` sets

`rot_hours = round(24 × round(1.75 + 0.36 × phase_mod, 2), 1)`  
`tilt_deg = round(14.0 + 2.4 × sin(P × 0.31 + R_p), 1)`

with `phase_mod = ((P × 0.137 + M_p × 0.29) mod 1) − 0.5`. That formula returns the flagship’s stored 43.0 hours and 15.8 degrees. Surface temperature is `T_eq(A=0.25) × (288/255) − 273.15`. The flagship’s `teq_k_ab25` is 261.4 K, which returns the stored +22.1 °C.

The archipelago pillar still passes at 3.4% visual water coverage (shader copy 3.7%). The scorer’s alternate branch treats interior `h2o_volatile_ice_pct` of 2.7% as a pass. `KX06` says not to equate bulk water mass with surface ocean area. Six of the eight rows show 6/7 pillars. The flagship and `TIC-271478281-06` show 7/7. TESS photometry does not measure the rotation, tilt, or surface-temperature inputs.

Of the 845 radii, 64 lie in the abstract’s 0.75–1.48 R⊕ interval, and 44 of those also have `P > 60` d. The opening sentence describes an under-recovered class. The catalog that follows is mostly outside that class (radius range 0.88–12.14 R⊕).

### 4. The public verifier checks the receipt, a host-language identity, and a synthetic dip

`verify_chord_sieves_public_cartridge.py`, run here, printed all four gates and exited 0.

- Gate 1 matches the size, the SHA-256, and the 80 `QEG5` headers. That part checks the file.
- Gate 2 evaluates `|φ² − φ − 1|` on `(1+√5)/2` in Python, then checks that decoded 12-vertex norms are finite and positive. The identity does not come from the cartridge bytes.
- Gate 3 draws `np.random.default_rng(27147828105)`, subtracts 412 ppm inside the core mask, and asserts SNR ≥ 5.8. This run reported SNR 48.75. It does not open a FITS file, does not call `evaluate_chord_window`, and does not apply the odd/even, secondary, V-shape, or centroid gates named in the docstring. The kernel’s real window test uses core `|t| ≤ 0.40 D`, flanks `0.85 D ≤ |t| ≤ 2.2 D`, sigma `1.4826 × MAD`, and `SNR = depth × √N_core / sigma`. Those zones are in `chord_sieves_kernel.py`. The verifier reimplements a cousin of that formula on a line-spaced synthetic curve.
- Gate 4 asserts literals in the receipt, including `total_star_systems_indexed == 390` and `ephemeris_precision_rate_pct == 100.0`. It does not open `discoveries.json`. The semi-major-axis assert is `abs(a − 0.4437) < 1e-4`. The algebra is 0.44375 AU, so 0.4438 passes a comparison constant of 0.4437. The docstring also prints 0.4437 AU.

The receipt field `tic_271478281_05_keplerian_a_au` is 0.4438. The stored Lumen excerpt prints 0.3178 AU. The stored BBB excerpt prints 0.74 AU, which is the stellar mass left outside the one-third power. Gate 4 ignores both excerpts.

## Close condition

Revise the tex and `pdf-source.html`, then point Gate 4 at `discoveries.json`, before a second sign-off:

1. Relabel the crossing pairs as competing solutions, or drop every adjacent pair inside ~3.5 mutual Hill radii. Remove the immediate EPRV/JWST request for those pairs from the folio.
2. Print 386 hosts for the 845. Define 390 as the union with the four marked-only TIC ids above.
3. Count 8 worlds at ≥ 85% on `discoveries.json`. Remove the four marked-file labels whose primary scores are 77.7, 84.2, 84.4, and 84.9, or recompute those scores from the primary record before calling them bullseyes.
4. Replace the flagship stellar radius with 0.691, or cite the catalog row that says 0.72.
5. Lead the audit section with 2,170 / 4,957 on-time. Keep the 2,592-window zero-`WRONG` rate in the same sentence.
6. Remove `KX01`–`KX08` from the planet rows. State that surface temperature, rotation, obliquity, and the few-percent water coverage are pipeline fields. Apply `KX02`’s mass ceiling to the table.
7. Make the verifier fail when the unique `tic_id` count of the 845 is not the host count printed for that catalog. Name Gate 3 a synthetic formula replay. Evaluate any golden-ratio identity from the cell bytes.

## Signature

Independent recount by Grok on 2026-10-20. Arena digest checked on both binaries: `c7237583ff3af261e0f1f3262dbe88c37e36d2ecdfff02a7a5bd3e6d00255ba5`. Public verifier exit code 0, with the gate limits above. This verdict was not posted to the mesh.
