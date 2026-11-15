"""SQLite R04 receipt/journal negative tests, isolated temporary databases, native owner only."""
import sys,unittest,tempfile,shutil,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from world_r04_ledger import Ledger,DuplicateConflict,IntegrityError
class R04LedgerTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name)/'lab.sqlite'
  self.ledger=Ledger(self.p,create=True);self.ledger.create_session('a',6,17)
 def tearDown(self):
  self.ledger.close();self.tmp.cleanup()
 def test_sqlite_schema_version_is_three(self):
  self.assertEqual(self.ledger.db.execute('PRAGMA user_version').fetchone()[0],4)
 def test_first_receipt_and_replay(self):
  r=self.ledger.submit('a','a-0',0,1,0)
  self.assertEqual((r['code'],r['revision']),(1,1));self.assertEqual(self.ledger.verify('a')['events'],1)
 def test_uid_replay_is_idempotent(self):
  a=self.ledger.submit('a','u0',0,1,0)
  b=self.ledger.submit('a','u0',0,1,0)
  self.assertEqual(a['digest'],b['digest']);self.assertTrue(b['idempotent'])
  self.assertEqual(self.ledger.verify('a')['events'],1)
 def test_uid_conflict_is_rejected(self):
  self.ledger.submit('a','u0',0,1,0)
  with self.assertRaises(DuplicateConflict):self.ledger.submit('a','u0',0,1,1)
  self.assertEqual(self.ledger.verify('a')['events'],1)
 def test_stale_revision_receipt_not_accepted_as_event(self):
  self.ledger.submit('a','u0',0,1,0)
  r=self.ledger.submit('a','u1',0,1,0)
  self.assertEqual((r['code'],r['revision']),(10,1))
  self.assertEqual(self.ledger.verify('a')['events'],1)
 def test_unsupported_command_fail_closed(self):
  r=self.ledger.submit('a','u0',0,12,0)
  self.assertEqual((r['code'],r['revision']),(11,0))
  self.assertEqual(self.ledger.verify('a')['events'],0)
 def test_receipt_recovery_isolation(self):
  self.ledger.create_session('b',18,0)
  self.ledger.submit('a','same',0,1,0)
  self.assertEqual(self.ledger.verify('b')['events'],0)
  self.ledger.submit('b','same',0,1,0)
  self.assertEqual(self.ledger.verify('b')['events'],1)
 def test_first_session_character_state_isolated(self):
  self.ledger.create_session('b',12,18)
  self.ledger.submit('a','u0',0,1,0)
  self.assertNotEqual(self.ledger.snapshot('a')['state']['revision'],self.ledger.snapshot('b')['state']['revision'])
 def test_tampered_accepted_result_detected(self):
  self.ledger.submit('a','u0',0,1,0)
  self.ledger.db.execute("UPDATE events SET result=3 WHERE session_id='a'")
  self.ledger.db.commit()
  with self.assertRaises(IntegrityError):self.ledger.verify('a')
 def test_tampered_chain_detected(self):
  self.ledger.submit('a','u0',0,1,0)
  self.ledger.db.execute("UPDATE events SET chain_hash='fake' WHERE session_id='a'");self.ledger.db.commit()
  with self.assertRaises(IntegrityError):self.ledger.verify('a')
 def test_create_existing_rejected(self):
  with self.assertRaises(FileExistsError):Ledger(self.p,create=True)
 def test_schema_from_r02_rejected(self):
  self.ledger.db.execute('PRAGMA user_version=3');self.ledger.db.commit();self.ledger.close()
  with self.assertRaises(IntegrityError):Ledger(self.p)
  self.ledger=Ledger(self.p,create=False) if False else self.ledger
 def test_fully_accepted_trace_fixture(self):
  fixed=Ledger(ROOT/'artifacts/R04_SQLITE_WORLD_JOURNAL.sqlite')
  try:
   result=fixed.verify('fixture-r04-six-seventeen')
   self.assertEqual(result['events'],121)
  finally:fixed.close()
if __name__=='__main__':unittest.main(verbosity=2)
