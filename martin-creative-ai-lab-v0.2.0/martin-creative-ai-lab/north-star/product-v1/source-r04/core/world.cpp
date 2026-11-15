#include "world.h"
namespace {
 constexpr uint32_t MAX_REV=500000u;
 constexpr uint32_t bossMax[3]={15u,20u,27u};
 constexpr uint32_t ax[8]={0,13,13,6,16,20,4,12};
 constexpr uint32_t ay[8]={0,16,10,11,10,5,5,3};
 inline uint32_t dist(uint32_t x,uint32_t y,uint32_t a,uint32_t b){return (x>a?x-a:a-x)+(y>b?y-b:b-y);}
 bool check(const ns_world_state& s){
  return s.abi==NSW_ABI&&s.initialized==1&&s.primary>=1&&s.primary<=21&&
  s.secondary<=21&&s.primary!=s.secondary&&s.revision<=MAX_REV&&
  s.x>0&&s.x<NSW_COLUMNS-1&&s.y>0&&s.y<NSW_ROWS-1&&s.quest<=7&&
  s.herbs<=2&&s.work_xp<=100&&s.remedies<=3&&s.health<=30&&s.focus<=3&&s.sp<=8&&
  s.defeats<=3&&s.active_boss<=3&&s.boss_phase<=1&&s.boss_intent<=2&&
  ((s.active_boss==0&&s.boss_hp==0&&s.boss_intent==0)||
   (s.active_boss==s.defeats+1 &&s.boss_hp>0&&s.boss_hp<=bossMax[s.defeats]&&s.boss_intent>0))&&
  s.quest>=s.defeats+4*(s.defeats>0);
 }
 // Called only on accepted combat intentions; an explicit targeted warning always precedes a strike.
 int opponent(ns_world_state& s,bool defending){
  if(s.boss_hp==0){
   s.active_boss=0;s.boss_intent=0;s.boss_phase=0;s.focus=0;
   ++s.defeats;s.quest=4+s.defeats;s.remedies=s.remedies<3?s.remedies+1:3;
   s.health=(s.health+8>30)?30:s.health+8;
   s.sp=8;
   return s.defeats==3?NSW_FINALE:NSW_BOSS_WIN;
  }
  s.boss_phase=s.boss_hp<=(bossMax[s.active_boss-1]/2)?1:0;
  if(s.boss_intent==1){
   const uint32_t radius=(s.active_boss==2 || (s.active_boss==3&&s.boss_phase==1))?2u:1u;
   uint32_t damage=3u+s.active_boss+s.boss_phase*2u;
   if(dist(s.x,s.y,s.target_x,s.target_y)<=radius){
    if(defending)damage=(damage+3)/4;
    s.health=s.health>damage?s.health-damage:0;
    // B02 laboratory behavior: marsh shock drains focus capacity (SP) on contact.
    if(s.active_boss==2&&!defending && s.sp>0)--s.sp;
   }
   s.boss_intent=2;
  }else{
   s.boss_intent=1;s.target_x=s.x;s.target_y=s.y;
  }
  return s.health?NSW_OK:NSW_DEFEATED;
 }
}
extern "C" {
uint32_t nsw_abi(void){return NSW_ABI;}
uint32_t nsw_object_x(uint32_t id){return id<8?ax[id]:0;}
uint32_t nsw_object_y(uint32_t id){return id<8?ay[id]:0;}
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
void nsw_reset(ns_world_state* s){if(s)*s={NSW_ABI,0,0,0,0,12,17,0,0,0,2,30,0,8,0,0,0,0,0,0,0,0,0};}
int32_t nsw_create(ns_world_state* s,uint32_t a,uint32_t b){
 if(!s)return NSW_INVALID;
 nsw_reset(s);
 if(a<1||a>21||b>21||b==a)return NSW_INVALID;
 s->initialized=1;s->primary=a;s->secondary=b;s->last_code=NSW_OK;
 return NSW_OK;
}
int32_t nsw_apply(ns_world_state* s,const ns_world_command* c){
 if(!s||!c||!check(*s))return NSW_NO_SESSION;
 if(c->abi!=NSW_ABI||c->type<1||c->type>8)return NSW_INVALID;
 if(c->expected_revision!=s->revision)return NSW_STALE;
 if(s->active_boss && s->health==0 && c->type!=7)return NSW_CANNOT_ACT;
 if(s->revision>=MAX_REV)return NSW_INVALID;
 int rc=NSW_WRONG_STAGE;
 if(c->type==1){
  if(c->value<0||c->value>3)return NSW_INVALID;
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
   rc=NSW_BOSS_START;
  }
 }else if(s->active_boss){
  if(c->type==7){s->active_boss=0;s->boss_hp=0;s->boss_intent=0;s->boss_phase=0;s->health=30;s->sp=8;s->focus=0;rc=NSW_OK;}
  else if(s->health==0)return NSW_CANNOT_ACT;
  else if(c->type==6){
   if(s->remedies==0)return NSW_NO_RESOURCE;
   --s->remedies;s->health=(s->health+9>30)?30:s->health+9;rc=opponent(*s,false);
  }else if(c->type==3||c->type==8){
   if(dist(s->x,s->y,ax[s->active_boss+4],ay[s->active_boss+4])>3)return NSW_TOO_FAR;
   if(c->type==8){if(s->sp<3)return NSW_NO_RESOURCE;s->sp-=3;}
   uint32_t damage=c->type==3?3+static_cast<uint32_t>(s->focus>0):5+s->focus;
   s->boss_hp=s->boss_hp>damage?s->boss_hp-damage:0;s->focus=0;
   rc=opponent(*s,false);
  }else if(c->type==4){rc=opponent(*s,true);}
  else if(c->type==5){if(s->focus<3)++s->focus;rc=opponent(*s,false);}
  else if(c->type==1){rc=NSW_OK;} // movement already handled above
 }else return NSW_WRONG_STAGE;
 if(rc<10){++s->revision;++s->world_tick;s->last_code=rc;}
 return rc;
}
#ifdef NS_PRODUCT_WASM
static ns_world_state world{};
int32_t nsw_wasm_create(uint32_t a,uint32_t b){return nsw_create(&world,a,b);}
int32_t nsw_wasm_apply(uint32_t r,uint32_t t,int32_t v){ns_world_command cmd={NSW_ABI,r,t,v};return nsw_apply(&world,&cmd);}
#define NSW_GET(field) uint32_t nsw_wasm_##field(void){return world.field;}
NSW_GET(revision) NSW_GET(x) NSW_GET(y) NSW_GET(quest) NSW_GET(herbs) NSW_GET(work_xp)
NSW_GET(remedies) NSW_GET(health) NSW_GET(focus) NSW_GET(sp) NSW_GET(boss_hp)
NSW_GET(boss_intent) NSW_GET(boss_phase) NSW_GET(defeats) NSW_GET(world_tick) NSW_GET(last_code)
uint32_t nsw_wasm_boss(void){return world.active_boss;}
uint32_t nsw_wasm_boss_target_x(void){return world.target_x;}
uint32_t nsw_wasm_boss_target_y(void){return world.target_y;}
uint32_t nsw_wasm_code(void){return world.last_code;}
#endif
}
