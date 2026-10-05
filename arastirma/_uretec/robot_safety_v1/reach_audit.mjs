// Every saved QR entry/withdrawal pose tested against the new cabinet and migrated devices.
// Triangle intersections are finite pose checks, not continuous safety certification.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import * as T from './vendor/three.mjs';
import {MeshBVH} from './vendor/bvh.mjs';
import {Rig} from './vendor/rig.mjs';
const HERE=path.dirname(fileURLToPath(import.meta.url));
function solid(name,g,m=new T.Matrix4(),body=null){g.computeBoundingBox();return {name,g,m,body,box:g.boundingBox.clone().applyMatrix4(m),bvh:null};}
function load(file){const b=fs.readFileSync(file),len=b.readUInt32LE(12),j=JSON.parse(b.subarray(20,20+len)),bin=b.subarray(28+len);const out=[];
 function acc(id){const a=j.accessors[id],v=j.bufferViews[a.bufferView],n={SCALAR:1,VEC2:2,VEC3:3,VEC4:4}[a.type],f={5126:['getFloat32',4],5125:['getUint32',4],5123:['getUint16',2],5121:['getUint8',1]}[a.componentType],dv=new DataView(bin.buffer,bin.byteOffset,bin.byteLength),res=[];for(let i=0;i<a.count;i++)for(let k=0;k<n;k++)res.push(dv[f[0]]((v.byteOffset||0)+(a.byteOffset||0)+i*(v.byteStride||n*f[1])+k*f[1],true));return res;}
 function visit(id,parent){const n=j.nodes[id],m=n.matrix?new T.Matrix4().fromArray(n.matrix):new T.Matrix4().compose(new T.Vector3(...(n.translation||[0,0,0])),new T.Quaternion(...(n.rotation||[0,0,0,1])),new T.Vector3(...(n.scale||[1,1,1])));m.premultiply(parent);
  if(/^(QR62_|CELL62_|QR_|ELK_QR)/.test(n.name||'')&&n.mesh!=null)for(const p of j.meshes[n.mesh].primitives){const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(acc(p.attributes.POSITION),3));if(p.indices!=null)g.setIndex(acc(p.indices));out.push(solid(n.name,g,m.clone()));}
  for(const c of n.children||[])visit(c,m);
 }for(const n of j.scenes[j.scene||0].nodes)visit(n,new T.Matrix4());return out;
}
const read=n=>JSON.parse(fs.readFileSync(path.join(HERE,'inputs',n)));
const data=read('rig.json'),rig=new Rig(data,{mountForward:.1,railForward:.5});
const robot=read('collision.json').map(s=>{const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(s.vertices.flat(),3));g.setIndex(s.faces.flat());return solid(s.path,g,new T.Matrix4(),s.body);});
const obstacles=load(process.argv[2]),C=new T.Matrix4().makeRotationX(-Math.PI/2),grid=read('qr_grid_v13.json');
let poses=0;const hits=[],cells=[];
for(const cell of grid.results){let cellHits=0;
 for(const task of cell.tasks){const states=[...task.sequence.map(p=>p.state),task.state];
  for(const state of states){poses++;const w=rig.matrices(state.q,state.rail,state.jaw);
   for(const a of robot){a.m=C.clone().multiply(new T.Matrix4().set(...w[a.body]));a.box.copy(a.g.boundingBox).applyMatrix4(a.m);
    for(const b of obstacles){if(!a.box.intersectsBox(b.box))continue;
     a.bvh??=new MeshBVH(a.g);b.bvh??=new MeshBVH(b.g);
     if(a.bvh.intersectsGeometry(b.g,a.m.clone().invert().multiply(b.m))){cellHits++;if(hits.length<60)hits.push({floor_mm:cell.floor_mm,column:cell.column,task:task.key,pose:poses,body:a.body,obstacle:b.name});}
    }
   }
  }
 }cells.push({floor_mm:cell.floor_mm,column:cell.column,passed:cellHits===0,hit_pairs:cellHits});console.log('Cell',cell.floor_mm,cell.column,'hit pairs',cellHits);
}
const result={poses,verified_cells:cells.filter(c=>c.passed).length,total_cells:12,cells,hits,passed:cells.every(c=>c.passed),scope:'all saved QR poses against new cabinet/device meshes; not machine pickup routes, continuous collision or physics certification'};
fs.writeFileSync(path.join(HERE,'reach_audit.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({poses,cells:result.verified_cells,passed:result.passed,hits:hits.length}));process.exit(result.passed?0:1);
