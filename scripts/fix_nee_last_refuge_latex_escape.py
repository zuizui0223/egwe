from pathlib import Path

path = Path("manuscript/nee_flagship_article.md")
data = path.read_bytes()

# The manuscript-integration helper used a non-raw Python string for one display
# equation. Repair only the control-character forms that can result from
# \t, \f, and \r escapes, then verify the exact intended equation is present.
if data.count(b"\x09heta_{10}") == 1:
    data = data.replace(b"\x09heta_{10}", b"\\theta_{10}")
assert data.count(b"\x0crac") == 1, "expected exactly one form-feed corruption before rac"
data = data.replace(b"\x0crac", b"\\frac")
assert data.count(b"\x0dight") == 1, "expected exactly one carriage-return corruption before ight"
data = data.replace(b"\x0dight", b"\\right")

expected = (
    b"M_j=d_j(0.6q_j+0.3T_j+0.1G_j)-\\left(\\theta_{10}+"
    b"\\frac{\\operatorname{logit}(0.625)}{4.5}\\right),"
)
assert expected in data, "corrected last-refuge equation not found"

bad_controls = sorted({byte for byte in data if byte < 32 and byte != 10})
assert not bad_controls, f"unexpected control bytes remain: {bad_controls}"

path.write_bytes(data)
print("NEE last-refuge LaTeX escape repair: PASS")
