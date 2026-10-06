// One integrated customer-facing column. Door/lock safety is outside this layout.
import {rounded} from './routing_js.mjs';
export function qrCustomer({add,box,bolt,T,cableMesh,read}){
 const x0=5.230,x1=5.390,z0=1.750,z1=2.125,h=2.050,t=.002,metal=0xaeb8bd,dark=0x29373e;
 const make=(name,lo,hi,col=metal,connection='folded 2 mm sheet, M5 to QR frame')=>box('QR_KOLON_'+name,lo,hi,col,connection,null,'GOVDE');
 make('DUVAR_YANI',[x1-t,0,z0],[x1,h,z1]);
 make('ROBOT_YUZ',[x0,0,z0],[x1-t,h,z0+t]);
 make('UST',[x0,h-t,z0+t],[x1-t,h,z1-t]);
 box('QR_YENI_UST_ON_SAC',[3.757,1.653,2.081],[5.230,2.050,2.083],metal,'plain customer-facing QR header; old reader apertures removed',null,'GOVDE');
 // Bottom sheet has an actual 70 mm conduit entry; no cable through solid sheet.
 const bottom=new T.Shape([new T.Vector2(x0,z0+t),new T.Vector2(x1-t,z0+t),new T.Vector2(x1-t,z1-t),new T.Vector2(x0,z1-t)]);
 const entry=new T.Path([new T.Vector2(5.248,2.008),new T.Vector2(5.322,2.008),new T.Vector2(5.322,2.082),new T.Vector2(5.248,2.082)]);bottom.holes.push(entry);
 const bg=new T.ExtrudeGeometry(bottom,{depth:t,bevelEnabled:false});bg.rotateX(Math.PI/2);add('QR_KOLON_ALTI',bg,metal,[0,t,0],'folded sheet with real cable entry',null,'GOVDE');
 const front=new T.Shape([new T.Vector2(x0,0),new T.Vector2(x1-t,0),new T.Vector2(x1-t,h-t),new T.Vector2(x0,h-t)]);
 function hole(cx,cy,w,hh){const p=new T.Path([new T.Vector2(cx-w/2,cy-hh/2),new T.Vector2(cx+w/2,cy-hh/2),new T.Vector2(cx+w/2,cy+hh/2),new T.Vector2(cx-w/2,cy+hh/2)]);front.holes.push(p);}
 hole(5.310,1.430,.0435,.0263);hole(5.310,1.220,.084,.102);
 const fg=new T.ExtrudeGeometry(front,{depth:t,bevelEnabled:false});add('QR_KOLON_MUSTERI_YUZU',fg,metal,[0,0,z1-t],'front screwed to folded sides; scanner and keypad cutouts',null,'GOVDE');
 // Side flange touches existing right QR post, screws are outside the bay opening.
 for(const y of [.035,.58,1.11,1.65,2.02]){
  make('BAGLANTI_KULAK_'+y,[5.230,y-.012,1.754],[5.252,y+.012,1.780]);
  bolt('QR_KOLON_BAGLANTI_'+y,5.242,y,1.765,'Z');
 }
 const cad=read('keypad_cad.json'),centre=cad.centre_xy_mm.map(v=>v/1000),cadOffset=[5.310-centre[0],1.220-centre[1],2.125];
 const keypad=[];
 for(const p of cad.parts){const geo=new T.BufferGeometry();geo.setAttribute('position',new T.Float32BufferAttribute(p.vertices,3));geo.setIndex(p.indices);geo.computeVertexNormals();keypad.push(add('QR_STORM_'+p.name,geo,p.name==='KEYPAD'?0xced3d4:dark,cadOffset,'unchanged manufacturer STEP; front-panel mounting screws',null,'KONTROL'));}
 // Telephone legends are shallow markings only, never altered supplier CAD.
 const font={'1':[[.5,0,.5,1]],'2':[[0,1,1,1],[1,1,1,.5],[1,.5,0,.5],[0,.5,0,0],[0,0,1,0]],'3':[[0,1,1,1],[1,1,1,0],[0,.5,1,.5],[0,0,1,0]],'4':[[0,1,0,.5],[0,.5,1,.5],[1,1,1,0]],'5':[[1,1,0,1],[0,1,0,.5],[0,.5,1,.5],[1,.5,1,0],[1,0,0,0]],'6':[[1,1,0,1],[0,1,0,0],[0,0,1,0],[1,0,1,.5],[1,.5,0,.5]],'7':[[0,1,1,1],[1,1,.4,0]],'8':[[0,0,0,1],[0,1,1,1],[1,1,1,0],[1,0,0,0],[0,.5,1,.5]],'9':[[1,0,1,1],[1,1,0,1],[0,1,0,.5],[0,.5,1,.5]],'0':[[0,0,0,1],[0,1,1,1],[1,1,1,0],[1,0,0,0]],'*':[[0,0,1,1],[1,0,0,1],[0,.5,1,.5]],'#':[[.3,0,.3,1],[.7,0,.7,1],[0,.3,1,.3],[0,.7,1,.7]]};
 const legends=['1','2','3','4','5','6','7','8','9','*','0','#'];
 for(let i=0;i<12;i++){const cx=5.310+(i%3-1)*.025,cy=1.220+(.5-(Math.floor(i/3)-1))*.025,z=2.125+cad.front_z_mm/1000+.0002;for(const [j,seg]of font[legends[i]].entries()){const [a,b,c,d]=seg;add('QR_TUS_'+legends[i]+'_'+j,cableMesh([[cx+(a-.5)*.006,cy+(b-.5)*.008,z],[cx+(c-.5)*.006,cy+(d-.5)*.008,z]],.00035),dark,[0,0,0],'telephone legend marking',null,'KONTROL');}}
 // FM430 exact catalogue outer envelope (not a supplied manufacturer CAD file).
 const scanner=box('QR_NEWLAND_FM430',[5.28925,1.41785,2.0755],[5.33075,1.44215,2.125],dark,'41.5×49.5×24.3 mm FM430; USB powered, retained behind aperture',null,'KONTROL');
 box('QR_FM430_OPTIK_PENCERE',[5.2905,1.419,2.125],[5.3295,1.441,2.126],0x111921,'optical window, customer faces +Z',null,'KONTROL');
 make('OKUYUCU_BRAKET',[5.282,1.41585,2.0735],[5.338,1.41785,2.123]);
 for(const x of [5.283,5.337])make('OKUYUCU_MESAFE_'+x,[x,1.415,2.074],[x+.002,1.451,2.076]);
 for(const y of [1.177,1.263])for(const x of [5.268,5.352]){const gg=new T.CylinderGeometry(.0025,.0025,.018,10);gg.rotateX(Math.PI/2);add('QR_KEYPAD_M5_'+x+'_'+y,gg,0x667d8a,[x,y,2.120],'supplier 4-hole front flange to own panel',null,'GOVDE');}
 // Hidden controller bay below the first shelf; gland conduit terminates at this bay.
 make('ALT_PANO_PLAKA',[5.242,.200,2.065],[5.377,.445,2.067]);
 make('ALT_PANO_AYAK',[5.242,.002,2.065],[5.377,.200,2.067]);
 box('QR_ALT_KONTROL_MODULU',[5.250,.205,2.024],[5.365,.335,2.065],dark,'controller module directly on own screwed lower mounting plate; supplier selection pending',null,'KONTROL');
 box('QR_STORM_450_USB_ENCODER',[5.280,1.178,2.072],[5.342,1.245,2.090],0x316b53,'Storm 450 USB encoder behind keypad; connector/hole pattern to confirm',null,'KONTROL');
 make('ENCODER_TUTUCU',[5.278,1.176,2.090],[5.344,1.247,2.093]);
 make('ENCODER_MESAFE',[5.278,1.176,2.093],[5.281,1.247,2.123]);
 // Protected internal column trunk is behind controls, never on external QR face.
 make('IC_KANAL_SOL',[5.245,.335,1.960],[5.2465,1.480,2.020]);
 const trunkSide=new T.Shape([new T.Vector2(-2.020,.335),new T.Vector2(-1.960,.335),new T.Vector2(-1.960,1.480),new T.Vector2(-2.020,1.480)]);
 for(const y of [1.205,1.430])trunkSide.holes.push(new T.Path([new T.Vector2(-2.018,y-.027),new T.Vector2(-1.962,y-.027),new T.Vector2(-1.962,y+.027),new T.Vector2(-2.018,y+.027)]));
 const tg=new T.ExtrudeGeometry(trunkSide,{depth:.0015,bevelEnabled:false});tg.rotateY(Math.PI/2);add('QR_KOLON_IC_KANAL_SAG',tg,metal,[5.285,0,0],'two actual USB branch openings in retained internal trunk',null,'GOVDE');
 make('IC_KANAL_ARKA',[5.245,.335,1.9585],[5.2865,1.480,1.960]);
 const cover=new T.Shape([new T.Vector2(5.245,.335),new T.Vector2(5.2865,.335),new T.Vector2(5.2865,1.480),new T.Vector2(5.245,1.480)]);
 for(const [x,y]of [[5.255,.410],[5.272,.500]])cover.holes.push(new T.Path([new T.Vector2(x-.004,y-.030),new T.Vector2(x+.004,y-.030),new T.Vector2(x+.004,y+.030),new T.Vector2(x-.004,y+.030)]));
 add('QR_KOLON_IC_KANAL_KAPAK',new T.ExtrudeGeometry(cover,{depth:.0015,bevelEnabled:false}),metal,[0,0,2.020],'entry slots in cover aligned with rounded USB leads',null,'GOVDE');
 for(const y of [.40,.80,1.20,1.46])make('IC_KANAL_DESTEK_'+y,[5.244,y-.009,1.958],[5.248,y+.009,2.123]);
 const routes=[
  {name:'QR_OKUYUCU_USB',r:.0025,raw:[[5.255,.330,2.040],[5.255,.410,2.040],[5.255,.410,1.975],[5.255,1.430,1.975],[5.310,1.430,1.975],[5.310,1.430,2.0755]]},
  {name:'QR_TUS_USB',r:.0025,raw:[[5.272,.330,2.049],[5.272,.500,2.049],[5.272,.500,1.991],[5.272,1.205,1.991],[5.330,1.205,1.991],[5.330,1.205,2.072]]}
 ];
 for(const c of routes){const r=rounded(c.raw,.025);c.points=r.points;c.minimum_radius_m=r.minimum_radius_m;add(c.name,cableMesh(c.points,c.r),0x2a74be,[0,0,0],'USB 5V/data inside retained column trunk; R25 branch to module',null,'GUC');}
 add('QR_KEYPAD_MATRIX',cableMesh([[5.310,1.201,2.114],[5.310,1.201,2.090]],.0015),0x343c43,[0,0,0],'keypad rear matrix plug to Storm 450 encoder',null,'GUC');
 return {column_bounds:[[x0,0,z0],[x1,h,z1]],width_added_mm:160,customer_face:'+Z',cabinet_bays:12,external_locks_removed:true,keypad:{manufacturer:cad.manufacturer,model:cad.model,manufacturer_cad:true,source:cad.source,sha256:cad.source_step_sha256,dimensions_mm:cad.dimensions_mm,node_ids:keypad,usb_encoder_required:cad.usb_encoder_required},reader:{model:'Newland FM430 Barracuda USB',manufacturer_cad:false,dimensions_mm:[41.5,49.5,24.3],source:'https://www.newland-id.com/en/products/fixed-mount-scanners/fm430-barracuda',node:scanner},internal_usb_routes:routes,control_enclosure_certified:false};
}
