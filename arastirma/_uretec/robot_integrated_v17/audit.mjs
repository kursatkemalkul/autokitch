import fs from 'node:fs';
import {machine,robot,rig,T,C,matrix,update,intersects,read,box} from './geometry.mjs';
rig.setRailForward(.5);
const record=read('order_v16.json'), grid=read('qr_grid_v13.json');
const removed=n=>/^(QR_|ELK_QR|TEZGAH_|DUZ_TEZGAH)/.test(n);
const obstacles=machine.filter(o=>!removed(o.name));
for(const p of grid.parts)obstacles.push(box('QR17_'+p.name,p.min,p.max));
for(const o of obstacles)o.initial=o.m.clone();
const stride=Number(process.argv[2]||30), finds=[], counts=new Map();
console.log('Loaded latest native machine',machine.length,'active meshes',obstacles.length);
const drawerFor={Dough:'CEK_K1_lahm_1',Cola:'CEK_K5_ic1_1',Dessert:'CEK_K6_tatli_1'};
for(let i=0;i<record.trajectory.length;i+=stride){
 const f=record.trajectory[i], w=rig.matrices(f.state.q,f.state.rail,f.state.jaw);
 for(const a of robot)update(a,C.clone().multiply(matrix(w[a.body])));
 for(const b of obstacles){const d=b.name.match(/^(CEK_K\d+_[^_]+_\d+)__/);let m=b.initial.clone();if(d&&b.name.includes('CEKMECE'))m.premultiply(new T.Matrix4().makeTranslation(0,0,(f.drawers[d[1]]||0)*(b.name.includes('CEKMECE_ARA')?.5:1)));update(b,m);}
 for(const a of robot)for(const b of obstacles){
  if(a.body.includes('/Gripper/')&&f.carrying&&b.name.startsWith(drawerFor[f.carrying]+'__')&&/__(?:hamur|kutu_icecek)__/.test(b.name))continue;
  if(intersects(a,b)){const key=a.body.split('/').pop()+' > '+b.name;counts.set(key,(counts.get(key)||0)+1);if(finds.length<80)finds.push({index:i,time_s:f.time_s,stage:f.stage,hit:key});}
 }
 if(i%600===0)console.log('Checked',i,'/',record.trajectory.length,'hits',finds.length);
}
const out={machine:'step55 v9w',stride,sampled_frames:Math.ceil(record.trajectory.length/stride),counts:Object.fromEntries(counts),finds,passed:counts.size===0,scope:'Sampled triangle intersection; stock contact exceptions; static machine rest pose plus drawer stroke. Not continuous collision or physics certification.'};
fs.mkdirSync('otonom/hat3d/robot-integrated-v17',{recursive:true});fs.writeFileSync('otonom/hat3d/robot-integrated-v17/collision_audit.json',JSON.stringify(out,null,2));console.log(JSON.stringify(out,null,2));
