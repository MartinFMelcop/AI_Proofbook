import unittest, json, tempfile
from pathlib import Path
from hashlib import sha256
from PIL import Image
from tools.validate_facades_r07 import validate
class PhysicalGate(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name)
  self.d={'state':'AUTHOR_ART_APPROVED','buildings':{}}
  for i,name in {'1':'r07_cottage','2':'r07_forge','3':'r07_apothecary'}.items():
   faces=[f'{name}_{f}' for f in range(4)];hashes=[]
   for f,base in enumerate(faces):
    im=Image.new('RGBA',(128,128),(f*40,int(i)*30,80,0));im.paste((200,20+f*55,100,255),(26,25+f,106,115));path=self.root/(base+'.webp');im.save(path,lossless=True);hashes.append(sha256(path.read_bytes()).hexdigest())
   self.d['buildings'][i]={'license_checked':True,'scale_anchor_reviewed':True,'faces':faces,'sha256':hashes}
 def test_ready_to_review_is_not_author_approved(self):
  x=validate(self.d,self.root);self.assertEqual(x['status'],'READY_FOR_HUMAN_VISUAL_REVIEW_ONLY');self.assertFalse(x['eligible_for_art_approval'])
 def test_missing_file(self):
  (self.root/'r07_forge_2.webp').unlink();self.assertEqual(validate(self.d,self.root)['status'],'BLOCKED')
 def test_approval_missing(self):
  self.d['state']='ART_REVIEW_PENDING';self.assertIn('approval_not_granted',validate(self.d,self.root)['errors'])
 def test_duplicate_image(self):
  src=self.root/'r07_cottage_0.webp';dst=self.root/'r07_cottage_1.webp';dst.write_bytes(src.read_bytes());self.assertIn('identical_asset_bytes',' '.join(validate(self.d,self.root)['errors']))
 def test_wrong_hash(self):
  self.d['buildings']['1']['sha256'][0]='a'*64;self.assertIn('hash_mismatch',' '.join(validate(self.d,self.root)['errors']))
 def test_dimensions_mismatch(self):
  im=Image.new('RGBA',(256,128),(40,40,40,0));im.paste((255,230,200,255),(20,20,150,110));f=self.root/'r07_apothecary_1.webp';im.save(f,lossless=True)
  self.d['buildings']['3']['sha256'][1]=sha256(f.read_bytes()).hexdigest();self.assertIn('inconsistent_canvas_dimensions',' '.join(validate(self.d,self.root)['errors']))
 def test_license_pending(self):
  self.d['buildings']['3']['license_checked']=False;self.assertIn('license_checked_not_verified',' '.join(validate(self.d,self.root)['errors']))
if __name__=='__main__': unittest.main()
