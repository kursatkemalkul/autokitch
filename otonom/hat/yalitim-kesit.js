/* Real planar foam sections. No bounding-box fills: intersect source triangles,
 * then even/odd trapezoid tessellation preserves ducts, holes and empty spaces.
 * Geometry is view-only; CAD/GLB, dimensions and animations are unchanged. */
(() => {
  'use strict';
  const mv=document.getElementById('mv'), entries=new Map();
  const foam=n=>/^(MC_TOPPING_MODUL__yalitim_gorunur|MB_B_KASA__pu)$/.test(n);
  // Segments in a planar 2D section. Each vertex ordinate defines a band in
  // which edge ordering is constant. Pair crossings (even/odd) for holes.
  function tessellate(segments){
    const ys=[...new Set(segments.flatMap(s=>[s[0][1],s[1][1]]).map(y=>Math.round(y*1e7)/1e7))].sort((a,b)=>a-b),out=[];
    const xAt=(s,y)=>s[0][0]+(y-s[0][1])*(s[1][0]-s[0][0])/(s[1][1]-s[0][1]);
    for(let i=1;i<ys.length;i++){
      const a=ys[i-1],b=ys[i];if(b-a<1e-8)continue;const mid=(a+b)/2;
      const crossing=segments.filter(s=>Math.min(s[0][1],s[1][1])<mid && Math.max(s[0][1],s[1][1])>mid).sort((s,t)=>xAt(s,mid)-xAt(t,mid));
      // An odd crossing is an open source contour: do NOT invent a closure.
      if(crossing.length%2)continue;
      for(let j=0;j<crossing.length;j+=2){const l=crossing[j],r=crossing[j+1];if(xAt(r,mid)-xAt(l,mid)<1e-8)continue;
        const p=[xAt(l,a),a],q=[xAt(r,a),a],s=[xAt(r,b),b],t=[xAt(l,b),b];out.push(p,q,s,p,s,t);
      }
    }return out;
  }
  function section(mesh,plane){
    const g=mesh.geometry,p=g.attributes.position,ix=g.index,m=mesh.matrixWorld.elements,n=plane.normal;
    // World plane -> mesh-local coefficients (M transpose), including translation.
    const local=[n.x*m[0]+n.y*m[1]+n.z*m[2],n.x*m[4]+n.y*m[5]+n.z*m[6],n.x*m[8]+n.y*m[9]+n.z*m[10]],d=plane.constant+n.x*m[12]+n.y*m[13]+n.z*m[14];
    const axis=local.map(Math.abs).indexOf(Math.max(...local.map(Math.abs))),other=[0,1,2].filter(a=>a!==axis);
    if(other.some(a=>Math.abs(local[a])>1e-5))return [];// current cut UI is axis-aligned
    const c=-d/local[axis],segments=[];
    for(let i=0;i<ix.count;i+=3){const v=[0,1,2].map(j=>{const k=ix.getX(i+j);return [p.getX(k),p.getY(k),p.getZ(k)]});
      const hits=[];for(let j=0;j<3;j++){const a=v[j],b=v[(j+1)%3],da=a[axis]-c,db=b[axis]-c;
        if((da<0&&db>=0)||(db<0&&da>=0)){const f=da/(da-db);hits.push(other.map(k=>a[k]+f*(b[k]-a[k])));}}
      if(hits.length===2 && Math.hypot(hits[0][0]-hits[1][0],hits[0][1]-hits[1][1])>1e-9)segments.push(hits);
    }
    return tessellate(segments).flatMap(p=>{const v=[0,0,0];v[axis]=c;v[other[0]]=p[0];v[other[1]]=p[1];return v;});
  }
  function update(){
    if(!mv?.loaded)return;const sc=mv[Object.getOwnPropertySymbols(mv).find(s=>s.description==='scene')];if(!sc)return;
    sc.updateMatrixWorld(true);const meshes=[];sc.traverse(o=>{if(o.isMesh&&!o.userData.yalitimKesit&&foam(o.material?.name))meshes.push(o);});
    let changed=false;
    for(const mesh of meshes){
      let e=entries.get(mesh);if(!e){e={key:''};entries.set(mesh,e);}
      const plane=mesh.material.clippingPlanes?.[0];
      if(!plane||!mesh.visible){if(e.cap?.visible){e.cap.visible=false;changed=true;}e.key='';continue;}
      const key=[mesh.geometry.uuid,...Object.values(plane.normal),plane.constant,...mesh.matrixWorld.elements].map(v=>typeof v==='number'?v.toFixed(7):v).join('|');
      if(key===e.key)continue;e.key=key;
      const verts=section(mesh,plane);
      if(!e.cap){const clipping=mesh.material.clippingPlanes;let material;
        try{mesh.material.clippingPlanes=null;material=mesh.material.clone();}finally{mesh.material.clippingPlanes=clipping;}
        material.onBeforeCompile=()=>{};material.clippingPlanes=null;material.side=2;material.transparent=false;material.opacity=1;material.metalness=0;material.roughness=1;
        material.polygonOffset=true;material.polygonOffsetFactor=-1;material.polygonOffsetUnits=-1;material.color.setRGB(0.86,0.10,0.08);if(material.emissive)material.emissive.setRGB(0.55,0.05,0.04);material.envMapIntensity=0;/* Kemal 29 Eyl: kesit KIRMIZI */
        e.cap=new mesh.constructor(new mesh.geometry.constructor(),material);e.cap.name='YALITIM_KESIT_'+mesh.material.name;e.cap.userData.yalitimKesit=true;e.cap.raycast=()=>{};mesh.add(e.cap);
      }
      const geometry=new mesh.geometry.constructor(),Attribute=mesh.geometry.attributes.position.constructor;
      geometry.setAttribute('position',new Attribute(new Float32Array(verts),3));geometry.computeVertexNormals();geometry.computeBoundingSphere();e.cap.geometry.dispose();e.cap.geometry=geometry;e.cap.visible=verts.length>0;changed=true;
    }
    for(const [mesh,e] of entries)if(!meshes.includes(mesh)){if(e.cap){mesh.remove(e.cap);e.cap.geometry.dispose();e.cap.material.dispose();}entries.delete(mesh);}
    if(changed)sc.queueRender();
  }
  setInterval(update,120);
})();
