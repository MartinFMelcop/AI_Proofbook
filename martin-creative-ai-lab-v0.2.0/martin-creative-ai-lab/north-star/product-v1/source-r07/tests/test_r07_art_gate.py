"""R07 tests: actual painted multi-facing facades are not in the archive.
No image hash or pixel-delta test can authorize art promotion.
"""
from pathlib import Path
import unittest,json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]
SH=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
class R07AssetGate(unittest.TestCase):
 def test_manifest_is_blocked(self):
  d=json.loads((ROOT/'docs/R07_FACADE_ART_GATE.json').read_text())
  self.assertEqual(d['state'],'ART_BLOCKED')
  self.assertEqual(len(d['buildings']),3)
  for item in d['buildings'].values():
   self.assertIsNone(item['faces']);self.assertFalse(item['license_checked'])
 def test_four_art_fallbacks_kept(self):
  for name in ['r04_cottage','r04_forge','r04_apothecary']:
   p=ROOT/'site/assets/world'/f'{name}.webp'
   self.assertTrue(p.is_file());self.assertGreater(p.stat().st_size,100000)
 def test_original_png_and_wasm_unchanged(self):
  old=ROOT/'R06_PACKAGE_MANIFEST.json'
  d=json.loads(old.read_text())['files']
  for name in ['core/world_r05.cpp','core/world_r05.h','site/product.wasm','site/assets/world/r04_cottage.webp','site/assets/world/r04_forge.webp','site/assets/world/r04_apothecary.webp','site/assets/opening_animatic.mp4']:
   with self.subTest(n=name):self.assertEqual(SH(ROOT/name),d[name])
 def test_observer_only_no_core(self):
  t=(ROOT/'site/atmosphere_r07.js').read_text()
  self.assertNotIn('nsw_wasm_apply',t);self.assertNotIn('localStorage',t)
  self.assertNotIn('WebAssembly.instantiate',t)
 def test_visual_facades_fail_closed(self):
  s=(ROOT/'site/world.js').read_text()
  self.assertIn('NSFacadeR07?.resolve',s)
  self.assertIn('NSAtmosphereR07?.cast',s)
  self.assertIn('R05 does NOT yet ship author-approved',s)
 def test_gui_integration(self):
  html=(ROOT/'site/index.html').read_text()
  for n in ['facades_r07.js','atmosphere_r07.js']:
   self.assertIn(f'src="{n}"',html)
  self.assertLess(html.index('src="facades_r07.js"'),html.index('src="world.js"'))
 def test_no_fake_four_paintings(self):
  self.assertEqual(list((ROOT/'site/assets/world').glob('r07_*_?.webp')),[])
 def test_previous_art_experimental_still_refused(self):
  html=(ROOT/'site/index.html').read_text()
  self.assertIn('ART_REVIEW_PENDING',html)
  self.assertNotIn('PRODUCT_GO',html)
 def test_current_owner_is_abi5(self):
  h=(ROOT/'core/world_r05.h').read_text()
  self.assertIn('nsw_wasm_structure_x',h)
  self.assertEqual(SH(ROOT/'site/product.wasm'),json.loads((ROOT/'R06_PACKAGE_MANIFEST.json').read_text())['files']['site/product.wasm'])
if __name__=='__main__': unittest.main()
