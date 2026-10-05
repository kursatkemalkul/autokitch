import fs from 'node:fs';
import assert from 'node:assert/strict';
const dir='otonom/hat3d/robot-main-v1/';
const record=JSON.parse(fs.readFileSync(dir+'order_trajectory_v4.json','utf8'));
assert.equal(record.version,4);assert.equal(record.physics,false);assert.equal(record.collision_approved,false);
const frames=record.trajectory;assert.equal(frames.length,record.frames);assert(frames.length>800);
const required=['Dough','Cola','Dessert','Box'];
const angle=x=>Math.atan2(Math.sin(x),Math.cos(x));let maxJointStep=0,maxRailStep=0;
for(let i=0;i<frames.length;i++){
 const f=frames[i],s=f.state;assert.equal(s.q.length,6);assert(s.q.every(x=>Number.isFinite(x)&&Math.abs(x)<=Math.PI+1e-9));assert(s.rail>=1.176-1e-9&&s.rail<=4.86+1e-9);assert(s.jaw>=0&&s.jaw<=45);
 assert(f.offset.every(Number.isFinite));for(const p of Object.values(f.placed))assert(p.length===3&&p.every(Number.isFinite));
 if(i){const a=frames[i-1].state;maxJointStep=Math.max(maxJointStep,...s.q.map((q,k)=>Math.abs(angle(q-a.q[k]))));maxRailStep=Math.max(maxRailStep,Math.abs(s.rail-a.rail));}
}
assert(maxJointStep<.16,'Abrupt joint step');assert(maxRailStep<.12,'Abrupt rail step');
let last=-1;for(const key of required){const first=frames.findIndex(f=>f.carrying===key);assert(first>last,'Wrong order');last=first;assert(frames.some(f=>f.placed[key]),'Missing release');}
const end=frames.at(-1);assert(required.every(k=>end.placed[k]));assert(Object.values(end.drawers).every(x=>x===0));assert.equal(end.qr,0);
assert(Math.abs(end.placed.Dough[0]-1.086)<.001);assert(Math.abs(end.placed.Dough[2]+.17)<.001);
assert(end.placed.Cola[0]>5&&end.placed.Cola[2]>end.placed.Dessert[2]);assert(end.placed.Box[0]<5);
const summary={version:4,storyboard_checks_passed:true,frames:frames.length,max_joint_step_deg:maxJointStep*180/Math.PI,max_rail_step_mm:maxRailStep*1000,items:required,final_positions_m:end.placed,collision_approved:false,recorded_intersection_frames:record.findings.length,physics:false};
fs.writeFileSync(dir+'storyboard_checks.json',JSON.stringify(summary,null,2)+'\n');console.log(JSON.stringify(summary,null,2));
