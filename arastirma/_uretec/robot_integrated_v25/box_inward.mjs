// Keep the accepted pickup/release poses. Turn the held box inside the corridor.
import fs from 'node:fs';
import {Rig,point} from '../../../otonom/hat/robot-integrated-v25/rig.js';
const A='otonom/hat3d/robot-integrated-v25/';
const source=JSON.parse(fs.readFileSync('otonom/hat3d/robot-integrated-v24/order_v16.json'));
const rig=new Rig(JSON.parse(fs.readFileSync(A+'rig.json')),{mountForward:.1,railForward:.5});
const t=source.trajectory;
const begin=t.findIndex(f=>f.stage==='Box · QR girişine taşı');
const end=t.findIndex(f=>f.stage==='Box · ideal tutuş hizası');
const first=t[begin-1],last=t[end];
const m0=rig.tcp(first.state.q,first.state.rail,first.state.jaw);
const m1=rig.tcp(last.state.q,last.state.rail,last.state.jaw);
const toWeb=p=>[p[0],p[2],-p[1]],toIsaac=p=>[p[0],-p[2],p[1]];
const local=[.000000799220388,-.00000114247412,.1442837412011861];
const tau=2*Math.PI,nearest=(q,previous)=>q.map((v,i)=>v+tau*Math.round((previous[i]-v)/tau));
const smooth=x=>x*x*x*(10+x*(-15+6*x));
let state=structuredClone(first.state),clock=first.time_s;
const frames=[],proof=[];
function pose(yaw,p){
 const c=Math.cos(yaw),s=Math.sin(yaw),m=[...m0];
 // Rotation about Isaac +Z = web +Y, preserving the horizontal payload.
 for(let k=0;k<3;k++){m[k]=c*m0[k]-s*m0[4+k];m[4+k]=s*m0[k]+c*m0[4+k];}
 const a=toIsaac(p);
 // point() accepts indexed row-major arrays; zero translation explicitly.
 const r=[...m];r[3]=r[7]=r[11]=0;const d=point(r,local);
 m[3]=a[0]-d[0];m[7]=a[1]-d[1];m[11]=a[2]-d[2];return m;
}
const product0=toWeb(point(m0,local));
let lastP=product0,lastYaw=0;
function segment(name,p,yaw,rail,duration,count){
 const start=structuredClone(state),p0=[...lastP],yaw0=lastYaw,temporary=[];
 let seed=[...state.q],maxPosition=0,maxAngle=0;
 for(let i=1;i<=count;i++){
  const u=smooth(i/count),targetP=p0.map((v,k)=>v+(p[k]-v)*u),angle=yaw0+(yaw-yaw0)*u,r=start.rail+(rail-start.rail)*u,target=pose(angle,targetP);
  const solved=rig.solve(target,r,start.jaw,seed);
  if(!solved.valid)throw Error(name+' IK '+JSON.stringify({i,position:solved.position,angle:solved.angle,p:targetP,rail:r}));
  const q=nearest(solved.q,seed);seed=q;maxPosition=Math.max(maxPosition,solved.position);maxAngle=Math.max(maxAngle,solved.angle);
  const actual=rig.tcp(q,r,start.jaw),product=toWeb(point(actual,local));
  temporary.push({...structuredClone(first),stage:name,state:{q,rail:r,jaw:start.jaw},product,carrying:'Box',time_s:clock+duration*i/count,tcp_cap_m_s:.35});
 }
 // Retiming is checked from actual FK, not a nominal interpolation speed.
 let stretch=1,previous={state:start,product:p0,time_s:clock},lastVelocity=null;
 for(const f of temporary){const dt=f.time_s-previous.time_s;
  const dq=f.state.q.map((q,i)=>(q-previous.state.q[i])/dt),rv=(f.state.rail-previous.state.rail)/dt,pv=f.product.map((x,i)=>(x-previous.product[i])/dt);
  stretch=Math.max(stretch,...dq.map((v,i)=>Math.abs(v)/source.limits.joint_velocity_rad_s[i]),Math.abs(rv)/source.limits.rail_velocity_m_s,Math.hypot(...pv)/.35);
  if(lastVelocity){const h=(dt+lastVelocity.dt)/2;
   stretch=Math.max(stretch,...dq.map((v,i)=>Math.sqrt(Math.abs(v-lastVelocity.dq[i])/h/source.limits.joint_acceleration_rad_s2)),Math.sqrt(Math.abs(rv-lastVelocity.rv)/h/source.limits.rail_acceleration_m_s2),Math.sqrt(Math.hypot(...pv.map((v,i)=>v-lastVelocity.pv[i]))/h/source.limits.tcp_acceleration_m_s2));
  }
  lastVelocity={dq,rv,pv,dt};previous=f;
 }
 stretch=Math.max(1,stretch*1.08);for(const f of temporary)f.time_s=clock+(f.time_s-clock)*stretch;
 frames.push(...temporary);clock+=duration*stretch;state=structuredClone(frames.at(-1).state);lastP=[...p];lastYaw=yaw;
 proof.push({stage:name,frames:count,duration_s:duration*stretch,maximum_ik_position_m:maxPosition,maximum_ik_orientation_deg:maxAngle});
}
// Straight back first; then travel left. The box stays level throughout.
segment('Kutu · duvardan uzak koridora çek',[product0[0],product0[1],.800],0,4.2,3.0,160);
segment('Kutu · rayda sola taşı',[product0[0]-.400,product0[1],.800],0,3.8,2.0,120);
segment('Kutu · koridor içinde dönüş konumuna al',[3.960,product0[1],.920],0,3.8,2.4,140);
segment('Kutu · duvarın ters tarafından yatay dön',[3.960,product0[1],.920],Math.PI,3.8,4.0,360);
// Approach the accepted right-bay pose from the corridor, not the wall side.
const finalP=toWeb(point(m1,local));
segment('Kutu · QR önüne koridordan taşı',[4.350,product0[1],1.35],Math.PI,4.1,3.0,180);
segment('Box · QR girişine taşı',finalP,Math.PI,last.state.rail,3.0,180);
// Native target pose is retained to avoid altering the accepted QR insertion.
const endQ=nearest(last.state.q,state.q),delta=endQ.map((q,i)=>q-state.q[i]);
if(Math.max(...delta.map(Math.abs))>.06)throw Error('Final IK branch differs from accepted insertion: '+JSON.stringify({current:state.q,target:endQ,delta}));
const exact=structuredClone(last);exact.state.q=endQ;exact.time_s=clock+.3;exact.stage='Kutu · QR giriş hizasını koru';frames.push(exact);clock=exact.time_s;
const shift=clock-t[end].time_s;
const tail=t.slice(end).map(f=>({...structuredClone(f),time_s:f.time_s+shift,state:{...f.state,q:nearest(f.state.q,endQ)}}));
// Eliminate the duplicated join timestamp while preserving the native pose.
tail[0].time_s=clock+.001;
source.trajectory=[...t.slice(0,begin),...frames,...tail];
source.phases=[];source.summary={...source.summary,version:25,duration_s:source.trajectory.at(-1).time_s,frames:source.trajectory.length,geometric_audit:'New inward box corridor checked by v25 motion bounds audit; full station collision not certified',inward_box_turn:true};
fs.writeFileSync(A+'order_v25.json',JSON.stringify(source));
fs.writeFileSync(A+'box_turn_audit.json',JSON.stringify({version:25,turn_side:'corridor/left, away from right wall',box_level:true,pickup_preserved:true,release_preserved:true,source:'order_v16.json',original_box_transfer_s:t[end].time_s-first.time_s,new_box_transfer_s:clock-first.time_s,stages:proof,final_joint_difference_rad:delta,passed:true,full_collision_certified:false},null,2));
console.log(JSON.stringify({frames:source.trajectory.length,proof,final_joint_difference_rad:delta}));
