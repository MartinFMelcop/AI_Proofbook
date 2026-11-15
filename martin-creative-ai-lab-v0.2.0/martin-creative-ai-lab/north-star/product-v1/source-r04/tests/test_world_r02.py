"""R02 laboratory world: 21 expressive class modes, two professions and explicit NPC states.
Mechanics are NOT approved North Star canonical rules or 21 complete class kits.
"""
import ctypes as c
import unittest
from pathlib import Path
from test_world import shortest, DIR
root=Path(__file__).resolve().parent.parent
lib=c.CDLL(str(root/'artifacts/libns_world_r02.so'))
FIELDS=('abi revision initialized primary secondary x y quest herbs work_xp remedies health focus sp '
 'active_boss boss_hp boss_intent target_x target_y boss_phase defeats world_tick last_code '
 'ore ingots mining_xp smithing_xp kit_ward kit_echo kit_burn kit_mark kit_root kit_tempo kit_fatigue '
 'boss_pattern boss_turn being_last_talk weapon_grade').split()
class State(c.Structure):_fields_=[(n,c.c_uint32) for n in FIELDS]
class Cmd(c.Structure):_fields_=[('abi',c.c_uint32),('expected_revision',c.c_uint32),('type',c.c_uint32),('value',c.c_int32)]
lib.nsw_create.argtypes=[c.POINTER(State),c.c_uint32,c.c_uint32];lib.nsw_create.restype=c.c_int32
lib.nsw_apply.argtypes=[c.POINTER(State),c.POINTER(Cmd)];lib.nsw_apply.restype=c.c_int32
lib.nsw_tile.argtypes=[c.c_uint32,c.c_uint32];lib.nsw_tile.restype=c.c_uint32
lib.nsw_object_x.argtypes=[c.c_uint32];lib.nsw_object_y.argtypes=[c.c_uint32]
lib.nsw_kit_mode.argtypes=[c.c_uint32];lib.nsw_kit_cost.argtypes=[c.c_uint32];lib.nsw_kit_power.argtypes=[c.c_uint32]
lib.nsw_being_behavior.argtypes=[c.POINTER(State),c.c_uint32];lib.nsw_being_behavior.restype=c.c_uint32
lib.nsw_being_x.argtypes=[c.c_uint32,c.c_uint32];lib.nsw_being_y.argtypes=[c.c_uint32,c.c_uint32]

def new(primary=1,secondary=0):
 s=State();assert lib.nsw_create(c.byref(s),primary,secondary)==1;return s

def action(s,t,v=0,rev=None):return lib.nsw_apply(c.byref(s),c.byref(Cmd(2,s.revision if rev is None else rev,t,v)))

def visit(s,obj):
 for k in shortest(s,lib.nsw_object_x(obj),lib.nsw_object_y(obj)):
  rc=action(s,1,k)
  assert rc==1,(s.quest,s.active_boss,s.x,s.y,k,rc)
 return action(s,2,obj)

def unlock(s):
 assert visit(s,1)==2
 assert visit(s,2)==2
 assert visit(s,3)==1
 assert visit(s,3)==2
 assert visit(s,4)==2
 assert s.quest==4

def boss(s,b):
 assert visit(s,4+b)==3
 for _ in range(90):
  if not s.active_boss:break
  if s.boss_intent==1:rc=action(s,4)
  elif s.health<=10 and s.remedies:rc=action(s,6)
  else:rc=action(s,3)
  assert rc in (1,4,5),(b,rc,s.health,s.revision)
 assert s.defeats==b

class WorldR02Tests(unittest.TestCase):
 def test_abi(self):self.assertEqual(lib.nsw_abi(),2)
 def test_legacy_isolation(self):
  self.assertEqual(c.CDLL(str(root/'artifacts/libns_world.so')).nsw_abi(),1)
 def test_full_prologue(self):
  s=new(6,17);unlock(s)
  for b in range(1,4):boss(s,b)
  self.assertEqual((s.quest,s.defeats),(7,3))
 def test_all_21_skill_modes(self):
  for i in range(1,22):
   with self.subTest(profile=i):
    s=new(i);unlock(s);visit(s,5)
    self.assertEqual(lib.nsw_kit_mode(i),i)
    self.assertGreater(lib.nsw_kit_cost(i),0)
    self.assertGreater(lib.nsw_kit_power(i),0)
    before=s.revision
    self.assertIn(action(s,8,0),(1,4,5))
    self.assertEqual(s.revision,before+1)
 def test_invalid_secondary_refused(self):
  s=new(2);unlock(s);visit(s,5)
  b=s.revision;self.assertEqual(action(s,8,1),11);self.assertEqual(s.revision,b)
 def test_secondary_is_active_and_selectable(self):
  s=new(6,18);unlock(s);visit(s,5)
  old=s.health;rc=action(s,8,1)
  self.assertIn(rc,(1,4,5));self.assertGreaterEqual(s.health,old-6)
  self.assertLess(s.boss_hp,15)
 def test_skill_bad_value_no_mutation(self):
  s=new();unlock(s);visit(s,5)
  snap=bytes(s);self.assertEqual(action(s,8,2),11);self.assertEqual(bytes(s),snap)
 def test_mining_not_allowed_before_leader(self):
  s=new();b=bytes(s);self.assertEqual(action(s,9,1),14);self.assertEqual(bytes(s),b)
 def test_mining_requires_proximity(self):
  s=new();visit(s,1);visit(s,2);b=s.revision
  self.assertEqual(action(s,9,1),13);self.assertEqual(s.revision,b)
 def test_mining_and_forge_loop(self):
  s=new();visit(s,1);visit(s,2)
  for k in shortest(s,18,7):self.assertEqual(action(s,1,k),1)
  self.assertEqual(action(s,9,1),1);self.assertEqual((s.ore,s.mining_xp),(1,7))
  for k in shortest(s,17,11):self.assertEqual(action(s,1,k),1)
  self.assertEqual(action(s,9,2),1);self.assertEqual((s.ore,s.ingots,s.smithing_xp),(0,1,9))
  self.assertEqual(action(s,9,2),15) # no resource; never creates ore from nothing
  self.assertEqual(action(s,9,3),1);self.assertEqual((s.weapon_grade,s.ingots),(1,0))
  self.assertEqual(action(s,9,3),15)
 def test_profession_capacity(self):
  s=new();visit(s,1);visit(s,2)
  for k in shortest(s,18,7):action(s,1,k)
  for _ in range(3):self.assertEqual(action(s,9,1),1)
  self.assertEqual(action(s,9,1),15)
 def test_npc_concern_is_stage_limited(self):
  s=new()
  self.assertIn(lib.nsw_being_behavior(c.byref(s),1),(0,1,2))
  for k in shortest(s,13,16):action(s,1,k)
  self.assertEqual(lib.nsw_being_behavior(c.byref(s),1),2)
  self.assertEqual(action(s,10,1),1)
  self.assertEqual(s.being_last_talk,1)
 def test_remote_npc_cannot_be_talked_to(self):
  s=new();b=bytes(s);self.assertEqual(action(s,10,3),13);self.assertEqual(bytes(s),b)
 def test_npc_unknown_id_rejected(self):
  s=new();self.assertEqual(action(s,10,5),11)
 def test_boss_distinct_patterns(self):
  for b in range(1,4):
   s=new();unlock(s)
   for prev in range(1,b):boss(s,prev)
   visit(s,b+4)
   self.assertEqual(s.boss_pattern,2 if b==2 else 1)
   self.assertEqual(s.active_boss,b)
 def test_soldier_mark_is_for_next_attack(self):
  s=new(1);unlock(s);visit(s,5);action(s,8,0)
  self.assertGreater(s.kit_mark,0)
  action(s,3)
  self.assertEqual(s.kit_mark,0)
 def test_berserker_cost_has_actual_consequence(self):
  s=new(3);unlock(s);visit(s,5);hp=s.health;action(s,8,0)
  self.assertLess(s.health,hp)
 def test_knight_ward_not_cosmetic(self):
  s=new(6);unlock(s);visit(s,5);action(s,8,0)
  self.assertGreaterEqual(s.kit_ward,0)
  self.assertLess(s.boss_hp,15)
 def test_pyro_burn_delayed(self):
  s=new(12);unlock(s);visit(s,5);action(s,8,0)
  self.assertGreater(s.kit_burn,0)
 def test_necro_echo_is_deferred(self):
  s=new(13);unlock(s);visit(s,5);action(s,8,0)
  self.assertGreater(s.kit_echo,0) # deferred effect must NOT resolve immediately
  action(s,4)
  self.assertEqual(s.kit_echo,0)
 def test_cleric_heal_bounded(self):
  s=new(18);unlock(s);visit(s,5);action(s,8,0)
  self.assertLessEqual(s.health,30)
 def test_rogue_a_opportunity_changes_damage(self):
  a=new(4);b=new(4);unlock(a);unlock(b);visit(a,5);visit(b,5)
  action(a,8,0) # first beat, telegraph target
  action(b,4) # first beat guarded, boss now in recovery
  self.assertIn(action(b,8,0),(1,4,5))
  self.assertLess(b.boss_hp,a.boss_hp)
 def test_sp_insufficient_fails_without_tick(self):
  s=new(10);unlock(s);visit(s,5)
  for _ in range(4):
   if s.sp<3:break
   action(s,8,0)
   if s.active_boss==0:break
  if s.active_boss:
   b=s.revision;self.assertEqual(action(s,8,0),15);self.assertEqual(s.revision,b)
 def test_old_command_abi_rejected(self):
  s=new();b=bytes(s);x=Cmd(1,s.revision,1,0)
  self.assertEqual(lib.nsw_apply(c.byref(s),c.byref(x)),11);self.assertEqual(bytes(s),b)
 def test_no_external_canon_knowledge(self):
  s=new();self.assertEqual(s.being_last_talk,0)
  for k in shortest(s,13,16):action(s,1,k)
  self.assertEqual(lib.nsw_being_behavior(c.byref(s),1),2)
  self.assertEqual(s.quest,0)

if __name__=='__main__':unittest.main(verbosity=2)
