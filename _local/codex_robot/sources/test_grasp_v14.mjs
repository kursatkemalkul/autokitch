import fs from 'node:fs';import assert from 'node:assert/strict';
import {T,rig,root,read,hits,update,robot,intersects}from './geometry.mjs';
import {environment,obstacles,products,productAt}from './world.mjs';
import {clipGripNotch}from '../../../otonom/hat/robot-main-v1/grip-notch.js';
rig.setRailForward(.5);const data=read('grasp_v14.json');assert.equal(data.results.length,2);
for(const o of obstacles.filter(o=>o.name==='E_KALIP__sac__NEST')){clipGripNotch(T,o.g,o.m);o.bvh=null;update(o,o.m);}
let poses=0;
for(const r of data.results){assert.equal(r.path.length,21);for(const side of ['left_inner_finger','right_inner_finger'])assert(r.contacts.some(n=>n.includes(side)));
 environment(r.key==='Cola'?{CEK_K5_ic1_1:.7}:{},{});productAt(r.key,r.product);
 for(const state of r.path){assert.deepEqual(hits(state,obstacles.filter(o=>!o.name.startsWith('QR_'))),[]);poses++;}
 assert.deepEqual(hits(r.state,obstacles.filter(o=>!o.name.startsWith('QR_'))),[]);
 for(const p of products[r.key].parts)for(const rb of robot.filter(x=>!x.name.includes('Food')&&!x.name.includes('SupportLip')))assert(!intersects(p,rb),'Non-pad product collision');
 const pads=robot.filter(r=>r.name.endsWith('FoodFace_1')),delta=pads[0].box.getCenter(new T.Vector3()).sub(pads[1].box.getCenter(new T.Vector3())).normalize();
 if(r.key==='Box')assert(Math.abs(delta.y)>.99,'Box grip must close vertically');else assert(Math.abs(delta.y)<.01,'Cola grip must close horizontally');
}
const result={passed:true,opening_closing_poses:poses,both_pads_contact:true,box_closing_axis:'vertical',cola_closing_axis:'horizontal',scope:'source gripping geometry only',real_grip_forces:false,corrected_qr_placement_validated:false};fs.writeFileSync(root+'grasp_v14_checks.json',JSON.stringify(result,null,2));console.log(result);
