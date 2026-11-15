"""Independent R05 ABI5 tests: owner geometry and NPC-facing contracts are pure.
No new canon, collision or unofficial class powers are introduced."""
import ctypes as c, json, unittest
from pathlib import Path
from test_world_r04 import NAMES
ROOT=Path(__file__).resolve().parents[1]
class State(c.Structure):_fields_=[(n,c.c_uint32) for n in NAMES]
class Cmd(c.Structure):_fields_=[('abi',c.c_uint32),('expected_revision',c.c_uint32),('type',c.c_uint32),('value',c.c_int32)]
LIB=c.CDLL(str(ROOT/'artifacts/libns_world_r05.so'))
LIB.nsw_create.argtypes=[c.POINTER(State),c.c_uint32,c.c_uint32];LIB.nsw_create.restype=c.c_int32
LIB.nsw_apply.argtypes=[c.POINTER(State),c.POINTER(Cmd)];LIB.nsw_apply.restype=c.c_int32
for name,args in [('nsw_structure_at',2),('nsw_structure_x',1),('nsw_structure_y',1),('nsw_being_facing',2),('nsw_being_x',2),('nsw_being_y',2),('nsw_tile',2)]:
 f=getattr(LIB,name);f.argtypes=[c.c_uint32]*args;f.restype=c.c_uint32
class R05Geometry(unittest.TestCase):
 def new(self):
  s=State();self.assertEqual(LIB.nsw_create(c.byref(s),6,17),1);return s
 def test_abi5(self):self.assertEqual(LIB.nsw_abi(),5)
 def test_three_structures_match_existing_blocked_tiles(self):
  expect={1:(10,7,9,8),2:(17,8,9,8),3:(20,10,11,10)}
  for sid,(x,y0,y1,cy) in expect.items():
   with self.subTest(sid=sid):
    self.assertEqual((LIB.nsw_structure_x(sid),LIB.nsw_structure_y(sid)),(x,cy))
    for y in range(y0,y1+1):
     self.assertEqual(LIB.nsw_structure_at(x,y),sid)
     self.assertEqual(LIB.nsw_tile(x,y),9)
 def test_outside_structure_is_zero(self):
  for x,y in [(9,8),(11,8),(16,8),(19,10),(20,12),(23,19),(500,500)]:self.assertEqual(LIB.nsw_structure_at(x,y),0)
 def test_structure_query_never_owns_new_collision(self):
  for y in range(20):
   for x in range(24):
    if LIB.nsw_structure_at(x,y):self.assertEqual(LIB.nsw_tile(x,y),9)
 def test_route_facing_in_world_coordinates(self):
  for tick in range(0,120):
   for being in range(1,5):self.assertIn(LIB.nsw_being_facing(being,tick),range(4))
 def test_moving_being_facing_matches_accepted_position(self):
  seen=0
  for tick in range(1,160):
   for being in range(1,5):
    a=(LIB.nsw_being_x(being,tick-1),LIB.nsw_being_y(being,tick-1));b=(LIB.nsw_being_x(being,tick),LIB.nsw_being_y(being,tick))
    if a!=b:
     facing=0 if b[1]<a[1] else 1 if b[0]>a[0] else 2 if b[1]>a[1] else 3
     self.assertEqual(LIB.nsw_being_facing(being,tick),facing);seen+=1
  self.assertGreaterEqual(seen,12)
 def test_observation_does_not_mutate_session(self):
  s=self.new();before=bytes(s)
  for _ in range(5):
   for x,y in [(10,8),(17,8),(20,10),(23,19)]:LIB.nsw_structure_at(x,y)
   for t in range(0,25):
    for i in range(1,5):LIB.nsw_being_facing(i,t)
  self.assertEqual(bytes(s),before)
 def test_legacy_revision_rejected_without_mutation(self):
  s=self.new();old=bytes(s);rc=LIB.nsw_apply(c.byref(s),c.byref(Cmd(4,0,1,0)))
  self.assertEqual(rc,11);self.assertEqual(bytes(s),old)
 def test_collider_rejects_architectural_footprint_without_revision(self):
  # Position manually staged for this isolated legality counterexample.
  s=self.new();s.x=11;s.y=8;original=bytes(s)
  rc=LIB.nsw_apply(c.byref(s),c.byref(Cmd(5,s.revision,1,3)))
  self.assertEqual(rc,12);self.assertEqual(bytes(s),original)
 def test_world_direction_queries_do_not_advance_world_tick(self):
  s=self.new();before=bytes(s)
  for i in range(1,5):LIB.nsw_being_facing(i,s.world_tick)
  self.assertEqual(bytes(s),before)
 def test_new_revision_stale_rejected(self):
  s=self.new();old=bytes(s);rc=LIB.nsw_apply(c.byref(s),c.byref(Cmd(5,10,1,0)))
  self.assertEqual(rc,10);self.assertEqual(bytes(s),old)
 def test_new_tell_uses_existing_damage_rule(self):
  s=self.new();LIB.nsw_boss_threatens.argtypes=[c.POINTER(State),c.c_uint32,c.c_uint32];LIB.nsw_boss_threatens.restype=c.c_uint32
  self.assertEqual(LIB.nsw_boss_threatens(c.byref(s),s.x,s.y),0)
 def test_historic_native_trace_unchanged_except_abi(self):
  j=json.loads((ROOT/'artifacts/R04_WORLD_NATIVE_TRACE.json').read_text());s=self.new()
  for i,e in enumerate(j['events']):
   self.assertEqual(s.revision,e['rev'])
   rc=LIB.nsw_apply(c.byref(s),c.byref(Cmd(5,e['rev'],e['type'],e['value'])))
   self.assertEqual(rc,e['code'],i)
   for name,value in e['state'].items():self.assertEqual(getattr(s,{'boss':'active_boss','boss_target_x':'target_x','boss_target_y':'target_y'}.get(name,name)),value,(i,name))
  self.assertEqual((s.defeats,s.quest),(3,7))
if __name__=='__main__':unittest.main()
