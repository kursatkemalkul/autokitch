import fs from 'node:fs';
const dir='arastirma/_uretec/robot_main_v1/';
let old=fs.readFileSync(dir+'rail_animation_v12.mjs','utf8');
let helpers=old.slice(old.indexOf('const worldTCP='),old.indexOf('function retargetDoughPick'));
helpers=helpers.replace('rail:4.2+rand()*.563','rail:1.176+rand()*3.684');
// Keep the previously tested native mesh edge/RRT checker; first try a controlled Cartesian corridor.
helpers=helpers.replace("console.log('CONNECT',label,'goal',check(b));","console.log('CONNECT',label,'goal',check(b));if(edge(st,b)){append(b,label);return;}if(carrying&&cartesianConnect(b,label))return;");
const header=`import fs from 'node:fs';import{T,C,matrix,rig,root,read,box,hits,intersects,robot,solid,update}from './geometry.mjs';import{environment,obstacles,products,productAt,tcpScene}from './world.mjs';import{env}from './layout_v11.mjs';import{clipGripNotch}from '../../../otonom/hat/robot-main-v1/grip-notch.js';
rig.setRailForward(.5);const grid=read('qr_grid_v13.json'),src=read('source_dense_v12.json'),delivery=read('qr_delivery_v15.json'),clone=structuredClone;
for(const product of Object.values(products))for(const p of product.parts){const ids=Array.from(new Set(p.g.index.array)),map=new Map(ids.map((id,i)=>[id,i])),v=[];for(const id of ids)v.push(p.g.attributes.position.getX(id),p.g.attributes.position.getY(id),p.g.attributes.position.getZ(id));const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(v,3));g.setIndex(Array.from(p.g.index.array,id=>map.get(id)));g.computeBoundingBox();p.g=g;p.bvh=null;p.box=g.boundingBox.clone().applyMatrix4(p.m);}
for(const o of obstacles.filter(o=>o.name==='E_KALIP__sac__NEST')){clipGripNotch(T,o.g,o.m);o.bvh=null;update(o,o.m);}
const base=obstacles.filter(o=>!o.name.startsWith('QR_')),cab=env(grid,2,850);
let checks=0,drawers={},carrying=null,local=null,placed={},frames=[],st=null;
`;
let body=fs.readFileSync(dir+'order_body_v15.txt','utf8');
body=body.replace('ik=rig.solve(row,rail,jaw,q)','ik=solveCandidate(row,rail,jaw,q,b.q)');
body=`function solveCandidate(row,rail,jaw,q,goal){let a=rig.solve(row,rail,jaw,q);if(a.valid)return a;for(const seed of [goal,...Object.values(read('poses_v12.json')).map(p=>p.q)]){a=rig.solve(row,rail,jaw,seed);if(a.valid&&!check({q:a.q,rail,jaw}).length)return a;}return a;}\n`+body;
fs.writeFileSync(dir+'order_v15.mjs',header+helpers+body);
