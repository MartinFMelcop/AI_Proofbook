"""Generate the R03 ledger adapter from the proven R02 implementation, changing only ABI/record shape.
Produces new file; R02 ledgers unchanged. This is a lab-only record consumer.
"""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'tools/world_r02_ledger.py').read_text()
s=s.replace('R02 C++ world','R03 C++ world').replace('world_r02.cpp','world_r03.cpp')
s=s.replace('libns_world_r02.so','libns_world_r03.so')
s=s.replace('boss_pattern boss_turn being_last_talk weapon_grade\').split()',
'''boss_pattern boss_turn being_last_talk weapon_grade '
'being_talk_mask last_talk_tick research_last_class research_last_action boss_pressure').split()''')
s=s.replace('Cmd(2,expected,type,value)','Cmd(3,expected,type,value)')
s=s.replace("'abi':2", "'abi':3")
s=s.replace('PRAGMA user_version=2','PRAGMA user_version=3')
s=s.replace('!=2:raise IntegrityError','!=3:raise IntegrityError')
s=s.replace('NOT the Windows game save','NOT the Windows game save')
(root/'tools/world_r03_ledger.py').write_text(s)
print('R03 ledger source',len(s))
