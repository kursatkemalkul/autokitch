import * as T from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
const $=id=>document.getElementById(id),res=await fetch('../../../../_local/codex_k_montaj/source_bending.json');
if(!res.ok)throw Error(`Kaynak sac verisi ${res.status}`);
const data=await res.json(),renderer=new T.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));document.body.append(renderer.domElement);
const scene=new T.Scene();scene.background=new T.Color(0xe9edf2);scene.add(new T.HemisphereLight(0xffffff,0x64748b,2));const sun=new T.DirectionalLight(0xffffff,2);sun.position.set(2,3,4);scene.add(sun);
const camera=new T.PerspectiveCamera(40,1,.001,30),controls=new OrbitControls(camera,renderer.domElement);camera.up.set(0,0,1);
const group=new T.Group();scene.add(group);group.scale.setScalar(.001);
const material=new T.MeshStandardMaterial({color:0xa6b2c1,side:T.DoubleSide,metalness:.4,roughness:.5});let sheet,mesh,clock=0,running=false;
const vec=a=>new T.Vector3(...a),matrix=a=>new T.Matrix4().set(...a.flat());
function child(b,f){
 if(f===0)return matrix(b.flat_child);
 const th=b.angle*f,R=b.BA/th-b.K*sheet.t,A=vec(b.p0).add(new T.Vector3(0,0,b.direction>0?sheet.t+R:-R)),q=new T.Quaternion().setFromAxisAngle(vec(b.axis),th);
 const o=vec(b.out).applyQuaternion(q),n=new T.Vector3(0,0,1).applyQuaternion(q),origin=vec(b.p0).sub(A).applyQuaternion(q).add(A);
 return new T.Matrix4().makeBasis(o,vec(b.edge),n).setPosition(origin);
}
function strip(b,p,f){
 const [s,w,z]=p;if(f===0)return vec(b.p0).addScaledVector(vec(b.out),s).addScaledVector(vec(b.edge),w).add(new T.Vector3(0,0,z));
 const th=b.angle*f,R=b.BA/th-b.K*sheet.t,A=vec(b.p0).add(new T.Vector3(0,0,b.direction>0?sheet.t+R:-R));
 const radial=new T.Vector3(0,0,b.direction>0?-(R+sheet.t-z):R+z).applyAxisAngle(vec(b.axis),th*s/b.BA);
 return A.add(radial).addScaledVector(vec(b.edge),w);
}
function update(){
 const progress=clock*sheet.order.length,states=new Map(sheet.order.map((id,i)=>[id,Math.max(0,Math.min(1,progress-i))])),poses=new Map([[0,new T.Matrix4()]]),bends=new Map();
 for(const b of sheet.bends){poses.set(b.child,poses.get(b.parent).clone().multiply(child(b,states.get(b.number)||0)));bends.set(b.number,b);}
 const pos=mesh.geometry.attributes.position;
 for(let i=0;i<sheet.encoded_vertices.length;i++){
  const r=sheet.encoded_vertices[i];let v;if('panel' in r)v=vec(r.point).applyMatrix4(poses.get(r.panel));else{const b=bends.get(r.bend);v=strip(b,r.point,states.get(b.number)||0).applyMatrix4(poses.get(b.parent));}pos.setXYZ(i,v.x,v.y,v.z);
 }
 pos.needsUpdate=true;mesh.geometry.computeVertexNormals();mesh.geometry.computeBoundingSphere();$('time').value=clock;
 $('status').textContent=`${sheet.name} · ${sheet.order.length} büküm · kaynak bitiş eşlemesi ${sheet.folded_endpoint_max_error_mm.toExponential(2)} mm · takım ve montaj henüz denetlenmedi`;
}
function select(i){sheet=data.sheets[i];if(!sheet.endpoint_passed)throw Error('Eşleşmeyen sac oynatılamaz');group.traverse(o=>o.geometry?.dispose());group.clear();clock=0;running=false;$('play').textContent='Oynat';
 const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(new Float32Array(sheet.vertices.length*3),3));g.setIndex(sheet.triangles.flat());mesh=new T.Mesh(g,material);group.add(mesh);group.position.set(0,0,0);update();scene.updateMatrixWorld(true);
 const box=new T.Box3().setFromObject(group),c=box.getCenter(new T.Vector3()),s=box.getSize(new T.Vector3()),span=Math.max(...s.toArray(),.08);group.position.sub(c);controls.target.set(0,0,0);camera.position.set(span*.7,-span*.9,span*1.6);controls.update();
}
data.sheets.forEach((s,i)=>{if(!s.endpoint_passed)return;$('part').add(new Option(s.name,i));});$('part').onchange=()=>select(Number($('part').value));
$('play').onclick=()=>{if(clock===1)clock=0;running=!running;$('play').textContent=running?'Duraklat':'Oynat';};$('reset').onclick=()=>{clock=0;running=false;$('play').textContent='Oynat';update();};$('time').oninput=()=>{running=false;clock=Number($('time').value);$('play').textContent='Oynat';update();};
function resize(){renderer.setSize(innerWidth,innerHeight);camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();}addEventListener('resize',resize);resize();select(data.sheets.findIndex(s=>s.name==='sol_sac_urun_girisi'));
let previous=performance.now();renderer.setAnimationLoop(now=>{if(running){clock=Math.min(1,clock+Math.min((now-previous)/1000,.1)/Math.max(3,sheet.order.length*3));update();if(clock===1){running=false;$('play').textContent='Tekrar oynat';}}previous=now;controls.update();renderer.render(scene,camera);});
