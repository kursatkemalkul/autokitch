import * as T from 'https://esm.sh/three@0.160.1';
import {OrbitControls} from 'https://esm.sh/three@0.160.1/examples/jsm/controls/OrbitControls.js';

const q=id=>document.getElementById(id),method=document.body.dataset.method;
const V=1316/210,TRANSFER=method==='fold'?300/V:332/V;
const START=method==='fold'?6:8,END=START+TRANSFER,TOTAL=END+3;
const clamp=x=>Math.max(0,Math.min(1,x)),ease=x=>{x=clamp(x);return x*x*(3-2*x);};
let time=0,playing=false,last=0,lastPhase='',follow=true,camMode=method==='fold'?'side':'iso';
try{
const scene=new T.Scene();scene.background=new T.Color('#f7f9fc');
scene.add(new T.HemisphereLight('#ffffff','#aebfce',2));const sun=new T.DirectionalLight('#ffffff',2);sun.position.set(200,700,600);scene.add(sun);
const renderer=new T.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));q('view').appendChild(renderer.domElement);
const camera=new T.PerspectiveCamera(38,1,1,8000),controls=new OrbitControls(camera,renderer.domElement);controls.minDistance=360;controls.maxDistance=3000;controls.enablePan=true;
const material=(c,props={})=>new T.MeshStandardMaterial({color:c,roughness:.68,metalness:.08,...props});
const steel=material('#a6b5c4'),table=material('#d2dce5'),beltMat=material('#318db4'),orange=material('#cf772d'),dark=material('#64788b'),bread=material('#e4bb67',{metalness:0,side:T.DoubleSide}),meat=material('#b45132'),green=material('#4e853e'),glass=material('#abbecf',{transparent:true,opacity:.11,depthWrite:false});
const unit=new T.BoxGeometry(1,1,1);
function box(p,x,y,z,w,h,d,m){const o=new T.Mesh(unit,m);o.position.set(x,y,z);o.scale.set(w,h,d);p.add(o);return o;}
function cyl(p,x,y,z,r,h,m,axis='y'){const o=new T.Mesh(new T.CylinderGeometry(r,r,h,48),m);if(axis==='z')o.rotation.x=Math.PI/2;if(axis==='x')o.rotation.z=Math.PI/2;o.position.set(x,y,z);p.add(o);return o;}
function rod(p,a,b,r,m){const v=new T.Vector3(...b).sub(new T.Vector3(...a)),o=new T.Mesh(new T.CylinderGeometry(r,r,v.length(),12),m);o.position.copy(new T.Vector3(...a).addScaledVector(v,.5));o.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),v.normalize());p.add(o);return o;}
function circle(p,r,y,color){const pts=[];for(let i=0;i<=96;i++){const a=i*Math.PI/48;pts.push(new T.Vector3(r*Math.cos(a),y,r*Math.sin(a)));}const l=new T.Line(new T.BufferGeometry().setFromPoints(pts),new T.LineBasicMaterial({color}));p.add(l);return l;}
function pointLine(p,pts,color){const l=new T.Line(new T.BufferGeometry().setFromPoints(pts.map(x=>new T.Vector3(...x))),new T.LineBasicMaterial({color}));p.add(l);return l;}

// Relative origin: current disk centre x2337, y1000, z-170. Oven dimensions from FT8.
box(scene,200.25,-4,0,56.5,4,320,table);for(const x of [183.5,217])cyl(scene,x,-13.5,0,11.5,320,dark,'z');
box(scene,500,-5,-34,538,6,381,table);for(const z of [-232,164])box(scene,500,-30,z,540,32,12,steel);
box(scene,595,86,-34,350,10,440,glass);box(scene,595,35,-250,350,90,10,glass);
const ovenTicks=[];for(let i=0;i<28;i++)ovenTicks.push(box(scene,235+i*19,-1.65,-34,1,.4,377,dark));
const insetTicks=[];for(let i=0;i<6;i++)insetTicks.push(box(scene,174+i*9,-1.6,0,1,.4,316,dark));

// Shared dough mesh. Its bending path is prescribed, not a contact / adhesion solver.
const N=64,R=14,base=[],idx=[],layerSize=(R+1)*N;
for(let l=0;l<2;l++)for(let r=0;r<=R;r++)for(let j=0;j<N;j++){const a=j*2*Math.PI/N;base.push([150*r/R*Math.cos(a),150*r/R*Math.sin(a),l]);}
for(let l=0;l<2;l++)for(let r=0;r<R;r++)for(let j=0;j<N;j++){const a=l*layerSize+r*N+j,b=l*layerSize+r*N+(j+1)%N,c=a+N,d=b+N;idx.push(a,c,b,b,c,d);}
for(let j=0;j<N;j++){const a=R*N+j,b=R*N+(j+1)%N;idx.push(a,b,a+layerSize,b,b+layerSize,a+layerSize);}
const dg=new T.BufferGeometry();dg.setAttribute('position',new T.Float32BufferAttribute(new Float32Array(base.length*3),3));dg.setIndex(idx);const food=new T.Mesh(dg,bread);food.frustumCulled=false;scene.add(food);
const toppings=[];for(let i=0;i<48;i++){const a=i*2.39996323,r=Math.sqrt((i+.5)/48)*132,o=cyl(scene,0,0,0,i%3?7:4,i%3?3:1.5,i%3?meat:green);toppings.push({o,x:Math.cos(a)*r,z:Math.sin(a)*r});}
const labels=[];function label(text,pos){const e=document.createElement('span');e.className='label3d';e.textContent=text;q('view').appendChild(e);labels.push({e,pos:new T.Vector3(...pos)});return labels.at(-1);}
label('Fırın bandı · 998 mm',[430,-50,170]);
let tilt,flap,travel,turn,head,sweep,oldRing,actuator,stamp,lock,feedTicks=[];

if(method==='fold'){
 // Circular disk split by chord x=120: the front 50 mm circular segment folds inward.
 function segment(keepFront){const poly=[];for(let i=0;i<144;i++){const a=i*2*Math.PI/144;poly.push([170*Math.cos(a),170*Math.sin(a)]);}const out=[];for(let i=0;i<poly.length;i++){const a=poly[i],b=poly[(i+1)%poly.length],ia=keepFront?a[0]>=120:a[0]<=120,ib=keepFront?b[0]>=120:b[0]<=120;if(ia)out.push(a);if(ia!==ib){const f=(120-a[0])/(b[0]-a[0]);out.push([120,a[1]+f*(b[1]-a[1])]);}}
  const sh=new T.Shape();out.forEach(([x,z],i)=>i?sh.lineTo(x-120,z):sh.moveTo(x-120,z));sh.closePath();const g=new T.ExtrudeGeometry(sh,{depth:6,bevelEnabled:false});const m=new T.Mesh(g,keepFront?orange:table);m.rotation.x=Math.PI/2;return m;
 }
 travel=new T.Group();scene.add(travel);tilt=new T.Group();tilt.position.x=120;travel.add(tilt);tilt.add(segment(false));flap=new T.Group();tilt.add(flap);flap.add(segment(true));
 cyl(tilt,0,-4,0,4,240,steel,'z');box(travel,25,-105,0,260,12,250,steel);
 for(const z of [-110,110]){box(scene,25,-124,z,370,16,14,steel);box(travel,20,-111,z,160,14,24,dark);rod(travel,[120,-97,z],[120,-8,z],6,steel);}
 actuator=rod(travel,[-85,-100,0],[-85,-9,0],10,orange);cyl(scene,0,-165,0,35,70,steel);box(scene,0,-203,0,240,10,250,steel);
 oldRing=circle(scene,170,.3,'#8e9cab');oldRing.visible=false;
 stamp=label('50 mm uç · aşağı / içeri',[122,-75,130]);
}else{
 for(const z of [-105,105])box(scene,-355,-97,z,1060,16,20,steel);
 for(const x of [-830,155])for(const z of [-105,105]){box(scene,x,-151,z,22,98,24,steel);box(scene,x,-201,z,75,8,65,steel);}
 travel=new T.Group();scene.add(travel);for(const z of [-105,105])box(travel,0,-83,z,160,16,35,dark);
 box(travel,0,-69,0,240,12,240,steel);cyl(travel,0,-46,0,82,34,dark);turn=new T.Group();travel.add(turn);
 // Backing plate supports the belt during pressing; locks are conceptual only.
 box(turn,0,-6.6,0,300,10,318,steel);box(turn,5,-.8,0,340,1.6,320,beltMat);box(turn,0,-31,0,338,1.6,320,beltMat);
 cyl(turn,-165,-15,0,15,320,beltMat,'z');cyl(turn,177,-3,0,3,320,beltMat,'z');
 for(const z of [-166,166])box(turn,0,-24,z,360,16,8,steel);
 cyl(turn,-165,-15,-195,17,44,orange,'z');box(turn,-165,-15,-222,34,34,12,orange);
 lock=box(travel,90,-39,0,18,22,30,orange);
 for(let i=0;i<18;i++)feedTicks.push(box(turn,-156+i*18,.15,0,1,.35,312,table));
 sweep=circle(travel,Math.hypot(360,340)/2,3,'#c4772b');oldRing=circle(travel,170,4,'#7e91a4');
 // Context stations only: press and one topping nozzle, not the detailed machine.
 for(const z of [-220,220])box(scene,-650,80,z,25,200,25,steel);box(scene,-650,184,0,36,24,465,steel);
 head=new T.Group();head.position.x=-650;scene.add(head);cyl(head,0,0,0,150,12,table);cyl(head,0,40,0,24,70,steel);
 box(scene,-390,131,-228,32,262,24,steel);box(scene,-390,250,-100,32,20,265,steel);cyl(scene,-390,191,0,47,102,glass);cyl(scene,-390,132,0,10,18,orange);
 label('Pres · bant kilitli',[-650,205,0]).context='press';label('Topping · tabla döner',[-390,285,0]).context='topping';stamp=label('Döner bant kaseti',[-650,-125,195]);
}

function state(t){
 if(method==='fold'){
  const a=12*Math.PI/180*ease(t/2),fold=120*Math.PI/180*ease((t-2)/1.5),dock=ease((t-3.5)/2.5),feed=V*Math.max(0,Math.min(TRANSFER,t-START));
  const ret=ease(t-END),unfold=ease(t-END-1),flatten=ease(t-END-2);
  return{a:a*(1-flatten),fold:fold*(1-unfold),dock:dock*(1-ret),x:50*dock*(1-ret),lift:8*ease(t/2)*(1-flatten),feed,ret,phase:t<2?'tilt':t<3.5?'fold':t<6?'dock':t<END?'feed':'return'};
 }
 let x=-650,angle=0,feed=0,phase='press';
 if(t>=2&&t<4){x=-650+260*ease((t-2)/2);phase='travel';}
 if(t>=4&&t<6){x=-390;angle=2*Math.PI*ease((t-4)/2);phase='topping';}
 if(t>=6&&t<8){x=-390+380*ease((t-6)/2);angle=2*Math.PI;phase='dock';}
 if(t>=8&&t<END){x=-10;angle=2*Math.PI;feed=(t-8)*V;phase='feed';}
 if(t>=END){x=-10-640*ease((t-END)/3);angle=2*Math.PI;feed=332;phase='return';}
 return{x,angle,feed,phase};
}

function foodPoint(x,z,s){
 if(method==='belt'){
  if(time<START){return new T.Vector3(s.x+x*Math.cos(s.angle)+z*Math.sin(s.angle),0,-x*Math.sin(s.angle)+z*Math.cos(s.angle));}
  const cx=-10+s.feed+(time>=END?V*(time-END):0),wx=cx+x;return new T.Vector3(wx,-2*clamp((wx-170)/2),z);
 }
 if(time>=END){return new T.Vector3(170+(x-120)+300+V*(time-END),-2,z);}
 const arc=x-120+s.feed,hinge=120+s.x;
 if(arc<=0)return new T.Vector3(hinge+arc*Math.cos(s.a),s.lift-arc*Math.sin(s.a),z);
 const yf=s.lift-arc*Math.sin(s.a),curve=s.lift-(s.lift+2)*ease(arc/30),blend=s.dock;
 return new T.Vector3(hinge+arc*Math.cos(s.a)*(1-blend)+arc*blend,yf*(1-blend)+curve*blend,z);
}

const explanations={fold:{tilt:'1 · Tabla fırına doğru 12° eğiliyor; hamur henüz çekilmiyor.',fold:'2 · Ön uç 120° aşağı ve içeri katlanıyor. Banttan uzakta olduğu için çarpışma önleniyor.',dock:'3 · Tabla 50 mm yaklaşıyor; hamurun ön ucu alt banda oturuyor.',feed:'4 · Alt bant yavaşça çekiyor. Arkada yapışma olmadığı varsayılarak hareket gösteriliyor.',return:'5 · Hamur tamamen bantta; tabla düzleşip başlangıç yerine dönüyor.'},belt:{press:'1 · Pres altında bant ve tabla dönüşü kilitli. Destek plakası yükü taşıyor.',travel:'2 · Bant dönmeden, tüm kaset ray üzerinde topping noktasına ilerliyor.',topping:'3 · Kaset kendi etrafında dönüyor; bant sabit. Malzeme üstüne dağılıyor.',dock:'4 · Dönüş duruyor; kaset fırın girişine hizalanıyor.',feed:'5 · Kasetin bandı çalışıyor; fırınla aynı 6,27 mm/sn hızda aktarıyor.',return:'6 · Hamur tamamen fırında; boş kaset pres noktasına geri dönüyor.'}};
function render(){renderer.render(scene,camera);const w=q('view').clientWidth,h=q('view').clientHeight,phase=state(time).phase;for(const l of labels){const p=l.pos.clone().project(camera);l.e.hidden=(l.context&&l.context!==phase)||p.z>1||p.x<-.95||p.x>.95||p.y<-.95||p.y>.95;if(!l.e.hidden){l.e.style.left=`${Math.max(85,Math.min(w-85,(p.x+1)*w/2))}px`;l.e.style.top=`${Math.max(16,Math.min(h-16,(1-p.y)*h/2))}px`;}}}
function aim(mode){camMode=mode;follow=mode!=='all';const s=state(time),cx=method==='belt'&&follow?s.x+95:method==='belt'?-140:170;controls.target.set(cx,15,0);camera.up.set(0,1,0);
 if(mode==='top'){camera.position.set(cx,1120,.1);camera.up.set(0,0,-1);}else if(mode==='side')camera.position.set(cx,80,1130);else if(mode==='all')camera.position.set(80,1070,1830);else camera.position.set(cx+410,625,950);controls.update();render();}
function update(){const s=state(time);travel.position.x=s.x;
 if(method==='fold'){
  tilt.rotation.z=-s.a;tilt.position.y=s.lift;flap.rotation.z=-s.fold;
  const rearY=s.lift+205*Math.sin(s.a)-8,bot=new T.Vector3(-85,-100,0),end=new T.Vector3(120-205*Math.cos(s.a),rearY,0),v=end.clone().sub(bot);actuator.position.copy(bot).addScaledVector(v,.5);actuator.scale.y=v.length()/91;actuator.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),v.normalize());
  stamp.pos.set(s.x+120,-80,130);
 }else{
  turn.rotation.y=s.angle;head.position.y=95-85*Math.sin(Math.PI*clamp(time/2));lock.position.y=s.phase==='press'?-31:-44;
  feedTicks.forEach((o,i)=>o.position.x=-153+((i*18+s.feed)%312));stamp.pos.set(s.x,-120,190);
  if(follow){const cx=s.x+95,dx=cx-controls.target.x;controls.target.x+=dx;camera.position.x+=dx;controls.update();}
 }
 const pos=dg.attributes.position;for(let i=0;i<base.length;i++){const[x,z,l]=base[i],p=foodPoint(x,z,s);pos.setXYZ(i,p.x,p.y+l*4,p.z);}pos.needsUpdate=true;dg.computeVertexNormals();
 toppings.forEach(({o,x,z},i)=>{o.visible=method==='fold'||time>=4+(i/toppings.length)*2;const p=foodPoint(x,z,s);o.position.copy(p).add(new T.Vector3(0,5.5,0));if(method==='fold'&&time<END&&x-120+s.feed<0)o.rotation.z=-s.a;else o.rotation.z=0;});
 const dist=V*time;ovenTicks.forEach((o,i)=>o.position.x=235+((i*19+dist)%530));insetTicks.forEach((o,i)=>o.position.x=173+((i*9+dist)%56));
 if(lastPhase!==s.phase){q('state').textContent=explanations[method][s.phase];lastPhase=s.phase;}
 const moved=Math.min(TRANSFER,Math.max(0,time-START));q('time').value=String(time);q('elapsed').textContent=`Konum: ${time.toFixed(1)} / ${TOTAL.toFixed(1)} sn · hazırlık / dönüş temsili`;
 q('transfer').textContent=`Hesaplı aktarım: ${moved.toFixed(1)} / ${TRANSFER.toFixed(1)} sn`;
 q('detail').textContent=method==='fold'?`Eğim ${(s.a*180/Math.PI).toFixed(0)}° · uç ${(s.fold*180/Math.PI).toFixed(0)}°`:`Dönüş ${(s.angle*180/Math.PI).toFixed(0)}° · bant ${s.phase==='feed'?V.toFixed(2):'0'} mm/sn`;
 document.body.dataset.phase=s.phase;document.body.dataset.finite=String([...pos.array].every(Number.isFinite));document.body.dataset.feed=s.feed.toFixed(2);render();
}
q('time').max=String(TOTAL);q('play').disabled=false;
function stop(){playing=false;q('play').textContent=time>=TOTAL?'Tekrar oynat':'Oynat';}
function tick(now){if(!playing)return;time=Math.min(TOTAL,time+Math.min(.08,(now-last)/1000)*Number(q('speed').value));last=now;update();if(time>=TOTAL){stop();return;}requestAnimationFrame(tick);}
q('play').onclick=()=>{if(playing){stop();return;}if(time>=TOTAL)time=0;playing=true;last=performance.now();q('play').textContent='Duraklat';requestAnimationFrame(tick);};
q('time').oninput=e=>{time=Number(e.target.value);stop();update();};
q('side').onclick=()=>aim('side');q('iso').onclick=()=>aim('iso');q('top').onclick=()=>aim('top');if(q('all'))q('all').onclick=()=>aim('all');
q('envelope').onchange=e=>{oldRing.visible=e.target.checked;if(sweep)sweep.visible=e.target.checked;render();};
controls.addEventListener('change',render);
new ResizeObserver(()=>{const w=q('view').clientWidth,h=q('view').clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.zoom=Math.min(1,w/630);camera.updateProjectionMatrix();render();}).observe(q('view'));
aim(camMode);stop();update();
}catch(e){q('error').hidden=false;q('error').textContent='3D açılamadı: '+e.message;q('play').textContent='3D yüklenemedi';console.error(e);}
