import * as T from '../robot_integrated_v22/vendor/three.mjs';
// One indexed closed mesh, with parallel-transport frames for circular tubes.
export function sweep(points,profile,normal=null,hollow=false){
 const p=points.map(v=>new T.Vector3(...v)),vertices=[],indices=[],frames=[];
 let previous=null,u=null;
 for(let i=0;i<p.length;i++){
  const t=p[Math.min(i+1,p.length-1)].clone().sub(p[Math.max(i-1,0)]).normalize();
  let v;
  if(normal){v=new T.Vector3(...normal);u=v.clone().cross(t).normalize();}
  else if(!previous){v=Math.abs(t.y)<.9?new T.Vector3(0,1,0):new T.Vector3(0,0,1);u=v.cross(t).normalize();}
  else u.applyQuaternion(new T.Quaternion().setFromUnitVectors(previous,t)).normalize();
  v=t.clone().cross(u).normalize();previous=t;frames.push([u.clone(),v.clone()]);
  for(const [x,y]of profile){const q=p[i].clone().addScaledVector(u,x).addScaledVector(v,y);vertices.push(...q.toArray());}
 }
 const count=profile.length,ring=hollow?count/2:count;
 const quad=(a,b,c,d)=>indices.push(a,b,c,a,c,d);
 for(let i=1;i<p.length;i++)for(let k=0;k<count;k++){
  const offset=hollow&&k>=ring?ring:0,next=offset+(k-offset+1)%ring;
  if(!hollow||k<ring)quad((i-1)*count+k,(i-1)*count+next,i*count+next,i*count+k);
  else quad((i-1)*count+next,(i-1)*count+k,i*count+k,i*count+next);
 }
 if(hollow)for(let k=0;k<ring;k++){const j=(k+1)%ring,last=(p.length-1)*count;quad(k,k+ring,j+ring,j);quad(last+j,last+j+ring,last+k+ring,last+k);}
 else{const first=vertices.length/3;vertices.push(...p[0].toArray(),...p.at(-1).toArray());for(let k=0;k<count;k++){const j=(k+1)%count,last=(p.length-1)*count;indices.push(first,j,k,first+1,last+k,last+j);}}
 const geo=new T.BufferGeometry();geo.setAttribute('position',new T.Float32BufferAttribute(vertices,3));geo.setIndex(indices);geo.computeVertexNormals();return geo;
}
export const cableMesh=(points,r)=>sweep(points,Array.from({length:16},(_,i)=>[r*Math.cos(2*Math.PI*i/16),r*Math.sin(2*Math.PI*i/16)]));
export function ductMesh(d){const w=d.width_m/2,h=d.height_m/2,t=d.wall_m;return sweep(d.points,[[-w,-h],[w,-h],[w,h],[-w,h],[-w+t,-h+t],[w-t,-h+t],[w-t,h-t],[-w+t,h-t]],d.normal,true);}
