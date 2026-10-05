import fs from 'node:fs';
import {T,C,matrix,rig,read,root,robot,update,hits,intersects} from './geometry.mjs';
import {environment,obstacles,products,productAt} from './world.mjs';
import {clipGripNotch,notch} from '../../../otonom/hat/robot-main-v1/grip-notch.js';
const poses=read('poses_v12.json'),grid=read('qr_grid_v13.json');rig.setRailForward(.5);
const F='/World/RailSystem/Gripper/',zero=[0,0,0,0,0,0];
function gap(jaw){const w=rig.matrices(zero,2,jaw);const a=new T.Vector3(.1845,.05596,0).applyMatrix4(matrix(w[F+'left_inner_finger']));const b=new T.Vector3(.1845,-.05596,0).applyMatrix4(matrix(w[F+'right_inner_finger']));return a.distanceTo(b);}
function jawFor(d){let lo=0,hi=45;for(let i=0;i<40;i++){const mid=(lo+hi)/2;if(gap(mid)>d)lo=mid;else hi=mid;}return (lo+hi)/2;}
const results=[];
for(const o of obstacles.filter(o=>o.name==='E_KALIP__sac__NEST')){clipGripNotch(T,o.g,o.m);o.bvh=null;update(o,o.m);}
for(const key of ['Box','Cola']){
 const old=poses[key+'_pick'],pos=[old.product[0][3],old.product[2][3],-old.product[1][3]],jaw=key==='Box'?jawFor(.0445):old.jaw,rotation=key==='Box'?[[1,0,0],[0,0,1],[0,-1,0]]:old.rotation;
 // Box: opposing pads above/below its front edge. Cola: vertical approach and upper-body contact.
 const tcp=key==='Box'?[pos[0],-pos[2]-.145,pos[1]]:[old.tcp[0],old.tcp[1],old.tcp[2]];
 const target=[...rotation[0],tcp[0],...rotation[1],tcp[1],...rotation[2],tcp[2],0,0,0,1];
 environment(key==='Cola'?{CEK_K5_ic1_1:.7}:{},{});productAt(key,pos);
 const seeds=[old.q,...grid.results.flatMap(r=>r.tasks.map(t=>t.state.q)),...Array.from({length:40},(_,i)=>Array.from({length:6},(_,j)=>Math.sin(i*12.9898+j*78.233)*Math.PI))];
 let result=null,last=[];
 outer:for(const rail of [old.rail,pos[0],pos[0]-.15,pos[0]+.15,pos[0]-.3,pos[0]+.3].map(x=>Math.max(1.376069,Math.min(4.86,x))))for(const seed of seeds){
  const ik=rig.solve(target,rail,jaw,seed);if(!ik.valid)continue;
  const state={q:ik.q,rail,jaw};last=hits(state,obstacles.filter(o=>!o.name.startsWith('QR_')));if(last.length)continue;
  const w=rig.matrices(state.q,rail,jaw);for(const a of robot)update(a,C.clone().multiply(matrix(w[a.body])));
  const otherHits=[];for(const a of products[key].parts)for(const b of robot.filter(r=>!r.name.includes('Food')&&!r.name.includes('SupportLip')))if(intersects(a,b))otherHits.push(b.name);
  if(otherHits.length){last=otherHits;continue;}
  const contacts=robot.filter(r=>/FoodFace/.test(r.name)&&products[key].parts.some(p=>intersects(p,r))).map(r=>r.name);
  const padBounds=robot.filter(r=>r.name.endsWith('FoodFace_1')).map(r=>({name:r.name,min:r.box.min.toArray(),max:r.box.max.toArray()}));
  const path=[];let q=state.q;
  for(let i=0;i<=20;i++){const span=key==='Box'?4:2,jj=jaw-span+span*i/20,r=rig.solve(target,rail,jj,q),s={q:r.q,rail,jaw:jj};if(!r.valid){last=['closure IK'];break;}const h=hits(s,obstacles.filter(o=>!o.name.startsWith('QR_')));if(h.length){last=h;break;}path.push(s);q=r.q;}
  if(path.length!==21)continue;
  result={key,state,product:pos,rotation,tcp:rig.tcp(state.q,rail,jaw),jaw_gap_mm:gap(jaw)*1000,contacts,padBounds,ik_position_error_m:ik.position,environment_hits:[],body_product_hits:[],ideal_grasp:true,path};break outer;
 }
 results.push(result||{key,passed:false,last,jaw,tcp});
 fs.writeFileSync(root+'grasp_v14.json',JSON.stringify({version:14,scope:'Two source holding poses only; prior QR paths do not validate the corrected box grasp',results},null,2));
 console.log(JSON.stringify(results.at(-1)));if(!result)process.exit(1);
}
const light=read('light_scene_v12.json');for(const p of light.meshes.filter(p=>p.name==='E_KALIP__sac__NEST')){
 const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p.positions,3));g.setIndex(p.indices);clipGripNotch(T,g,new T.Matrix4().fromArray(p.matrix));
 p.positions=Array.from(g.attributes.position.array);p.indices=Array.from({length:g.attributes.position.count},(_,i)=>i);
}
fs.writeFileSync(root+'light_scene_v14.json',JSON.stringify(light));

