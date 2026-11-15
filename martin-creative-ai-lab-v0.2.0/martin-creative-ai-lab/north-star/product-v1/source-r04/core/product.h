#ifndef NS_PRODUCT_PREPRODUCTION_H
#define NS_PRODUCT_PREPRODUCTION_H
#include <stdint.h>
#if defined(_WIN32)
# if defined(NS_BUILD_DLL)
#  define NS_API __declspec(dllexport)
# else
#  define NS_API __declspec(dllimport)
# endif
#else
# define NS_API __attribute__((visibility("default")))
#endif
#ifdef __cplusplus
extern "C" {
#endif
#define NS_PRODUCT_ABI 1u
/* Source-based, NON-CANONICAL game-loop laboratory; NEVER a substitute for the
 * 21 class rules, author-accepted bosses, or online authority. */
typedef struct ns_product_state {
    uint32_t abi, revision, initialized, primary, secondary;
    uint32_t chapter_step, active_boss, defeats, health, potions, focus, boss_hp;
    uint32_t last_code;
} ns_product_state;
typedef struct ns_product_command {
    uint32_t abi, expected_revision, type;
    int32_t value;
} ns_product_command;
enum ns_product_code {
    NSP_OK = 1, NSP_BOSS_STARTED = 2, NSP_BOSS_COMPLETED = 3, NSP_CHAPTER_COMPLETED = 4,
    NSP_STALE=10, NSP_INVALID=11, NSP_WRONG_GATE=12, NSP_NO_RESOURCE=13, NSP_DEFEAT=14,
    NSP_NO_SESSION=15
};
/* type: 1=story gate (value=1..4); 2=start next boss; 3=basic strike;
 * 4=guard; 5=study; 6=use potion; 7=withdraw. No class skills here. */
NS_API uint32_t nsp_abi(void);
NS_API void nsp_reset(ns_product_state* s);
NS_API int32_t nsp_create(ns_product_state* s,uint32_t primary,uint32_t secondary);
NS_API int32_t nsp_apply(ns_product_state* s, const ns_product_command* cmd);
NS_API int32_t nsp_boss_hp(const ns_product_state* s);
#ifdef NS_PRODUCT_WASM
NS_API int32_t nsp_wasm_create(uint32_t primary,uint32_t secondary);
NS_API int32_t nsp_wasm_apply(uint32_t revision,uint32_t type,int32_t value);
NS_API uint32_t nsp_wasm_revision(void);
NS_API uint32_t nsp_wasm_step(void);
NS_API uint32_t nsp_wasm_primary(void);
NS_API uint32_t nsp_wasm_secondary(void);
NS_API uint32_t nsp_wasm_boss(void);
NS_API uint32_t nsp_wasm_defeats(void);
NS_API uint32_t nsp_wasm_health(void);
NS_API uint32_t nsp_wasm_potions(void);
NS_API uint32_t nsp_wasm_focus(void);
NS_API uint32_t nsp_wasm_code(void);
NS_API int32_t nsp_wasm_boss_hp(void);
#endif
#ifdef __cplusplus
}
#endif
#endif
