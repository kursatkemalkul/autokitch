import fs from 'node:fs';
import {rig,root,poses}from './geometry.mjs';
const path=root+'order_trajectory_v4.json',r=JSON.parse(fs.readFileSync(path));
if(r.grasp_refined)throw Error('Already refined');
const begin=r.trajectory.findIndex(f=>f.stage==='Tatlı · kaynağın önüne git'),end=r.trajectory.findIndex(f=>f.carrying==='Dessert'),closed=poses.Dessert_pick.jaw,oldOpen=closed-1,startJaw=r.trajectory[begin-1].state.jaw;
const changed=[];
for(let i=begin;i<end;i++){
 const f=r.trajectory[i],a=f.state,old=rig.tcp(a.q,a.rail,a.jaw);
 let jaw;if(f.stage==='Tatlı · kavra')jaw=closed-3+3*(a.jaw-oldOpen);else jaw=a.jaw-2*Math.max(0,Math.min(1,(startJaw-a.jaw)/(startJaw-oldOpen)));
 const q=rig.solve(old,a.rail,jaw,a.q);if(!q.valid)throw Error('Opening IK '+i);
 f.state={q:q.q.map(v=>Math.atan2(Math.sin(v),Math.cos(v))),rail:a.rail,jaw};changed.push(i);
}
for(let i=0;i<r.trajectory.length;i++){
 const f=r.trajectory[i];if(f.stage!=='Pide kutusu · yaklaş'||f.carrying)continue;
 const m=rig.tcp(f.state.q,f.state.rail,f.state.jaw),p=poses.Box_pick.tcp;
 if(Math.hypot(m[3]-p[0],m[7]-p[1],m[11]-(p[2]+.012))<=.0401){f.touching='Box';f.ideal_target_contact='box front lip; final 40mm of approach';changed.push(i);}
}
r.grasp_refined={dessert_opening_deg:closed-3,box_ideal_contact_distance_mm:40,changed_frames:changed};fs.writeFileSync(path,JSON.stringify(r));console.log('REFINED',changed.length);
