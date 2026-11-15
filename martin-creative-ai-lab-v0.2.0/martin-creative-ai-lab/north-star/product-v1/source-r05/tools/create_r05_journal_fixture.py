import sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from world_r05_ledger import Ledger
fixture=json.loads((R/'artifacts/R05_WORLD_NATIVE_TRACE.json').read_text())
p=R/'artifacts/R05_SQLITE_WORLD_JOURNAL.sqlite'
ledger=Ledger(p,create=True)
try:
 ledger.create_session('fixture-r05-six-seventeen',fixture['profile']['primary'],fixture['profile']['secondary'])
 for i,event in enumerate(fixture['events']):
  out=ledger.submit('fixture-r05-six-seventeen',f'r05-event-{i:03d}',event['rev'],event['type'],event['value'])
  assert out['code']==event['code'] and out['revision']==event['state']['revision']
 print(json.dumps(ledger.verify('fixture-r05-six-seventeen')))
finally:ledger.close()
