import fs from 'node:fs';
import assert from 'node:assert/strict';
import {root,rig,robot,intersects} from './geometry.mjs';
import {environment,collision,products,productAt,tcpScene} from './world.mjs';
const partial=process.argv.includes('--partial');
const record=JSON.parse(fs.readFileSync(root+(partial?'order_trajectory_v4.partial.json':'order_trajectory_v4.json')));
assert.equal(record.version,4);if(!partial)assert.equal(record.physics,false);
const angle=x=>Math.atan2(Math.sin(x),Math.cos(x)),findings=[];
let maxJoint=0,maxRail=0,maxProduct=0;
for(let i=0;i<record.trajectory.length;i++){
 const f=record.trajectory[i],prev=record.trajectory[i-1];
 environment(f.drawers,f.trays);
 const h=collision(f.state,f.carrying?{key:f.carrying,position:tcpScene(f.state).map((v,k)=>v+f.offset[k]),yaw:f.carried_yaw||0}:{});
 if(h.length)findings.push({frame:i,stage:f.stage,hits:h});
 for(const [key,p] of Object.entries(f.placed)){
  const hits=collision(f.state,{key,position:p,yaw:key==='Box'?f.placed_box_yaw||Math.PI:0,grasp:f.touching===key,robot_ready:true});
  if(hits.length)findings.push({frame:i,stage:f.stage,placed:key,hits});
 }
 const located=Object.keys(f.placed);if(f.carrying)located.push(f.carrying);
 for(let a=0;a<located.length;a++)for(let b=a+1;b<located.length;b++){
  const k=located[a],j=located[b];
  productAt(k,f.placed[k]||tcpScene(f.state).map((v,n)=>v+f.offset[n]),k==='Box'?(f.placed_box_yaw||f.carried_yaw||0):0);
  productAt(j,f.placed[j]||tcpScene(f.state).map((v,n)=>v+f.offset[n]),j==='Box'?(f.placed_box_yaw||f.carried_yaw||0):0);
  if(products[k].parts.some(x=>products[j].parts.some(y=>intersects(x,y))))findings.push({frame:i,hits:[k+' > '+j]});
 }
 if(prev){maxJoint=Math.max(maxJoint,...f.state.q.map((v,k)=>Math.abs(angle(v-prev.state.q[k]))));maxRail=Math.max(maxRail,Math.abs(f.state.rail-prev.state.rail));
  if(f.carrying&&prev.carrying===f.carrying){const a=tcpScene(prev.state).map((v,k)=>v+prev.offset[k]),b=tcpScene(f.state).map((v,k)=>v+f.offset[k]);maxProduct=Math.max(maxProduct,Math.hypot(...b.map((v,k)=>v-a[k])));}}
 if(i%250===0)console.log('AUDIT',i,findings.length);
}
const last=record.trajectory.at(-1),keys=['Dough','Cola','Dessert','Box'];
if(!partial){assert(keys.every(k=>last.placed[k]));assert(Object.values(last.drawers).every(v=>v===0));assert(Object.values(last.trays).every(v=>Math.abs(v)<1e-8));}
assert(maxJoint<.05);assert(maxRail<.02);
const summary={version:4,frames:record.trajectory.length,sampled_collision_frames:new Set(findings.map(f=>f.frame)).size,findings,max_joint_step_deg:maxJoint*180/Math.PI,max_rail_step_mm:maxRail*1000,max_carried_product_step_mm:maxProduct*1000,final_positions_m:last.placed,all_tasks_saved:Object.keys(last.placed),physics:false,continuous_sweep_certified:false};
fs.writeFileSync(root+(partial?'scenario_checks.partial.json':'scenario_checks.json'),JSON.stringify(summary,null,2));console.log(JSON.stringify(summary));
if(findings.length)process.exitCode=1;
