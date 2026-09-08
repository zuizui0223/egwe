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

print("Normalized portability overlap wording safely")
