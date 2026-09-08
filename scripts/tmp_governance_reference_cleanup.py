from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def patch(path, old, new):
    p=ROOT/path
    text=p.read_text(encoding='utf-8')
    n=text.count(old)
    if n != 1:
        raise RuntimeError(f'{path}: expected one match, got {n}: {old[:120]!r}')
    p.write_text(text.replace(old,new,1),encoding='utf-8')


def prepend(path, banner):
    p=ROOT/path
    text=p.read_text(encoding='utf-8')
    if banner.splitlines()[0] in text[:500]:
        return
    p.write_text(banner.rstrip()+'\n\n'+text,encoding='utf-8')

patch(
    'REPRODUCIBILITY.md',
    'This repository is the **independent condition-recovery extension and two-lane submission orchestrator** for the eco-genetic warning study.',
    'This repository is the **independent condition-recovery extension and flagship-first submission orchestrator with two frozen fallback manuscripts** for the eco-genetic warning study.',
)

patch(
    'manuscript/artifact_index.md',
    '| active warning-validity manuscript | `manuscript/warning_validity.md` | none; presents the frozen full-denominator audit |\n| active state-validity manuscript | `manuscript/state_validity_and_empirical_measurement_gates.md` | none; presents locked representation, portability, and empirical-gate results |\n| machine-readable lane registry | `manuscript/publication_lanes.json` | claim ownership only |',
    '| active NEE flagship manuscript | `manuscript/nee_flagship_article.md` | integrates state/warning evidence and adds load-bearing operator/reserve results |\n| frozen warning-validity fallback | `manuscript/warning_validity.md` | preserves the six-rule audit; requires later holdout reporting before reactivation |\n| frozen state-validity fallback | `manuscript/state_validity_and_empirical_measurement_gates.md` | preserves locked representation/propagation results for possible later reactivation |\n| machine-readable lane registry | `manuscript/publication_lanes.json` | binding active/fallback/exclusivity state |',
)
patch(
    'manuscript/artifact_index.md',
    'The split does not regenerate, replace, or reinterpret any artifact listed below.',
    'The current routing change does not regenerate, replace, or reinterpret any artifact listed below. It changes submission governance only: the flagship is active and the standalone state/warning manuscripts are frozen fallbacks.',
)

old='''| lane | active manuscript | owned claims |\n|---|---|---|\n| warning validity | `warning_validity.md` | P3, P4, S27; the full-denominator interpretation of the six frozen rules |\n| state validity | `state_validity_and_empirical_measurement_gates.md` | joint-state representation, process-specific portability boundaries, empirical measurement/representation gates, residual origin/history, and cross-origin identifiability |\n\n`main_text.md` is an integrated source archive, not an active submission path.\nThe router in `publication_lanes.json` is fail-closed: a new reader-facing claim\nmust be assigned to exactly one active lane before publication.  Lane ownership\ndoes not modify any evidence status below.'''
new='''| role | current manuscript surface | claim status |\n|---|---|---|\n| active NEE flagship | `nee_flagship_article.md` | integrates state representation, operator-resolved mechanism, warning representation and continuous last-refuge fate ranking |\n| frozen warning fallback | `warning_validity.md` | P3/P4/S27 remain valid, but the manuscript is not submission-current until later holdout evidence is integrated/reported |\n| frozen state fallback | `state_validity_and_empirical_measurement_gates.md` | representation/propagation claims remain valid as fallback evidence |\n\n`main_text.md` is an integrated source archive, not an active submission path. The router in `publication_lanes.json` is fail-closed: the active flagship explicitly registers reused fallback evidence and flagship-only load-bearing evidence; overlapping fallbacks cannot be simultaneously active. Routing does not modify any evidence status below.'''
patch('manuscript/claim_evidence_map.md',old,new)

prepend(
    'manuscript/main_story_revision.md',
    '# HISTORICAL STORY-REVISION NOTE — NOT CURRENT PUBLICATION ROUTER\n\n> This note predates the flagship-first governance state. Current routing is defined by `publication_lanes.json`, `PUBLICATION_LANES.md`, and `EG_SERIES_SUBMISSION_STATUS_2026-09-08.md`.',
)

print('Cleaned stale publication-reference labels')
