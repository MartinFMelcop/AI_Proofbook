"""R03 C++ owner: 21× research-only two-action kits, boss pressure, bounded beings.
All local fixtures. NOT lore canon, balancing, MMO AI, or visual acceptance.
"""
import ctypes as c,unittest
from pathlib import Path
from test_world import shortest
ROOT=Path(__file__).resolve().parents[1]
NAMES=('abi revision initialized primary secondary x y quest herbs work_xp remedies health focus sp '
 'active_boss boss_hp boss_intent target_x target_y boss_phase defeats world_tick last_code '
 'ore ingots mining_xp smithing_xp kit_ward kit_echo kit_burn kit_mark kit_root kit_tempo kit_fatigue '
 'boss_pattern boss_turn being_last_talk weapon_grade '
 'being_talk_mask last_talk_tick research_last_class research_last_action boss_pressure').split()
class State(c.Structure):_fields_=[(n,c.c_uint32) for n in NAMES]
class Cmd(c.Structure):_fields_=[('abi',c.c_uint32),('expected_revision',c.c_uint32),('type',c.c_uint32),('value',c.c_int32)]
lib=c.CDLL(str(ROOT/'artifacts/libns_world_r03.so'))
lib.nsw_create.argtypes=[c.POINTER(State),c.c_uint32,c.c_uint32];lib.nsw_create.restype=c.c_int32
lib.nsw_apply.argtypes=[c.POINTER(State),c.POINTER(Cmd)];lib.nsw_apply.restype=c.c_int32
for fn in ['nsw_object_x','nsw_object_y','nsw_kit_cost','nsw_kit_aux_cost','nsw_kit_passive_family','nsw_kit_mode','nsw_kit_power']:
 getattr(lib,fn).argtypes=[c.c_uint32];getattr(lib,fn).restype=c.c_uint32
lib.nsw_being_behavior.argtypes=[c.POINTER(State),c.c_uint32];lib.nsw_being_behavior.restype=c.c_uint32
lib.nsw_being_x.argtypes=[c.c_uint32,c.c_uint32];lib.nsw_being_y.argtypes=[c.c_uint32,c.c_uint32]
def new(a=1,b=0):
 s=State();assert lib.nsw_create(c.byref(s),a,b)==1;return s
def action(s,t,v=0,rev=None):return lib.nsw_apply(c.byref(s),c.byref(Cmd(3,s.revision if rev is None else rev,t,v)))
def visit(s,obj):
 for k in shortest(s,lib.nsw_object_x(obj),lib.nsw_object_y(obj)):
  rc=action(s,1,k);assert rc==1,(obj,s.x,s.y,rc)
 return action(s,2,obj)
def unlock(s):
 assert visit(s,1)==2;assert visit(s,2)==2;assert visit(s,3)==1;assert visit(s,3)==2;assert visit(s,4)==2
 assert s.quest==4
def beat(s,b):
 assert visit(s,b+4)==3
 for _ in range(90):
  if not s.active_boss:break
  if s.boss_intent==1:rc=action(s,4)
  elif s.health<=12 and s.remedies:rc=action(s,6)
  elif s.sp>=2 and s.boss_hp>3:rc=action(s,8,1 if s.secondary and s.world_tick%3==0 else 0)
  else:rc=action(s,3)
  assert rc in (1,4,5),(b,rc,s.health,s.boss_hp)
 assert s.defeats==b,(s.defeats,s.health,s.quest)
class WorldR03(unittest.TestCase):
 def test_abi(self):self.assertEqual(lib.nsw_abi(),3)
 def test_r02_cannot_claim_r03_session(self):
  s=new();before=bytes(s)
  self.assertEqual(lib.nsw_apply(c.byref(s),c.byref(Cmd(2,s.revision,1,0))),11)
  self.assertEqual(bytes(s),before)
 def test_21_profiles_all_have_signature_aux_passive(self):
  for cls in range(1,22):
   with self.subTest(cls=cls):
    s=new(cls);unlock(s);self.assertEqual(visit(s,5),3)
    self.assertEqual(lib.nsw_kit_mode(cls),cls)
    self.assertGreater(lib.nsw_kit_cost(cls),0)
    self.assertGreater(lib.nsw_kit_aux_cost(cls),0)
    self.assertIn(lib.nsw_kit_passive_family(cls),range(1,8))
    b=s.revision
    self.assertIn(action(s,11,0),(1,4,5))
    self.assertEqual(s.revision,b+1)
    self.assertEqual((s.research_last_class,s.research_last_action),(cls,2))
 def test_21_signature_research_actions(self):
  for cls in range(1,22):
   with self.subTest(cls=cls):
    s=new(cls);unlock(s);visit(s,5);b=s.revision
    self.assertIn(action(s,8,0),(1,4,5))
    self.assertEqual((s.research_last_class,s.research_last_action),(cls,1))
    self.assertEqual(s.revision,b+1)
 def test_mono_secondary_aux_rejected_without_mutation(self):
  s=new(6);unlock(s);visit(s,5);b=bytes(s)
  self.assertEqual(action(s,11,1),11);self.assertEqual(bytes(s),b)
 def test_secondary_aux_consumes_resource(self):
  s=new(6,17);unlock(s);visit(s,5);sp=s.sp
  self.assertIn(action(s,11,1),(1,4,5));self.assertEqual(s.research_last_class,17)
  self.assertLess(s.sp,sp)
 def test_bad_aux_choice_rejected(self):
  s=new(6,17);unlock(s);visit(s,5);b=bytes(s)
  self.assertEqual(action(s,11,55),11);self.assertEqual(bytes(s),b)
 def test_no_remote_utility(self):
  s=new(6);unlock(s);visit(s,5);s.x=2;s.y=2
  b=bytes(s);self.assertEqual(action(s,11,0),13);self.assertEqual(bytes(s),b)
 def test_no_resource_no_progress(self):
  s=new(6);unlock(s);visit(s,5);s.sp=0
  b=bytes(s);self.assertEqual(action(s,11,0),15);self.assertEqual(bytes(s),b)
 def test_older_revision_rejected(self):
  s=new();b=bytes(s);self.assertEqual(action(s,1,0,rev=999),10);self.assertEqual(bytes(s),b)
 def test_full_three_boss_prologue(self):
  s=new(6,17);unlock(s)
  for b in range(1,4):beat(s,b)
  self.assertEqual((s.quest,s.defeats),(7,3))
 def test_passive_family_bounded(self):
  for cls in range(1,22):
   with self.subTest(cls=cls):
    s=new(cls);unlock(s);visit(s,5)
    self.assertLessEqual(s.kit_ward,10);self.assertLessEqual(s.kit_mark,5)
    self.assertLessEqual(s.kit_echo,10);self.assertLessEqual(s.kit_tempo,5)
    self.assertLessEqual(s.health,30);self.assertLessEqual(s.focus,3)
 def test_being_talk_memory_is_local_and_observable(self):
  s=new(6);self.assertEqual(s.being_talk_mask,0)
  for k in shortest(s,13,16):self.assertEqual(action(s,1,k),1)
  self.assertEqual(action(s,10,1),1)
  self.assertEqual(s.being_talk_mask,1);self.assertEqual(s.last_talk_tick,s.world_tick)
  self.assertEqual(lib.nsw_being_behavior(c.byref(s),1),2)
  isolated=new(6);self.assertEqual(isolated.being_talk_mask,0)
 def test_being_remote_conversation_cannot_create_memory(self):
  s=new();before=bytes(s);self.assertEqual(action(s,10,3),13);self.assertEqual(bytes(s),before)
 def test_boss_2_pattern_5_possible_in_synthetic_phase(self):
  s=new(6);unlock(s);beat(s,1);visit(s,6)
  # explicitly SYNTHETIC phase fixture: does not pretend a naturally played encounter
  s.boss_hp=9;s.boss_phase=1;s.boss_intent=2;s.boss_turn=2
  self.assertEqual(action(s,4),1)
  self.assertEqual(s.boss_pattern,5)
 def test_boss_3_pattern_6_possible_in_synthetic_phase(self):
  s=new(6);unlock(s);beat(s,1);beat(s,2);visit(s,7)
  s.boss_hp=13;s.boss_phase=1;s.boss_intent=2;s.boss_turn=2
  self.assertEqual(action(s,4),1)
  self.assertEqual(s.boss_pattern,6)
 def test_unsupported_command_fails_closed(self):
  s=new();snap=bytes(s);self.assertEqual(action(s,12,0),11);self.assertEqual(bytes(s),snap)
 def test_other_session_does_not_inherit_research_action(self):
  a=new(17);b=new(17);unlock(a);visit(a,5);action(a,11,0)
  self.assertGreater(a.research_last_class,0);self.assertEqual(b.research_last_class,0)
if __name__=='__main__':unittest.main(verbosity=2)
