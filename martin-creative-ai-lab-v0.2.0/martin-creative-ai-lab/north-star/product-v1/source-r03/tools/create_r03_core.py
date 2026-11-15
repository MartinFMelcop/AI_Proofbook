"""Produce additive ABI3 owner from exactly the preserved R02 source, no in-place edits.
A research-only prototype; preserves all 21 historical profiles with no canonization.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
h=(ROOT/'core/world_r02.h').read_text()
c=(ROOT/'core/world_r02.cpp').read_text()
assert '#define NSW_ABI 2u' in h and 'c->type>10' in c
h=h.replace('#define NSW_WORLD_R02_H','#define NSW_WORLD_R03_H').replace('#define NS_WORLD_R02_H','#define NS_WORLD_R03_H')
h=h.replace('#define NSW_ABI 2u','#define NSW_ABI 3u')
h=h.replace(' uint32_t boss_pattern,boss_turn,being_last_talk,weapon_grade;',' uint32_t boss_pattern,boss_turn,being_last_talk,weapon_grade;\n // R03 append-only: bounded observable NPC feedback, and mechanics research receipts.\n uint32_t being_talk_mask,last_talk_tick,research_last_class,research_last_action,boss_pressure;')
h=h.replace('// 21 abilities are LAB_ONLY hypotheses, never canonical skills or balanced class kits.','// 8 skill (primary/secondary signature); 11 utility technique (primary/secondary).\n// 21 two-technique + passive LAB_ONLY kits are research hypotheses, not canonical skills or balanced kits.')
h=h.replace('NSW_API uint32_t nsw_kit_power(uint32_t class_id);','NSW_API uint32_t nsw_kit_power(uint32_t class_id);\nNSW_API uint32_t nsw_kit_aux_cost(uint32_t class_id);\nNSW_API uint32_t nsw_kit_passive_family(uint32_t class_id);')
h=h.replace('NSW_API uint32_t nsw_wasm_kit_power(uint32_t id);','NSW_API uint32_t nsw_wasm_kit_power(uint32_t id);\nNSW_API uint32_t nsw_wasm_kit_aux_cost(uint32_t id);\nNSW_API uint32_t nsw_wasm_kit_passive_family(uint32_t id);\nNSW_API uint32_t nsw_wasm_being_talk_mask(void);\nNSW_API uint32_t nsw_wasm_research_last_class(void);\nNSW_API uint32_t nsw_wasm_research_last_action(void);\nNSW_API uint32_t nsw_wasm_boss_pressure(void);')
# Keep public function name for compatibility; ABI3 is explicit and new wasm fail closes on ABI2 journal.
c=c.replace('#include "world_r02.h"','#include "world_r03.h"')
c=c.replace('constexpr uint32_t bossMax[3]={15u,20u,27u};','constexpr uint32_t bossMax[3]={15u,20u,27u};\n constexpr uint32_t auxCost[22]={0,2,2,2,2,2,2,2,2,2,3,2,3,2,2,2,2,2,2,2,2,2};')
c=c.replace('s.boss_pattern<=4&&s.boss_turn<=MAX_REV&&s.being_last_talk<=4&&s.weapon_grade<=2;',
'''s.boss_pattern<=6&&s.boss_turn<=MAX_REV&&s.being_last_talk<=4&&s.weapon_grade<=2&&
  s.being_talk_mask<=15&&s.last_talk_tick<=s.world_tick&&
  s.research_last_class<=21&&s.research_last_action<=2&&s.boss_pressure<=4;''')
c=c.replace('if(s.kit_echo&&s.boss_turn%2==0){','if(s.boss_pressure>0)--s.boss_pressure;\n  if(s.kit_echo&&s.boss_turn%2==0){')
c=c.replace('s.kit_ward=0;s.kit_mark=0;s.kit_root=0;s.kit_burn=0;s.kit_echo=0;s.kit_tempo=0;s.kit_fatigue=0;',
'''s.kit_ward=0;s.kit_mark=0;s.kit_root=0;s.kit_burn=0;s.kit_echo=0;s.kit_tempo=0;s.kit_fatigue=0;s.boss_pressure=0;''')
c=c.replace('(s.boss_pattern==2||s.boss_pattern==3)?2u:1u','(s.boss_pattern==2||s.boss_pattern==3||s.boss_pattern==5||s.boss_pattern==6)?2u:1u')
c=c.replace('if(s.boss_pattern==4)damage+=2;', 'if(s.boss_pattern==4)damage+=2;\n   if(s.boss_pattern==6)damage+=1;')
c=c.replace('if(s.active_boss==2&&!defending&&s.sp>0)--s.sp;',
'''if(s.active_boss==2&&!defending&&s.sp>0)--s.sp;
    if(s.boss_pattern==5&&!defending&&s.sp>0){s.sp=s.sp>1?s.sp-2:0;}
    if(s.boss_pattern==6&&!defending){s.boss_pressure=2; /* roots impede one movement request; defensible by guarding */}''')
c=c.replace('s.boss_pattern=(s.active_boss==1?(s.boss_phase&&s.boss_turn%4==0?4:1):s.active_boss==2?2:(s.boss_phase?3:1));',
'''s.boss_pattern=(s.active_boss==1?(s.boss_phase&&s.boss_turn%4==0?4:1):
     s.active_boss==2?(s.boss_phase&&s.boss_turn%3==0?5:2):
      (s.boss_phase?(s.boss_turn%3==0?6:3):1));''')
# New auxiliary spell function with 21 distinct conditions (no canonical skill name).
start=c.index('\n}\nextern "C" {')
extra='''
int utility(ns_world_state& s,uint32_t cls){
 if(cls<1||cls>21)return NSW_INVALID;
 if(s.sp<auxCost[cls])return NSW_NO_RESOURCE;
 const uint32_t d=dist(s.x,s.y,ax[s.active_boss+4],ay[s.active_boss+4]);
 if(d>4)return NSW_TOO_FAR;
 s.sp-=auxCost[cls];
 switch(cls){
  case 1:s.kit_ward=addCap(s.kit_ward,3,10);s.kit_mark=addCap(s.kit_mark,1,5);break; // Soldier: readiness
  case 2:s.focus=addCap(s.focus,s.boss_phase?2:1,3);break; // Dragon Slayer: scale read
  case 3:s.focus=addCap(s.focus,2,3);s.health=s.health>2?s.health-2:1;break; // Berserker: cost
  case 4:s.kit_tempo=addCap(s.kit_tempo,s.boss_intent==2?2:1,5);break; // Rogue A: window
  case 5:s.kit_root=addCap(s.kit_root,1,5);s.kit_tempo=addCap(s.kit_tempo,1,5);break; // Rogue B: bait
  case 6:s.kit_ward=addCap(s.kit_ward,6,10);break; // Knight: interpose
  case 7:s.kit_mark=addCap(s.kit_mark,d>=3?2:1,5);break; // Ranger: geometry
  case 8:s.kit_ward=addCap(s.kit_ward,d<=1?5:2,10);break; // Warrior: contact
  case 9:s.focus=addCap(s.focus,1,3);s.kit_ward=addCap(s.kit_ward,3,10);break; // Monk
  case 10:s.kit_echo=addCap(s.kit_echo,2,10);s.kit_ward=addCap(s.kit_ward,2,10);break; // Battlemage
  case 11:s.kit_mark=addCap(s.kit_mark,3,5);break; // Dark Mage: condition
  case 12:s.kit_burn=addCap(s.kit_burn,3,5);break; // Pyromancer: heat persistence
  case 13:s.kit_echo=addCap(s.kit_echo,4,10);break; // Necromancer: delayed agent proxy
  case 14:s.kit_tempo=addCap(s.kit_tempo,3,5);break; // Esper: bounded opportunity
  case 15:if(s.remedies){--s.remedies;s.kit_ward=addCap(s.kit_ward,8,10);}else{s.focus=addCap(s.focus,1,3);}break; // Alchemist
  case 16:s.kit_root=addCap(s.kit_root,3,5);break; // Cryomancer: temporary constraint
  case 17:s.kit_tempo=addCap(s.kit_tempo,1,5);s.focus=addCap(s.focus,1,3);break; // Bard: timing
  case 18:s.health=addCap(s.health,6,30);s.kit_ward=addCap(s.kit_ward,2,10);break; // Cleric
  case 19:if(nsw_tile(s.x,s.y)==2||nsw_tile(s.x,s.y)==6){s.health=addCap(s.health,5,30);}else{s.kit_ward=addCap(s.kit_ward,2,10);}break; // Druid
  case 20:s.kit_ward=addCap(s.kit_ward,7,10);break; // Sentinel
  case 21:s.kit_echo=addCap(s.kit_echo,2,10);s.kit_mark=addCap(s.kit_mark,2,5);break; // Shaman
 }
 s.research_last_class=cls;s.research_last_action=2;
 return opponent(s,false);
}
void passiveAtEncounter(ns_world_state& s,uint32_t cls,bool secondary){
 // Seven effect families, with 21 class-specific power/cost combinations: research-only.
 // Secondary carries a strictly weaker initial benefit; no infinite stacking.
 if(cls==0)return;
 uint32_t weight=secondary?1u:2u;
 switch((cls-1)%7){
  case 0:s.kit_ward=addCap(s.kit_ward,weight,10);break;
  case 1:s.focus=addCap(s.focus,weight,3);break;
  case 2:s.sp=addCap(s.sp,weight,8);break;
  case 3:s.kit_mark=addCap(s.kit_mark,weight,5);break;
  case 4:s.kit_tempo=addCap(s.kit_tempo,weight,5);break;
  case 5:s.health=addCap(s.health,weight+1,30);break;
  case 6:s.kit_echo=addCap(s.kit_echo,weight,10);break;
 }
}
'''
c=c[:start]+extra+c[start:]
c=c.replace('uint32_t nsw_kit_power(uint32_t cls){return cls<=21?kitPower[cls]:0;}','uint32_t nsw_kit_power(uint32_t cls){return cls<=21?kitPower[cls]:0;}\nuint32_t nsw_kit_aux_cost(uint32_t cls){return cls<=21?auxCost[cls]:0;}\nuint32_t nsw_kit_passive_family(uint32_t cls){return cls>=1&&cls<=21?1+(cls-1)%7:0;}')
c=c.replace('uint32_t proximity=dist(s->x,s->y,x,y);','uint32_t proximity=dist(s->x,s->y,x,y);\n if(s->being_last_talk==id&&s->world_tick-s->last_talk_tick<=4&&proximity<=3)return 2;')
c=c.replace('if(c->abi!=NSW_ABI||c->type<1||c->type>10)return NSW_INVALID;','if(c->abi!=NSW_ABI||c->type<1||c->type>11)return NSW_INVALID;')
c=c.replace('if(c->type==1){\n  if(c->value<0||c->value>3)return NSW_INVALID;',
'''if(c->type==1){
  if(c->value<0||c->value>3)return NSW_INVALID;
  if(s->active_boss&&s->boss_pressure>0)return NSW_BLOCKED;''')
c=c.replace('s->kit_ward=0;s->kit_echo=0;s->kit_burn=0;s->kit_mark=0;s->kit_root=0;s->kit_tempo=0;\n   rc=NSW_BOSS_START;',
'''s->kit_ward=0;s->kit_echo=0;s->kit_burn=0;s->kit_mark=0;s->kit_root=0;s->kit_tempo=0;s->boss_pressure=0;
   passiveAtEncounter(*s,s->primary,false);passiveAtEncounter(*s,s->secondary,true);
   rc=NSW_BOSS_START;''')
c=c.replace('s->kit_ward=0;s->kit_echo=0;s->kit_burn=0;s->kit_mark=0;s->kit_root=0;s->kit_tempo=0;rc=NSW_OK;',
'''s->kit_ward=0;s->kit_echo=0;s->kit_burn=0;s->kit_mark=0;s->kit_root=0;s->kit_tempo=0;s->boss_pressure=0;rc=NSW_OK;''')
c=c.replace('rc=cast(*s,cls);','rc=cast(*s,cls);\n   if(rc<10){s->research_last_class=cls;s->research_last_action=1;}')
c=c.replace('}else if(c->type==3){', '''}else if(c->type==11){
   if(c->value!=0&&c->value!=1)return NSW_INVALID;
   const uint32_t cls=(c->value==0?s->primary:s->secondary);
   if(!cls)return NSW_INVALID;
   rc=utility(*s,cls);
  }else if(c->type==3){''')
c=c.replace('s->being_last_talk=id;rc=NSW_OK;',
'''s->being_last_talk=id;s->being_talk_mask|=(1u<<(id-1));
  s->last_talk_tick=s->world_tick+1;rc=NSW_OK;''')
c=c.replace('NSW_GET(boss_pattern) NSW_GET(boss_turn) NSW_GET(weapon_grade)',
'NSW_GET(boss_pattern) NSW_GET(boss_turn) NSW_GET(weapon_grade)\nNSW_GET(being_talk_mask) NSW_GET(research_last_class) NSW_GET(research_last_action) NSW_GET(boss_pressure)')
c=c.replace('uint32_t nsw_wasm_kit_power(uint32_t cls){return nsw_kit_power(cls);}',
'''uint32_t nsw_wasm_kit_power(uint32_t cls){return nsw_kit_power(cls);}
uint32_t nsw_wasm_kit_aux_cost(uint32_t cls){return nsw_kit_aux_cost(cls);}
uint32_t nsw_wasm_kit_passive_family(uint32_t cls){return nsw_kit_passive_family(cls);}''')
(ROOT/'core/world_r03.h').write_text(h)
(ROOT/'core/world_r03.cpp').write_text(c)
print('R03 C++',len(c),'header',len(h))
