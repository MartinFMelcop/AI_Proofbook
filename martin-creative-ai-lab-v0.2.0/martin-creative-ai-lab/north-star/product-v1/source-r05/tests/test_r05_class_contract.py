"""Source-traced profile and character-pair QA, *not* class or boss canonization."""
import ctypes as c, json, unittest
from pathlib import Path
from test_world_r05 import State,LIB
ROOT=Path(__file__).resolve().parents[1]
class ClassMatrixR05(unittest.TestCase):
 def test_source_profiles_21_and_missing_canon_ids(self):
  j=json.loads((ROOT/'docs/R03_CLASS_KITS_LAB.json').read_text())
  a=j['records'];self.assertEqual(len(a),21)
  self.assertEqual([r['source_id'] for r in a],[f'R{i:02d}' for i in range(1,22)])
  for r in a:
   self.assertIsNone(r['canonical_skill_id']);self.assertIsNone(r['canonical_kit_id']);self.assertIsNone(r['weapon_ids'])
   self.assertEqual(r['skills_implemented'],2);self.assertIn('LAB',r['status'])
  self.assertEqual(j['rogue_a_b'],'SHARED_LEGACY_KEY_UNVERIFIED')
 def test_all_21_mono_and_420_ordered_double_pairings(self):
  successful=0
  for a in range(1,22):
   for b in range(0,22):
    s=State();rc=LIB.nsw_create(c.byref(s),a,b)
    if a==b:self.assertEqual(rc,11)
    else:
     self.assertEqual(rc,1,(a,b));self.assertEqual((s.primary,s.secondary),(a,b));successful+=1
  self.assertEqual(successful,441)
 def test_invalid_character_choices_fail_closed(self):
  for a,b in [(0,0),(22,0),(0,21),(22,22),(1,1),(1,22),(999,1)]:
   s=State();self.assertEqual(LIB.nsw_create(c.byref(s),a,b),11)
 def test_no_approved_power_documented_by_mechanical_coverage(self):
  j=json.loads((ROOT/'docs/R03_CLASS_KITS_LAB.json').read_text())
  self.assertEqual(j['canon'],'NO_NEW_CANON')
  self.assertIn('CLASS_OWNER_ACK',j['approval_gate'])
  self.assertIn('COMBAT_BALANCE',j['approval_gate'])
if __name__=='__main__':unittest.main()
