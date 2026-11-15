import ctypes as c,json,sys,hashlib
from pathlib import Path
from test_world_r05 import State,Cmd,LIB,NAMES
R=Path(__file__).resolve().parents[1]
prior=json.loads((R/'artifacts/R04_WORLD_NATIVE_TRACE.json').read_text())
s=State();assert LIB.nsw_create(c.byref(s),prior['profile']['primary'],prior['profile']['secondary'])==1
entries=[]
for index,ev in enumerate(prior['events']):
 assert s.revision==ev['rev'];rc=LIB.nsw_apply(c.byref(s),c.byref(Cmd(5,s.revision,ev['type'],ev['value'])))
 assert rc==ev['code'],index
 aliases={'boss':'active_boss','boss_target_x':'target_x','boss_target_y':'target_y'}
 fields={n:int(getattr(s,aliases.get(n,n))) for n in ev['state']}
 assert fields==ev['state'],(index,[k for k in fields if fields[k]!=ev['state'].get(k)])
 entries.append({**ev,'facings':[LIB.nsw_being_facing(i,s.world_tick) for i in range(1,5)]})
assert len(entries)==121
j={'schema':'mmai.r05.native-replay.v1','source':'core/world_r05.cpp executable shared library, not copied R04 output','abi':5,'profile':prior['profile'],'events':entries,'conclusion':'121 accepted actions same historical decisions; new independent facing observables'}
d=R/'artifacts/R05_WORLD_NATIVE_TRACE.json';d.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':'PASS','events':len(entries),'sha256':hashlib.sha256(d.read_bytes()).hexdigest()}))
