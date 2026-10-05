import * as T from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
const $=id=>document.getElementById(id),base='../../../../_local/codex_k_montaj/';const response=await fetch(base+'support_workshop.json');if(!response.ok)throw Error(`Montaj planı ${response.status}`);const D=await response.json();
const renderer=new T.WebGLRenderer({antialias:true});renderer.localClippingEnabled=true;renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));document.body.append(renderer.domElement);
const scene=new T.Scene();scene.background=new T.Color(0xe9edf2);scene.add(new T.HemisphereLight(0xffffff,0x64748b,2));const sun=new T.DirectionalLight(0xffffff,2);sun.position.set(2,4,3);scene.add(sun);
const camera=new T.PerspectiveCamera(40,1,.005,30),controls=new OrbitControls(camera,renderer.domElement);camera.position.set(2,1.8,2.5);controls.target.set(.1,.65,0);controls.update();
const loaded=await new GLTFLoader().loadAsync(base+'support_workshop.glb'),root=loaded.scene;root.position.set(-4.5,0,.4);scene.add(root);
const entries=new Map(),fixture=new Set(D.fixture_nodes),welds=new Set(D.events.filter(e=>e.operation==='weld').flatMap(e=>e.nodes));
for(const name of [...fixture,...Object.keys(D.initial_offsets_mm)]){
 if(entries.has(name))continue;let object=root.getObjectByName(name);if(!object)throw Error(`Eksik parça: ${name}`);
 object.traverse(o=>{if(!o.isMesh)return;o.material=o.material.clone();o.material.color.set(welds.has(name)?0xc63024:fixture.has(name)?0x53718f:0xacb8c5);o.userData.baseColor=o.material.color.clone();});
 let basePosition=object.position.clone();
 if(name.endsWith('_mil')){
  root.updateMatrixWorld(true);const box=new T.Box3().setFromObject(object),pivot=new T.Vector3((box.min.x+box.max.x)/2,box.min.y,(box.min.z+box.max.z)/2);root.worldToLocal(pivot);const parent=object.parent,group=new T.Group();group.position.copy(pivot);parent.add(group);parent.remove(object);group.add(object);object.position.sub(pivot);object=group;basePosition=pivot;
 }
 entries.set(name,{object,basePosition});
}
const torch=new T.Group(),toolMaterial=new T.MeshStandardMaterial({color:0x596575,metalness:.7,roughness:.35});
for(const [r,y0,y1] of [[.0008,0,.004],[.004,.004,.024],[.006,.024,.05]]){const m=new T.Mesh(new T.CylinderGeometry(r,r,y1-y0,16),toolMaterial);m.position.y=(y0+y1)/2;torch.add(m);}root.add(torch);
let clock=0,running=false,active;
const v=a=>new T.Vector3(...a).multiplyScalar(.001),mix=(a,b,f)=>a.map((x,i)=>x+(b[i]-x)*f);
function arrival(e,f){if(e.operation!=='arrive')return mix(e.start_mm,e.end_mm,f);const a=e.start_mm,b=e.end_mm,height=Math.max(a[1],b[1])+100,up=[a[0],height,a[2]],over=[b[0],height,b[2]];if(f<.25)return mix(a,up,f*4);if(f<.75)return mix(up,over,(f-.25)*2);return mix(over,b,(f-.75)*4);}
function renderState(){
 const poses=new Map(),visible=new Map(),clipping=new Map(),temp=new Map();for(const [name,p] of Object.entries(D.initial_offsets_mm)){if(p===null)visible.set(name,false);else poses.set(name,p);}
 torch.visible=false;const phase=clock*D.events.length,index=Math.min(D.events.length-1,Math.floor(phase));active=D.events[index];
 for(let i=0;i<=index;i++){
  const e=D.events[i],f=i<index?1:clock===1?1:phase-index;
  if(e.operation==='weld'){
   const progress=Math.max(0,Math.min(1,(f-.2)/.6)),axis=v(e.p1_mm).sub(v(e.p0_mm)).normalize(),point=v(mix(e.p0_mm,e.p1_mm,progress));
   for(const name of e.nodes){visible.set(name,progress>0);clipping.set(name,progress<1?new T.Plane().setFromNormalAndCoplanarPoint(axis.clone().negate(),point):null);}
   if(progress===1)for(const name of e.fixes||[])temp.delete(name);
   if(i===index&&f<1){const d=new T.Vector3(...e.torch_outward);let p;if(f<.2)p=v(e.p0_mm).addScaledVector(d,.1-.098*f/.2);else if(f<.8)p=point.clone().addScaledVector(d,.002);else p=v(e.p1_mm).addScaledVector(d,.002+.098*(f-.8)/.2);torch.position.copy(p);torch.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),d);torch.visible=true;}
  }else{
   const p=arrival(e,f);for(const name of e.nodes){const q=[...p];if(e.jaw_extra_mm&&(/_mil$|_pabuc$/.test(name)))q[1]+=e.jaw_extra_mm;poses.set(name,q);visible.set(name,true);}
   if(f===1&&e.operation==='arrive'&&e.warning)temp.set(e.nodes[0],e.warning);
   if(f===1&&e.operation==='clamp_close')for(const name of e.fixes||[])temp.delete(name);
  }
 }
 for(const [name,entry] of entries){const p=poses.get(name)||[0,0,0];entry.object.position.copy(entry.basePosition).add(v(p));entry.object.visible=visible.get(name)!==false;
  if(name.endsWith('_mil'))entry.object.rotation.y=-p[1]*2*Math.PI/1.25;
  entry.object.traverse(o=>{if(!o.isMesh)return;o.material.clippingPlanes=clipping.get(name)?[clipping.get(name)]:[];o.material.color.copy(o.userData.baseColor);if(active.nodes.includes(name))o.material.color.set(welds.has(name)?0xc63024:0xf28c28);});
 }
 $('time').value=clock;$('status').textContent=`${index+1}/${D.events.length} · ${active.text}`;$('temporary').textContent=[...temp.values()].join(' ');
}
$('play').onclick=()=>{if(clock===1)clock=0;running=!running;$('play').textContent=running?'Duraklat':'Oynat';};$('reset').onclick=()=>{clock=0;running=false;$('play').textContent='Oynat';renderState();};$('time').oninput=()=>{running=false;clock=Number($('time').value);$('play').textContent='Oynat';renderState();};
$('focus').onclick=()=>{const e=entries.get(active.nodes[0]);if(!e)return;root.updateMatrixWorld(true);const box=new T.Box3().setFromObject(e.object),c=box.getCenter(new T.Vector3()),span=Math.max(.15,...box.getSize(new T.Vector3()).toArray());controls.target.copy(c);camera.position.copy(c).add(new T.Vector3(span,span,span));controls.update();};
function resize(){renderer.setSize(innerWidth,innerHeight);camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();}addEventListener('resize',resize);resize();renderState();let last=performance.now();
renderer.setAnimationLoop(now=>{if(running){clock=Math.min(1,clock+Math.min((now-last)/1000,.1)*Number($('speed').value)/(D.events.length*2.5));renderState();if(clock===1){running=false;$('play').textContent='Tekrar oynat';}}last=now;controls.update();renderer.render(scene,camera);});
