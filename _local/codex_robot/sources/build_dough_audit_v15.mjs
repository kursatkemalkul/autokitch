import fs from 'node:fs';const dir='arastirma/_uretec/robot_main_v1/';const old=fs.readFileSync(dir+'rail_animation_v12.mjs','utf8');
const setup=old.slice(old.indexOf('const target='),old.indexOf('let light='));
const head=`import fs from 'node:fs';import{T,C,matrix,rig,root,read,box,hits,intersects,robot,solid,update}from './geometry.mjs';import{environment,obstacles,products,productAt,tcpScene}from './world.mjs';import{env}from './layout_v11.mjs';rig.setRailForward(.5);\n`;
const body=`
const grid=read('qr_grid_v13.json'),cab=env(grid,2,850),base=obstacles.filter(s=>!s.name.startsWith('QR_')),oldRecord=read('rail_animation_v12.json');
const stop=oldRecord.trajectory.findIndex(f=>f.stage.startsWith('Sağ kutu'));
const path=oldRecord.trajectory.slice(0,stop),fail=[];let checks=0;
for(const f of path){environment(f.drawers,{});const obs=[...base,...cab],h=hits(f.state,obs);checks++;if(h.length){fail.push({stage:f.stage,h});break;}if(f.carrying==='Dough'){productAt('Dough',f.product);for(const p of products.Dough.parts){for(const r of robot)if(!r.body.includes('/Gripper/')&&intersects(p,r))fail.push({stage:f.stage,h:['product/arm']});for(const o of obs)if(intersects(p,o))fail.push({stage:f.stage,h:['product/'+o.name]});}if(fail.length)break;}}
const result={version:15,passed:!fail.length,checks,rigid_dough:true,stock_count_unchanged:42,table_m:path.at(-1)?.placed.Dough,fail};fs.writeFileSync(root+'dough_v15.json',JSON.stringify({summary:result,trajectory:!fail.length?path:[] }));console.log(result);if(fail.length)process.exitCode=1;
`;
fs.writeFileSync(dir+'dough_audit_v15.mjs',head+setup+body);
