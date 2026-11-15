"""Synthetic fixtures test a preflight algorithm, NOT generated game art."""
import json
import sys
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from fourview_inspector_r08 import inspect, similarity_under_reflections, _anchors


def painted_fixture(direction: int, structure: int = 1):
    """Deliberately flat polygons used ONLY by unit tests, not game renderer."""
    im = Image.new('RGBA', (300, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 30 + direction * 2
    col = [(90, 62, 45, 255), (80, 90, 68, 255), (76, 73, 99, 255)][structure - 1]
    d.rectangle([x, 105, 270, 262], fill=col)
    d.polygon([(x-5, 110), (145, 20 + 2 * direction), (277, 110)], fill=(38, 38, 45, 255))
    if direction == 0:
        d.rectangle([135, 174, 184, 262], fill=(12, 10, 14, 255))
        d.rectangle([60, 145, 100, 190], fill=(233, 178, 86, 255))
    elif direction == 1:
        d.rectangle([210, 157, 254, 207], fill=(218, 191, 99, 255))
        d.rectangle([75, 220, 110, 262], fill=(20, 25, 29, 255))
        d.rectangle([115, 117, 130, 145], fill=(215, 190, 154, 255))
    elif direction == 2:
        d.rectangle([72, 157, 115, 201], fill=(210, 184, 92, 255))
        d.rectangle([212, 181, 243, 221], fill=(210, 184, 92, 255))
        d.ellipse([144, 123, 173, 151], fill=(80, 15, 20, 255))
    else:
        d.rectangle([38, 192, 85, 261], fill=(210, 181, 142, 255))
        d.line([130, 126, 230, 220], fill=(245, 210, 120, 255), width=14)
        d.rectangle([155, 145, 190, 184], fill=(240, 220, 150, 255))
    return im


def fixture_manifests(directory):
    buildings = {}
    for n, name in [('1','cottage'), ('2','forge'), ('3','apothecary')]:
        faces, hashes = [], []
        for v in range(4):
            filename = f'r07_{name}_{v}'
            fp = directory / (filename+'.webp')
            painted_fixture(v, int(n)).save(fp, format='WEBP', lossless=True)
            faces.append(filename)
            hashes.append(sha256(fp.read_bytes()).hexdigest())
        buildings[n] = {'faces':faces,'sha256':hashes, 'license_checked':True, 'scale_anchor_reviewed':True}
    return {'state':'ART_CANDIDATE','buildings':buildings}


def replace_view(folder, manifest, building='1', view=1, image=None):
    prefix=manifest['buildings'][building]['faces'][view]
    p=folder/(prefix+'.webp')
    image.save(p, format='WEBP', lossless=True)
    manifest['buildings'][building]['sha256'][view]=sha256(p.read_bytes()).hexdigest()


class FourviewInspectorTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.assets=Path(self.temp.name)
        self.manifest=fixture_manifests(self.assets)

    def tearDown(self):self.temp.cleanup()

    def test_existing_project_still_blocked(self):
        d=json.loads((ROOT/'docs/R07_FACADE_ART_GATE.json').read_text())
        result=inspect(d,ROOT/'site/assets/world')
        self.assertEqual('BLOCKED',result['status'])
        self.assertEqual(0,result['buildings_with_four_physical_faces'])

    def test_distinct_synthetic_views_only_ready_for_human_review(self):
        result=inspect(self.manifest,self.assets)
        self.assertEqual('READY_FOR_HUMAN_VISUAL_REVIEW_ONLY',result['status'],result['technical_issues'])
        self.assertFalse(result['rendering_approved'])
        self.assertFalse(result['author_art_approved'])

    def test_manually_asserted_approval_does_not_certify_art(self):
        self.manifest['state']='AUTHOR_ART_APPROVED'
        result=inspect(self.manifest,self.assets)
        self.assertFalse(result['author_art_approved'])
        self.assertFalse(result['rendering_approved'])

    def test_exact_reuse_with_renamed_bytes_is_flagged(self):
        replace_view(self.assets,self.manifest,image=painted_fixture(0))
        result=inspect(self.manifest,self.assets)
        self.assertEqual('BLOCKED',result['status'])
        self.assertTrue(any('suspected_recolored' in s for s in result['technical_issues']))

    def test_mirrored_copy_with_distinct_file_hash_is_flagged(self):
        replace_view(self.assets,self.manifest,image=ImageOps.mirror(painted_fixture(0)))
        result=inspect(self.manifest,self.assets)
        self.assertEqual('BLOCKED',result['status'])
        self.assertTrue(any('suspected_recolored' in s for s in result['technical_issues']))

    def test_recolored_copy_with_distinct_hash_is_flagged(self):
        rgb=painted_fixture(0)
        rgba=Image.new('RGBA',rgb.size,(0,0,0,0))
        color=ImageEnhance.Color(rgb.convert('RGB')).enhance(.2)
        rgba.paste(color,mask=rgb.getchannel('A'))
        replace_view(self.assets,self.manifest,image=rgba)
        result=inspect(self.manifest,self.assets)
        self.assertEqual('BLOCKED',result['status'],result['technical_issues'])
        self.assertTrue(any('suspected_recolored' in s for s in result['technical_issues']))

    def test_wrong_hash_blocks(self):
        self.manifest['buildings']['2']['sha256'][2]='0'*64
        self.assertIn('2:2:hash_mismatch',inspect(self.manifest,self.assets)['technical_issues'])

    def test_file_missing_blocks(self):
        (self.assets/'r07_apothecary_3.webp').unlink()
        self.assertEqual('BLOCKED',inspect(self.manifest,self.assets)['status'])

    def test_ground_anchor_shift_blocks(self):
        base=painted_fixture(1)
        shifted=Image.new('RGBA',base.size,(0,0,0,0))
        shifted.alpha_composite(base.resize((175,175)),(48,0))
        replace_view(self.assets,self.manifest,image=shifted)
        result=inspect(self.manifest,self.assets)
        self.assertTrue(any('ground_anchor' in s for s in result['technical_issues']),result['technical_issues'])

    def test_missing_license_blocks(self):
        self.manifest['buildings']['1']['license_checked']=False
        self.assertIn('1:license_checked_not_verified',inspect(self.manifest,self.assets)['technical_issues'])

    def test_physical_alpha_required(self):
        self.assertIsNotNone(_anchors(painted_fixture(0)))
        invalid=Image.new('RGB',(300,300),(45,45,45))
        p=self.assets/'r07_forge_2.webp'
        invalid.save(p,format='WEBP')
        self.manifest['buildings']['2']['sha256'][2]=sha256(p.read_bytes()).hexdigest()
        result=inspect(self.manifest,self.assets)
        self.assertEqual('BLOCKED',result['status'])

    def test_symmetry_detection_is_never_an_approval(self):
        a=painted_fixture(0)
        same=ImageOps.mirror(a)
        sim=similarity_under_reflections(a,same)
        self.assertGreater(sim['luma_similarity'],.98)
        self.assertGreater(sim['edge_similarity'],.95)


if __name__=='__main__':unittest.main()
