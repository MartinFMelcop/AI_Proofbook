/* North Star PRODUCT V1 spatial consumer, not an authority. Dynamic isometric projection.
 * World/collision/quest/NPC positions/boss outcomes are ALL read from the compiled C++ WASM owner.
 * Camera projection, weather, art, paths-to-propose and UI are observational only.
 */
(function(root){'use strict';
const C=root.NSCamera4;
const COLS=24,ROWS=20,QUESTS=[
 ['A Estrada do Sul','Encontre o jovem guarda e seu cão perto da ponte.',1],
 ['Sete casas e uma ausência','Converse com a líder na praça da vila.',2],
 ['Rastros entre raízes','Investigue o ponto de coleta e obtenha duas ervas.',3],
 ['Ofício e remédio','Leve as ervas à bancada de preparação.',4],
 ['Primeiro encontro','Siga até o Vigia das Ruínas. Confronto técnico proposto, não canônico.',5],
 ['Ecos do pântano','Encontre o Sussurro do Brejo. Confronto técnico proposto, não canônico.',6],
 ['Uma árvore enferma','Investigue a Árvore Guardiã, referência histórica de Rave Masters.',7],
 ['A semente e o caminho','Prólogo técnico concluído. História ainda não canonizada.',0]
];
const OBJECTS={1:'Guarda',2:'Líder da vila',3:'Ervas da floresta',4:'Bancada de remédios',5:'Vigia das Ruínas',6:'Sussurro do Brejo',7:'Árvore Guardiã'};
// Authored-looking four-view CONCEPT billboards; placement is observational and does not
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
];
const NPCS=[
 {id:1,name:'Guarda da ponte',h:'#45616b',hat:'#bac6cb'},
 {id:2,name:'Líder da vila',h:'#7e4b6b',hat:'#f4c990'},
 {id:3,name:'Mercador',h:'#535774',hat:'#ab875b'},
 {id:4,name:'Herbalista',h:'#2d6554',hat:'#c4d6ad'}
];
const BOSS_NAMES=['Vigia das Ruínas','Sussurro do Brejo','Árvore Guardiã'];
const R06_WRAITH=Array.from({length:4},(_,face)=>Array.from({length:4},(_,p)=>'r06_wraith_'+face+'_'+p)).flat();
const R06_BOSS_MOTION=[...Array.from({length:4},(_,face)=>Array.from({length:3},(_,p)=>'r06_boss_guard_'+face+'_motion_'+(p+1))).flat(),...Array.from({length:3},(_,p)=>'r06_boss_wisp_motion_'+(p+1)),...Array.from({length:3},(_,p)=>'r06_boss_tree_motion_'+(p+1))];
const R06_NPC_MOTION=Array.from({length:4},(_,id)=>Array.from({length:4},(_,face)=>Array.from({length:3},(_,p)=>'npc_'+(id+1)+'_'+face+'_motion_'+(p+1))).flat()).flat();
const R04_ASSETS=['r04_cottage','r04_forge','r04_apothecary','r04_stonebridge','r04_lamppost','r04_fountain','r04_blossom','r04_eldertree','r04_shrine','r04_guardian_boss','r04_wisp',...Array.from({length:4},(_,i)=>'r04_ruinguardian_'+i)];
const R10_ART_PREVIEW_NAMES={1:'cottage',2:'forge',3:'apothecary'};
const R11_ART_PREVIEW_NAMES={1:'cottage',2:'forge',3:'apothecary'};
let api=null, raf=0,active=false,canvas=null,ctx=null,corner=0,zoom=1,px=0,py=0,viewW=0,viewH=0,paintLast=0,walkQueue=[],walkLast=0,images={};
let lastPlayerStep=-1,lastWorldPos=null,lastPlayerMove=[12,17],heroFrame=0,npcLastTick=-1,npcChangeMs=0,heroWorldFacing=0;
const byId=id=>document.getElementById(id);
const get=id=>api&&api.engine['nsw_wasm_'+id]();
function preload(){const spriteNames=Array.from({length:16},(_,k)=>'hero_'+Math.floor(k/4)+'_'+(k%4));const materialNames=[0,1,2,3,4,6,7,8,9].flatMap(i=>Array.from({length:5},(_,v)=>'material_'+i+'_'+v));for(const name of [...spriteNames,...materialNames,...Array.from({length:16},(_,k)=>'npc_'+(Math.floor(k/4)+1)+'_'+(k%4)),'hero_0','hero_1','hero_2','hero_3','watchtower','deadpine','runestone','brazier','wagon','well',...R04_ASSETS,...R06_BOSS_MOTION,...R06_NPC_MOTION,...R06_WRAITH,...(root.NSR10ArtPreview===true?Object.values(R10_ART_PREVIEW_NAMES).flatMap(n=>Array.from({length:4},(_,k)=>'r10_'+n+'_'+k)):[]),...((root.NSR11ArtPreview===true||root.NSR12VisualLab===true)?Object.values(R11_ART_PREVIEW_NAMES).flatMap(n=>Array.from({length:4},(_,k)=>'r11_'+n+'_'+k)):[]),...(root.NSFacadeR07Manifest?.state==='AUTHOR_ART_APPROVED'?Object.values(root.NSFacadeR07Manifest.buildings||{}).flatMap(v=>v.faces||[]):[])]){
 const im=new Image();im.src='assets/world/'+name+'.webp';images[name]=im;
}}
function stage(){return Math.min(get('quest'),7);}
function objectPos(id){return {x:api.engine.nsw_object_x(id),y:api.engine.nsw_object_y(id)};}
function projection(x,y){const p=C.project(x,y,corner,COLS,ROWS,0,0,38*zoom,20*zoom);const player=C.project(get('x'),get('y'),corner,COLS,ROWS,0,0,38*zoom,20*zoom);return{x:viewW*.50+p.x-player.x,y:viewH*.55+p.y-player.y};}
function path(ctx,pts){ctx.beginPath();ctx.moveTo(pts[0][0],pts[0][1]);for(let i=1;i<pts.length;i++)ctx.lineTo(pts[i][0],pts[i][1]);ctx.closePath();}
function tileColor(t,x,y){const z=(x*92821+y*71373)%7;
 switch(t){case 1:return ['#404b56','#3c4851','#46525c'][z%3];case 2:return ['#31554c','#395d51','#315046'][z%3];case 3:return '#284f65';case 4:return '#1a272b';case 6:return ['#344e42','#425c4b','#32473d'][z%3];case 7:return '#817b71';case 8:return '#1b302c';case 9:return '#4e4d52';default:return ['#3a5145','#3e5547','#405a49','#354c40'][z%4];}}
function tile(x,y,t,ms){const {x:sx,y:sy}=projection(x,y),hw=38*zoom,hh=20*zoom;
 if(sx+hw<0||sx-hw>viewW||sy+hh<0||sy-hh>viewH)return;
 const q=[[sx,sy-hh],[sx+hw,sy],[sx,sy+hh],[sx-hw,sy]];
 const variant=(x*11+y*17+((x*y)%19))%5;
 const material=images['material_'+t+'_'+variant]||images['material_'+t];
 if(material?.complete&&material.naturalWidth){
  ctx.drawImage(material,sx-hw,sy-hh,hw*2,hh*2);
 }else{
  path(ctx,q);ctx.fillStyle=tileColor(t,x,y);ctx.fill();
 }
 // C++ ABI4 authoritative threat footprint, not re-derived JS combat math.
 if(api.engine.nsw_wasm_boss_threatens?.(x,y)){
  const alpha=.30+.13*Math.sin(ms/180);
  ctx.save();path(ctx,q);ctx.fillStyle=`rgba(237,58,72,${alpha})`;ctx.fill();
  ctx.lineWidth=1.5*zoom;ctx.strokeStyle='#f7b39ba8';ctx.stroke();ctx.restore();
 }
 // Avoid black lattice across every tile: emphasize only actual biome boundaries.
 const north=api.engine.nsw_tile(x,y-1),west=api.engine.nsw_tile(x-1,y);
 if(north!==t||west!==t){
  path(ctx,q);ctx.strokeStyle=t===3?'#4f9ba448':'#17262b35';ctx.lineWidth=.6*zoom;ctx.stroke();
 }
 // Spatially deterministic organic ground detail; no gameplay RNG or extra authority.
 if(t===2||t===6||t===0){
  const seeds=2+((x*9+y*7)%3);ctx.save();ctx.lineCap='round';
  for(let j=0;j<seeds;j++){
   const rx=sx+((((x*37+y*13+j*53)%19)-9)/11)*hw;
   const ry=sy+((((x*19+y*47+j*23)%15)-7)/11)*hh;
   const len=(3+(x+y+j)%4)*zoom;
   ctx.beginPath();ctx.moveTo(rx,ry);ctx.lineTo(rx+len*.4,ry-len);
   ctx.moveTo(rx,ry);ctx.lineTo(rx-len*.36,ry-len*.68);
   ctx.strokeStyle=t===6?'#72946344':'#7097743b';ctx.lineWidth=.85*zoom;ctx.stroke();
  }ctx.restore();
 }

 if(t===3){ctx.beginPath();ctx.moveTo(sx-hw*.35,sy);ctx.quadraticCurveTo(sx,sy+Math.sin(ms/700+x)*hh*.14,sx+hw*.4,sy);ctx.strokeStyle='#78b8c077';ctx.lineWidth=1.1*zoom;ctx.stroke();}
 else if(t===1||t===7||t===9){let k=(x*31+y*19)%11;ctx.beginPath();ctx.moveTo(sx-hw*.43,sy+((k%3)-1)*hh*.14);ctx.lineTo(sx+hw*.07,sy+hh*.24);ctx.moveTo(sx+hw*.21,sy-hh*.31);ctx.lineTo(sx+hw*.52,sy-hh*.02);ctx.strokeStyle='#adb0a043';ctx.stroke();}
 else if(t===2||t===6||t===0){ctx.fillStyle='#a7a56c50';for(let i=0;i<3;i++){const rx=sx+((((x*53+y*17+i*13)%23)-11)/15)*hw,ry=sy+((((x*23+y*31+i*11)%15)-7)/15)*hh;ctx.fillRect(rx,ry,1.2*zoom,1.8*zoom);}}
}
function imageProp(name,x,y,h,opacity=1){let i=images[name];if(!i||!i.complete||!i.naturalWidth)return;
 const a=projection(x,y);const hh=h*zoom,ww=hh*i.naturalWidth/i.naturalHeight;
 ctx.save();ctx.globalAlpha=opacity;ctx.shadowColor='#000a';ctx.shadowBlur=12*zoom;ctx.drawImage(i,a.x-ww/2,a.y-hh*.92,ww,hh);ctx.restore();}
function person(x,y,name,h,hat,t,ms,mood=0){
 const a=projection(x,y), ownerFacing=api.engine.nsw_wasm_being_facing(t);
 const pose=((ownerFacing-corner)%4+4)%4;
 const tick=get('world_tick'), prevX=api.engine.nsw_being_x(t,tick?tick-1:0),prevY=api.engine.nsw_being_y(t,tick?tick-1:0);
 const translated=prevX!==x||prevY!==y;
 const movingCycle=translated&&npcChangeMs>0&&(ms-npcChangeMs)<440;
 const stepFrame=movingCycle?Math.min(3,Math.max(0,Math.floor((ms-npcChangeMs)/108))):0;
 const frameKey='npc_'+t+'_'+pose+(stepFrame?'_motion_'+stepFrame:'');
 const sprite=images[frameKey]||images['npc_'+t+'_'+pose];
 const moving=mood===1||mood===3;
 const sway=Math.sin(ms/(moving?260:830)+t)*(.8+(moving?2.5:0))*zoom;
 const tween=translated&&npcChangeMs>0?Math.min(1,Math.max(0,(ms-npcChangeMs)/230)):1;
 const previous=projection(prevX,prevY),shiftX=(previous.x-a.x)*(1-tween),shiftY=(previous.y-a.y)*(1-tween);

 ctx.save();ctx.translate(a.x+shiftX,a.y+sway+shiftY);
 ctx.beginPath();ctx.ellipse(0,4*zoom,16*zoom,6*zoom,0,0,Math.PI*2);ctx.fillStyle='#081519a8';ctx.fill();
 if(sprite&&sprite.complete&&sprite.naturalWidth){
  const hh=(mood===5?108:104)*zoom,ww=hh*sprite.naturalWidth/sprite.naturalHeight;
  ctx.shadowColor='#11151c';ctx.shadowBlur=4*zoom;
  // Four authored facing poses: deterministic camera-consumer, not gameplay state.
  if(root.NSR12VisualLab===true&&root.NSFinishingR12){root.NSFinishingR12.actor(ctx,sprite,ww,hh,ms,movingCycle,t);}
  else ctx.drawImage(sprite,-ww/2,-hh*.96,ww,hh);
  if(mood===5){ctx.globalCompositeOperation='screen';const g=ctx.createRadialGradient(0,-60*zoom,1,0,-60*zoom,55*zoom);
   g.addColorStop(0,'#f5b37436');g.addColorStop(1,'#00000000');ctx.fillStyle=g;ctx.fillRect(-60*zoom,-120*zoom,120*zoom,120*zoom);}
 }else{
  // Honest fallback for missing asset; screenshot/asset tests flag it as degraded.
  const body=ctx.createLinearGradient(-14*zoom,-47*zoom,14*zoom,0);body.addColorStop(0,h);body.addColorStop(1,'#1b2330');
  path(ctx,[[-9*zoom,-33*zoom],[-16*zoom,1],[15*zoom,1],[9*zoom,-32*zoom]]);ctx.fillStyle=body;ctx.fill();
 }
 ctx.restore();
 if(Math.hypot(a.x-px,a.y-py)<310*zoom){
  const moodNames=['Repouso','Patrulha','Atento','Atividade','Preocupação','Alerta'];
  label(a.x+shiftX,a.y+shiftY-110*zoom,name,'#f5dfb5');
  if(mood!==0)label(a.x+shiftX,a.y+shiftY-121*zoom,moodNames[mood]||'','#c0dbe1');
  // Emotional cues are *read-only* consequences of the C++ being mood.
  const nearWorld=Math.abs(get('x')-x)+Math.abs(get('y')-y)<=3;
  if(nearWorld&&(mood===2||mood===4||mood===5)){
    const cue=mood===2?'?':'!',color=mood===5?'#ff9c85':mood===4?'#ffc87b':'#cae8ff';
    const bx=a.x+shiftX+24*zoom,by=a.y+shiftY-91*zoom+Math.sin(ms/510+t)*2*zoom;
    ctx.save();ctx.beginPath();ctx.arc(bx,by,9*zoom,0,Math.PI*2);ctx.fillStyle='#15232fc9';ctx.fill();
    ctx.lineWidth=1*zoom;ctx.strokeStyle=color;ctx.stroke();ctx.fillStyle=color;
    ctx.font=`bold ${Math.round(12*zoom)}px system-ui`;ctx.textAlign='center';ctx.fillText(cue,bx,by+4*zoom);
    ctx.restore();
  }
 }
}
function label(x,y,s,color='#f7e0b5'){ctx.save();ctx.textAlign='center';ctx.font=`600 ${Math.round(10*zoom)}px system-ui`;ctx.shadowColor='#030b10';ctx.shadowBlur=5*zoom;ctx.fillStyle=color;ctx.fillText(s,x,y);ctx.restore();}
function star(x,y,ms,primary=false){const a=projection(x,y),bob=6*Math.sin(ms/400);ctx.save();ctx.translate(a.x,a.y-44*zoom+bob);ctx.rotate(ms/1750);ctx.strokeStyle=primary?'#ffe5a0':'#e6d089';ctx.lineWidth=2.2*zoom;ctx.shadowColor='#ffc45e';ctx.shadowBlur=12;const s=10*zoom;ctx.beginPath();ctx.moveTo(0,-s);ctx.lineTo(3*zoom,0);ctx.lineTo(0,s);ctx.lineTo(-3*zoom,0);ctx.closePath();ctx.stroke();ctx.restore();}
function lighting(ms){
 ctx.save();ctx.globalCompositeOperation='screen';
 for(const [x,y,name] of PROP_POS){if(name!=='brazier'&&name!=='watchtower'&&name!=='r04_lamppost'&&name!=='r04_forge')continue;
  const p=projection(x,y);const r=90*zoom;
  const g=ctx.createRadialGradient(p.x,p.y-25*zoom,1,p.x,p.y-25*zoom,r);
  g.addColorStop(0,'#ffab5453');g.addColorStop(.42,'#d5812d23');g.addColorStop(1,'#00000000');
  ctx.fillStyle=g;ctx.fillRect(p.x-r,p.y-r,r*2,r*2);
 }
 ctx.restore();
}
function effects(ms){ctx.save();for(let i=0;i<34;i++){
 const x=((i*217+ms*(i%4+1)/96)%(viewW+30))-15,y=((i*173-ms/145)%(viewH+30)+viewH+30)%(viewH+30);
 ctx.beginPath();ctx.fillStyle=i%3===0?'#eebc6170':'#e6d6b23d';ctx.arc(x,y,i%5===0?1.7:1.0,0,Math.PI*2);ctx.fill();}
 const g=ctx.createRadialGradient(viewW*.5,viewH*.47,viewW*.08,viewW*.5,viewH*.5,viewW*.78);g.addColorStop(0,'#02080b00');g.addColorStop(1,'#04070bd0');ctx.fillStyle=g;ctx.fillRect(0,0,viewW,viewH);ctx.restore();}
function boss(ms){let b=get('boss');if(!b)return;const loc=objectPos(b+4);const p=projection(loc.x,loc.y);
 ctx.save();ctx.globalCompositeOperation='screen';const aura=ctx.createRadialGradient(p.x,p.y-50*zoom,2,p.x,p.y-50*zoom,80*zoom);const colors=['#ecb96f','#b860d4','#76be96'];aura.addColorStop(0,colors[b-1]+'8c');aura.addColorStop(1,'#00000000');ctx.fillStyle=aura;ctx.fillRect(p.x-90*zoom,p.y-160*zoom,180*zoom,200*zoom);ctx.restore();
 // Boss concept silhouettes in the SAME real gameplay scene, not promotional art.
 // R04 assets are experimental and face the screen (no fake four-view claims).
 const frame=Math.floor(ms/170)%4;
 // Animated concept deformation from the same R04 sprites. No new authored boss,
 // no rig and no gameplay influence; fallback always preserves original artwork.
 const bossKey=b===1?(frame?'r06_boss_guard_'+corner+'_motion_'+frame:'r04_ruinguardian_'+corner)
  :b===2?('r06_wraith_'+corner+'_'+frame)
  :(frame?'r06_boss_tree_motion_'+frame:'r04_guardian_boss');
 if(root.NSR12VisualLab===true&&root.NSFinishingR12&&images[bossKey]?.complete&&images[bossKey]?.naturalWidth){
  root.NSFinishingR12.boss(ctx,images[bossKey],p,b,ms,zoom,get('boss_intent'),get('boss_pattern'));
 }else imageProp(bossKey,loc.x,loc.y,b===3?230:b===2?208:165);
 label(p.x,p.y-125*zoom,BOSS_NAMES[b-1],'#f4b8b7');
 if(get('boss_intent')===1){const target=projection(get('boss_target_x'),get('boss_target_y'));
  const pulse=(.4+.25*Math.sin(ms/130));ctx.save();ctx.strokeStyle=`rgba(240,68,74,${pulse+.25})`;ctx.lineWidth=2*zoom;const r=api.engine.nsw_wasm_boss_threat_radius();ctx.beginPath();ctx.ellipse(target.x,target.y,36*r*zoom,17*r*zoom,0,0,Math.PI*2);ctx.stroke();ctx.restore();}
}
function draw(ms){if(!active)return;
 const bounds=canvas.getBoundingClientRect(),dpr=Math.min(2,root.devicePixelRatio||1);if(Math.abs(canvas.width-bounds.width*dpr)>3||Math.abs(canvas.height-bounds.height*dpr)>3){canvas.width=Math.max(1,Math.round(bounds.width*dpr));canvas.height=Math.max(1,Math.round(bounds.height*dpr));}
 viewW=bounds.width;viewH=bounds.height;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,viewW,viewH);
 const bg=ctx.createLinearGradient(0,0,0,viewH);bg.addColorStop(0,'#121e2c');bg.addColorStop(1,'#192e2e');ctx.fillStyle=bg;ctx.fillRect(0,0,viewW,viewH);
 const currentTick=get('world_tick');if(currentTick!==npcLastTick){npcLastTick=currentTick;npcChangeMs=ms;}
 const tiles=[];for(let y=0;y<ROWS;y++)for(let x=0;x<COLS;x++){const p=projection(x,y);tiles.push({x,y,sy:p.y,t:api.engine.nsw_tile(x,y)});}
 tiles.sort((a,b)=>a.sy-b.sy || a.x-b.x);
 for(const c of tiles)tile(c.x,c.y,c.t,ms);
 lighting(ms);
 const objs=[];
 // All built architecture is placed at centers reported by C++; no second
 // house/collision map in the browser. Volumes rotate physically with projection.
 for(let sid=1;sid<=3;sid++){
  const x=api.engine.nsw_wasm_structure_x(sid),y=api.engine.nsw_wasm_structure_y(sid);
  const center=projection(x,y);const near=Math.abs(get('x')-x)+Math.abs(get('y')-y)<=2;
  const inFront=center.y>projection(get('x'),get('y')).y;
  const opacity=near&&inFront?.54:1;
  // Four-face *geometry* can be inspected internally, but its flat materials
  // failed the R05 visual gate. Keep the rich existing art in default gameplay.
  // R05 does NOT yet ship author-approved distinct painted facades.
  const conceptNames={1:'r04_cottage',2:'r04_forge',3:'r04_apothecary'};
  const conceptHeights={1:164,2:170,3:155};
  objs.push({y:center.y,draw:()=>{
   root.NSAtmosphereR07?.cast(ctx,projection,x,y,zoom,1.6);
   if(root.NSArchitecturePreviewMode===true){root.NSArchitectureR05?.draw(ctx,projection,sid,x,y,zoom,opacity,ms);}
   else {
    // Default is still the richer R04 painting. Four-view candidate requires
    // provenance, 4 UNIQUE images and explicit author art approval.
    // R10 LAB PREVIEW ONLY: 12 generated candidate paintings, not approved art.
    // Disabled by default; the AUTHOR_ART_APPROVED R07 gate is NOT bypassed.
    // R11 curated candidate has priority ONLY inside private opt-in art preview;
    // it never bypasses R07 AUTHOR_ART_APPROVED gate in normal gameplay.
    const r12Preview=root.NSR12VisualLab===true;const r11Preview=root.NSR11ArtPreview===true||r12Preview;
    const previewName=r11Preview?'r11_'+R11_ART_PREVIEW_NAMES[sid]+'_'+corner:'r10_'+R10_ART_PREVIEW_NAMES[sid]+'_'+corner;
    const previewTexture=(r11Preview||root.NSR10ArtPreview===true)?images[previewName]:null;
    if(previewTexture?.complete && previewTexture.naturalWidth){
      if(r12Preview&&root.NSFinishingR12){
       root.NSFinishingR12.building(ctx,previewTexture,center,sid,corner,zoom,opacity,ms);
      }else imageProp(previewName,x,y,r11Preview?({1:209,2:216,3:206}[sid]):conceptHeights[sid],opacity);
    } else {
      const art=root.NSFacadeR07?.resolve(sid,corner,root.NSFacadeR07Manifest,images);
      imageProp(art?.name||conceptNames[sid],x,y,conceptHeights[sid],opacity);
    }
    if(sid===1||sid===2)root.NSAtmosphereR07?.chimney(ctx,projection,x,y,ms,conceptHeights[sid]*.77,sid===1?-13:-5,zoom);
    root.NSAtmosphereR07?.light(ctx,projection,x,y,ms,sid===2?88*zoom:64*zoom);
   }
  }});
 }
 for(const [x,y,name,h] of PROP_POS){
  if(['r04_cottage','r04_forge','r04_apothecary'].includes(name))continue;
  const currentBoss=get('boss');const bossLoc=currentBoss?objectPos(currentBoss+4):null;
  const closeToBoss=bossLoc && Math.abs(bossLoc.x-x)+Math.abs(bossLoc.y-y)<=3;
  // During combat, decorative copies cannot masquerade as or hide the boss silhouette.
  if(closeToBoss && ['r04_eldertree','r04_blossom','r04_shrine'].includes(name))continue;
  objs.push({y:projection(x,y).y,draw:()=>{
  // Transparent in front of the actor to preserve legibility. Never affects collision/visibility rules.
  const near=Math.abs(get('x')-x)+Math.abs(get('y')-y)<=2;
  const inFront=projection(x,y).y>projection(get('x'),get('y')).y;
  if(['r04_eldertree','r04_blossom','deadpine','watchtower','r04_shrine'].includes(name))root.NSAtmosphereR07?.cast(ctx,projection,x,y,zoom,.95);
  imageProp(name,x,y,h,closeToBoss?.28:(near&&inFront?.48:1));
 }});}
 const quest=stage(),id=QUESTS[quest][2];
 for(const n of NPCS){const x=api.engine.nsw_being_x(n.id,get('world_tick')),y=api.engine.nsw_being_y(n.id,get('world_tick'));
 objs.push({y:projection(x,y).y,draw:()=>person(x,y,n.name,n.h,n.hat,n.id,ms,api.engine.nsw_wasm_being_behavior(n.id))});}
 if(get('boss')){const pos=objectPos(get('boss')+4);objs.push({y:projection(pos.x,pos.y).y,draw:()=>boss(ms)});}
 objs.push({y:projection(get('x'),get('y')).y,draw:()=>{const a=projection(get('x'),get('y'));
 ctx.save();ctx.beginPath();ctx.ellipse(a.x,a.y+7*zoom,17*zoom,8*zoom,0,0,2*Math.PI);ctx.fillStyle='#000a';ctx.fill();ctx.strokeStyle='#e9c788';ctx.stroke();ctx.restore();
 const walking=lastPlayerStep>=0 && (ms-lastPlayerStep)<480;
 root.NSAmbienceR06?.footfall(ctx,a.x,a.y,zoom,ms,walking);
 const frame=walking?Math.floor(Math.max(0,ms-lastPlayerStep)/110)%4:0;
 const avatarView=((heroWorldFacing-corner)%4+4)%4;
 const im=images['hero_'+avatarView+'_'+frame]||images['hero_'+avatarView];
 if(im&&im.complete&&im.naturalWidth){
   let h=122*zoom,w=h*im.naturalWidth/im.naturalHeight;
   let motionX=0,motionY=0;
   // Visual smoothing only: actor world state stays on accepted integer tile. No client authority.
   if(walking&&lastWorldPos){const p=projection(lastWorldPos[0],lastWorldPos[1]);
     const t=Math.min(1,(ms-lastPlayerStep)/190);motionX=(p.x-a.x)*(1-t);motionY=(p.y-a.y)*(1-t);}
   if(root.NSR12VisualLab===true&&root.NSFinishingR12){
    ctx.save();ctx.translate(a.x+motionX,a.y+motionY+2*zoom);
    root.NSFinishingR12.actor(ctx,im,w,h,ms,walking,0);ctx.restore();
   }else ctx.drawImage(im,a.x-w/2+motionX,a.y-h*.94+motionY,w,h);
 }else person(get('x'),get('y'),'', '#7d3a4e','#b58b76',0,ms);}});
 objs.sort((a,b)=>a.y-b.y);for(const it of objs)it.draw();
 // R06 weather and warm-light pass observes projection/time only. It cannot
 // amend any authoritative C++ state or create artificial NPC observations.
 root.NSAmbienceR06?.ambience(ctx,projection,zoom,ms,viewW,viewH);
 if(id){const target=objectPos(id);star(target.x,target.y,ms,true);}
 root.NSAtmosphereR07?.veil(ctx,viewW,viewH,ms);
 effects(ms);
 if(root.NSR10ArtPreview===true||root.NSR11ArtPreview===true||root.NSR12VisualLab===true){
  ctx.save();ctx.fillStyle='#080d17db';ctx.fillRect(8,8,360,28);
  ctx.font='bold 13px system-ui';ctx.fillStyle='#f6dcad';
  ctx.textAlign='left';ctx.fillText(root.NSR12VisualLab===true?'R12 VISUAL LAB · NOT APPROVED':root.NSR11ArtPreview===true?'R11 ART CANDIDATE · NOT APPROVED':'R10 ART CANDIDATE · NOT APPROVED',17,27);
  ctx.restore();
 }
 px=viewW*.5;py=viewH*.55;
 raf=root.requestAnimationFrame(draw);
}
function refresh(){if(!active)return;
 const q=stage(),obj=QUESTS[q],bossId=get('boss');
 byId('world-location').textContent=q<2?'VAU DO SUL':q<4?'A VILA DAS SETE CASAS':q===7?'O DESPERTAR DA ESTRELA':'AS FRONTEIRAS DA FLORESTA';
 byId('world-quest-title').textContent=obj[0];byId('world-quest-text').textContent=obj[1];
 byId('world-hp').textContent=`${get('health')}/30`;byId('world-sp').textContent=`${get('sp')}/8`;
 byId('world-herbs').textContent=`Ervas ${get('herbs')}/2 · Herbalismo ${get('work_xp')} XP`;
 const idA=api.profile?.primary||1,idB=api.profile?.secondary||0;
 const klass=api.profile?.classNames||{};
 byId('world-kit-primary').textContent=`Primária ${klass[idA]||'R'+String(idA).padStart(2,'0')} · ataque ${api.engine.nsw_wasm_kit_cost(idA)}SP / suporte ${api.engine.nsw_wasm_kit_aux_cost(idA)}SP / passiva L${api.engine.nsw_wasm_kit_passive_family(idA)}`;
 byId('world-kit-secondary').textContent=idB?`Secundária ${klass[idB]||'R'+String(idB).padStart(2,'0')} · ataque ${api.engine.nsw_wasm_kit_cost(idB)}SP / suporte ${api.engine.nsw_wasm_kit_aux_cost(idB)}SP / passiva L${api.engine.nsw_wasm_kit_passive_family(idB)}`:'Monoclasse · nenhum segundo kit';
 byId('world-profession').textContent=`Minério ${get('ore')}/3 · Lingotes ${get('ingots')}/3 · Ferramenta ${get('weapon_grade')}/2 · Min ${get('mining_xp')} / For ${get('smithing_xp')} XP`;
 const nps=NPCS.map(n=>`${n.name}: ${['repouso','patrulha','atento','trabalho','preocupado','alerta'][api.engine.nsw_wasm_being_behavior(n.id)]}`).join(' | ');
 byId('world-npc-state').textContent=nps;
 byId('world-remedies').textContent=`Curas ${get('remedies')} · ${get('defeats')}/3 confrontos`;
 byId('world-camera').textContent=`VISTA ${corner+1} / 4 · ${corner*90}°`;
 byId('world-coordinates').textContent=`X ${get('x')} · Y ${get('y')} · REV ${get('revision')}`;
 let combat=byId('world-combat');combat.hidden=!bossId;
 if(bossId){byId('world-boss-name').textContent=`${BOSS_NAMES[bossId-1]} · CONFRONTO DE LABORATÓRIO`;
  byId('world-boss-hp').textContent=`${get('boss_hp')}/${[15,20,27][bossId-1]}`;
  byId('world-boss-bar').style.width=`${get('boss_hp')/[15,20,27][bossId-1]*100}%`;
  const patterns={1:'corte anunciado',2:'onda pantanosa: raio 2, desgaste de SP',3:'raízes expandidas: raio 2',4:'finta de ruínas com impacto forte',5:'maré corrosiva: drenagem ampliada de SP',6:'raízes que restringem movimento temporariamente'};
  const pattern=patterns[get('boss_pattern')]||'padrão não identificado';
  const threat=api.engine.nsw_wasm_boss_threatens?.(get('x'),get('y'))?'POSIÇÃO EM RISCO: defenda-se ou saia da zona':'FORA DA ZONA DE RISCO';
  byId('world-boss-tell').textContent=get('boss_intent')===1?`⚠ ${pattern} · ${threat}`:'Janela de recuperação: ataque ou prepare-se';
 }
 const oi=obj[2], dist=oi?Math.abs(get('x')-api.engine.nsw_object_x(oi))+Math.abs(get('y')-api.engine.nsw_object_y(oi)):0;
 byId('world-interact-hint').textContent=oi?(dist<=2?`E · Interagir: ${OBJECTS[oi]}`:`Aproxime-se do objetivo · ${dist} células`):'Capítulo experimental concluído';
 if(api.lastMessage)byId('world-notice').textContent=api.lastMessage;
 for(const el of byId('world-interact').querySelectorAll('button[data-world-command]')){
  const t=Number(el.dataset.worldCommand),v=Number(el.dataset.worldValue||0);
  const combatOnly=[3,4,5,6,7,8,11].includes(t);
  el.disabled=(combatOnly&&!bossId)||(t===2&&!oi)||((t===8||t===11)&&v===1&&!idB)||(t===9&&(bossId||q<2))||(t===10&&bossId);
 }
}
function userAction(type,value=0){if(!active||!api)return;
 const old=type===1?[get('x'),get('y')]:null;
 const code=api.action(type,value);
 if(type===1&&code>=1&&code<=6){lastWorldPos=old;lastPlayerStep=root.performance?.now?.()||0;heroWorldFacing=value;}
 refresh();return code;
}
function closestAndInteract(){let id=QUESTS[stage()][2];if(id)userAction(2,id);}
function rotate(delta){corner=C.turn(corner,delta);refresh();}
function key(e){if(!active)return;
 if(e.key==='Escape'){e.preventDefault();api.openMenu();return;}
 if(['r','R'].includes(e.key)){e.preventDefault();rotate(e.shiftKey?-1:1);return;}
 if(['e','E'].includes(e.key)){e.preventDefault();closestAndInteract();return;}
 if(['+','='].includes(e.key)){zoom=Math.min(1.45,zoom+.09);refresh();return;}
 if(['-','_'].includes(e.key)){zoom=Math.max(.6,zoom-.09);refresh();return;}
 const map={w:0,ArrowUp:0,d:1,ArrowRight:1,s:2,ArrowDown:2,a:3,ArrowLeft:3};
 let wanted=map[e.key.length===1?e.key.toLowerCase():e.key];if(wanted!==undefined){e.preventDefault();walkQueue=[];userAction(1,(wanted-corner+4)%4);return;}
 if(e.key==='1')userAction(3);if(e.key==='2')userAction(4);if(e.key==='3')userAction(5);if(e.key==='4')userAction(8,0);if(e.key==='5')userAction(6);
 if(e.key==='6')userAction(8,1);if(e.key==='0')userAction(11,0);if(e.key==='q')userAction(11,1);if(e.key==='7')userAction(9,1);if(e.key==='8')userAction(9,2);if(e.key==='9')userAction(9,3);if(e.key.toLowerCase()==='t')userAction(10,1);
}
function click(e){if(!active||get('boss'))return;const rect=canvas.getBoundingClientRect(),clickX=e.clientX-rect.left,clickY=e.clientY-rect.top;
 let best=null,d=Infinity;for(let y=1;y<19;y++)for(let x=1;x<23;x++){
 const pt=projection(x,y),dd=Math.pow((pt.x-clickX)/(38*zoom),2)+Math.pow((pt.y-clickY)/(20*zoom),2);
 if(dd<d){best={x,y};d=dd;}}
 if(!best)return;
 const start=[get('x'),get('y')],keyOf=(x,y)=>x+','+y,dirs=[[0,-1],[1,0],[0,1],[-1,0]],seen=new Map([[keyOf(...start),null]]),queue=[start];
 for(let j=0;j<queue.length;j++){
 const [x,y]=queue[j];if(x===best.x&&y===best.y)break;
 for(let k=0;k<4;k++){const [dx,dy]=dirs[k],xx=x+dx,yy=y+dy;if(xx<=0||xx>=23||yy<=0||yy>=19)continue;
 const key=keyOf(xx,yy);if(seen.has(key)||[3,4,8,9].includes(api.engine.nsw_tile(xx,yy)))continue;seen.set(key,{prev:keyOf(x,y),dir:k});queue.push([xx,yy]);}}
 const steps=[];let cur=keyOf(best.x,best.y);if(!seen.has(cur))return;
 while(seen.get(cur)!==null){const rec=seen.get(cur);steps.push(rec.dir);cur=rec.prev;if(steps.length>500)break;}
 walkQueue=steps.reverse();walkLast=0;
}
function stepQueue(ms){if(!active)return;if(walkQueue.length&&ms-walkLast>155){walkLast=ms;const d=walkQueue.shift();userAction(1,d);}root.requestAnimationFrame(stepQueue);}
function mount(owner){if(active)unmount();api=owner;lastPlayerStep=-1;lastWorldPos=null;heroWorldFacing=0;npcLastTick=-1;npcChangeMs=0;canvas=byId('world-canvas');if(!canvas)return;ctx=canvas.getContext('2d');corner=0;zoom=1.12;walkQueue=[];preload();active=true;canvas.addEventListener('pointerdown',click);root.addEventListener('keydown',key);refresh();raf=root.requestAnimationFrame(draw);root.requestAnimationFrame(stepQueue);}
function unmount(){active=false;if(raf)root.cancelAnimationFrame(raf);root.removeEventListener('keydown',key);if(canvas)canvas.removeEventListener('pointerdown',click);canvas=null;ctx=null;api=null;walkQueue=[];}
const API={mount,unmount,refresh,rotate,userAction,get active(){return active}};
if(typeof module!=='undefined'&&module.exports)module.exports=API;else root.NSWorld=API;
})(typeof globalThis!=='undefined'?globalThis:this);
