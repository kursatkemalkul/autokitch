import fs from 'node:fs';
import {rig,root,read,box,intersects} from './geometry.mjs';
import {obstacles,environment} from './world.mjs';
import {grid,env} from './layout_v11.mjs';
import {solve} from './compact_qr_v5.mjs';
const old=read('qr_grid_v11.json'),g=grid(old.config.front,[588,850,1112,1374],500);
g.version=13;g.config.version=13;g.capacity.retained=12;g.capacity.cells=12;
g.human_minimum_floor_mm=588;g.human_minimum_is_design_assumption=true;
g.method+=' Added bottom floor588mm is262mm below previous850mm; user ergonomics not certified.';
rig.setRailForward(.5);environment({},{});
g.static_hits=[];
for(const p of g.parts)for(const b of obstacles.filter(s=>!s.name.startsWith('QR_')&&!s.name.includes('TEZGAH')))if(intersects(box(p.name,p.min,p.max),b))g.static_hits.push([p.name,b.name]);
for(const mm of g.floors_mm)for(let column=0;column<3;column++){
 const prior=old.results.filter(r=>r.column===column).sort((a,b)=>Math.abs(a.floor_mm-mm)-Math.abs(b.floor_mm-mm));
 const seeds=[...prior.flatMap(r=>r.tasks.map(t=>t.state.q)),...old.results.flatMap(r=>r.tasks.map(t=>t.state.q)),...Array.from({length:48},(_,i)=>Array.from({length:6},(_,j)=>Math.sin(i*12.9898+j*78.233)*Math.PI))];
 const rails=Object.fromEntries(['Dessert','Cola','Box'].map(key=>{const prev=prior[0].tasks.find(t=>t.key===key).state.rail;return [key,[prev,g.columns_x[column]+.3,g.columns_x[column],g.columns_x[column]-.3,g.columns_x[column]+.6,g.columns_x[column]-.65,g.columns_x[column]-.85].map(x=>Math.max(1.3760691692136846,Math.min(4.86,x)))];}));
 const a=solve({...g.config,x:g.columns_x[column],cabinet_parts:env(g,column,mm),ignore_workbench:true,lift_m:.02,box_lift_m:.02,search_yaws:true,extra_seeds:seeds,task_rails:rails,samples:40},mm);
 a.column=column;g.results.push(a);
 g.overall_passed=g.results.length===12&&g.results.every(r=>r.passed)&&!g.static_hits.length;
 g.verified_cells=g.results.filter(r=>r.passed).length;
 g.total_task_paths=g.results.reduce((n,r)=>n+r.tasks.filter(t=>t.passed).length*2,0);
 fs.writeFileSync(root+'qr_grid_v13.json',JSON.stringify(g,null,2));
 console.log(JSON.stringify({mm,column,passed:a.passed,tasks:a.tasks.map(t=>[t.key,t.passed,t.last,t.state?.rail])}));
 if(!a.passed)process.exit(1);
}



