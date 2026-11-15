#include "product.h"
namespace {
    /* Stable fixture scalars: *not* North Star balance. */
    constexpr uint32_t max_rev = 100000u;
    constexpr int32_t health_by_boss[3] = {9, 12, 15};
    bool valid(const ns_product_state& s) {
        return s.abi==NS_PRODUCT_ABI && s.initialized==1 && s.primary>=1 && s.primary<=21 &&
               s.secondary<=21 && s.primary!=s.secondary && s.chapter_step<=7 &&
               s.defeats<=3 && s.active_boss<=3 && s.health<=20 && s.potions<=3 &&
               s.focus<=4 && s.revision<=max_rev && s.boss_hp<=15 &&
               ((s.active_boss==0 && s.boss_hp==0) || (s.active_boss==s.defeats+1 && s.boss_hp>0)) &&
               (s.chapter_step<4 || s.chapter_step==4+s.defeats);
    }
}
extern "C" {
uint32_t nsp_abi(void){return NS_PRODUCT_ABI;}
void nsp_reset(ns_product_state* s){if(s)*s={NS_PRODUCT_ABI,0,0,0,0,0,0,0,20,2,0,0,0};}
int32_t nsp_create(ns_product_state* s,uint32_t a,uint32_t b){
    if(!s)return NSP_INVALID;
    nsp_reset(s);
    if(a<1||a>21||b>21||a==b)return NSP_INVALID;
    s->initialized=1;s->primary=a;s->secondary=b;s->last_code=NSP_OK;
    return NSP_OK;
}
int32_t nsp_boss_hp(const ns_product_state* s){return s && s->active_boss?static_cast<int32_t>(s->boss_hp):0;}
int32_t nsp_apply(ns_product_state* s,const ns_product_command* c){
    if(!s||!c||!valid(*s))return NSP_NO_SESSION;
    if(c->abi!=NS_PRODUCT_ABI||c->type<1||c->type>7)return NSP_INVALID;
    if(c->expected_revision!=s->revision)return NSP_STALE;
    if(s->revision>=max_rev)return NSP_INVALID;
    int rc=NSP_WRONG_GATE;
    if(c->type==1){
        if(s->active_boss==0 && s->chapter_step<4 && c->value>=1 && c->value<=4 &&
           static_cast<uint32_t>(c->value)==s->chapter_step+1){
           ++s->chapter_step;rc=NSP_OK;
        }
    } else if(c->type==2){
        if(s->active_boss==0 && s->chapter_step>=4 && s->chapter_step<7 && s->health>0){
           s->active_boss=s->defeats+1;s->boss_hp=health_by_boss[s->defeats];rc=NSP_BOSS_STARTED;
        }
    } else if(c->type==3 || c->type==4 || c->type==5 || c->type==6 || c->type==7){
        if(s->active_boss && (s->health || c->type==7)){
            if(c->type==7){s->active_boss=0;s->boss_hp=0;s->focus=0;if(s->health==0)s->health=10;rc=NSP_OK;}
            else if(c->type==6 && s->potions==0){rc=NSP_NO_RESOURCE;}
            else {
                if(c->type==3){uint32_t damage=3+(s->focus>0);s->boss_hp=s->boss_hp>damage?s->boss_hp-damage:0;s->focus=0;}
                if(c->type==5 && s->focus<4)++s->focus;
                if(c->type==6){--s->potions;s->health=(s->health+5>20)?20:s->health+5;}
                if(s->boss_hp==0){s->active_boss=0;++s->defeats;
                    s->chapter_step=4+s->defeats;rc=(s->defeats==3)?NSP_CHAPTER_COMPLETED:NSP_BOSS_COMPLETED;}
                else {uint32_t damage=(c->type==4)?1:2;
                    s->health=s->health>damage?s->health-damage:0;
                    rc=s->health?NSP_OK:NSP_DEFEAT;
                }
            }
        }
    }
    if(rc<10){++s->revision;s->last_code=rc;}
    return rc;
}
#ifdef NS_PRODUCT_WASM
static ns_product_state running{};
int32_t nsp_wasm_create(uint32_t a,uint32_t b){return nsp_create(&running,a,b);}
int32_t nsp_wasm_apply(uint32_t rev,uint32_t t,int32_t v){const ns_product_command cmd={NS_PRODUCT_ABI,rev,t,v};return nsp_apply(&running,&cmd);}
uint32_t nsp_wasm_revision(void){return running.revision;}
uint32_t nsp_wasm_step(void){return running.chapter_step;}
uint32_t nsp_wasm_primary(void){return running.primary;}
uint32_t nsp_wasm_secondary(void){return running.secondary;}
uint32_t nsp_wasm_boss(void){return running.active_boss;}
uint32_t nsp_wasm_defeats(void){return running.defeats;}
uint32_t nsp_wasm_health(void){return running.health;}
uint32_t nsp_wasm_potions(void){return running.potions;}
uint32_t nsp_wasm_focus(void){return running.focus;}
uint32_t nsp_wasm_code(void){return running.last_code;}
int32_t nsp_wasm_boss_hp(void){return nsp_boss_hp(&running);}
#endif
}
