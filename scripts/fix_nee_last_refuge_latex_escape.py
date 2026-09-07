from pathlib import Path

article_path = Path("manuscript/nee_flagship_article.md")
article_bytes = article_path.read_bytes()

# Idempotent repair for the one display equation that was written through a
# non-raw Python string. Only the expected control-character forms are touched.
if b"\x0crac" in article_bytes:
    assert article_bytes.count(b"\x0crac") == 1
    article_bytes = article_bytes.replace(b"\x0crac", b"\\frac")
if b"\x0dight" in article_bytes:
    assert article_bytes.count(b"\x0dight") == 1
    article_bytes = article_bytes.replace(b"\x0dight", b"\\right")
if b"\x09heta_{10}" in article_bytes:
    assert article_bytes.count(b"\x09heta_{10}") == 1
    article_bytes = article_bytes.replace(b"\x09heta_{10}", b"\\theta_{10}")

expected_equation = (
    b"M_j=d_j(0.6q_j+0.3T_j+0.1G_j)-\\left(\\theta_{10}+"
    b"\\frac{\\operatorname{logit}(0.625)}{4.5}\\right),"
)
assert expected_equation in article_bytes, "corrected last-refuge equation not found"

bad_controls = sorted({byte for byte in article_bytes if byte < 32 and byte != 10})
assert not bad_controls, f"unexpected control bytes remain: {bad_controls}"
article_path.write_bytes(article_bytes)

article = article_path.read_text()
old_article = "direct eco-genetic feedback repairs interaction–bundle mismatch"
new_article = "direct eco-genetic feedback recouples interaction state toward the local trait/genetic bundle"
if old_article in article:
    assert article.count(old_article) == 1
    article = article.replace(old_article, new_article, 1)
assert new_article in article
article_path.write_text(article)

cover_path = Path("manuscript/nee_flagship_cover_letter.md")
cover = cover_path.read_text()
replacements = {
    "Direct eco-genetic feedback supplies a second repair route.":
        "Direct eco-genetic feedback supplies a distinct recoupling route.",
    "recruitment and direct feedback repair two different kinds of mismatch":
        "recruitment buffers trait–allele mismatch while direct feedback recouples interaction to the local bundle",
}
for old, new in replacements.items():
    if old in cover:
        assert cover.count(old) == 1
        cover = cover.replace(old, new, 1)
    assert new in cover
cover_path.write_text(cover)

print("NEE last-refuge LaTeX + operator-wording repair: PASS")
