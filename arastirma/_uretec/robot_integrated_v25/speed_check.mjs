import fs from 'node:fs';
const A='otonom/hat3d/robot-integrated-v25/';
const order=JSON.parse(fs.readFileSync(A+'order_v25.json'));
let previous=null,velocity=null;
const worst=[];
for(let j=0;j<order.trajectory.length;j++){
 const f=order.trajectory[j];
 if(previous){const dt=f.time_s-previous.time_s,v=f.state.q.map((x,i)=>(x-previous.state.q[i])/dt);
  if(velocity)for(let i=0;i<6;i++){const acc=Math.abs(v[i]-velocity[i])/((dt+velocity.dt)/2);if(acc>2.01)worst.push({j,joint:i,acc,stage:f.stage,previous:previous.stage,dt});}
  v.dt=dt;velocity=v;
 }
 previous=f;
}
console.log(JSON.stringify({limits:order.limits,worst:worst.sort((a,b)=>b.acc-a.acc).slice(0,20)}));
