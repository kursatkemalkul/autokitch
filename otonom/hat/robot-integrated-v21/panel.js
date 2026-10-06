import {compileOrder,planDemand} from './workflow-v16.js';
import {scenarioOrders} from './demand-v16.js';
const BASE='../hat3d/robot-integrated-v21/',$=id=>document.getElementById(id);
const load=async name=>{const r=await fetch(BASE+name);if(!r.ok)throw Error(name+' HTTP '+r.status);return r.json();};
const mv=$('mv'),sip=$('sip'),oy=$('oy'),tz=$('tz'),sn=$('sn'),adim=$('adim'),anlat=$('anlat');
const panel=document.createElement('div');panel.className='robot-panel';panel.innerHTML=`
<p id="robot-load" role="status">Robot, ray ve sipariş kayıtları yükleniyor…</p>
<label>Sipariş ürünü<select id="robot-recipe" aria-label="Sipariş ürünü"></select></label>
<label>İzlemek istediğin görev<select id="robot-task" aria-label="Sipariş görevi"><option value="all">Bir sipariş · hepsi</option><option value="Dough">Hamur → tabla</option><option value="Cola">İçecek → QR</option><option value="Dessert">Tatlı → QR</option><option value="Box">Kutu → QR</option></select></label>
<button id="robot-restart">Baştan</button><button id="robot-ready" disabled>Makine · kutu hazır sinyali</button>
<label>Sipariş geliş profili<select id="robot-demand" aria-label="Sipariş geliş profili"><option value="tek">Tek sipariş</option><option value="uc">Üç sipariş peş peşe</option><option value="aksam">Akşam 17–20</option><option value="cmt">Cumartesi 17–20</option><option value="surekli">Sürekli · 90 s / sipariş</option></select></label>
<label>Senaryo tohumu<input id="robot-seed" type="number" min="1" value="1"></label>
<button id="robot-plan">Yoğunluk planını hesapla</button><p id="robot-plan-result"></p>
<button id="robot-export">Isaac aktarım kaydını indir</button>
<p>Ray dış boyu: 4080 mm; özel strok: 3684 mm. Yayındaki v10l makine + ısıtıcısız 3×4 QR. El yıkama tezgâhı kaldırıldı. Kayıtlı hareketler ideal tutuşla oynar; güncel makineyle tam çarpışma ve fiziksel kavrama onayı yok. Yoğunluk hesabı, çok siparişin 3B doğrulaması değildir.</p>`;
sip.after(panel);
for(const control of panel.querySelectorAll('button,select,input'))control.disabled=true;
let D,config,base,current,loaded=false,gateReleased=false,busy=false,task='all',running=false,clock=0,lastTick=0;
const taskKey=stage=>/^(Box|Kutu)/.test(stage)?'Box':/^(Dessert|Tatlı)/.test(stage)?'Dessert':/^(Cola|İçecek)/.test(stage)?'Cola':'Dough';
function taskStart(){return task==='all'?0:current.stages.find(s=>taskKey(s.ad)===task)?.t??0;}
function status(t){
 const s=current.stages.filter(s=>s.t<=t+.001).at(-1)||current.stages[0];
 sn.textContent=`${t.toFixed(1)} / ${current.sure.toFixed(1)} sn`;
 anlat.textContent=`${current.ad} · ${s.ad}`;
 for(const b of adim.querySelectorAll('button'))b.classList.toggle('ak',Math.abs(+b.dataset.time-s.t)<.01);
}
function seek(t){running=false;mv.pause();oy.textContent='Oynat';clock=Math.max(0,Math.min(current.sure,t));mv.currentTime=Math.min(current.sure-.001,clock);tz.value=clock;status(clock);}
function play(){
 if(!loaded||busy)return;
 if(current.gate&&!gateReleased&&clock>=current.gate.time_s-.001){mv.pause();$('robot-ready').disabled=false;anlat.textContent='Makine · kutu hazır sinyali bekleniyor';return;}
 if(clock>=current.sure-.05)seek(taskStart());
 running=true;lastTick=0;mv.pause();oy.textContent='Duraklat';
}
async function selectOrder(id){
 busy=true;running=false;mv.pause();current=D.orders.find(s=>s.recipe===id);gateReleased=false;task='all';$('robot-task').value='all';$('robot-ready').disabled=true;
 mv.animationName='siparis_'+current.kod;tz.max=current.sure;
 // Give model-viewer one frame to switch its mixer before resetting the clock.
 await new Promise(requestAnimationFrame);mv.play({repetitions:1});mv.pause();seek(0);busy=false;
 adim.replaceChildren();for(const s of current.stages){const b=document.createElement('button');b.textContent=s.ad;b.dataset.time=s.t;b.onclick=()=>{task='all';$('robot-task').value='all';seek(s.t);};adim.appendChild(b);}
 for(const b of sip.querySelectorAll('button'))b.classList.toggle('ak',b.dataset.recipe===id);
 $('robot-recipe').value=id;
}
oy.onclick=()=>{if(!running)play();else{running=false;mv.pause();oy.textContent='Oynat';}};
tz.oninput=()=>{if(current)seek(+tz.value);};
$('robot-restart').onclick=()=>{gateReleased=false;$('robot-ready').disabled=true;seek(taskStart());play();};
$('robot-recipe').onchange=()=>selectOrder($('robot-recipe').value);
$('robot-task').onchange=()=>{task=$('robot-task').value;seek(taskStart());};
$('robot-ready').onclick=()=>{gateReleased=true;$('robot-ready').disabled=true;play();};
$('robot-plan').onclick=()=>{
 const arrivals=scenarioOrders({scenario:$('robot-demand').value,seed:Math.max(1,+$('robot-seed').value||1),lahm:true,lahmPct:25,gapSec:90,randArr:false}).map(x=>({...x,cola:true,dessert:true}));
 const p=planDemand(arrivals,config,base),s=p.summary;
 $('robot-plan-result').textContent=`${s.orders} sipariş · ${s.completed} zaman planı · en uzun tamamlanma ${Math.round(s.max_wait_s)} sn · robot doluluğu %${Math.round(s.robot_utilization*100)}. Çoklu sipariş hesabı; ayrı 3B güzergâh onayı yok.`;
};
$('robot-export').onclick=()=>{
 const recipe=config.recipes.find(r=>r.id===current.recipe),record=compileOrder(base,recipe),out={version:21,source_machine:D.source_sha256,units:'SI: metres, radians, seconds',frame:'native Isaac Z-up; GLB display uses X rotation -90deg',recipe,current_time_s:mv.currentTime,record,phase_schema:config.phase_schema,limits:config.limits,ideal_grasp:true,collision_certified:false};
 const url=URL.createObjectURL(new Blob([JSON.stringify(out)],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download=`robot_v21_${current.recipe}_isaac.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};
for(const b of $('hz').querySelectorAll('button'))b.onclick=()=>{mv.timeScale=+b.dataset.h;for(const x of $('hz').querySelectorAll('button'))x.classList.toggle('ak',x===b);$('hzn').textContent=+b.dataset.h===1?'gerçek süre':b.dataset.h+'× izleme';};
try{
 [D,config,base]=await Promise.all([load('manifest.json'),load('workflow_v21.json'),load('order_v16.json')]);
 const r=await fetch(BASE+'hat3_robot_v21.glb.gz?v='+D.raw_web_sha256.slice(0,12));if(!r.ok)throw Error('GLB HTTP '+r.status);
 const raw=await new Response(r.body.pipeThrough(new DecompressionStream('gzip'))).arrayBuffer();
 const digest=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',raw)),x=>x.toString(16).padStart(2,'0')).join('');if(raw.byteLength!==D.raw_web_bytes||digest!==D.raw_web_sha256)throw Error('Model bütünlük kontrolü başarısız');
 await customElements.whenDefined('model-viewer');
 const ready=new Promise((resolve,reject)=>{mv.addEventListener('load',resolve,{once:true});mv.addEventListener('error',()=>reject(Error('3B model açılamadı')),{once:true});});
 mv.src=URL.createObjectURL(new Blob([raw],{type:'model/gltf-binary'}));await ready;
 const missing=D.orders.filter(s=>!mv.availableAnimations.includes('siparis_'+s.kod));if(missing.length)throw Error('Robot animasyon kanalı eksik');
 sip.replaceChildren();for(const s of D.orders){const b=document.createElement('button');b.textContent=s.ad;b.dataset.recipe=s.recipe;b.onclick=()=>{selectOrder(s.recipe).then(play);};sip.appendChild(b);const o=document.createElement('option');o.value=s.recipe;o.textContent=s.ad;$('robot-recipe').appendChild(o);}
 loaded=true;for(const control of panel.querySelectorAll('button,select,input'))control.disabled=false;$('robot-ready').disabled=true;await selectOrder(D.orders[0].recipe);
 sip.parentNode.insertBefore(panel,sip);
 $('robot-load').textContent='UR10e + igus ray + 12 gözlü QR · 8 sipariş kaydı hazır';
 function tick(now){
  requestAnimationFrame(tick);
  if(busy||!loaded||!running){lastTick=0;return;}
  const dt=lastTick?Math.min(.1,(now-lastTick)/1000):0;lastTick=now;
  let t=Math.min(current.sure,clock+dt*(mv.timeScale||1));
  let stop=false,waiting=false;
  if(current.gate&&!gateReleased&&t>=current.gate.time_s){t=current.gate.time_s;stop=true;waiting=true;}
  if(task!=='all'){const next=current.stages.find(s=>s.t>taskStart()+.01&&taskKey(s.ad)!==task);if(next&&t>=next.t){t=next.t;stop=true;}}
  if(t>=current.sure)stop=true;
  clock=t;mv.currentTime=Math.min(current.sure-.001,t);tz.value=t;status(t);
  if(stop){running=false;oy.textContent=t>=current.sure?'Tekrar oynat':'Oynat';}
  if(waiting){$('robot-ready').disabled=false;anlat.textContent='Makine · kutu hazır sinyali bekleniyor';}
 }
 requestAnimationFrame(tick);
}catch(e){console.error(e);$('robot-load').textContent='Robot sahnesi açılamadı: '+e.message;}
