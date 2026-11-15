/* R07 renderer-only atmospheric lighting / cast-shadow study.
 * No gameplay authority. World light direction rotates WITH the camera projection
 * so shadows remain attached to the same geographic direction in all 4 views.
 * Not final licensed/author-approved art or physically based rendering.
 */
(function(root){'use strict';
function bounded(v,lo,hi){return Math.max(lo,Math.min(hi,v));}
function shadowVector(projection,x,y,zoom=1){
 const a=projection(x,y),b=projection(x-.65,y+.32);
 const dx=b.x-a.x,dy=b.y-a.y;
 return {dx:bounded(dx,-65*zoom,65*zoom),dy:bounded(dy,-30*zoom,30*zoom)};
}
function cast(ctx,projection,x,y,scale=1,weight=1){
 if(!Number.isFinite(x)||!Number.isFinite(y)||!Number.isFinite(scale)||scale<=0)return;
 const p=projection(x,y),sun=shadowVector(projection,x,y,scale);
 ctx.save();ctx.globalCompositeOperation='multiply';
 ctx.beginPath();ctx.ellipse(p.x+sun.dx*.50,p.y+sun.dy*.50+4*scale,27*scale,9*scale,0,0,Math.PI*2);
 ctx.fillStyle=`rgba(11,17,26,${bounded(.21*weight,0,.56)})`;ctx.fill();
 ctx.restore();
}
function light(ctx,projection,x,y,t=0,radius=90){
 const p=projection(x,y),r=radius;
 const f=1+.04*Math.sin(t/260+x*17+y*7);
 ctx.save();ctx.globalCompositeOperation='screen';
 const g=ctx.createRadialGradient(p.x,p.y-r*.34,0,p.x,p.y-r*.34,r*f);
 g.addColorStop(0,'rgba(238,151,85,0.22)');g.addColorStop(.46,'rgba(232,118,58,0.095)');g.addColorStop(1,'rgba(0,0,0,0)');
 ctx.fillStyle=g;ctx.fillRect(p.x-r,p.y-r*1.34,2*r,2*r);
 ctx.restore();
}
function chimney(ctx,projection,x,y,ms,height=135,offsetX=-19,zoom=1){
 const p=projection(x,y),baseX=p.x+offsetX*zoom,baseY=p.y-height*zoom;
 ctx.save();ctx.globalCompositeOperation='screen';
 for(let i=0;i<5;i++){
  const phase=((ms/3800+i/5)%1+1)%1;
  const drift=phase*27*zoom+Math.sin((ms/650)+i*2.7)*4*zoom;
  const cx=baseX+drift,cy=baseY-phase*51*zoom;
  const r=(3.5+phase*12)*zoom;
  const g=ctx.createRadialGradient(cx,cy,0,cx,cy,r);
  g.addColorStop(0,`rgba(180,184,194,${.19*(1-phase)})`);
  g.addColorStop(1,'rgba(148,159,168,0)');
  ctx.fillStyle=g;ctx.fillRect(cx-r,cy-r,r*2,r*2);
 }
 ctx.restore();
}
function veil(ctx,w,h,ms){
 if(!(w>0&&h>0))return;
 ctx.save();ctx.globalCompositeOperation='screen';
 const shift=Math.sin(ms/8800)*w*.08;
 const g=ctx.createLinearGradient(-w*.6+shift,h*.1,w*.7+shift,h*.95);
 g.addColorStop(0,'rgba(92,125,134,0)');
 g.addColorStop(.42,'rgba(76,115,124,0.035)');
 g.addColorStop(.72,'rgba(104,122,148,0.045)');
 g.addColorStop(1,'rgba(66,90,121,0)');
 ctx.fillStyle=g;ctx.fillRect(0,0,w,h);ctx.restore();
}
const api=Object.freeze({shadowVector,cast,light,chimney,veil});
if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.NSAtmosphereR07=api;
})(typeof globalThis!=='undefined'?globalThis:this);
