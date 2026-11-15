"""Test a sheet importer with synthetic graphics, never North Star game art."""
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from import_fourview_atlas_r08 import import_atlas, _unpack
from test_r08_fourview_inspector import painted_fixture


def make_sheet(path, mode='RGBA', duplicates=False):
    im=Image.new('RGBA',(1200,900),(0,0,0,0))
    for row in range(3):
        for col in range(4):
            crop=painted_fixture(0 if duplicates else col,row+1)
            im.alpha_composite(crop,(300*col,300*row))
    if mode!='RGBA':im=im.convert(mode)
    im.save(path)


class AtlasImportTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.folder=Path(self.tmp.name)
        self.sheet=self.folder/'sheet.png'
        self.out=self.folder/'candidate'
        self.origin={'creator':'synthetic fixture','origin':'test suite only'}

    def tearDown(self):self.tmp.cleanup()

    def test_clean_3x4_sheet_exports_twelve_unapproved_candidates(self):
        make_sheet(self.sheet)
        report=import_atlas(self.sheet,self.out,self.origin)
        self.assertEqual(12,len(list(self.out.glob('r07_*.webp'))))
        self.assertEqual(3,report['buildings_with_four_physical_faces'])
        self.assertFalse(report['author_art_approved'])
        self.assertFalse(report['rendering_approved'])
        self.assertEqual('BLOCKED',report['status']) # rights + anchor ACK pending

    def test_repeated_view_atlas_detected(self):
        make_sheet(self.sheet,duplicates=True)
        report=import_atlas(self.sheet,self.out,self.origin)
        self.assertTrue(any('suspected_recolored' in s for s in report['technical_issues']))

    def test_non_rgba_is_rejected(self):
        make_sheet(self.sheet,'RGB')
        with self.assertRaisesRegex(ValueError,'RGBA'):import_atlas(self.sheet,self.out,self.origin)
        self.assertFalse(self.out.exists())

    def test_wrong_dimensions_is_rejected(self):
        Image.new('RGBA',(1231,900),(0,0,0,0)).save(self.sheet)
        with self.assertRaisesRegex(ValueError,'four equal columns'):import_atlas(self.sheet,self.out,self.origin)

    def test_incomplete_or_bleeding_atlas_is_rejected(self):
        im=Image.new('RGBA',(1200,900),(0,0,0,0))
        im.putpixel((0,0),(255,255,255,255))
        im.save(self.sheet)
        with self.assertRaises(ValueError):import_atlas(self.sheet,self.out,self.origin)

    def test_requires_provenance_and_never_overwrites(self):
        make_sheet(self.sheet)
        with self.assertRaisesRegex(ValueError,'creator'):import_atlas(self.sheet,self.out,{'origin':'x'})
        import_atlas(self.sheet,self.out,self.origin)
        with self.assertRaises(FileExistsError):import_atlas(self.sheet,self.out,self.origin)

    def test_original_r04_architecture_sheet_is_not_four_view_atlas(self):
        p=ROOT/'art_sources/r04_architecture_sheet.png'
        with self.assertRaises(ValueError):_unpack(p)


if __name__=='__main__':unittest.main()
