import ctypes as c, unittest
from pathlib import Path
lib=c.CDLL(str(Path(__file__).resolve().parent.parent/'artifacts'/'libns_product.so'))
class State(c.Structure):
 _fields_=[(name,c.c_uint32) for name in ['abi','revision','initialized','primary','secondary','chapter_step','active_boss','defeats','health','potions','focus','boss_hp','last_code']]
class Command(c.Structure):
 _fields_=[('abi',c.c_uint32),('expected_revision',c.c_uint32),('type',c.c_uint32),('value',c.c_int32)]
lib.nsp_reset.argtypes=[c.POINTER(State)];lib.nsp_create.argtypes=[c.POINTER(State),c.c_uint32,c.c_uint32];lib.nsp_create.restype=c.c_int32
lib.nsp_apply.argtypes=[c.POINTER(State),c.POINTER(Command)];lib.nsp_apply.restype=c.c_int32
lib.nsp_boss_hp.argtypes=[c.POINTER(State)];lib.nsp_boss_hp.restype=c.c_int32

def init(a=1,b=0):
 s=State();assert lib.nsp_create(c.byref(s),a,b)==1;return s

def event(s,t,value=0,revision=None):
 x=Command(1,s.revision if revision is None else revision,t,value);return lib.nsp_apply(c.byref(s),c.byref(x))

def unlock(s):
 for e in range(1,5):assert event(s,1,e)==1

class CompositeCoreTests(unittest.TestCase):
 def test_abi(self):self.assertEqual(lib.nsp_abi(),1)
 def test_all_21_primary_choices(self):
  for a in range(1,22):self.assertEqual(init(a).primary,a)
 def test_all_distinct_pairings(self):
  for a in range(1,22):
   for b in range(1,22):
    if a==b:continue
    s=init(a,b);self.assertEqual((s.primary,s.secondary),(a,b))
 def test_reject_invalid_identity(self):
  for a,b in [(0,0),(22,0),(2,2),(1,22),(100,100)]:
   s=State();self.assertEqual(lib.nsp_create(c.byref(s),a,b),11)
 def test_initial_state(self):
  s=init();self.assertEqual((s.health,s.potions,s.revision,s.chapter_step),(20,2,0,0))
 def test_no_skipping_quest(self):
  s=init();self.assertEqual(event(s,1,4),12);self.assertEqual(s.revision,0)
 def test_quest_gate_order(self):
  s=init();unlock(s);self.assertEqual((s.chapter_step,s.revision),(4,4))
 def test_no_boss_before_quest(self):self.assertEqual(event(init(),2),12)
 def test_no_attack_outside_boss(self):self.assertEqual(event(init(),3),12)
 def test_stale_revision_fails_closed(self):
  s=init();event(s,1,1);self.assertEqual(event(s,1,2,revision=0),10);self.assertEqual(s.chapter_step,1)
 def test_three_boss_fixture_to_epilogue(self):
  s=init();unlock(s)
  for boss in range(1,4):
   self.assertEqual(event(s,2),2);self.assertEqual(s.active_boss,boss)
   self.assertEqual(lib.nsp_boss_hp(c.byref(s)),[9,12,15][boss-1])
   while s.active_boss:
    rc=event(s,3)
    self.assertIn(rc,[1,3,4]);self.assertGreaterEqual(s.health,0)
   self.assertEqual(s.defeats,boss)
  self.assertEqual((s.chapter_step,s.defeats),(7,3));self.assertGreater(s.health,0)
 def test_boss_state_is_per_session(self):
  a,b=init(),init(8,16);unlock(a);unlock(b);event(a,2);event(b,2);event(a,3)
  self.assertEqual(lib.nsp_boss_hp(c.byref(a)),6);self.assertEqual(lib.nsp_boss_hp(c.byref(b)),9)
 def test_observe_raises_focus(self):
  s=init();unlock(s);event(s,2);event(s,5);self.assertEqual(s.focus,1)
 def test_guard_reduces_damage(self):
  s=init();unlock(s);event(s,2);event(s,4);self.assertEqual(s.health,19)
 def test_potion_consumed(self):
  s=init();unlock(s);event(s,2);event(s,3);event(s,6);self.assertEqual(s.potions,1)
 def test_potion_exhaustion_rejected(self):
  s=init();unlock(s);event(s,2)
  for _ in range(2):event(s,6)
  prior=s.revision;self.assertEqual(event(s,6),13);self.assertEqual(s.revision,prior)
 def test_retreat_no_boss_grant(self):
  s=init();unlock(s);event(s,2);self.assertEqual(event(s,7),1);self.assertEqual((s.defeats,s.chapter_step,s.boss_hp),(0,4,0))
 def test_invalid_action_rejected(self):
  s=init();self.assertEqual(event(s,99),11)
 def test_revision_guard(self):
  s=init();event(s,1,1);self.assertEqual(event(s,1,2,revision=1),1)
 def test_replay_deterministic(self):
  def run():
   s=init(9,12);trace=[]
   for value in range(1,5):trace.append(event(s,1,value))
   for _ in range(3):
    trace.append(event(s,2))
    while s.active_boss:trace.append(event(s,3))
   return trace,tuple(getattr(s,k) for k,_ in State._fields_)
  self.assertEqual(run(),run())
 def test_camera_independence(self):
  s=init();initial=(s.revision,s.chapter_step,s.health)
  for angle in [0,90,180,270,360]:self.assertEqual((s.revision,s.chapter_step,s.health),initial)
if __name__=='__main__':unittest.main(verbosity=2)

