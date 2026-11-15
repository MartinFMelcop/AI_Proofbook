/** R06 observational scene effects. All seeds are static art constants and time.
 * No quests, materials, positions, collision, NPC memory or combat results are written.
 * This module has NO direct imports from the core or game world.
 */
(function(root){'use strict';
function ambience(ctx,projection,zoom,ms,width,height){
 const lights=[[14,11,1.3],[17,8,1.7],[9,8,1],[19,10,.8],[11,12,.65]];
 ctx.save();ctx.globalCompositeOperation='screen';
 for(let i=0;i<lights.length;i++){
  const [x,y,energy]=lights[i],p=projection(x,y);
  const flicker=.87+.08*Math.sin(ms/410+i*7)+.05*Math.sin(ms/176+i*12),radius=61*zoom*energy;
  const g=ctx.createRadialGradient(p.x,p.y-16*zoom,0,p.x,p.y-16*zoom,radius);
  g.addColorStop(0,'rgba(255,201,119,'+(.13*flicker)+')');
  g.addColorStop(.4,'rgba(222,116,51,'+(.065*flicker)+')');
  g.addColorStop(1,'rgba(219,97,22,0)');ctx.fillStyle=g;
  ctx.fillRect(p.x-radius,p.y-radius-16*zoom,radius*2,radius*2);
 }
 ctx.restore();
 // Low-opacity drifting pollen, bounded at 24 pixels: readable beings and bosses
 // are not covered by opaque decorative particles.
 ctx.save();
 for(let i=0;i<24;i++){
   const xx=((i*179.1+Math.sin(i*10.3)*47+ms*(.007+(i%4)*.004))%(width+40))-20;
   const yy=(((i*83.9+ms*(.002+(i%3)*.006))%(height+30))+height+30)%(height+30);
   const radius=(.55+(i%4)*.25)*zoom;ctx.beginPath();ctx.arc(xx,yy,radius,0,Math.PI*2);
   ctx.fillStyle=i%5===0?'rgba(255,220,161,.42)':'rgba(225,242,185,.17)';ctx.fill();
 }
 ctx.restore();
}
function footfall(ctx,x,y,zoom,ms,walking){
 if(!walking)return;
 ctx.save();const fade=Math.max(0,.21-.1*Math.abs(Math.sin(ms/120)));
 ctx.beginPath();ctx.ellipse(x,y+5*zoom,14*zoom,4*zoom,0,0,Math.PI*2);
 ctx.fillStyle='rgba(207,178,126,'+fade.toFixed(3)+')';ctx.fill();ctx.restore();
}
const api={ambience,footfall};
if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.NSAmbienceR06=api;
})(typeof globalThis!=='undefined'?globalThis:this);
