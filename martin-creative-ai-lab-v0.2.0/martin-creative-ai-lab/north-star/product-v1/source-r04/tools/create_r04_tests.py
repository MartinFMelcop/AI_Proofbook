from pathlib import Path
R=Path(__file__).resolve().parents[1]
def copy(src,dst):
 s=(R/src).read_text();s=s.replace('world_r03','world_r04').replace('WORLD_R03','WORLD_R04').replace('WorldR03','WorldR04').replace('R03','R04').replace('r03','r04')
 (R/dst).write_text(s)
copy('tests/test_world_r03.py','tests/test_world_r04.py')
# source test import from R03's shortest helper but use R04 local State and lib
p=R/'tests/test_world_r04.py';s=p.read_text().replace('Cmd(3,','Cmd(4,').replace('lib.nsw_abi(),3','lib.nsw_abi(),4').replace('Cmd(2,s.revision','Cmd(3,s.revision')
s=s.replace('"""R03 C++','"""R04 C++')
needle='class WorldR04(unittest.TestCase):'
add='''lib.nsw_boss_threatens.argtypes=[c.POINTER(State),c.c_uint32,c.c_uint32]
lib.nsw_boss_threatens.restype=c.c_uint32
lib.nsw_boss_threat_radius.argtypes=[c.POINTER(State)]
lib.nsw_boss_threat_radius.restype=c.c_uint32
'''
s=s.replace(needle,add+needle)
needle=' def test_abi(self):self.assertEqual(lib.nsw_abi(),4)'
assert needle in s
s=s.replace(needle,needle+'''
 def test_threat_query_is_pure_and_outside_range_safe(self):
  s=new(6);unlock(s);self.assertEqual(visit(s,5),3)
  before=bytes(s);r=lib.nsw_boss_threat_radius(c.byref(s))
  self.assertEqual(r,1)
  self.assertEqual(lib.nsw_boss_threatens(c.byref(s),s.target_x,s.target_y),1)
  self.assertEqual(lib.nsw_boss_threatens(c.byref(s),s.target_x+1,s.target_y),1)
  self.assertEqual(lib.nsw_boss_threatens(c.byref(s),s.target_x+2,s.target_y),0)
  self.assertEqual(lib.nsw_boss_threatens(c.byref(s),999,999),0)
  self.assertEqual(bytes(s),before)
 def test_threat_query_rejected_on_mismatched_abi(self):
  s=new();s.abi=3
  self.assertEqual(lib.nsw_boss_threatens(c.byref(s),s.x,s.y),0)
  self.assertEqual(lib.nsw_boss_threat_radius(c.byref(s)),0)
 def test_telegraph_moves_from_radius_one_to_two_in_boss_two(self):
  s=new(6);unlock(s);beat(s,1);self.assertEqual(visit(s,6),3)
  self.assertEqual(lib.nsw_boss_threat_radius(c.byref(s)),2)
  self.assertEqual(lib.nsw_boss_threatens(c.byref(s),s.target_x+2,s.target_y),1)
  self.assertEqual(lib.nsw_boss_threatens(c.byref(s),s.target_x+3,s.target_y),0)
 def test_threat_query_does_not_prevent_boss_damage(self):
  s=new(6);unlock(s);self.assertEqual(visit(s,5),3)
  before=s.health
  self.assertEqual(lib.nsw_boss_threatens(c.byref(s),s.x,s.y),1)
  self.assertEqual(action(s,5),1)  # observe while standing in telegraph; opponent hits
  self.assertLess(s.health,before)
  self.assertEqual(lib.nsw_boss_threat_radius(c.byref(s)),0)
''')
p.write_text(s)
copy('tests/generate_world_trace_r03.py','tests/generate_world_trace_r04.py')
p=R/'tests/generate_world_trace_r04.py';s=p.read_text().replace("'abi':3","'abi':4")
# Record C++ threat shape field for every action (no JS recalc).
needle="trace.append({'rev':before,'type':t,'value':v,'code':rc,'state':state,'beings':[lib.nsw_being_behavior(c.byref(s),i) for i in range(1,5)]})"
assert needle in s
s=s.replace(needle,"""trace.append({'rev':before,'type':t,'value':v,'code':rc,'state':state,'beings':[lib.nsw_being_behavior(c.byref(s),i) for i in range(1,5)],
 'threat':{'radius':lib.nsw_boss_threat_radius(c.byref(s)),
 'tiles':[lib.nsw_boss_threatens(c.byref(s),int(x),int(y)) for x,y in [(s.x,s.y),(s.target_x,s.target_y),(min(23,s.target_x+2),s.target_y),(23,19)]]}})""")
p.write_text(s)
copy('tools/world_r03_ledger.py','tools/world_r04_ledger.py')
p=R/'tools/world_r04_ledger.py';s=p.read_text().replace('Cmd(3,','Cmd(4,').replace("'abi':3","'abi':4").replace('PRAGMA user_version=3','PRAGMA user_version=4').replace('!=3:raise IntegrityError','!=4:raise IntegrityError');p.write_text(s)
copy('tools/create_r03_journal_fixture.py','tools/create_r04_journal_fixture.py')
copy('tests/test_world_r03_ledger.py','tests/test_world_r04_ledger.py')
p=R/'tests/test_world_r04_ledger.py';s=p.read_text().replace("fetchone()[0],3)","fetchone()[0],4)").replace("self.ledger.db.execute('PRAGMA user_version=2')","self.ledger.db.execute('PRAGMA user_version=3')")
p.write_text(s)
copy('tests/test_world_r03_wasm.mjs','tests/test_world_r04_wasm.mjs')
p=R/'tests/test_world_r04_wasm.mjs';s=p.read_text().replace('nsw_abi(),3','nsw_abi(),4')
needle=' count++;'
assert needle in s
s=s.replace(needle,''' const probes=[[e.nsw_wasm_x(),e.nsw_wasm_y()],[e.nsw_wasm_boss_target_x(),e.nsw_wasm_boss_target_y()],
  [Math.min(23,e.nsw_wasm_boss_target_x()+2),e.nsw_wasm_boss_target_y()],[23,19]];
 assert.equal(e.nsw_wasm_boss_threat_radius(),ev.threat.radius,'threat radius '+count);
 for(let j=0;j<probes.length;j++)assert.equal(e.nsw_wasm_boss_threatens(...probes[j]),ev.threat.tiles[j],'threat tile '+count+'/'+j);
 count++;''')
p.write_text(s)
copy('tests/c17_abi_r03.c','tests/c17_abi_r04.c')
p=R/'tests/c17_abi_r04.c';s=p.read_text().replace('nsw_abi()!=3u','nsw_abi()!=4u').replace('s.abi!=3u','s.abi!=4u').replace('move={3u','move={4u');
s=s.replace('move.expected_revision=0u;', '''if(nsw_boss_threat_radius(&s)!=0u||nsw_boss_threatens(&s,12,16)!=0u)return 8;
 move.expected_revision=0u;''')
p.write_text(s)
print('generated R04 focused tests, native and WASM replay, lab ledger, C17 consumer')
