import * as T from './vendor/three.mjs';
// Main-scene geometry only. Electrical ratings remain subject to circuit design.
export function installServices({g,mesh,node,bodyNodes,read}){
 const ids=[],ducts=[],mounts=[],chain=[],portRoutes=[],cart=bodyNodes['/World/RailSystem/Carriage'];
 const colors={metal:0xa9b4bc,power:0xbd3430,data:0x2a74be,chain:0x30373c};
 const extra=(name,connection,kat='GUC')=>({kat,mek:kat==='ROBOT'?'Robot/Ray':'Robot/Elektrik',connection,part:name,version:22});
 function add(name,geo,col,at=[0,0,0],connection='unit',parent=null,kat='GUC'){
  const id=mesh('ROBOT22_'+name,geo,col,at,extra(name,connection,kat));ids.push(id);
  if(parent!=null){g.scenes[g.scene||0].nodes=g.scenes[g.scene||0].nodes.filter(i=>i!==id);g.nodes[parent].children??=[];g.nodes[parent].children.push(id);}
  return id;
 }
 function box(name,lo,hi,col=colors.metal,connection='supported',parent=null,kat='GUC'){
  return add(name,new T.BoxGeometry(...hi.map((v,i)=>v-lo[i])),col,lo.map((v,i)=>(v+hi[i])/2),connection,parent,kat);
 }
 const tube=(a,b,r)=>{let geom=new T.CylinderGeometry(r,r,Math.hypot(...a.map((v,i)=>v-b[i])),10);geom.applyQuaternion(new T.Quaternion().setFromUnitVectors(new T.Vector3(0,1,0),new T.Vector3(...b.map((v,i)=>v-a[i])).normalize()));return geom;};
 function cable(name,points,r,col,parent=null){let result=[];points=points.map(p=>p[1]<0&&parent===null?[p[0],col===colors.data?-.022:-.060,p[2]]:p);for(let i=1;i<points.length;i++)result.push(add(name+'_'+i,tube(points[i-1],points[i],r),col,points[i-1].map((v,k)=>(v+points[i][k])/2),'inside protected trunk or retained P-clips',parent));return result;}
 function duct(name,a,b,w=.06,h=.06){
  if(a[1]<0&&b[1]<0){ducts.push({name,a,b,width_m:.080,height_m:.080,shared_recessed_trench:true,nodes:[]});return [];}
  const d=new T.Vector3(...b.map((v,i)=>v-a[i])),len=d.length(),at=a.map((v,i)=>(v+b[i])/2),q=new T.Quaternion().setFromUnitVectors(new T.Vector3(1,0,0),d.normalize()),pieces=[];
  // Coordinate around local X; hollow closed 304 trunk with removable cover.
  for(const [suffix,sz,off]of [['base',[len,.002,w],[0,-h/2+.001,0]],['left',[len,h-.0035,.0015],[0,-.00075,-w/2+.00075]],['right',[len,h-.0035,.0015],[0,-.00075,w/2-.00075]],['cover',[len,.0015,w],[0,h/2-.00075,0]]]){
   const geo=new T.BoxGeometry(...sz);geo.translate(...off);geo.applyQuaternion(q);pieces.push(add(name+'_'+suffix,geo,colors.metal,at,suffix==='cover'?'captive cover screws to side returns':'factory folded 304 trunk; anchored base'));
  }
  ducts.push({name,a,b,width_m:w,height_m:h,nodes:pieces});return pieces;
 }
 function route(name,pts,w=.06,h=.06){for(let i=1;i<pts.length;i++)duct(name+'_'+i,pts[i-1],pts[i],w,h);return pts;}
 function bolt(name,x,y,z,axis='Y',parent=null){let geo=new T.CylinderGeometry(.004,.004,.020,10);if(axis==='Z')geo.rotateX(Math.PI/2);if(axis==='X')geo.rotateZ(Math.PI/2);const id=add(name,geo,0x597d92,[x,y,z],'M8 ISO4762 in existing/own mounting holes',parent);mounts.push(id);return id;}
 function plate(name,width,depth,t,holes,at,parent=null){
  const s=new T.Shape();s.moveTo(-width/2,-depth/2);s.lineTo(width/2,-depth/2);s.lineTo(width/2,depth/2);s.lineTo(-width/2,depth/2);s.closePath();
  for(const [x,z,r]of holes){const hole=new T.Path();hole.absarc(x,z,r,0,2*Math.PI,true);s.holes.push(hole);}
  const geo=new T.ExtrudeGeometry(s,{depth:t,bevelEnabled:false,curveSegments:12});
  return add(name,geo,colors.metal,at,'M8 into supplied carriage pattern; M8 robot pattern Ø95',parent,'ROBOT');
 }
 // Real igus manufacturer tessellation. Only the continuous axial region was
 // extended to a supplier-confirmation concept; source STEP is archived intact.
 const cad=read('rail_cad.json');
 // The old simulator carriage geometry lives in child meshes, not on the body.
 // Keep the animated rigid-body frame but discard its three obsolete plates.
 delete g.nodes[cart].mesh;g.nodes[cart].children=[];delete g.nodes[bodyNodes['/World/RailSystem/RailBase']].mesh;
 for(const p of cad.parts){const geo=new T.BufferGeometry();geo.setAttribute('position',new T.Float32BufferAttribute(p.vertices,3));geo.setIndex(p.indices);geo.computeVertexNormals();add('IGUS_'+p.name,geo,p.moving?0x5b8791:0x9aa5ac,[0,0,0],p.moving?'manufacturer carriage; linear bearings on original profile':'manufacturer CAD / axial length concept',p.moving?cart:null,'ROBOT');}
 // 50 mm level anchored bed supports the unchanged 130 mm robot mounting plane.
 box('RAY_TABAN', [.978,0,.819],[5.058,.05,1.101],0x747e87,'anchored steel bed',null,'ROBOT');
 for(const x of [1.04,1.65,2.3,2.95,3.6,4.25,4.99])for(const z of [.834,1.086])bolt('RAY_ZEMIN_M8_'+x+'_'+z,x,.016,z);
 // Three standard thicknesses total 16 mm. Carriage geometry top=.114 m.
 const holes=[[-.033588,-.033588,.0045],[.033588,-.033588,.0045],[-.033588,.033588,.0045],[.033588,.033588,.0045],[-.090,-.077,.0045],[.090,-.077,.0045],[-.090,.077,.0045],[.090,.077,.0045]];
 let z=.019;for(const [i,t]of [.006,.006,.004].entries()){plate('ADAPTOR_PLAKA_'+i,.22,.25,t,holes,[0,-.1,z],cart);z+=t;}
 for(const [x,y]of holes.slice(0,4).map(([x,y])=>[x,y]))bolt('ROBOT_MONTAJ_'+x+'_'+y,x,-.1-y,.025,'Z',cart);
 for(const [x,y]of holes.slice(4).map(([x,y])=>[x,y]))bolt('ARABA_MONTAJ_'+x+'_'+y,x,-.1-y,.019,'Z',cart);
 // Remove the old QR-imported box; its baked world vertices made translation
 // incorrect. Define a single neutral enclosure directly under the QR instead.
 const controller=box('UR_KONTROL_KUTUSU',[4.355,.100,1.775],[4.830,.523,2.043],0x747f88,'purchased controller envelope supported on own cradle',null,'KONTROL');
 g.nodes[controller].extras.dimensions_mm=[475,423,268];
 // Open space under the enclosure: floor trunks never pass through a solid block.
 const cradleShape=new T.Shape();cradleShape.moveTo(4.335,1.765);cradleShape.lineTo(4.85,1.765);cradleShape.lineTo(4.85,2.053);cradleShape.lineTo(4.335,2.053);cradleShape.closePath();
 const entry=new T.Path();entry.moveTo(4.595,1.845);entry.lineTo(4.595,1.965);entry.lineTo(4.755,1.965);entry.lineTo(4.755,1.845);entry.closePath();cradleShape.holes.push(entry);
 const cradleGeo=new T.ExtrudeGeometry(cradleShape,{depth:.003,bevelEnabled:false});cradleGeo.rotateX(Math.PI/2);cradleGeo.translate(0,.097,0);
 add('KONTROL_KUTUSU_KAIDE',cradleGeo,0x6f7981,[0,0,0],'3 mm stand top with cable-entry cutout');
 for(const x of [4.345,4.84])for(const zz of [1.775,2.043])box('UR_KAIDE_AYAK_'+x+'_'+zz,[x-.01,0,zz-.01],[x+.01,.094,zz+.01],0x6f7981,'floor-supported stand legs; welded top');
 // Rubber pads and low capture lips support the purchased box without drilling it.
 for(const x of [4.355,4.815])for(const zz of [1.785,2.03])box('UR_KAUCUK_'+x+'_'+zz,[x-.009,.097,zz-.009],[x+.009,.100,zz+.009],0x333b3f,'elastomer pad on cradle');
 box('EKSEN_SURUCU_KAIDE',[3.80,.020,1.80],[4.12,.040,2.05],0x6f7981,'sits on QR lower shelf; captured by stops');
 box('EKSEN_SURUCU_KUTUSU',[3.82,.040,1.82],[4.10,.34,2.03],0x53646c,'driver enclosure on base; sizing concept');
 box('EKSEN_SURUCU_ON_KAPAK',[3.823,.045,1.8185],[4.097,.335,1.82],0x8797a1,'captive enclosure door screws');
 for(const x of [3.832,4.088])for(const y of [.065,.315])bolt('SURUCU_KAPAK_'+x+'_'+y,x,y,1.815,'Z');
 // The downloaded STEP is the mechanical belt axis, not a supplied motor CAD.
 // A supported motor/interface envelope makes the electrical destination explicit.
 box('EKSEN_MOTOR_PABUC',[4.988,0,.749],[5.062,.0515,.812],0x747e87,'floor-supported motor bracket; sizing concept',null,'MOTOR');
 const motorGeo=new T.CylinderGeometry(.030,.030,.085,24);motorGeo.rotateX(Math.PI/2);
 const motor=add('EKSEN_MOTOR_KONSEPT',motorGeo,0x48545e,[5.025,.0815,.7875],'motor / flange / shaft concept; supplier selection required',null,'MOTOR');
 g.nodes[motor].extras.manufacturer_cad=false;g.nodes[motor].extras.sizing_confirmed=false;
 box('EKSEN_MOTOR_FLANS',[4.995,.0515,.830],[5.055,.1115,.834],0x697783,'flange at belt drive head; supplier mounting pattern open',null,'MOTOR');
 cable('EKSEN_MOTOR_SAFT',[[5.025,.0815,.830],[5.025,.0815,.850]],.006,0xadb8c0);
 // One recessed floor service tree. Branches share a single protected trench.
 const floor=read('floor_plan.json'),paths=floor.paths;
 function shape(poly){const s=new T.Shape(poly.outer.map(p=>new T.Vector2(...p)));for(const h of poly.holes)s.holes.push(new T.Path(h.map(p=>new T.Vector2(...p))));return s;}
 function surface(name,polys,depth,top,color,connection){for(const [i,p]of polys.entries()){const geo=new T.ExtrudeGeometry(shape(p),{depth,bevelEnabled:false});geo.rotateX(Math.PI/2);add(name+'_'+i,geo,color,[0,top,0],connection,null,'DUKKAN');}}
 surface('ZEMIN_TEMIZ',floor.floor,.010,0,0xdbdbd6,'continuous floor; retired service holes filled');
 surface('GOMULU_KANAL_TABAN',floor.trench,.002,-.078,colors.metal,'recessed supported trench bottom');
 surface('GOMULU_KANAL_YAN',floor.walls,.072,-.006,colors.metal,'folded 304 trench wall / lid support');
 surface('GOMULU_KANAL_AYIRICI',floor.trench,.0015,-.03925,colors.metal,'horizontal divider separates mains and signal compartments');
 surface('ZEMIN_SIFIR_KAPAK',floor.lids,.006,0,0xa8adae,'6 mm removable flush lid; supported all edges; floor load confirmation pending');
 const destinations={wall:'existing wall supply cabinet bottom',machine:'existing machine rear inlet',QR:'QR electrical gland','UR controller':'UR controller bottom entry','axis feed':'axis driver bottom entry','arm output':'fixed energy-chain entry','axis drive':'axis motor connector'};
 for(const [name,pts]of Object.entries(paths)){route(name.replaceAll(' ','_').toUpperCase(),pts,name==='QR'?.034:name==='arm output'?.042:.040,.060);portRoutes.push({name,points:pts,destination:destinations[name]});}
 cable('QR_GUC',paths.QR,.004,colors.power);cable('ROBOT_BESLEME',paths['UR controller'],.005,colors.power);cable('MAKINE_BESLEME',paths.machine,.005,colors.power);cable('SURUCU_BESLEME',paths['axis feed'],.004,colors.power);
 cable('UR_HIGH_FLEX_12M_SABIT',paths['arm output'],.0073,colors.data);
 cable('SERVO_MOTOR_KABLO',paths['axis drive'],.004,colors.power);
 const fixed=paths['arm output'].at(-1);
 // Side guide and moving chain, radius 150 mm > UR dynamic minimum 116.8 mm.
 box('ZINCIR_OLUK_TABAN',[1.056,.039,1.145],[5.16,.041,1.225],0x7c878f,'guide bottom on floor-supported standoffs');
 for(const zz of [1.145,1.2235])box('ZINCIR_OLUK_YAN_'+zz,[1.056,.041,zz],[5.16,.094,zz+.0015],0x7c878f,'TIG to chain guide base');
 for(const x of [1.10,2.10,3.10,4.10,5.11])box('OLUK_ZEMIN_PABUC_'+x,[x-.020,0,1.145],[x+.020,.039,1.225],0x7c878f,'floor-supported spacer, anchored through guide');
 for(const x of [1.10,2.10,3.10,4.10,5.11])for(const zz of [1.151,1.219])bolt('OLUK_ANKRAJ_'+x+'_'+zz,x,.037,zz);
 const radius=.150,straight=2.05,length=straight+Math.PI*radius,N=80,pitch=length/N;
 function chainPose(index,rail){
  const m=rail,b=(fixed[0]+m+straight)/2,s=(index+.5)*pitch,L=b-fixed[0];
  if(s<L)return {p:[fixed[0]+s,fixed[1],fixed[2]],angle:0};
  if(s<L+Math.PI*radius){const t=(s-L)/radius;return{p:[b+radius*Math.sin(t),fixed[1]+radius*(1-Math.cos(t)),fixed[2]],angle:t};}
  return{p:[b-(s-L-Math.PI*radius),fixed[1]+2*radius,fixed[2]],angle:Math.PI};
 }
 for(let i=0;i<N;i++){
  // Hollow links with an internal corridor for robot cable / Ethernet / air.
  const geometries=[];for(const [sz,off]of [[[pitch*.94,.034,.003],[0,0,-.0335]],[[pitch*.94,.034,.003],[0,0,.0335]],[[pitch*.94,.003,.064],[0,-.0155,0]],[[pitch*.94,.003,.064],[0,.0155,0]]]){const z=new T.BoxGeometry(...sz);z.translate(...off);geometries.push(z);}
  const parts=geometries.map((z,k)=>add('ZINCIR_LINK_'+i+'_'+k,z,colors.chain,[0,0,0],'linked articulated cable carrier; closed crossbar'));
  const root=node({name:'ROBOT22_ZINCIR_LINK_'+i,children:parts,extras:extra('energy chain','linked chain supported by guide','GUC')});
  g.scenes[g.scene||0].nodes=g.scenes[g.scene||0].nodes.filter(n=>!parts.includes(n));chain.push(root);
 }
 // The moving cable and its bracket belong to the carriage, never to the floor.
 box('ZINCIR_ARABA_BRAKETI',[ -.018,-.315,.035],[.018,-.312,.263],0x89979d,'3 mm folded 304; TIG to own adapter',cart,'ROBOT');
 box('ZINCIR_ARABA_BRAKET_AYAK',[-.018,-.315,.035],[.018,-.212,.038],0x89979d,'3 mm flange; TIG to own adapter outer edge',cart,'ROBOT');
 const movingCable=[[0,-.325,.263],[0,-.325,.075],[0,-.22,.075],[0,-.195,.055]];
 cable('UR_HIGH_FLEX_ARABA',movingCable,.0073,colors.data,cart);
 for(const zz of [.10,.18,.25])box('ARABA_P_KLIPS_'+zz,[-.012,-.336,zz-.006],[.012,-.325,zz+.006],0x222a30,'P-clip retained to own carriage bracket',cart);
 return {ids,ducts,mounts,chain,chainPose,portRoutes,cad,chain_spec:{radius_m:radius,length_m:length,fixed_world:fixed,moving_y_m:.358,guide_z_m:[1.145,1.225],cable_diameter_m:.0146,cable_dynamic_min_radius_m:.1168,cable_max_m:12},floor_plan:floor,legacy_carriage_removed:true,legacy_yellow_controller_removed:true,glass_removed:'CELL62_gate_screen',physicalSafetyCertified:false};
}
