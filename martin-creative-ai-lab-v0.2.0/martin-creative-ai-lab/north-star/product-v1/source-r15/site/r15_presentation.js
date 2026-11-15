/* R15 optical presentation. Reads painted-alpha anchors and C++ boss intent; never submits gameplay commands.
 * A strike-frame is shown only after C++ has adjudicated intent==2. No synthetic hit timing.
 * Original image bytes are NOT edited; all adjustments are observational Canvas transforms.
 */
(function(root){'use strict';
const palette={1:'#efc27f',2:'#bcb5ff',3:'#b4dfad'};
function finite(n){return Number.isFinite(n);}
function sample(name){return root.NSR15Anchors?.[name]||null;}
function bossStage(intent,elapsedMs){
 if(intent===1)return elapsedMs<160?0:1; // pending telegraph, never draw impact here
 if(intent===2)return elapsedMs<240?2:3; // C++ already resolved strike, then recovery
 return 0;
}
function observedBoss(owner,elapsedMs){
 if(!owner||![1,2,3].includes(owner.boss)||![1,2].includes(owner.intent)||!finite(elapsedMs))return null;
 const frame=bossStage(owner.intent,Math.max(0,elapsedMs));
 return Object.freeze({frame,orientation:owner.face,owner_intent:owner.intent,owner_turn:owner.turn,
   owner_phase:owner.phase,owner_pattern:owner.pattern,visual_only:true});
}
function drawAnchored(ctx,img,x,y,h,name,alpha=1){
 const m=sample(name);if(!m||!img?.complete||!img.naturalWidth||!(h>0))return false;
 const scale=h/m.silhouette_h,w=img.naturalWidth*scale,hh=img.naturalHeight*scale;
 ctx.save();ctx.globalAlpha=Math.max(.25,Math.min(1,alpha));
 ctx.shadowColor='rgba(2,8,14,.65)';ctx.shadowBlur=5;
 ctx.drawImage(img,x-m.anchor_x*scale,y-m.anchor_y*scale,w,hh);ctx.restore();
 return {x,y,scale,foot_x:m.anchor_x,foot_y:m.anchor_y,source:name};
}
function building(ctx,img,pos,sid,face,zoom,opacity,ms,name){
 const h=({1:191,2:201,3:195})[sid]*zoom;
 if(!h)return false;
 const m=sample(name);if(!m)return false;
 ctx.save();ctx.beginPath();ctx.ellipse(pos.x,pos.y+2*zoom,75*zoom,18*zoom,0,0,Math.PI*2);
 ctx.fillStyle='rgba(2,9,13,.43)';ctx.fill();ctx.restore();
 return drawAnchored(ctx,img,pos.x,pos.y,h,name,opacity);
}
function actor(ctx,img,w,h,ms,moving,name){
 const m=sample(name);if(!m||!img?.complete||!img.naturalWidth)return false;
 const time=ms/1000,hop=moving?Math.sin(time*12)*.7:0;
 return drawAnchored(ctx,img,0,-hop,h*(m.silhouette_h/m.height),name);
}
function portrait(ctx,img,p,b,zoom,ms,intent,pattern,name){
 if(!palette[b])return false;
 ctx.save();ctx.translate(0,-(b===2?Math.sin(ms/480)*2.5:Math.sin(ms/660)*.6)*zoom);
 const result=drawAnchored(ctx,img,p.x,p.y,({1:210,2:254,3:277})[b]*zoom,name);
 ctx.restore();return result;
}
function cue(ctx,p,b,zoom,intent,ms,threatAtPlayer){
 if(!palette[b]||![1,2].includes(intent))return null;
 const label=intent===1?(threatAtPlayer?'ATENÇÃO · ÁREA AMEAÇADA':'ANTECIPAÇÃO · EVITE A ÁREA'):'RECUPERAÇÃO · GOLPE JÁ RESOLVIDO';
 ctx.save();ctx.font=`600 ${Math.round(10*zoom)}px system-ui`;ctx.textAlign='center';
 const w=270*zoom,y=p.y+33*zoom;
 ctx.fillStyle='rgba(6,13,23,.84)';ctx.fillRect(p.x-w/2,y-14*zoom,w,23*zoom);
 ctx.fillStyle=palette[b];ctx.fillText(label,p.x,y+1*zoom);
 ctx.restore();return label;
}
const api={sample,bossStage,observedBoss,drawAnchored,building,actor,portrait,cue,visual_only:true};
root.NSPresentationR15=Object.freeze(api);
if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
