#!/usr/bin/env python3
"""SQLite-only offline journal receipt for C++ world trace.
Not a server, not a Maker/MER migration, not the browser player's save.
Do NOT overwrite databases or mutate user-owned data. Pure stdlib.
"""
import argparse, hashlib, json, os, sqlite3
from pathlib import Path

SCHEMA_VERSION=1
SCHEMA="""
PRAGMA foreign_keys=ON;
CREATE TABLE journal_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE journal_event (
 sequence_no INTEGER PRIMARY KEY CHECK(sequence_no >= 0),
 expected_revision INTEGER NOT NULL CHECK(expected_revision >= 0),
 command_type INTEGER NOT NULL CHECK(command_type BETWEEN 1 AND 8),
 command_value INTEGER NOT NULL,
 return_code INTEGER NOT NULL CHECK(return_code BETWEEN 1 AND 6),
 state_json TEXT NOT NULL,
 previous_hash TEXT NOT NULL,
 event_hash TEXT NOT NULL UNIQUE
);
"""

def canonical(data):
 return json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':'))

def receipt(prev,sequence,event):
 doc={k:event[k] for k in ('rev','type','value','code','state')}
 content=canonical(doc)
 return hashlib.sha256((prev+'\n'+str(sequence)+'\n'+content).encode('utf-8')).hexdigest(),content

def create(db_path,trace_path):
 db_path=Path(db_path).absolute()
 if db_path.exists() or db_path.is_symlink():raise FileExistsError(f'Refusing to replace existing DB: {db_path}')
 if not db_path.parent.exists():raise FileNotFoundError(db_path.parent)
 trace=json.loads(Path(trace_path).read_text('utf-8'))
 if trace.get('schema')!='mmai.product.world.trace.v1':raise ValueError('Trace schema mismatch')
 events=trace.get('trace')
 if not isinstance(events,list) or not events or len(events)>10000:raise ValueError('Invalid trace size')
 cn=sqlite3.connect(f'file:{db_path}?mode=rwc',uri=True)
 try:
  cn.executescript(SCHEMA)
  prev='0'*64
  with cn:
   for i,e in enumerate(events):
    if e['rev']!=i or e['code'] not in range(1,7):raise ValueError('Nonmonotonic revision or unaccepted intent')
    digest,serialized=receipt(prev,i,e)
    cn.execute('INSERT INTO journal_event VALUES (?,?,?,?,?,?,?,?)',
      (i,e['rev'],e['type'],e['value'],e['code'],serialized,prev,digest))
    prev=digest
   for k,v in {'schema':str(SCHEMA_VERSION),'source':'mmai.product.world.trace.v1','events':str(len(events)),'terminal_hash':prev,'status':'LAB_FIXTURE_ONLY'}.items():
    cn.execute('INSERT INTO journal_meta VALUES (?,?)',(k,v))
  return {'events':len(events),'terminal_hash':prev,'sqlite_integrity':cn.execute('PRAGMA integrity_check').fetchone()[0]}
 except Exception:
  cn.close();db_path.unlink(missing_ok=True);raise
 finally:
  try:cn.close()
  except:pass

def verify(db_path):
 url=f'file:{Path(db_path).absolute()}?mode=ro'
 cn=sqlite3.connect(url,uri=True)
 try:
  if cn.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('SQLite integrity mismatch')
  meta=dict(cn.execute('SELECT key,value FROM journal_meta'))
  if meta.get('schema')!=str(SCHEMA_VERSION):raise ValueError('Schema mismatch')
  prev='0'*64;count=0
  for seq,rev,typ,val,rc,raw,old,digest in cn.execute('SELECT * FROM journal_event ORDER BY sequence_no'):
   if seq!=count or rev!=count or old!=prev:raise ValueError(f'Broken revision/chain at event {count}')
   event=json.loads(raw)
   if any(event[k]!=v for k,v in [('rev',rev),('type',typ),('value',val),('code',rc)]):raise ValueError('Tampered event columns')
   expected,content=receipt(prev,count,event)
   if raw!=content or expected!=digest:raise ValueError(f'Tampered event {count}')
   prev=expected;count+=1
  if meta['terminal_hash']!=prev or int(meta['events'])!=count:raise ValueError('Terminal hash/count mismatch')
  return {'PASS':True,'events':count,'terminal_hash':prev}
 finally:cn.close()

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['create','verify']);p.add_argument('database');p.add_argument('--trace');a=p.parse_args()
 print(json.dumps(create(a.database,a.trace) if a.action=='create' else verify(a.database),sort_keys=True))
if __name__=='__main__':main()
