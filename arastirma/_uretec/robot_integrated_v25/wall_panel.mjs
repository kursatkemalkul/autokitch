// Actual catalogue families/envelopes; protective ratings require load/earthing design.
export function wallPanel({add:baseAdd,box:baseBox,bolt:baseBolt,T,cableMesh,layout}){
 const wallX=layout.right_wall_inner_x_m;
 const dx=wallX+.220-6.216,dz=1.110;
 const shift=p=>[p[0]+dx,p[1],p[2]+dz];
 const add=(name,geo,col,at=[0,0,0],...rest)=>baseAdd(name,geo,col,shift(at),...rest);
 const box=(name,lo,hi,...rest)=>baseBox(name,shift(lo),shift(hi),...rest);
 const bolt=(name,x,y,z,...rest)=>baseBolt(name,x+dx,y,z+dz,...rest);
 const grey=0xaeb5b8,white=0xe7e6df,dark=0x46525a;
 // Only 3 mm perimeter/corner lines; no opaque right wall surfaces.
 const z0=-.86,z1=2.17,h=2.4;
 for(const [i,a,b]of [[0,[wallX,0,z0],[wallX,h,z0]],[1,[wallX,0,z1],[wallX,h,z1]],[2,[wallX,0,z0],[wallX,0,z1]],[3,[wallX,h,z0],[wallX,h,z1]]])
  baseAdd('SAG_DUVAR_KOSE_CIZGI_'+i,cableMesh([a,b],.0015),0x74808a,[0,0,0],'visual boundary only; actual wall plane retained for clearance',null,'DUKKAN');
 const frame=(name,lo,hi)=>box(name,lo,hi,grey,'2 mm sheet enclosure, folded butt joints; fixed to right wall',null,'GOVDE');
 const backShape=new T.Shape([new T.Vector2(.45,1.0),new T.Vector2(-.15,1.0),new T.Vector2(-.15,1.70),new T.Vector2(.45,1.70)]);
 for(const [z,y,r]of [[-.35,1.65,.0135],[.04,1.65,.006]]){const h=new T.Path();h.absarc(-z,y,r,0,2*Math.PI,true);backShape.holes.push(h);}
 const backGeo=new T.ExtrudeGeometry(backShape,{depth:.002,bevelEnabled:false,curveSegments:12});backGeo.rotateY(Math.PI/2);backGeo.translate(6.194,0,0);add('DUVAR_PANO_ARKA',backGeo,grey,[0,0,0],'back sheet with actual building feeder/WAN entry holes',null,'GOVDE');
 add('BINA_ANA_GUC_GIRIS',cableMesh([[6.270,1.65,-.35],[6.194,1.65,-.35],[6.145,1.65,-.35]],.008),0xbd3430,[0,0,0],'building feeder enters rear gland; circuit selection pending');
 add('BINA_WAN_GIRIS',cableMesh([[6.270,1.65,.04],[6.194,1.65,.04],[6.145,1.65,.04]],.003),0x2a74be,[0,0,0],'building ONT/modem WAN enters rear gland');
 frame('DUVAR_PANO_SOL',[5.948,1.0,-.45],[6.194,1.70,-.448]);
 frame('DUVAR_PANO_SAG',[5.948,1.0,.148],[6.194,1.70,.15]);
 frame('DUVAR_PANO_UST',[5.948,1.698,-.448],[6.194,1.70,.148]);
 // Four genuine bottom gland cutouts rather than cables through an uncut sheet.
 const shape=new T.Shape([new T.Vector2(5.948,-.448),new T.Vector2(6.194,-.448),new T.Vector2(6.194,.148),new T.Vector2(5.948,.148)]);
 for(const [x,z,r]of [[6.17,-.36,.007],[6.15,-.32,.007],[6.13,-.28,.007],[6.11,-.24,.007],[6.10,0,.005],[6.092,.022,.005],[6.084,.044,.005]]){const h=new T.Path();h.absarc(x,z,r,0,2*Math.PI,true);shape.holes.push(h);}
 const bottom=new T.ExtrudeGeometry(shape,{depth:.002,bevelEnabled:false,curveSegments:12});bottom.rotateX(Math.PI/2);bottom.translate(0,1.002,0);add('DUVAR_PANO_ALTI_RAKOR_DELIK',bottom,grey,[0,0,0],'open gland holes in bottom sheet',null,'GOVDE');
 frame('DUVAR_PANO_KAPI',[5.946,1.003,-.448],[5.948,1.697,.148]);
 box('DUVAR_PANO_KILIT',[5.932,1.34,.092],[5.946,1.37,.118],dark,'quarter turn latch on door',null,'GOVDE');
 for(const y of [1.09,1.61])box('DUVAR_PANO_MENTESE_'+y,[5.945,y,-.452],[5.966,y+.04,-.445],grey,'hinge fixed to enclosure side and door',null,'GOVDE');
 for(const y of [1.03,1.66])for(const z of [-.40,.10]){box('PANO_DUVAR_PABUC_'+y+'_'+z,[6.196,y,z-.02],[6.216,y+.025,z+.02],grey,'mounting lug, M8 wall anchor',null,'GOVDE');bolt('PANO_DUVAR_ANKRAJ_'+y+'_'+z,6.217,y+.0125,z,'X');}
 const mountingShape=new T.Shape([new T.Vector2(.42,1.025),new T.Vector2(-.125,1.025),new T.Vector2(-.125,1.675),new T.Vector2(.42,1.675)]);
 for(const [z,r]of [[-.35,.0135],[.04,.006]]){const h=new T.Path();h.absarc(-z,1.65,r,0,2*Math.PI,true);mountingShape.holes.push(h);}
 const mountingGeo=new T.ExtrudeGeometry(mountingShape,{depth:.002,bevelEnabled:false,curveSegments:12});mountingGeo.rotateY(Math.PI/2);mountingGeo.translate(6.173,0,0);add('PANO_MONTAJ_PLAKASI',mountingGeo,grey,[0,0,0],'spacers/M5 to enclosure back; incoming cable holes aligned with rear glands');
 for(const [name,z]of [['ANA_GIRIS',-.35],['WAN_GIRIS',.04]]){box(name+'_KLEMENS',[6.128,1.638,z-.012],[6.150,1.662,z+.012],dark,'incoming feeder terminates on retained terminal');box(name+'_KLEMENS_BRAKET',[6.150,1.637,z-.013],[6.173,1.663,z+.013],grey,'terminal mount attached to plate');}
 for(const y of [1.05,1.65])for(const z of [-.395,.10]){box('PANO_PLAKA_MESAFE_'+y+'_'+z,[6.175,y-.007,z-.007],[6.194,y+.007,z+.007],grey,'19 mm standoff between plate and back sheet');bolt('PANO_PLAKA_M5_'+y+'_'+z,6.176,y,z,'X');}
 box('PANO_GUC_AG_AYIRICI',[5.96,1.01,-.037],[6.173,1.69,-.035],grey,'earthed sheet partition, power/data separated');
 function din(name,y,z0,z1){box(name,[6.158,y-.018,z0],[6.166,y+.018,z1],0x8a949b,'TS35 DIN rail screwed to mounting plate');for(const z of [z0+.015,z1-.015]){box(name+'_MESAFE_'+z,[6.166,y-.006,z-.006],[6.173,y+.006,z+.006],grey,'7 mm DIN standoff');bolt(name+'_VIDA_'+z,6.166,y,z,'X');}}
 din('DIN_UST_ANA_AYIRICI',1.585,-.402,-.065);din('DIN_ALT_CIKISLAR',1.405,-.402,-.065);din('DIN_KLEMENS',1.185,-.402,-.065);
 function device(name,y,z,width,poles,reference){
  const id=box(name,[6.088,y-.046,z],[6.158,y+.046,z+width],white,'catalogue unit clipped to TS35 rail');
  // The mechanism, front levers and terminal ports distinguish it from a plain box.
  for(let i=0;i<poles;i++){const zz=z+(i+.5)*width/poles;box(name+'_KOL_'+i,[6.073,y-.003,zz-.006],[6.088,y+.012,zz+.006],name.includes('ISW')?0xd43c32:dark,'switch lever belongs to purchased unit');for(const yy of [y-.037,y+.037])box(name+'_KLEM_'+i+'_'+yy,[6.083,yy-.004,zz-.003],[6.088,yy+.004,zz+.003],dark,'purchased screw terminal');}
  return {node:id,reference,poles,outline_only:true};
 }
 device('SCHNEIDER_ISW_4P_63A',1.585,-.395,.072,4,'A9S65463');
 device('SCHNEIDER_IID_B_4P_63A',1.585,-.295,.072,4,'A9Z61463; sensitivity/selectivity subject to final design');
 for(const [name,z,poles]of [['MAKINE',-.395,3],['QR',-.315,2],['ROBOT',-.253,2],['EKSEN',-.191,2],['AG',-.129,2]])device('IC60N_'+name,1.405,z,.018*poles,poles,'Acti9 iC60N family; final current and curve not selected');
 for(let i=0;i<12;i++)box('PANO_PT2_5_'+i,[6.112,1.164,-.393+i*.019],[6.158,1.205,-.377+i*.019],i<4?0x7fa45c:grey,'DIN terminal block, PE/N/L distribution');
 box('PANO_PE_BARASI',[6.154,1.087,-.395],[6.162,1.097,-.105],0xc49b56,'protective earth bus bolted to mounting plate');
 for(const z of [-.37,-.13])box('PE_BARASI_MESAFE_'+z,[6.162,1.082,z-.006],[6.173,1.102,z+.006],grey,'PE support, screwed to earthed mounting plate');
 for(const y of [1.28,1.50])box('PANO_KABLO_KANALI_'+y,[6.139,y-.021,-.403],[6.173,y+.021,-.060],grey,'closed internal DIN wiring trunk; screw fixed to plate');
 // ER605 is a wired router. WAN comes from the premises ONT/modem; machine PC remains in QR.
 box('TP_LINK_ER605',[6.133,1.49,-.022],[6.158,1.591,.136],dark,'158×101×25 mm router on own bolted cradle',null,'KONTROL');
 box('ER605_TUTUCU_ALT',[6.132,1.487,-.024],[6.173,1.490,.138],grey,'3 mm shelf on mounting plate',null,'KONTROL');
 for(let i=0;i<5;i++)box('ER605_RJ45_'+i,[6.122,1.505+i*.015,.121],[6.133,1.515+i*.015,.135],0x22272a,'router RJ45 socket',null,'KONTROL');
 box('AG_12V_ADAPTOR',[6.121,1.35,.02],[6.161,1.435,.095],dark,'purchased router 12V supply retained to plate',null,'KONTROL');
 box('AG_ADAPTOR_BRAKET',[6.161,1.348,.018],[6.173,1.437,.097],grey,'bolted retaining cradle for router adapter',null,'KONTROL');
 box('AG_WAN_RJ45',[6.126,1.21,.07],[6.166,1.25,.11],grey,'WAN feed termination on bolted cradle',null,'KONTROL');
 box('WAN_KONNEKTOR_BRAKET',[6.166,1.208,.068],[6.173,1.252,.112],grey,'bolted WAN bracket on plate',null,'KONTROL');
 // Real glands: annular sealing and strain-relief profiles surrounding each cable.
 for(const [i,x,z,r]of [[0,6.17,-.36,.005],[1,6.15,-.32,.004],[2,6.13,-.28,.005],[3,6.11,-.24,.004],[4,6.10,0,.003],[5,6.092,.022,.003],[6,6.084,.044,.003]]){
  const s=new T.Shape();s.absarc(0,0,r+.006,0,Math.PI*2,false);const h=new T.Path();h.absarc(0,0,r+.0002,0,Math.PI*2,true);s.holes.push(h);const geo=new T.ExtrudeGeometry(s,{depth:.014,bevelEnabled:false,curveSegments:12});geo.rotateX(Math.PI/2);add('PANO_IP68_RAKOR_'+i,geo,0x666f74,[x,1.004,z],'locknut to existing gland hole; sealed cable strain relief');
 }
 // Enclosed circuit-to-gland leads are separate lanes; incoming feeder/ONT provided by building.
 for(let i=0;i<4;i++){
  const z=-.36+i*.04,x=6.17-i*.02;
  const curve=new T.CubicBezierCurve3(new T.Vector3(6.14,1.164,z),new T.Vector3(6.14,1.09,z),new T.Vector3(x,1.075,z),new T.Vector3(x,1.004,z));
  add('PANO_CIKIS_IC_KABLO_'+i,cableMesh(curve.getPoints(48).map(p=>p.toArray()),.0035),0xbd3430,[0,0,0],'rounded retained terminal-to-gland lead');
 }
 return {enclosure_mm:[600,700,250],right_wall_x_m:wallX,cabinet_recess_m:.200,wall_thickness_m:.280,cabinet_recess_structural_approval:false,wall_outline_only:true,cabinet_centre_z_m:.960,router:'TP-Link ER605',electrical_schematic_certified:false};
}
