"""R06 asset-consumer tests. No art approval is inferred from pixel checks."""
from pathlib import Path
from PIL import Image
import unittest, json, hashlib
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'site/assets/world'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
class R06VisualIntegrity(unittest.TestCase):
 def setUp(self):
  self.motion=json.loads((ROOT/'docs/R06_MOTION_RECEIPTS.json').read_text())
  self.wraith=json.loads((ROOT/'docs/R06_WRAITH_RECEIPTS.json').read_text())
 def test_motion_count(self):
  self.assertEqual(self.motion['count'],66)
  self.assertEqual(len(self.motion['frames']),66)
 def test_each_motion_reproducible_hashes(self):
  for r in self.motion['frames']:
   with self.subTest(name=r['target']):
    self.assertEqual(sha(ASSETS/r['source']),r['source_sha256'])
    self.assertEqual(sha(ASSETS/r['target']),r['sha256'])
 def test_images_preserve_transparency(self):
  for r in self.motion['frames']:
   with self.subTest(frame=r['target']):
    im=Image.open(ASSETS/r['target']).convert('RGBA');self.assertGreater(im.getextrema()[3][1],230)
    self.assertLess(im.getextrema()[3][0],10)
 def test_frames_are_not_duplicates(self):
  for k in range(1,5):
   for face in range(4):
    original=sha(ASSETS/f'npc_{k}_{face}.webp')
    sample=[sha(ASSETS/f'npc_{k}_{face}_motion_{f}.webp') for f in (1,2,3)]
    self.assertEqual(len({original,*sample}),4)
 def test_wraith_is_noncanonical_derivation(self):
  self.assertEqual(len(self.wraith['entries']),16)
  self.assertEqual(self.wraith['approval'],'ART_REVIEW_PENDING')
  for r in self.wraith['entries']:
   self.assertEqual(sha(ASSETS/r['source']),r['source_sha256'])
   self.assertEqual(sha(ASSETS/r['target']),r['target_sha256'])
 def test_code_uses_only_observer_features(self):
  s=(ROOT/'site/world.js').read_text()
  self.assertIn('NSAmbienceR06?.ambience',s)
  self.assertIn('r06_wraith_',s)
  self.assertIn('stepFrame',s)
  self.assertIn('nsw_wasm_boss_threatens',s)
  self.assertIn('nsw_wasm_structure_x',s)
  self.assertNotIn('new NSProductOwner',s)
 def test_old_abi_and_art_not_overwritten(self):
  manifest=json.loads((ROOT/'R05_PACKAGE_MANIFEST.json').read_text())
  for file in ['core/world_r05.cpp','core/world_r05.h','site/assets/world/r04_cottage.webp','site/assets/world/r04_forge.webp','site/assets/world/r04_apothecary.webp','site/assets/world/npc_1_0.webp','site/assets/world/r04_wisp.webp','site/assets/opening_animatic.mp4']:
   self.assertEqual(sha(ROOT/file),manifest['files'][file],file)
 def test_visual_product_go_remains_closed(self):
  self.assertIn('ART_REVIEW_PENDING',(ROOT/'docs/R06_WRAITH_RECEIPTS.json').read_text())
if __name__=='__main__':unittest.main()
