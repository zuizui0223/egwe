from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "manuscript/nee_flagship_article.md"

old_natural = """A separately protocol-locked five-cluster natural synthesis provides bounded external-consistency evidence rather than validation. Under its source-supported paired-dependence reconstruction, the global intersection test gave Fisher `p=0.0121`; omitting *Serapias* gave `p=0.1819`. A zero-covariance sensitivity remained below 0.05 (`p=0.0386`), but a covariance-free Cauchy–Schwarz certification bound did not (`p=0.2806`). The natural inference is therefore conditional on within-system dependence information and is reported in full separately; it is not used to validate the finite operators here."""
new_natural = """An independently protocol-locked five-cluster natural synthesis provides bounded external-consistency evidence but is not load-bearing here. Its source-supported paired-dependence test gave Fisher `p=0.0121`; omitting *Serapias* gave `p=0.1819`. Zero covariance gave `p=0.0386`, whereas a covariance-free Cauchy–Schwarz bound gave `p=0.2806`. Natural inference is therefore dependence-conditional and does not validate the finite operators."""

old_prediction = """These finite results make two testable natural-system predictions rather than claims of external validation. First, fragmentation responses should differ among interaction, reproductive, demographic and genetic layers in magnitude or timing. Second, the degree and timing of discordance should covary with independently measured movement, reproductive assurance, pollination mode and cohort or landscape history. The separate natural synthesis evaluates the first prediction; future moderator analyses can address the second without converting either result into validation of the finite operators."""
new_prediction = """These finite results predict that fragmentation responses can diverge among biological layers, and that discordance should covary with movement, reproductive assurance, pollination mode and cohort or landscape history. The separate natural synthesis evaluates the first prediction; future moderator analyses can test the second without validating the finite operators."""

old_generality = """Two kinds of result require different claim ceilings. The transition-sufficiency result is constructive: if two admissible states share the declared marginal representation but have different exact transitions, then those marginals cannot be universally sufficient for every system admitted by that representation. Likewise, temporal precedence does not logically entail fate discrimination, because sensitivity 1 and specificity 0 can coexist. These are **non-implication results**. Their force does not depend on the numerical values `0.2543`, `q*=0.625` or any particular generation generalizing to nature."""
new_generality = """The transition-sufficiency result is constructive: two admissible states can share the declared marginals yet have different exact transitions, so those marginals cannot be universally sufficient. Likewise, temporal precedence does not entail fate discrimination because sensitivity 1 and specificity 0 can coexist. These **non-implication results** do not depend on `0.2543`, `q*=0.625` or any particular generation generalizing to nature."""

text = ARTICLE.read_text(encoding="utf-8")
for old, new, label in (
    (old_natural, new_natural, "natural boundary"),
    (old_prediction, new_prediction, "prediction paragraph"),
    (old_generality, new_generality, "generality paragraph"),
):
    assert text.count(old) == 1, f"{label}: expected one match"
    text = text.replace(old, new, 1)

ARTICLE.write_text(text, encoding="utf-8")
print("Trimmed NEE reframe below working main-text ceiling")
