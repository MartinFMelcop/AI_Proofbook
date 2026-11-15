from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
base=(R/'core/world_r03.cpp').read_text()
hdr=(R/'core/world_r03.h').read_text().replace('#ifndef NS_WORLD_R03_H','#ifndef NS_WORLD_R04_H').replace('#define NS_WORLD_R03_H','#define NS_WORLD_R04_H').replace('#define NSW_ABI 3u','#define NSW_ABI 4u')
hdr=hdr.replace('NSW_API uint32_t nsw_being_behavior(const ns_world_state* s,uint32_t id);', '''NSW_API uint32_t nsw_being_behavior(const ns_world_state* s,uint32_t id);
// Observation-only query shared by telegraph render and opponent damage; no state mutation.
NSW_API uint32_t nsw_boss_threatens(const ns_world_state* s,uint32_t x,uint32_t y);
NSW_API uint32_t nsw_boss_threat_radius(const ns_world_state* s);''')
hdr=hdr.replace('NSW_API uint32_t nsw_wasm_boss_pressure(void);','''NSW_API uint32_t nsw_wasm_boss_pressure(void);
NSW_API uint32_t nsw_wasm_boss_threatens(uint32_t x,uint32_t y);
NSW_API uint32_t nsw_wasm_boss_threat_radius(void);''')
(R/'core/world_r04.h').write_text(hdr)
cpp=base.replace('#include "world_r03.h"','#include "world_r04.h"')
needle=' inline uint32_t dist(uint32_t x,uint32_t y,uint32_t a,uint32_t b){return (x>a?x-a:a-x)+(y>b?y-b:b-y);}'
assert needle in cpp
cpp=cpp.replace(needle,needle+'''
 // A pure authoritative threat predicate; visual consumer may only query it.
 inline uint32_t threatRadius(const ns_world_state& s){
  if(s.active_boss==0||s.boss_intent!=1)return 0;
  return (s.boss_pattern==2||s.boss_pattern==3||s.boss_pattern==5||s.boss_pattern==6)?2u:1u;
 }
 inline bool threatens(const ns_world_state& s,uint32_t x,uint32_t y){
  return s.active_boss>0&&s.boss_intent==1&&x<NSW_COLUMNS&&y<NSW_ROWS&&
   dist(x,y,s.target_x,s.target_y)<=threatRadius(s);
 }''')
needle='   const uint32_t radius=(s.boss_pattern==2||s.boss_pattern==3||s.boss_pattern==5||s.boss_pattern==6)?2u:1u;'
assert needle in cpp
cpp=cpp.replace(needle,'')
needle='   if(dist(s.x,s.y,s.target_x,s.target_y)<=radius){'
assert needle in cpp
cpp=cpp.replace(needle,'   if(threatens(s,s.x,s.y)){')
needle='uint32_t nsw_abi(void){return NSW_ABI;}'
assert needle in cpp
cpp=cpp.replace(needle,needle+'''
uint32_t nsw_boss_threatens(const ns_world_state* s,uint32_t x,uint32_t y){return s&&check(*s)&&threatens(*s,x,y)?1u:0u;}
uint32_t nsw_boss_threat_radius(const ns_world_state* s){return s&&check(*s)?threatRadius(*s):0u;}
''')
needle='uint32_t nsw_wasm_boss(void){return world.active_boss;}'
assert needle in cpp
cpp=cpp.replace(needle,needle+'''
uint32_t nsw_wasm_boss_threatens(uint32_t x,uint32_t y){return nsw_boss_threatens(&world,x,y);}
uint32_t nsw_wasm_boss_threat_radius(void){return nsw_boss_threat_radius(&world);}
''')
(R/'core/world_r04.cpp').write_text(cpp)
site=(R/'site/world.js').read_text()
old=re.search(r'const PROP_POS=\[.*?\];',site,re.S)
assert old
new="""// Authored-looking four-view CONCEPT billboards; placement is observational and does not
// create collisions or forge any house count / canon world in the core.
const PROP_POS=[
 [10,8,'r04_cottage',164],[17,8,'r04_forge',170],[20,10,'r04_apothecary',155],
 [3,3,'r04_eldertree',190],[6,4,'r04_blossom',145],[8,4,'r04_eldertree',153],
 [12,2,'r04_eldertree',194],[16,4,'r04_blossom',157],[20,6,'r04_blossom',140],
 [9,12,'r04_fountain',106],[12,15,'r04_stonebridge',116],[14,11,'r04_lamppost',114],
 [8,9,'r04_lamppost',106],[17,12,'r04_lamppost',105],[5,9,'r04_blossom',142],
 [19,3,'r04_shrine',150],[2,10,'deadpine',122],[15,4,'deadpine',105],
 [15,11,'brazier',60],[18,10,'well',71],[5,15,'r04_lamppost',111],
 [7,7,'r04_blossom',113],[10,3,'r04_eldertree',148]
];"""
site=site[:old.start()]+new+site[old.end():]
needle="const BOSS_NAMES=['Vigia das Ruínas','Sussurro do Brejo','Árvore Guardiã'];"
assert needle in site
site=site.replace(needle,needle+"\nconst R04_ASSETS=['r04_cottage','r04_forge','r04_apothecary','r04_stonebridge','r04_lamppost','r04_fountain','r04_blossom','r04_eldertree','r04_shrine','r04_wisp'];")
needle="'hero_0','hero_1','hero_2','hero_3','watchtower','deadpine','runestone','brazier','wagon','well'"
assert needle in site
site=site.replace(needle,needle+",...R04_ASSETS")
# Add runtime hazard mask using same native predicate as actual damage.
needle=' // Avoid black lattice across every tile: emphasize only actual biome boundaries.'
assert needle in site
site=site.replace(needle,''' // C++ ABI4 authoritative threat footprint, not re-derived JS combat math.
 if(api.engine.nsw_wasm_boss_threatens?.(x,y)){
  const alpha=.30+.13*Math.sin(ms/180);
  ctx.save();path(ctx,q);ctx.fillStyle=`rgba(237,58,72,${alpha})`;ctx.fill();
  ctx.lineWidth=1.5*zoom;ctx.strokeStyle='#f7b39ba8';ctx.stroke();ctx.restore();
 }
'''+needle)
site=site.replace("if(name!=='brazier'&&name!=='watchtower')continue;","if(name!=='brazier'&&name!=='watchtower'&&name!=='r04_lamppost'&&name!=='r04_forge')continue;")
old="if(b===1)imageProp('runestone',loc.x,loc.y,110);\n else if(b===2)imageProp('brazier',loc.x,loc.y,100);\n else imageProp('deadpine',loc.x,loc.y,188);"
assert old in site
new="""// Boss concept silhouettes in the SAME real gameplay scene, not promotional art.
 // R04 assets are experimental and face the screen (no fake four-view claims).
 if(b===1)imageProp('r04_shrine',loc.x,loc.y,144);
 else if(b===2)imageProp('r04_wisp',loc.x,loc.y,170);
 else imageProp('r04_eldertree',loc.x,loc.y,207);"""
site=site.replace(old,new)
old="const r=(b===2 || (b===3&&get('boss_phase')===1))?2:1;ctx.beginPath();ctx.ellipse(target.x,target.y,36*r*zoom,17*r*zoom,0,0,Math.PI*2);ctx.stroke();ctx.restore();"
assert old in site
site=site.replace(old,"const r=api.engine.nsw_wasm_boss_threat_radius();ctx.beginPath();ctx.ellipse(target.x,target.y,36*r*zoom,17*r*zoom,0,0,Math.PI*2);ctx.stroke();ctx.restore();")
site=site.replace("const pattern=patterns[get('boss_pattern')]||'padrão não identificado';","const pattern=patterns[get('boss_pattern')]||'padrão não identificado';\n  const threat=api.engine.nsw_wasm_boss_threatens?.(get('x'),get('y'))?'POSIÇÃO EM RISCO: defenda-se ou saia da zona':'FORA DA ZONA DE RISCO';")
site=site.replace("`⚠ ${pattern}: alvo (${get('boss_target_x')}, ${get('boss_target_y')}) — defenda-se ou desvie`","`⚠ ${pattern} · ${threat}`")
(R/'site/world.js').write_text(site)
app=(R/'site/app.js').read_text().replace('mmai_ns_product_v1_r03_save','mmai_ns_product_v1_r04_save').replace('version===4','version===5').replace('version:4','version:5').replace('engine.nsw_abi()!==3','engine.nsw_abi()!==4')
(R/'site/app.js').write_text(app)
html=(R/'site/index.html').read_text().replace('R03: KITS DUPLOS LAB / NPCS ILUSTRADOS','R04: VILA ILUSTRADA / ZONAS DE PERIGO C++ / KITS LAB')
(R/'site/index.html').write_text(html)
# New build target appended, preserving all R01-R03 historical builds. Last site/product.wasm is R04.
sh=(R/'tools/build.sh').read_text()
sh+='''\n# R04 authoritative world. R03 remains archived in an explicit old WASM binary.
clang++ --target=wasm32 -std=c++20 -O2 -fno-exceptions -fno-rtti -nostdlib -DNS_PRODUCT_WASM \\
 -Wl,--no-entry -Wl,--export-all -Wl,--strip-debug -Wl,--initial-memory=131072 core/world_r03.cpp -o artifacts/world_r03.wasm
${CXX:-g++} -std=c++20 -Wall -Wextra -Werror -O2 -fPIC -shared -DNS_BUILD_DLL core/world_r04.cpp -o artifacts/libns_world_r04.so
clang++ --target=wasm32 -std=c++20 -O2 -fno-exceptions -fno-rtti -nostdlib -DNS_PRODUCT_WASM \\
 -Wl,--no-entry -Wl,--export-all -Wl,--strip-debug -Wl,--initial-memory=131072 core/world_r04.cpp -o site/product.wasm
'''
(R/'tools/build.sh').write_text(sh)
# adapted Skia render for R04
script=(R/'tests/render_world_skia_r03.mjs').read_text().replace('nsw_abi(),3','nsw_abi(),4').replace('R03_SKIA_VIEW_','R04_SKIA_VIEW_').replace('650','900')
(R/'tests/render_world_skia_r04.mjs').write_text(script)
print('patched R04 core, client, and build without modifying R03 sources')
