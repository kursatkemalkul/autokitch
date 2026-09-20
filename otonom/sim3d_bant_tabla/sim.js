/* AUTOKITCH 3D simülasyon · BANTLI HAT v6 / ATOSA TABLALI HAT v2 — 19 Eyl 2026 · TEK ROBOT.
   mm · x hat boyu · y kot · z: hat yüzü 0, hat içi −, koridor +
   KAYNAK PAFTALAR: FULL_MAKINE/HAT_BANTLI_v6_teknik.png · HAT_ATOSA_TABLALI_v2_teknik.png (A + B = HAT 2 KOL v19).
   Ürün TEPSİSİZ akar: pres → (bant | tabla arabası) → konveyör fırın → kesme plakası → kutu. Robot yalnız: hamur topu çekmeceden prese / tablaya ·
   kapalı kutuyu (kutu tepsisiyle) QR gözüne · içecek + tatlıyı K3 üstü çekmeceden QR gözüne. Robot, el, IK, çarpışma motoru sim3d (HAT v19) ile aynı. */
const V = (x,y,z)=>new THREE.Vector3(x,y,z);
const HATTIP = (new URLSearchParams(location.search).get('hat')==='tabla')?'tabla':'bant';
const TABLA = HATTIP==='tabla';
const PK = TABLA?1340:1150;                 // süreç kotu: bant üstü / tabla seyir kotu = fırın bandı = kesme plakası
const EKSEN = -270;                         // bant · tabla · fırın bandı · kesme plakası · kutu ekseni (z)
const ROBOT = {
  FR5:  {ad:"FR5 · 922 · 8.490 €",      d1:152, a2:425,  a3:395, taban:149},
  FR10: {ad:"FR10 · 1400 · 13.590 €",   d1:228, a2:700,  a3:536, taban:190}
};
const EL = {BILEK:100, AVUC:40, PIM:40, PARMAK:90, PARMAK_W:8, PARMAK_H:30, SAP:150, TEPSI_R:170, TABAN_R:150, TOP_R:47.5,
  KUTU:320, KUTU_H:45, KOLA_R:33, KOLA_H:115, TATLI_R:45, TATLI_H:60};
const YUK = { bos:{L:500,P:-20}, tepsi:{L:500,P:-20}, top:{L:232.5,P:0}, kola:{L:242.5,P:0}, tatli:{L:230,P:-15} };
const HAT = {yuk:2030, derin:830, B_yuk:1060, boy:5300};
const MOD = [["A · PRESS",0,700,1060,2030],["B · ÇEKMECE",0,2500,0,1060],["C · TOPPING",700,2500,1060,2030],["F · KONVEYÖR FIRIN",2500,4000,0,2030],["K · KESME" + (new URLSearchParams(location.search).get("icecek")!=="sol" ? " + İÇECEK" : ""),4000,4600,0,2030],["E · KUTU",4600,5300,0,2030]];
const KOLON = {
  K1:{x0:62.5,  x1:682.5,  kotlar:[167.5,275.5,383.5,491.5,599.5,707.5], ic:75, tip:"pide", acik:700},
  K2:{x0:717.5, x1:1337.5, kotlar:[167.5,275.5,383.5,476.5,569.5,662.5,755.5,848.5], ic:60, tip:"karma", acik:700},
  K3:{x0:1372.5,x1:1992.5, kotlar:[167.5,260.5,353.5,446.5,539.5,632.5], ic:60, tip:"lahm", acik:700},
  KI:{x0:1372.5,x1:1992.5, kotlar:[725.5,862.5], ic:104, tip:"icecek", acik:700, yanAcik:true}
};
/* İÇECEK ÇEKMECESİ SAĞ UÇTA (Kemal 20 Eyl 2026): K·KESME modülünün altına, QR dolabının hemen soluna alındı →
   2 robotta SAĞ robot içecek için hattın soluna inmez, iki robot birbirini beklemez. ?icecek=sol ile eski yeri. */
const ICECEK_SAG = new URLSearchParams(location.search).get('icecek')!=='sol';
if(ICECEK_SAG){ KOLON.KI.x0=3890; KOLON.KI.x1=4510; }
function icecekPos(tip,kat,k){ const K=KOLON.KI, y0=K.kotlar[kat]+12; return tip==='kola'?(k<16?V(K.x0+216+116*(k%2), y0+EL.KOLA_H/2, 62+75*Math.floor(k/2)):V(K.x0+100, y0+EL.KOLA_H/2, 62+75*(k-16))):V(K.x1-60-100*Math.floor(k/5), y0+EL.TATLI_H/2, 200+95*(k%5)); }
/* C · TOPPING: 6 hazne tek sıra (pafta: bantlıda v19 yerleri, tablalıda 30 sola) · başlık + hazne kotları */
const T_BAS = TABLA?[1490,1624]:[1183,1317], T_KAS = TABLA?[1627,1987]:[1320,1680], KAY = TABLA?-30:0;
const HAZNE = [["HARÇ 1",280,1070+KAY,0xc06040],["HARÇ 2",280,1350+KAY,0xc06040],["KIYMA",140,1560+KAY,0x9a5a3a],["KUŞBAŞI",140,1700+KAY,0x8a4a3a],["KAŞAR",280,1910+KAY,0xffd24a],["SUCUK",180,2140+KAY,0xb03a2a]];
const NOZ = {kasar:{x:1910+KAY,renk:0xffd24a}, harc:{x:1350+KAY,renk:0xb0402a}, harc2:{x:1070+KAY,renk:0xb0402a}, z:EKSEN, alt:T_BAS[0]};
/* makine geometrisi */
const BANT = {x0:640, x1:2500, giris:810, cikis:2500, gen:400};            // bantlı: topping bandı (ürün merkezi 810'da banda iner, 2500'de fırın bandına geçer)
const TAB  = {ray:[90,2460], pres:350, firin:2330, kalk:100};               // tablalı: tabla arabası (pres altı 350 · fırın ağzı 2330 · dozajda 100 kalkar)
const FIRIN = {x:[2500,4000], hz:[2550,3950], y:[PK-300,PK+320], hazne:1400, adim:350};
const KESP = {cx:4300, cz:EKSEN, w:560, d:450};
const KUT = {x:[4630,5270], y:[PK-90,PK+160], z:[-768,0], cx:4950, cz:EKSEN, trayY:PK-60};   // kutu tepsisi ağızda, kutu dolum konumunda bekler (tepsi yüzü PK−60 → kutu üstü PK−10)
const QR = {x:[4295,5300], y:[400,2000], z:[900,1340], kol:[[4310,4790],[4810,5290]], satir:[410,610,810,1010,1210,1410], derin:440, goz_h:190,
  serit:78, kutuX:305, tatliZ:965, kolaZ:1080, kutuZ:1165};
const KOR=900, DUVAR_X=[0,5300]; let RAY_X=[200,5100];
function PRES(){ return TABLA?{x:[53,647], y:[PK,PK+220], z:[-650,0], cx:350, cz:EKSEN, plaka:PK}:{x:[53,647], y:[PK,PK+220], z:[-650,0], cx:350, cz:-440, plaka:PK}; }
const carPres=()=>PRES().cx+400;
/* hızlar · süreler — kaynak/varsayım notu index.html altında */
let HIZ={serbest:600, orta:400, ince:200, mikro:80, ray:500, ivmeKol:2000, ivmeRay:1000, eklem:150, parmak:0.6, pim:0.8, cekmece:2.8, kapak:1.5, qrkapak:1.5, itici:2.0,
  pres:9, kasar:15, harc:20, pisme:240, kesim:4, sprey:3, kapan:4, musteri:150,
  gecis:5, bantV:15, plakaGecis:3, katla:15, kutuKoy:1, tablaV:500, tablaZ:1, geriEm:1.5, siyir:1, it:1.2,
  atosaTur:60};   // atosaTur: ÜRETİCİ VERİSİ · Auto Pizza Artisan broşürü ≤ 1 dk / pizza → tabla bir ürünü 60 sn'den hızlı çeviremez (Kemal 15 Eyl + 19 Eyl: kendi dozaj varsayımımla kısaltma)

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
function silindir(r0,r1,h,c,o=1,n=24){ return new THREE.Mesh(new THREE.CylinderGeometry(r0,r1,h,n),M(c,o)); }
aabb(-600,6000,-10,0,-1000,2400,0x1a1f28,1,false);
aabb(-600,6000,0,2400,KOR,KOR+60,0x1c212b,.5,false);
MOD.forEach(([ad,x0,x1,y0,y1],i)=>aabb(x0+2,x1-2,y0,y1,-HAT.derin,0,i%2?0x2a3140:0x2f3748,.30));
function agiz(x0,x1,y0,y1,z0,z1){ return aabb(x0,x1,y0,y1,z0,z1,0xff5c5c,.10,0xff5c5c); }
const presAgiz=agiz(53,647,PK,PK+220,-650,0);
agiz(KUT.x[0],KUT.x[1],KUT.y[0],KUT.y[1],KUT.z[0],KUT.z[1]);
aabb(2035,2420,375,675,-820,-6,0xd9b04a,1,0x20242c); aabb(2035,2420,140,360,-306,-6,0x5a6472,1,0x20242c);   // K4: kaşar + sucuk deposu · soğutma grubu
aabb(2560,3200,135,270,-400,-6,0x5a6472,1,0x20242c);                                                       // F tabanı: robot kontrol kutusu (ray yanında)
if(TABLA){ aabb(2560,2960,320,670,-260,-6,0x4a5a72,1,0x20242c); aabb(2980,3230,320,670,-260,-6,0x3a4250,1,0x20242c); }   // tablalı: ana pano + UPS F tabanında
/* C · 6 hazne + dozaj başlığı + çıkış */
HAZNE.forEach(([ad,gw,xc,renk])=>{ aabb(xc-gw/2+6,xc+gw/2-6,T_KAS[0]+8,T_KAS[1]-8,NOZ.z-200,NOZ.z+200,renk,1,0x20242c);
  aabb(xc-(TABLA?45:150),xc+(TABLA?45:150),T_BAS[0]+30,T_BAS[1],NOZ.z-90,NOZ.z+90,0x6a7484,.9);
  const n=TABLA?silindir(22,16,26,0xe8eaed):box(300,14,60,0xe8eaed); n.position.set(xc,NOZ.alt+(TABLA?13:22),NOZ.z); scene.add(n); });
const akisM=silindir(7,7,1,0xffffff,.9,10); akisM.visible=false; scene.add(akisM);
/* A · pres */
const altPlaka=silindir(170,170,12,0xa0a6b0,1,32); scene.add(altPlaka); altPlaka.visible=!TABLA;
const ustPlaka=silindir(145,145,50,0x9aa3b2,1,32); scene.add(ustPlaka);
/* bant | tabla */
let tablaM=null, tablaKol=null;
if(TABLA){ aabb(TAB.ray[0],TAB.ray[1],1085,1120,EKSEN-30,EKSEN+30,0x2997ff,1);                        // tabla rayı
  aabb(180,520,1220,PK-14,EKSEN-170,EKSEN+170,0x6a7484,.9);                                           // sabit örs
  aabb(730,2470,1210,1240,-760,-10,0x3a4250,.6);                                                     // damlama tavası
  tablaM=silindir(170,170,12,0xcfe2ff,1,40); scene.add(tablaM); tablaKol=silindir(22,22,1,0x8a94a4,1,12); scene.add(tablaKol); }
else { aabb(BANT.x0,BANT.x1,PK-60,PK-2,EKSEN-BANT.gen/2,EKSEN+BANT.gen/2,0x9fc2ff,.85,0x3b6ea8); }
/* F · konveyör fırın: hazne (sıcak) + bant */
aabb(FIRIN.hz[0],FIRIN.hz[1],FIRIN.y[0]+50,FIRIN.y[1]-50,EKSEN-250,EKSEN+250,0xff7a3a,.10,0xc8602a);
aabb(FIRIN.x[0]-60,FIRIN.x[1]+30,PK-10,PK-2,EKSEN-225,EKSEN+225,0xd08060,.95,0x8a4a2a);
aabb(FIRIN.x[0]+35,FIRIN.x[1]-35,FIRIN.y[1]+10,2026,-790,-6,0x3a4250,.35);                          // davlumbaz
/* K · kesme plakası + yıldız bıçak + itici */
aabb(KESP.cx-KESP.w/2,KESP.cx+KESP.w/2,PK-14,PK-2,KESP.cz-KESP.d/2,KESP.cz+KESP.d/2,0x9fc2ff,.9,0x3b6ea8);
const bicak=silindir(150,150,20,0xb0b8c4,.9,6); scene.add(bicak);
const itici=box(30,50,300,0xff8c40); scene.add(itici);
/* QR dolabı */
const qrKapak=[];
QR.kol.forEach((k,ci)=>QR.satir.forEach((y,ri)=>{ aabb(k[0],k[1],y,y+QR.goz_h,QR.z[0],QR.z[0]+QR.derin,0x2997ff,.12,0x3b6ea8);
  aabb(k[0]+131,k[0]+134,y,y+20,QR.z[0]+20,QR.z[0]+QR.derin-20,0x3b6ea8,.9,false);
  const d=box(k[1]-k[0]-10,QR.goz_h-10,14,0x5a6a80,.95); edge(d,0x8899aa); scene.add(d); qrKapak.push({m:d,x:(k[0]+k[1])/2,k0:k[0],y,ci,ri}); }));
aabb(QR.x[0],QR.x[1],QR.y[0],QR.y[1],QR.z[0],QR.z[1],0x4a5568,.30);
const cekMesh={};
Object.entries(KOLON).forEach(([k,K])=>{ K.kotlar.forEach(y=>{ const f=box(K.x1-K.x0-16,K.ic+26,24,K.tip==='icecek'?0x3f7fbf:0x3f9c7a); f.position.set((K.x0+K.x1)/2,y+(K.ic+30)/2,-12); scene.add(f); });
  const a=box(K.x1-K.x0-4,K.tip==='icecek'?30:K.ic+26,K.acik,K.tip==='icecek'?0x6fb0ff:0x5fd3a8,.5); a.visible=false; scene.add(a); cekMesh[k]=a; });
const ray=box(HAT.boy,120,120,0x2997ff); scene.add(ray);
function mkRobotM(renk){ const o={}; const ek=m=>{ scene.add(m); return m; };
  o.araba=ek(box(400,140,300,0x3a4250)); o.kaide=ek(silindir(100,100,1,0x596273)); o.tabanM=ek(silindir(75,75,120,0x9aa3b2));
  o.ustKol=ek(silindir(45,45,1,0xe8eaed,1,16)); o.onKol=ek(silindir(40,40,1,0xe8eaed,1,16)); o.bilekM=ek(silindir(35,35,1,0xb8bfc9,1,16));
  o.eklem=[0,0,0].map(()=>ek(new THREE.Mesh(new THREE.SphereGeometry(50,16,12),M(renk)))); o.avucM=ek(silindir(40,40,EL.AVUC,renk)); o.pimM=ek(silindir(10,10,EL.PIM,0xffb340,1,12));
  o.parmakM=[ek(box(EL.PARMAK_W,EL.PARMAK_H,EL.PARMAK,0x7fb8ff)),ek(box(EL.PARMAK_W,EL.PARMAK_H,EL.PARMAK,0x7fb8ff))];
  o.hepsi=[o.araba,o.kaide,o.tabanM,o.ustKol,o.onKol,o.bilekM,o.avucM,o.pimM].concat(o.eklem,o.parmakM); return o; }
const ROBM=[mkRobotM(0x2997ff),mkRobotM(0xff8c40)];   /* 2. robot (turuncu): hattın sağ ucunda, kutu + QR + içecek */
function havuz(n,mk){ const a=[]; for(let i=0;i<n;i++){ const g=mk(); g.visible=false; scene.add(g); a.push(g); } return a; }
function mkKutu(){ const g=new THREE.Group(), K=EL.KUTU, H=EL.KUTU_H, c=0xe0c890; const tb=box(K,4,K,c); tb.position.y=-H/2+2; g.add(tb);
  [[0,K/2-2,K,4],[0,-K/2+2,K,4],[K/2-2,0,4,K],[-K/2+2,0,4,K]].forEach(([x,z,w,d])=>{ const b=box(w,H,d,c); b.position.set(x,0,z); g.add(b); });
  const pd=silindir(150,150,10,0xd9a45a,1,32); pd.position.y=-H/2+10; pd.visible=false; g.add(pd); g.userData.pide=pd;
  const mnt=new THREE.Group(); mnt.position.set(0,H/2,-K/2); const kp=box(K,4,K,0xd8be84); edge(kp,0xa08a5a); kp.position.set(0,0,K/2); mnt.add(kp); g.add(mnt); g.userData.kapak=mnt; return g; }
function kutuGoster(g,n){ g.userData.pide.visible=n.icerik==='pide'&&!n.kapali; g.userData.kapak.rotation.x=-(1-(n.kapanma===undefined?(n.kapali?1:0):n.kapanma))*Math.PI*0.58; }
function mkTepsi(){ const g=new THREE.Group(); const t=silindir(EL.TEPSI_R,EL.TEPSI_R,10,0xd8dde6,1,40); g.add(t);
  const sap=box(30,30,EL.SAP,0xb0b8c4); sap.position.set(0,20,EL.TEPSI_R+EL.SAP/2); g.add(sap); const sok=box(34,34,30,0x2997ff); sok.position.set(0,20,EL.TEPSI_R+EL.SAP-15); g.add(sok);
  const kutu=mkKutu(); kutu.position.y=5+EL.KUTU_H/2; g.add(kutu); g.userData.kutu=kutu; return g; }
/* ürün: hamur topu → basılmış taban → üstü dozajlı → pişmiş (tepsisiz; bant / tabla / fırın bandı / plaka üstünde) */
function mkUrun(){ const g=new THREE.Group(); const top=new THREE.Mesh(new THREE.SphereGeometry(EL.TOP_R,16,12),M(0xf0d9a8)); top.position.y=EL.TOP_R; g.add(top); g.userData.top=top;
  const taban=silindir(EL.TABAN_R,EL.TABAN_R,8,0xf0d9a8,1,40); taban.position.y=4; g.add(taban); g.userData.taban=taban;
  const ust=silindir(140,140,5,0xffd24a,1,40); ust.position.y=10.5; g.add(ust); g.userData.ust=ust; return g; }
const HAVUZ={ tepsi:havuz(2,mkTepsi), kutu:havuz(40,mkKutu), urun:havuz(14,mkUrun),
  kola:havuz(70,()=>silindir(EL.KOLA_R,EL.KOLA_R,EL.KOLA_H,0xd03030,1,16)),
  tatli:havuz(40,()=>silindir(EL.TATLI_R,EL.TATLI_R-6,EL.TATLI_H,0xf5e6c8,1,16)),
  top:havuz(12,()=>new THREE.Mesh(new THREE.SphereGeometry(EL.TOP_R,16,12),M(0xf0d9a8))) };
const temasM=havuz(36,()=>new THREE.Mesh(new THREE.SphereGeometry(22,10,8),new THREE.MeshBasicMaterial({color:0xff2d2d})));

/* ================= DURUM ================= */
const mkRob=(x)=>({carX:x, tcp:V(x+300,1300,220), t:V(0,0,-1), u:V(0,1,0), yuk:'bos', tasi:null, parmak:70, sonIK:null, temas:[]});
const ROB=[mkRob(1100),mkRob(4400)];
const S={ri:0, n:1, cek:{}, cekI:{}, qrk:{}, itme:0, ustPlakaY:0, bicakY:0, akis:null, nesne:[], tabla:{x:TAB.pres,y:PK,rot:0}};
['carX','tcp','t','u','yuk','tasi','parmak','sonIK','temas'].forEach(k=>Object.defineProperty(S,k,{get(){ return ROB[S.ri][k]; },set(v){ ROB[S.ri][k]=v; }}));
Object.keys(KOLON).forEach(k=>{ S.cek[k]=0; S.cekI[k]=0; });
const $=id=>document.getElementById(id);
const model=$('model'), omuz=$('omuz'), railz=$('railz'), pay=$('pay'), hiz=$('hiz'), out=$('out'), step=$('step'), log=$('log');
Object.entries(ROBOT).forEach(([k,r])=>{ const o=document.createElement('option'); o.value=k; o.textContent=r.ad; model.appendChild(o); });
const R=()=>ROBOT[model.value], railZ=()=>+railz.value, omuzY=()=>+omuz.value, tabanY=()=>omuzY()-R().d1;
const xAxis=()=>V(0,0,0).crossVectors(S.u,S.t).normalize();
function Wof(st){ const y=YUK[st.yuk]; return st.tcp.clone().addScaledVector(st.t,-y.L).addScaledVector(st.u,-y.P); }
function tcpOf(W,st,yuk){ const y=YUK[yuk]; return W.clone().addScaledVector(st.t,y.L).addScaledVector(st.u,y.P); }
function nesneGoster(n){ if(!n.mesh){ n.mesh=HAVUZ[n.tip].find(m=>!m.visible&&!m.userData.sahip); if(!n.mesh) return; n.mesh.userData.sahip=n; } n.mesh.visible=true; if(S.nesne.indexOf(n)<0) S.nesne.push(n); }
function nesneSil(n){ if(n.mesh){ n.mesh.visible=false; n.mesh.userData.sahip=null; n.mesh=null; } const i=S.nesne.indexOf(n); if(i>=0) S.nesne.splice(i,1); ROB.forEach(r=>{ if(r.tasi===n) r.tasi=null; }); }

/* ================= ENGELLER / BOŞLUKLAR ================= */
function cavities(){
  const P=PRES(), c=[{ad:"pres ağzı",b:[P.x[0],P.x[1],P.y[0],P.y[1],P.z[0],100]},
    {ad:"kutulama ağzı",b:[KUT.x[0],KUT.x[1],KUT.y[0],KUT.y[1],KUT.z[0],100]}];
  qrKapak.forEach((q,i)=>{ if((S.qrk[i]||0)>0.95) c.push({ad:"QR göz",b:[q.x-240,q.x+240,q.y-15,q.y+QR.goz_h,QR.z[0]-100,QR.z[0]+QR.derin]}); });
  Object.entries(KOLON).forEach(([k,K])=>{ const a=S.cek[k]||0; if(a>0.02) c.push({ad:"açık "+k,b:[K.x0+20,K.yanAcik?K.x1+300:K.x1-20,K.kotlar[S.cekI[k]]+12,K.kotlar[S.cekI[k]]+2000,20,a*K.acik-20]}); });
  return c;
}
function solids(){
  const s=MOD.map(([ad,x0,x1,y0,y1])=>({ad,b:[x0,x1,y0,y1,-HAT.derin,0]}));
  s.push({ad:"zemin",b:[-9000,9000,-500,0,-9000,9000]}, {ad:"koridor duvarı",b:[-9000,9000,0,3000,KOR,KOR+300]}, {ad:"QR dolabı",b:[QR.x[0],QR.x[1],QR.y[0],QR.y[1],QR.z[0],QR.z[1]]},
    {ad:"ray + araba",b:[S.carX-200,S.carX+200,0,260,railZ()-150,railZ()+150]});
  Object.entries(KOLON).forEach(([k,K])=>{ const a=S.cek[k]||0; if(a>0.02){ const y=K.kotlar[S.cekI[k]]; s.push({ad:"açık çekmece "+k,b:[K.x0,K.x1,y,y+K.ic+30,0,a*K.acik]}); } });
  qrKapak.forEach((q,i)=>{ const a=S.qrk[i]||0; if(a>0.05) s.push({ad:"açık QR kapağı",b:[q.x-235,q.x+235,q.y-14,q.y,QR.z[0]-a*(QR.goz_h-10),QR.z[0]]}); });
  return s;
}
/* ================= IK — dirsek HEP yukarı ================= */
function ikq(W,carX){
  const r=R(), Sh=V(carX,omuzY(),railZ());
  const dx=W.x-Sh.x, dz=W.z-Sh.z, h=W.y-Sh.y, rr=Math.hypot(dx,dz), D=Math.hypot(rr,h);
  const maxD=(r.a2+r.a3)*(+pay.value), minD=Math.abs(r.a2-r.a3)+20, ok=D<=maxD&&D>=minD;
  const Duse=Math.min(Math.max(D,minD),r.a2+r.a3-1), dir=rr>1?V(dx,0,dz).normalize():V(0,0,-1);
  const cosE=(r.a2*r.a2+Duse*Duse-r.a3*r.a3)/(2*r.a2*Duse), acs=Math.acos(Math.max(-1,Math.min(1,cosE))), th=Math.atan2(h,rr)+acs;
  const E=Sh.clone().addScaledVector(dir,r.a2*Math.cos(th)); E.y=Sh.y+r.a2*Math.sin(th);
  const Wr=ok?W.clone():E.clone().add(Sh.clone().addScaledVector(V(dx,h,dz).normalize(),Duse).sub(E).normalize().multiplyScalar(r.a3));
  const phi=Math.atan2(Wr.y-E.y,Math.hypot(Wr.x-E.x,Wr.z-E.z));
  return {ok,D,maxD,Sh,E,W:Wr,rr,q:[Math.atan2(dx,dz),th,phi],dirsek:'yukarı'};
}
function ik(W){ return ikq(W,S.carX); }
function inside(p,b,r){ return p.x>b[0]-r&&p.x<b[1]+r&&p.y>b[2]-r&&p.y<b[3]+r&&p.z>b[4]-r&&p.z<b[5]+r; }
function insideShrunk(p,b,r){ return p.x>b[0]+r&&p.x<b[1]-r&&p.y>b[2]+r&&p.y<b[3]-r&&p.z>b[4]+r&&p.z<b[5]-r; }
/* ================= ÇARPIŞMA ÖRNEKLEMİ ================= */
function orneklem(k){
  const pts=[], seg=(a,b,r,ad,skip=0)=>{ const n=Math.max(2,Math.ceil(a.distanceTo(b)/40)); for(let i=0;i<=n;i++){ const p=a.clone().lerp(b,i/n); if(p.distanceTo(a)<skip) continue; pts.push({p,r,parca:ad}); } };
  const W=k.W, t=S.t, u=S.u, x=xAxis(), pt=(tt,uu,xx=0)=>W.clone().addScaledVector(t,tt).addScaledVector(u,uu).addScaledVector(x,xx);
  seg(k.Sh,k.E,45,"üst kol",120); seg(k.E,k.W,40,"ön kol"); seg(W,pt(EL.BILEK,0),35,"bilek");
  pts.push({p:pt(EL.BILEK+20,0),r:42,parca:"avuç"}); seg(pt(EL.BILEK+EL.AVUC,0),pt(EL.BILEK+EL.AVUC+EL.PIM,0),10,"pim");
  const g=S.parmak/2+EL.PARMAK_W/2; for(const sx of [-g,g]) for(const uu of [-15,15]) for(const xx of [-3,3]) seg(pt(EL.BILEK+EL.AVUC,uu,sx+xx),pt(EL.BILEK+EL.AVUC+EL.PARMAK,uu,sx+xx),3,"parmak");
  const c=tcpOf(W,S,S.yuk), n=S.tasi;
  if(n&&n.tip==='tepsi'){ for(let i=0;i<16;i++){ const a=i/16*Math.PI*2; pts.push({p:c.clone().addScaledVector(x,170*Math.cos(a)).addScaledVector(t,170*Math.sin(a)),r:5,parca:"tepsi"}); }
    for(const uu of [5,35]) for(const xx of [-15,15]) seg(pt(EL.BILEK+EL.AVUC+EL.PIM,uu-20,xx),pt(EL.BILEK+EL.AVUC+EL.PIM+EL.SAP,uu-20,xx),3,"sap");
    if(n.icerik==='kutu') for(const a of [-160,160]) for(const b of [-160,160]) for(const cc of [5,50]) pts.push({p:c.clone().addScaledVector(x,a).addScaledVector(t,b).addScaledVector(u,cc),r:3,parca:"kutu"}); }
  else if(n&&n.tip==='top') pts.push({p:c.clone(),r:EL.TOP_R,parca:"hamur topu"});
  else if(n&&n.tip==='kola'){ for(const tt of [-EL.KOLA_H/2+8,EL.KOLA_H/2-8]) for(let i=0;i<8;i++){ const a=i/8*Math.PI*2; pts.push({p:c.clone().addScaledVector(x,EL.KOLA_R*Math.cos(a)).addScaledVector(u,EL.KOLA_R*Math.sin(a)).addScaledVector(t,tt),r:3,parca:"kola"}); } }
  else if(n&&n.tip==='tatli'){ for(const uu of [-EL.TATLI_H/2+8,EL.TATLI_H/2-8]) for(let i=0;i<8;i++){ const a=i/8*Math.PI*2; pts.push({p:c.clone().addScaledVector(x,EL.TATLI_R*Math.cos(a)).addScaledVector(t,EL.TATLI_R*Math.sin(a)).addScaledVector(u,uu),r:3,parca:"tatlı"}); } }
  return pts;
}
/* 2 robotta diğer robotun arabası + gövdesi engeldir */
function digerRobotKatilari(){ if(S.n<2) return []; const ox=ROB[1-S.ri].carX, z=railZ();
  return [{ad:'DİĞER ROBOT arabası',b:[ox-200,ox+200,0,260,z-150,z+150]},{ad:'DİĞER ROBOT gövdesi',b:[ox-100,ox+100,0,tabanY()+60,z-100,z+100]}]; }
function carpisma(k){
  const sol=solids(), cav=cavities(), hits=[], ax=S.carX, az=railZ(), ust=omuzY()+60;
  for(const q of orneklem(k)){
    if(q.parca!=='üst kol'&&q.p.y<ust+q.r&&Math.hypot(q.p.x-ax,q.p.z-az)<q.r+(q.p.y<tabanY()?100:80)){ hits.push({p:q.p,parca:q.parca,engel:"KENDİ GÖVDESİ"}); continue; }
    for(const s of sol){ if(!inside(q.p,s.b,q.r)) continue; let ex=false; for(const c of cav){ if(insideShrunk(q.p,c.b,q.r*0.6)){ ex=true; break; } } if(!ex){ hits.push({p:q.p,parca:q.parca,engel:s.ad}); break; } } }
  if(k.rr<140) hits.push({p:k.W,parca:"bilek",engel:"OMUZ EKSENİ (taban dönüşü sıçrar)"});
  return hits;
}
