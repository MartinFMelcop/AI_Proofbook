"""Proves recoverability and fail-closed idempotency of a SQLite journal over C++ ABI2."""
import tempfile,unittest,sqlite3
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/"tools"))
from world_r02_ledger import Ledger,IntegrityError,DuplicateConflict

class LedgerR02Tests(unittest.TestCase):
 def setUp(self):
  self.dir=tempfile.TemporaryDirectory();self.addCleanup(self.dir.cleanup)
  self.db=Path(self.dir.name)/'fixture.sqlite';self.a=Ledger(self.db,create=True);self.addCleanup(self.a.close)
  self.a.create_session('owner-alpha',6,17)
 def test_uninitialized_file_is_protected(self):
  with self.assertRaises(FileExistsError):Ledger(self.db,create=True)
 def test_create_invalid_class(self):
  with self.assertRaises(ValueError):self.a.create_session('bad',0,0)
 def test_create_duplicate_session(self):
  with self.assertRaises(sqlite3.IntegrityError):self.a.create_session('owner-alpha',1,0)
 def test_move_native_and_replay(self):
  out=self.a.submit('owner-alpha','a1',0,1,0)
  self.assertEqual((out['code'],out['revision']),(1,1))
  self.assertEqual(self.a.verify('owner-alpha')['events'],1)
  self.assertEqual(self.a.snapshot('owner-alpha')['state']['y'],16)
 def test_idempotent_uid_same_payload(self):
  first=self.a.submit('owner-alpha','x',0,1,0)
  second=self.a.submit('owner-alpha','x',0,1,0)
  self.assertEqual(second['digest'],first['digest'])
  self.assertTrue(second['idempotent'])
  self.assertEqual(self.a.verify('owner-alpha')['events'],1)
 def test_duplicate_uid_different_payload_fail_closed(self):
  self.a.submit('owner-alpha','x',0,1,0)
  with self.assertRaises(DuplicateConflict):self.a.submit('owner-alpha','x',0,1,1)
  self.assertEqual(self.a.verify('owner-alpha')['events'],1)
 def test_stale_intent_record_no_mutation(self):
  self.a.submit('owner-alpha','x',0,1,0)
  denied=self.a.submit('owner-alpha','denied',0,1,0)
  self.assertEqual((denied['code'],denied['revision']),(10,1))
  self.assertEqual(self.a.verify('owner-alpha')['events'],1)
 def test_invalid_out_of_range_rejected(self):
  with self.assertRaises(ValueError):self.a.submit('owner-alpha','bad',0,1,2**40)
 def test_bool_rejected_as_number(self):
  with self.assertRaises(ValueError):self.a.submit('owner-alpha','bad',True,1,0)
 def test_missing_uid_rejected(self):
  with self.assertRaises(ValueError):self.a.submit('owner-alpha','',0,1,0)
 def test_tampered_event_detected(self):
  self.a.submit('owner-alpha','x',0,1,0)
  self.a.db.execute('UPDATE events SET value=2 WHERE request_uid=?',('x',));self.a.db.commit()
  with self.assertRaises(IntegrityError):self.a.verify('owner-alpha')
 def test_tampered_head_detected(self):
  self.a.submit('owner-alpha','x',0,1,0)
  self.a.db.execute("UPDATE sessions SET head='f' WHERE session_id='owner-alpha'");self.a.db.commit()
  with self.assertRaises(IntegrityError):self.a.verify('owner-alpha')
 def test_multiple_sessions_isolation(self):
  self.a.create_session('owner-beta',2,0)
  self.a.submit('owner-alpha','x',0,1,0)
  self.a.submit('owner-beta','x',0,1,3)
  self.assertEqual(self.a.snapshot('owner-alpha')['state']['y'],16)
  self.assertEqual(self.a.snapshot('owner-beta')['state']['x'],11)
 def test_snapshot_no_unknown_session(self):
  with self.assertRaises(KeyError):self.a.snapshot('missing')
 def test_persistence_reopen(self):
  self.a.submit('owner-alpha','x',0,1,0)
  second=Ledger(self.db)
  try:self.assertEqual(second.verify('owner-alpha')['revision'],1)
  finally:second.close()
 def test_failed_uid_replay_idempotent(self):
  first=self.a.submit('owner-alpha','deny',0,3,0)
  second=self.a.submit('owner-alpha','deny',0,3,0)
  self.assertEqual(first['code'],14);self.assertEqual(second['code'],14);self.assertTrue(second['idempotent'])
  self.assertEqual(self.a.verify('owner-alpha')['events'],0)
if __name__=='__main__':unittest.main(verbosity=2)
