#ifndef NS_WORLD_V1_H
#define NS_WORLD_V1_H
#include <stdint.h>
#if defined(_WIN32)
 #if defined(NS_BUILD_DLL)
  #define NSW_API __declspec(dllexport)
 #else
  #define NSW_API __declspec(dllimport)
 #endif
#else
 #define NSW_API __attribute__((visibility("default")))
#endif
#ifdef __cplusplus
extern "C" {
#endif
#define NSW_ABI 1u
#define NSW_COLUMNS 24u
#define NSW_ROWS 20u
// A research fixture. No data/class/boss imported into North Star canon.
typedef struct ns_world_state {
 uint32_t abi,revision,initialized,primary,secondary;
 uint32_t x,y,quest,herbs,work_xp,remedies,health,focus,sp;
 uint32_t active_boss,boss_hp,boss_intent,target_x,target_y,boss_phase,defeats;
 uint32_t world_tick,last_code;
} ns_world_state;
typedef struct ns_world_command {uint32_t abi,expected_revision,type;int32_t value;} ns_world_command;
enum ns_world_code {NSW_OK=1,NSW_QUEST=2,NSW_BOSS_START=3,NSW_BOSS_WIN=4,NSW_FINALE=5,NSW_DEFEATED=6,
 NSW_STALE=10,NSW_INVALID=11,NSW_BLOCKED=12,NSW_TOO_FAR=13,NSW_WRONG_STAGE=14,
 NSW_NO_RESOURCE=15,NSW_NO_SESSION=16,NSW_CANNOT_ACT=17};
// Commands: 1 move: N/E/S/W [0,1,2,3]; 2 interact: [1 guard,2 leader,3 herbs,4 bench,5..7 boss locations];
// 3 basic attack; 4 guard; 5 observe; 6 potion; 7 retreat; 8 skill.
NSW_API uint32_t nsw_abi(void);
NSW_API void nsw_reset(ns_world_state* s);
NSW_API int32_t nsw_create(ns_world_state* s,uint32_t primary,uint32_t secondary);
NSW_API int32_t nsw_apply(ns_world_state* s,const ns_world_command* c);
NSW_API uint32_t nsw_tile(uint32_t x,uint32_t y);
NSW_API uint32_t nsw_being_x(uint32_t id,uint32_t tick);
NSW_API uint32_t nsw_being_y(uint32_t id,uint32_t tick);
NSW_API uint32_t nsw_object_x(uint32_t id);
NSW_API uint32_t nsw_object_y(uint32_t id);
#ifdef NS_PRODUCT_WASM
NSW_API int32_t nsw_wasm_create(uint32_t primary,uint32_t secondary);
NSW_API int32_t nsw_wasm_apply(uint32_t rev,uint32_t type,int32_t value);
NSW_API uint32_t nsw_wasm_revision(void);
NSW_API uint32_t nsw_wasm_x(void);
NSW_API uint32_t nsw_wasm_y(void);
NSW_API uint32_t nsw_wasm_quest(void);
NSW_API uint32_t nsw_wasm_herbs(void);
NSW_API uint32_t nsw_wasm_work_xp(void);
NSW_API uint32_t nsw_wasm_remedies(void);
NSW_API uint32_t nsw_wasm_health(void);
NSW_API uint32_t nsw_wasm_focus(void);
NSW_API uint32_t nsw_wasm_sp(void);
NSW_API uint32_t nsw_wasm_boss(void);
NSW_API uint32_t nsw_wasm_boss_hp(void);
NSW_API uint32_t nsw_wasm_boss_intent(void);
NSW_API uint32_t nsw_wasm_boss_target_x(void);
NSW_API uint32_t nsw_wasm_boss_target_y(void);
NSW_API uint32_t nsw_wasm_boss_phase(void);
NSW_API uint32_t nsw_wasm_defeats(void);
NSW_API uint32_t nsw_wasm_world_tick(void);
NSW_API uint32_t nsw_wasm_code(void);
#endif
#ifdef __cplusplus
}
#endif
#endif
