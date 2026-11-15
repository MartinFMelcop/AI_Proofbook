"""Annotate 21 experimental two-active + passive kits against Combat Philosophies.
No authorization to canonize mechanics, weapons, characters, bosses or independent Rogues.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
raw=json.loads((ROOT/'docs/R02_CLASS_RESEARCH_BINDINGS.json').read_text())
assert len(raw['records'])==21
aux=[
 'Preparar linha e marca', 'Analisar escala em movimento', 'Reforçar pressão assumindo custo',
 'Guardar a abertura possível', 'Finta com resposta incerta', 'Interposição adicional',
 'Marcação por distância', 'Aparar pelo contato', 'Concentrar e redirecionar',
 'Tecer proteção com eco', 'Condicionar e marcar', 'Propagar calor residual',
 'Eco de agente diferido', 'Antecipação limitada', 'Destilar o que foi coletado',
 'Restringir passagem temporariamente', 'Marcar o tempo compartilhado',
 'Abrigo e recuperação', 'Florescer com terreno existente', 'Guardar um setor',
 'Foco ancorado e eco limitado'
]
passives=['Preparação defensiva','Abertura de foco','Fôlego inicial','Marcação de oportunidade','Reserva temporal','Preservação','Eco diferido']
cost=[0,2,2,2,2,2,2,2,2,2,3,2,3,2,2,2,2,2,2,2,2,2]
records=[]
for i,r in enumerate(raw['records'],1):
 assert r['id']==i
 records.append({**r,'signature_active':{'name':r['lab_mode_name'],'research_cost':None,'implementation':'core/world_r03.cpp cast switch(cls)'},
  'utility_active':{'name':aux[i-1],'research_sp_cost':cost[i],'implementation':'core/world_r03.cpp utility switch(cls)'},
  'passive_study':{'name':passives[(i-1)%7],'family':1+(i-1)%7,'application':'bounded once at boss start, primary stronger than secondary'},
  'identity_status':'PENDING_A2' if i in (4,5) else 'RESEARCH_NOT_CANON',
  'canonical_skill_id':None,'canonical_kit_id':None,'weapon_ids':None,'skills_implemented':2,
  'passives_researched':1,'qa':'MECHANICAL_FIXTURE_ONLY', 'source_drive_id':raw['source_drive_id']})
manifest={'schema':'mmai.r03.class-kit-research.v1','source_title':'Combat Philosophies and Other Complements','source_drive_id':raw['source_drive_id'],
 'source_anchor':'Class profiles R01–R21; class philosophy A2=21 attempted identities, Rogue A/B independence unproven',
 'canon':'NO_NEW_CANON','rogue_a_b':'SHARED_LEGACY_KEY_UNVERIFIED','mechanics':'LAB_NOT_BALANCED',
 'approval_gate':['CLASS_OWNER_ACK','IDENTITY_21_GATE','COMBAT_BALANCE','ART_PALLETE','ACCESSIBILITY','WEAPON_DATA','NPC_LORE_GATE'],
 'records':records}
(ROOT/'docs/R03_CLASS_KITS_LAB.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
(ROOT/'site/classes_r03.js').write_text('// Two-active + passive studies, NOT author-approved class kits.\nwindow.NSKitLab='+json.dumps(records,ensure_ascii=False,separators=(',',':'))+';\n')
print(json.dumps({'kits':len(records),'actives':len(records)*2,'passive_families':7}))
