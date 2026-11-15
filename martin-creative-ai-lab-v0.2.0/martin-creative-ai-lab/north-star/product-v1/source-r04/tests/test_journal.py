import sqlite3, tempfile, unittest, json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'tools'))
from spatial_journal_sqlite import create,verify
ROOT=Path(__file__).resolve().parent.parent
TRACE=ROOT/'artifacts/WORLD_NATIVE_TRACE.json'
class SpatialJournalTests(unittest.TestCase):
 def test_replay_receipt(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'fixture.sqlite';r=create(p,TRACE)
   self.assertEqual((r['events'],r['sqlite_integrity']),(100,'ok'))
   self.assertEqual(verify(p)['events'],100)
 def test_double_create_fail_closed(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'fixture.sqlite';create(p,TRACE)
   with self.assertRaises(FileExistsError):create(p,TRACE)
   self.assertEqual(verify(p)['events'],100)
 def test_tamper_hash_detects(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'fixture.sqlite';create(p,TRACE)
   db=sqlite3.connect(p)
   try:
    db.execute('UPDATE journal_event SET command_value=999 WHERE sequence_no=15')
    db.commit()
   finally:db.close()
   with self.assertRaises(ValueError):verify(p)
 def test_missing_source_does_not_create_database(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'fixture.sqlite'
   with self.assertRaises(FileNotFoundError):create(p,Path(t)/'not-there.json')
   self.assertFalse(p.exists())
 def test_reject_invalid_schema(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'fixture.sqlite';j=Path(t)/'invalid.json';j.write_text(json.dumps({'schema':'wrong','trace':[]}))
   with self.assertRaises(ValueError):create(p,j)
   self.assertFalse(p.exists())
if __name__=='__main__':unittest.main()
