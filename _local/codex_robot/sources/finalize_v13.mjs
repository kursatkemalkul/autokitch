import fs from 'node:fs';
import assert from 'node:assert/strict';
const root='otonom/hat3d/robot-main-v1/',read=n=>JSON.parse(fs.readFileSync(root+n)),save=(n,j)=>fs.writeFileSync(root+n,JSON.stringify(j,null,2)+'\n');
const g=read('qr_grid_v13.json'),a=read('assembly.json'),anim=read('rail_animation_v12.json');
assert(g.overall_passed&&g.verified_cells===12&&g.total_task_paths===72&&g.static_hits.length===0);
assert.deepEqual(g.floors_mm,[588,850,1112,1374]);
let maxStep=0;
for(const r of g.results)for(const t of r.tasks)for(const path of [t.sequence,t.exit])for(let i=1;i<path.length;i++)for(let k=0;k<6;k++){
 const prev=path[i-1].state.q[k];let q=path[i].state.q[k];while(q-prev>Math.PI)q-=2*Math.PI;while(q-prev< -Math.PI)q+=2*Math.PI;path[i].state.q[k]=q;maxStep=Math.max(maxStep,Math.abs(q-prev));
}
assert(maxStep<.16,'Excessive consecutive joint movement');g.max_adjacent_joint_step_deg=maxStep*180/Math.PI;
const railMax=Math.max(...g.results.flatMap(r=>r.tasks.flatMap(t=>[t.state.rail,...t.sequence.map(v=>v.state.rail),...t.exit.map(v=>v.state.rail)]))),railMin=anim.summary.rail_start_m+.24;
for(const r of g.results)for(const t of r.tasks){assert(t.passed);assert.equal(t.sequence.length,41);assert.equal(t.exit.length,41);assert(t.state.rail>=railMin&&t.state.rail<=railMax);}
g.rail_requirement={carriage_min_m:railMin,carriage_max_m:railMax,rail_start_m:railMin-.24,rail_end_m:railMax+.24,required_stroke_mm:Math.ceil((railMax-railMin)*1000),geometric_rail_length_mm:Math.ceil((railMax-railMin+.48)*1000),recommended_with_50mm_each_end_mm:Math.ceil((railMax-railMin+.58)*1000),assumptions:'Existing CAD end allowance240mm each; extra50mm each remains design assumption; combined separate source and QR routes, not a continuous new full order.'};
save('qr_grid_v13.json',g);
a.version='v13';a.fixed_qr_reach='qr_grid_v13.json';a.qr_capacity=12;a.qr_layout={...a.qr_layout,rows:4,cells:12,floors_mm:g.floors_mm};a.qr_rail_requirement=g.rail_requirement;
a.fixed_qr_checks={cells:12,paths:72,poses:2952};
a.open=a.open.filter(v=>!v.startsWith('v13:'));
a.open.push('v13: added lower3cells, floor588mm; unchanged1473mm width and1636mm top. All12cells x3products xentry/exit passed41sample poses each path, static0. 588mm floor below prior850mm human comfort assumption; human ergonomics unverified. Original v12 animation is retained and is not a full12cell order animation. Ideal grasp, no real forces or continuous sweep certification. Right upper cola/dessert needs carriage4.86m,97mm beyond v12endpoint measurement; combined recommended rail4064mm with assumed stop margins.');
save('assembly.json',a);
console.log(JSON.stringify({passed:true,cells:12,paths:72,sampled_poses:2952,rail:g.rail_requirement}));
