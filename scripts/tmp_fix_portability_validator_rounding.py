from pathlib import Path

root = Path(__file__).resolve().parents[1]
p = root / "scripts/validate_publication_lanes.py"
text = p.read_text(encoding="utf-8")
old = '        "p=.694",\n'
new = '        ".693686",\n'
if text.count(old) != 1:
    raise RuntimeError(f"expected one legacy rounded token, found {text.count(old)}")
p.write_text(text.replace(old, new, 1), encoding="utf-8")
print("Updated portability validator to frozen Phase-U McNemar precision")
