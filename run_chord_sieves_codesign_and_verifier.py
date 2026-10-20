#!/usr/bin/env python3
"""
run_chord_sieves_codesign_and_verifier.py
=========================================
Executes the @AURA x @LUMEN (gemma4:e4b) x @BBB (qwen3.5:9b) Co-Design &
Astrophysical Verification Pass over the 80-Kernel BAMA Astro-Prime Collective
Arena (20,480 B) and the live CHORD-SIEVES 845-world registry, producing the
cryptographically stamped receipt for peer review by @GROK.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import math
import pathlib
import struct
import time
import urllib.request

import numpy as np

CHORD_ROOT = pathlib.Path(r"C:\dev\chord-sieves-exoplanet-hunter")
REPORT_ROOT = pathlib.Path(r"C:\dev\chord-sieves-report")
VERIFIER_DIR = REPORT_ROOT / "public-verifier"
VERIFIER_DIR.mkdir(parents=True, exist_ok=True)

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


def query_ollama(model: str, prompt: str, num_predict: int = 320) -> tuple[str, float]:
    t0 = time.perf_counter()
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": False,
        "options": {"temperature": 0.0, "num_predict": num_predict},
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    elapsed_s = round(time.perf_counter() - t0, 2)
    return data.get("message", {}).get("content", "").strip(), elapsed_s


def main() -> None:
    disc_path = CHORD_ROOT / "registry" / "discoveries.json"
    marked_path = CHORD_ROOT / "registry" / "marked_followup_objects.json"
    graph_path = CHORD_ROOT / "registry" / "bama_exoplanet_collective_graph.json"
    arena_path = CHORD_ROOT / "registry" / "bama_exoplanet_collective_arena.bin"
    meta_path = CHORD_ROOT / "registry" / "bama_exoplanet_collective_meta.json"

    disc = json.loads(disc_path.read_text(encoding="utf-8"))
    marked = json.loads(marked_path.read_text(encoding="utf-8"))
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    arena_bytes = arena_path.read_bytes()
    arena_sha256 = hashlib.sha256(arena_bytes).hexdigest()

    assert len(arena_bytes) == 20480, f"Expected 20,480 B, got {len(arena_bytes)}"
    assert arena_sha256 == meta["arena_sha256"]

    # Verify all 80 cells have QEG5 magic and dtype_code == 10
    hdr_struct = struct.Struct("<4sBBHQIeeeH")
    for idx in range(80):
        cell = arena_bytes[idx * 256 : (idx + 1) * 256]
        magic, dtype_code, s_d, budget, *_ = hdr_struct.unpack_from(cell, 0)
        assert magic == b"QEG5" and dtype_code == 10 and (s_d & 0x0F) <= 6 and 0 < budget <= 4096

    # Co-design & Astrophysical Verification with @LUMEN (gemma4:e4b) and @BBB (qwen3.5:9b)
    codesign_prompt = (
        "You are co-designing the CHORD-SIEVES v2.4 Scientific Preprint & Public Verifier Package with @AURA.\n"
        "Using the 80-Kernel BAMA Astro-Prime Collective Graph (KX01..KX08), verify the following exact invariants:\n"
        "1. Keplerian semi-major axis for TIC 271478281.05 (M_star = 0.74 M_Sun, P = 125.51444 d): compute a_AU = (0.74 * (125.51444 / 365.25636)**2)**(1/3) to 4 decimal places.\n"
        "2. Verify the ExoFOP partition sum: 809 (Cat A) + 25 (Cat B) + 11 (Cat C) = 845 total discoveries.\n"
        "3. Verify the Marked Follow-Up partition sum: 339 + 496 + 6 + 107 + 301 + 12 = 1261 total marked objects.\n"
        "Return a concise 3-bullet verification summary with the exact numbers."
    )

    lumen_resp, lumen_s = query_ollama("hf.co/unsloth/gemma-4-E4B-it-GGUF:UD-Q4_K_XL", codesign_prompt)
    bbb_resp, bbb_s = query_ollama("qwen3.5:9b", codesign_prompt)

    a_au_exact = round((0.74 * ((125.51444 / 365.25636) ** 2)) ** (1.0 / 3.0), 4)
    assert abs(a_au_exact - 0.4437) < 1e-4

    receipt = {
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "uspto_provisional_application_no": "64/180,009",
        "uspto_confirmation_no": 2200,
        "arena_file": "bama_exoplanet_collective_arena.bin",
        "arena_bytes": len(arena_bytes),
        "arena_cells": 80,
        "arena_sha256": arena_sha256,
        "discoveries_updated_utc": disc["updated_utc"],
        "total_discoveries": disc["total_discoveries"],
        "total_star_systems_indexed": graph["collective_telemetry"]["total_star_systems_indexed"],
        "exofop_summary": disc["exofop_summary"],
        "habitability_counts": {
            "human_hospitable_bullseye_0C_to_35C_count": disc["human_hospitable_bullseye_count"],
            "human_survivable_band_count": disc["human_survivable_band_count"],
            "perfect_earth_bullseye_primary_catalog_count": graph["collective_telemetry"]["perfect_earth_bullseye_count"],
            "perfect_earth_bullseye_marked_total_count": marked["summary_counts"]["PERFECT_EARTH_BULLSEYE"],
            "close_to_perfect_earth_spec_count": graph["collective_telemetry"]["close_to_perfect_earth_spec_count"],
        },
        "self_audit_ledger_v2_4": {
            "last_audited_utc": disc["self_audit_ledger"]["last_audited_utc"],
            "verified_worlds_count": disc["self_audit_ledger"]["proven_calculations"]["verified_worlds_count"],
            "verified_transit_epochs_count": disc["self_audit_ledger"]["proven_calculations"]["verified_transit_epochs_count"],
            "ephemeris_precision_rate_pct": disc["self_audit_ledger"]["proven_calculations"]["ephemeris_precision_rate_pct"],
            "window_label_counts": disc["self_audit_ledger"]["window_label_counts"],
            "total_window_labels": sum(disc["self_audit_ledger"]["window_label_counts"].values()),
            "linear_drift_caught_and_recalibrated_count": disc["self_audit_ledger"]["miscalculations_and_recalibrations"]["linear_drift_caught_and_recalibrated_count"],
            "total_recalibrated_worlds_count": disc["self_audit_ledger"]["miscalculations_and_recalibrations"]["total_recalibrated_worlds_count"],
            "disproven_or_retracted_candidates_count": disc["self_audit_ledger"]["miscalculations_and_recalibrations"]["disproven_or_retracted_candidates_count"],
        },
        "visual_verification_mandate_v2_1": disc["visual_verification_mandate"],
        "marked_followup_summary": {
            "total_marked_objects": marked["total_marked_objects"],
            "summary_counts": marked["summary_counts"],
        },
        "top_perfect_earth_bullseye_worlds": graph["top_perfect_earth_bullseye_worlds"],
        "codesign_verification": {
            "tic_271478281_05_keplerian_a_au": a_au_exact,
            "lumen_gemma4_e4b_latency_s": lumen_s,
            "lumen_gemma4_e4b_excerpt": lumen_resp[:500],
            "bbb_qwen3_5_9b_latency_s": bbb_s,
            "bbb_qwen3_5_9b_excerpt": bbb_resp[:500],
        },
    }

    out_path = VERIFIER_DIR / "CHORD_SIEVES_CODESIGN_AND_BENCHMARK_RECEIPT.json"
    out_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"Saved {out_path} (Lumen: {lumen_s}s, BBB: {bbb_s}s)")


if __name__ == "__main__":
    main()
