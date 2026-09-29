import assert from 'node:assert/strict';
import {P,state} from '../../../otonom/hat/denemeler/k-dar/motion.mjs';
let mins={elbowLeft:1e9,elbowBack:1e9,windowZ:1e9,windowY:1e9,cutterToRaisedArm:1e9};
let failures=[];
for(let i=0;i<=4000;i++){
 const s=state(i/200),e=s.elbow;
 assert(Math.abs(Math.hypot(e.x-P.shoulderX,e.z-P.shoulderZ)-P.L1)<1e-6);
 assert(Math.abs(Math.hypot(s.fx-12-e.x,s.fz-e.z)-P.L2)<1e-6);
 mins.elbowLeft=Math.min(mins.elbowLeft,e.x-22-1.5);
 mins.elbowBack=Math.min(mins.elbowBack,e.z-22+828.5);
 if(s.fx>400){
   let u=(400-e.x)/(s.fx-12-e.x),z=e.z+u*(s.fz-e.z);
   if(s.fx-12>400){mins.windowZ=Math.min(mins.windowZ,z-8+372,-24-z-8);mins.windowY=Math.min(mins.windowY,1046+s.lift-8-978,1062-1046-s.lift-8);}
   mins.windowY=Math.min(mins.windowY,999+s.lift-978,1062-1044-s.lift);
   mins.windowZ=Math.min(mins.windowZ,s.fz-130+372,-24-s.fz-130);
 }
 if(s.t>=6.6&&s.t<8.5)mins.cutterToRaisedArm=Math.min(mins.cutterToRaisedArm,1121.5-(1046+s.lift+8));
 // Parked second link stays outside cutter envelope in plan; cutter down phase only.
 if(s.t>=4&&s.t<=6.5){for(let j=0;j<=100;j++){let u=j/100,x=e.x+(s.fx-12-e.x)*u,z=e.z+(s.fz-e.z)*u;if(Math.hypot(x-200,z+170)<166)failures.push('cut-arm');}}
}
for(const [k,v]of Object.entries(mins))if(v<0)failures.push(k+': '+v);
assert.equal(state(10.1).x,660);assert(Math.abs(state(10.4).y-937.6)<1e-6);
assert.equal(P.W/2-P.guard,42);
console.log(JSON.stringify({samples:4001,minimum_mm:mins,failures,scope:'Simplified kinematics only; not full CAD or physical product simulation'},null,2));
assert.equal(failures.length,0);
