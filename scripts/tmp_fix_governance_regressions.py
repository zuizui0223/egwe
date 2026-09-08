from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def replace(path, old, new):
    p=ROOT/path
    text=p.read_text(encoding='utf-8')
    if text.count(old) != 1:
        raise RuntimeError(f'{path}: anchor count {text.count(old)} for {old[:100]!r}')
    p.write_text(text.replace(old,new,1),encoding='utf-8')

replace(
    'README.md',
    'The four-layer series remains a useful **scientific decomposition**. It is not a declaration that all four component manuscripts are simultaneously active. `manuscript/main_text.md` is an integrated source archive, and `manuscript/grand_synthesis_flagship.md` is the superseded initial flagship spine.\n',
    'The four-layer series remains a useful **scientific decomposition**. It is not a declaration that all four component manuscripts are simultaneously active. `manuscript/main_text.md` is an integrated source archive, and `manuscript/grand_synthesis_flagship.md` is the superseded initial flagship spine.\n\nThe retained **scientific condition spine** is `C0 → C1 → C2 → C3 → C4`: these are evidence/condition labels, not publication lanes. In that spine, **warning is a downstream conditional outcome** evaluated only after the loss-generating state is defined.\n',
)
replace(
    'manuscript/README.md',
    'This table replaces the prior C0→C4→E manuscript-routing ladder. Condition labels remain useful scientific provenance, but they are not a second publication router.\n',
    'This table replaces the prior C0→C4→E manuscript-routing ladder. The retained scientific condition spine is `C0 → C1 → C2 → C3 → C4`; those labels remain scientific provenance, not a second publication router. Warning is a downstream conditional outcome after the loss-generating state is defined.\n',
)
replace(
    'manuscript/README.md',
    'No historical phase/status file overrides the current router.\n',
    'No historical phase/status file overrides the current router. Historical **phase-specific result notes** remain provenance only and do not compete with the current publication sources of truth.\n',
)
replace(
    'tests/test_natural_data_manuscript_spine.py',
    '    assert natural["status"] == "development_go_primary_ecological_indicators"\n    assert natural["primary_target"] == "Ecological Indicators"\n',
    '    assert natural["status"] == "migrated_authoritative_in_egwee"\n    assert natural["authoritative_repository"] == "zuizui0223/egwee"\n    assert natural["primary_target"] == "Ecological Indicators"\n',
)
print('Applied governance regression fixes')
