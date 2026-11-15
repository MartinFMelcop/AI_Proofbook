/* Actual C17 consumer of C++20 world_r02 .so. No C++ runtime dependencies in header. */
#include "world_r04.h"
#include <stdint.h>
#include <stdio.h>
int main(void){
 ns_world_state s;
 if(nsw_abi()!=4u)return 1;
 if(nsw_create(&s,6u,17u)!=NSW_OK)return 2;
 if(s.abi!=4u||s.primary!=6u||s.secondary!=17u)return 3;
 ns_world_command move={4u,0u,1u,0};
 if(nsw_apply(&s,&move)!=NSW_OK||s.y!=16u||s.revision!=1u)return 4;
 if(nsw_kit_mode(21)!=21u||nsw_kit_cost(6)==0u||nsw_kit_aux_cost(17)==0u||nsw_kit_passive_family(21)==0u)return 5;
 if(nsw_being_behavior(&s,1)>5u)return 6;
 if(nsw_boss_threat_radius(&s)!=0u||nsw_boss_threatens(&s,12,16)!=0u)return 8;
 move.expected_revision=0u;
 if(nsw_apply(&s,&move)!=NSW_STALE||s.revision!=1u)return 7;
 printf("{\"suite\":\"c17_to_cpp20_r04\",\"PASS\":true,\"abi\":%u,\"revision\":%u}\n",s.abi,s.revision);
 return 0;
}
