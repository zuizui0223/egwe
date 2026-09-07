from pathlib import Path

source = Path('scripts/tmp_route_reserve_final_sync.py').read_text(encoding='utf-8')
marker = '\nwf = Path(".github/workflows/nee-math-first-flagship.yml")\n'
if source.count(marker) != 1:
    raise RuntimeError('final-sync workflow boundary drifted')
prefix = source.split(marker, 1)[0] + '\n'
exec(compile(prefix, 'route-reserve-nonworkflow-sync', 'exec'), {})
