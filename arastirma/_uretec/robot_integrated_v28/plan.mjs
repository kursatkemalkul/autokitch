import fs from 'node:fs';
import {Rig,point} from '../../../otonom/hat/robot-integrated-v25/rig.js';
const A='otonom/hat3d/robot-integrated-v28/';
const original=JSON.parse(fs.readFileSync('otonom/hat3d/robot-integrated-v25/order_v25.json'));
const rig=new Rig(JSON.parse(fs.readFileSync('otonom/hat3d/robot-integrated-v25/rig.json')),{mountForward:.1,railForward:.5});
const t=original.trajectory,begin=t.findIndex(f=>f.stage==='Kutu · duvardan uzak koridora çek'),end=t.findIndex(f=>f.stage==='Box · ideal tutuş hizası');
const first=structuredClone(t[begin-1]),last=structuredClone(t[end]);
// Same physical wrist angle, without the old accumulating -2pi/-4pi turns.
first.state.q[4]+=2*Math.PI;
const tau=2*Math.PI,nearest=(q,p)=>q.map((x,i)=>x+tau*Math.round((p[i]-x)/tau));
const web=p=>[p[0],p[2],-p[1]],native=p=>[p[0],-p[2],p[1]];
const local=[.000000799220388,-.00000114247412,.1442837412011861];
const m0=rig.tcp(first.state.q,first.state.rail,first.state.jaw),m1=rig.tcp(last.state.q,last.state.rail,last.state.jaw);
const product=f=>web(point(rig.tcp(f.state.q,f.state.rail,f.state.jaw),local));
const smooth=x=>x*x*x*(10+x*(-15+6*x));
function pose(yaw,p){const c=Math.cos(yaw),s=Math.sin(yaw),m=[...m0];for(let k=0;k<3;k++){m[k]=c*m0[k]-s*m0[4+k];m[k+4]=s*m0[k]+c*m0[4+k];}const r=[...m];r[3]=r[7]=r[11]=0;const d=point(r,local),a=native(p);m[3]=a[0]-d[0];m[7]=a[1]-d[1];m[11]=a[2]-d[2];return m;}
let state=structuredClone(first.state),clock=first.time_s,yaw=0,p=product(first),frames=[],stages=[];
function append(name,states,duration){const start=clock;states.forEach((st,i)=>{const f={...structuredClone(first),stage:name,state:st,time_s:start+duration*(i+1)/states.length,carrying:'Box',tcp_cap_m_s:.35};f.product=product(f);frames.push(f);});clock+=duration;state=structuredClone(states.at(-1));p=frames.at(-1).product;stages.push({stage:name,start_s:start,end_s:clock,frames:states.length});}
function linear(name,targetP,targetYaw,targetRail,duration,count=240){const start=structuredClone(state),startP=p,startYaw=yaw,states=[];let seed=[...state.q];for(let i=1;i<=count;i++){const u=smooth(i/count),r=start.rail+(targetRail-start.rail)*u,pp=startP.map((x,k)=>x+(targetP[k]-x)*u),a=startYaw+(targetYaw-startYaw)*u;const solved=rig.solve(pose(a,pp),r,start.jaw,seed);if(!solved.valid)throw Error(name+' IK '+JSON.stringify({i,solved,pp,r}));seed=nearest(solved.q,seed);states.push({q:[...seed],rail:r,jaw:start.jaw});}append(name,states,duration);yaw=targetYaw;}
const pullZ=+(process.argv[2]||'.60');
const pull=rig.solve(pose(0,[p[0],p[1],pullZ]),state.rail,state.jaw,state.q);
if(!pull.valid)throw Error('Withdrawal endpoint unreachable');
const pullQ=nearest(pull.q,state.q),pullStart=structuredClone(state),pullStates=[];
for(let i=1;i<=240;i++){const u=smooth(i/240);pullStates.push({...structuredClone(pullStart),q:pullStart.q.map((x,k)=>x+(pullQ[k]-x)*u)});}
append('Kutu · açık dönüş için yataktan uzaklaştır',pullStates,3.5);
// Turn the shoulder pan with every downstream joint held: the entire arm follows
// one arc, not a fixed TCP spin solved through folded IK configurations.
const turnAngle=+(process.argv[3]||String(Math.PI));
const start=structuredClone(state),rot=[];for(let i=1;i<=720;i++){const u=smooth(i/720),q=[...start.q];q[0]+=turnAngle*u;rot.push({...structuredClone(start),q});}
append('Kutu · ray sabitken açık taraftan dön',rot,7);yaw=turnAngle;
const finalP=web(point(m1,local));
const entryQ=nearest(last.state.q,state.q),entryStart=structuredClone(state),entry=[];
// Resolve the known wrist singularity in joint space on the same elbow branch.
// Both endpoints have q2+q3+q4=0 and q5=q1-pi: interpolation keeps the box level.
const wristClearanceYaw=+(process.argv[4]||'1.15');
for(let i=1;i<=480;i++){const u=smooth(i/480),q=entryStart.q.map((x,k)=>x+(entryQ[k]-x)*u);q[4]-=wristClearanceYaw*Math.sin(Math.PI*u)**2;const ru=1-(1-u)**2;entry.push({q,rail:entryStart.rail+(last.state.rail-entryStart.rail)*ru,jaw:entryStart.jaw});}
append('Kutu · QR girişine ileri taşı',entry,5);
const exact=nearest(last.state.q,state.q),delta=exact.map((x,i)=>x-state.q[i]);
if(Math.max(...delta.map(Math.abs))>.04)throw Error('QR entry branch mismatch '+JSON.stringify(delta));
// Replace numerical IK residual by the accepted entry pose over a gentle blend.
const blendStart=structuredClone(state),blend=[];for(let i=1;i<=3;i++){const u=smooth(i/3);blend.push({...structuredClone(state),q:blendStart.q.map((x,k)=>x+delta[k]*u)});}append('Kutu · QR giriş hizasını koru',blend,.05);
let prefix=t.slice(0,begin).map(f=>{const n=structuredClone(f);n.state.q[4]+=tau;return n;});
let previous=structuredClone(first),retimedClock=first.time_s;
for(const s of stages){const group=frames.filter(f=>f.stage===s.stage),before=structuredClone(previous);let v0=null,stretch=1;
 for(const f of group){const dt=f.time_s-previous.time_s,qv=f.state.q.map((q,i)=>(q-previous.state.q[i])/dt),rv=(f.state.rail-previous.state.rail)/dt,tm=rig.tcp(f.state.q,f.state.rail,f.state.jaw),pm=rig.tcp(previous.state.q,previous.state.rail,previous.state.jaw),tv=[3,7,11].map(k=>(tm[k]-pm[k])/dt);stretch=Math.max(stretch,...qv.map((x,i)=>Math.abs(x)/original.limits.joint_velocity_rad_s[i]),Math.abs(rv)/original.limits.rail_velocity_m_s,Math.hypot(...tv)/.35);if(v0){const h=(dt+v0.dt)/2;stretch=Math.max(stretch,...qv.map((x,i)=>Math.sqrt(Math.abs(x-v0.qv[i])/h/original.limits.joint_acceleration_rad_s2)),Math.sqrt(Math.abs(rv-v0.rv)/h/original.limits.rail_acceleration_m_s2),Math.sqrt(Math.hypot(...tv.map((x,i)=>x-v0.tv[i]))/h/original.limits.tcp_acceleration_m_s2));}v0={dt,qv,rv,tv};previous=structuredClone(f);}
 stretch=Math.max(1,stretch*1.05);const duration=(s.end_s-s.start_s)*stretch;for(const f of group)f.time_s=retimedClock+(f.time_s-s.start_s)*stretch;s.start_s=retimedClock;s.end_s=retimedClock+duration;s.speed_stretch=stretch;retimedClock+=duration;
}
const newEnd=frames.at(-1).time_s,shift=newEnd-t[end].time_s;
let prev=exact;const tail=t.slice(end+1).map(f=>{const n=structuredClone(f);n.time_s+=shift;n.state.q=nearest(n.state.q,prev);prev=n.state.q;return n;});
const out={...original,trajectory:[...prefix,...frames,...tail],phases:[],summary:{...original.summary,version:28,inward_box_turn:true,box_turn:'fixed rail; rigid arm arc through open side',frames:prefix.length+frames.length+tail.length,duration_s:tail.at(-1).time_s}};
fs.mkdirSync(A,{recursive:true});fs.writeFileSync(A+'order_v28.json',JSON.stringify(out));
const proof={version:28,begin_index:begin,end_index:end,old_begin_s:first.time_s,old_end_s:t[end].time_s,new_end_s:newEnd,shift_s:shift,pull_z_m:pullZ,stages,exact_entry_delta_rad:delta,rail_during_turn_m:first.state.rail,rail_backtracking_m:0,turn_shoulder_angle_rad:turnAngle,grasp:'ideal rigid attachment; physics not claimed'};
fs.writeFileSync(A+'turn_plan.json',JSON.stringify(proof,null,2));console.log(JSON.stringify(proof));
