/* MMORPG Maker AI · North Star V1 composite candidate. UI-only shell.
 * The authoritative experimental world, navigation legality, quests, profession actions,
 * NPC routes and three boss simulations are in one C++20 core compiled to WASM.
 * No client-side grant or fake fallback. Art / story / skills / bosses NOT CANON.
 */
(function(){'use strict';
const CLASSES=[
 [1,'Soldier'],[2,'Dragon Slayer'],[3,'Berserker'],[4,'Rogue A'],[5,'Rogue B'],
 [6,'Knight'],[7,'Ranger'],[8,'Warrior'],[9,'Monk'],[10,'Battlemage'],
 [11,'Dark Mage'],[12,'Pyromancer'],[13,'Necromancer'],[14,'Esper'],
 [15,'Alchemist'],[16,'Cryomancer'],[17,'Bard'],[18,'Cleric'],[19,'Druid'],
 [20,'Sentinel'],[21,'Shaman']
];
const KEY='mmai_ns_product_v1_r05_save'; // R01 journal remains untouched; ABI2 migration is fail-closed.
let scene='splash',engine=null,profile=null,log=[],settings={reduce:false,subtitles:true,volume:.6},lastMessage='';
const $=id=>document.getElementById(id);
function getSaved(){try{const d=JSON.parse(localStorage.getItem(KEY));return d&&d.version===6&&d.profile&&Array.isArray(d.commands)&&d.commands.length<=10000?d:null;}catch{return null;}}
function save(){if(!profile)return;try{localStorage.setItem(KEY,JSON.stringify({version:6,profile,commands:log}));}catch{lastMessage='O armazenamento local recusou salvar a jornada.';}}
function labelFor(id){return id===0?'Nenhuma':(CLASSES.find(x=>x[0]===id)||['','?'])[1];}
async function loadEngine(){try{
 const res=await fetch('product.wasm');if(!res.ok)throw Error('WASM HTTP '+res.status);
 const wasm=await WebAssembly.instantiate(await res.arrayBuffer(),{});engine=wasm.instance.exports;
 if(engine.nsw_abi()!==5||!engine.nsw_wasm_create||!engine.nsw_wasm_apply)throw Error('ABI mismatch');
 $('runtime').textContent='CORE C++20 / WASM · MUNDO NATIVO';
}catch(err){engine=null;$('runtime').textContent='CORE AUSENTE · PROGRESSO BLOQUEADO';console.warn('Core:',err.message);}}
function setScene(next){
 if(window.NSWorld?.active)window.NSWorld.unmount();
 const templates={splash:'tpl-splash',opening:'tpl-opening',title:'tpl-title',menu:'tpl-menu',creator:'tpl-creator',world:'tpl-world',options:'tpl-options',credits:'tpl-credits'};
 const t=$(templates[next]);if(!t)throw Error('unknown scene: '+next);scene=next;$('screen').innerHTML=t.innerHTML;
 const backdrop={splash:'brand',opening:'ensemble',title:'title',menu:'city',creator:'ensemble',world:'city',options:'title',credits:'ensemble'}[next];
 $('scene-art').style.backgroundImage=`url('assets/${backdrop}.webp')`;
 if(next==='opening'){
  const v=$('opening-video');v.volume=settings.volume;v.muted=settings.volume===0;
  v.addEventListener('ended',()=>setScene('title'),{once:true});v.play().catch(()=>{});
 }
 if(next==='creator')mountClasses();
 if(next==='menu')$('continue-btn').disabled=!getSaved();
 if(next==='world'){
  if(!engine||!profile){$('screen').innerHTML='<div class="simple-panel"><h2>CORE NÃO CONECTADO</h2><p>Não é possível simular a sessão sem o núcleo C++/WebAssembly.</p><button data-action="menu" class="primary">VOLTAR</button></div>';return;}
  window.NSWorld.mount({engine,action,profile:{...profile,classNames:Object.fromEntries(CLASSES)},openMenu:()=>setScene('menu'),get lastMessage(){return lastMessage;}});
 }
 if(next==='options'){$('reduce-motion').checked=settings.reduce;$('subtitles').checked=settings.subtitles;$('opening-volume').value=Math.round(settings.volume*100);}
}
function mountClasses(){const a=$('primary-class'),b=$('secondary-class');for(const [id,name] of CLASSES){
 const text=`R${String(id).padStart(2,'0')} · ${name}`;a.add(new Option(text,id));b.add(new Option(text,id));}
 const render=()=>{
  const root=document.getElementById('kit-preview');if(!root)return;
  const arr=window.NSKitLab||[];
  const pri=arr.find(v=>v.id===Number(a.value)),sec=arr.find(v=>v.id===Number(b.value));
  const fmt=(v,label)=>v?`${label}: ${v.source_id} ${v.name} — ${v.lab_mode_name}; suporte: ${v.utility_active.name}; passiva: ${v.passive_study.name}. ${v.lab_effect_description}`:`${label}: nenhuma classe adicional`;
  $('kit-preview-primary').textContent=fmt(pri,'Primária');
  $('kit-preview-secondary').textContent=fmt(sec,'Secundária');
  root.style.borderColor=pri?.research_primary_hex||'#cba976';
 };
 a.addEventListener('change',render);b.addEventListener('change',render);render();
}
const MESSAGES={1:'Ação espacial aceita pelo núcleo.',2:'Marco da missão confirmado pelo núcleo.',3:'Confronto iniciado com aviso de ataque.',4:'Confronto encerrado; resultado registrado.',5:'Sequência de três encontros concluída (fixture).',6:'Você caiu. Retire-se do encontro para recuperar.',10:'Comando recusado: revisão obsoleta.',11:'Comando inválido.',12:'Caminho bloqueado: colisão.',13:'Objetivo fora do alcance.',14:'Ação incompatível com o estágio.',15:'Recurso insuficiente.',16:'Sessão inexistente.',17:'Ação bloqueada: personagem incapacitado; recuo disponível.'};
function action(type,value=0){
 if(!engine||!profile){lastMessage='Núcleo de gameplay indisponível.';return 16;}
 if(log.length>=10000){lastMessage='Journal de laboratório lotado: nenhuma ação nova autorizada.';return 15;}
 const revision=engine.nsw_wasm_revision(),code=engine.nsw_wasm_apply(revision,type,value);
 lastMessage=MESSAGES[code]||'Resposta não identificada.';
 if(code>0&&code<10){
  log.push({revision,type,value,code});save();
  if(log.length>10000){lastMessage='Limite do save de laboratório alcançado. Exporte o journal antes de continuar.';}
 }
 return code;
}
function validate(p){return p&&Number.isInteger(p.primary)&&p.primary>=1&&p.primary<=21&&Number.isInteger(p.secondary)&&p.secondary>=0&&p.secondary<=21&&p.primary!==p.secondary&&typeof p.name==='string'&&p.name.length>=2&&p.name.length<=24;}
function begin(p,previous=[]){
 if(!engine||!validate(p)||!Array.isArray(previous)||previous.length>10000)return false;
 if(engine.nsw_wasm_create(p.primary,p.secondary)!==1)return false;
 const accepted=[];for(const evt of previous){
  if(!evt||!Number.isInteger(evt.type)||!Number.isInteger(evt.value)||!Number.isInteger(evt.revision)||evt.revision!==engine.nsw_wasm_revision())return false;
  const rc=engine.nsw_wasm_apply(evt.revision,evt.type,evt.value);if(rc!==evt.code||rc<1||rc>6)return false;
  accepted.push(evt);
 }
 profile=p;log=accepted;lastMessage=previous.length?'Estado reconstruído por replay do core C++ local. Não equivale a autenticação.':'Bem-vindo à estrada do sul. Fale com o guarda.';
 setScene('world');return true;
}
$('screen').addEventListener('click',e=>{
 const command=e.target.closest('[data-world-command]');if(command&&scene==='world'){
  const t=Number(command.dataset.worldCommand);if(t===2){const quest=engine.nsw_wasm_quest(),id=[1,2,3,4,5,6,7,0][Math.min(quest,7)];if(id)action(2,id);}
  else action(t,Number(command.dataset.worldValue||0));window.NSWorld.refresh();return;
 }
 const b=e.target.closest('[data-action]');if(!b)return;const k=b.dataset.action;
 if(k==='turn-left'||k==='turn-right'){if(scene==='world')window.NSWorld.rotate(k==='turn-right'?1:-1);return;}
 if(k==='creator'){setScene('creator');return;}
 if(k==='continue'){const s=getSaved();if(!s||!begin(s.profile,s.commands))alert('Save incompatível ou inválido. Nenhum progresso foi inventado.');return;}
 if(k==='menu'||k==='title'||k==='splash'||k==='opening'||k==='options'||k==='credits')setScene(k);
});
$('screen').addEventListener('submit',e=>{
 if(e.target.id!=='create-form')return;e.preventDefault();const p={
  name:$('hero-name').value.trim(),pronoun:$('pronoun').value,background:$('background').value,
  primary:Number($('primary-class').value),secondary:Number($('secondary-class').value)
 };
 if(!begin(p)){alert('Não foi possível criar o personagem: verifique as classes e o núcleo C++.');return;}
 save();
});
$('screen').addEventListener('change',e=>{
 const id=e.target.id;if(id==='reduce-motion'){settings.reduce=e.target.checked;document.querySelector('.app').classList.toggle('reduced-motion',settings.reduce);}
 if(id==='subtitles')settings.subtitles=e.target.checked;
 if(id==='opening-volume')settings.volume=Number(e.target.value)/100;
});
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&scene==='title'){e.preventDefault();setScene('menu');}});
setScene('splash');loadEngine();
})();
