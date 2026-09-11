from pathlib import Path
p = Path('.github/workflows/nee-math-first-flagship.yml')
text = p.read_text(encoding='utf-8')
old = 'cdaf155817153fb10115116808aa89ca87831c9e'
new = '5e16e861a769ab56da5bef14c68b0297dea05ef5'
count = text.count(old)
if count != 2:
    raise RuntimeError(f'expected 2 old EGWEE pins, found {count}')
p.write_text(text.replace(old, new), encoding='utf-8')
print('updated NEE EGWEE projection pin')
