from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'site/world.js'
s=p.read_text()
def repl(a,b):
 global s
 if a not in s: raise RuntimeError('patch missing anchor '+repr(a[:120]))
 s=s.replace(a,b)
repl("...((root.NSR14ArtLab===true||root.NSR15ArtLab===true)&&root.NSArtR14?root.NSArtR14.assetKeys():[]),", "...((root.NSR14ArtLab===true||root.NSR15ArtLab===true)&&root.NSArtR14?root.NSArtR14.assetKeys():[]),...(root.NSR16ArtLab===true&&root.NSArtR16?root.NSArtR16.assetKeys():[]),")
repl("const r14Npc=(root.NSR14ArtLab===true||root.NSR15ArtLab===true)&&t===1?images[root.NSArtR14?.guard(pose,stepFrame)]:null;", "const npcPaintName=root.NSR16ArtLab===true?root.NSArtR16?.guard(pose,stepFrame):root.NSArtR14?.guard(pose,stepFrame);\n const r14Npc=(root.NSR14ArtLab===true||root.NSR15ArtLab===true||root.NSR16ArtLab===true)&&t===1?images[npcPaintName]:null;")
repl("if(root.NSR15ArtLab===true && root.NSPresentationR15 && sprite===r14Npc && r14Npc){root.NSPresentationR15.actor(ctx,sprite,ww,hh,ms,movingCycle,root.NSArtR14.guard(pose,stepFrame));}", "if(root.NSR16ArtLab===true&&root.NSPresentationR16&&sprite===r14Npc&&r14Npc){root.NSPresentationR16.actor(ctx,sprite,ww,hh,ms,movingCycle,npcPaintName);}\n  else if(root.NSR15ArtLab===true && root.NSPresentationR15 && sprite===r14Npc && r14Npc){root.NSPresentationR15.actor(ctx,sprite,ww,hh,ms,movingCycle,root.NSArtR14.guard(pose,stepFrame));}")
repl("(root.NSR14ArtLab===true||root.NSR15ArtLab===true))&&root.NSFinishingR12", "(root.NSR14ArtLab===true||root.NSR15ArtLab===true||root.NSR16ArtLab===true))&&root.NSFinishingR12")
repl("const frame=(root.NSR15ArtLab===true&&root.NSPresentationR15)?r15BossVisibleFrame:Math.floor(ms/170)%4;", "const frame=((root.NSR15ArtLab===true||root.NSR16ArtLab===true)&&root.NSPresentationR15)?r15BossVisibleFrame:Math.floor(ms/170)%4;")
repl("if((root.NSR14ArtLab===true||root.NSR15ArtLab===true)&&root.NSArtR14){const candidate=root.NSArtR14.boss(b,corner,frame);if(candidate&&images[candidate]?.complete&&images[candidate].naturalWidth)bossKey=candidate;}", "if((root.NSR14ArtLab===true||root.NSR15ArtLab===true||root.NSR16ArtLab===true)&&root.NSArtR14){const artSelector=root.NSR16ArtLab===true?root.NSArtR16:root.NSArtR14;const candidate=artSelector?.boss(b,corner,frame);if(candidate&&images[candidate]?.complete&&images[candidate].naturalWidth)bossKey=candidate;}")
repl("root.NSR14ArtLab===true||root.NSR15ArtLab===true))root.NSStagecraftR13", "root.NSR14ArtLab===true||root.NSR15ArtLab===true||root.NSR16ArtLab===true))root.NSStagecraftR13")
repl("if(root.NSR15ArtLab===true&&root.NSPresentationR15){root.NSPresentationR15.portrait(ctx,images[bossKey],p,b,zoom,ms,get('boss_intent'),get('boss_pattern'),bossKey);}", "if(root.NSR16ArtLab===true&&root.NSPresentationR16){root.NSPresentationR16.portrait(ctx,images[bossKey],p,b,zoom,ms,get('boss_intent'),get('boss_pattern'),bossKey);}\n  else if(root.NSR15ArtLab===true&&root.NSPresentationR15){root.NSPresentationR15.portrait(ctx,images[bossKey],p,b,zoom,ms,get('boss_intent'),get('boss_pattern'),bossKey);}")
repl("if(root.NSR15ArtLab===true){const b=get('boss');", "if(root.NSR15ArtLab===true||root.NSR16ArtLab===true){const b=get('boss');")
repl("root.NSR14ArtLab===true||root.NSR15ArtLab===true));const r11Preview", "root.NSR14ArtLab===true||root.NSR15ArtLab===true||root.NSR16ArtLab===true));const r11Preview")
repl("const previewName=(root.NSR14ArtLab===true||root.NSR15ArtLab===true)?root.NSArtR14?.building(sid,corner)", "const previewName=root.NSR16ArtLab===true?root.NSArtR16?.building(sid,corner):(root.NSR14ArtLab===true||root.NSR15ArtLab===true)?root.NSArtR14?.building(sid,corner)")
repl("if(root.NSR15ArtLab===true&&root.NSPresentationR15){\n       root.NSPresentationR15.building", "if(root.NSR16ArtLab===true&&root.NSPresentationR16){root.NSPresentationR16.building(ctx,previewTexture,center,sid,corner,zoom,opacity,ms,previewName);}\n      else if(root.NSR15ArtLab===true&&root.NSPresentationR15){\n       root.NSPresentationR15.building")
repl("const heroR14=(root.NSR14ArtLab===true||root.NSR15ArtLab===true)?images[root.NSArtR14?.hero(avatarView,frame)]:null;", "const heroPaintName=root.NSR16ArtLab===true?root.NSArtR16?.hero(avatarView,frame):root.NSArtR14?.hero(avatarView,frame);\n const heroR14=(root.NSR14ArtLab===true||root.NSR15ArtLab===true||root.NSR16ArtLab===true)?images[heroPaintName]:null;")
repl("if(root.NSR15ArtLab===true&&root.NSPresentationR15&&heroR14?.complete", "if(root.NSR16ArtLab===true&&root.NSPresentationR16&&heroR14?.complete&&heroR14.naturalWidth){\n    ctx.save();ctx.translate(a.x+motionX,a.y+motionY+2*zoom);\n    root.NSPresentationR16.actor(ctx,heroR14,w,h,ms,walking,heroPaintName);ctx.restore();\n   }else if(root.NSR15ArtLab===true&&root.NSPresentationR15&&heroR14?.complete")
repl("if(root.NSR15ArtLab===true&&get('boss')&&root.NSPresentationR15)", "if((root.NSR15ArtLab===true||root.NSR16ArtLab===true)&&get('boss')&&root.NSPresentationR15)")
repl("root.NSR14ArtLab===true||root.NSR15ArtLab===true)){", "NOTPRESENT") if False else None
repl("root.NSR14ArtLab===true||root.NSR15ArtLab===true)){", "root.NSR14ArtLab===true||root.NSR15ArtLab===true||root.NSR16ArtLab===true)){")
repl("root.NSR15ArtLab===true?'R15 PAINTED MOTION LAB", "root.NSR16ArtLab===true?'R16 REFINED EDGES LAB · NOT APPROVED':root.NSR15ArtLab===true?'R15 PAINTED MOTION LAB")
p.write_text(s)
h=R/'site/index.html';t=h.read_text()
a='<script src="r15_anchors.js"></script><script src="r15_presentation.js"></script>'
assert a in t
t=t.replace(a,a+'<script src="r16_art.js"></script><script src="r16_presentation.js"></script>')
h.write_text(t)
print('PATCH_R16_OK',len(s),len(t))
