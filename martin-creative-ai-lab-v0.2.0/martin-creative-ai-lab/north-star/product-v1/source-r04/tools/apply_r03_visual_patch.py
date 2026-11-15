"""Additive visual-source patch to R03 copy of existing site/world.js.
Preserves all C++ quest authority. This is not an artist-approved world renderer.
"""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'site/world.js'
s=p.read_text()
assert s.count('function person(')==1
s=s.replace("for(const name of [...spriteNames,...materialNames,'hero_0'", "for(const name of [...spriteNames,...materialNames,...Array.from({length:16},(_,k)=>'npc_'+(Math.floor(k/4)+1)+'_'+(k%4)),'hero_0'")
# tile strokes: no dense grid on identical materials, preserve water edge cue when biome changes.
s=s.replace("path(ctx,q);ctx.strokeStyle=t===1?'#7a828083':'#192d2c8a';ctx.lineWidth=.7*zoom;ctx.stroke();", """// Avoid black lattice across every tile: emphasize only actual biome boundaries.
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
""")
old=s[s.index('function person('):s.index('function label(')]
new="""function person(x,y,name,h,hat,t,ms,mood=0){
 const a=projection(x,y),sprite=images['npc_'+t+'_'+corner];
 const moving=mood===1||mood===3;
 const sway=Math.sin(ms/(moving?260:830)+t)*(.8+(moving?2.5:0))*zoom;
 ctx.save();ctx.translate(a.x,a.y+sway);
 ctx.beginPath();ctx.ellipse(0,4*zoom,16*zoom,6*zoom,0,0,Math.PI*2);ctx.fillStyle='#081519a8';ctx.fill();
 if(sprite&&sprite.complete&&sprite.naturalWidth){
  const hh=(mood===5?108:104)*zoom,ww=hh*sprite.naturalWidth/sprite.naturalHeight;
  ctx.shadowColor='#11151c';ctx.shadowBlur=4*zoom;
  // Four authored facing poses: deterministic camera-consumer, not gameplay state.
  ctx.drawImage(sprite,-ww/2,-hh*.96,ww,hh);
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
  label(a.x,a.y-110*zoom,name,'#f5dfb5');
  if(mood!==0)label(a.x,a.y-121*zoom,moodNames[mood]||'','#c0dbe1');
 }
}
"""
s=s.replace(old,new)
# Atmospheric point lights and water visible on Skia; additive-only rendering code.
needle="function effects(ms){ctx.save();"
assert needle in s
s=s.replace(needle,"""function lighting(ms){
 ctx.save();ctx.globalCompositeOperation='screen';
 for(const [x,y,name] of PROP_POS){if(name!=='brazier'&&name!=='watchtower')continue;
  const p=projection(x,y);const r=90*zoom;
  const g=ctx.createRadialGradient(p.x,p.y-25*zoom,1,p.x,p.y-25*zoom,r);
  g.addColorStop(0,'#ffab5453');g.addColorStop(.42,'#d5812d23');g.addColorStop(1,'#00000000');
  ctx.fillStyle=g;ctx.fillRect(p.x-r,p.y-r,r*2,r*2);
 }
 ctx.restore();
}
function effects(ms){ctx.save();""")
s=s.replace("for(const c of tiles)tile(c.x,c.y,c.t,ms);","for(const c of tiles)tile(c.x,c.y,c.t,ms);\n lighting(ms);")
# existing boss_pattern HUD extends new pattern 5/6.
s=s.replace("4:'finta de ruínas com impacto forte'","4:'finta de ruínas com impacto forte',5:'maré corrosiva: drenagem ampliada de SP',6:'raízes que restringem movimento temporariamente'")
s=s.replace("(b===2 || (b===3&&get('boss_phase')===1))?2:1", "(b===2 || (b===3&&get('boss_phase')===1))?2:1")
s=s.replace("if(['r','R'].includes(e.key))", "if(['r','R'].includes(e.key))")
s=s.replace("if(e.key==='6')userAction(8,1);", "if(e.key==='6')userAction(8,1);if(e.key==='0')userAction(11,0);if(e.key==='q')userAction(11,1);")
p.write_text(s)
print('R03 renderer patched',len(s),'chars')
