import fs from 'node:fs';import{T,C,matrix,rig,read,root,robot,update,intersects}from './geometry.mjs';import{products,productAt}from './world.mjs';rig.setRailForward(.5);
for(const p of Object.values(products).flatMap(p=>p.parts)){const ids=[...new Set(p.g.index.array)],map=new Map(ids.map((id,i)=>[id,i])),v=[];for(const id of ids)v.push(p.g.attributes.position.getX(id),p.g.attributes.position.getY(id),p.g.attributes.position.getZ(id));const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(v,3));g.setIndex(Array.from(p.g.index.array,id=>map.get(id)));g.computeBoundingBox();p.g=g;p.bvh=null;p.box=g.boundingBox.clone().applyMatrix4(p.m);}
const data=read('order_v15.json');if(!data.summary.completed.includes('Dough'))throw Error('Whole order not ready');
let checks=0;const failures=[];
for(let i=0;i<data.trajectory.length;i++){const f=data.trajectory[i],s=f.state,w=rig.matrices(s.q,s.rail,s.jaw);for(const r of robot)update(r,C.clone().multiply(matrix(w[r.body])));
 const active=f.carrying||(/^(Box|Kutu)/.test(f.stage)?'Box':/^(Dessert|Tatlı)/.test(f.stage)?'Dessert':/^(Cola|İçecek)/.test(f.stage)?'Cola':'Dough');
 if(f.carrying){const m=C.clone().multiply(matrix(rig.tcp(s.q,s.rail,s.jaw)));productAt(f.carrying,f.product,f.carrying==='Box'?Math.atan2(m.elements[8],m.elements[10]):0);}
 for(const[key,pos]of Object.entries(f.placed)){productAt(key,pos,0);for(const p of products[key].parts){for(const r of robot){if(key===active&&r.body.includes('/Gripper/'))continue;checks++;if(intersects(p,r))failures.push({frame:i,stage:f.stage,placed:key,hit:r.body});}if(f.carrying&&key!==f.carrying)for(const a of products[f.carrying].parts){checks++;if(intersects(p,a))failures.push({frame:i,stage:f.stage,placed:key,hit:'carried '+f.carrying});}}}
 if(failures.length)break;
}
const result={passed:!failures.length,checked_frames:data.trajectory.length,checks,intended_gripper_contact_exempt_only_for_active_product:true,failures};fs.writeFileSync(root+'placed_audit_v15.json',JSON.stringify(result,null,2));console.log(result);if(failures.length)process.exitCode=1;
