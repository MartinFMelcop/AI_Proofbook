"""Oracle: one actual native C++ completed journey, for differential WASM regression."""
import json,ctypes as c,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from test_world import new,action,shortest,lib
ROOT=Path(__file__).resolve().parent.parent
s=new(6,17)
trace=[]
FIELDS='revision x y quest herbs work_xp remedies health focus sp active_boss boss_hp boss_intent target_x target_y boss_phase defeats world_tick last_code'.split()
def take(t,v=0):
 rev=s.revision;rc=action(s,t,v)
 rec={'rev':rev,'type':t,'value':v,'code':rc,'state':{k:getattr(s,k) for k in FIELDS}}
 trace.append(rec)
 return rc

def visit(id):
 for k in shortest(s,lib.nsw_object_x(id),lib.nsw_object_y(id)):
  assert take(1,k) in (1,)
 return take(2,id)
assert visit(1)==2
assert visit(2)==2
assert visit(3)==1
assert visit(3)==2
assert visit(4)==2
for boss in range(1,4):
 assert visit(4+boss)==3
 for n in range(80):
  if s.active_boss==0:break
  if s.boss_intent==1:rc=take(4)
  elif s.health<=10 and s.remedies:rc=take(6)
  else:rc=take(3)
  assert rc in (1,4,5)
 assert s.active_boss==0 and s.defeats==boss
assert s.quest==7
out={'schema':'mmai.product.world.trace.v1','inputs':{'primary':6,'secondary':17},'trace':trace,'final':trace[-1]['state']}
p=ROOT/'artifacts/WORLD_NATIVE_TRACE.json';p.parent.mkdir(exist_ok=True)
p.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'output':str(p),'events':len(trace),'finalQuest':s.quest,'defeats':s.defeats,'finalHealth':s.health}))
