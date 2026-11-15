"""One deterministic, owner-replayed R03 SQLite ledger. Refuse overwrite of existing fixture."""
import json
from pathlib import Path
from world_r03_ledger import Ledger
root=Path(__file__).resolve().parent.parent
trace=json.loads((root/'artifacts/R03_WORLD_NATIVE_TRACE.json').read_text())
p=root/'artifacts/R03_SQLITE_WORLD_JOURNAL.sqlite'
L=Ledger(p,create=True)
try:
 L.create_session('fixture-r03-six-seventeen',6,17)
 for i,e in enumerate(trace['events']):
  r=L.submit('fixture-r03-six-seventeen','r03-a-'+str(i),e['rev'],e['type'],e['value'])
  if r['code']!=e['code'] or r['revision']!=e['state']['revision']:
   raise RuntimeError('journal diverged at '+str(i))
 r=L.verify('fixture-r03-six-seventeen')
 assert r['events']==len(trace['events'])
 print(json.dumps({'events':r['events'],'revision':r['revision'],'head':r['head'],'sqlite_path':p.name}))
finally:L.close()
