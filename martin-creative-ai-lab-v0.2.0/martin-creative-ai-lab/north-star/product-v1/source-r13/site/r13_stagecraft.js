/* R13 dark-fantasy stagecraft. Pure graphics, never a second authority.
 * Only active in opt-in NSR13ArtLab; no hitboxes, timers, outcomes or NPC AI.
 * Every active boss, intent and pattern is passed from C++20 ABI5.
 */
(function(root){'use strict';
const PI=Math.PI,TAU=PI*2;
const COLORS={
  1:{edge:'#e7a76a',core:'#ffd99d',shade:'rgba(52,18,12,0.40)'},
  2:{edge:'#ae9aee',core:'#d7ddff',shade:'rgba(33,14,63,0.50)'},
  3:{edge:'#82b59c',core:'#d7dfa0',shade:'rgba(14,45,33,0.45)'}
};
const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
function ellipse(ctx,x,y,rx,ry,start=0,end=TAU){ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,start,end);}
function rgbGradient(ctx,x,y,r,c1,c2){const g=ctx.createRadialGradient(x,y,1,x,y,r);g.addColorStop(0,c1);g.addColorStop(1,c2);return g;}
function before(ctx,p,b,zoom,ms,intent,pattern){
  if(!COLORS[b])return false;
  const pal=COLORS[b],s=ms/1000,tension=intent===1?1:0.45;
  ctx.save();
  // Painted-looking dark stage anchored under the *actual* C++ boss tile.
  ctx.fillStyle=rgbGradient(ctx,p.x,p.y,83*zoom,pal.shade,'rgba(0,0,0,0)');
  ctx.fillRect(p.x-90*zoom,p.y-76*zoom,180*zoom,152*zoom);
  ctx.lineWidth=(.8+.55*tension)*zoom;
  for(let k=0;k<3;k++){
    const rx=(37+12*k)*zoom,ry=(14+4.5*k)*zoom;
    const alpha=(.22+.16*tension)*(1-k*.20);
    ctx.strokeStyle=pal.edge;ctx.globalAlpha=alpha;
    ellipse(ctx,p.x,p.y+5*zoom,rx,ry,(s*.17+k*.21)%TAU,TAU+.1);ctx.stroke();
  }
  ctx.globalAlpha=.7;
  if(b===1){
    // The ruin sentinel: iron, forge sparks, broken ward compass.
    for(let k=0;k<8;k++){
      const a=k*TAU/8+s*.035,r=43*zoom;
      const x=p.x+Math.cos(a)*r,y=p.y+Math.sin(a)*r*.38+4*zoom;
      ctx.strokeStyle=k%2?pal.edge:pal.core;ctx.lineWidth=1.25*zoom;
      ctx.beginPath();ctx.moveTo(x,y-4*zoom);ctx.lineTo(x+3*zoom,y);ctx.lineTo(x,y+4*zoom);ctx.stroke();
    }
  }else if(b===2){
    // The mire whisper: low spectral whirl, intentionally not a damage radius.
    for(let k=0;k<5;k++){
      const a=s*.38+k*TAU/5;
      ctx.beginPath();ctx.moveTo(p.x+Math.cos(a)*12*zoom,p.y+Math.sin(a)*6*zoom);
      ctx.bezierCurveTo(p.x+Math.cos(a+.7)*25*zoom,p.y-23*zoom,p.x+Math.cos(a+1.7)*41*zoom,p.y+Math.sin(a+1.7)*17*zoom,p.x+Math.cos(a+2.2)*56*zoom,p.y+10*zoom);
      ctx.strokeStyle=k%2?'#9985db':'#c3cbff';ctx.lineWidth=(.7+k*.17)*zoom;ctx.stroke();
    }
  }else{
    // Guardian tree: differentiated paired root geometry rooted at the tile.
    for(let k=0;k<6;k++){
      const v=k-2.5,ex=p.x+v*18*zoom;
      ctx.beginPath();ctx.moveTo(p.x,p.y+2*zoom);
      ctx.quadraticCurveTo(p.x+v*5*zoom,p.y+(8+Math.abs(v)*4)*zoom,ex,p.y+11*zoom);
      ctx.strokeStyle=k%2?'#8a7950':'#508975';ctx.lineWidth=(3-Math.abs(v)*.35)*zoom;ctx.stroke();
    }
  }
  ctx.restore();
  return {kind:b,owner_intent:intent,owner_pattern:pattern,visual_only:true};
}
function after(ctx,p,b,zoom,ms,intent,pattern){
  if(!COLORS[b])return false;
  const pal=COLORS[b],s=ms/1000;
  ctx.save();ctx.globalCompositeOperation='screen';
  // Distinct ambient language per encounter; emission is visual time ONLY.
  const num=b===1?15:b===2?13:11;
  for(let k=0;k<num;k++){
    const phase=(k*.61803398875+s*(b===1?.21:b===2?.11:.07))%1;
    const ang=k*2.39996,rx=(13+Math.sqrt(k+1)*11)*zoom;
    const xx=p.x+Math.cos(ang+phase*.4)*rx;
    const yy=p.y-(24+phase*(b===1?88:b===2?115:75))*zoom+Math.sin(ang)*11*zoom;
    const radius=clamp((b===2?2.5:1.6)+(k%3)*.55,1,4)*zoom;
    ctx.globalAlpha=(b===2?.26:.16)+(1-phase)*(intent===1?.50:.22);
    ctx.fillStyle=k%3===0?pal.core:pal.edge;
    ellipse(ctx,xx,yy,radius,b===2?radius*1.9:radius*.75);ctx.fill();
  }
  if(intent===1){
    // This is a telegraph *accent*, not a second computation of danger cells.
    const x=p.x,y=p.y-(b===3?105:b===2?133:117)*zoom;
    const pulse=.5+.5*Math.sin(ms/140);
    ctx.globalAlpha=.32+.20*pulse;ctx.strokeStyle=pal.core;ctx.lineWidth=(1.1+.6*pulse)*zoom;
    ellipse(ctx,x,y,16*zoom,8*zoom);ctx.stroke();
    ctx.globalAlpha=.55+.18*pulse;
    ctx.beginPath();ctx.moveTo(x-4*zoom,y);ctx.lineTo(x,y-7*zoom);ctx.lineTo(x+4*zoom,y);ctx.lineTo(x,y+7*zoom);ctx.closePath();ctx.stroke();
  }
  ctx.restore();return {kind:b,visual_only:true};
}
// New R13 encounter portrait staging: enlarged SOURCE sprite, unchanged pixel content.
// This is a readable game-frame presentation, NOT a new character drawing or rig.
function portrait(ctx,img,p,b,zoom,ms,intent,pattern){
 if(!img?.complete||!img.naturalWidth||!COLORS[b])return false;
 const pal=COLORS[b],sizes={1:215,2:260,3:288};
 const h=sizes[b]*zoom,w=h*img.naturalWidth/img.naturalHeight;
 const phase=ms/1000;
 const bob=b===1?Math.sin(phase*4)*1.5:b===2?Math.sin(phase*2.3)*4.7:Math.sin(phase*1.6)*1.7;
 ctx.save();ctx.translate(p.x,p.y-bob*zoom);
 // Painting shadows behind original pixels improve outline against similarly-toned flora.
 ctx.shadowColor=b===1?'rgba(214,125,67,.82)':b===2?'rgba(108,112,228,.88)':'rgba(79,141,102,.82)';
 ctx.shadowBlur=(intent===1?24:15)*zoom;
 ctx.globalAlpha=b===2?.90+.07*Math.sin(phase*2.1):1;
 ctx.drawImage(img,-w/2,-h*.92,w,h);
 ctx.restore();
 return {boss:b,source:'R06_SPRITE_UNCHANGED',visual_only:true,portrait_height:h};
}

// Painted boss nameplate is attached to the C++-reported world position.
function nameplate(ctx,p,b,zoom,label){
 if(!COLORS[b])return false;
 const w=154*zoom,h=24*zoom;
 const y=p.y-(b===1?222:b===2?253:270)*zoom;
 ctx.save();ctx.fillStyle='rgba(8,15,22,.79)';ctx.fillRect(p.x-w/2,y-h/2,w,h);
 ctx.strokeStyle=COLORS[b].edge;ctx.globalAlpha=.58;ctx.lineWidth=1*zoom;
 ctx.strokeRect(p.x-w/2,y-h/2,w,h);
 ctx.globalAlpha=1;ctx.font=`600 ${Math.round(11*zoom)}px system-ui`;
 ctx.fillStyle='#f5e4c6';ctx.textAlign='center';ctx.fillText(label,p.x,y+4*zoom);
 ctx.restore();return true;
}

// Cinematic framing is observational. It returns a read-only camera target.
function focus(player,boss,active){
 if(!active||!boss||![player.x,player.y,boss.x,boss.y].every(Number.isFinite))return {...player};
 const weight=.30;
 return {x:player.x*(1-weight)+boss.x*weight,y:player.y*(1-weight)+boss.y*weight};
}
root.NSStagecraftR13={before,after,portrait,nameplate,focus,readonly:true};
if(typeof module!=='undefined'&&module.exports)module.exports=root.NSStagecraftR13;
})(typeof globalThis!=='undefined'?globalThis:this);
