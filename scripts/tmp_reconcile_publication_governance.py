from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def write(path, text):
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(path, old, new):
    text = read(path)
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{path}: expected one match, got {n}: {old[:120]!r}")
    write(path, text.replace(old, new, 1))


def replace_section(path, start, end, replacement):
    text = read(path)
    i = text.index(start)
    j = text.index(end, i)
    write(path, text[:i] + replacement.rstrip() + "\n\n" + text[j:])


def prepend_once(path, banner):
    text = read(path)
    if banner.splitlines()[0] in text[:500]:
        return
    write(path, banner.rstrip() + "\n\n" + text)


# Historical status now explicitly superseded.
prepend_once(
    "manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-05.md",
    "# SUPERSEDED — historical status only\n\n> This 2026-09-05 routing state was superseded after PR #165 made the NEE flagship a complete load-bearing manuscript. The current operational source of truth is `EG_SERIES_SUBMISSION_STATUS_2026-09-08.md`. Do not use the optional-flagship / four-simultaneous-ready-paper language below for submission decisions.",
)

# Root README: one routing surface and one crosswalk, instead of parallel ladders.
replace_section(
    "README.md",
    "## Active publication paths",
    "## Central result",
    """## Publication routing

There is **one active EGWE submission lane**: [`manuscript/nee_flagship_article.md`](manuscript/nee_flagship_article.md), currently routed to **Nature Ecology & Evolution**. The standalone state-validity and warning-validity manuscripts are **frozen fallback** packages and must not be submitted simultaneously with the overlapping flagship.

The binding machine router is [`manuscript/publication_lanes.json`](manuscript/publication_lanes.json); the human-readable contract is [`manuscript/PUBLICATION_LANES.md`](manuscript/PUBLICATION_LANES.md); the current operational status is [`manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md`](manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md).

### Publication crosswalk

| programme layer | scientific question | current surface | status |
|---|---|---|---|
| EGC | what biological states separate under fragmentation? | `zuizui0223/eco-genetic-criticality` | independent parent paper |
| EGWE state | what representation preserves future-relevant distinctions? | evidence incorporated into `nee_flagship_article.md`; standalone state manuscript retained | frozen fallback |
| EGWE warning | when is an early signal actually fate-discriminative? | binary audit + continuous last-refuge holdout in `nee_flagship_article.md`; standalone warning manuscript retained | frozen fallback |
| EGWEE | when does an empirical measurement earn state/proxy status? | `zuizui0223/egwee` | independent empirical programme |
| EGWE flagship | how do representation, operators and strongest-local reserve jointly determine vulnerability and predictability? | `nee_flagship_article.md` | **active primary submission** |

The four-layer series remains a useful **scientific decomposition**. It is not a declaration that all four component manuscripts are simultaneously active. `manuscript/main_text.md` is an integrated source archive, and `manuscript/grand_synthesis_flagship.md` is the superseded initial flagship spine.
""",
)
replace_section(
    "README.md",
    "## Scientific sources of truth",
    "## Reproduce and package",
    """## Scientific sources of truth

For current publication decisions, use this order:

1. `manuscript/publication_lanes.json` — binding submission state, exclusivity and fallback reactivation rules;
2. `manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md` and `manuscript/PUBLICATION_LANES.md` — human-readable operational routing;
3. the active flagship (`nee_flagship_article.md` + `nee_flagship_source_manifest.json`) and its locked artifacts/result notes.

`claim_evidence_map.md`, `artifact_index.md`, hypothesis ledgers and historical phase/status documents remain provenance/evidence maps; they do not override the current submission router. `main_text.md` and `grand_synthesis_flagship.md` are archives, not active competing manuscripts.
""",
)

# Manuscript workspace router.
replace_section(
    "manuscript/README.md",
    "## Active manuscripts",
    "The manuscript is downstream of the scientific condition map.",
    """## Active and fallback manuscripts

| role | manuscript | current status |
|---|---|---|
| NEE flagship | [`nee_flagship_article.md`](nee_flagship_article.md) | **active primary submission** |
| state validity | [`state_validity_and_empirical_measurement_gates.md`](state_validity_and_empirical_measurement_gates.md) | **frozen fallback** |
| warning validity | [`warning_validity.md`](warning_validity.md) | **frozen fallback; later holdout evidence must be integrated/reported before reactivation** |

The binding router is [`publication_lanes.json`](publication_lanes.json), the claim/exclusivity contract is [`PUBLICATION_LANES.md`](PUBLICATION_LANES.md), and the current status is [`EG_SERIES_SUBMISSION_STATUS_2026-09-08.md`](EG_SERIES_SUBMISSION_STATUS_2026-09-08.md). [`main_text.md`](main_text.md) is an integrated archive. [`grand_synthesis_flagship.md`](grand_synthesis_flagship.md) is the superseded initial flagship spine.

""",
)
replace_section(
    "manuscript/README.md",
    "## Publication logic",
    "## Current evidence",
    """## Publication crosswalk

The series logic and the submission router are deliberately separated:

| layer | question | execution now |
|---|---|---|
| EGC | biological-state separation | independent parent paper |
| EGWE state | representation adequacy | incorporated into active flagship; standalone fallback frozen |
| EGWE warning | fate discrimination | binary failure plus continuous last-refuge result incorporated into active flagship; standalone fallback frozen |
| EGWEE | empirical state/proxy adequacy | independent `zuizui0223/egwee` programme |
| EGWE flagship | integrated operator + reserve explanation/prediction | active NEE submission lane |

This table replaces the prior C0→C4→E manuscript-routing ladder. Condition labels remain useful scientific provenance, but they are not a second publication router.
""",
)
replace_section(
    "manuscript/README.md",
    "## Publication sources of truth",
    "## Main line",
    """## Publication sources of truth

1. [`publication_lanes.json`](publication_lanes.json) — binding active/fallback/exclusivity state;
2. [`EG_SERIES_SUBMISSION_STATUS_2026-09-08.md`](EG_SERIES_SUBMISSION_STATUS_2026-09-08.md) and [`PUBLICATION_LANES.md`](PUBLICATION_LANES.md) — human-readable routing;
3. [`nee_flagship_article.md`](nee_flagship_article.md) and [`nee_flagship_source_manifest.json`](nee_flagship_source_manifest.json) — active manuscript and evidence contract;
4. locked preregistrations, result notes, `claim_evidence_map.md`, `artifact_index.md` and historical manuscripts — provenance/fallback evidence only.

No historical phase/status file overrides the current router.
""",
)

# State and warning surfaces are visibly frozen fallbacks.
prepend_once(
    "manuscript/cover_letter.md",
    "# FROZEN FALLBACK — NOT FOR SUBMISSION WHILE NEE FLAGSHIP IS ACTIVE\n\n> **REACTIVATION GATE:** use this state-validity cover letter only after the NEE flagship is no longer under consideration (withdrawn, rejected without transfer, or explicitly abandoned), then perform a fresh author exclusivity confirmation and live journal-policy check.",
)
replace_once(
    "manuscript/cover_letter.md",
    "[EXCLUSIVITY CONFIRMATION: The manuscript is not published, accepted, or under consideration elsewhere.]",
    "[REACTIVATION GATE: Before using this fallback letter, confirm that the overlapping NEE flagship is no longer under consideration and that this manuscript is not published, accepted, or under consideration elsewhere.]",
)
prepend_once(
    "manuscript/warning_validity.md",
    "# FROZEN FALLBACK — NOT CURRENT-EVIDENCE COMPLETE FOR SUBMISSION\n\n> The six-rule full-denominator audit below remains scientifically valid, but this standalone warning manuscript was frozen before the prospectively locked continuous last-refuge holdout. While the NEE flagship is active, this manuscript is not a simultaneous submission. Before any later reactivation, it must incorporate or explicitly report the last-refuge result (AUC 0.92734, +0.02135 beyond co-timed max q) and the predeclared `H_alpha` directional inversion (AUC 0.23253) without post-hoc sign rescue.",
)
prepend_once(
    "manuscript/grand_synthesis_flagship.md",
    "# SUPERSEDED INITIAL FLAGSHIP SPINE — PROVENANCE ONLY\n\n> This was the 2026-09-05 initial synthesis spine. It is superseded by the complete active manuscript `nee_flagship_article.md` and must not be treated as a competing flagship or submission source of truth.",
)
replace_once(
    "manuscript/main_text.md",
    "> The two active publication paths are declared in `PUBLICATION_LANES.md` and\n> `publication_lanes.json`.",
    "> The current active/fallback publication state is declared in `PUBLICATION_LANES.md` and\n> `publication_lanes.json`; the NEE flagship is active and the state/warning papers are frozen fallbacks.",
)

# Report the omitted H_alpha comparator in the actual flagship manuscript.
replace_once(
    "manuscript/nee_flagship_article.md",
    "Mean q, mean population and `H_gamma` had lower AUCs of 0.88944, 0.85010 and 0.86223, respectively.",
    "Mean q, mean population and `H_gamma` had lower AUCs of 0.88944, 0.85010 and 0.86223, respectively. Under the same predeclared orientation in which lower state implied higher future-loss risk, `H_alpha` was **directionally inverted** (AUC **0.23253**). We did not reverse its sign post hoc and reclassify it as a successful warning; the inversion is retained as a boundary on the assumed warning direction.",
)
replace_once(
    "docs/LAST_REFUGE_WARNING_HOLDOUT_RESULTS_2026-09-07.md",
    "The `H_alpha` direction is notably opposite to the predeclared lower-is-higher-risk score convention in this ensemble: event trajectories had higher mean `H_alpha` at the observation time than non-events. This does not alter the earlier frozen-threshold result; it reinforces that marginal diversity state and functional-fate information are not interchangeable.",
    "The `H_alpha` result is **directionally inverted** relative to the predeclared lower-is-higher-risk score convention in this ensemble: event trajectories had higher mean `H_alpha` at the observation time than non-events, yielding AUC **0.23253** in the frozen direction. We do **not** flip its sign post hoc to manufacture a successful warning comparator. This does not alter the earlier frozen-threshold result; it records a recovered directional boundary and reinforces that marginal diversity state and functional-fate information are not interchangeable.",
)
replace_once(
    "manuscript/nee_flagship_display_plan.md",
    "- co-timed max-q AUC **0.90598** `[0.90078,0.91118]`;\n",
    "- co-timed max-q AUC **0.90598** `[0.90078,0.91118]`;\n- predeclared lower-is-higher-risk `H_alpha` comparator AUC **0.23253** (directionally inverted; no post-hoc sign rescue);\n",
)

# Submission metadata: explicit governance and comparator accounting.
meta = read("manuscript/nee_flagship_submission_metadata.md")
anchor = "## Submission overlap rule"
insert = """## Publication governance — flagship-first

This repository currently has **one active EGWE submission lane**: this NEE flagship. The standalone state-validity and warning-validity manuscripts are frozen fallbacks and are not simultaneously submittable while the flagship is under consideration. This flagship-first state is governed by `publication_lanes.json` schema 4 and `EG_SERIES_SUBMISSION_STATUS_2026-09-08.md`.

The warning comparator panel is reported without outcome-based direction changes. Under the predeclared lower-state=higher-risk orientation, co-timed `H_alpha` had AUC **0.23253** and was therefore **directionally inverted**. Its sign is not flipped post hoc to claim success. If the standalone warning fallback is ever reactivated, this later holdout and inversion must be incorporated or explicitly reported.

"""
if insert.strip() not in meta:
    if meta.count(anchor) != 1:
        raise RuntimeError("submission metadata overlap-rule anchor drifted")
    meta = meta.replace(anchor, insert + anchor, 1)
    write("manuscript/nee_flagship_submission_metadata.md", meta)

# Project boundary now follows the actual router.
replace_section(
    "docs/PROJECT_BOUNDARY.md",
    "## Publication boundary inside this repository",
    "## Prohibited shortcuts",
    """## Publication boundary inside this repository

The repository exposes **one active EGWE submission manuscript**, `manuscript/nee_flagship_article.md`. The standalone warning- and state-validity manuscripts are frozen fallback packages. They remain valid provenance/reproducibility surfaces but cannot be simultaneously submitted with the overlapping flagship.

The binding router is `manuscript/publication_lanes.json` (schema 4). Fallback reactivation requires the flagship to be no longer under consideration plus the author-controlled gates recorded there. In particular, the warning fallback must incorporate or explicitly report the later last-refuge holdout before reactivation.

`manuscript/main_text.md` is an integrated archive and `manuscript/grand_synthesis_flagship.md` is a superseded initial spine. Neither is an active submission.
""",
)

# Release ledger: replace the stale lane-count claims while preserving historical evidence notes.
replace_once(
    "RELEASE_READINESS.md",
    "- [x] two active EGWE manuscript paths and their disjoint claim ownership are fixed in `manuscript/publication_lanes.json`",
    "- [x] one active EGWE NEE flagship lane plus two frozen non-simultaneous fallbacks are fixed in `manuscript/publication_lanes.json` schema 4",
)
replace_once(
    "RELEASE_READINESS.md",
    "Owns two active manuscript lanes: state representation/horizon-dependent propagation/process portability, and warning predictive validity. The integrated source archive remains provenance only.",
    "Owns one active NEE flagship submission lane integrating state representation, operator-resolved mechanism and warning representation, with state/warning standalone manuscripts retained as frozen fallbacks. The integrated source archive remains provenance only.",
)

print("Applied bounded publication-governance reconciliation")
