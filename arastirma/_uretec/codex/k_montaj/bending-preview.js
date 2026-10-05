import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
const $=id=>document.getElementById(id);
const response=await fetch('../../../../_local/codex_k_montaj/bending_data.json');
if(!response.ok)throw new Error(`Sac verisi yüklenemedi: ${response.status}`);
const D=await response.json();
const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));document.body.append(renderer.domElement);
const scene=new THREE.Scene();scene.background=new THREE.Color(0xe9edf2);
scene.add(new THREE.HemisphereLight(0xffffff,0x64748b,2));
const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(2,3,4);scene.add(light);
const camera=new THREE.PerspectiveCamera(40,1,.001,30),controls=new OrbitControls(camera,renderer.domElement);
const group=new THREE.Group();scene.add(group);
const neutral=new THREE.MeshStandardMaterial({color:0xa6b2c1,metalness:.4,roughness:.5,side:THREE.DoubleSide});
const active=new THREE.MeshStandardMaterial({color:0xf28c28,metalness:.2,roughness:.5,side:THREE.DoubleSide});
let sheet,panels=[],strips=[],clock=0,running=false;
const vec=a=>new THREE.Vector3(...a);
function matrix(rows){return new THREE.Matrix4().set(...rows.flat());}
function mesh(data){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(data.vertices.flat(),3));g.setIndex(data.triangles.flat());g.computeVertexNormals();return new THREE.Mesh(g,neutral);}
function child(b,f){
 if(f===0)return matrix(b.flat_child);
 const theta=b.angle*f,R=b.BA/theta-b.K*sheet.t,p=vec(b.p0),A=p.clone().add(new THREE.Vector3(0,0,b.direction>0?sheet.t+R:-R));
 const q=new THREE.Quaternion().setFromAxisAngle(vec(b.axis),theta);
 const out=vec(b.out).applyQuaternion(q),edge=vec(b.edge),normal=new THREE.Vector3(0,0,1).applyQuaternion(q);
 const origin=p.sub(A).applyQuaternion(q).add(A);
 return new THREE.Matrix4().makeBasis(out,edge,normal).setPosition(origin);
}
function stripPoint(b,s,w,z,f){
 const p=vec(b.p0),edge=vec(b.edge);
 if(f===0)return p.addScaledVector(vec(b.out),s).addScaledVector(edge,w).add(new THREE.Vector3(0,0,z));
 const th=b.angle*f,R=b.BA/th-b.K*sheet.t;
 const A=p.add(new THREE.Vector3(0,0,b.direction>0?sheet.t+R:-R));
 const radial=new THREE.Vector3(0,0,b.direction>0?-(R+sheet.t-z):R+z);
 radial.applyAxisAngle(vec(b.axis),th*s/b.BA);
 return A.add(radial).addScaledVector(edge,w);
}
function update(){
 const count=sheet.order.length,stage=clock*count,states=new Map();
 sheet.order.forEach((id,i)=>states.set(id,Math.min(1,Math.max(0,stage-i))));
 const transforms=new Map([[0,new THREE.Matrix4()]]);
 for(const b of sheet.bends)transforms.set(b.child,transforms.get(b.parent).clone().multiply(child(b,states.get(b.number)||0)));
 for(const p of panels){p.mesh.matrixAutoUpdate=false;p.mesh.matrix.copy(transforms.get(p.number));}
 for(const p of strips){
  const f=states.get(p.b.number)||0,position=p.mesh.geometry.attributes.position;
  for(let i=0;i<p.base.length;i++){const v=stripPoint(p.b,...p.base[i],f);position.setXYZ(i,v.x,v.y,v.z);}
  position.needsUpdate=true;p.mesh.geometry.computeVertexNormals();p.mesh.geometry.computeBoundingSphere();
  p.mesh.matrixAutoUpdate=false;p.mesh.matrix.copy(transforms.get(p.b.parent));p.mesh.material=f>0&&f<1?active:neutral;
 }
 $('time').value=clock;
 $('status').textContent=count===0?'Düz sac; büküm yok.':clock===1?'Bükümler tamamlandı. Bağlantı/PEM montajı henüz yok.':`Büküm ${Math.min(count,Math.floor(stage)+1)} / ${count} · yalnız sac geometrisi; takım/destek henüz gösterilmiyor`;
}
function select(i){
 $('part').value=String(i);
 group.traverse(o=>o.geometry?.dispose());group.clear();panels=[];strips=[];sheet=D.sheets[i];clock=0;running=false;
 for(const p of sheet.panels){const m=mesh(p.mesh);group.add(m);panels.push({number:p.number,mesh:m});}
 for(const b of sheet.bends)for(const data of b.strips){const m=mesh(data);group.add(m);strips.push({b,base:data.vertices,mesh:m});}
 group.scale.setScalar(.001);group.position.set(0,0,0);update();scene.updateMatrixWorld(true);
 const box=new THREE.Box3().setFromObject(group),center=box.getCenter(new THREE.Vector3()),size=box.getSize(new THREE.Vector3()),span=Math.max(...size.toArray(),.08);
 group.position.sub(center);controls.target.set(0,0,0);camera.position.set(span*.7,-span*.9,span*1.6);camera.up.set(0,0,1);controls.update();$('play').textContent='Oynat';
}
D.sheets.forEach((s,i)=>$('part').add(new Option(s.name,i)));
$('part').onchange=()=>select(Number($('part').value));
$('play').onclick=()=>{if(clock===1)clock=0;running=!running;$('play').textContent=running?'Duraklat':'Oynat';};
$('reset').onclick=()=>{clock=0;running=false;$('play').textContent='Oynat';update();};
$('time').oninput=()=>{running=false;clock=Number($('time').value);$('play').textContent='Oynat';update();};
function resize(){renderer.setSize(innerWidth,innerHeight);camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();}addEventListener('resize',resize);resize();select(D.sheets.findIndex(s=>s.name==='sol_sac_urun_girisi'));
let previous=performance.now();
renderer.setAnimationLoop(now=>{if(running){clock=Math.min(1,clock+Math.min((now-previous)/1000,.1)/Math.max(3,sheet.order.length*3));update();if(clock===1){running=false;$('play').textContent='Tekrar oynat';}}previous=now;controls.update();renderer.render(scene,camera);});
