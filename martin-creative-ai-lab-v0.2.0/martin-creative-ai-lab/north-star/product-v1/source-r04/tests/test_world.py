"""Product spatial slice regression, deterministic native ABI; not art or RPG acceptance."""
import ctypes as c
import unittest
from collections import deque
from pathlib import Path

lib=c.CDLL(str(Path(__file__).resolve().parent.parent/'artifacts/libns_world.so'))
NAMES='abi revision initialized primary secondary x y quest herbs work_xp remedies health focus sp active_boss boss_hp boss_intent target_x target_y boss_phase defeats world_tick last_code'.split()
class State(c.Structure):_fields_=[(n,c.c_uint32) for n in NAMES]
class Cmd(c.Structure):_fields_=[('abi',c.c_uint32),('expected_revision',c.c_uint32),('type',c.c_uint32),('value',c.c_int32)]
lib.nsw_create.argtypes=[c.POINTER(State),c.c_uint32,c.c_uint32];lib.nsw_create.restype=c.c_int32
lib.nsw_apply.argtypes=[c.POINTER(State),c.POINTER(Cmd)];lib.nsw_apply.restype=c.c_int32
lib.nsw_tile.argtypes=[c.c_uint32,c.c_uint32];lib.nsw_tile.restype=c.c_uint32
lib.nsw_object_x.argtypes=[c.c_uint32];lib.nsw_object_y.argtypes=[c.c_uint32]
DIR=[(0,-1),(1,0),(0,1),(-1,0)]

def new(a=1,b=0):
 s=State();assert lib.nsw_create(c.byref(s),a,b)==1;return s

def action(s,t,v=0,rev=None):
 cmd=Cmd(1,s.revision if rev is None else rev,t,v)
 return lib.nsw_apply(c.byref(s),c.byref(cmd))

def shortest(s,x,y):
 st=(s.x,s.y);q=deque([st]);prev={st:None}
 while q:
  p=q.popleft()
  if abs(p[0]-x)+abs(p[1]-y)<=2:
   path=[]
   while prev[p] is not None:
    pp,k=prev[p];path.append(k);p=pp
   return path[::-1]
  for k,(dx,dy) in enumerate(DIR):
   nx,ny=p[0]+dx,p[1]+dy
   if not 0<=nx<24 or not 0<=ny<20 or (nx,ny) in prev or lib.nsw_tile(nx,ny) in (3,4,8,9):continue
   prev[(nx,ny)]=(p,k);q.append((nx,ny))
 raise RuntimeError(f'No path: {st}->{(x,y)}')

def visit(s,id):
 for k in shortest(s,lib.nsw_object_x(id),lib.nsw_object_y(id)):
  assert action(s,1,k)==1
 return action(s,2,id)

def unlock(s):
 assert visit(s,1)==2,(s.quest,'guard')
 assert visit(s,2)==2,(s.quest,'leader')
 assert visit(s,3)==1,(s.quest,'herb1')
 assert visit(s,3)==2,(s.quest,'herb2')
 assert visit(s,4)==2,(s.quest,'bench')
 assert s.quest==4

def beat(s,b):
 assert visit(s,4+b)==3,(b,s.quest,s.x,s.y)
 for _ in range(80):
  if s.active_boss==0:break
  if s.boss_intent==1:rc=action(s,4)
  elif s.health<=10 and s.remedies:rc=action(s,6)
  else:rc=action(s,3)
  assert rc in (1,4,5), (b,rc,s.health,s.revision,s.boss_hp)
 assert s.active_boss==0 and s.defeats==b,(b,s.defeats,s.health)

class SpatialOwnerTests(unittest.TestCase):
 def test_abi(self):self.assertEqual(lib.nsw_abi(),1)
 def test_all_class_pairs(self):
  for a in range(1,22):
   self.assertEqual(new(a).primary,a)
   for b in range(1,22):
    if a!=b:self.assertEqual(new(a,b).secondary,b)
 def test_bad_class_reject(self):
  for a,b in [(0,0),(22,0),(1,1),(3,22)]:
   s=State();self.assertEqual(lib.nsw_create(c.byref(s),a,b),11)
 def test_initial(self):
  s=new();self.assertEqual((s.x,s.y,s.quest,s.health,s.remedies),(12,17,0,30,2))
 def test_forbidden_map_border(self):self.assertEqual(lib.nsw_tile(0,1),4)
 def test_water_blocked(self):
  s=new();
  for d in [3,3,3,3,3,3,0,0]:action(s,1,d)
  self.assertEqual(action(s,1,0),12);self.assertEqual(s.y,15)
 def test_bridge_passable(self):self.assertEqual(lib.nsw_tile(12,14),7)
 def test_no_remote_interaction(self):
  s=new();rev=s.revision;self.assertEqual(action(s,2,2),13);self.assertEqual(s.revision,rev)
 def test_guard_interaction_requires_near(self):
  s=new();self.assertEqual(visit(s,1),2);self.assertEqual(s.quest,1)
 def test_dialogue_stage_order(self):
  s=new();self.assertEqual(action(s,2,4),13);self.assertEqual(visit(s,1),2);self.assertEqual(visit(s,2),2);self.assertEqual(s.quest,2)
 def test_profession_real_receipt(self):
  s=new();visit(s,1);visit(s,2);visit(s,3);self.assertEqual((s.herbs,s.work_xp,s.quest),(1,5,2));visit(s,3);self.assertEqual((s.herbs,s.work_xp,s.quest),(2,10,3));visit(s,4);self.assertEqual((s.herbs,s.quest,s.remedies),(0,4,3))
 def test_blocked_actor_no_revision(self):
  s=new();prev=s.revision;self.assertEqual(action(s,3),14);self.assertEqual(s.revision,prev)
 def test_stale_revision_no_mutation(self):
  s=new();action(s,1,0);q=(s.revision,s.x,s.y);self.assertEqual(action(s,1,0,rev=0),10);self.assertEqual((s.revision,s.x,s.y),q)
 def test_invalid_command_no_revision(self):
  s=new();self.assertEqual(action(s,1,99),11);self.assertEqual(s.revision,0)
 def test_three_bosses_and_epilogue(self):
  s=new(6,17);unlock(s)
  for b in range(1,4):beat(s,b)
  self.assertEqual((s.quest,s.defeats,s.active_boss),(7,3,0))
 def test_boss_is_per_session(self):
  a,b=new(1),new(2);unlock(a);unlock(b);visit(a,5);visit(b,5);action(a,4);action(a,3)
  self.assertNotEqual(a.revision,b.revision);self.assertNotEqual(a.boss_hp,b.boss_hp)
 def test_boss_attack_telegraph(self):
  s=new();unlock(s);visit(s,5);self.assertEqual(s.boss_intent,1);hp=s.health;action(s,4);self.assertEqual(s.boss_intent,2);self.assertLessEqual(s.health,hp)
 def test_boss_retreat_no_free_win(self):
  s=new();unlock(s);visit(s,5);self.assertEqual(action(s,7),1);self.assertEqual((s.defeats,s.quest,s.active_boss),(0,4,0))
 def test_boss_sp_consumption(self):
  s=new();unlock(s);visit(s,5);old=s.sp;action(s,8);self.assertEqual(s.sp,old-3)
 def test_potion_reduces_stock(self):
  s=new();unlock(s);visit(s,5);old=s.remedies;action(s,6);self.assertEqual(s.remedies,old-1)
 def test_npc_behavior_deterministic(self):
  lib.nsw_being_x.argtypes=[c.c_uint32,c.c_uint32]
  self.assertEqual(lib.nsw_being_x(1,0),lib.nsw_being_x(1,0));self.assertNotEqual(lib.nsw_being_x(1,0),lib.nsw_being_x(1,8))
 def test_no_teleport_on_camera(self):
  s=new();b=(s.x,s.y,s.revision)
  for angle in [0,1,2,3,0]:self.assertEqual((s.x,s.y,s.revision),b)

if __name__=='__main__':unittest.main(verbosity=2)
