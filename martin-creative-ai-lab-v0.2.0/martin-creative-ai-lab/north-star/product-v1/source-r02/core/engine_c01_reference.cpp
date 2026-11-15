#include "northstar_core.h"

namespace {
constexpr char board[NS_H][NS_W+1] = {
    "##########",
    "#........#",
    "#..##....#",
    "#........#",
    "#....N...#",
    "#..##....#",
    "#........#",
    "##########"
};
constexpr int NPC_X=5, NPC_Y=4;
inline bool walkable(int x,int y) {return x>=0 && x<NS_W && y>=0 && y<NS_H && board[y][x]=='.';}
inline bool state_ok(const ns_state &s) {
    return s.abi_version==NS_ABI_VERSION && walkable(s.x,s.y) &&
        s.moves<=NS_MAX_ACTIONS && s.npc_met<=1 &&
        s.revision==s.moves+s.npc_met;
}
}
extern "C" {
uint32_t ns_abi_version(void) { return NS_ABI_VERSION; }
uint32_t ns_ruleset_version(void) { return NS_RULESET_VERSION; }
void ns_initial(ns_state *dst) {if(dst) *dst={NS_ABI_VERSION,1,1,0,0,0};}
int32_t ns_tile(int32_t x,int32_t y) {
    if(x<0 || y<0 || x>=NS_W || y>=NS_H)return 0;
    return board[y][x];
}
int32_t ns_apply(const ns_state *before,const ns_intent *intent,ns_state *after,ns_receipt *receipt) {
    if(!before||!intent||!after||!receipt)return -1;
    *after=*before;
    *receipt={0,NS_INVALID_STATE,before->revision,before->revision};
    if(!state_ok(*before)||intent->abi_version!=NS_ABI_VERSION)return -2;
    if(intent->expected_revision!=before->revision){receipt->code=NS_STALE;return 0;}
    if(intent->kind!=1 && intent->kind!=2){receipt->code=NS_BAD_ACTION;return 0;}
    const bool cardinal=(intent->dx==0 && (intent->dy==1 || intent->dy==-1)) ||
                        (intent->dy==0 && (intent->dx==1 || intent->dx==-1));
    if(!cardinal){receipt->code=NS_BAD_ACTION;return 0;}
    const int tx=before->x+intent->dx, ty=before->y+intent->dy;
    if(tx<0||ty<0||tx>=NS_W||ty>=NS_H){receipt->code=NS_OUT_OF_RANGE;return 0;}
    if(intent->kind==1){
        if(!walkable(tx,ty)){receipt->code=NS_BLOCKED;return 0;}
        if(before->revision>=NS_MAX_ACTIONS){receipt->code=NS_LIMIT_REACHED;return 0;}
        after->x=tx;after->y=ty;after->moves++;after->revision++;
        receipt->accepted=1;receipt->code=NS_MOVED;
    } else {
        if(tx!=NPC_X||ty!=NPC_Y){receipt->code=NS_OUT_OF_RANGE;return 0;}
        if(before->npc_met){receipt->code=NS_ALREADY;return 0;}
        if(before->revision>=NS_MAX_ACTIONS){receipt->code=NS_LIMIT_REACHED;return 0;}
        after->npc_met=1;after->revision++;
        receipt->accepted=1;receipt->code=NS_NPC_CONTACT;
    }
    receipt->revision_after=after->revision;
    return 0;
}
#ifdef NS_WASM_CLIENT
static ns_state wasm_state={NS_ABI_VERSION,1,1,0,0,0};
static ns_receipt wasm_last={0,0,0,0};
void ns_wasm_reset(void) {ns_initial(&wasm_state);wasm_last={0,0,0,0};}
int32_t ns_wasm_apply(uint32_t revision,int32_t kind,int32_t dx,int32_t dy) {
    const ns_intent intent={NS_ABI_VERSION,revision,kind,dx,dy};
    ns_state after{};
    const int32_t rc=ns_apply(&wasm_state,&intent,&after,&wasm_last);
    if(rc==0)wasm_state=after;
    return rc;
}
uint32_t ns_wasm_revision(void){return wasm_state.revision;}
int32_t ns_wasm_x(void){return wasm_state.x;}
int32_t ns_wasm_y(void){return wasm_state.y;}
uint32_t ns_wasm_moves(void){return wasm_state.moves;}
uint32_t ns_wasm_npc_met(void){return wasm_state.npc_met;}
int32_t ns_wasm_last_code(void){return wasm_last.code;}
#endif
}
