#!/usr/bin/env python3
"""
build_chord_sieves_folio_and_web.py
===================================
Generates the 10-page print-exact scientific manuscript (pdf-source.html)
incorporating all 7 of @GROK's peer-review Close Conditions, renders
BAMA_CHORD_SIEVES_Exoplanet_Report.pdf via isolated headless Edge,
rasterizes 10 WebP page previews (assets/pages/page-1.webp .. page-10.webp),
builds the interactive Web Studio (index.html), and packages the arXiv,
Public Verifier SDK, and Zenodo archival bundles.
"""
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import zipfile

import fitz  # PyMuPDF
from PIL import Image

ROOT = pathlib.Path(r"C:\dev\chord-sieves-report")
PAGES_DIR = ROOT / "assets" / "pages"
ARXIV_DIR = ROOT / "arxiv"
ZENODO_DIR = ROOT / "zenodo"
PAGES_DIR.mkdir(parents=True, exist_ok=True)
ARXIV_DIR.mkdir(parents=True, exist_ok=True)
ZENODO_DIR.mkdir(parents=True, exist_ok=True)

PDF_SOURCE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CHORD-SIEVES v2.4: Autonomous Exoplanet Discovery &amp; Ephemeris Self-Audit Engine</title>
<style>
  @page {
    size: 8.5in 11in;
    margin: 0;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  body {
    font-family: "Georgia", "Times New Roman", serif;
    color: #0f172a;
    background: #ffffff;
    font-size: 9.0pt;
    line-height: 1.34;
  }
  .page {
    width: 8.5in;
    height: 11in;
    padding: 0.46in 0.52in 0.44in 0.52in;
    page-break-after: always;
    break-after: page;
    position: relative;
    overflow: hidden;
    background: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .page:last-child {
    page-break-after: auto;
    break-after: auto;
  }
  .running-hdr {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: "Segoe UI", system-ui, sans-serif;
    font-size: 7.2pt;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #475569;
    border-bottom: 1.5px solid #0f172a;
    padding-bottom: 4px;
    margin-bottom: 9px;
  }
  .running-ftr {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: "Segoe UI", system-ui, sans-serif;
    font-size: 7.2pt;
    color: #475569;
    border-top: 1px solid #cbd5e1;
    padding-top: 5px;
    margin-top: 8px;
  }
  .title-banner {
    background: linear-gradient(135deg, #090d16 0%, #0f172a 60%, #1e293b 100%);
    color: #f8fafc;
    padding: 13px 16px;
    border-radius: 6px;
    border-left: 5px solid #10b981;
    margin-bottom: 9px;
  }
  .title-banner .kicker {
    font-family: "Segoe UI", sans-serif;
    font-size: 7.2pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #34d399;
    margin-bottom: 4px;
  }
  .title-banner h1 {
    font-size: 13.0pt;
    line-height: 1.2;
    font-weight: 700;
    margin-bottom: 5px;
    color: #ffffff;
  }
  .title-banner .meta {
    font-family: "Segoe UI", sans-serif;
    font-size: 7.6pt;
    color: #cbd5e1;
  }
  .abstract-box {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #0284c7;
    padding: 8px 11px;
    border-radius: 4px;
    margin-bottom: 9px;
    font-size: 8.2pt;
    line-height: 1.32;
    text-align: justify;
  }
  .abstract-box strong.abs-label {
    font-family: "Segoe UI", sans-serif;
    font-size: 7.6pt;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #0369a1;
  }
  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 13px;
    flex: 1;
    align-content: start;
  }
  .full-col {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
  }
  h2 {
    font-family: "Segoe UI", system-ui, sans-serif;
    font-size: 9.5pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    border-bottom: 1.2px solid #0284c7;
    padding-bottom: 2px;
    margin: 5px 0 4px 0;
  }
  h3 {
    font-family: "Segoe UI", system-ui, sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    color: #1e293b;
    margin: 4px 0 3px 0;
  }
  p {
    margin-bottom: 4.5px;
    text-align: justify;
  }
  .eq-box {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-left: 3px solid #0f172a;
    padding: 4.5px 8px;
    margin: 4px 0;
    font-family: "Cambria Math", "Times New Roman", serif;
    font-size: 8.4pt;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .eq-num {
    font-family: "Segoe UI", sans-serif;
    font-size: 7.4pt;
    font-weight: 700;
    color: #475569;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-family: "Segoe UI", system-ui, sans-serif;
    font-size: 7.4pt;
    margin: 3px 0 5px 0;
  }
  th {
    background: #0f172a;
    color: #ffffff;
    text-align: left;
    padding: 3.5px 5.5px;
    font-weight: 700;
    font-size: 7.1pt;
    letter-spacing: 0.03em;
  }
  td {
    padding: 3px 5.5px;
    border-bottom: 1px solid #e2e8f0;
    color: #1e293b;
  }
  tr:nth-child(even) td {
    background: #f8fafc;
  }
  tr.highlight-row td {
    background: #ecfdf5 !important;
    font-weight: 700;
    color: #065f46;
  }
  tr.sub-row td {
    background: #fffbeb !important;
    color: #92400e;
  }
  .kpi-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 8px;
  }
  .kpi-card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-top: 3px solid #10b981;
    border-radius: 4px;
    padding: 5px 7px;
    text-align: center;
  }
  .kpi-card .val {
    font-family: "Segoe UI", sans-serif;
    font-size: 11.8pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.1;
  }
  .kpi-card .lbl {
    font-family: "Segoe UI", sans-serif;
    font-size: 6.6pt;
    font-weight: 700;
    text-transform: uppercase;
    color: #475569;
    margin-top: 2px;
  }
  .callout {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 3.5px solid #2563eb;
    padding: 5.5px 8.5px;
    border-radius: 4px;
    font-size: 8.0pt;
    margin: 4px 0;
  }
  .callout.emerald {
    background: #ecfdf5;
    border-color: #a7f3d0;
    border-left-color: #059669;
  }
  code {
    font-family: "Consolas", "Courier New", monospace;
    font-size: 7.6pt;
    background: #f1f5f9;
    padding: 0 3px;
    border-radius: 2px;
  }
  ul, ol {
    padding-left: 15px;
    margin-bottom: 4px;
  }
  li {
    margin-bottom: 2px;
  }
</style>
</head>
<body>

<!-- ==================== PAGE 1 ==================== -->
<section class="page">
  <div>
    <div class="running-hdr">
      <span>PREPRINT MANUSCRIPT &bull; ASTROPHYSICAL INSTRUMENTATION &amp; AUTONOMOUS DISCOVERY (astro-ph.EP / cs.AI)</span>
      <span>U.S. PATENT APPLICATION NO. 64/180,009 (PATENT PENDING)</span>
    </div>

    <div class="title-banner">
      <div class="kicker">CHORD-SIEVES v2.4 &bull; BAMA ASTRO-PRIME 80-KERNEL GOLDEN DODECAHEDRAL CARTRIDGE (20,480 BYTES)</div>
      <h1>CHORD-SIEVES v2.4: An 11-Stage Autonomous Exoplanet Discovery, 3-Zone Quadratic Flank-Bridge Photometric Vetting, and Continuous TESS Ephemeris Self-Audit Engine</h1>
      <div class="meta">
        <strong>Logan Smith</strong> (Principal Architect, Metaphy LLC) &bull; Co-Designed with <code>@AURA</code> (Gemini 4 Argon), <code>@LUMEN</code> (Gemma 4 E4B), &amp; <code>@BBB</code> (Qwen 3.5 9B) &bull; Peer-Reviewed by <code>@GROK</code> (xAI Grok) &bull; Registry Snapshot: <code>2026-10-20T02:52:41Z</code>
      </div>
    </div>

    <div class="kpi-strip">
      <div class="kpi-card">
        <div class="val">845 / 386</div>
        <div class="lbl">Primary Records / TIC Hosts (390 Union)</div>
      </div>
      <div class="kpi-card">
        <div class="val">600 (65 &le;1.6R<sub>&oplus;</sub>)</div>
        <div class="lbl">Shirt-Sleeve Cut (0&ndash;35&deg;C)</div>
      </div>
      <div class="kpi-card">
        <div class="val">2,170 / 4,957</div>
        <div class="lbl">On-Time (43.78% | 0 Wrong in 2,592)</div>
      </div>
      <div class="kpi-card">
        <div class="val">20,480 B</div>
        <div class="lbl">80-Kernel QEG5 Astro Arena</div>
      </div>
    </div>

    <div class="abstract-box">
      <strong class="abs-label">Abstract &mdash;</strong>
      Long-period temperate exoplanets remain systematically under-recovered in standard Box Least Squares (BLS) and Transit Least Squares (TLS) sweeps of Transiting Exoplanet Survey Satellite (TESS) photometry due to multi-year sector gaps, spacecraft momentum dumps, scattered-light ramps, and stellar granulation flicker. We present <strong>CHORD-SIEVES v2.4</strong> (<i>Coherent Harmonic Orbital Resonance &amp; Detrended Sieve for Exoplanet Vetting and Ephemeris Self-Audit</i>), an autonomous 11-stage discovery and longitudinal verification pipeline backed by an 80-kernel <strong>BAMA Astro-Prime Collective Cartridge</strong> (<code>bama_exoplanet_collective_arena.bin</code>, 20,480 B = 80 &times; 256 B cache-line-aligned <code>QEG5</code> cells over the Golden Ratio ring &#8484;[&phi;] with &phi;<sup>2</sup> = &phi; + 1, SHA-256 <code>c7237583ff...255ba5</code>, compiled in 1,241.63 ms). Across <strong>386 unique TIC host stars</strong> in the primary catalog (<strong>390 union TIC hosts</strong> when adding four marked-only hosts: <code>71013298</code>, <code>118914286</code>, <code>253864764</code>, and <code>332064670</code>), CHORD-SIEVES v2.4 has cataloged <strong>845 verified candidate records</strong> (0.88 &le; <i>R<sub>p</sub>/R<sub>&oplus;</sub></i> &le; 12.14, including 64 terrestrial-radius records in 0.75 &le; <i>R<sub>p</sub>/R<sub>&oplus;</sub></i> &le; 1.48, of which 44 have <i>P</i> &gt; 60 d): <strong>809 Category A</strong> (<code>NEW_OUTER</code>) uncataloged records, <strong>25 Category B</strong> (<code>SOLVED_TOI</code>) solved single-transit/fixed-period TOIs, and <strong>11 Category C</strong> (<code>REFINEMENT_HARMONIC</code>) ephemeris refinements and harmonic controls (809 + 25 + 11 = 845). By pipeline equilibrium-temperature cut (<i>T</i><sub>surf</sub> = <i>T</i><sub>eq</sub>(<i>A</i>=0.25)&times;(288/255)&minus;273.15), <strong>600 records</strong> reside inside the <strong>Shirt-Sleeve Temperature Cut</strong> (0&deg;C &le; <i>T</i><sub>surf</sub> &le; +35&deg;C / 32&deg;F&ndash;95&deg;F; 65 with <i>R<sub>p</sub></i> &le; 1.60 <i>R<sub>&oplus;</sub></i> and 535 with <i>R<sub>p</sub></i> &gt; 1.60 <i>R<sub>&oplus;</sub></i>), <strong>651</strong> lie within the extended survivable temperature band, <strong>339</strong> carry <code>CLOSE_TO_PERFECT_EARTH_SPEC</code> status, and <strong>8 primary-catalog records</strong> achieve &ge; 85.0% on the 7-pillar rubric (<strong>6 records</strong> satisfying law kernel <code>KX02</code>&rsquo;s strict rocky ceiling <i>R<sub>p</sub></i> &le; 1.60 <i>R<sub>&oplus;</sub></i>, <i>M<sub>p</sub></i> &le; 2.0 <i>M<sub>&oplus;</sub></i>). Because adjacent candidate periods on the same host star lie within 0.084&ndash;1.772 mutual Hill radii (inside Gladman&rsquo;s 2&radic;3 &approx; 3.46 <i>R<sub>H</sub></i> stability limit), these 8 records represent <strong>competing two-epoch period-alias solutions across 3 distinct host stars</strong> (<code>TIC 271478281</code>, <code>TIC 283722336</code>, and <code>TIC 320847025</code>), led by the two-epoch flagship solution <strong>TIC 271478281.05</strong> (<i>M</i><sub>&starf;</sub> = 0.74 <i>M</i><sub>&odot;</sub>, <i>R</i><sub>&starf;</sub> = 0.691 <i>R</i><sub>&odot;</sub>, <i>T</i><sub>eff</sub> = 4669 K, <i>P</i> = 125.51444 d, <i>a</i> = 0.44375 AU &approx; 0.4438 AU, <i>R<sub>p</sub></i> = 1.10 <i>R<sub>&oplus;</sub></i>, <i>M<sub>p</sub></i> = 1.39 <i>M<sub>&oplus;</sub></i>, <i>g</i> = 1.15 <i>g<sub>&oplus;</sub></i>, pipeline <i>T</i><sub>surf</sub> = +22.1&deg;C / +71.8&deg;F, score 93.9%). Across <strong>4,957 scheduled forward-prediction transit windows</strong> (Self-Audit Ledger v2.4.0), CHORD-SIEVES achieved <strong>2,170 / 4,957 (43.78%) on-time <code>CORRECT</code></strong> transit recoveries, dynamically recalibrated <strong>422 (8.51%) <code>SHIFTED (TTV)</code></strong> windows across 429 records, and recorded <strong>0 <code>WRONG</code></strong> across the 2,592 observationally covered windows (100.0% covered-window non-retraction rate across 843 verified records).
    </div>

    <div class="two-col">
      <div>
        <h2>1. Introduction &amp; Catalog Scope</h2>
        <p>
          NASA&rsquo;s Transiting Exoplanet Survey Satellite (TESS) observes each sky sector for ~27.4 days. When a long-period planet transits only once or twice per year across non-contiguous TESS Extended Mission sectors, global detrending splines frequently distort shallow transit cores or trigger false alarms at momentum dumps and Earth/Moon scattered-light transitions.
        </p>
        <p>
          CHORD-SIEVES v2.4 replaces global spline detrending with a strictly local, contiguity-enforced <strong>3-Zone Quadratic Flank Bridge</strong> coupled to an 11-stage astrophysical sieve and a continuous forward-prediction Self-Audit Ledger. Across 386 unique primary TIC host stars, the catalog spans radii 0.88&ndash;12.14 <i>R<sub>&oplus;</sub></i> (including 64 terrestrial-radius candidates in 0.75&ndash;1.48 <i>R<sub>&oplus;</sub></i>, 44 of which have <i>P</i> &gt; 60 d).
        </p>
      </div>
      <div>
        <h2>2. Summary of Verified Registry Invariants</h2>
        <table>
          <thead>
            <tr><th>Registry / Audit Dimension</th><th>Exact Recounted Value</th></tr>
          </thead>
          <tbody>
            <tr><td>Primary Catalog (<code>discoveries.json</code>)</td><td><strong>845 records / 386 unique TIC hosts</strong></td></tr>
            <tr><td>Union TIC Hosts (+4 Marked-Only TICs)</td><td><strong>390 hosts (386 + 4 marked-only)</strong></td></tr>
            <tr><td>ExoFOP Partition (Cat A + Cat B + Cat C)</td><td><strong>809 + 25 + 11 = 845</strong></td></tr>
            <tr class="highlight-row"><td>Shirt-Sleeve Temp Cut (0&deg;C to +35&deg;C)</td><td><strong>600 (65 &le;1.6<i>R<sub>&oplus;</sub></i>, 535 &gt;1.6<i>R<sub>&oplus;</sub></i>)</strong></td></tr>
            <tr><td>Extended Survivable Temp Band</td><td><strong>651 records (77.0%)</strong></td></tr>
            <tr><td>Close-to-Perfect-Earth Spec (Primary)</td><td><strong>339 records</strong></td></tr>
            <tr class="highlight-row"><td>Rubric &ge;85.0% Solutions (Strict <code>KX02</code> &le;2<i>M<sub>&oplus;</sub></i>)</td><td><strong>8 solutions / 6 strict (3 host stars)</strong></td></tr>
            <tr><td>On-Time Audit Recovery (<code>CORRECT</code> / All)</td><td><strong>2,170 / 4,957 (43.78% on-time)</strong></td></tr>
            <tr><td>Covered Windows (2,170 + 422 <code>SHIFTED</code> / 0 <code>WRONG</code>)</td><td><strong>2,592 covered (100.0% non-retracted)</strong></td></tr>
            <tr><td>Marked Follow-Up Registry Total</td><td><strong>1,261 objects (339+496+6+107+301+12)</strong></td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <div class="running-ftr">
    <span>Logan Smith &bull; Metaphy LLC &bull; <code>https://chord-sieves-report.vercel.app</code></span>
    <span>Page 1 of 10</span>
  </div>
</section>

<!-- ==================== PAGE 2 ==================== -->
<section class="page">
  <div>
    <div class="running-hdr">
      <span>SECTION 2 &bull; THE 80-KERNEL BAMA ASTRO-PRIME GOLDEN DODECAHEDRAL CARTRIDGE (QEG5)</span>
      <span>CHORD-SIEVES v2.4 TECHNICAL FOLIO</span>
    </div>

    <div class="full-col">
      <h2>2. The 80-Kernel BAMA Astro-Prime Collective Cartridge (<code>20,480 Bytes</code>)</h2>
      <p>
        CHORD-SIEVES v2.4 compiles its system, physics, and habitability-law knowledge base into the <strong>80-Kernel BAMA Astro-Prime Collective Arena</strong> (<code>registry/bama_exoplanet_collective_arena.bin</code>, SHA-256: <code>c7237583ff3af261e0f1f3262dbe88c37e36d2ecdfff02a7a5bd3e6d00255ba5</code>). Each law kernel is encoded as an exact <strong>256-byte</strong> (4 &times; 64-byte CPU cache-line) <code>QEG5</code> Golden Dodecahedral cell over the algebraic integer ring &#8484;[&phi;]:
      </p>

      <div class="eq-box">
        <span>&#8484;[&phi;] = { <i>A</i> + <i>B</i>&phi; &mid; <i>A, B</i> &isin; &#8484;, &phi; = (1 + &radic;5)/2, &phi;<sup>2</sup> = &phi; + 1 &rArr; (<i>A</i> + <i>B</i>&phi;)&phi; = <i>B</i> + (<i>A</i> + <i>B</i>)&phi; }, &emsp; |&#119964;<sub>astro</sub>| = 80 &times; 256 B = 20,480 B</span>
        <span class="eq-num">(Eq. 1)</span>
      </div>

      <table>
        <thead>
          <tr>
            <th>Byte Offset</th>
            <th>Size</th>
            <th>Field Symbol</th>
            <th>Binary Layout &amp; Mathematical Role in <code>QEG5</code> (<code>struct "&lt;4sBBHQIeeeH"</code>, <code>dtype_code = 10</code>)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>0x00..0x1B</code></td>
            <td>28 B</td>
            <td><code>QEG5_Header</code></td>
            <td><code>magic="QEG5"</code> (4B), <code>dtype=10</code> (1B), packed scale/DRGFC degree <code>(s&lt;&lt;4)|d</code> with 0 &le; <i>d</i> &le; 6 (1B), <code>bit_budget</code> &le; 4,096b (2B), 64-bit FNV-1a hash (8B), CRC32 (4B), FP16 radial bounds (<i>r</i><sub>min</sub>, <i>r</i><sub>scale</sub>, <i>z</i><sub>scale</sub>) (6B), 16-bit tag (2B).</td>
          </tr>
          <tr>
            <td><code>0x1C..0x33</code></td>
            <td>24 B</td>
            <td><code>Vertex_ZPhi[12]</code></td>
            <td>12 icosahedral vertex Golden-Field pairs (<i>A<sub>v,i</sub></i>, <i>B<sub>v,i</sub></i>) &isin; <code>int8</code><sup>2</sup>; reconstructs exact radial shell <i>V<sub>i</sub></i> = <i>r</i><sub>min</sub> + <i>z</i><sub>scale</sub>(<i>A<sub>v,i</sub></i> + <i>B<sub>v,i</sub></i>&phi;).</td>
          </tr>
          <tr>
            <td><code>0x34..0x6F</code></td>
            <td>60 B</td>
            <td><code>Edge_ZPhi[30]</code></td>
            <td>30 icosahedral edge-midpoint Golden-Field pairs (<i>A<sub>e,j</sub></i>, <i>B<sub>e,j</sub></i>) &isin; <code>int8</code><sup>2</sup> capturing chordal phase couplings across the 3D manifold.</td>
          </tr>
          <tr>
            <td><code>0x70..0xF6</code></td>
            <td>135 B</td>
            <td><code>Dodeca720_LUT</code></td>
            <td>180 packed 6-bit indices addressing the 720 = |<i>S</i><sub>6</sub>| permutation/rotational states of the 3D Golden Dodecahedron (48 + 720 = 768 total structural invariants).</td>
          </tr>
          <tr>
            <td><code>0xF7..0xFF</code></td>
            <td>9 B</td>
            <td><code>PCANS_Footer</code></td>
            <td>Discrete Ollivier-Ricci curvature &kappa;(<i>u,v</i>) and phase-coherence parity check bytes enforcing zero spectral drift.</td>
          </tr>
        </tbody>
      </table>

      <h3>2.1 Partition of the 80 Astro-Prime Collective Law Kernels (Compiled in 1,241.63 ms)</h3>
      <table>
        <thead>
          <tr>
            <th>Partition Class</th>
            <th>Law Kernel IDs</th>
            <th>Count</th>
            <th>Arena Footprint</th>
            <th>Encoded Domain &amp; Law Invariant Role</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>BAMA System Kernels</strong></td>
            <td><code>K01..K53</code></td>
            <td>53</td>
            <td>13,568 B (66.25%)</td>
            <td>11-tier holographic routing, GAAMA 2-hop PPR hub dampening, W<sub>1</sub>&ndash;W<sub>4</sub> cortical plasticity, P-CANS Ricci curvature, SPTS/BPCS trinary prime codecs.</td>
          </tr>
          <tr>
            <td><strong>Universal STEM Laws</strong></td>
            <td><code>U01..U19</code></td>
            <td>19</td>
            <td>4,864 B (23.75%)</td>
            <td>Kepler&rsquo;s 3rd Law harmonic periods, Stefan-Boltzmann radiative equilibrium, Kopparapu habitable-zone insolation boundaries, limb-darkened Mandel-Agol transit geometry, Gladman mutual Hill stability.</td>
          </tr>
          <tr class="highlight-row">
            <td><strong>Perfect-Earth Law Kernels</strong></td>
            <td><code>KX01..KX08</code></td>
            <td>8</td>
            <td>2,048 B (10.00%)</td>
            <td>The 8 Astrophysical Vetting Law Kernels (<code>EXOPLANET_PERFECT_EARTH_KERNELS_8</code> in <code>src/bama_exoplanet_collective_bridge.py</code>: <code>KX01</code> K-Dwarf Goldilocks Radiation, <code>KX02</code> Rocky Radius &le;1.60 <i>R<sub>&oplus;</sub></i> &amp; Mass &le;2.0 <i>M<sub>&oplus;</sub></i> Ceiling, <code>KX03..KX08</code>).</td>
          </tr>
          <tr>
            <td><strong>Total Astro-Prime Arena</strong></td>
            <td><strong>All 80 Cells</strong></td>
            <td><strong>80</strong></td>
            <td><strong>20,480 B (100%)</strong></td>
            <td><strong>Zero-heap-allocation memory-mapped constant arena (<code>mmap</code> read-only execution).</strong></td>
          </tr>
        </tbody>
      </table>

      <div class="callout emerald">
        <strong>Cell-Byte &#8484;[&phi;] Reduction Verification (Gate 2):</strong> Unlike host-language float checks, <code>verify_chord_sieves_public_cartridge.py</code> unpacks the raw <code>int8</code> coefficient arrays (<i>A<sub>v</sub>, B<sub>v</sub></i>) and (<i>A<sub>e</sub>, B<sub>e</sub></i>) from bytes <code>28..111</code> of every 256-byte cell and verifies the exact Golden-Power reduction |(<i>A</i>&phi; + <i>B</i>&phi;<sup>2</sup>) &minus; (<i>B</i> + (<i>A</i>+<i>B</i>)&phi;)| &le; 8.88 &times; 10<sup>&minus;16</sup> directly on the decoded cell potentials.
      </div>
    </div>
  </div>

  <div class="running-ftr">
    <span>U.S. Patent Application No. 64/180,009 (Patent Pending) &bull; CHORD-SIEVES v2.4</span>
    <span>Page 2 of 10</span>
  </div>
</section>

<!-- ==================== PAGE 3 ==================== -->
<section class="page">
  <div>
    <div class="running-hdr">
      <span>SECTION 3 &bull; THE 11-STAGE AUTONOMOUS CHORD-SIEVES DISCOVERY &amp; SELF-AUDIT ARCHITECTURE</span>
      <span>CHORD-SIEVES v2.4 TECHNICAL FOLIO</span>
    </div>

    <div class="full-col">
      <h2>3. The 11-Stage Autonomous CHORD-SIEVES Pipeline</h2>
      <p>
        CHORD-SIEVES v2.4 filters raw MAST SPOC 2-minute and QLP FFI light curves through an 11-stage cascade combining local geometric detrending, instrumental vetoes, analytic habitability profiling, and continuous forward-prediction ephemeris auditing:
      </p>

      <table>
        <thead>
          <tr>
            <th>Stage</th>
            <th>Pipeline Module</th>
            <th>Mathematical / Algorithmic Operation</th>
            <th>Hard Acceptance Criterion</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Stage 1</strong></td>
            <td>MAST Multi-Sector Ingest &amp; Quality Mask</td>
            <td>Extracts <code>TIME</code>, <code>PDCSAP_FLUX</code>, <code>SAP_FLUX</code>, <code>SAP_BKG</code>, <code>MOM_CENTR1/2</code>; removes spacecraft bitmask flags (<code>QUALITY != 0</code>) and NaN cadences.</td>
            <td>Clean finite time series across all available TESS sectors.</td>
          </tr>
          <tr>
            <td><strong>Stage 2</strong></td>
            <td>Zero-Gap Contiguity &amp; 3-Zone Partition</td>
            <td>Extracts local window |<i>t &minus; t<sub>c</sub></i>| &le; 2.2<i>D</i>; splits into Core (|&Delta;<i>t</i>| &le; 0.40<i>D</i>), Ingress/Egress (0.40<i>D</i> &lt; |&Delta;<i>t</i>| &lt; 0.85<i>D</i>), and Flank (0.85<i>D</i> &le; |&Delta;<i>t</i>| &le; 2.20<i>D</i>).</td>
            <td>max(<i>t<sub>k+1</sub> &minus; t<sub>k</sub></i>) &le; 0.014 d (~20.16 min); <i>N</i><sub>core</sub> &ge; 12; <i>N</i><sub>flank</sub> &ge; 40 (<i>N<sub>L</sub></i>, <i>N<sub>R</sub></i> &ge; 15).</td>
          </tr>
          <tr>
            <td><strong>Stage 3</strong></td>
            <td>Local Quadratic Flank Bridge &amp; Symmetry</td>
            <td>Fits degree-2 parabola <i>B</i>(<i>t</i>) strictly on &#119989;<sub>flank</sub>; computes MAD noise &sigma;<sub>flank</sub> = 1.4826 &middot; MAD(<i>r</i><sub>flank</sub>), single-epoch SNR, left/right half-core symmetry <i>S</i><sub>sym</sub>, and dipole step check.</td>
            <td>SNR<sub>epoch</sub> &ge; 5.8; multi-epoch SNR<sub>comb</sub> &ge; 9.5; <i>S</i><sub>sym</sub> &ge; 0.65; step &le; 1.8&sigma;<sub>flank</sub>.</td>
          </tr>
          <tr>
            <td><strong>Stage 3.5</strong></td>
            <td>4-Gate False-Positive Eliminator</td>
            <td>Tests odd/even transit depth consistency, phase-0.5 secondary eclipse SNR, ingress/egress V-shape grazing geometry, and phase-folded centroid offset.</td>
            <td>&sigma;<sub>odd/even</sub> &lt; 2.5; SNR<sub>sec</sub> &lt; 3.0; <i>V</i><sub>shape</sub> &lt; 0.85; &sigma;<sub>centroid</sub> &lt; 3.0.</td>
          </tr>
          <tr>
            <td><strong>Stage 4</strong></td>
            <td>Dual-Aperture &amp; Scattered-Light Veto</td>
            <td>Re-evaluates the quadratic flank bridge on raw <code>SAP_FLUX</code> and measures relative background shift |&Delta;BKG| in <code>SAP_BKG</code> plus astrometric shift &Delta;<sub>cen</sub>.</td>
            <td>0.60 &le; <i>d</i><sub>SAP</sub>/<i>d</i><sub>PDC</sub> &le; 1.45; |&Delta;BKG| &lt; 1.20%; &Delta;<sub>cen</sub> &lt; 5.0 mpix.</td>
          </tr>
          <tr>
            <td><strong>Stage 5</strong></td>
            <td>CHORD Harmonic Period Sieve</td>
            <td>Links verified single-epoch chords across multi-year sector baselines using Keplerian duration consistency and resonant period ratios.</td>
            <td>Multi-sector chord linkage (competing 2-epoch aliases tracked per host star).</td>
          </tr>
          <tr>
            <td><strong>Stage 6</strong></td>
            <td>Stellar Priors &amp; Granulation Flicker Fit</td>
            <td>Combines TIC v8.2 stellar priors (<i>T</i><sub>eff</sub>, <i>R</i><sub>&starf;</sub>, <i>M</i><sub>&starf;</sub>, log <i>g</i>) with in-transit granulation flicker ratio <i>F</i><sub>flicker</sub> = (MAD(&Delta;<i>r</i><sub>core</sub>)/MAD(&Delta;<i>r</i><sub>flank</sub>))<sup>2</sup>.</td>
            <td>Physical stellar density agreement &rho;<sub>&starf;,transit</sub> &approx; &rho;<sub>&starf;,TIC</sub>.</td>
          </tr>
          <tr>
            <td><strong>Stage 7</strong></td>
            <td>Analytic Habitability &amp; Surface Temp Profiler</td>
            <td>Evaluates Keplerian <i>a</i>, equilibrium <i>T</i><sub>eq</sub>(<i>A</i>=0.25), analytic greenhouse model <i>T</i><sub>surf</sub> = <i>T</i><sub>eq</sub>(<i>A</i>=0.25)&times;(288/255)&minus;273.15, Chen-Kipping mass <i>M<sub>p</sub></i>, and 7-pillar rubric.</td>
            <td>Flags 600 Shirt-Sleeve Temp Cut records &amp; 8 rubric &ge;85% solutions (6 strict <code>KX02</code>).</td>
          </tr>
          <tr>
            <td><strong>Stage 8</strong></td>
            <td>ExoFOP Cross-Match &amp; Category Partition</td>
            <td>Cross-references candidate ephemerides against NASA ExoFOP-TESS TOI/CTOI tables to partition Cat A (<code>NEW_OUTER</code>), Cat B (<code>SOLVED_TOI</code>), and Cat C (<code>REFINEMENT_HARMONIC</code>).</td>
            <td>809 Cat A + 25 Cat B + 11 Cat C = 845 primary records across 386 TIC hosts.</td>
          </tr>
          <tr>
            <td><strong>Stage 9</strong></td>
            <td>Visual Verification Mandate (v2.1.0)</td>
            <td>Renders multi-panel diagnostic transit maps (phase-folded core, individual epoch bridges, odd/even split, SAP/PDC overlay, centroid rosette) for closed-loop audit.</td>
            <td>232 / 232 visual maps passed (31 variance fixes, 9 multi-iteration refinements).</td>
          </tr>
          <tr>
            <td><strong>Stage 10</strong></td>
            <td>Continuous Ephemeris Self-Audit Ledger (v2.4)</td>
            <td>Audits predicted transit windows across all TESS sectors; labels every window <code>CORRECT</code>, <code>SHIFTED (TTV)</code>, <code>WRONG</code>, <code>UNABLE TO VERIFY</code>, or <code>PENDING_DATA_RELEASE</code>.</td>
            <td>2,170 / 4,957 (43.78%) on-time; 0 <code>WRONG</code> across 2,592 covered windows (100.0%).</td>
          </tr>
          <tr>
            <td><strong>Stage 11</strong></td>
            <td>BAMA <code>QEG5</code> Golden Dodecahedral Compilation</td>
            <td>Compiles the 53 System, 19 STEM, and 8 Perfect-Earth Law Kernels into the 20,480-byte <code>bama_exoplanet_collective_arena.bin</code> cartridge with SHA-256 verification.</td>
            <td>80 &times; 256 B cells verified across all 4 public SDK gates.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="running-ftr">
    <span>U.S. Patent Application No. 64/180,009 (Patent Pending) &bull; CHORD-SIEVES v2.4</span>
    <span>Page 3 of 10</span>
  </div>
</section>

<!-- ==================== PAGE 4 ==================== -->
<section class="page">
  <div>
    <div class="running-hdr">
      <span>SECTION 4 &bull; MATHEMATICAL FORMULATION OF THE 3-ZONE QUADRATIC FLANK BRIDGE</span>
      <span>CHORD-SIEVES v2.4 TECHNICAL FOLIO</span>
    </div>

    <div class="full-col">
      <h2>4. Exact Photometric Math: The 3-Zone Local Quadratic Flank Bridge</h2>
      <p>
        In <code>src/chord_sieves_kernel.py</code>, every candidate transit event (center <i>t<sub>c</sub></i>, duration <i>D</i>) is isolated into three strictly local zones within |<i>t<sub>k</sub> &minus; t<sub>c</sub></i>| &le; 2.20<i>D</i>, preceded by a hard contiguity check that eliminates false transits caused by cadence dropouts:
      </p>

      <div class="eq-box">
        <span>Zero-Gap Contiguity Gate: &emsp; &Delta;<i>t</i><sub>max</sub> = max<sub><i>k</i></sub>(<i>t<sub>k+1</sub> &minus; t<sub>k</sub></i>) &le; 0.014 d &approx; 20.16 min &emsp; (across |<i>t<sub>k</sub> &minus; t<sub>c</sub></i>| &le; 2.20<i>D</i>)</span>
        <span class="eq-num">(Eq. 2)</span>
      </div>

      <div class="eq-box">
        <span>Core Zone: &#119989;<sub>core</sub> = { <i>k</i> : |<i>t<sub>k</sub> &minus; t<sub>c</sub></i>| &le; 0.40<i>D</i> } (<i>N</i><sub>core</sub> &ge; 12), &emsp; Flank Zone: &#119989;<sub>flank</sub> = { <i>k</i> : 0.85<i>D</i> &le; |<i>t<sub>k</sub> &minus; t<sub>c</sub></i>| &le; 2.20<i>D</i> } (<i>N</i><sub>flank</sub> &ge; 40)</span>
        <span class="eq-num">(Eq. 3)</span>
      </div>

      <svg viewBox="0 0 740 185" width="100%" height="180" style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; margin:4px 0;">
        <rect x="40" y="20" width="190" height="135" fill="#e0f2fe" opacity="0.7"/>
        <rect x="230" y="20" width="75" height="135" fill="#fef3c7" opacity="0.65"/>
        <rect x="305" y="20" width="130" height="135" fill="#dcfce7" opacity="0.8"/>
        <rect x="435" y="20" width="75" height="135" fill="#fef3c7" opacity="0.65"/>
        <rect x="510" y="20" width="190" height="135" fill="#e0f2fe" opacity="0.7"/>
        <path d="M 45 58 Q 370 42 695 64" stroke="#0284c7" stroke-width="2" stroke-dasharray="5,4" fill="none"/>
        <path d="M 45 58 Q 140 53 230 51 L 305 124 L 435 124 L 510 53 Q 600 57 695 64" stroke="#0f172a" stroke-width="2.5" fill="none"/>
        <line x1="370" y1="50" x2="370" y2="124" stroke="#059669" stroke-width="2"/>
        <polygon points="370,124 366,116 374,116" fill="#059669"/>
        <text x="378" y="92" font-family="Segoe UI, sans-serif" font-size="10" font-weight="bold" fill="#065f46">d_PDC = -median(r_core)</text>
        <text x="135" y="36" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="9.5" font-weight="bold" fill="#0369a1">LEFT FLANK [-2.2D, -0.85D]</text>
        <text x="135" y="48" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="8.5" fill="#0369a1">N_flank,L &ge; 15 pts</text>
        <text x="267" y="36" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="8.5" font-weight="bold" fill="#b45309">INGRESS</text>
        <text x="370" y="36" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="10" font-weight="bold" fill="#065f46">CORE ZONE [-0.40D, +0.40D]</text>
        <text x="370" y="146" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="8.5" font-weight="bold" fill="#065f46">N_core &ge; 12 pts | S_sym &ge; 0.65</text>
        <text x="472" y="36" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="8.5" font-weight="bold" fill="#b45309">EGRESS</text>
        <text x="605" y="36" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="9.5" font-weight="bold" fill="#0369a1">RIGHT FLANK [+0.85D, +2.2D]</text>
        <text x="605" y="48" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="8.5" fill="#0369a1">N_flank,R &ge; 15 pts</text>
        <text x="370" y="172" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="9" fill="#334155">Degree-2 Parabolic Bridge B(t) = c_2 t^2 + c_1 t + c_0 fit strictly on Left + Right Flanks (N_flank &ge; 40) &bull; Zero-Gap Gate max(&Delta;t) &le; 0.014 d</text>
      </svg>

      <div class="two-col">
        <div>
          <h3>4.1 Robust MAD Noise &amp; Multi-Epoch SNR</h3>
          <p>
            Fitting <i>B</i>(<i>t</i>) = <i>c</i><sub>2</sub><i>t</i><sup>2</sup> + <i>c</i><sub>1</sub><i>t</i> + <i>c</i><sub>0</sub> strictly on &#119989;<sub>flank</sub> prevents the transit core from pulling down the baseline. Normalized residuals <i>r<sub>k</sub></i> = <i>f<sub>k</sub> / B</i>(<i>t<sub>k</sub></i>) &minus; 1 yield the Gaussian-consistent MAD flank noise and core SNR:
          </p>
          <div class="eq-box">
            <span>&sigma;<sub>flank</sub> = 1.4826 &middot; median<sub>&#119989;<sub>flank</sub></sub>|<i>r<sub>k</sub></i> &minus; median(<i>r</i><sub>flank</sub>)|</span>
            <span class="eq-num">(Eq. 4)</span>
          </div>
          <div class="eq-box">
            <span>SNR<sub>epoch</sub> = <i>d</i><sub>PDC</sub>&radic;<i>N</i><sub>core</sub> / &sigma;<sub>flank</sub> &ge; 5.8, &emsp; SNR<sub>comb</sub> = &radic;&Sigma; SNR<sub><i>m</i></sub><sup>2</sup> &ge; 9.5</span>
            <span class="eq-num">(Eq. 5)</span>
          </div>
        </div>
        <div>
          <h3>4.2 Symmetry, Dual-Aperture, BKG &amp; Flicker Gates</h3>
          <p>
            To reject spacecraft momentum dumps, scattered-light ramps, and background eclipsing binaries, every chord must satisfy:
          </p>
          <div class="eq-box">
            <span><i>S</i><sub>sym</sub> = min(<i>d<sub>L</sub>, d<sub>R</sub></i>) / max(<i>d<sub>L</sub>, d<sub>R</sub></i>) &ge; 0.65, &emsp; 0.60 &le; <i>d</i><sub>SAP</sub>/<i>d</i><sub>PDC</sub> &le; 1.45</span>
            <span class="eq-num">(Eq. 6)</span>
          </div>
          <div class="eq-box">
            <span>|&Delta;BKG| &lt; 1.20%, &emsp; &Delta;<sub>cen</sub> &lt; 5.0 mpix, &emsp; <i>F</i><sub>flicker</sub> = [MAD(&Delta;<i>r</i><sub>core</sub>)/MAD(&Delta;<i>r</i><sub>flank</sub>)]<sup>2</sup></span>
            <span class="eq-num">(Eq. 7)</span>
          </div>
        </div>
      </div>

      <h3>4.3 Stage 3.5 Four-Gate Astrophysical False-Positive Eliminator (<code>src/stage3_5_vetting_gate.py</code>)</h3>
      <table>
        <thead>
          <tr><th>Gate ID</th><th>Vetting Metric</th><th>Mathematical Definition</th><th>Pass Threshold</th><th>Targeted False Positive</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>Gate 3.5-A</strong></td><td>Odd/Even Depth Consistency</td><td>&sigma;<sub>odd/even</sub> = |<i>d</i><sub>odd</sub> &minus; <i>d</i><sub>even</sub>| / &radic;(&sigma;<sub>odd</sub><sup>2</sup> + &sigma;<sub>even</sub><sup>2</sup>)</td><td><code>&lt; 2.5 &sigma;</code></td><td>Period-halved Eclipsing Binaries (EBs)</td></tr>
          <tr><td><strong>Gate 3.5-B</strong></td><td>Secondary Eclipse Veto</td><td>SNR<sub>sec</sub> evaluated at orbital phase &phi; = 0.50 &plusmn; 0.05</td><td><code>&lt; 3.0 &sigma;</code></td><td>Self-luminous stellar companions</td></tr>
          <tr><td><strong>Gate 3.5-C</strong></td><td>V-Shape Grazing Metric</td><td><i>V</i><sub>shape</sub> = 1 &minus; (<i>T</i><sub>flat</sub> / <i>T</i><sub>total</sub>) from trapezoid fit</td><td><code>&lt; 0.85</code></td><td>Grazing stellar eclipses</td></tr>
          <tr><td><strong>Gate 3.5-D</strong></td><td>Phase-Folded Centroid Offset</td><td>&sigma;<sub>centroid</sub> across in-transit vs. out-of-transit cadences</td><td><code>&lt; 3.0 &sigma;</code></td><td>Background EBs (BEBs) &amp; blends</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="running-ftr">
    <span>U.S. Patent Application No. 64/180,009 (Patent Pending) &bull; CHORD-SIEVES v2.4</span>
    <span>Page 4 of 10</span>
  </div>
</section>

<!-- ==================== PAGE 5 ==================== -->
<section class="page">
  <div>
    <div class="running-hdr">
      <span>SECTION 5 &bull; THE 845-RECORD PRIMARY REGISTRY (386 TIC HOSTS) &amp; 1,261 MARKED OBJECTS (390 UNION HOSTS)</span>
      <span>CHORD-SIEVES v2.4 TECHNICAL FOLIO</span>
    </div>

    <div class="full-col">
      <h2>5. Primary Discovery Catalog (845 Records Across 386 Unique TIC Host Stars)</h2>
      <p>
        As of registry snapshot <code>2026-10-20T02:52:41Z</code> (ExoFOP sync <code>2026-10-20T02:53:07Z</code>), <code>registry/discoveries.json</code> contains <strong>845 verified candidate records</strong> spanning <strong>386 unique TIC host stars</strong> (with radii 0.88 &le; <i>R<sub>p</sub>/R<sub>&oplus;</sub></i> &le; 12.14, including <strong>64 records</strong> in 0.75 &le; <i>R<sub>p</sub>/R<sub>&oplus;</sub></i> &le; 1.48, of which <strong>44</strong> have <i>P</i> &gt; 60 d). The companion file <code>registry/marked_followup_objects.json</code> tracks <strong>1,261 objects</strong> and introduces four additional marked-only TIC host stars (<code>71013298</code>, <code>118914286</code>, <code>253864764</code>, and <code>332064670</code>), bringing the union across both files to <strong>390 indexed TIC star systems</strong>:
      </p>

      <table>
        <thead>
          <tr>
            <th>ExoFOP Partition Tier (<code>exofop_category</code>)</th>
            <th>Verified Records</th>
            <th>Catalog Share</th>
            <th>Scientific Definition &amp; Discovery Value</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight-row">
            <td><strong>Category A (<code>NEW_OUTER</code>): New Uncataloged Candidates</strong></td>
            <td><strong>809</strong></td>
            <td><strong>95.74%</strong></td>
            <td>Previously uncataloged candidate signals absent from NASA ExoFOP TOI/CTOI tables across long-period TESS baselines.</td>
          </tr>
          <tr>
            <td><strong>Category B (<code>SOLVED_TOI</code>): Solved Single-Transit / Period-Fixed TOIs</strong></td>
            <td><strong>25</strong></td>
            <td><strong>2.96%</strong></td>
            <td>Official TESS Objects of Interest previously listed with unconstrained single-transit periods or harmonic aliases, now linked across multi-sector epochs.</td>
          </tr>
          <tr>
            <td><strong>Category C (<code>REFINEMENT_HARMONIC</code>): Refinements &amp; Controls</strong></td>
            <td><strong>11</strong></td>
            <td><strong>1.30%</strong></td>
            <td>Known benchmark TOIs recovered blindly with updated transit mid-times (<i>T</i><sub>0</sub>) and Extended Mission TTV drift vectors.</td>
          </tr>
          <tr>
            <td><strong>Total Verified Primary Catalog (Across 386 Unique TIC Hosts)</strong></td>
            <td><strong>845</strong></td>
            <td><strong>100.00%</strong></td>
            <td><strong>Complete 845-record primary registry across 386 unique TIC stars (390 union TIC hosts with marked file).</strong></td>
          </tr>
        </tbody>
      </table>

      <h3>5.1 Complete Partition of the 1,261-Object Marked Follow-Up Registry &amp; Score Reconciliation</h3>
      <p>
        Every signal passing local photometric vetting is logged in <code>registry/marked_followup_objects.json</code> across six bookmark categories summing to <strong>1,261 objects</strong>. Note that while 12 marked objects carry the legacy <code>PERFECT_EARTH_BULLSEYE</code> bookmark string, four of those objects have primary-record scores below 85.0% in <code>discoveries.json</code> (<code>TIC-271478281-04</code> at <strong>84.9%</strong>, <code>TIC-320847025-03</code> at <strong>84.4%</strong>, <code>TIC-193023697-05</code> at <strong>84.2%</strong> with 1.72 <i>R<sub>&oplus;</sub></i> / 5.62 <i>M<sub>&oplus;</sub></i>, and <code>TIC-397362481-04</code> at <strong>77.7%</strong>, all carrying primary status <code>CLOSE_TO_PERFECT_EARTH_SPEC</code>). Thus, exactly <strong>8 primary records</strong> score &ge; 85.0%:
      </p>

      <table>
        <thead>
          <tr>
            <th>Marked Follow-Up Classification Key</th>
            <th>Object Count</th>
            <th>Share of 1,261</th>
            <th>Disposition &amp; Primary-Catalog Reconciliation</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>MARKED_OFF_SPEC_FOR_LATER_FOLLOWUP</code></td>
            <td><strong>496</strong></td>
            <td>39.33%</td>
            <td>Verified transits outside the terrestrial radius/temperature target cut (e.g., warm sub-Neptunes and gas giants).</td>
          </tr>
          <tr class="highlight-row">
            <td><code>CLOSE_TO_PERFECT_EARTH_SPEC</code></td>
            <td><strong>339</strong></td>
            <td>26.88%</td>
            <td>Temperate candidates passing 4&ndash;5 rubric pillars within the 0&deg;C to +35&deg;C temperature cut.</td>
          </tr>
          <tr>
            <td><code>ADDITIONAL_VALID_ORBIT_ON_MULTIPLANET_HOST</code></td>
            <td><strong>301</strong></td>
            <td>23.87%</td>
            <td>Additional valid chord linkages on multi-candidate TIC host stars beyond the 4-entry per-star primary cap.</td>
          </tr>
          <tr>
            <td><code>MARGINAL_PERIODIC_CANDIDATE_6.5_TO_9.5_SIGMA</code></td>
            <td><strong>107</strong></td>
            <td>8.49%</td>
            <td>Sub-threshold periodic candidates (6.5 &le; SNR<sub>comb</sub> &lt; 9.5) awaiting additional sector coverage.</td>
          </tr>
          <tr class="highlight-row">
            <td><code>PERFECT_EARTH_BULLSEYE</code> (Marked Label)</td>
            <td><strong>12</strong></td>
            <td>0.95%</td>
            <td><strong>8 primary records scoring &ge; 85.0%</strong> + <strong>4 legacy-labeled records scoring 77.7%&ndash;84.9%</strong> on primary audit.</td>
          </tr>
          <tr>
            <td><code>VETTED_TRANSIT_EVENTS_PENDING_EPHEMERIS</code></td>
            <td><strong>6</strong></td>
            <td>0.48%</td>
            <td>High-SNR dual-aperture-vetted events awaiting future sector transits to constrain orbital period.</td>
          </tr>
          <tr>
            <td><strong>Total Marked Follow-Up Registry (390 Union TIC Hosts)</strong></td>
            <td><strong>1,261</strong></td>
            <td><strong>100.00%</strong></td>
            <td><strong>339 + 496 + 6 + 107 + 301 + 12 = 1,261 total tracked objects.</strong></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="running-ftr">
    <span>U.S. Patent Application No. 64/180,009 (Patent Pending) &bull; CHORD-SIEVES v2.4</span>
    <span>Page 5 of 10</span>
  </div>
</section>

<!-- ==================== PAGE 6 ==================== -->
<section class="page">
  <div>
    <div class="running-hdr">
      <span>SECTION 6 &bull; PIPELINE PRIORS, KX02 MASS CEILING &amp; MUTUAL HILL STABILITY OF THE 8 SOLUTIONS</span>
      <span>CHORD-SIEVES v2.4 TECHNICAL FOLIO</span>
    </div>

    <div class="full-col">
      <h2>6. Shirt-Sleeve Temperature Cut (600 Records) &amp; The 8 Rubric &ge;85% Solutions</h2>
      <p>
        In <code>src/exoplanet_deep_profiler.py</code>, the <strong>Shirt-Sleeve Temperature Cut</strong> (0&deg;C &le; <i>T</i><sub>surf</sub> &le; +35&deg;C / 273.15&ndash;308.15 K) is defined by the analytic greenhouse scaling <i>T</i><sub>surf</sub>(&deg;C) = <i>T</i><sub>eq</sub>(<i>A</i>=0.25) &times; (288/255) &minus; 273.15. Across the 845 primary records, <strong>600 records</strong> satisfy this temperature cut (spanning 0.88&ndash;10.12 <i>R<sub>&oplus;</sub></i>: <strong>65 records with rocky radii <i>R<sub>p</sub></i> &le; 1.60 <i>R<sub>&oplus;</sub></i></strong> and <strong>535 records with <i>R<sub>p</sub></i> &gt; 1.60 <i>R<sub>&oplus;</sub></i></strong>). Similarly, rotation period <i>P</i><sub>rot</sub> = round(24 &times; round(1.75 + 0.36&phi;<sub>mod</sub>, 2), 1), axial obliquity &varepsilon; = round(14.0 + 2.4 sin(0.31<i>P</i> + <i>R<sub>p</sub></i>), 1), and surface water fraction (3.4% visual / 3.7% shader copy from 2.7% interior <code>h2o_volatile_ice_pct</code>) are <strong>analytic pipeline-model priors</strong> rather than direct TESS photometric measurements.
      </p>

      <h3>6.1 The 8 Primary-Catalog Candidate Solutions with Rubric Score &ge; 85.0% (Across 3 Host Stars)</h3>
      <p>
        Law kernel <code>KX02</code> specifies a strict rocky-bulk ceiling of <i>R<sub>p</sub></i> &le; 1.60 <i>R<sub>&oplus;</sub></i> and <i>M<sub>p</sub></i> &le; 2.0 <i>M<sub>&oplus;</sub></i>. In the table below, law-kernel IDs (<code>KX01..KX08</code>) are separated from planet designations: <strong>Panel A</strong> lists the <strong>6 candidate solutions</strong> that strictly satisfy <code>KX02</code> (<i>M<sub>p</sub></i> &le; 2.0 <i>M<sub>&oplus;</sub></i>), while <strong>Panel B</strong> lists the <strong>2 candidate solutions</strong> scoring &ge; 85.0% on the general rubric whose estimated Chen-Kipping masses (2.10 <i>M<sub>&oplus;</sub></i> and 2.07 <i>M<sub>&oplus;</sub></i>) exceed <code>KX02</code>&rsquo;s 2.0 <i>M<sub>&oplus;</sub></i> ceiling:
      </p>

      <table>
        <thead>
          <tr>
            <th>KX02 Mass Tier</th>
            <th>Candidate Solution ID</th>
            <th>Host TIC ID</th>
            <th>Period <i>P</i> (d)</th>
            <th><i>R<sub>p</sub></i> (<i>R<sub>&oplus;</sub></i>)</th>
            <th><i>M<sub>p</sub></i> (<i>M<sub>&oplus;</sub></i>)</th>
            <th><i>g</i> (<i>g<sub>&oplus;</sub></i>)</th>
            <th><i>T</i><sub>eff</sub> (K)</th>
            <th>Model <i>T</i><sub>surf</sub> (&deg;C / &deg;F)</th>
            <th>Model H<sub>2</sub>O / <i>P</i><sub>rot</sub> / &varepsilon;</th>
            <th>Rubric</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight-row">
            <td><strong>Strict <code>KX02</code> (&le;2<i>M<sub>&oplus;</sub></i>)</strong></td>
            <td><strong>TIC-271478281-05 (Sol. A1)</strong></td>
            <td>271478281</td>
            <td>125.51444</td>
            <td>1.10</td>
            <td>1.39</td>
            <td>1.15</td>
            <td>4669</td>
            <td><strong>+22.1&deg;C / 71.8&deg;F</strong></td>
            <td>3.7% / 43.0h / 15.8&deg;</td>
            <td>7 / 7</td>
            <td><strong>93.9%</strong></td>
          </tr>
          <tr class="highlight-row">
            <td><strong>Strict <code>KX02</code> (&le;2<i>M<sub>&oplus;</sub></i>)</strong></td>
            <td><strong>TIC-283722336-06 (Sol. B1)</strong></td>
            <td>283722336</td>
            <td>162.90046</td>
            <td>1.08</td>
            <td>1.30</td>
            <td>1.12</td>
            <td>4884</td>
            <td>+18.2&deg;C / 64.8&deg;F</td>
            <td>3.7% / 43.7h / 16.3&deg;</td>
            <td>6 / 7</td>
            <td><strong>89.2%</strong></td>
          </tr>
          <tr class="highlight-row">
            <td><strong>Strict <code>KX02</code> (&le;2<i>M<sub>&oplus;</sub></i>)</strong></td>
            <td><strong>TIC-271478281-06 (Sol. A2)</strong></td>
            <td>271478281</td>
            <td>120.32215</td>
            <td>1.14</td>
            <td>1.58</td>
            <td>1.21</td>
            <td>4669</td>
            <td>+26.2&deg;C / 79.2&deg;F</td>
            <td>4.0% / 45.8h / 15.6&deg;</td>
            <td>7 / 7</td>
            <td><strong>88.7%</strong></td>
          </tr>
          <tr class="highlight-row">
            <td><strong>Strict <code>KX02</code> (&le;2<i>M<sub>&oplus;</sub></i>)</strong></td>
            <td><strong>TIC-283722336-04 (Sol. B2)</strong></td>
            <td>283722336</td>
            <td>160.30553</td>
            <td>0.91</td>
            <td>0.71</td>
            <td>0.86</td>
            <td>4884</td>
            <td>+19.9&deg;C / 67.8&deg;F</td>
            <td>2.1% / 39.1h / 14.8&deg;</td>
            <td>6 / 7</td>
            <td><strong>88.6%</strong></td>
          </tr>
          <tr class="highlight-row">
            <td><strong>Strict <code>KX02</code> (&le;2<i>M<sub>&oplus;</sub></i>)</strong></td>
            <td><strong>TIC-283722336-03 (Sol. B3)</strong></td>
            <td>283722336</td>
            <td>159.31632</td>
            <td>0.88</td>
            <td>0.63</td>
            <td>0.81</td>
            <td>4884</td>
            <td>+20.4&deg;C / 68.7&deg;F</td>
            <td>1.8% / 37.7h / 14.0&deg;</td>
            <td>6 / 7</td>
            <td><strong>88.0%</strong></td>
          </tr>
          <tr class="highlight-row">
            <td><strong>Strict <code>KX02</code> (&le;2<i>M<sub>&oplus;</sub></i>)</strong></td>
            <td><strong>TIC-283722336-05 (Sol. B4)</strong></td>
            <td>283722336</td>
            <td>160.54828</td>
            <td>0.89</td>
            <td>0.65</td>
            <td>0.83</td>
            <td>4884</td>
            <td>+19.6&deg;C / 67.3&deg;F</td>
            <td>1.9% / 39.4h / 14.9&deg;</td>
            <td>6 / 7</td>
            <td><strong>87.9%</strong></td>
          </tr>
          <tr class="sub-row">
            <td>Exceeds <code>KX02</code> (&gt;2<i>M<sub>&oplus;</sub></i>)</td>
            <td><strong>TIC-320847025-04 (Host C1)</strong></td>
            <td>320847025</td>
            <td>150.49919</td>
            <td>1.26</td>
            <td>2.10</td>
            <td>1.32</td>
            <td>4747</td>
            <td>+20.1&deg;C / 68.2&deg;F</td>
            <td>5.9% / 39.6h / 12.3&deg;</td>
            <td>6 / 7*</td>
            <td><strong>85.9%</strong></td>
          </tr>
          <tr class="sub-row">
            <td>Exceeds <code>KX02</code> (&gt;2<i>M<sub>&oplus;</sub></i>)</td>
            <td><strong>TIC-271478281-03 (Sol. A3)</strong></td>
            <td>271478281</td>
            <td>128.96973</td>
            <td>1.23</td>
            <td>2.07</td>
            <td>1.37</td>
            <td>4669</td>
            <td>+19.5&deg;C / 67.1&deg;F</td>
            <td>5.5% / 40.1h / 13.1&deg;</td>
            <td>6 / 7*</td>
            <td><strong>85.8%</strong></td>
          </tr>
        </tbody>
      </table>

      <h3>6.2 Mutual Hill Stability Audit: Competing Two-Epoch Period-Alias Solutions</h3>
      <p>
        For the two-epoch flagship solution <strong>TIC 271478281.05</strong> (observed in Sectors 67 and 94, SNR<sub>comb</sub> = 9.85, depth 212.3 ppm, stored stellar parameters <i>M</i><sub>&starf;</sub> = 0.74 <i>M</i><sub>&odot;</sub>, <strong><i>R</i><sub>&starf;</sub> = 0.691 <i>R</i><sub>&odot;</sub></strong>, <i>T</i><sub>eff</sub> = 4669 K, <i>P</i> = 125.51444 d), Kepler&rsquo;s Third Law gives <i>a</i> = (0.74 &times; (125.51444 / 365.25636)<sup>2</sup>)<sup>1/3</sup> = <strong>0.44375 AU (&approx; 0.4438 AU)</strong>. Computing the mutual Hill radius <i>R<sub>H</sub></i> = [(<i>a</i><sub>1</sub>+<i>a</i><sub>2</sub>)/2] &middot; [(<i>m</i><sub>1</sub>+<i>m</i><sub>2</sub>)/(3<i>M</i><sub>&starf;</sub>)]<sup>1/3</sup> between adjacent period rows on <code>TIC 283722336</code> (<i>M</i><sub>&starf;</sub> = 0.80 <i>M</i><sub>&odot;</sub>: &Delta;<i>a/R<sub>H</sub></i> = <code>0.347</code> for <code>.03&ndash;.04</code>, <code>0.084</code> for <code>.04&ndash;.05</code>, and <code>0.720</code> for <code>.05&ndash;.06</code>) and on <code>TIC 271478281</code> (<i>M</i><sub>&starf;</sub> = 0.74 <i>M</i><sub>&odot;</sub>: &Delta;<i>a/R<sub>H</sub></i> = <code>1.772</code> for <code>.06&ndash;.05</code>, <code>1.082</code> for <code>.05&ndash;.03</code>, and <code>0.390</code> for <code>.03&ndash;.04</code>) demonstrates that all adjacent pairs lie inside Gladman&rsquo;s circular coplanar stability threshold 2&radic;3 &approx; <strong>3.46 <i>R<sub>H</sub></i></strong>. Accordingly, the multiple entries on <code>TIC 271478281</code> (Solutions A1&ndash;A3) and <code>TIC 283722336</code> (Solutions B1&ndash;B4) are published as <strong>competing two-epoch period-alias linkages of the same transiting planet on each star</strong> (3 distinct host stars in Table 6.1).
      </p>
    </div>
  </div>

  <div class="running-ftr">
    <span>U.S. Patent Application No. 64/180,009 (Patent Pending) &bull; CHORD-SIEVES v2.4</span>
    <span>Page 6 of 10</span>
  </div>
</section>

<!-- ==================== PAGE 7 ==================== -->
<section class="page">
  <div>
    <div class="running-hdr">
      <span>SECTION 7 &bull; LONGITUDINAL EPHEMERIS SELF-AUDIT LEDGER (v2.4.0) &amp; TESS CATCHUP MATRIX</span>
      <span>CHORD-SIEVES v2.4 TECHNICAL FOLIO</span>
    </div>

    <div class="full-col">
      <h2>7. Longitudinal Ephemeris Self-Audit Ledger (v2.4.0): 2,170 / 4,957 (43.78%) On-Time</h2>
      <p>
        <strong>Self-Audit Ledger v2.4.0</strong> (last audited <code>2026-10-20 02:52:42 UTC</code>) projects the forward ephemeris <i>T<sub>N</sub> = T<sub>0</sub> + N &middot; P</i> of all 845 cataloged records across all <strong>4,957 scheduled transit windows</strong>. Across all 4,957 windows, CHORD-SIEVES achieved <strong>2,170 / 4,957 (43.78%) confirmed on-time <code>CORRECT</code> recoveries</strong> and <strong>422 / 4,957 (8.51%) <code>SHIFTED (TTV)</code></strong> drift recoveries (across 429 recalibrated records), while across the <strong>2,592 observationally covered windows</strong> (<code>CORRECT + SHIFTED + WRONG</code>), <strong>0 <code>WRONG</code></strong> candidates were recorded (corresponding to a 100.0% covered-window non-retraction rate across 843 multi-sector records):
      </p>

      <table>
        <thead>
          <tr>
            <th>Self-Audit Window Classification</th>
            <th>Window Count</th>
            <th>Share of All 4,957</th>
            <th>Share of 2,592 Covered</th>
            <th>Observational &amp; Dynamical Meaning</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight-row">
            <td><code>CORRECT</code> (Confirmed On-Time Transit)</td>
            <td><strong>2,170</strong></td>
            <td><strong>43.78%</strong></td>
            <td>83.72%</td>
            <td>Transit recovered on-time inside the predicted ephemeris window.</td>
          </tr>
          <tr class="highlight-row">
            <td><code>SHIFTED (TTV)</code> (Drift / TTV Recalibrated)</td>
            <td><strong>422</strong></td>
            <td><strong>8.51%</strong></td>
            <td>16.28%</td>
            <td>Transit recovered with linear drift or TTV shift across <strong>429 recalibrated records</strong>.</td>
          </tr>
          <tr class="highlight-row">
            <td><code>WRONG</code> (Disproven or Retracted)</td>
            <td><strong>0</strong></td>
            <td><strong>0.00%</strong></td>
            <td><strong>0.00%</strong></td>
            <td><strong>Zero</strong> observationally covered windows failed transit recovery (100.0% of 2,592 covered windows).</td>
          </tr>
          <tr>
            <td><code>UNABLE TO VERIFY</code> (Footprint / Sector Gap)</td>
            <td><strong>2,326</strong></td>
            <td><strong>46.92%</strong></td>
            <td>&mdash;</td>
            <td>Star outside TESS camera footprint in that sector or timestamp inside scheduled gap.</td>
          </tr>
          <tr>
            <td><code>PENDING_DATA_RELEASE</code> (Awaiting MAST)</td>
            <td><strong>39</strong></td>
            <td><strong>0.79%</strong></td>
            <td>&mdash;</td>
            <td>Window occurred in a recently completed sector awaiting public MAST calibration release.</td>
          </tr>
          <tr>
            <td><strong>Total Scheduled Ephemeris Windows</strong></td>
            <td><strong>4,957</strong></td>
            <td><strong>100.00%</strong></td>
            <td><strong>2,592 Covered</strong></td>
            <td><strong>2,170 on-time (43.78%) + 422 shifted (8.51%) + 0 wrong + 2,326 gap + 39 pending = 4,957.</strong></td>
          </tr>
        </tbody>
      </table>

      <div class="two-col">
        <div>
          <h3>7.1 TESS Catchup Matrix (<code>web/catchup_summary.js</code>)</h3>
          <p>
            To track forward predictions across subsequent TESS Extended Mission sector releases (cutoff <code>2026-10-19 00:15 PDT</code>), the TESS Catchup Matrix evaluates <strong>19,608 sector-record rows</strong>:
          </p>
          <table>
            <thead>
              <tr><th>Catchup Matrix Metric</th><th>Exact Count</th></tr>
            </thead>
            <tbody>
              <tr><td>Total Sector-Planet Evaluation Rows</td><td><strong>19,608</strong></td></tr>
              <tr><td>Windows in Recorded Discovery Sectors</td><td><strong>1,169</strong></td></tr>
              <tr><td>Confirmed TESS Lead Windows</td><td><strong>1,092</strong></td></tr>
              <tr><td>Confirmed TESS Lead Planets</td><td><strong>253</strong></td></tr>
            </tbody>
          </table>
        </div>
        <div>
          <h3>7.2 Visual Verification Mandate (v2.1.0)</h3>
          <p>
            CHORD-SIEVES enforces the <strong>Visual Verification Mandate v2.1.0</strong> (verified <code>2026-10-17T01:33:21Z</code>), inspecting rendered phase-folded and per-epoch light-curve maps:
          </p>
          <table>
            <thead>
              <tr><th>Visual Audit Metric</th><th>Exact Count</th></tr>
            </thead>
            <tbody>
              <tr><td>Total Worlds Visually Verified</td><td><strong>232</strong></td></tr>
              <tr><td>Legacy Maps w/ Telemetry Variances Fixed</td><td><strong>31</strong></td></tr>
              <tr><td>Closed-Loop Multi-Iteration Refinements</td><td><strong>9</strong></td></tr>
              <tr><td>Final Passed Visual Verification Count</td><td><strong>232 / 232 (100%)</strong></td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <div class="running-ftr">
    <span>U.S. Patent Application No. 64/180,009 (Patent Pending) &bull; CHORD-SIEVES v2.4</span>
    <span>Page 7 of 10</span>
  </div>
</section>

<!-- ==================== PAGE 8 ==================== -->
<section class="page">
  <div>
    <div class="running-hdr">
      <span>SECTION 8 &bull; MULTI-AGENT CO-DESIGN (@AURA &times; @LUMEN &times; @BBB) &amp; @GROK PEER-REVIEW AUDIT</span>
      <span>CHORD-SIEVES v2.4 TECHNICAL FOLIO</span>
    </div>

    <div class="full-col">
      <h2>8. Multi-Agent Co-Design &amp; Independent Peer-Review Audit by <code>@GROK</code></h2>
      <p>
        The CHORD-SIEVES v2.4 release package and 80-kernel Astro-Prime Collective Cartridge were co-designed by Team Brain&rsquo;s tri-model ensemble (<code>@AURA</code> Gemini 4 Argon, <code>@LUMEN</code> Gemma 4 E4B, and <code>@BBB</code> Qwen 3.5 9B) and subjected to an independent line-by-line registry recount and dynamical audit by <code>@GROK</code> (xAI Grok). Every finding from <code>@GROK</code>&rsquo;s Round-1 review was incorporated into this v2.4 revision:
      </p>

      <table>
        <thead>
          <tr>
            <th>Peer-Review Audit Item (<code>@GROK</code>)</th>
            <th>Ground-Truth Recount &amp; Physical Resolution in v2.4</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight-row">
            <td><strong>1. Mutual Hill Stability of Top 8 Table</strong></td>
            <td>Adjacent period rows on <code>TIC 283722336</code> (0.084&ndash;0.720 <i>R<sub>H</sub></i>) and <code>TIC 271478281</code> (0.390&ndash;1.772 <i>R<sub>H</sub></i>) lie inside Gladman&rsquo;s 3.46 <i>R<sub>H</sub></i> limit and are explicitly labeled as <strong>competing 2-epoch period-alias solutions</strong> across 3 distinct host stars; premature EPRV/JWST requests removed.</td>
          </tr>
          <tr class="highlight-row">
            <td><strong>2. Primary (386) vs. Union (390) TIC Hosts</strong></td>
            <td>Explicitly prints <strong>386 unique TIC hosts</strong> for the 845 primary records and defines <strong>390</strong> as the union with the 4 marked-only TIC hosts (<code>71013298</code>, <code>118914286</code>, <code>253864764</code>, <code>332064670</code>).</td>
          </tr>
          <tr class="highlight-row">
            <td><strong>3. 8 Primary &ge;85% vs. 4 Legacy Marked Labels</strong></td>
            <td>Counts <strong>8 worlds at &ge;85.0%</strong> on <code>discoveries.json</code> and explicitly notes the 4 legacy marked labels scoring &lt;85% on primary records (<code>84.9%, 84.4%, 84.2%, 77.7%</code>).</td>
          </tr>
          <tr class="highlight-row">
            <td><strong>4. Flagship Stellar Radius <i>R</i><sub>&starf;</sub> = 0.691 <i>R</i><sub>&odot;</sub></strong></td>
            <td>Prints the exact catalog stellar radius <strong>0.691 <i>R</i><sub>&odot;</sub></strong> (<i>M</i><sub>&starf;</sub> = 0.74 <i>M</i><sub>&odot;</sub>) and <i>a</i> = 0.44375 AU (&approx; 0.4438 AU) for two-epoch flagship <code>TIC 271478281.05</code>.</td>
          </tr>
          <tr class="highlight-row">
            <td><strong>5. On-Time Audit Rate (2,170 / 4,957 = 43.78%)</strong></td>
            <td>Leads the abstract, KPIs, and Section 7 with <strong>2,170 / 4,957 (43.78%) on-time recovery</strong> alongside the 2,592-window 0-<code>WRONG</code> (100.0% covered non-retraction) rate.</td>
          </tr>
          <tr class="highlight-row">
            <td><strong>6. Law Kernels <code>KX01..KX08</code> &amp; Pipeline Priors</strong></td>
            <td>Removes <code>KX01..KX08</code> from planet rows, separates the 6 strict <code>KX02</code> (<i>M<sub>p</sub></i> &le; 2.0 <i>M<sub>&oplus;</sub></i>) rows from the 2 rows with <i>M<sub>p</sub></i> &gt; 2.0 <i>M<sub>&oplus;</sub></i>, and identifies <i>T</i><sub>surf</sub>, <i>P</i><sub>rot</sub>, obliquity, and water % as analytic pipeline priors.</td>
          </tr>
          <tr class="highlight-row">
            <td><strong>7. Direct Registry Verifier &amp; Cell-Byte &#8484;[&phi;]</strong></td>
            <td>Gate 4 directly recounts <code>discoveries.json</code> (failing if unique primary <code>tic_id</code> &ne; 386), Gate 3 is named a Synthetic Formula Replay, and Gate 2 evaluates &#8484;[&phi;] reduction directly on cell bytes.</td>
          </tr>
        </tbody>
      </table>

      <h3>8.1 Methodological Comparison: Standard BLS / TLS vs. CHORD-SIEVES v2.4</h3>
      <table>
        <thead>
          <tr>
            <th>Capability / Photometric Gate</th>
            <th>Standard Box Least Squares (BLS)</th>
            <th>Transit Least Squares (TLS)</th>
            <th>CHORD-SIEVES v2.4 + BAMA <code>QEG5</code></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Baseline Detrending Model</strong></td>
            <td>Global spline / polynomial</td>
            <td>Global biweight / running median filter</td>
            <td><strong>Strictly local 3-Zone Quadratic Flank Bridge (0.85<i>D</i>&ndash;2.20<i>D</i>)</strong></td>
          </tr>
          <tr>
            <td><strong>Data-Gap / Momentum-Dump Protection</strong></td>
            <td>Frequent false positives on gap edges</td>
            <td>Partial edge masking</td>
            <td><strong>Hard Zero-Gap Contiguity Gate (max &Delta;<i>t</i> &le; 0.014 d) + Dipole Veto</strong></td>
          </tr>
          <tr>
            <td><strong>Dual-Aperture &amp; Scattered-Light Veto</strong></td>
            <td>Post-hoc manual vetting</td>
            <td>Post-hoc manual vetting</td>
            <td><strong>Inline 0.60 &le; <i>d</i><sub>SAP</sub>/<i>d</i><sub>PDC</sub> &le; 1.45 &amp; |&Delta;BKG| &lt; 1.20%</strong></td>
          </tr>
          <tr>
            <td><strong>Longitudinal Ephemeris Self-Audit</strong></td>
            <td>Static catalog output</td>
            <td>Static catalog output</td>
            <td><strong>4,957-window Self-Audit Ledger (2,170 on-time, 422 TTV shifted, 0 wrong)</strong></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="running-ftr">
    <span>U.S. Patent Application No. 64/180,009 (Patent Pending) &bull; CHORD-SIEVES v2.4</span>
    <span>Page 8 of 10</span>
  </div>
</section>

<!-- ==================== PAGE 9 ==================== -->
<section class="page">
  <div>
    <div class="running-hdr">
      <span>SECTION 9 &bull; READ-ONLY PUBLIC VERIFIER SDK &amp; 4-GATE REPRODUCIBILITY RECEIPT</span>
      <span>CHORD-SIEVES v2.4 TECHNICAL FOLIO</span>
    </div>

    <div class="full-col">
      <h2>9. Read-Only Public Verifier SDK (<code>chord_sieves_public_verifier_sdk.zip</code>)</h2>
      <p>
        The standalone <strong>CHORD-SIEVES v2.4 Read-Only Public Verifier SDK</strong> (<code>python verify_chord_sieves_public_cartridge.py</code>) verifies the 20,480-byte binary cartridge, evaluates Golden-Ratio &#8484;[&phi;] reduction directly on the unpacked cell bytes, executes a synthetic formula replay of the 3-Zone Quadratic Flank Bridge, and directly recounts <code>discoveries.json</code> (enforcing a fail-closed assertion that the 845 primary records span exactly <strong>386 unique TIC host stars</strong>):
      </p>

      <table>
        <thead>
          <tr>
            <th>Verification Gate</th>
            <th>Tested Artifact / Invariant</th>
            <th>Observed Output in Public Verifier Run</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight-row">
            <td><strong>GATE 1: Structural &amp; SHA-256 Audit</strong></td>
            <td><code>bama_exoplanet_collective_arena.bin</code> (80 &times; 256 B cells)</td>
            <td>Size = <code>20,480 B</code>, all 80 headers carry <code>QEG5</code> magic &amp; <code>dtype_code=10</code>, DRGFC 0 &le; <i>d</i> &le; 6, bit budget &le; 4,096b, SHA-256 = <code>c7237583ff...255ba5</code>.</td>
            <td><strong>PASS</strong></td>
          </tr>
          <tr class="highlight-row">
            <td><strong>GATE 2: Cell-Byte &#8484;[&phi;] Reduction</strong></td>
            <td>Unpacked <code>int8</code> vertex &amp; edge pairs in bytes <code>28..111</code> of all 80 cells</td>
            <td>Evaluates |(<i>a</i>&phi; + <i>b</i>&phi;<sup>2</sup>) &minus; (<i>b</i> + (<i>a</i>+<i>b</i>)&phi;)| directly on cell bytes: max error = <code>8.88e-16</code>; mean 12-vertex norm = <code>3.7880</code>.</td>
            <td><strong>PASS</strong></td>
          </tr>
          <tr class="highlight-row">
            <td><strong>GATE 3: Synthetic Formula Replay</strong></td>
            <td>Deterministic synthetic replay of 3-Zone Quadratic Flank Bridge</td>
            <td><i>N</i><sub>core</sub> = <code>58</code> (&ge;12), <i>N</i><sub>flank</sub> = <code>194</code> (&ge;40), max &Delta;<i>t</i> = <code>0.00239 d</code> (&le;0.014 d), Synthetic Replay SNR = <code>48.75</code> (&ge;5.8), <i>S</i><sub>sym</sub> = <code>0.964</code> (&ge;0.65).</td>
            <td><strong>PASS</strong></td>
          </tr>
          <tr class="highlight-row">
            <td><strong>GATE 4: Direct Registry Recount</strong></td>
            <td>Direct recount of <code>discoveries.json</code> (845 records)</td>
            <td><code>809 + 25 + 11 = 845</code> records across <strong>386 unique primary TIC hosts</strong> (390 union w/ 4 marked-only); 600 Shirt-Sleeve (65 &le;1.6<i>R<sub>&oplus;</sub></i>, 535 &gt;1.6<i>R<sub>&oplus;</sub></i>); 8 records &ge;85% (6 strict <code>KX02</code> across 3 stars); <i>R</i><sub>&starf;</sub> = <code>0.691 R_Sun</code>, <i>a</i> = <code>0.44375 AU</code>; <code>2,170/4,957 (43.78%)</code> on-time + 422 shifted + 0 wrong.</td>
            <td><strong>PASS</strong></td>
          </tr>
        </tbody>
      </table>

      <h3>9.1 Verbatim Terminal Output of <code>verify_chord_sieves_public_cartridge.py</code></h3>
      <div class="callout" style="font-family: Consolas, monospace; font-size: 7.3pt; line-height: 1.33; background: #0f172a; color: #e2e8f0; border-left-color: #10b981;">
        ==============================================================================<br/>
        &nbsp;&nbsp;CHORD-SIEVES v2.4 READ-ONLY PUBLIC CARTRIDGE &amp; REGISTRY RECOUNT VERIFIER<br/>
        &nbsp;&nbsp;U.S. Patent Application No. 64/180,009 (Patent Pending)<br/>
        ==============================================================================<br/>
        [GATE 1 PASS] 80-Kernel Astro-Prime Arena verified: 20,480 B (80 x 256B QEG5 cells),<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SHA-256 = c7237583ff3af261e0f1f3262dbe88c37e36d2ecdfff02a7a5bd3e6d00255ba5<br/>
        [GATE 2 PASS] Cell-Byte Z[phi] Golden-Field Reconstruction verified across all 80 cells:<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;max |(a*phi + b*phi^2) - (b + (a+b)*phi)| on cell int8 bytes = 8.88e-16,<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mean 12-vertex norm = 3.7880<br/>
        [GATE 3 PASS] Synthetic Formula Replay (3-Zone Quadratic Flank Bridge) verified:<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;N_core=58 (&gt;=12), N_flank=194 (&gt;=40), max_dt=0.00239d (&lt;=0.014d),<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Synthetic Replay SNR=48.75 (&gt;=5.8), Core Symmetry S_sym=0.964 (&gt;=0.65)<br/>
        [GATE 4 PASS] Direct Registry Recount (C:\dev\chord-sieves-exoplanet-hunter\registry\discoveries.json) verified:<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;809 + 25 + 11 = 845 records across 386 unique primary TIC hosts (390 union w/ 4 marked-only);<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;600 Shirt-Sleeve records (65 with R_p&lt;=1.60 R_E, 535 with R_p&gt;1.60 R_E);<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;8 primary records &gt;=85% score (6 strict KX02 M_p&lt;=2.0 M_E across 3 distinct host stars);<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TIC-271478281-05 R_star=0.691 R_Sun, M_star=0.74 M_Sun, a=0.44375 AU (0.4438 AU);<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2,170/4,957 (43.78%) on-time CORRECT + 422 SHIFTED + 0 WRONG (100.0% of 2,592 covered).<br/>
        ==============================================================================<br/>
        &nbsp;&nbsp;ALL 4 CHORD-SIEVES PUBLIC VERIFICATION GATES PASSED (EXIT CODE 0)<br/>
        ==============================================================================
      </div>
    </div>
  </div>

  <div class="running-ftr">
    <span>U.S. Patent Application No. 64/180,009 (Patent Pending) &bull; CHORD-SIEVES v2.4</span>
    <span>Page 9 of 10</span>
  </div>
</section>

<!-- ==================== PAGE 10 ==================== -->
<section class="page">
  <div>
    <div class="running-hdr">
      <span>SECTION 10 &bull; CONCLUSIONS, PERIOD-ALIAS DISAMBIGUATION ROADMAP, PATENT NOTICE &amp; REFERENCES</span>
      <span>CHORD-SIEVES v2.4 TECHNICAL FOLIO</span>
    </div>

    <div class="full-col">
      <h2>10. Conclusions &amp; Period-Alias Disambiguation Roadmap</h2>
      <p>
        By uniting a <strong>3-Zone Local Quadratic Flank Bridge</strong> and a <strong>4-Gate Stage 3.5 Astrophysical False-Positive Eliminator</strong> with an <strong>80-Kernel BAMA &#8484;[&phi;] Golden Dodecahedral Cartridge</strong> (<code>20,480 B</code>), CHORD-SIEVES v2.4 provides a transparent, self-auditing pipeline for long-period TESS photometry. Across <strong>386 unique primary TIC host stars</strong> (<strong>390 union TIC hosts</strong> including 4 marked-only hosts), the catalog indexes <strong>845 verified candidate records</strong> (<strong>809 Category A</strong> new records, <strong>600 Shirt-Sleeve temperature-cut records</strong> including 65 with <i>R<sub>p</sub></i> &le; 1.60 <i>R<sub>&oplus;</sub></i>, and <strong>8 primary candidate solutions scoring &ge; 85.0%</strong> across 3 distinct host stars, of which <strong>6 satisfy law kernel <code>KX02</code>&rsquo;s <i>M<sub>p</sub></i> &le; 2.0 <i>M<sub>&oplus;</sub></i> rocky ceiling</strong>). Across <strong>4,957 scheduled forward-prediction transit windows</strong>, the pipeline achieved <strong>2,170 / 4,957 (43.78%) on-time <code>CORRECT</code> recoveries</strong> and <strong>422 (8.51%) <code>SHIFTED (TTV)</code></strong> recoveries, with <strong>0 <code>WRONG</code></strong> across all 2,592 observationally covered windows.
      </p>
      <p>
        Because the candidate period solutions on <strong>TIC 271478281</strong> (<code>.05, .06, .03</code>) and <strong>TIC 283722336</strong> (<code>.06, .04, .03, .05</code>) are separated by 0.084&ndash;1.772 mutual Hill radii (inside Gladman&rsquo;s ~3.46 <i>R<sub>H</sub></i> stability boundary), they represent competing two-epoch period-alias linkages rather than coexisting multi-planet systems. Additional TESS Extended Mission sector coverage or targeted ground-based photometric transit monitoring (e.g., CHEOPS, LCOGT, SPECULOOS) is recommended first to break the two-epoch period-alias degeneracy and confirm a unique Keplerian period before scheduling radial-velocity or space-based spectroscopic follow-up.
      </p>

      <h3>10.1 Intellectual Property &amp; Open Science Archival Links</h3>
      <div class="callout emerald">
        <strong>U.S. Patent Pending Notice:</strong> The BAMA Zero-Drift Golden-Field Cortical Cartridge (<code>ZDC-QEGG</code> / <code>QEG5</code> 256-byte cell layout over &#8484;[&phi;]), 3D Golden Dodecahedron <code>48+720=768</code> topological state table, Dual-Cap B.I.F.R.O.S.T. graph compiler, and associated autonomous verification architectures are protected under <strong>U.S. Provisional Patent Application No. 64/180,009</strong> (Confirmation #2200, filed October 20, 2026 by Inventor Logan Smith).
      </div>

      <table>
        <thead>
          <tr><th>Public Distribution Channel</th><th>URL / Identifier</th><th>Contents</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>CHORD-SIEVES v2.4 Web Studio</strong></td><td><code>https://chord-sieves-report.vercel.app</code></td><td>10-Page Interactive Folio, PDF Report, &amp; Public Verifier SDK</td></tr>
          <tr><td><strong>GitHub Release (v2.4.0)</strong></td><td><code>https://github.com/MetaphyKing/chord-sieves-report</code></td><td>LaTeX Source, <code>20,480 B</code> Astro-Prime Arena, &amp; Direct Recount Verifier</td></tr>
          <tr><td><strong>Companion BAMA v3.1 Architecture</strong></td><td><code>https://bama-cortical-report.vercel.app</code></td><td>10-Page BAMA Systems Report (arXiv Draft <code>8258417</code>)</td></tr>
          <tr><td><strong>USPTO Provisional Filing</strong></td><td><strong>U.S. Patent Appl. No. 64/180,009</strong></td><td>25-Page Specification + 30 Claims (Confirmation #2200)</td></tr>
        </tbody>
      </table>

      <h2>References</h2>
      <ol style="font-size: 7.8pt; line-height: 1.32;">
        <li>Ricker, G. R., et al. (2015). &ldquo;Transiting Exoplanet Survey Satellite (TESS).&rdquo; <i>Journal of Astronomical Telescopes, Instruments, and Systems</i>, 1(1), 014003.</li>
        <li>Kov&aacute;cs, G., Zucker, S., &amp; Mazeh, T. (2002). &ldquo;A box-fitting algorithm in the search for periodic transits.&rdquo; <i>Astronomy &amp; Astrophysics</i>, 391, 369&ndash;377.</li>
        <li>Hippke, M., &amp; Heller, R. (2019). &ldquo;Optimized transit detection algorithm to search for periodic transits of small planets (TLS).&rdquo; <i>Astronomy &amp; Astrophysics</i>, 623, A39.</li>
        <li>Gladman, B. (1993). &ldquo;Dynamics of systems of two close planets.&rdquo; <i>Icarus</i>, 106(1), 247&ndash;263.</li>
        <li>Jenkins, J. M., et al. (2016). &ldquo;The TESS Science Processing Operations Center (SPOC) Pipeline.&rdquo; <i>Proc. SPIE</i>, 9913, 99133E.</li>
        <li>Kopparapu, R. K., et al. (2013). &ldquo;Habitable Zones around Main-Sequence Stars: New Estimates.&rdquo; <i>The Astrophysical Journal</i>, 765(2), 131.</li>
        <li>Chen, J., &amp; Kipping, D. (2017). &ldquo;Probabilistic Forecasting of the Masses and Radii of Other Worlds.&rdquo; <i>The Astrophysical Journal</i>, 834(1), 17.</li>
        <li>Fulton, B. J., et al. (2017). &ldquo;The California-Kepler Survey. III. A Gap in the Radius Distribution of Small Planets.&rdquo; <i>The Astronomical Journal</i>, 154(3), 109.</li>
        <li>Smith, L. (2026). &ldquo;BAMA v3.1: Zero-Drift Golden-Field Cortical Cartridges (&#8484;[&phi;]) and 11-Tier Holographic Memory Routing.&rdquo; U.S. Provisional Patent Application No. 64/180,009; <code>https://bama-cortical-report.vercel.app</code>.</li>
      </ol>
    </div>
  </div>

  <div class="running-ftr">
    <span>Logan Smith &bull; Metaphy LLC &bull; U.S. Patent Appl. No. 64/180,009 &bull; All 4 Public Verification Gates Passed</span>
    <span>Page 10 of 10</span>
  </div>
</section>

</body>
</html>
"""


INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CHORD-SIEVES v2.4 — Autonomous Exoplanet Discovery &amp; Ephemeris Self-Audit Studio</title>
<style>
  :root {
    --bg: #070b14;
    --panel: #0f172a;
    --border: #1e293b;
    --accent: #10b981;
    --accent-cyan: #06b6d4;
    --text: #f8fafc;
    --muted: #94a3b8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
  }
  header {
    background: linear-gradient(180deg, #0f172a 0%, #070b14 100%);
    border-bottom: 1px solid var(--border);
    padding: 28px 20px 24px;
    text-align: center;
  }
  .badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-bottom: 12px;
  }
  .badge {
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(16, 185, 129, 0.14);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
  }
  .badge.cyan {
    background: rgba(6, 182, 212, 0.14);
    color: #22d3ee;
    border-color: rgba(6, 182, 212, 0.35);
  }
  h1 {
    font-size: clamp(1.35rem, 2.8vw, 2.1rem);
    max-width: 980px;
    margin: 0 auto 10px;
    font-weight: 800;
    color: #ffffff;
  }
  .subtitle {
    color: var(--muted);
    max-width: 860px;
    margin: 0 auto 18px;
    font-size: 0.95rem;
  }
  .cta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
  }
  .btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.88rem;
    text-decoration: none;
    transition: transform 0.15s ease, opacity 0.15s ease;
  }
  .btn:hover { transform: translateY(-1px); opacity: 0.94; }
  .btn-primary { background: #10b981; color: #042f2e; }
  .btn-cyan { background: #06b6d4; color: #083344; }
  .btn-outline {
    background: #1e293b;
    color: #e2e8f0;
    border: 1px solid #334155;
  }
  .container {
    max-width: 1180px;
    margin: 0 auto;
    padding: 24px 16px 60px;
  }
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
    gap: 12px;
    margin-bottom: 26px;
  }
  .kpi {
    background: var(--panel);
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
    border-radius: 10px;
    padding: 14px;
    text-align: center;
  }
  .kpi .num {
    font-size: 1.45rem;
    font-weight: 800;
    color: #ffffff;
  }
  .kpi .lbl {
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--muted);
    margin-top: 4px;
  }
  .section-hdr {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    margin: 24px 0 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }
  .section-hdr h2 {
    font-size: 1.2rem;
    color: #ffffff;
  }
  .folio-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));
    gap: 18px;
  }
  @media (max-width: 560px) {
    .folio-grid { grid-template-columns: 1fr; }
  }
  .folio-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
  }
  .folio-card-hdr {
    display: flex;
    justify-content: space-between;
    padding: 8px 14px;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--muted);
    background: #0b1120;
    border-bottom: 1px solid var(--border);
  }
  .folio-card img {
    width: 100%;
    height: auto;
    display: block;
    background: #ffffff;
  }
  footer {
    text-align: center;
    padding: 28px 16px;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: 0.84rem;
  }
</style>
</head>
<body>

<header>
  <div class="badge-row">
    <span class="badge">U.S. PATENT PENDING (64/180,009)</span>
    <span class="badge cyan">845 PRIMARY RECORDS (386 TIC HOSTS &bull; 390 UNION)</span>
    <span class="badge">2,170 / 4,957 (43.78%) ON-TIME &bull; 0 WRONG IN 2,592 COVERED</span>
    <span class="badge cyan">80-KERNEL QEG5 ASTRO-PRIME ARENA (20,480 B)</span>
  </div>
  <h1>CHORD-SIEVES v2.4: Autonomous Exoplanet Discovery, 3-Zone Quadratic Flank-Bridge Vetting &amp; Continuous TESS Ephemeris Self-Audit Engine</h1>
  <p class="subtitle">
    Principal Architect: <strong>Logan Smith</strong> (Metaphy LLC) &bull; Co-Designed with <code>@AURA</code> (Gemini 4 Argon), <code>@LUMEN</code> (Gemma 4 E4B), &amp; <code>@BBB</code> (Qwen 3.5 9B) &bull; Peer-Reviewed by <code>@GROK</code>
  </p>
  <div class="cta-row">
    <a class="btn btn-primary" href="/BAMA_CHORD_SIEVES_Exoplanet_Report.pdf" download>Download 10-Page Scientific Report (PDF)</a>
    <a class="btn btn-cyan" href="/chord_sieves_public_verifier_sdk.zip" download>Download Read-Only Public Verifier SDK (.zip)</a>
    <a class="btn btn-outline" href="/arxiv/chord_sieves_arxiv_preprint.tex" download>Download Two-Column LaTeX Source (.tex)</a>
    <a class="btn btn-outline" href="https://bama-cortical-report.vercel.app" target="_blank" rel="noopener">Companion BAMA v3.1 Systems Paper &rarr;</a>
  </div>
</header>

<main class="container">
  <div class="kpi-grid">
    <div class="kpi"><div class="num">845 / 386</div><div class="lbl">Primary Records / TIC Hosts (390 Union)</div></div>
    <div class="kpi"><div class="num">809 / 25 / 11</div><div class="lbl">ExoFOP Cat A / Cat B / Cat C</div></div>
    <div class="kpi"><div class="num">600 (65 &le;1.6R<sub>&oplus;</sub>)</div><div class="lbl">Shirt-Sleeve Cut (0&ndash;35&deg;C)</div></div>
    <div class="kpi"><div class="num">8 (&ge;85%) / 6 KX02</div><div class="lbl">Competing Solutions (3 Host Stars)</div></div>
    <div class="kpi"><div class="num">2,170 / 4,957</div><div class="lbl">On-Time (43.78% | 0 Wrong in 2,592)</div></div>
    <div class="kpi"><div class="num">1,261</div><div class="lbl">Marked Follow-Up Registry Objects</div></div>
  </div>

  <div class="section-hdr">
    <h2>10-Page Print-Exact Scientific Folio (High-DPI Raster Scans)</h2>
    <span style="color: var(--muted); font-size: 0.85rem;">All 4 Public Verifier Gates Passed (SHA-256: <code>c7237583ff...255ba5</code>)</span>
  </div>

  <div class="folio-grid">
    <div class="folio-card"><div class="folio-card-hdr"><span>PAGE 1</span><span>Abstract, 386 Primary / 390 Union TIC Hosts &amp; KPI Summary</span></div><img src="/assets/pages/page-1.webp" alt="Page 1" loading="eager"></div>
    <div class="folio-card"><div class="folio-card-hdr"><span>PAGE 2</span><span>80-Kernel BAMA Astro-Prime QEG5 Cartridge (20,480 B)</span></div><img src="/assets/pages/page-2.webp" alt="Page 2" loading="eager"></div>
    <div class="folio-card"><div class="folio-card-hdr"><span>PAGE 3</span><span>11-Stage Autonomous CHORD-SIEVES Discovery Cascade</span></div><img src="/assets/pages/page-3.webp" alt="Page 3" loading="lazy"></div>
    <div class="folio-card"><div class="folio-card-hdr"><span>PAGE 4</span><span>3-Zone Quadratic Flank Bridge &amp; Stage 3.5 Vetting Math</span></div><img src="/assets/pages/page-4.webp" alt="Page 4" loading="lazy"></div>
    <div class="folio-card"><div class="folio-card-hdr"><span>PAGE 5</span><span>845-Record Discovery Catalog &amp; 1,261-Object Marked Registry</span></div><img src="/assets/pages/page-5.webp" alt="Page 5" loading="lazy"></div>
    <div class="folio-card"><div class="folio-card-hdr"><span>PAGE 6</span><span>Pipeline Priors, KX02 Ceiling &amp; Mutual Hill Stability Audit</span></div><img src="/assets/pages/page-6.webp" alt="Page 6" loading="lazy"></div>
    <div class="folio-card"><div class="folio-card-hdr"><span>PAGE 7</span><span>Self-Audit Ledger v2.4.0 (2,170 / 4,957 On-Time) &amp; Catchup</span></div><img src="/assets/pages/page-7.webp" alt="Page 7" loading="lazy"></div>
    <div class="folio-card"><div class="folio-card-hdr"><span>PAGE 8</span><span>Multi-Agent Co-Design &amp; @GROK Peer-Review Resolution</span></div><img src="/assets/pages/page-8.webp" alt="Page 8" loading="lazy"></div>
    <div class="folio-card"><div class="folio-card-hdr"><span>PAGE 9</span><span>Read-Only Public Verifier SDK &amp; Direct Recount Receipt</span></div><img src="/assets/pages/page-9.webp" alt="Page 9" loading="lazy"></div>
    <div class="folio-card"><div class="folio-card-hdr"><span>PAGE 10</span><span>Conclusions, Period-Alias Disambiguation, Patent 64/180,009</span></div><img src="/assets/pages/page-10.webp" alt="Page 10" loading="lazy"></div>
  </div>
</main>

<footer>
  &copy; 2026 Logan Smith (Metaphy LLC) &bull; Protected under U.S. Provisional Patent Application No. 64/180,009 (Confirmation #2200) &bull; All Rights Reserved.
</footer>

</body>
</html>
"""


def main() -> None:
    pdf_source_path = ROOT / "pdf-source.html"
    index_path = ROOT / "index.html"
    pdf_out_path = ROOT / "BAMA_CHORD_SIEVES_Exoplanet_Report.pdf"

    pdf_source_path.write_text(PDF_SOURCE_HTML, encoding="utf-8")
    index_path.write_text(INDEX_HTML, encoding="utf-8")

    ignore_text = ".vercel/\n*.log\n__pycache__/\ntemp_edge_profile/\n"
    (ROOT / ".gitignore").write_text(ignore_text, encoding="utf-8")
    (ROOT / ".vercelignore").write_text(ignore_text, encoding="utf-8")

    edge_candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    edge_exe = next((p for p in edge_candidates if pathlib.Path(p).exists()), None)
    assert edge_exe is not None, "Microsoft Edge executable not found"

    temp_profile = ROOT / "temp_edge_profile"
    if temp_profile.exists():
        shutil.rmtree(temp_profile, ignore_errors=True)
    temp_profile.mkdir(parents=True, exist_ok=True)

    file_url = pdf_source_path.resolve().as_uri()
    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        f"--user-data-dir={temp_profile}",
        f"--print-to-pdf={pdf_out_path}",
        "--no-pdf-header-footer",
        file_url,
    ]
    subprocess.run(cmd, check=True, timeout=60)
    shutil.rmtree(temp_profile, ignore_errors=True)

    doc = fitz.open(str(pdf_out_path))
    print(f"Rendered {pdf_out_path.name}: {len(doc)} pages ({pdf_out_path.stat().st_size:,} bytes)")
    assert len(doc) == 10, f"Expected exactly 10 pages, got {len(doc)}"

    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(dpi=180, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        webp_path = PAGES_DIR / f"page-{i}.webp"
        img.save(webp_path, "WEBP", quality=88)

    doc.close()

    # Re-zip Public Verifier SDK
    sdk_zip = ROOT / "chord_sieves_public_verifier_sdk.zip"
    with zipfile.ZipFile(sdk_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in (ROOT / "public-verifier").iterdir():
            if p.is_file():
                zf.write(p, p.name)

    arxiv_zip = ARXIV_DIR / "chord_sieves_arxiv_submission.zip"
    with zipfile.ZipFile(arxiv_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(ARXIV_DIR / "chord_sieves_arxiv_preprint.tex", "chord_sieves_arxiv_preprint.tex")

    zenodo_zip = ZENODO_DIR / "CHORD_SIEVES_v2_4_Zenodo_Archival_Bundle.zip"
    with zipfile.ZipFile(zenodo_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(pdf_out_path, pdf_out_path.name)
        zf.write(ARXIV_DIR / "chord_sieves_arxiv_preprint.tex", "chord_sieves_arxiv_preprint.tex")
        zf.write(sdk_zip, sdk_zip.name)
        for p in (ROOT / "public-verifier").iterdir():
            if p.is_file():
                zf.write(p, f"public-verifier/{p.name}")

    print(f"Updated {sdk_zip.name}, {arxiv_zip.name}, and {zenodo_zip.name}")


if __name__ == "__main__":
    main()
