#include "world_r04.h"
#ifdef NS_PRODUCT_WASM
// Freestanding WASM libc shim: deterministic memory zeroing only, no runtime host.
#include <stddef.h>
extern "C" void* memset(void* dst,int c,size_t n){
 volatile unsigned char* p=(volatile unsigned char*)dst;
 for(size_t i=0;i<n;i++)p[i]=(unsigned char)c;
 return dst;
}
#endif
namespace {
 constexpr uint32_t MAX_REV=500000u;
 constexpr uint32_t bossMax[3]={15u,20u,27u};
 constexpr uint32_t auxCost[22]={0,2,2,2,2,2,2,2,2,2,3,2,3,2,2,2,2,2,2,2,2,2};
 // R02 research-only expressive modes; each Rxx is a profile, NOT an approved skill.
 constexpr uint32_t kitCost[22]={0,2,3,2,2,2,2,2,2,2,3,2,3,2,2,3,2,2,2,2,2,2};
 constexpr uint32_t kitPower[22]={0,4,6,7,9,3,3,6,8,5,5,5,4,3,2,8,3,2,2,5,2,3};
 constexpr uint32_t ax[10]={0,13,13,6,16,20,4,12,18,17};
 constexpr uint32_t ay[10]={0,16,10,11,10,5,5,3,7,11};
 inline uint32_t dist(uint32_t x,uint32_t y,uint32_t a,uint32_t b){return (x>a?x-a:a-x)+(y>b?y-b:b-y);}
 // A pure authoritative threat predicate; visual consumer may only query it.
 inline uint32_t threatRadius(const ns_world_state& s){
  if(s.active_boss==0||s.boss_intent!=1)return 0;
  return (s.boss_pattern==2||s.boss_pattern==3||s.boss_pattern==5||s.boss_pattern==6)?2u:1u;
 }
 inline bool threatens(const ns_world_state& s,uint32_t x,uint32_t y){
  return s.active_boss>0&&s.boss_intent==1&&x<NSW_COLUMNS&&y<NSW_ROWS&&
   dist(x,y,s.target_x,s.target_y)<=threatRadius(s);
 }
 bool check(const ns_world_state& s){
  return s.abi==NSW_ABI&&s.initialized==1&&s.primary>=1&&s.primary<=21&&
  s.secondary<=21&&s.primary!=s.secondary&&s.revision<=MAX_REV&&
  s.x>0&&s.x<NSW_COLUMNS-1&&s.y>0&&s.y<NSW_ROWS-1&&s.quest<=7&&
  s.herbs<=2&&s.work_xp<=100&&s.remedies<=3&&s.health<=30&&s.focus<=3&&s.sp<=8&&
  s.defeats<=3&&s.active_boss<=3&&s.boss_phase<=1&&s.boss_intent<=2&&
  ((s.active_boss==0&&s.boss_hp==0&&s.boss_intent==0)||
   (s.active_boss==s.defeats+1 &&s.boss_hp>0&&s.boss_hp<=bossMax[s.defeats]&&s.boss_intent>0))&&
  s.quest>=s.defeats+4*(s.defeats>0)&&s.ore<=3&&s.ingots<=3&&
  s.mining_xp<=100&&s.smithing_xp<=100&&s.kit_ward<=10&&s.kit_echo<=10&&
  s.kit_burn<=5&&s.kit_mark<=5&&s.kit_root<=5&&s.kit_tempo<=5&&s.kit_fatigue<=3&&
  s.boss_pattern<=6&&s.boss_turn<=MAX_REV&&s.being_last_talk<=4&&s.weapon_grade<=2&&
  s.being_talk_mask<=15&&s.last_talk_tick<=s.world_tick&&
  s.research_last_class<=21&&s.research_last_action<=2&&s.boss_pressure<=4;
 }
 // Only C++ owns opponent intents/telegraphs and world results.
 inline void hit(ns_world_state& s,uint32_t dmg){s.boss_hp=s.boss_hp>dmg?s.boss_hp-dmg:0;}
 inline uint32_t addCap(uint32_t a,uint32_t b,uint32_t max){return a+b>max?max:a+b;}
 int opponent(ns_world_state& s,bool defending){
  ++s.boss_turn;
  if(s.boss_pressure>0)--s.boss_pressure;
  if(s.kit_echo&&s.boss_turn%2==0){hit(s,s.kit_echo);s.kit_echo=0;}
  if(s.kit_burn){hit(s,2);--s.kit_burn;}
  if(s.boss_hp==0){
   s.active_boss=0;s.boss_intent=0;s.boss_phase=0;s.boss_pattern=0;s.focus=0;
   s.kit_ward=0;s.kit_mark=0;s.kit_root=0;s.kit_burn=0;s.kit_echo=0;s.kit_tempo=0;s.kit_fatigue=0;s.boss_pressure=0;
   ++s.defeats;s.quest=4+s.defeats;s.remedies=s.remedies<3?s.remedies+1:3;
   s.health=addCap(s.health,8,30);s.sp=8;
   return s.defeats==3?NSW_FINALE:NSW_BOSS_WIN;
  }
  s.boss_phase=s.boss_hp<=(bossMax[s.active_boss-1]/2)?1:0;
  // Existing two-beat pattern preserved: tell -> strike -> new tell.
  if(s.boss_intent==1){
   if(s.kit_root){--s.kit_root;s.boss_intent=2;return NSW_OK;}

   uint32_t damage=3u+s.active_boss+s.boss_phase*2u;
   if(s.boss_pattern==4)damage+=2;
   if(s.boss_pattern==6)damage+=1; // B01 phase-two feint, distinct cue.
   if(threatens(s,s.x,s.y)){
    if(defending)damage=(damage+3)/4;
    const uint32_t absorbed=s.kit_ward<damage?s.kit_ward:damage;
    s.kit_ward-=absorbed;damage-=absorbed;
    s.health=s.health>damage?s.health-damage:0;
    if(s.active_boss==2&&!defending&&s.sp>0)--s.sp;
    if(s.boss_pattern==5&&!defending&&s.sp>0){s.sp=s.sp>1?s.sp-2:0;}
    if(s.boss_pattern==6&&!defending){s.boss_pressure=2; /* roots impede one movement request; defensible by guarding */}
    if(s.active_boss==3&&s.boss_phase&&!defending&&s.focus>0)--s.focus;
   }
   s.boss_intent=2;
  }else{
   s.boss_intent=1;s.target_x=s.x;s.target_y=s.y;
   s.boss_pattern=(s.active_boss==1?(s.boss_phase&&s.boss_turn%4==0?4:1):
     s.active_boss==2?(s.boss_phase&&s.boss_turn%3==0?5:2):
      (s.boss_phase?(s.boss_turn%3==0?6:3):1));
   if(s.kit_tempo){--s.kit_tempo;s.boss_intent=2;} // temporary opportunity, explicit owner state
  }
  return s.health?NSW_OK:NSW_DEFEATED;
 }
 int cast(ns_world_state& s,uint32_t cls){
  if(cls<1||cls>21)return NSW_INVALID;
  if(s.sp<kitCost[cls])return NSW_NO_RESOURCE;
  const uint32_t d=dist(s.x,s.y,ax[s.active_boss+4],ay[s.active_boss+4]);
  if(d>(cls==7?5u:3u))return NSW_TOO_FAR;
  const uint32_t beforeHp=s.health;
  s.sp-=kitCost[cls];uint32_t dmg=0;
  switch(cls){
   case 1:dmg=4;s.kit_mark=addCap(s.kit_mark,1,5);s.kit_ward=addCap(s.kit_ward,1,10);break; // coordination
   case 2:dmg=3+(s.boss_phase?6u:1u);break; // scale under changing conditions
   case 3:dmg=7;s.health=s.health>2?s.health-2:1;break; // pressure has a cost
   case 4:dmg=(s.boss_intent==2?9u:3u);break; // exploit real opening
   case 5:dmg=3;s.kit_root=addCap(s.kit_root,1,5);s.kit_ward=addCap(s.kit_ward,1,10);break; // bait, limited opportunity
   case 6:dmg=3;s.kit_ward=addCap(s.kit_ward,5,10);break; // interpose
   case 7:dmg=3+(d>=3?3u:0u);break; // geometry
   case 8:dmg=4+(d<=1?4u:0u);break; // contact
   case 9:dmg=2+s.focus*2;s.kit_ward=addCap(s.kit_ward,3,10);break; // redirect
   case 10:dmg=5;s.kit_ward=addCap(s.kit_ward,2,10);break; // blended
   case 11:dmg=3;s.kit_mark=addCap(s.kit_mark,2,5);break; // conditions
   case 12:dmg=4;s.kit_burn=addCap(s.kit_burn,2,5);break; // propagating heat
   case 13:dmg=3;s.kit_echo=addCap(s.kit_echo,3,10);break; // deferred agent (simulation only)
   case 14:dmg=2;s.kit_tempo=addCap(s.kit_tempo,2,5);break; // uncertain foresight: opportunity not omniscience
   case 15:dmg=s.remedies?8u:4u;if(s.remedies)--s.remedies;break; // materials matter
   case 16:dmg=3;s.kit_root=addCap(s.kit_root,2,5);break; // temporary space restriction
   case 17:dmg=2;s.sp=addCap(s.sp,2,8);s.kit_tempo=addCap(s.kit_tempo,1,5);break; // timing
   case 18:dmg=2;s.health=addCap(s.health,8,30);break; // preservation
   case 19:dmg=3;if(nsw_tile(s.x,s.y)==2||nsw_tile(s.x,s.y)==6)s.health=addCap(s.health,5,30);else s.kit_ward=addCap(s.kit_ward,1,10);break; // environment
   case 20:dmg=2;s.kit_ward=addCap(s.kit_ward,s.boss_intent==1?6u:4u,10);break; // sector defense
   case 21:dmg=2;s.kit_mark=addCap(s.kit_mark,1,5);s.kit_echo=addCap(s.kit_echo,2,10);break; // spatial focus
  }
  hit(s,dmg);
  // All cases retain the opponent's turn and are replayable.
  const int out=opponent(s,false);
  if(beforeHp==0&&out==NSW_OK)return NSW_DEFEATED;
  return out;
 }

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

}
extern "C" {
uint32_t nsw_abi(void){return NSW_ABI;}
uint32_t nsw_boss_threatens(const ns_world_state* s,uint32_t x,uint32_t y){return s&&check(*s)&&threatens(*s,x,y)?1u:0u;}
uint32_t nsw_boss_threat_radius(const ns_world_state* s){return s&&check(*s)?threatRadius(*s):0u;}

uint32_t nsw_kit_mode(uint32_t cls){return cls<=21?cls:0;}
uint32_t nsw_kit_cost(uint32_t cls){return cls<=21?kitCost[cls]:0;}
uint32_t nsw_kit_power(uint32_t cls){return cls<=21?kitPower[cls]:0;}
uint32_t nsw_kit_aux_cost(uint32_t cls){return cls<=21?auxCost[cls]:0;}
uint32_t nsw_kit_passive_family(uint32_t cls){return cls>=1&&cls<=21?1+(cls-1)%7:0;}
uint32_t nsw_being_behavior(const ns_world_state* s,uint32_t id){
 if(!s||!s->initialized||id<1||id>4)return 0;
 uint32_t x=nsw_being_x(id,s->world_tick),y=nsw_being_y(id,s->world_tick);
 uint32_t proximity=dist(s->x,s->y,x,y);
 if(s->being_last_talk==id&&s->world_tick-s->last_talk_tick<=4&&proximity<=3)return 2;
 if(s->active_boss>0&&proximity<=3)return 5; // alarm / avoids combat
 if(id==1&&s->quest==0&&proximity<=2)return 2; // noticing newcomer
 if(id==2&&s->quest==1&&proximity<=2)return 4; // concern
 if(proximity<=2)return 2; // regard attention not mind-reading
 if(id==3&&((s->world_tick/9)%3)==0)return 3; // market activity
 if(id==4&&s->quest>=2&&((s->world_tick/8)%2)==1)return 3; // herbalist works
 return ((s->world_tick/8+id)%3)==0?1:0; // controlled ambient idle/motion
}
uint32_t nsw_object_x(uint32_t id){return id<10?ax[id]:0;}
uint32_t nsw_object_y(uint32_t id){return id<10?ay[id]:0;}
uint32_t nsw_being_x(uint32_t id,uint32_t tick){
 switch(id){case 1:return 13u+(tick/8u)%2u;case 2:return 13u;case 3:return 18u-(tick/12u)%2u;case 4:return 6u;default:return 0u;}}
uint32_t nsw_being_y(uint32_t id,uint32_t tick){
 switch(id){case 1:return 16u;case 2:return 10u;case 3:return 10u;case 4:return 10u+(tick/9u)%2u;default:return 0u;}}
uint32_t nsw_tile(uint32_t x,uint32_t y){
 if(x>=NSW_COLUMNS||y>=NSW_ROWS)return 4; // impassable wall
 if(x==0||y==0||x==23||y==19)return 4;
 if(y==14) return x>=10&&x<=14?7:3; // river and stone bridge
 if((x==10&&y>=7&&y<=9)||(x==17&&y>=8&&y<=9)||(x==20&&y>=10&&y<=11))return 9; // buildings
 if((x==2||x==3)&&(y>=2&&y<=4))return 8;
 if((x==8||x==9)&&y>=3&&y<=5)return 8;
 if(x>=17&&x<=19&&y==3)return 8;
 if(x>=2&&x<=7&&y>=3&&y<=8)return 6; // marsh, passable except ruins
 if((x>=9&&x<=16&&y>=7&&y<=13)||(x>=11&&x<=13&&y>=14))return 1; // village paving
 if(x>=18&&y<=7&&((x+y)%4==0))return 9; // scattered ruins
 if(x>=10&&x<=14&&y<=6)return 2; // guardian grove
 return ((x*17+y*13)%9<3)?2:0;
}
void nsw_reset(ns_world_state* s){if(s){*s={};s->abi=NSW_ABI;s->x=12;s->y=17;s->remedies=2;s->health=30;s->sp=8;}}
int32_t nsw_create(ns_world_state* s,uint32_t a,uint32_t b){
 if(!s)return NSW_INVALID;
 nsw_reset(s);
 if(a<1||a>21||b>21||b==a)return NSW_INVALID;
 s->initialized=1;s->primary=a;s->secondary=b;s->last_code=NSW_OK;
 return NSW_OK;
}
int32_t nsw_apply(ns_world_state* s,const ns_world_command* c){
 if(!s||!c||!check(*s))return NSW_NO_SESSION;
 if(c->abi!=NSW_ABI||c->type<1||c->type>11)return NSW_INVALID;
 if(c->expected_revision!=s->revision)return NSW_STALE;
 if(s->active_boss && s->health==0 && c->type!=7)return NSW_CANNOT_ACT;
 if(s->revision>=MAX_REV)return NSW_INVALID;
 int rc=NSW_WRONG_STAGE;
 if(c->type==1){
  if(c->value<0||c->value>3)return NSW_INVALID;
  if(s->active_boss&&s->boss_pressure>0)return NSW_BLOCKED;
  uint32_t xx=s->x,yy=s->y;
  if(c->value==0 &&yy>0)--yy;
  if(c->value==1 &&xx<NSW_COLUMNS-1)++xx;
  if(c->value==2 &&yy<NSW_ROWS-1)++yy;
  if(c->value==3 &&xx>0)--xx;
  uint32_t tile=nsw_tile(xx,yy);
  if(tile==3||tile==4||tile==8||tile==9)return NSW_BLOCKED;
  s->x=xx;s->y=yy;rc=s->active_boss?opponent(*s,false):NSW_OK;
 }else if(c->type==2){
  uint32_t target=static_cast<uint32_t>(c->value);
  if(c->value<1||c->value>7)return NSW_INVALID;
  if(s->active_boss)return NSW_WRONG_STAGE;
  if(dist(s->x,s->y,ax[target],ay[target])>2)return NSW_TOO_FAR;
  if(target==1&&s->quest==0){s->quest=1;rc=NSW_QUEST;}
  else if(target==2&&s->quest==1){s->quest=2;rc=NSW_QUEST;}
  else if(target==3&&s->quest==2){
   if(s->herbs<2){++s->herbs;s->work_xp+=5;rc=NSW_OK;}
   if(s->herbs==2){s->quest=3;rc=NSW_QUEST;}
  }else if(target==4&&s->quest==3&&s->herbs==2){s->herbs=0;s->quest=4;s->remedies=3;rc=NSW_QUEST;}
  else if(target>=5&&target<=7&&s->quest==target-1&&s->health>0){
   s->active_boss=target-4;s->boss_hp=bossMax[s->active_boss-1];
   s->boss_intent=1;s->target_x=s->x;s->target_y=s->y;s->boss_phase=0;
   s->boss_pattern=s->active_boss==2?2:1;s->boss_turn=0;
   s->kit_ward=0;s->kit_echo=0;s->kit_burn=0;s->kit_mark=0;s->kit_root=0;s->kit_tempo=0;s->boss_pressure=0;
   passiveAtEncounter(*s,s->primary,false);passiveAtEncounter(*s,s->secondary,true);
   rc=NSW_BOSS_START;
  }
 }else if(s->active_boss){
  if(c->type==7){s->active_boss=0;s->boss_hp=0;s->boss_intent=0;s->boss_phase=0;s->boss_pattern=0;s->health=30;s->sp=8;s->focus=0;
   s->kit_ward=0;s->kit_echo=0;s->kit_burn=0;s->kit_mark=0;s->kit_root=0;s->kit_tempo=0;s->boss_pressure=0;rc=NSW_OK;}
  else if(s->health==0)return NSW_CANNOT_ACT;
  else if(c->type==6){
   if(s->remedies==0)return NSW_NO_RESOURCE;
   --s->remedies;s->health=(s->health+9>30)?30:s->health+9;rc=opponent(*s,false);
  }else if(c->type==8){
   if(c->value!=0&&c->value!=1)return NSW_INVALID;
   uint32_t cls=(c->value==0?s->primary:s->secondary);
   if(!cls)return NSW_INVALID;
   rc=cast(*s,cls);
   if(rc<10){s->research_last_class=cls;s->research_last_action=1;}
  }else if(c->type==11){
   if(c->value!=0&&c->value!=1)return NSW_INVALID;
   const uint32_t cls=(c->value==0?s->primary:s->secondary);
   if(!cls)return NSW_INVALID;
   rc=utility(*s,cls);
  }else if(c->type==3){
   if(dist(s->x,s->y,ax[s->active_boss+4],ay[s->active_boss+4])>3)return NSW_TOO_FAR;
   uint32_t damage=3+static_cast<uint32_t>(s->focus>0)+s->weapon_grade+s->kit_mark;
   s->kit_mark=0;
   s->boss_hp=s->boss_hp>damage?s->boss_hp-damage:0;s->focus=0;
   rc=opponent(*s,false);
  }else if(c->type==4){rc=opponent(*s,true);}
  else if(c->type==5){if(s->focus<3)++s->focus;rc=opponent(*s,false);}
  else if(c->type==1){rc=NSW_OK;} // movement already handled above
 }else if(c->type==9){ // side-professions, only after the leader, without quest shortcuts
  if(s->quest<2)return NSW_WRONG_STAGE;
  const int v=c->value;if(v<1||v>3)return NSW_INVALID;
  uint32_t node=(v==1?8:9);
  if(dist(s->x,s->y,ax[node],ay[node])>2)return NSW_TOO_FAR;
  if(v==1){if(s->ore>=3)return NSW_NO_RESOURCE;++s->ore;s->mining_xp=addCap(s->mining_xp,7,100);rc=NSW_OK;}
  else if(v==2){if(s->ore==0||s->ingots>=3)return NSW_NO_RESOURCE;--s->ore;++s->ingots;s->smithing_xp=addCap(s->smithing_xp,9,100);rc=NSW_OK;}
  else{if(s->ingots==0||s->weapon_grade>=2)return NSW_NO_RESOURCE;--s->ingots;++s->weapon_grade;s->smithing_xp=addCap(s->smithing_xp,12,100);rc=NSW_OK;}
 }else if(c->type==10){ // acknowledge one visible ordinary being, no fabricated quest permission
  if(c->value<1||c->value>4)return NSW_INVALID;
  uint32_t id=static_cast<uint32_t>(c->value);
  if(dist(s->x,s->y,nsw_being_x(id,s->world_tick),nsw_being_y(id,s->world_tick))>2)return NSW_TOO_FAR;
  s->being_last_talk=id;s->being_talk_mask|=(1u<<(id-1));
  s->last_talk_tick=s->world_tick+1;rc=NSW_OK;
 }else return NSW_WRONG_STAGE;
 if(rc<10){++s->revision;++s->world_tick;s->last_code=rc;}
 return rc;
}
#ifdef NS_PRODUCT_WASM
static ns_world_state world{};
int32_t nsw_wasm_create(uint32_t a,uint32_t b){return nsw_create(&world,a,b);}
int32_t nsw_wasm_apply(uint32_t r,uint32_t t,int32_t v){ns_world_command cmd={NSW_ABI,r,t,v};return nsw_apply(&world,&cmd);}
#define NSW_GET(field) uint32_t nsw_wasm_##field(void){return world.field;}
NSW_GET(ore) NSW_GET(ingots) NSW_GET(mining_xp) NSW_GET(smithing_xp)
NSW_GET(kit_ward) NSW_GET(kit_echo) NSW_GET(kit_burn) NSW_GET(kit_mark) NSW_GET(kit_root) NSW_GET(kit_tempo) NSW_GET(kit_fatigue)
NSW_GET(boss_pattern) NSW_GET(boss_turn) NSW_GET(weapon_grade)
NSW_GET(being_talk_mask) NSW_GET(research_last_class) NSW_GET(research_last_action) NSW_GET(boss_pressure)
NSW_GET(revision) NSW_GET(x) NSW_GET(y) NSW_GET(quest) NSW_GET(herbs) NSW_GET(work_xp)
NSW_GET(remedies) NSW_GET(health) NSW_GET(focus) NSW_GET(sp) NSW_GET(boss_hp)
NSW_GET(boss_intent) NSW_GET(boss_phase) NSW_GET(defeats) NSW_GET(world_tick) NSW_GET(last_code)
uint32_t nsw_wasm_boss(void){return world.active_boss;}
uint32_t nsw_wasm_boss_threatens(uint32_t x,uint32_t y){return nsw_boss_threatens(&world,x,y);}
uint32_t nsw_wasm_boss_threat_radius(void){return nsw_boss_threat_radius(&world);}

uint32_t nsw_wasm_boss_target_x(void){return world.target_x;}
uint32_t nsw_wasm_boss_target_y(void){return world.target_y;}
uint32_t nsw_wasm_code(void){return world.last_code;}
uint32_t nsw_wasm_being_behavior(uint32_t id){return nsw_being_behavior(&world,id);}
uint32_t nsw_wasm_kit_mode(uint32_t cls){return nsw_kit_mode(cls);}
uint32_t nsw_wasm_kit_cost(uint32_t cls){return nsw_kit_cost(cls);}
uint32_t nsw_wasm_kit_power(uint32_t cls){return nsw_kit_power(cls);}
uint32_t nsw_wasm_kit_aux_cost(uint32_t cls){return nsw_kit_aux_cost(cls);}
uint32_t nsw_wasm_kit_passive_family(uint32_t cls){return nsw_kit_passive_family(cls);}
#endif
}
