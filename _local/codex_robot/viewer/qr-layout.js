// Twelve compartments retained. Simple robot-access layout proposal in CAD metres.
export const layout={version:4,columns:4,rows:3,x:3.79,pitch:.410,front:.85,depth:.44,floors:[.30,.56,.82],height:.24,wall:.012,stroke:.30};
export function qrParts(){const p=[],L=layout,x0=L.x,x1=x0+L.columns*L.pitch,z0=L.front,z1=z0+L.depth,top=L.floors.at(-1)+L.height,w=L.wall;
 const add=(name,min,max,kind='wall')=>p.push({name:'QR_V4_'+name,min,max,kind});
 add('back_bottom',[x0,.25,z1-w],[x1,L.floors[0],z1]);
 for(let r=1;r<L.rows;r++)add('back_sill_'+r,[x0,L.floors[r]-.02,z1-w],[x1,L.floors[r],z1]);
 add('back_top',[x0,top-w,z1-w],[x1,top,z1]);
 for(let c=0;c<=L.columns;c++)add('wall_'+c,[c===0?x0:c===L.columns?x1-w:x0+c*L.pitch-w/2,.25,z0],[c===0?x0+w:c===L.columns?x1:x0+c*L.pitch+w/2,top,z1]);
 for(let r=0;r<L.rows;r++)for(let c=0;c<L.columns;c++){const x=x0+c*L.pitch;add('tray_'+r+c,[x+w,L.floors[r]-w,z0],[x+L.pitch-w,L.floors[r],z1-w],'shelf');}
 add('roof',[x0,top,z0],[x1,top+w,z1]);
 add('control_housing',[4.65,.025,.90],[5.32,.245,1.27]);
 for(let c=0;c<L.columns;c++)for(let r=0;r<L.rows;r++){const f=L.floors[r],x=x0+c*L.pitch;add('customer_door_'+r+c,[x+w/2,f,z1],[x+L.pitch-w/2,f+L.height,z1+.006],'door');}
 for(const x of [x0+.04,x1-.04])for(const z of [z0+.04,z1-.04])add('leg_'+x+'_'+z,[x-.02,0,z-.02],[x+.02,.288,z+.02],'leg');
 return p;
}
export function installQR(T,scene,machineMeshes){const group=new T.Group();group.name='QR_LAYOUT_V4';scene.add(group);const materials={wall:new T.MeshStandardMaterial({color:0x9daeb8,metalness:.35,roughness:.6}),shelf:new T.MeshStandardMaterial({color:0xbed6df,metalness:.25,roughness:.65}),door:new T.MeshStandardMaterial({color:0x82b2c0,transparent:true,opacity:.28,roughness:.45}),leg:new T.MeshStandardMaterial({color:0x485660,metalness:.65,roughness:.4})};for(const p of qrParts()){const size=p.max.map((v,i)=>v-p.min[i]),g=new T.BoxGeometry(...size);g.computeBoundingBox();const m=new T.Mesh(g,materials[p.kind]);m.name=p.name;m.position.set(...p.min.map((v,i)=>(v+p.max[i])/2));group.add(m);machineMeshes.push(m);const e=new T.LineSegments(new T.EdgesGeometry(g),new T.LineBasicMaterial({color:0x28353e}));m.add(e);}return group;}

