/* R12 visual finishing; pure/read-only Canvas consumer of the C++20 ABI5 world.
 * Nothing here owns movement, collision, damage, AI or quest state.
 * Enabled ONLY with NSR12VisualLab true. Never an AUTHOR_ART_APPROVED gate.
 */
(function(root){'use strict';
const FACE={1:'cottage',2:'forge',3:'apothecary'};
// Target apparent painted-height, in CSS px at zoom=1; not a physical collision size.
const VISIBLE={1:190,2:201,3:196};
const BASE_SHADOW={1:[75,18],2:[83,20],3:[74,19]};
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
function measured(sid,view){const name=FACE[sid]+'_'+view;return root.NSR12AssetAnchors?.[name]||null;}
function circleLight(ctx,x,y,r,color,alpha){
 ctx.save();ctx.globalCompositeOperation='screen';const g=ctx.createRadialGradient(x,y,1,x,y,r);
 g.addColorStop(0,color.replace('ALPHA',String(alpha)));g.addColorStop(.5,color.replace('ALPHA',String(alpha*.35)));
 g.addColorStop(1,color.replace('ALPHA','0'));ctx.fillStyle=g;ctx.fillRect(x-r,y-r,2*r,2*r);ctx.restore();
}
function shadow(ctx,x,y,rx,ry,alpha=0.42){
 ctx.save();const g=ctx.createRadialGradient(x,y,1,x,y,rx);
 g.addColorStop(0,`rgba(2,7,12,${alpha})`);g.addColorStop(.65,`rgba(2,7,12,${alpha*.40})`);g.addColorStop(1,'rgba(2,7,12,0)');
 ctx.translate(x,y);ctx.scale(1,ry/rx);ctx.fillStyle=g;ctx.beginPath();ctx.arc(0,0,rx,0,Math.PI*2);ctx.fill();ctx.restore();
}
function building(ctx,img,pos,sid,view,zoom,opacity,ms){
 const m=measured(sid,view);if(!m||!img?.complete||!img.naturalWidth)return false;
 // Draw using measured silhouette, NOT transparent 640-square margins; one common
 // painted foot anchor per building and orientation. No invented polygon/room/collider.
 const scale=(VISIBLE[sid]*zoom)/m.silhouette_h;
 const left=pos.x-m.anchor_x*scale,top=pos.y-m.anchor_y*scale;
 const [rx,ry]=BASE_SHADOW[sid];shadow(ctx,pos.x,pos.y+2*zoom,rx*zoom,ry*zoom,.53*opacity);
 if(sid===2){const flicker=.8+.2*Math.sin(ms/281);circleLight(ctx,pos.x+8*zoom,pos.y-13*zoom,92*zoom,'rgba(245,138,51,ALPHA)',.105*flicker);}
 else if(sid===3)circleLight(ctx,pos.x+6*zoom,pos.y-13*zoom,72*zoom,'rgba(173,106,198,ALPHA)',.065);
 else circleLight(ctx,pos.x+2*zoom,pos.y-13*zoom,75*zoom,'rgba(252,168,82,ALPHA)',.08);
 ctx.save();ctx.globalAlpha=clamp(opacity,0.25,1);ctx.shadowColor='#030a12aa';ctx.shadowBlur=7*zoom;
 ctx.drawImage(img,left,top,img.naturalWidth*scale,img.naturalHeight*scale);
 ctx.restore();
 return {ground_x:pos.x,ground_y:pos.y,visible_height:VISIBLE[sid]*zoom,scale,silhouette_w:m.silhouette_w*scale,face:m,source:'R11_PAINTED_NOT_APPROVED'};
}
function actor(ctx,img,w,h,ms,moving,kind=0){
 if(!img?.complete||!img.naturalWidth)return false;
 // A bounded gait of existing authored poses, not a skeletal rig. The feet remain
 // glued to the accepted C++ world cell; visual time never submits an action.
 const cadence=kind===0?205:kind===1?250:300;
 const phase=ms/cadence+kind*1.37;
 const step=moving?Math.sin(phase*Math.PI*2):0;
 const rise=moving?Math.max(0,step)*1.8:Math.sin(phase)*.65;
 const lean=moving?Math.sin(phase)*.024:Math.sin(phase)*.009;
 const sx=1+(moving?.018:0)*Math.sin(phase*2),sy=1-(moving?.024:0)*Math.sin(phase*2);
 ctx.save();ctx.translate(0,-rise);ctx.rotate(lean);ctx.scale(sx,sy);
 ctx.drawImage(img,-w/2,-h*.96,w,h);ctx.restore();return true;
}
function boss(ctx,img,pos,b,ms,zoom,intent,pattern){
 if(!img?.complete||!img.naturalWidth)return false;
 const s=ms/1000,bob=b===1?Math.sin(s*3.8)*1.9:b===2?Math.sin(s*2.2)*6.2:Math.sin(s*1.4)*1.4;
 const tilt=b===1?Math.sin(s*3.8)*.028:b===2?Math.sin(s*1.9)*.047:Math.sin(s*1.2)*.011;
 const h=(b===1?165:b===2?208:230)*zoom,w=h*img.naturalWidth/img.naturalHeight;
 const tension=intent===1?0.7+0.3*Math.sin(ms/125):0.4;
 shadow(ctx,pos.x,pos.y+3*zoom,(b===3?65:49)*zoom,(b===3?19:13)*zoom,.44*(1+(b===2?bob/32:0)));
 ctx.save();ctx.translate(pos.x,pos.y-bob*zoom);
 ctx.rotate(tilt);ctx.shadowColor=b===1?'#f8a75f77':b===2?'#cf6ee699':'#80e3b066';ctx.shadowBlur=(intent===1?17:8)*zoom;
 if(b===2){ctx.globalAlpha=.92+.05*Math.sin(s*2.4);}
 ctx.drawImage(img,-w/2,-h*.92,w,h);ctx.restore();
 if(intent===1){
  // Distinct legible anticipation types, but the footprint is exclusively
  // nsw_wasm_boss_threatens in tile(), not these decorative world-space FX.
  if(b===1){circleLight(ctx,pos.x,pos.y-70*zoom,52*zoom,'rgba(248,162,67,ALPHA)',.14*tension);}
  if(b===2){circleLight(ctx,pos.x,pos.y-88*zoom,91*zoom,'rgba(173,99,237,ALPHA)',.18*tension);}
  if(b===3){circleLight(ctx,pos.x,pos.y-57*zoom,104*zoom,'rgba(93,200,116,ALPHA)',.13*tension);}
 }
 return {boss:b,owner_intent:intent,owner_pattern:pattern,synthetic_visual_phase:s,gameplay_mutation:false};
}
const api={building,actor,boss,measured,clamp,VISIBLE};
root.NSFinishingR12=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
