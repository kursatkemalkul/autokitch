import fs from 'node:fs';
import * as T from '../robot_integrated_v22/vendor/three.mjs';
import {Rig} from '../../../otonom/hat/robot-integrated-v25/rig.js';
const A='otonom/hat3d/robot-integrated-v25/';
const rigData=JSON.parse(fs.readFileSync(A+'rig.json')),rig=new Rig(rigData,{mountForward:.1,railForward:.5});
const raw=fs.readFileSync(A+'ur10e_short.glb'),len=raw.readUInt32LE(12),g=JSON.parse(raw.subarray(20,20+len));
const corners=(lo,hi)=>[0,1,2,3,4,5,6,7].map(i=>new T.Vector3(i&1?hi[0]:lo[0],i&2?hi[1]:lo[1],i&4?hi[2]:lo[2]));
const mat=n=>n.matrix?new T.Matrix4().fromArray(n.matrix):new T.Matrix4().compose(new T.Vector3(...(n.translation||[0,0,0])),new T.Quaternion(...(n.rotation||[0,0,0,1])),new T.Vector3(...(n.scale||[1,1,1])));
function descend(id,m){const n=g.nodes[id],out=[];for(const p of n.mesh!=null?g.meshes[n.mesh].primitives:[]){const a=g.accessors[p.attributes.POSITION];out.push(...corners(a.min,a.max).map(v=>v.applyMatrix4(m)));}for(const c of n.children||[])out.push(...descend(c,m.clone().multiply(mat(g.nodes[c]))));return out;}
const bodies=Object.fromEntries(Object.entries(rigData.body_nodes).filter(([b])=>!b.endsWith('/RailBase')&&!b.endsWith('/Carriage')).map(([b,n])=>[b,descend(g.nodes.findIndex(x=>x.name===n),new T.Matrix4())]));
const C=new T.Matrix4().makeRotationX(-Math.PI/2),record=JSON.parse(fs.readFileSync(A+'order_v25.json'));
const payloadSizes={Dough:[.095,.075,.095],Cola:[.066,.115,.066],Dessert:[.095,.060,.095],Box:[.320,.045,.320]};
let maximum=-Infinity,panel=-Infinity,boxMax=-Infinity,leftColumnClear=Infinity,boxMachineClear=Infinity;
const byStage={},modified=new Set(record.trajectory.filter(f=>/Kutu · (duvardan|rayda|koridor içinde|duvarın|QR önüne)|Box · QR girişine taşı/.test(f.stage)).map(f=>f.stage));
function observe(p,stage,isBox=false){const lo=[0,1,2].map(k=>Math.min(...p.map(v=>v.getComponent(k)))),hi=[0,1,2].map(k=>Math.max(...p.map(v=>v.getComponent(k))));maximum=Math.max(maximum,hi[0]);if(isBox)boxMax=Math.max(boxMax,hi[0]);if(hi[1]>=1&&lo[1]<=1.7&&hi[2]>=.66&&lo[2]<=1.26)panel=Math.max(panel,hi[0]);
 const s=byStage[stage]??={min:[Infinity,Infinity,Infinity],max:[-Infinity,-Infinity,-Infinity]};for(let k=0;k<3;k++){s.min[k]=Math.min(s.min[k],lo[k]);s.max[k]=Math.max(s.max[k],hi[k]);}
 if(hi[1]>=0&&lo[1]<=2.05&&hi[2]>=1.75&&lo[2]<=2.083){const gap=Math.max(3.597-hi[0],lo[0]-3.757);leftColumnClear=Math.min(leftColumnClear,gap);}
 if(isBox&&modified.has(stage)){const gap=lo[2]-.079;boxMachineClear=Math.min(boxMachineClear,gap);}
}
let speeds=Array(6).fill(0),accels=Array(6).fill(0),tcpSpeed=0,railSpeed=0,lastV=null,previous=null,maxStep=0;
for(const f of record.trajectory){const w=rig.matrices(f.state.q,f.state.rail,f.state.jaw);for(const [body,pts]of Object.entries(bodies)){const m=C.clone().multiply(new T.Matrix4().set(...w[body]));observe(pts.map(v=>v.clone().applyMatrix4(m)),f.stage);}
 if(f.carrying&&f.product){const s=payloadSizes[f.carrying],tcp=C.clone().multiply(new T.Matrix4().set(...rig.tcp(f.state.q,f.state.rail,f.state.jaw))),yaw=f.carrying==='Box'?Math.atan2(tcp.elements[8],tcp.elements[10]):0,m=new T.Matrix4().makeRotationY(yaw).setPosition(...f.product);observe(corners(s.map(x=>-x/2),s.map(x=>x/2)).map(v=>v.applyMatrix4(m)),f.stage,f.carrying==='Box');}
 if(previous){const dt=f.time_s-previous.time_s,v=f.state.q.map((x,k)=>(x-previous.state.q[k])/dt);for(let k=0;k<6;k++){speeds[k]=Math.max(speeds[k],Math.abs(v[k]));if(lastV)accels[k]=Math.max(accels[k],Math.abs(v[k]-lastV[k])/((dt+lastV.dt)/2));}lastV=v;lastV.dt=dt;railSpeed=Math.max(railSpeed,Math.abs(f.state.rail-previous.state.rail)/dt);const tcp0=rig.tcp(previous.state.q,previous.state.rail,previous.state.jaw),tcp1=rig.tcp(f.state.q,f.state.rail,f.state.jaw),d=Math.hypot(...[3,7,11].map(i=>tcp1[i]-tcp0[i]));tcpSpeed=Math.max(tcpSpeed,d/dt);maxStep=Math.max(maxStep,d);}previous=f;
}
const wall=Math.ceil(Math.max(5.23+.05,maximum+.05,panel+.064+.05)*100)/100;
const errors=[];if(leftColumnClear<0)errors.push('Left QR column intersects a conservative moving-body bound');if(boxMachineClear<.01)errors.push('New box route enters unchanged machine front envelope');
if(accels.some(v=>v>record.limits.joint_acceleration_rad_s2*1.001))errors.push('Recorded joint acceleration exceeds configured trial limit');
if(speeds.some((v,i)=>v>record.limits.joint_velocity_rad_s[i]*1.001)||railSpeed>record.limits.rail_velocity_m_s*1.001||tcpSpeed>record.limits.tcp_operating_cap_m_s*1.001)errors.push('Recorded velocity exceeds configured operating limit');
const report={version:25,method:'Native rigid-body FK and transformed conservative mesh bounds at every frame; payload yaw included',frames:record.trajectory.length,robot_product_maximum_x_m:maximum,box_maximum_x_m:boxMax,panel_band_robot_or_product_maximum_x_m:panel,right_wall_inner_x_m:wall,wall_clearance_m:wall-maximum,panel_clearance_m:wall-.064-panel,new_qr_column_bounds:[[3.597,0,1.75],[3.757,2.05,2.083]],qr_column_clearance_m:leftColumnClear,box_front_machine_clearance_m:boxMachineClear,speed:{max_joint_rad_s:speeds,max_joint_acc_rad_s2:accels,max_tcp_m_s:tcpSpeed,max_rail_m_s:railSpeed,max_tcp_sample_step_m:maxStep},stage_bounds:byStage,passed:!errors.length,errors,full_path_collision_certified:false};
fs.writeFileSync(A+'layout_scan.json',JSON.stringify(report,null,2));console.log(JSON.stringify({...report,stage_bounds:undefined}));
if(errors.length)process.exitCode=1;
