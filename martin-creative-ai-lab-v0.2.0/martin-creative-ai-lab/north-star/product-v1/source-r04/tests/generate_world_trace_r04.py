"""Original native C++20 source of accepted R04 intents, for independent Node WASM replay.
Exactly one C++ world authority. No simulation, proxy or canonical boss score.
"""
import sys,json,hashlib,ctypes as c
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tests'))
from test_world_r04 import new,action,lib,shortest,NAMES
s=new(6,17);trace=[]
getters='revision x y quest herbs work_xp remedies health focus sp boss_hp boss_intent boss_phase defeats world_tick last_code ore ingots mining_xp smithing_xp kit_ward kit_echo kit_burn kit_mark kit_root kit_tempo kit_fatigue boss_pattern boss_turn weapon_grade being_talk_mask research_last_class research_last_action boss_pressure'.split()
def native(t,v=0):
 before=s.revision;rc=action(s,t,v)
 assert 1<=rc<=6,('unexpected rejection',before,t,v,rc,s.health,s.active_boss)
 assert s.revision==before+1
 state={k:int(getattr(s,k)) for k in getters};state.update(boss=s.active_boss,boss_target_x=s.target_x,boss_target_y=s.target_y)
 trace.append({'rev':before,'type':t,'value':v,'code':rc,'state':state,'beings':[lib.nsw_being_behavior(c.byref(s),i) for i in range(1,5)],
 'threat':{'radius':lib.nsw_boss_threat_radius(c.byref(s)),
 'tiles':[lib.nsw_boss_threatens(c.byref(s),int(x),int(y)) for x,y in [(s.x,s.y),(s.target_x,s.target_y),(min(23,s.target_x+2),s.target_y),(23,19)]]}})
 return rc
def move_to(x,y):
 for direction in shortest(s,x,y):native(1,direction)
def interact(id):
 move_to(lib.nsw_object_x(id),lib.nsw_object_y(id));return native(2,id)
assert interact(1)==2
native(10,1) # guard remembers this bounded contact
assert interact(2)==2
move_to(18,7)
for _ in range(2):native(9,1)
move_to(17,11)
for _ in range(2):native(9,2)
for _ in range(2):native(9,3)
assert s.weapon_grade==2
assert interact(3)==1
assert interact(3)==2
assert interact(4)==2
for b in range(1,4):
 assert interact(b+4)==3
 for _ in range(150):
  if not s.active_boss:break
  if s.boss_intent==1:rc=native(4)
  elif s.health<=12 and s.remedies:rc=native(6)
  elif s.sp>=2 and s.boss_hp>4:rc=native(11 if s.world_tick%4==0 else 8,1 if s.world_tick%3==0 else 0)
  else:rc=native(3)
 assert s.defeats==b,('boss not naturally defeated',b,s.defeats,s.health,s.quest)
assert s.quest==7
obj={'schema':'mmai.r04.native-replay.v1','source':'core/world_r04.cpp/libns_world_r04.so','abi':4,'profile':{'primary':6,'secondary':17},'events':trace,'authority':'native C++20','canon':'NOT_CANON_LAB','gate':'PRODUCT_NO_GO'}
file=ROOT/'artifacts/R04_WORLD_NATIVE_TRACE.json';file.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'trace':'R04','events':len(trace),'quest':s.quest,'defeats':s.defeats,'revision':s.revision,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}))
