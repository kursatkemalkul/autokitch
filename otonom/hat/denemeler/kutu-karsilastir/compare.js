const $=id=>document.getElementById(id);
const viewers=[$('old'),$('new')], durations=[23,23], loaded=[false,false], originals=new Map();
let position=0,playing=false,last=0;
const endpoint=(t,d)=>Math.min(t,d-0.001);
function render(){
  viewers.forEach((v,i)=>{const t=endpoint(position*($('mode').value==='progress'?durations[i]:23),durations[i]);if(loaded[i]){v.pause();v.currentTime=t;} $('clock'+i).textContent=t.toFixed(2)+' s';});
  $('time').value=position*1000;$('readout').textContent=(position*100).toFixed(1)+'%';
  $('modeNote').textContent=$('mode').value==='seconds'?'İki sürüm aynı 0–23 s zamanında ilerler.':'Her sürüm kendi çevriminde %0–100 ilerler.';
}
function stop(){playing=false;$('play').textContent='▶ Oynat';}
function seek(p){stop();position=Math.max(0,Math.min(1,p));render();}
function shell(){viewers.forEach((v,i)=>{if(!loaded[i])return;for(const mat of v.model.materials){if(!/ME_E_GOVDE__(kabuk|on_seffaf)$/.test(mat.name))continue;
 const key=i+':'+mat.name;if(!originals.has(key))originals.set(key,{color:[...mat.pbrMetallicRoughness.baseColorFactor],alpha:mat.alphaMode});
 const original=originals.get(key),color=[...original.color];if(!$('shell').checked)color[3]=0;
 mat.setAlphaMode($('shell').checked?original.alpha:'BLEND');mat.pbrMetallicRoughness.setBaseColorFactor(color);
}});}
await customElements.whenDefined('model-viewer');
viewers.forEach((v,i)=>{
 function ready(){loaded[i]=true;v.pause();$('status'+i).textContent='';shell();render();$('play').disabled=!loaded.every(Boolean);}
 v.addEventListener('load',ready);if(v.loaded)ready();
 v.addEventListener('error',()=>{$('status'+i).textContent='Model yüklenemedi. Yerel sunucuyu / kaynak modeli kontrol et.';stop();});
 v.addEventListener('camera-change',event=>{if(!$('linkCamera').checked||event.detail.source!=='user-interaction')return;const other=viewers[1-i],o=v.getCameraOrbit(),t=v.getCameraTarget();other.cameraOrbit=`${o.theta}rad ${o.phi}rad ${o.radius}m`;other.cameraTarget=`${t.x}m ${t.y}m ${t.z}m`;other.fieldOfView=v.getFieldOfView()+'deg';other.jumpCameraToGoal();});
});
$('play').onclick=()=>{if(!loaded.every(Boolean))return;playing=!playing;if(playing&&position>=1)position=0;$('play').textContent=playing?'❚❚ Duraklat':'▶ Oynat';last=performance.now();};
$('time').oninput=()=>seek(Number($('time').value)/1000);
$('back').onclick=()=>seek(position-1/30/23);$('next').onclick=()=>seek(position+1/30/23);
$('reset').onclick=()=>seek(0);$('mode').onchange=()=>{stop();render();};$('shell').onchange=shell;
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>viewers.forEach(v=>{v.cameraOrbit=b.dataset.view;v.cameraTarget='4.94m 1.14m -0.2m';v.fieldOfView='30deg';v.jumpCameraToGoal();}));
document.querySelectorAll('[data-time]').forEach(b=>b.onclick=()=>seek(Number(b.dataset.time)/23));
function frame(now){if(playing){position+=Math.min((now-last)/1000,0.1)*Number($('speed').value)/23;if(position>=1){if($('loop').checked)position=0;else{position=1;stop();}}render();}last=now;requestAnimationFrame(frame);}render();requestAnimationFrame(frame);
