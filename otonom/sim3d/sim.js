/* AUTOKITCH 3D robot simülasyonu v3 — 18 Eyl 2026. mm · x hat boyu · y kot · z: hat yüzü 0, hat içi −, koridor +
   HAT v10 yerleşimi: A PRESS 0–700 · B ÇEKMECE 0–2500 (K1–K3 + K4 teknik/tepsi nişi) · C TOPPING 700–2500 · D FIRIN (altında içecek/tatlı çekmeceleri) 2500–3200 · E KUTU 3200–3900
   El: bilek → avuç Ø80 + merkez pim (tepsi soketi) + 2 paralel parmak (90 uzun, açıklık 20–140). Çatal yok; tepsi = el. */
const V = (x,y,z)=>new THREE.Vector3(x,y,z);
const ROBOT = {
  FR5:  {ad:"FR5 · 922 · 8.490 €",      d1:152, a2:425,  a3:395, taban:149},
  FR10: {ad:"FR10 · 1400 · 13.590 €",   d1:228, a2:700,  a3:536, taban:190},
  FR20: {ad:"FR20 · 1854 · 15.490 €",   d1:240, a2:1000, a3:813, taban:240},
  FR5WML:{ad:"FR5 WML · 1900 · 12.000 €", d1:152, a2:900, a3:850, taban:149}
};
/* el geometrisi (varsayım) — W bilek merkezi, t ileri, u yukarı */
const EL = {BILEK:100, AVUC:40, PIM:40, PARMAK:90, PARMAK_W:20, PARMAK_H:30, SAP:150, TEPSI_R:170, TABAN_R:150, TOP_R:47.5,
  KUTU:320, KUTU_H:45, KOLA_R:33, KOLA_H:115, TATLI_R:45, TATLI_H:60};
const YUK = {  // tcp = W + L t + P u  (yük merkezi)
  bos:{L:500,P:-20}, tepsi:{L:500,P:-20}, top:{L:187.5,P:0}, kola:{L:200,P:-42.5}, tatli:{L:200,P:-15}
};
const HAT = {yuk:2030, derin:830, B_yuk:1060};
const MOD = [["A · PRESS",0,700,1060,2030],["B · ÇEKMECE",0,2500,0,1060],["C · TOPPING",700,2500,1060,2030],["D · FIRIN + İÇECEK",2500,3200,0,2030],["E · KUTU",3200,3900,0,2030]];
const KOLON = {  // çekmeceler 620 × 680 — hamur: pide 4×5 (140 pitch) · lahm 5×7 (110/100) — içecek/tatlı D altında, 500 açılır, 5×6 (100 pitch), yükseltilmiş taban
  K1:{x0:62.5,  x1:682.5,  kotlar:[287.5,395.5,503.5,611.5,719.5,827.5], ic:75, tip:"pide", acik:700},
  K2:{x0:717.5, x1:1337.5, kotlar:[167.5,275.5,383.5,476.5,569.5,662.5,755.5,848.5], ic:60, tip:"karma", acik:700},
  K3:{x0:1372.5,x1:1992.5, kotlar:[167.5,260.5,353.5,446.5,539.5,632.5], ic:60, tip:"lahm", acik:700}
};
/* içecek + tatlı şarjörleri (D altı, çekmece yok): eğimli kanal kutuyu ön yuvaya yatık indirir; kap yığını dikey iner — robot yuvadan alır */
const YUVA={ kola:{x:2700,y:400,z:-75,yatay:true, b:[2600,2800,300,500,-160,100], n:45}, tatli:{x:2950,y:600,z:-75,yatay:false, b:[2860,3040,500,700,-160,100], n:24} };
const NIS={x:[2070,2455], y:[500,960], z:[-660,0], cx:2262, cz:-450, raf0:512, pitch:50, n:8};           // K4 tepsi nişi
const T_AGZ=[1070,1180], T_Y=1120, NOZ={kasar:{x:1910}, harc:{x:1350}, z:-310, alt:1183};                   // topping ağzı 730–2470
const FIR=[[1095,1406],[1411,1722],[1727,2030]];                                                            // göz: kapak y0+40..y1−40 · iç taban y0+100 · göz 1–2 lahm · göz 3 pide
const FIR_X={x:[2533,3167], ic:[2650,3050], cx:2850, cz:-360};
const KES={x:[2553,3147], y:[825,960], z:[-540,0], cx:2850, cz:-270};
const YAG={x:[2553,2920], y:[645,820], z:[-440,0], cx:2737, cz:-220};
const KUT={x:[3230,3870], y:[420,680], z:[-768,0], cx:3550, cz:-390, plaka:460, itme:360};                 // kutu plakası 460 · itici 360 strok → tepsiye
const QR ={x:[3040,3900], y:[400,2000], z:[900,1340], kol:[[3080,3460],[3480,3860]], satir:[410,610,810,1010,1210,1410], derin:440, goz_h:180};
const KOR=900, RAY_X=[200,3500];
const PRES_KIZAK={disari:230, iceri:-440};                                                                  // pres kızağı: tepsi ağız dışına çıkar (varsayım · Fersah'a sorulacak)
function PRES(){ const p=+plaka.value; return {x:[53,647], y:[p,p+180], z:[-650,0], cx:350, cz:-440, plaka:p}; }
/* hızlar (varsayım · FR5 katalog uç hızı 1 m/s) */
let HIZ={serbest:600, ince:200, mikro:80, ray:500, parmak:0.6, pim:0.8, cekmece:2.8, kapak:1.5, qrkapak:1.5, itici:2.0, kizak:2.0, pres:5, kasar:12, harc:15, firin:{pide:240, lahm:120}, kesim:4, sprey:3, kapan:4, musteri:150};

/* ================= SAHNE ================= */
const canvas=document.getElementById('c');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true}); renderer.setPixelRatio(Math.min(2,devicePixelRatio));
const scene=new THREE.Scene(); scene.background=new THREE.Color(0x0d1016);
const camera=new THREE.PerspectiveCamera(42,1,10,40000);
const controls=new THREE.OrbitControls(camera,canvas);
scene.add(new THREE.HemisphereLight(0xffffff,0x334455,1.0));
const dl=new THREE.DirectionalLight(0xffffff,.65); dl.position.set(1500,4000,3500); scene.add(dl);
const M=(c,o=1)=>new THREE.MeshLambertMaterial({color:c,transparent:o<1,opacity:o,side:THREE.DoubleSide});
function box(w,h,d,c,o=1){ return new THREE.Mesh(new THREE.BoxGeometry(w,h,d),M(c,o)); }
function edge(m,c=0x55606f){ m.add(new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry),new THREE.LineBasicMaterial({color:c}))); }
function aabb(x0,x1,y0,y1,z0,z1,c,o,ed){ const b=box(x1-x0,y1-y0,z1-z0,c,o); b.position.set((x0+x1)/2,(y0+y1)/2,(z0+z1)/2); if(ed!==false) edge(b, ed||0x55606f); scene.add(b); return b; }
aabb(-600,4600,-10,0,-1000,2400,0x1a1f28,1,false);
aabb(-600,4600,0,2400,KOR,KOR+60,0x1c212b,.5,false);
MOD.forEach(([ad,x0,x1,y0,y1],i)=>aabb(x0+2,x1-2,y0,y1,-HAT.derin,0,i%2?0x2a3140:0x2f3748,.42));
function agiz(x0,x1,y0,y1,z0,z1){ return aabb(x0,x1,y0,y1,z0,z1,0xff5c5c,.10,0xff5c5c); }
agiz(730,2470,T_AGZ[0],T_AGZ[1],-768,0); agiz(KES.x[0],KES.x[1],KES.y[0],KES.y[1],KES.z[0],KES.z[1]);
agiz(YAG.x[0],YAG.x[1],YAG.y[0],YAG.y[1],YAG.z[0],YAG.z[1]); agiz(KUT.x[0],KUT.x[1],KUT.y[0],KUT.y[1],KUT.z[0],KUT.z[1]);
agiz(NIS.x[0],NIS.x[1],NIS.y[0],NIS.y[1],NIS.z[0],NIS.z[1]);
[YUVA.kola,YUVA.tatli].forEach(y=>agiz(y.b[0],y.b[1],y.b[2],y.b[3],y.b[4],0));
const carPres=()=>Math.min(RAY_X[1],PRES().cx+350); const carFirin=()=>FIR_X.cx;   // fırın: araba tam önde (D'de çekmece yok)   // pres: araba kızağın sağında (kızak dışarıdayken omuz üstüne gelmesin)
const firinKapak=[];
FIR.forEach(f=>{ agiz(FIR_X.x[0],FIR_X.x[1],f[0]+40,f[1]-40,-160,0); agiz(FIR_X.ic[0],FIR_X.ic[1],f[0]+100,f[1]-100,-560,-160); aabb(FIR_X.ic[0],FIR_X.ic[1],f[0]+88,f[0]+100,-560,-160,0x8a6a4a,1);
  const k=box(FIR_X.x[1]-FIR_X.x[0],f[1]-f[0]-80,16,0xd08060,.9); edge(k,0x8a4a2a); scene.add(k); firinKapak.push({m:k,f}); });
const presAgiz=agiz(53,647,1640,1820,-650,0);
const kizakM=box(360,20,380,0xc0c6d0); scene.add(kizakM);
const qrKapak=[];
QR.kol.forEach((k,ci)=>QR.satir.forEach((y,ri)=>{ aabb(k[0],k[1],y,y+QR.goz_h,QR.z[0],QR.z[0]+QR.derin,0x2997ff,.12,0x3b6ea8);
  const d=box(k[1]-k[0]-10,QR.goz_h-10,14,0x5a6a80,.95); edge(d,0x8899aa); scene.add(d); qrKapak.push({m:d,x:(k[0]+k[1])/2,y,ci,ri}); }));
aabb(QR.x[0],QR.x[1],QR.y[0],QR.y[1],QR.z[0],QR.z[1],0x4a5568,.30);
const cekMesh={};
Object.entries(KOLON).forEach(([k,K])=>{ K.kotlar.forEach(y=>{ const f=box(K.x1-K.x0-16,K.ic+26,24,K.tip==='kola'?0x3f7fbf:K.tip==='tatli'?0xbf7f3f:0x3f9c7a); f.position.set((K.x0+K.x1)/2,y+(K.ic+30)/2,-12); scene.add(f); });
  const a=box(K.x1-K.x0-4,K.ic+26,K.acik,0x5fd3a8,.5); a.visible=false; scene.add(a); cekMesh[k]=a; });
const altPlaka=new THREE.Mesh(new THREE.CylinderGeometry(170,170,12,32),M(0xa0a6b0)); scene.add(altPlaka);
const ustPlaka=new THREE.Mesh(new THREE.CylinderGeometry(145,145,50,32),M(0x9aa3b2)); scene.add(ustPlaka);
const nozulK=new THREE.Mesh(new THREE.CylinderGeometry(30,18,120,16),M(0xd0a040)); nozulK.position.set(NOZ.kasar.x,NOZ.alt+60,NOZ.z); scene.add(nozulK);
const nozulH=new THREE.Mesh(new THREE.CylinderGeometry(30,18,120,16),M(0xc06040)); nozulH.position.set(NOZ.harc.x,NOZ.alt+60,NOZ.z); scene.add(nozulH);
const bicak=new THREE.Mesh(new THREE.CylinderGeometry(150,150,20,32),M(0xb0b8c4,.9)); bicak.position.set(KES.cx,KES.y[1]+100,KES.cz); scene.add(bicak);
aabb(KUT.cx-200,KUT.cx+200,KUT.plaka-10,KUT.plaka,KUT.cz-200,KUT.cz+200,0x8a94a4,1);
const itici=box(300,30,20,0xff8c40); scene.add(itici);
const ray=box(3900,120,120,0x2997ff); scene.add(ray);
const araba=box(400,140,300,0x3a4250); scene.add(araba);
const kaide=new THREE.Mesh(new THREE.CylinderGeometry(100,100,1,24),M(0x596273)); scene.add(kaide);
const tabanM=new THREE.Mesh(new THREE.CylinderGeometry(75,75,120,24),M(0x9aa3b2)); scene.add(tabanM);
const ustKol=new THREE.Mesh(new THREE.CylinderGeometry(45,45,1,16),M(0xe8eaed)); scene.add(ustKol);
const onKol=new THREE.Mesh(new THREE.CylinderGeometry(40,40,1,16),M(0xe8eaed)); scene.add(onKol);
const bilekM=new THREE.Mesh(new THREE.CylinderGeometry(35,35,1,16),M(0xb8bfc9)); scene.add(bilekM);
const eklem=[0,0,0].map(()=>{ const s=new THREE.Mesh(new THREE.SphereGeometry(50,16,12),M(0x2997ff)); scene.add(s); return s; });
const avucM=new THREE.Mesh(new THREE.CylinderGeometry(40,40,EL.AVUC,24),M(0x2997ff)); scene.add(avucM);
const pimM=new THREE.Mesh(new THREE.CylinderGeometry(10,10,EL.PIM,12),M(0xffb340)); scene.add(pimM);
const parmakM=[box(EL.PARMAK_W,EL.PARMAK_H,EL.PARMAK,0x7fb8ff),box(EL.PARMAK_W,EL.PARMAK_H,EL.PARMAK,0x7fb8ff)]; parmakM.forEach(m=>scene.add(m));
function havuz(n,mk){ const a=[]; for(let i=0;i<n;i++){ const g=mk(); g.visible=false; scene.add(g); a.push(g); } return a; }
function mkTepsi(){ const g=new THREE.Group(); const t=new THREE.Mesh(new THREE.CylinderGeometry(EL.TEPSI_R,EL.TEPSI_R,10,40),M(0xd8dde6)); g.add(t);
  const sap=box(30,30,EL.SAP,0xb0b8c4); sap.position.set(0,20,EL.TEPSI_R+EL.SAP/2); g.add(sap); const sok=box(34,34,30,0x2997ff); sok.position.set(0,20,EL.TEPSI_R+EL.SAP-15); g.add(sok);
  const taban=new THREE.Mesh(new THREE.CylinderGeometry(EL.TABAN_R,EL.TABAN_R,8,40),M(0xf0d9a8)); taban.position.y=9; g.add(taban); g.userData.taban=taban;
  const kas=new THREE.Mesh(new THREE.CylinderGeometry(140,140,5,40),M(0xffd24a)); kas.position.y=15.5; g.add(kas); g.userData.kasar=kas;
  const kutu=box(EL.KUTU,EL.KUTU_H,EL.KUTU,0xe0c890,1); edge(kutu,0xa08a5a); kutu.position.y=27.5; g.add(kutu); g.userData.kutu=kutu; return g; }
const HAVUZ={ tepsi:havuz(NIS.n,mkTepsi),
  kutu:havuz(24,()=>{ const b=box(EL.KUTU,EL.KUTU_H,EL.KUTU,0xe0c890,1); edge(b,0xa08a5a); return b; }),
  kola:havuz(40,()=>new THREE.Mesh(new THREE.CylinderGeometry(EL.KOLA_R,EL.KOLA_R,EL.KOLA_H,16),M(0xd03030))),
  tatli:havuz(40,()=>new THREE.Mesh(new THREE.CylinderGeometry(EL.TATLI_R,EL.TATLI_R-6,EL.TATLI_H,16),M(0xf5e6c8))),
  top:havuz(40,()=>new THREE.Mesh(new THREE.SphereGeometry(EL.TOP_R,16,12),M(0xf0d9a8))) };
const temasM=havuz(24,()=>new THREE.Mesh(new THREE.SphereGeometry(22,10,8),new THREE.MeshBasicMaterial({color:0xff2d2d})));
const erisimW=new THREE.LineSegments(new THREE.WireframeGeometry(new THREE.SphereGeometry(1,18,12)),new THREE.LineBasicMaterial({color:0x2997ff,transparent:true,opacity:.12})); scene.add(erisimW);

/* ================= DURUM ================= */
const S={carX:1100, tcp:V(1400,1300,220), t:V(0,0,-1), u:V(0,1,0), yuk:'bos', tasi:null, parmak:70,
  cek:{}, cekI:{}, kapak:[0,0,0], qrk:{}, itme:0, kizak:1, ustPlakaY:0, bicakY:0, nesne:[], sonIK:null, temas:[]};
Object.keys(KOLON).forEach(k=>{ S.cek[k]=0; S.cekI[k]=0; });
const $=id=>document.getElementById(id);
const model=$('model'), omuz=$('omuz'), railz=$('railz'), pay=$('pay'), hiz=$('hiz'), plaka=$('plaka'), out=$('out'), step=$('step'), log=$('log');
Object.entries(ROBOT).forEach(([k,r])=>{ const o=document.createElement('option'); o.value=k; o.textContent=r.ad; model.appendChild(o); });
const R=()=>ROBOT[model.value], railZ=()=>+railz.value, omuzY=()=>+omuz.value, tabanY=()=>omuzY()-R().d1;
const xAxis=()=>V(0,0,0).crossVectors(S.u,S.t).normalize();
function Wof(st){ const y=YUK[st.yuk]; return st.tcp.clone().addScaledVector(st.t,-y.L).addScaledVector(st.u,-y.P); }
function tcpOf(W,st,yuk){ const y=YUK[yuk]; return W.clone().addScaledVector(st.t,y.L).addScaledVector(st.u,y.P); }
/* dünya nesneleri: {tip, pos, icerik, kapali, mesh} */
function nesneGoster(n){ if(!n.mesh){ n.mesh=HAVUZ[n.tip].find(m=>!m.visible&&!m.userData.sahip); if(!n.mesh) return; n.mesh.userData.sahip=n; } n.mesh.visible=true; if(S.nesne.indexOf(n)<0) S.nesne.push(n); }
function nesneSil(n){ if(n.mesh){ n.mesh.visible=false; n.mesh.userData.sahip=null; n.mesh=null; } const i=S.nesne.indexOf(n); if(i>=0) S.nesne.splice(i,1); if(S.tasi===n) S.tasi=null; }

/* ================= ENGELLER / BOŞLUKLAR ================= */
function cavities(){
  const P=PRES(), c=[{ad:"pres ağzı",b:[P.x[0],P.x[1],P.y[0],P.y[1],P.z[0],100]},
    {ad:"topping ağzı",b:[730,2470,T_AGZ[0],T_AGZ[1],-768,100]},
    {ad:"kesim ağzı",b:[KES.x[0],KES.x[1],KES.y[0],KES.y[1],KES.z[0],100]},
    {ad:"sprey ağzı",b:[YAG.x[0],YAG.x[1],YAG.y[0],YAG.y[1],YAG.z[0],100]},
    {ad:"kutulama ağzı",b:[KUT.x[0],KUT.x[1],KUT.y[0],KUT.y[1],KUT.z[0],100]},
    {ad:"tepsi nişi",b:[NIS.x[0],NIS.x[1],NIS.y[0],NIS.y[1],NIS.z[0],100]}, {ad:"içecek yuvası",b:YUVA.kola.b}, {ad:"tatlı yuvası",b:YUVA.tatli.b}];
  FIR.forEach((f,i)=>{ if(S.kapak[i]>0.95) c.push({ad:"fırın kapağı "+(i+1),b:[FIR_X.x[0],FIR_X.x[1],f[0]+40,f[1]-40,-200,100]}); c.push({ad:"fırın iç "+(i+1),b:[FIR_X.ic[0],FIR_X.ic[1],f[0]+100,f[1]-100,-560,-160]}); });
  qrKapak.forEach((q,i)=>{ if((S.qrk[i]||0)>0.95) c.push({ad:"QR göz",b:[q.x-190,q.x+190,q.y-15,q.y+QR.goz_h,QR.z[0]-100,QR.z[0]+QR.derin]}); });
  Object.entries(KOLON).forEach(([k,K])=>{ const a=S.cek[k]||0; if(a>0.02) c.push({ad:"açık "+k,b:[K.x0+20,K.x1-20,K.kotlar[S.cekI[k]]+12,K.kotlar[S.cekI[k]]+2000,20,a*K.acik-20]}); });
  return c;
}
function solids(){
  const s=MOD.map(([ad,x0,x1,y0,y1])=>({ad,b:[x0,x1,y0,y1,-HAT.derin,0]}));
  s.push({ad:"zemin",b:[-9000,9000,-500,0,-9000,9000]}, {ad:"koridor duvarı",b:[-9000,9000,0,3000,KOR,KOR+300]}, {ad:"QR dolabı",b:[QR.x[0],QR.x[1],QR.y[0],QR.y[1],QR.z[0],QR.z[1]]},
    {ad:"ray + araba",b:[S.carX-200,S.carX+200,0,260,railZ()-150,railZ()+150]}, {ad:"robot kaidesi",b:[S.carX-100,S.carX+100,0,tabanY(),railZ()-100,railZ()+100]});
  Object.entries(KOLON).forEach(([k,K])=>{ const a=S.cek[k]||0; if(a>0.02){ const y=K.kotlar[S.cekI[k]]; s.push({ad:"açık çekmece "+k,b:[K.x0,K.x1,y,y+K.ic+30,0,a*K.acik]}); } });
  FIR.forEach((f,i)=>{ const a=S.kapak[i]||0; if(a>0.05) s.push({ad:"açık fırın kapağı "+(i+1),b:[FIR_X.x[0],FIR_X.x[1],f[1]-40-16,f[1]-40,0,a*(f[1]-f[0]-80)]}); });
  qrKapak.forEach((q,i)=>{ const a=S.qrk[i]||0; if(a>0.05) s.push({ad:"açık QR kapağı",b:[q.x-185,q.x+185,q.y-14,q.y,QR.z[0]-a*(QR.goz_h-10),QR.z[0]]}); });   // alttan menteşeli: açıkken öne yatar (rampa)
  if(S.kizak>0.02){ const P=PRES(); const z=P.cz+(PRES_KIZAK.disari-P.cz)*S.kizak; s.push({ad:"pres kızağı",b:[P.cx-180,P.cx+180,P.plaka-20,P.plaka,z-190,z+190]}); }
  return s;
}
/* ================= IK ================= */
function ik(W){
  const r=R(), Sh=V(S.carX,omuzY(),railZ());
  const dx=W.x-Sh.x, dz=W.z-Sh.z, h=W.y-Sh.y, rr=Math.hypot(dx,dz), D=Math.hypot(rr,h);
  const maxD=(r.a2+r.a3)*(+pay.value), minD=Math.abs(r.a2-r.a3)+20, ok=D<=maxD&&D>=minD;
  const Duse=Math.min(Math.max(D,minD),r.a2+r.a3-1), dir=rr>1?V(dx,0,dz).normalize():V(0,0,-1);
  const cosE=(r.a2*r.a2+Duse*Duse-r.a3*r.a3)/(2*r.a2*Duse), acs=Math.acos(Math.max(-1,Math.min(1,cosE))), base=Math.atan2(h,rr);
  const Wg=ok?W.clone():Sh.clone().addScaledVector(V(dx,h,dz).normalize(),Duse);
  const sol=[base+acs,base-acs].map(th=>{ const E=Sh.clone().addScaledVector(dir,r.a2*Math.cos(th)); E.y=Sh.y+r.a2*Math.sin(th);
    const Wr=ok?W.clone():E.clone().add(Wg.clone().sub(E).normalize().multiplyScalar(r.a3)); return {E,W:Wr,hits:kolTemas(Sh,E,Wr)}; });
  sol.sort((a,b)=>a.hits-b.hits||b.E.y-a.E.y);
  return {ok,D,maxD,Sh,E:sol[0].E,W:sol[0].W,dirsek:sol[0].E.y>=Sh.y?'yukarı':'aşağı'};
}
function inside(p,b,r){ return p.x>b[0]-r&&p.x<b[1]+r&&p.y>b[2]-r&&p.y<b[3]+r&&p.z>b[4]-r&&p.z<b[5]+r; }
function insideShrunk(p,b,r){ return p.x>b[0]+r&&p.x<b[1]-r&&p.y>b[2]+r&&p.y<b[3]-r&&p.z>b[4]+r&&p.z<b[5]-r; }
function kolTemas(Sh,E,W){ const sol=solids(), cav=cavities(); let n=0;
  const test=(a,b,r,skip)=>{ const m=Math.max(2,Math.ceil(a.distanceTo(b)/50)); for(let i=0;i<=m;i++){ const p=a.clone().lerp(b,i/m); if(p.distanceTo(a)<skip) continue; for(const s of sol){ if(s.ad==='robot kaidesi'||!inside(p,s.b,r)) continue; let ex=false; for(const c of cav){ if(insideShrunk(p,c.b,r*0.6)){ ex=true; break; } } if(!ex){ n++; break; } } } };
  test(Sh,E,45,120); test(E,W,40,0); return n; }
/* ================= ÇARPIŞMA ÖRNEKLEMİ ================= */
function orneklem(k){
  const pts=[], seg=(a,b,r,ad,skip=0)=>{ const n=Math.max(2,Math.ceil(a.distanceTo(b)/40)); for(let i=0;i<=n;i++){ const p=a.clone().lerp(b,i/n); if(p.distanceTo(a)<skip) continue; pts.push({p,r,parca:ad}); } };
  const W=k.W, t=S.t, u=S.u, x=xAxis(), pt=(tt,uu,xx=0)=>W.clone().addScaledVector(t,tt).addScaledVector(u,uu).addScaledVector(x,xx);
  seg(k.Sh,k.E,45,"üst kol",120); seg(k.E,k.W,40,"ön kol"); seg(W,pt(EL.BILEK,0),35,"bilek");
  pts.push({p:pt(EL.BILEK+20,0),r:42,parca:"avuç"}); seg(pt(EL.BILEK+EL.AVUC,0),pt(EL.BILEK+EL.AVUC+EL.PIM,0),10,"pim");
  const g=S.parmak/2+EL.PARMAK_W/2; for(const sx of [-g,g]) for(const uu of [-15,15]) for(const xx of [-10,10]) seg(pt(EL.BILEK+EL.AVUC,uu,sx+xx),pt(EL.BILEK+EL.AVUC+EL.PARMAK,uu,sx+xx),3,"parmak");
  const c=tcpOf(W,S,S.yuk), n=S.tasi;
  if(n&&n.tip==='tepsi'){ for(let i=0;i<16;i++){ const a=i/16*Math.PI*2; pts.push({p:c.clone().addScaledVector(x,170*Math.cos(a)).addScaledVector(t,170*Math.sin(a)),r:5,parca:"tepsi"});
      if(n.icerik&&n.icerik!=='kutu') pts.push({p:c.clone().addScaledVector(x,150*Math.cos(a)).addScaledVector(t,150*Math.sin(a)).addScaledVector(u,12),r:6,parca:"pide"}); }
    for(const uu of [5,35]) for(const xx of [-15,15]) seg(pt(EL.BILEK+EL.AVUC+EL.PIM,uu-20,xx),pt(EL.BILEK+EL.AVUC+EL.PIM+EL.SAP,uu-20,xx),3,"sap");
    if(n.icerik==='kutu') for(const a of [-160,160]) for(const b of [-160,160]) for(const cc of [5,50]) pts.push({p:c.clone().addScaledVector(x,a).addScaledVector(t,b).addScaledVector(u,cc),r:3,parca:"kutu"}); }
  else if(n&&n.tip==='top') pts.push({p:c.clone(),r:EL.TOP_R,parca:"hamur topu"});
  else if(n&&(n.tip==='kola'||n.tip==='tatli')){ const rr=n.tip==='kola'?EL.KOLA_R:EL.TATLI_R, hh=n.tip==='kola'?EL.KOLA_H:EL.TATLI_H; for(const uu of [-hh/2,hh/2]) for(let i=0;i<8;i++){ const a=i/8*Math.PI*2; pts.push({p:c.clone().addScaledVector(x,rr*Math.cos(a)).addScaledVector(t,rr*Math.sin(a)).addScaledVector(u,uu),r:4,parca:n.tip}); } }
  return pts;
}
function carpisma(k){
  const sol=solids(), cav=cavities(), hits=[];
  for(const q of orneklem(k)){ for(const s of sol){ if(s.ad==='robot kaidesi'&&(q.parca==='üst kol'||q.parca==='ön kol')) continue; if(!inside(q.p,s.b,q.r)) continue; let ex=false; for(const c of cav){ if(insideShrunk(q.p,c.b,q.r*0.6)){ ex=true; break; } } if(!ex){ hits.push({p:q.p,parca:q.parca,engel:s.ad}); break; } } }
  return hits;
}
