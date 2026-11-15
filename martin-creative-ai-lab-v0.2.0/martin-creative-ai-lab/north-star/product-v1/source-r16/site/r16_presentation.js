/* R16 adapter. Reuse R15 rigorously native-gated phase and measured original
 * pivots; the derived WebP shares dimensions/anchors with its R14 source.
 * No new gameplay authority, no synthetic damage or attack timings.
 */
(function(root){'use strict';
 const prev=root.NSPresentationR15;
 const original=n=>typeof n==='string'&&n.startsWith('r16_')?'r14_'+n.slice(4):null;
 const api=Object.freeze({
   observedBoss:prev.observedBoss,
   bossStage:prev.bossStage,
   cue:prev.cue,
   building:(ctx,img,p,id,face,zoom,alpha,ms,n)=>original(n)?prev.building(ctx,img,p,id,face,zoom,alpha,ms,original(n)):false,
   actor:(ctx,img,w,h,ms,moving,n)=>original(n)?prev.actor(ctx,img,w,h,ms,moving,original(n)):false,
   portrait:(ctx,img,p,id,zoom,ms,intent,pattern,n)=>original(n)?prev.portrait(ctx,img,p,id,zoom,ms,intent,pattern,original(n)):false,
   visualOnly:true,approved:false
 });
 root.NSPresentationR16=api;
 if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
