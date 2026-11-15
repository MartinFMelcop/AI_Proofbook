"""R02 native oracle: reversible intents/receipts, dual kit, side-profession and 3 encounters.
The trace is laboratory evidence, not a product/game balance claim.
"""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tests'))
from test_world_r02 import new,action,lib,shortest,FIELDS
s=new(6,17)
trace=[]
getters='revision x y quest herbs work_xp remedies health focus sp boss_hp boss_intent boss_phase defeats world_tick last_code ore ingots mining_xp smithing_xp kit_ward kit_echo kit_burn kit_mark kit_root kit_tempo kit_fatigue boss_pattern boss_turn weapon_grade'.split()

def native(t,v=0):
 before=s.revision;rc=action(s,t,v)
 assert 0<rc<10,(t,v,rc,before,s.revision)
 assert s.revision==before+1
 state={k:getattr(s,k) for k in getters}
 state.update(boss=s.active_boss,boss_target_x=s.target_x,boss_target_y=s.target_y)
 trace.append({'rev':before,'type':t,'value':v,'code':rc,'state':state,'beings':[lib.nsw_being_behavior(__import__('ctypes').byref(s),i) for i in range(1,5)]})
 return rc

def visit_node(x,y):
 for k in shortest(s,x,y):native(1,k)

def interact(id):
 visit_node(lib.nsw_object_x(id),lib.nsw_object_y(id));return native(2,id)
assert interact(1)==2
assert interact(2)==2
visit_node(18,7)
for _ in range(2):native(9,1)
visit_node(17,11)
for _ in range(2):native(9,2)
for _ in range(2):native(9,3)
assert (s.weapon_grade,s.ore,s.ingots)==(2,0,0)
assert interact(3)==1
assert interact(3)==2
assert interact(4)==2
for boss in range(1,4):
 assert interact(4+boss)==3
 for _ in range(120):
  if not s.active_boss:break
  if s.boss_intent==1:rc=native(4)
  elif s.health<=12 and s.remedies:rc=native(6)
  elif s.sp>=2 and s.boss_hp>3:rc=native(8, 1 if s.world_tick%3==0 else 0)
  else:rc=native(3)
  assert rc in (1,4,5)
 assert s.defeats==boss,(boss,s.defeats,s.health,s.quest)
assert s.quest==7
file=ROOT/'artifacts/R02_WORLD_NATIVE_TRACE.json'
obj={'source':'core/world_r02.cpp C++20 under libns_world_r02.so','abi':2,'profile':{'primary':6,'secondary':17},'events':trace,'status':'TECH_FIXTURE_ONLY','gate':'PRODUCT_NO_GO'}
file.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'accepted_intents':len(trace),'quest':s.quest,'defeats':s.defeats,'revision':s.revision,'weapon_grade':s.weapon_grade,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}))
