"""Standalone laboratory authority-journal bridge for the R04 C++ world.
NOT the Windows game save, an account system, a server, or a replacement for Makers/MER.
All semantic changes are delegated to world_r04.cpp via ctypes; SQLite holds append-only receipts.
"""
import ctypes as c
from dataclasses import dataclass
import hashlib,json,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
FIELDS=('abi revision initialized primary secondary x y quest herbs work_xp remedies health focus sp '
'active_boss boss_hp boss_intent target_x target_y boss_phase defeats world_tick last_code '
'ore ingots mining_xp smithing_xp kit_ward kit_echo kit_burn kit_mark kit_root kit_tempo kit_fatigue '
'boss_pattern boss_turn being_last_talk weapon_grade '
'being_talk_mask last_talk_tick research_last_class research_last_action boss_pressure').split()
class State(c.Structure):_fields_=[(n,c.c_uint32) for n in FIELDS]
class Cmd(c.Structure):_fields_=[('abi',c.c_uint32),('expected_revision',c.c_uint32),('type',c.c_uint32),('value',c.c_int32)]

LIB=c.CDLL(str(ROOT/'artifacts/libns_world_r04.so'))
LIB.nsw_create.argtypes=[c.POINTER(State),c.c_uint32,c.c_uint32];LIB.nsw_create.restype=c.c_int32
LIB.nsw_apply.argtypes=[c.POINTER(State),c.POINTER(Cmd)];LIB.nsw_apply.restype=c.c_int32
class IntegrityError(RuntimeError):pass
class DuplicateConflict(RuntimeError):pass

def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(text):return hashlib.sha256(text.encode('utf-8')).hexdigest()
def state_digest(s):return sha(canonical({k:int(getattr(s,k)) for k in FIELDS}))
def apply(s,expected,type,value):return int(LIB.nsw_apply(c.byref(s),c.byref(Cmd(4,expected,type,value))))

class Ledger:
 def __init__(self,path:Path,create=False):
  self.path=Path(path)
  if create:
   if self.path.exists():raise FileExistsError(f'Existing SQLite protected: {self.path}')
   self.path.parent.mkdir(parents=True,exist_ok=True)
  elif not self.path.exists():raise FileNotFoundError(self.path)
  self.db=sqlite3.connect(self.path)
  self.db.row_factory=sqlite3.Row
  self.db.execute('PRAGMA foreign_keys=ON')
  if create:
   self.db.executescript('''
   CREATE TABLE sessions(session_id TEXT PRIMARY KEY, primary_class INTEGER NOT NULL, secondary_class INTEGER NOT NULL, revision INTEGER NOT NULL DEFAULT 0, head TEXT NOT NULL, CHECK(length(session_id)<=64));
   CREATE TABLE events(session_id TEXT NOT NULL REFERENCES sessions, revision INTEGER NOT NULL CHECK(revision>=1), request_uid TEXT NOT NULL, kind INTEGER NOT NULL, value INTEGER NOT NULL, result INTEGER NOT NULL, state_hash TEXT NOT NULL, prev_hash TEXT NOT NULL, chain_hash TEXT NOT NULL, PRIMARY KEY(session_id,revision), UNIQUE(session_id,request_uid));
   CREATE TABLE receipts(session_id TEXT NOT NULL REFERENCES sessions, request_uid TEXT NOT NULL, expected_revision INTEGER NOT NULL, kind INTEGER NOT NULL, value INTEGER NOT NULL, result INTEGER NOT NULL, after_revision INTEGER NOT NULL, state_hash TEXT NOT NULL, PRIMARY KEY(session_id,request_uid));
   PRAGMA user_version=4;''')
  else:
   if self.db.execute('PRAGMA user_version').fetchone()[0]!=4:raise IntegrityError('schema version mismatch')
 def close(self):self.db.close()
 def create_session(self,sid:str,primary:int,secondary:int=0):
  if not isinstance(sid,str) or not sid or len(sid)>64:raise ValueError('invalid session ID')
  s=State();rc=LIB.nsw_create(c.byref(s),primary,secondary)
  if rc!=1:raise ValueError('invalid class pairing')
  seed=sha(canonical({'sid':sid,'primary':primary,'secondary':secondary,'abi':4}))
  with self.db:self.db.execute('INSERT INTO sessions VALUES(?,?,?,?,?)',(sid,primary,secondary,0,seed))
  return state_digest(s)
 def _replay(self,sid:str):
  row=self.db.execute('SELECT * FROM sessions WHERE session_id=?',(sid,)).fetchone()
  if row is None:raise KeyError(sid)
  s=State();assert LIB.nsw_create(c.byref(s),row['primary_class'],row['secondary_class'])==1
  h=sha(canonical({'sid':sid,'primary':row['primary_class'],'secondary':row['secondary_class'],'abi':4}))
  for e in self.db.execute('SELECT * FROM events WHERE session_id=? ORDER BY revision',(sid,)):
   if e['revision']!=s.revision+1 or e['prev_hash']!=h:raise IntegrityError('revision or chain broken')
   rc=apply(s,s.revision,e['kind'],e['value'])
   if rc!=e['result'] or rc>=10:raise IntegrityError('native result differs')
   dig=state_digest(s)
   if dig!=e['state_hash']:raise IntegrityError('state digest differs')
   expected_hash=sha(canonical({'previous':h,'revision':e['revision'],'request_uid':e['request_uid'],'kind':e['kind'],'value':e['value'],'result':rc,'state_hash':dig}))
   if expected_hash!=e['chain_hash']:raise IntegrityError('event hash mismatch')
   h=expected_hash
  if row['revision']!=s.revision or row['head']!=h:raise IntegrityError('session head mismatch')
  # Receipts cannot claim a revision that does not exist.
  invalid=self.db.execute('SELECT COUNT(*) FROM receipts WHERE session_id=? AND after_revision> ?',(sid,s.revision)).fetchone()[0]
  if invalid:raise IntegrityError('receipt beyond accepted state')
  return s,h
 def snapshot(self,sid):
  s,h=self._replay(sid)
  return {'revision':s.revision,'state':{k:int(getattr(s,k)) for k in FIELDS},'head':h}
 def submit(self,sid:str,uid:str,expected:int,kind:int,value:int):
  if not isinstance(uid,str) or not (1<=len(uid)<=96):raise ValueError('invalid UID')
  if not all(isinstance(v,int) and not isinstance(v,bool) for v in (expected,kind,value)):raise ValueError('invalid numeric type')
  if not (0<=expected<=500000 and 0<=kind<=255 and -(2**31)<=value<=2**31-1):raise ValueError('out of range')
  try:
   self.db.execute('BEGIN IMMEDIATE')
   prior=self.db.execute('SELECT * FROM receipts WHERE session_id=? AND request_uid=?',(sid,uid)).fetchone()
   s,h=self._replay(sid)
   if prior:
    if (prior['expected_revision'],prior['kind'],prior['value'])!=(expected,kind,value):raise DuplicateConflict('UID reused for different payload')
    result={'code':prior['result'],'revision':prior['after_revision'],'digest':prior['state_hash'],'idempotent':True}
   else:
    rc=apply(s,expected,kind,value)
    dig=state_digest(s)
    if 0<rc<10:
     next_hash=sha(canonical({'previous':h,'revision':s.revision,'request_uid':uid,'kind':kind,'value':value,'result':rc,'state_hash':dig}))
     self.db.execute('INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?)',(sid,s.revision,uid,kind,value,rc,dig,h,next_hash))
     self.db.execute('UPDATE sessions SET revision=?,head=? WHERE session_id=?',(s.revision,next_hash,sid))
    self.db.execute('INSERT INTO receipts VALUES(?,?,?,?,?,?,?,?)',(sid,uid,expected,kind,value,rc,s.revision,dig))
    result={'code':rc,'revision':s.revision,'digest':dig,'idempotent':False}
   self.db.commit();return result
  except BaseException:
   self.db.rollback();raise
 def verify(self,sid):
  s,h=self._replay(sid)
  integrity=self.db.execute('PRAGMA integrity_check').fetchone()[0]
  if integrity!='ok':raise IntegrityError('SQLite integrity_check: '+integrity)
  return {'status':'PASS','revision':s.revision,'head':h,'events':self.db.execute('SELECT COUNT(*) FROM events WHERE session_id=?',(sid,)).fetchone()[0]}
