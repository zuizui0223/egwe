from pathlib import Path

root = Path(__file__).resolve().parents[1]

validator = root / "scripts/validate_publication_lanes.py"
text = validator.read_text(encoding="utf-8")
text = text.replace('"p=.811",', '".811",').replace('"p=.728",', '".728",')
validator.write_text(text, encoding="utf-8")

manuscript = root / "manuscript/operator_portability.md"
text = manuscript.read_text(encoding="utf-8")
old = "This development lane is deliberately **not** a compressed version of the flagship. It does not use the `0.2543` aligned/anti-aligned counterexample, the `+5.33/+5.20` propagation contrasts, the 35/48/33/49 warning denominators, q-dependent sorting DID, recruitment buffering, direct recoupling, density-gate result, exact route-margin sign audit, or last-refuge AUC."
new = "This development lane is deliberately **not** a compressed version of the flagship. It excludes the state-alignment, horizon-propagation, warning-denominator, operator-balance and last-refuge evidence owned by the active flagship; the binding exclusion set is the flagship evidence registry in `publication_lanes.json`."
if text.count(old) != 1:
    raise RuntimeError(f"operator portability overlap paragraph count={text.count(old)}")
manuscript.write_text(text.replace(old, new, 1), encoding="utf-8")

state = root / "manuscript/state_validity_and_empirical_measurement_gates.md"
text = state.read_text(encoding="utf-8")
title = "# Matching eco-genetic summaries can hide different ecological futures"
banner = "# FROZEN FALLBACK — NOT FOR SIMULTANEOUS SUBMISSION"
if not text.startswith(banner + "\n\n"):
    raise RuntimeError("state frozen banner is not in expected temporary position")
marker = "\n\n" + title + "\n"
if text.count(marker) != 1:
    raise RuntimeError(f"state title anchor count={text.count(marker)}")
prefix, remainder = text.split(marker, 1)
if prefix.splitlines()[0] != banner:
    raise RuntimeError("unexpected state pre-title content")
state.write_text(title + "\n\n" + prefix + "\n\n" + remainder, encoding="utf-8")

print("Normalized portability overlap wording and preserved state title")
