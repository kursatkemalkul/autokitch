import fs from 'node:fs';
import {Rig,inv,point} from '../../../otonom/hat/robot-main-v1/rig.js';
const root='otonom/hat3d/robot-main-v1/',ui='otonom/hat/robot-main-v1/';
const read=n=>JSON.parse(fs.readFileSync(root+n));
const rig=new Rig(read('rig.json'),{mountForward:.10,railForward:.5});
const original=read('order_v15.json'),clone=structuredClone;
const sourceURL='https://www.universal-robots.com/media/1807466/ur10e_e-series_datasheets_web.pdf';
const limits={joint_velocity_rad_s:[120,120,180,180,180,180].map(x=>x*Math.PI/180),tcp_hardware_max_m_s:4,
 tcp_operating_cap_m_s:1,tcp_near_product_m_s:.12,joint_acceleration_rad_s2:2,
 tcp_acceleration_m_s2:1,rail_velocity_m_s:.5,rail_acceleration_m_s2:.6,jaw_velocity_deg_s:45,
 drawer_velocity_m_s:.19,drawer_acceleration_m_s2:.633,
 sources:{joint_speed:sourceURL,tcp_speed:sourceURL},
 assumptions:['1 m/s working TCP cap; 4 m/s datasheet ceiling is not attainable at every pose.',
 'Joint/TCP accelerations, rail and gripper limits are configured trial values, not manufacturer certification.',
 'Speed limits depend on hardware revision, payload, safety settings and controller; Isaac must revalidate dynamics.']};
const ease=t=>t*t*t*(10+t*(-15+6*t));
function inverseEase(x){if(x===0||x===1)return x;let lo=0,hi=1;for(let k=0;k<45;k++){let m=(lo+hi)/2;if(ease(m)<x)lo=m;else hi=m;}return (lo+hi)/2;}
const angle=x=>Math.atan2(Math.sin(x),Math.cos(x));
for(let i=1;i<original.trajectory.length;i++)for(let j=0;j<6;j++){const a=original.trajectory[i-1].state.q[j];original.trajectory[i].state.q[j]=a+angle(original.trajectory[i].state.q[j]-a);}
const scalarSlope=(a,b)=>a*b<=0?0:2*a*b/(a+b);
function curve(v,x){const k=Math.min(v.length-2,Math.floor(x)),t=x-k,d=v[k+1]-v[k],m0=k===0?0:scalarSlope(v[k]-v[k-1],d),m1=k+1===v.length-1?0:scalarSlope(d,v[k+2]-v[k+1]);return (2*t**3-3*t*t+1)*v[k]+(t**3-2*t*t+t)*m0+(-2*t**3+3*t*t)*v[k+1]+(t**3-t*t)*m1;}
function columns(frames){const q=Array.from({length:6},(_,j)=>{const a=[frames[0].state.q[j]];for(let i=1;i<frames.length;i++)a.push(a.at(-1)+angle(frames[i].state.q[j]-frames[i-1].state.q[j]));return a;});return [...q,frames.map(f=>f.state.rail),frames.map(f=>f.state.jaw)];}
const vec=s=>[...s.q,s.rail,s.jaw];
const tcp=s=>{let m=rig.tcp(s.q,s.rail,s.jaw);return [m[3],m[11],-m[7]];};
function ratios(frames,cap){let speed=0,acc=0,maxQ=Array(6).fill(0),maxA=Array(6).fill(0),maxTCP=0,maxRail=0;let lastV=null,lastDT=null;
 for(let i=1;i<frames.length;i++){let a=frames[i-1],b=frames[i],dt=b.time_s-a.time_s,v=vec(b.state).map((x,j)=>(x-vec(a.state)[j])/dt),pa=tcp(a.state),pb=tcp(b.state),tv=pb.map((x,j)=>(x-pa[j])/dt),drawerKeys=[...new Set([...Object.keys(a.drawers),...Object.keys(b.drawers)])];
  for(let j=0;j<6;j++){maxQ[j]=Math.max(maxQ[j],Math.abs(v[j]));speed=Math.max(speed,Math.abs(v[j])/limits.joint_velocity_rad_s[j]);}
  maxTCP=Math.max(maxTCP,Math.hypot(...tv));maxRail=Math.max(maxRail,Math.abs(v[6]));speed=Math.max(speed,Math.hypot(...tv)/cap,Math.abs(v[6])/limits.rail_velocity_m_s,Math.abs(v[7])/limits.jaw_velocity_deg_s);
  for(let k of drawerKeys)speed=Math.max(speed,Math.abs((b.drawers[k]||0)-(a.drawers[k]||0))/dt/limits.drawer_velocity_m_s);
  if(lastV){const h=(dt+lastDT)/2;for(let j=0;j<6;j++){maxA[j]=Math.max(maxA[j],Math.abs(v[j]-lastV[j])/h);acc=Math.max(acc,Math.abs(v[j]-lastV[j])/h/limits.joint_acceleration_rad_s2);}acc=Math.max(acc,Math.abs(v[6]-lastV[6])/h/limits.rail_acceleration_m_s2,Math.hypot(...tv.map((x,j)=>x-lastV[8+j]))/h/limits.tcp_acceleration_m_s2);
   for(let k of drawerKeys)acc=Math.max(acc,Math.abs(((b.drawers[k]||0)-(a.drawers[k]||0))/dt-(lastV.drawers[k]||0))/h/limits.drawer_acceleration_m_s2);
  }v.push(...tv);v.drawers=Object.fromEntries(drawerKeys.map(k=>[k,((b.drawers[k]||0)-(a.drawers[k]||0))/dt]));lastV=v;lastDT=dt;
 }return {speed,acc,max_joint_speed_rad_s:maxQ,max_joint_accel_rad_s2:maxA,max_tcp_speed_m_s:maxTCP,max_rail_speed_m_s:maxRail};}
const groups=[];for(let i=1;i<original.trajectory.length;i++){const f=original.trajectory[i];if(!groups.length||groups.at(-1).stage!==f.stage)groups.push({stage:f.stage,start:i-1,end:i});else groups.at(-1).end=i;}
let trajectory=[{...clone(original.trajectory[0]),time_s:0}],phases=[],now=0;
for(const g of groups){const src=original.trajectory.slice(g.start,g.end+1),cols=columns(src),n=src.length-1,out=[];
 for(let j=0;j<=n*4;j++){const x=j/4,i=Math.min(n-1,Math.floor(x)),t=x-i,a=src[i],b=src[i+1],state={q:cols.slice(0,6).map(v=>curve(v,x)),rail:curve(cols[6],x),jaw:curve(cols[7],x)},f=clone(t===1?b:a);f.state=state;f.stage=g.stage;f.time_s=inverseEase(x/n);
  f.drawers=Object.fromEntries([...new Set([...Object.keys(a.drawers),...Object.keys(b.drawers)])].map(k=>[k,(a.drawers[k]||0)+t*((b.drawers[k]||0)-(a.drawers[k]||0))]));
  if(a.carrying&&a.carrying===b.carrying&&a.product&&b.product){const toIsaac=p=>[p[0],-p[2],p[1]],la=point(inv(rig.tcp(a.state.q,a.state.rail,a.state.jaw)),toIsaac(a.product)),lb=point(inv(rig.tcp(b.state.q,b.state.rail,b.state.jaw)),toIsaac(b.product)),p=point(rig.tcp(state.q,state.rail,state.jaw),la.map((v,k)=>v+t*(lb[k]-v)));f.product=[p[0],p[2],-p[1]];}
  for(const k of Object.keys(f.placed))if(a.placed[k]&&b.placed[k])f.placed[k]=a.placed[k].map((v,k2)=>v+t*(b.placed[k][k2]-v));out.push(f);
 }
 const near=/yaklaş|kavra|kaldır|uzaklaş|hedefe|geri çek|yerleştir|pedleri|kenara|yataktan|parmakları/.test(g.stage),spatial=/yaklaş|geri çek|uzaklaş/.test(g.stage),cap=near&&!spatial?limits.tcp_near_product_m_s:limits.tcp_operating_cap_m_s,r=ratios(out,cap); const endTCP=tcp(/geri çek|uzaklaş/.test(g.stage)?out[0].state:out.at(-1).state),localCaps=out.map(f=>near&&( !spatial || Math.hypot(...tcp(f.state).map((x,k)=>x-endTCP[k]))<.18)?limits.tcp_near_product_m_s:limits.tcp_operating_cap_m_s);for(let i=0;i<out.length;i++)out[i].tcp_cap_m_s=localCaps[i];
 // Local timing: a sharp bend slows only its neighbourhood, not the entire transfer.
 const values=out.map(f=>[...vec(f.state),...tcp(f.state),...Object.keys(out[0].drawers).map(k=>f.drawers[k]||0)]),vmax=[...limits.joint_velocity_rad_s,limits.rail_velocity_m_s,limits.jaw_velocity_deg_s,cap,cap,cap,...Object.keys(out[0].drawers).map(()=>limits.drawer_velocity_m_s)],amax=[...Array(6).fill(limits.joint_acceleration_rad_s2),limits.rail_acceleration_m_s2,90,...Array(3).fill(limits.tcp_acceleration_m_s2),...Object.keys(out[0].drawers).map(()=>limits.drawer_acceleration_m_s2)];
 const ds=values.slice(1).map((v,i)=>Math.max(1e-7,Math.hypot(...v.map((x,k)=>(x-values[i][k])/(k>=8&&k<=10?Math.min(localCaps[i],localCaps[i+1]):vmax[k]))))),dirs=values.slice(1).map((v,i)=>v.map((x,k)=>(x-values[i][k])/ds[i])),velocity=out.map(()=>1),accel=out.map(()=>1);
 for(let i=0;i<out.length;i++){const left=dirs[Math.max(0,i-1)],right=dirs[Math.min(dirs.length-1,i)],h=(ds[Math.max(0,i-1)]+ds[Math.min(ds.length-1,i)])/2;for(let k=0;k<left.length;k++){const d=Math.max(Math.abs(left[k]),Math.abs(right[k])),curvature=Math.abs(right[k]-left[k])/h;if(d>1e-10)accel[i]=Math.min(accel[i],.35*amax[k]/d);if(curvature>1e-10)velocity[i]=Math.min(velocity[i],Math.sqrt(.35*amax[k]/curvature));}}
 velocity[0]=velocity[velocity.length-1]=0;
 for(let i=1;i<velocity.length;i++)velocity[i]=Math.min(velocity[i],Math.sqrt(velocity[i-1]**2+2*Math.min(accel[i],accel[i-1])*ds[i-1]));
 for(let i=velocity.length-2;i>=0;i--)velocity[i]=Math.min(velocity[i],Math.sqrt(velocity[i+1]**2+2*Math.min(accel[i],accel[i+1])*ds[i]));
 const dt=ds.map((d,i)=>Math.max(.001,2*d/Math.max(1e-9,velocity[i]+velocity[i+1])));
 let duration=dt.reduce((a,b)=>a+b,0),minimum=/çekmece.*(aç|kapat)/.test(g.stage)?3.97:/kavra|pedleri kapat|bırak$|parmakları aç/.test(g.stage)?.5:.15;if(duration<minimum){const f=minimum/duration;for(let i=0;i<dt.length;i++)dt[i]*=f;duration=minimum;}
 if(/çekmece.*(aç|kapat)/.test(g.stage)){const key=Object.keys(out[0].drawers).find(k=>Math.abs(out.at(-1).drawers[k]-out[0].drawers[k])>.1);if(key){const L=.7,v=.19,a=.633,ramp=v/a,T=L/v+ramp,d=v*v/(2*a),x0=out[0].drawers[key],inverse=x=>x<d?Math.sqrt(2*x/a):x>L-d?T-Math.sqrt(2*(L-x)/a):ramp+(x-d)/v;const times=out.map(f=>inverse(Math.min(L,Math.abs(f.drawers[key]-x0))));for(let i=0;i<dt.length;i++)dt[i]=times[i+1]-times[i];duration=T;}}
 out[0].time_s=now;for(let i=1;i<out.length;i++)out[i].time_s=out[i-1].time_s+dt[i-1];
 const start=trajectory.length-1;trajectory.push(...out.slice(1));phases.push({...g,frame_start:start,frame_end:trajectory.length-1,start_s:now,duration_s:duration,tcp_cap_m_s:cap,measurement:ratios(out,cap)});now+=duration;
}
// Final margin reconciles phase-boundary derivatives.
let overall=ratios(trajectory,1);const margin=Math.max(1,overall.speed*1.08,Math.sqrt(overall.acc/.85));
if(margin>1)for(const f of trajectory)f.time_s*=margin;now=trajectory.at(-1).time_s;
for(const p of phases){p.start_s=trajectory[p.frame_start].time_s;p.duration_s=trajectory[p.frame_end].time_s-p.start_s;p.measurement=ratios(trajectory.slice(p.frame_start,p.frame_end+1),p.tcp_cap_m_s);}
overall=ratios(trajectory,1);if(overall.speed>1.001||overall.acc>1.001)throw Error('Timing exceeds limits '+JSON.stringify({now,...overall}));
fs.writeFileSync(root+'order_v16.json',JSON.stringify({summary:{...original.summary,version:16,frames:trajectory.length,duration_s:now,geometric_audit:'pending cubic interpolation recheck',speed_audit:overall,ideal_grasp:true},limits,phases,trajectory}));
const machine=JSON.parse(fs.readFileSync('otonom/hat3d/v3/durum.json')),recipes=machine.siparis.map(s=>({id:s.kod,name:s.ad,source:'hat3_v7 durum.json',units:s.kod==='lahmacun'?2:1,events:s.adim.map(a=>({name:a.ad,time_s:a.t})),processing_after_dough_s:s.adim.find(a=>a.ad==='ROBOT → QR').t-s.adim.find(a=>a.ad.startsWith('AÇICI')).t,ready:'modelled',motion_certified:false}));
recipes.push(...[{id:'patatesli',name:'Patatesli pide'},{id:'tavuklu',name:'Tavuklu pide'}].map(r=>({...r,source:'Kemal request / Claude menu7 pending',units:1,events:[],processing_after_dough_s:null,ready:'requires machine.ready event',motion_certified:false})));
fs.writeFileSync(root+'workflow_v16.json',JSON.stringify({version:16,recipes,limits,phase_schema:{coordinate_frame:'Isaac right-handed Z-up metres; web maps (x,y,z) to (x,z,-y)',joint_order:read('rig.json').arm_joints,joint_units:'radians',rail_units:'metres',gripper_units:'degrees',payloads:'rigid ideal grip in web only',checkpoints:['drawer.opened','grasp.confirmed','table.robot_clear','machine.box_ready','qr.robot_clear','order.complete'],isaac_policy:'Follow time-stamped q and rail targets through articulation drives; synchronize sensor events. Rework contact grasp/release separately. Never overwrite rigid-body transforms to claim physical success.'},targets:{table:original.summary.final_positions_m.Dough,qr:{column:2,floor_mm:850,products:original.summary.final_positions_m},machine_frame:'unchanged v15; future mounting transform supplied by integration adapter'},known_limitations:['Single order motion checked at QR right850 only; demand simulation is separate and not a 12-bay trajectory certificate.','Two-lahmacun second dough pickup and bridge need native path validation.','New patates/tavuk recipes await real machine completion signal.']},null,2));
// Keep the archived arrival generator verbatim, not its obsolete robot/oven geometry.
const archive='arastirma/_uretec/robot_main_v1/demand_source_28sep.js',text=fs.readFileSync(archive,'utf8'),chunk=text.slice(text.indexOf('function rng('),text.indexOf('/* ---------- hat yerleşimi'));
fs.writeFileSync(ui+'demand-v16.js',chunk+'\nexport {scenarioOrders,SEN};\nexport const defaultDemand={lahm:true,lahmPct:65,seed:1,gapSec:90,randArr:true};\n');
// Archived demand source is tracked locally for reproducible builds.
console.log(JSON.stringify({duration_s:now,frames:trajectory.length,speed:overall,phases:phases.map(p=>({stage:p.stage,s:p.duration_s}))}));
