import unittest,json,hashlib
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
class R14Art(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=json.loads((R/'artifacts/R14_ART_RECEIPT.json').read_text())
 def test_source_sheets(self):self.assertEqual(self.data['source_sheets'],8)
 def test_sprite_count(self):self.assertEqual(self.data['sprites_created'],92)
 def test_all_manifest_assets(self):
  for family,entries in self.data['assets'].items():
   for frame in entries:
    p=R/'site/assets/world'/(frame['name']+'.webp')
    self.assertTrue(p.is_file(),p);self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),frame['webp_sha256'])
 def test_rgba_and_dimensions(self):
  for entries in self.data['assets'].values():
   for f in entries:
    p=R/'site/assets/world'/(f['name']+'.webp')
    with Image.open(p) as im:
     self.assertEqual(im.mode,'RGBA');self.assertEqual(im.size,tuple(f['dims']));self.assertLess(im.getchannel('A').getextrema()[0],255)
 def test_no_author_approval(self):
  self.assertEqual(self.data['status'],'ART_REVIEW_PENDING / PRODUCT_NO_GO')
  self.assertTrue(all(f['rights']=='ART_CANDIDATE_RIGHTS_REVIEW_PENDING' for a in self.data['assets'].values() for f in a))
 def test_frozen_engine_sources(self):
  b=Path('/mnt/data/MMAI_PRODUCT_V1_R13_WORK')
  for rel in ['core/world_r05.cpp','core/world_r05.h','site/product.wasm','site/camera4.js','site/r13_stagecraft.js']:
   self.assertEqual((R/rel).read_bytes(),(b/rel).read_bytes(),rel)
