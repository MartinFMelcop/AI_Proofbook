"""Create R02-only deterministic SQLite receipt chain from native trace; refuse overwrite.
This is a tool/test fixture, NOT the browser-save backend or multiplayer database.
"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from world_r02_ledger import Ledger
trace=json.loads((ROOT/'artifacts/R02_WORLD_NATIVE_TRACE.json').read_text())
path=ROOT/'artifacts/R02_SQLITE_WORLD_JOURNAL.sqlite'
ledger=Ledger(path,create=True)
try:
 ledger.create_session('fixture-r02-six-seventeen',trace['profile']['primary'],trace['profile']['secondary'])
 for i,ev in enumerate(trace['events']):
  receipt=ledger.submit('fixture-r02-six-seventeen',f'r02-{i:04}',ev['rev'],ev['type'],ev['value'])
  assert receipt['code']==ev['code'],(i,receipt,ev)
  assert receipt['revision']==ev['rev']+1,(i,receipt)
 output=ledger.verify('fixture-r02-six-seventeen')
 assert output['revision']==len(trace['events'])
 print(json.dumps({'sqlite_fixture':str(path.relative_to(ROOT)),'events':output['events'],'revision':output['revision'],'integrity':'PASS','NOTE':'not the game UI persistence'}))
finally:ledger.close()
