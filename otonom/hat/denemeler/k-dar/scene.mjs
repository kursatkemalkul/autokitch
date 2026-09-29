import * as T from 'https://esm.sh/three@0.160.1';
import {OrbitControls} from 'https://esm.sh/three@0.160.1/examples/jsm/controls/OrbitControls.js';
import {P,state} from './motion.mjs';
const $=s=>document.getElementById(s);
try{
const scene=new T.Scene();scene.background=new T.Color('#edf3f6');
scene.add(new T.HemisphereLight(0xffffff,0xabc2ce,2.3));let light=new T.DirectionalLight(0xffffff,2.5);light.position.set(-600,1800,1200);scene.add(light);
const renderer=new T.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));$('view').appendChild(renderer.domElement);
const camera=new T.PerspectiveCamera(36,1,1,12000),controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.minDistance=350;controls.maxDistance=5000;
const mat=(color,extra={})=>new T.MeshStandardMaterial({color,roughness:.55,metalness:.25,...extra});
const steel=mat('#bdcbd1'),dark=mat('#435c69'),blue=mat('#168ba9'),orange=mat('#ee973c'),belt=mat('#e0e8dc'),card=mat('#bc9561'),dough=mat('#e5ba70'),cheese=mat('#d48b38'),red=mat('#c64b35'),glass=mat('#bed5dc',{transparent:true,opacity:.1,depthWrite:false}),green=mat('#719b49');
const root=new T.Group();scene.add(root);const shells=new T.Group();root.add(shells);shells.visible=false;
function box(name,x,y,z,w,h,d,m,parent=root){let o=new T.Mesh(new T.BoxGeometry(w,h,d),m);o.position.set(x,y,z);o.name=name;parent.add(o);return o;}
function cyl(name,x,y,z,r,h,m,parent=root){let o=new T.Mesh(new T.CylinderGeometry(r,r,h,32),m);o.position.set(x,y,z);o.name=name;parent.add(o);return o;}
function segment(name,a,b,r,m,parent=root){let o=cyl(name,0,0,0,r,1,m,parent);place(o,a,b);return o;}
function place(o,a,b){let v=new T.Vector3(...b).sub(new T.Vector3(...a));o.position.copy(new T.Vector3(...a).addScaledVector(v,.5));o.scale.y=v.length();o.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),v.normalize());}
function line(points,color,parent=root){let o=new T.Line(new T.BufferGeometry().setFromPoints(points.map(v=>new T.Vector3(...v))),new T.LineBasicMaterial({color}));parent.add(o);return o;}
function label(message,pos,size=22,parent=root){let c=document.createElement('canvas');c.width=1024;c.height=128;let g=c.getContext('2d');g.fillStyle='#244557';g.font='bold 44px Arial';g.textAlign='center';g.fillText(message,512,72);let tx=new T.CanvasTexture(c);let sp=new T.Sprite(new T.SpriteMaterial({map:tx,depthTest:false}));sp.position.set(...pos);sp.scale.set(size*8,size,1);parent.add(sp);return sp;}
// Independent frame; rear/front datum and full cabinet height preserved.
for(let x of [20,380])for(let z of [-800,49]){box('30 mm dikme',x,950,z,30,1600,30,steel);cyl('Ayak',x,61.5,z,8,123,dark);cyl('Ayak tabanı',x,5,z,22,10,dark);}
for(let y of [140,877,1840]){box('Enine kayıt',200,y,-800,360,30,30,steel);box('Ön kayıt',200,y,49,360,30,30,steel);}
box('Alt tabla',200,894,-385,397,3,878,steel);
box('Arka kapak',200,994,-829.25,397,1738,1.5,glass,shells);box('Ön kapak',200,994,78.25,394,1738,1.5,glass,shells);
for(let x of [.75,399.25]){box('Yan alt',x,511,-385,1.5,770,878,glass,shells);box('Yan üst',x,1470,-385,1.5,790,878,glass,shells);box('Yan arka',x,985,-640,1.5,180,377,glass,shells);}
box('Üst kapak',200,1861.25,-385,400,1.5,909,glass,shells);
// K receiving belt, fixed 400mm belt width in z, custom shortened length in x.
box('K üst bant',200,995,-212,360,2,400,belt);box('Bant alt dönüş',200,932,-212,360,2,400,belt);box('Bant destek tablası',200,991,-212,315,6,396,steel);
for(let x of [20,380]){let r=cyl('Bant rulosu',x,969,-212,25,400,dark);r.rotation.x=Math.PI/2;}
for(let z of [-421,-3])box('Bant yan taşıyıcı',200,960,z,390,55,6,steel);
for(let x of [65,335])for(let z of [-421,-3])box('Bant ayağı',x,925,z,20,60,20,steel);
box('K ölü plaka',394,993,-212,12,6,400,steel);
box('Fırın bant referansı',-190,995,-212,375,6,400,mat('#919f9c'));
label('FIRIN →',[-140,1060,70],19);
const beltMarks=[];for(let i=0;i<14;i++)beltMarks.push(box('Bant izi',i*28,996.3,-212,1,.3,385,dark));
// Original cutter dimensions (simplified hardware).
for(let z of [-270,-45])box('Kesici köprü kirişi',200,1440,z,370,40,40,steel);
box('Silindir plakası',200,1416,-170,180,8,275,steel);
box('Kılavuzlu silindir',200,1334,-170,150,150,90,dark);
const cutter=new T.Group();root.add(cutter);
box('Kesici kafa plakası',200,1170.5,-170,170,8,125,steel,cutter);
for(let x of [145,200,255])cyl('Kılavuz mili',x,1310,-170,10,280,steel,cutter);
for(let i=0;i<6;i++){let a=i*Math.PI/3;let o=box('Yıldız bıçak',200+81.5*Math.cos(a),1144,-170+81.5*Math.sin(a),133,45,1.5,steel,cutter);o.rotation.y=-a;}
let ring=new T.Mesh(new T.TorusGeometry(157.25,.75,8,96),dark);ring.rotation.x=Math.PI/2;ring.position.set(200,1134,-170);cutter.add(ring);
cyl('Sprey nozülü',200,1177,-170,9,34,orange,cutter);
let spray=new T.Mesh(new T.ConeGeometry(145,142,48,1,true),mat('#efcc56',{transparent:true,opacity:.3,depthWrite:false}));spray.position.set(200,1082,-170);root.add(spray);
// Fixed tank and panel envelopes remain full size and mounted.
box('Pano montaj plakası',200,1664.5,-820,265,385,4,steel);box('Elektrik elemanları zarfı',200,1650,-770,250,340,92,dark);
box('Tank rafı',200,1469.5,-540,250,5,260,steel);
for(let x of [90,310])box('Tank raf konsolu',x,1449,-655,20,36,35,steel);
cyl('3 L tank Ø160 x 280',200,1612,-540,80,280,steel);cyl('Tank kapağı',200,1759,-540,88,14,dark);
segment('Isıtmalı hortum',[200,1770,-540],[360,1770,-360],5,orange);segment('Hortum iniş',[360,1770,-360],[360,1220,-360],5,orange);
// New articulated pusher. Actual drives are unselected envelopes, not scaled catalogue parts.
box('İtici arka travers',200,1000,-670,370,40,70,steel);
for(let x of [20,380])box('Travers askısı',x,948,-670,25,106,60,steel);
cyl('Omuz servo zarfı',P.shoulderX,1040,-670,40,60,dark);
const link1=segment('1. kol 180',[200,1080,-670],[300,1080,-600],12,blue);
const link2=segment('2. kol 430',[300,1046,-600],[30,1046,-350],8,blue);
const elbowJoint=cyl('Dirsek servo zarfı',0,1070,0,22,45,dark);
const wrist=cyl('Bilek servo zarfı',0,1038,0,20,38,dark);
const liftSupport=box('Kaldırma kızağı',P.shoulderX,1080,-670,65,60,60,dark);
const paddle=box('POM itici',26,1021.5,-350,8,45,260,orange);
const wristBracket=box('İtici bilek bağlantısı',20,1033,-350,36,16,22,steel);
const bridge=box('E köprü referansı',447,980,-206,90,3,320,steel);
const boxGroup=new T.Group();root.add(boxGroup);
box('Karton taban',660,936.8,-206,320,1.6,320,card,boxGroup);
for(let z of [-365.2,-46.8])box('Kutu yan duvarı',660,958.6,z,320,42,1.6,card,boxGroup);
box('Kutu arka duvarı',819.2,959.6,-206,1.6,44,320,card,boxGroup);
box('Kutu açık kapak',821,1139,-206,1.6,312,315,card,boxGroup);
box('Kutu ön duvarı',500.8,958.6,-206,1.6,42,320,card,boxGroup);
box('E kalıp ön referansı',495,945,-206,5,54,320,steel);
// E window outline; green when selected, envelope only, not full E mechanism.
line([[400,978,-372],[400,1062,-372],[400,1062,-24],[400,978,-24],[400,978,-372]],'#468d72');
label('KUTU / E',[700,1040,85],20);
const product=new T.Group();root.add(product);cyl('Pide zarfı Ø300',0,5,0,150,10,dough,product);cyl('Üst malzeme',0,12.5,0,142,5,cheese,product);
for(let i=0;i<12;i++){let a=i*2.4,r=25+(i%4)*28;cyl('Topping',Math.cos(a)*r,16,Math.sin(a)*r,9,3,i%2?green:red,product);}
const cuts=new T.Group();product.add(cuts);for(let i=0;i<3;i++){let o=box('Kesik',0,15.8,0,293,.6,1.3,dark,cuts);o.rotation.y=i*Math.PI/3;}
const old=new T.Box3Helper(new T.Box3(new T.Vector3(0,123,-830),new T.Vector3(600,1862,79)),0xc36d4b);root.add(old);old.visible=false;
let paths=[];for(let t=8.5;t<=10.101;t+=.02){let s=state(t);paths.push([s.fx,1021.5,s.fz]);}const path=line(paths,'#e39336');path.visible=false;
line([[0,902,115],[0,872,115],[400,872,115],[400,902,115]],'#16839c');label('K: 400 mm',[200,853,115],21);
const ground=new T.GridHelper(2500,25,0xc5d3da,0xe0e7eb);ground.position.set(400,0,-350);scene.add(ground);
function view(mode){let target=[300,1135,-250],pos=[1250,1660,1500];if(mode==='top'){target=[280,1000,-285];pos=[280,2850,-284];}if(mode==='side')pos=[300,1350,2000];if(mode==='full'){target=[240,920,-350];pos=[1850,1900,2500];}controls.target.set(...target);camera.position.set(...pos);controls.update();}
view('iso');let time=0,play=false,last=0;
function drawState(t){let s=state(t);cutter.position.y=-s.cut;spray.visible=s.spray;product.position.set(s.x,s.y,s.z);product.visible=s.visible;cuts.visible=s.marks;
let e=s.elbow;place(link1,[P.shoulderX,1080+s.lift,-670],[e.x,1080+s.lift,e.z]);place(link2,[e.x,1046+s.lift,e.z],[s.fx-12,1046+s.lift,s.fz]);elbowJoint.position.set(e.x,1070+s.lift,e.z);wrist.position.set(s.fx-12,1038+s.lift,s.fz);paddle.position.set(s.fx-4,1021.5+s.lift,s.fz);wristBracket.position.set(s.fx-17,1033+s.lift,s.fz);liftSupport.position.y=1050+s.lift/2;liftSupport.scale.y=1+s.lift/60;
for(let i=0;i<beltMarks.length;i++){beltMarks[i].position.x=20+(i*28+(t<2.3?t*80:184))%360;}
$('phase').textContent=s.phase;$('clock').textContent=t.toFixed(1)+' / 20 sn';$('time').value=t;}
drawState(0);$('loading').remove();
$('play').onclick=()=>{play=!play;$('play').textContent=play?'Ⅱ Duraklat':'▶ Çalıştır'};$('reset').onclick=()=>{time=0;play=false;$('play').textContent='▶ Çalıştır';drawState(time)};
$('time').oninput=e=>{time=Number(e.target.value);play=false;$('play').textContent='▶ Çalıştır';drawState(time)};
for(let k of ['iso','top','side','full'])$(k).onclick=()=>view(k);
$('shell').onchange=e=>shells.visible=e.target.checked;$('old').onchange=e=>old.visible=e.target.checked;$('track').onchange=e=>path.visible=e.target.checked;
$('check').textContent='Kontrol kapsamı: kol boyları ve eklem erişimi, kesici korumasının yan payı, örneklenen itici yolunun K yan sınırı ve E geçiş ağzı. Tam katı CAD/üretim çakışma taraması değildir.';
new ResizeObserver(()=>{let r=$('view').getBoundingClientRect();renderer.setSize(r.width,r.height);camera.aspect=r.width/r.height;camera.updateProjectionMatrix()}).observe($('view'));
function animate(now){let dt=Math.min(.05,(now-last)/1000);last=now;if(play){time+=dt*Number($('speed').value);if(time>20)time=0;drawState(time)}controls.update();renderer.render(scene,camera);requestAnimationFrame(animate)}requestAnimationFrame(animate);
}catch(e){$('error').textContent='3D açılamadı: '+e.message;throw e;}
