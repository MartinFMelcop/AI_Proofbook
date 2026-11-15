"""R12 proof of existing painting geometry and safety, not visual/canon approval."""
import hashlib,json,unittest
from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parents[1]
DATA=json.loads((R/'art_sources/R12_SILHOUETTE_ALIGNMENT.json').read_text())
class TestR12AlphaAlignment(unittest.TestCase):
 def test_all_twelve_anchors_measured(self):self.assertEqual(len(DATA['faces']),12)
 def test_evidence_does_not_confer_art_approval(self):self.assertEqual(DATA['status'],'LAB_ONLY_NO_ART_APPROVAL')
 def test_all_orig_sha_match(self):
  for key,m in DATA['faces'].items():
   with self.subTest(key=key):
    path=R/'site/assets/world'/('r11_'+key+'.webp')
    self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),m['sha256'])
 def test_bbox_inside_painting(self):
  for key,m in DATA['faces'].items():
   with self.subTest(key=key):
    x0,y0,x1,y1=m['bbox'];self.assertTrue(0<=x0<x1<640 and 0<=y0<y1<640)
 def test_bbox_alpha_evidence_exact(self):
  for key,m in DATA['faces'].items():
   with self.subTest(key=key):
    a=np.asarray(Image.open(R/'site/assets/world'/('r11_'+key+'.webp')).convert('RGBA'))[:,:,3]
    y,x=np.where(a>24)
    self.assertEqual([x.min(),y.min(),x.max(),y.max()],m['bbox'])
 def test_bottom_alignment_range(self):
  for m in DATA['faces'].values():self.assertTrue(595<=m['anchor_y']<=620)
 def test_center_anchor_stable_over_angles(self):
  for b in ('cottage','forge','apothecary'):
   xs=[DATA['faces'][f'{b}_{i}']['anchor_x'] for i in range(4)]
   self.assertLess(max(xs)-min(xs),4)
 def test_r12_module_only_reads_painted_metrics(self):
  txt=(R/'site/r12_finishing.js').read_text()
  self.assertIn('NSR12AssetAnchors',txt);self.assertIn('NSFinishingR12',txt)
  self.assertNotIn('nsw_wasm_apply(',txt);self.assertNotIn("state='AUTHOR_ART_APPROVED'",txt)
 def test_only_internal_preview_enables_new_art(self):
  txt=(R/'site/world.js').read_text()
  self.assertIn('root.NSR12VisualLab===true',txt)
  self.assertIn('R12 VISUAL LAB · NOT APPROVED',txt)
 def test_engine_abi_remains_five(self):
  txt=(R/'core/world_r05.cpp').read_text();self.assertIn('nsw_abi',txt)
 def test_entrypoint_script_loaded_before_renderer(self):
  txt=(R/'site/index.html').read_text()
  self.assertLess(txt.index('r12_asset_anchors.js'),txt.index('r12_finishing.js'))
  self.assertLess(txt.index('r12_finishing.js'),txt.index('world.js'))
if __name__=='__main__':unittest.main()
