from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f'{path}: expected one anchor, found {n}: {old[:100]!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')

replace_once(
    'manuscript/README.md',
    '| EGC | biological-state separation | independent parent paper |',
    '| EGC | **NEE Question 1:** biological-state separation under fragmentation | **load-bearing evidence imported into active NEE flagship; no separate active submission** |'
)
replace_once(
    'manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md',
    '| EGC | `zuizui0223/eco-genetic-criticality` | independent parent manuscript | separate mechanism/state-separation paper |',
    '| EGC | `zuizui0223/egc` | **load-bearing NEE Question 1 evidence source** | absorbed into the active NEE flagship; standalone manuscript retained only as provenance/fallback |'
)
replace_once(
    'manuscript/EG_SERIES_SUBMISSION_STATUS_2026-09-08.md',
    'But the current submission execution is different. The NEE flagship absorbs the state and warning evidence and adds new load-bearing operator/reserve evidence. Therefore the state and warning papers cannot remain concurrently active without creating substantial-overlap and exclusivity conflicts.',
    'But the current submission execution is different. The NEE flagship is explicitly a **two-question paper**: Question 1 imports the EGC state-separation evidence, and Question 2 combines EGWE representation, operator and warning/reserve evidence. The state and warning fallback papers therefore cannot remain concurrently active, and EGC is not a separate active submission in this programme.'
)
replace_once(
    'RELEASE_READINESS.md',
    'Mechanistic parent: theorem-guided interaction/fragmentation framework, finite-model evidence ledger, and biological-state separation. Its standalone manuscript does not own forecast sufficiency or predictive warning validity.',
    'Mechanistic evidence parent for **NEE Question 1**: theorem-guided interaction/fragmentation framework, finite-model evidence ledger, and biological-state separation. Its standalone manuscript is retained as provenance/fallback rather than a separate active submission; forecast sufficiency and predictive warning validity belong to NEE Question 2 in EGWE.'
)
print('closed EGC separate-submission routing drift')
