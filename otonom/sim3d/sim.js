/* AUTOKITCH 3D robot simülasyonu v4 — 19 Eyl 2026. mm · x hat boyu · y kot · z: hat yüzü 0, hat içi −, koridor +
   KAYNAK PAFTALAR: HAT_2KOL_v10 (A pres · B çekmece + K4 tepsi nişi · C topping 6 hazne · D fırın/kesim/sprey kotları) + DÜKKAN v10 rayli (QR dolabı karşıda). v5 (Kemal 19 Eyl): içecek + tatlı çekmecesi K3 ÜSTÜNE geri geldi (pafta v7 yeri) · kaşar+sucuk deposu topping genişleyince açılan K4 kolonuna · E modülü HAT v10'daki gibi (kutu ağzı 430–680).
   v4: pres kızağı YOK (tepsi doğrudan alt plakaya, hamur ağızdan içeri tepsi ortasına) · içecek/tatlı K3 üstü çekmeceden · 6 hazne + nozul çıkışları · fırın kapakları giyotin (süpürme yok) · dirsek hep yukarı (dal değişimi yok) · eklem hız sınırı · kendi gövdesi çarpışma testi · QR gözü: sol şerit tatlı (robot tarafı) + kola (derinde, yatık) · sağ kutu. */
const V = (x,y,z)=>new THREE.Vector3(x,y,z);
const ROBOT = {
  FR5:  {ad:"FR5 · 922 · 8.490 €",      d1:152, a2:425,  a3:395, taban:149},
  FR10: {ad:"FR10 · 1400 · 13.590 €",   d1:228, a2:700,  a3:536, taban:190},
  FR20: {ad:"FR20 · 1854 · 15.490 €",   d1:240, a2:1000, a3:813, taban:240},
  FR5WML:{ad:"FR5 WML · 1900 · 12.000 €", d1:152, a2:900, a3:850, taban:149}
};
/* el geometrisi (varsayım) — W bilek merkezi, t ileri, u yukarı · pim 40 çıkıntı → kavranan nesne avuç yüzünden ≥ 45 uzakta */
const EL = {BILEK:100, AVUC:40, PIM:40, PARMAK:90, PARMAK_W:8, PARMAK_H:30, SAP:150, TEPSI_R:170, TABAN_R:150, TOP_R:47.5,
  KUTU:320, KUTU_H:45, KOLA_R:33, KOLA_H:115, TATLI_R:45, TATLI_H:60};
const YUK = {  // tcp = W + L t + P u  (yük merkezi)
  bos:{L:500,P:-20}, tepsi:{L:500,P:-20}, top:{L:232.5,P:0}, kola:{L:242.5,P:0}, tatli:{L:230,P:-15}
};
const HAT = {yuk:2030, derin:830, B_yuk:1060};
const MOD = [["A · PRESS",0,700,1060,2030],["B · ÇEKMECE",0,2500,0,1060],["C · TOPPING",700,2500,1060,2030],["D · FIRIN",2500,3200,0,2030],["E · KUTU",3200,3900,0,2030]];
const KOLON = {  // çekmeceler 620 × 680 · motorlu 700 strok — hamur: pide 4×5 (140 pitch) · lahm 5×7 · KI: içecek + tatlı (K3 üstü, 2 katlı, 725–1000)
  K1:{x0:62.5,  x1:682.5,  kotlar:[167.5,275.5,383.5,491.5,599.5,707.5], ic:75, tip:"pide", acik:700},   // pafta v10: soğutma grubu K4'e gidince K1 167,5'ten başlar
  K2:{x0:717.5, x1:1337.5, kotlar:[167.5,275.5,383.5,476.5,569.5,662.5,755.5,848.5], ic:60, tip:"karma", acik:700},
  K3:{x0:1372.5,x1:1992.5, kotlar:[167.5,260.5,353.5,446.5,539.5,632.5], ic:60, tip:"lahm", acik:700},
  KI:{x0:1372.5,x1:1992.5, kotlar:[725.5,862.5], ic:104, tip:"icecek", acik:700, yanAcik:true}   // İÇECEK + TATLI · K3 ÜSTÜ (pafta v7 yeri · v11'de geri geldi) · 2 kat
};
/* E çekmecesi dizilişi: tatlı sol sütun (robot yandan, el yatay +x · kap dik kalır) · kola 3 sütun × 8 (üstten kavrama, parmak ekseni x → sütun aralığı 116) */
function icecekPos(tip,kat,k){ const K=KOLON.KI, y0=K.kotlar[kat]+12; return tip==='kola'?(k<16?V(K.x0+216+116*(k%2), y0+EL.KOLA_H/2, 62+75*Math.floor(k/2)):V(K.x0+100, y0+EL.KOLA_H/2, 62+75*(k-16))):V(K.x1-60-100*Math.floor(k/5), y0+EL.TATLI_H/2, 200+95*(k%5)); }   // kola 3 sütun: önce ortadaki 2 sütun (çekmecenin SAĞ duruşundan da erişilir → SAĞ robot SOL'un bölgesine girmez), sonra en soldaki sütun · tatlı SAĞDA 2 sütun: robot çekmecenin sağında durur, el −x yönünde girer → SAĞ robot kendi bölgesinden alır   // tatlı z ≥ 200: el +x yönünde girerken parmaklar hat yüzüne, dirsek D'ye girmesin
const NIS={x:[2070,2455], y:[690,1000], z:[-660,0], cx:2262, cz:-450, raf0:702, pitch:50, n:6};
const RAF={y:925};   // AKTARMA GÖZÜ (pafta v18): nişin en üst gözü (6 boş tepsi rafı 36 aralıkla altında kalır) · SOL robot topping'li tepsiyi soldan bırakır, SAĞ robot sağdan alıp fırına götürür          // K4 üstü: 6 tepsi (v11) · altında kaşar+sucuk deposu 375–675 · en altta soğutma grubu 140–360
/* AÇIK KORİDOR (Kemal 20 Eyl 2026): pres · dozaj · fırın · kesim+sprey · kutu ağızları AYNI derinlikte ve ön yüzleri açık →
   tepsi ağızdan hiç dışarı çıkmaz, robot onu tabla gibi yana kaydırır. Kesim ile sprey TEK ağız (bıçak + sprey üst üste). ?akis=acik */
const AKIS_ACIK = new URLSearchParams(location.search).get('akis')==='acik';
const Z_KORIDOR = -400;
const TABLA_VAR = new URLSearchParams(location.search).get('tabla')==='1';   /* ATOSA TABLASI: tepsiyi pres altından dozaja, oradan fırın ucuna taşır (robot topping'e hiç gitmez) */
const TAB = {x0:390, x1:2300, uc:2280, presY:1170, y:1100, z:-440, tur:60};   /* ray C modülünün altında · pres altında tepsi 1170 (alt plaka), dozaj + fırın ucunda 1100 (tepsi alınırken bilek 1140+35 < ağız tavanı 1180) · uç 2280: tepsi kenarı 2450 < D modülü 2500 · Atosa: ürün başına ≥ 60 s */
const T_AGZ=[1070,1180], T_Y=1120, T_BAS=[1183,1317], T_KAS=[1320,1680];
const HAZNE=[["HARÇ 1",280,1070,0xc06040],["HARÇ 2",280,1350,0xc06040],["KIYMA",140,1560,0x9a5a3a],["KUŞBAŞI",140,1700,0x8a4a3a],["KAŞAR",280,1910,0xffd24a],["SUCUK",180,2140,0xb03a2a]];   // pafta v10 YUVA sırası
const NOZ={kasar:{x:1910,renk:0xffd24a}, harc:{x:1350,renk:0xb0402a}, harc2:{x:1070,renk:0xb0402a}, z:-310, alt:1183};
const FIR=[[805,1120],[1125,1440],[1445,1768]];   // pafta v17 (3B tarama sonucu: omuz 970 · ray z 360 · D kolonu alt kotu 285) ·                                                            // pafta v10 kotları · kapak y0+40..y1−40 · iç taban y0+100 (iç 400×400×100 · taş)
const FIR_X={x:[2533,3167], ic:[2650,3050], cx:2850, cz:-360};
const KES={x:[2553,3147], y:[540,675], z:[-540,0], cx:2850, cz:-270};
const YAG={x:[2553,2920], y:[320,495], z:[-440,0], cx:2737, cz:-220};
const KUT={x:[3230,3870], y:[430,680], z:[-768,0], cx:3550, cz:-390, plaka:470, itme:360};                 // pafta HAT v10: kutu ağzı 430–680
/* QR: göz 480 × 190 × 440 (pafta 380: kutu 320 + tatlı Ø90 yan yana sığmıyor → sol şerit 135 + kutu 320 + paylar = 480 · varsayım) */
const QR ={x:[2895,3900], y:[400,2000], z:[900,1340], kol:[[2910,3390],[3410,3890]], satir:[410,610,810,1010,1210,1410], derin:440, goz_h:190,
  serit:78, kutuX:305, tatliZ:965, kolaZ:1080, kutuZ:1165};
const KOR=900, DUVAR_X=[0,3900]; let RAY_X=[200,3700];   // dükkân iç 3900 = hat boyu → araba (400) duvara dayanır: merkez 200…3700 · 'ray' seçimiyle değişir
const PRES_CX=350;
function PRES(){ const p=+plaka.value; return {x:[53,647], y:[p,p+220], z:[-650,0], cx:350, cz:AKIS_ACIK?Z_KORIDOR:-440, plaka:p}; }
if(AKIS_ACIK){ NOZ.z=Z_KORIDOR; FIR_X.cz=Z_KORIDOR; KES.cz=Z_KORIDOR; KUT.cz=Z_KORIDOR;
  YAG.cx=KES.cx; YAG.cz=Z_KORIDOR; YAG.y=[KES.y[0],KES.y[1]]; }   /* sprey kesim ağzının içine alındı: tek durak */
   // pafta v10: ağız 594 × 220, alt kenar plaka kotunda
const carPres=()=>PRES().cx+400;                                                                          // kol ağza çapraz girer: bilek omuz ekseninden geçmez, ön kol ağız üst kenarına değmez
/* hızlar — kaynak/varsayım notu index.html altında */
let HIZ={serbest:600, orta:400, ince:200, mikro:80, ray:500, ivmeKol:2000, ivmeRay:1000, eklem:150, parmak:0.6, pim:0.8, cekmece:2.8, kapak:1.5, qrkapak:1.5, itici:2.0, pres:9, kasar:15, harc:20, firin:{pide:240, lahm:120}, kesim:4, sprey:3, kapan:4, musteri:150};

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
aabb(-600,4600,-10,0,-1000,2400,0x1a1f28,1,false);
aabb(-600,4600,0,2400,KOR,KOR+60,0x1c212b,.5,false);
MOD.forEach(([ad,x0,x1,y0,y1],i)=>aabb(x0+2,x1-2,y0,y1,-HAT.derin,0,i%2?0x2a3140:0x2f3748,.38));
function agiz(x0,x1,y0,y1,z0,z1){ return aabb(x0,x1,y0,y1,z0,z1,0xff5c5c,.10,0xff5c5c); }
agiz(730,2470,T_AGZ[0],T_AGZ[1],-768,0); agiz(KES.x[0],KES.x[1],KES.y[0],KES.y[1],KES.z[0],KES.z[1]);
agiz(YAG.x[0],YAG.x[1],YAG.y[0],YAG.y[1],YAG.z[0],YAG.z[1]); agiz(KUT.x[0],KUT.x[1],KUT.y[0],KUT.y[1],KUT.z[0],KUT.z[1]);
agiz(NIS.x[0],NIS.x[1],NIS.y[0],NIS.y[1],NIS.z[0],NIS.z[1]);
aabb(2540,3160,140,275,-400,-6,0x5a6472,1,0x20242c);   // D altı: robot kontrol kutusu bölmesi (ray yanında)
aabb(2035,2420,375,675,-820,-6,0xd9b04a,1,0x20242c); aabb(2035,2420,140,360,-306,-6,0x5a6472,1,0x20242c);   // K4: KAŞAR + SUCUK DEPOSU (kapaklı · eleman doldurur) · soğutma grubu
/* C · TOPPING: 6 hazne (kaset) + dozaj başlığı + alt çıkış (nozul ağzı, robot ağzının tavanında) */
HAZNE.forEach(([ad,gw,xc,renk])=>{ aabb(xc-gw/2+6,xc+gw/2-6,T_KAS[0]+8,T_KAS[1]-8,NOZ.z-200,NOZ.z+200,renk,1,0x20242c);
  aabb(xc-45,xc+45,T_BAS[0],T_BAS[1],NOZ.z-90,NOZ.z+90,0x6a7484,.9); const h=silindir(60,24,T_KAS[0]-T_BAS[1]+30,renk,1); h.position.set(xc,(T_KAS[0]+T_BAS[1])/2+10,NOZ.z); scene.add(h);
  const n=silindir(22,16,26,0xe8eaed); n.position.set(xc,NOZ.alt-10,NOZ.z); scene.add(n); const halka=silindir(30,30,4,renk); halka.position.set(xc,NOZ.alt+2,NOZ.z); scene.add(halka); });
const akisM=silindir(7,7,1,0xffffff,.9,10); akisM.visible=false; scene.add(akisM);
/* D · FIRIN: giyotin kapak (göz 1–2 yukarı, göz 3 aşağı kayar · raylar kademeli) */
const firinKapak=[];
FIR.forEach((f,g)=>{ agiz(FIR_X.x[0],FIR_X.x[1],f[0]+40,f[1]-40,-160,0); agiz(FIR_X.ic[0],FIR_X.ic[1],f[0]+100,f[1]-100,-560,-160); aabb(FIR_X.ic[0],FIR_X.ic[1],f[0]+88,f[0]+100,-560,-160,0x8a6a4a,1);
  const k=box(FIR_X.x[1]-FIR_X.x[0],f[1]-f[0]-80,14,0xd08060,.9); edge(k,0x8a4a2a); scene.add(k); firinKapak.push({m:k,f,g}); });
const presAgiz=agiz(53,647,1640,1860,-650,0);
const qrKapak=[];
QR.kol.forEach((k,ci)=>QR.satir.forEach((y,ri)=>{ aabb(k[0],k[1],y,y+QR.goz_h,QR.z[0],QR.z[0]+QR.derin,0x2997ff,.12,0x3b6ea8);
  aabb(k[0]+131,k[0]+134,y,y+20,QR.z[0]+20,QR.z[0]+QR.derin-20,0x3b6ea8,.9,false);                       // şerit ayırıcı çıta
  const d=box(k[1]-k[0]-10,QR.goz_h-10,14,0x5a6a80,.95); edge(d,0x8899aa); scene.add(d); qrKapak.push({m:d,x:(k[0]+k[1])/2,k0:k[0],y,ci,ri}); }));
aabb(QR.x[0],QR.x[1],QR.y[0],QR.y[1],QR.z[0],QR.z[1],0x4a5568,.30);
const cekMesh={};
Object.entries(KOLON).forEach(([k,K])=>{ K.kotlar.forEach(y=>{ const f=box(K.x1-K.x0-16,K.ic+26,24,K.tip==='icecek'?0x3f7fbf:0x3f9c7a); f.position.set((K.x0+K.x1)/2,y+(K.ic+30)/2,-12); scene.add(f); });
  const a=box(K.x1-K.x0-4,K.tip==='icecek'?30:K.ic+26,K.acik,K.tip==='icecek'?0x6fb0ff:0x5fd3a8,.5); a.visible=false; scene.add(a); cekMesh[k]=a; });
const altPlaka=silindir(170,170,12,0xa0a6b0,1,32); scene.add(altPlaka);
let tablaM=null, tablaKol=null, tablaRay=null;
if(TABLA_VAR){ tablaRay=aabb(TAB.x0-60,TAB.x1+60,1085,1120,TAB.z-30,TAB.z+30,0x2997ff,1);
  tablaM=silindir(175,175,14,0xcfe2ff,1,40); scene.add(tablaM); tablaKol=silindir(24,24,1,0x8a94a4,1,12); scene.add(tablaKol); }
const ustPlaka=silindir(145,145,50,0x9aa3b2,1,32); scene.add(ustPlaka);
const bicak=silindir(150,150,20,0xb0b8c4,.9,32); bicak.position.set(KES.cx,KES.y[1]+100,KES.cz); scene.add(bicak);
aabb(KUT.cx-200,KUT.cx+200,KUT.plaka-10,KUT.plaka,KUT.cz-200,KUT.cz+200,0x8a94a4,1);
const itici=box(300,30,20,0xff8c40); scene.add(itici);
const ray=box(3900,120,120,0x2997ff); scene.add(ray);
/* robot görsel seti — iki robot için iki kopya (0: SOL · mavi, 1: SAĞ · turuncu) */
function mkRobotM(renk){ const o={}; const ek=m=>{ scene.add(m); return m; };
  o.araba=ek(box(400,140,300,0x3a4250)); o.kaide=ek(silindir(100,100,1,0x596273)); o.tabanM=ek(silindir(75,75,120,0x9aa3b2));
  o.ustKol=ek(silindir(45,45,1,0xe8eaed,1,16)); o.onKol=ek(silindir(40,40,1,0xe8eaed,1,16)); o.bilekM=ek(silindir(35,35,1,0xb8bfc9,1,16));
  o.eklem=[0,0,0].map(()=>ek(new THREE.Mesh(new THREE.SphereGeometry(50,16,12),M(renk)))); o.avucM=ek(silindir(40,40,EL.AVUC,renk)); o.pimM=ek(silindir(10,10,EL.PIM,0xffb340,1,12));
  o.parmakM=[ek(box(EL.PARMAK_W,EL.PARMAK_H,EL.PARMAK,0x7fb8ff)),ek(box(EL.PARMAK_W,EL.PARMAK_H,EL.PARMAK,0x7fb8ff))];
  o.hepsi=[o.araba,o.kaide,o.tabanM,o.ustKol,o.onKol,o.bilekM,o.avucM,o.pimM].concat(o.eklem,o.parmakM); return o; }
const ROBM=[mkRobotM(0x2997ff),mkRobotM(0xff8c40)];
function havuz(n,mk){ const a=[]; for(let i=0;i<n;i++){ const g=mk(); g.visible=false; scene.add(g); a.push(g); } return a; }
/* kutu: taban + 4 duvar + içinde pide + arkadan menteşeli kapak (kapanma 0..1) */
function mkKutu(){ const g=new THREE.Group(), K=EL.KUTU, H=EL.KUTU_H, c=0xe0c890; const tb=box(K,4,K,c); tb.position.y=-H/2+2; g.add(tb);
  [[0,K/2-2,K,4],[0,-K/2+2,K,4],[K/2-2,0,4,K],[-K/2+2,0,4,K]].forEach(([x,z,w,d])=>{ const b=box(w,H,d,c); b.position.set(x,0,z); g.add(b); });
  const pd=silindir(150,150,10,0xd9a45a,1,32); pd.position.y=-H/2+10; pd.visible=false; g.add(pd); g.userData.pide=pd;
  const mnt=new THREE.Group(); mnt.position.set(0,H/2,-K/2); const kp=box(K,4,K,0xd8be84); edge(kp,0xa08a5a); kp.position.set(0,0,K/2); mnt.add(kp); g.add(mnt); g.userData.kapak=mnt; return g; }
function kutuGoster(g,n){ g.userData.pide.visible=n.icerik==='pide'&&!n.kapali; g.userData.kapak.rotation.x=-(1-(n.kapanma===undefined?(n.kapali?1:0):n.kapanma))*Math.PI*0.58; }
function mkTepsi(){ const g=new THREE.Group(); const t=silindir(EL.TEPSI_R,EL.TEPSI_R,10,0xd8dde6,1,40); g.add(t);
  const sap=box(30,30,EL.SAP,0xb0b8c4); sap.position.set(0,20,EL.TEPSI_R+EL.SAP/2); g.add(sap); const sok=box(34,34,30,0x2997ff); sok.position.set(0,20,EL.TEPSI_R+EL.SAP-15); g.add(sok);
  const top=new THREE.Mesh(new THREE.SphereGeometry(EL.TOP_R,16,12),M(0xf0d9a8)); top.position.y=5+EL.TOP_R; g.add(top); g.userData.top=top;
  const taban=silindir(EL.TABAN_R,EL.TABAN_R,8,0xf0d9a8,1,40); taban.position.y=9; g.add(taban); g.userData.taban=taban;
  const kas=silindir(140,140,5,0xffd24a,1,40); kas.position.y=15.5; g.add(kas); g.userData.kasar=kas;
  const kutu=mkKutu(); kutu.position.y=5+EL.KUTU_H/2; g.add(kutu); g.userData.kutu=kutu; return g; }
const HAVUZ={ tepsi:havuz(NIS.n,mkTepsi), kutu:havuz(30,mkKutu),
  pide:havuz(4,()=>silindir(150,150,10,0xd9a45a,1,32)),
  kola:havuz(60,()=>silindir(EL.KOLA_R,EL.KOLA_R,EL.KOLA_H,0xd03030,1,16)),
  tatli:havuz(40,()=>silindir(EL.TATLI_R,EL.TATLI_R-6,EL.TATLI_H,0xf5e6c8,1,16)),
  top:havuz(40,()=>new THREE.Mesh(new THREE.SphereGeometry(EL.TOP_R,16,12),M(0xf0d9a8))) };
const temasM=havuz(36,()=>new THREE.Mesh(new THREE.SphereGeometry(22,10,8),new THREE.MeshBasicMaterial({color:0xff2d2d})));
/* erişim küresi kaldırıldı (menü sadeleşti) */

/* ================= DURUM ================= */
const mkRob=(x)=>({carX:x, tcp:V(x+300,1300,220), t:V(0,0,-1), u:V(0,1,0), yuk:'bos', tasi:null, parmak:70, sonIK:null, temas:[]});
const ROB=[mkRob(1100),mkRob(3300)];
const S={ri:0, n:1, cek:{}, cekI:{}, kapak:[0,0,0], qrk:{}, itme:0, ustPlakaY:0, bicakY:0, akis:null, nesne:[], tabla:{x:PRES_CX, y:1170, rot:0}};
['carX','tcp','t','u','yuk','tasi','parmak','sonIK','temas'].forEach(k=>Object.defineProperty(S,k,{get(){ return ROB[S.ri][k]; },set(v){ ROB[S.ri][k]=v; }}));   // S.carX vb. = AKTİF robotun alanı
Object.keys(KOLON).forEach(k=>{ S.cek[k]=0; S.cekI[k]=0; });
const $=id=>document.getElementById(id);
const model=$('model'), omuz=$('omuz'), railz=$('railz'), pay=$('pay'), hiz=$('hiz'), plaka=$('plaka'), out=$('out'), step=$('step'), log=$('log');
Object.entries(ROBOT).forEach(([k,r])=>{ const o=document.createElement('option'); o.value=k; o.textContent=r.ad; model.appendChild(o); });
const R=()=>ROBOT[model.value], railZ=()=>+railz.value, omuzY=()=>+omuz.value, tabanY=()=>omuzY()-R().d1;
const xAxis=()=>V(0,0,0).crossVectors(S.u,S.t).normalize();
function Wof(st){ const y=YUK[st.yuk]; return st.tcp.clone().addScaledVector(st.t,-y.L).addScaledVector(st.u,-y.P); }
function tcpOf(W,st,yuk){ const y=YUK[yuk]; return W.clone().addScaledVector(st.t,y.L).addScaledVector(st.u,y.P); }
/* dünya nesneleri: {tip, pos, icerik, kapali, yatik, mesh} */
function nesneGoster(n){ if(!n.mesh){ n.mesh=HAVUZ[n.tip].find(m=>!m.visible&&!m.userData.sahip); if(!n.mesh) return; n.mesh.userData.sahip=n; } n.mesh.visible=true; if(S.nesne.indexOf(n)<0) S.nesne.push(n); }
function nesneSil(n){ if(n.mesh){ n.mesh.visible=false; n.mesh.userData.sahip=null; n.mesh=null; } const i=S.nesne.indexOf(n); if(i>=0) S.nesne.splice(i,1); ROB.forEach(r=>{ if(r.tasi===n) r.tasi=null; }); }

/* ================= ENGELLER / BOŞLUKLAR ================= */
function cavities(){
  const P=PRES(), c=[{ad:"pres ağzı",b:[P.x[0],P.x[1],P.y[0],P.y[1],P.z[0],100]},
    {ad:"topping ağzı",b:[730,2470,T_AGZ[0],T_AGZ[1],-768,100]},
    {ad:"kesim ağzı",b:[KES.x[0],KES.x[1],KES.y[0],KES.y[1],KES.z[0],100]},
    {ad:"sprey ağzı",b:[YAG.x[0],YAG.x[1],YAG.y[0],YAG.y[1],YAG.z[0],100]},
    {ad:"kutulama ağzı",b:[KUT.x[0],KUT.x[1],KUT.y[0],KUT.y[1],KUT.z[0],100]},
    {ad:"tepsi nişi",b:[NIS.x[0],NIS.x[1],NIS.y[0],NIS.y[1],NIS.z[0],100]}];
  FIR.forEach((f,i)=>{ if(S.kapak[i]>0.95) c.push({ad:"fırın kapağı "+(i+1),b:[FIR_X.x[0],FIR_X.x[1],f[0]+40,f[1]-40,-200,100]}); c.push({ad:"fırın iç "+(i+1),b:[FIR_X.ic[0],FIR_X.ic[1],f[0]+100,f[1]-100,-560,-160]}); });
  qrKapak.forEach((q,i)=>{ if((S.qrk[i]||0)>0.95) c.push({ad:"QR göz",b:[q.x-240,q.x+240,q.y-15,q.y+QR.goz_h,QR.z[0]-100,QR.z[0]+QR.derin]}); });
  Object.entries(KOLON).forEach(([k,K])=>{ const a=S.cek[k]||0; if(a>0.02) c.push({ad:"açık "+k,b:[K.x0+20,K.yanAcik?K.x1+300:K.x1-20,K.kotlar[S.cekI[k]]+12,K.kotlar[S.cekI[k]]+2000,20,a*K.acik-20]}); });
  return c;
}
function solids(){
  const s=MOD.map(([ad,x0,x1,y0,y1])=>({ad,b:[x0,x1,y0,y1,-HAT.derin,0]}));
  s.push({ad:"zemin",b:[-9000,9000,-500,0,-9000,9000]}, {ad:"koridor duvarı",b:[-9000,9000,0,3000,KOR,KOR+300]}, {ad:"QR dolabı",b:[QR.x[0],QR.x[1],QR.y[0],QR.y[1],QR.z[0],QR.z[1]]},
    {ad:"ray + araba",b:[S.carX-200,S.carX+200,0,260,railZ()-150,railZ()+150]});
  if(S.n>1){ const ox=ROB[1-S.ri].carX; s.push({ad:"DİĞER ROBOT arabası",b:[ox-200,ox+200,0,260,railZ()-150,railZ()+150]},{ad:"DİĞER ROBOT gövdesi",b:[ox-100,ox+100,0,omuzY()+60,railZ()-100,railZ()+100]}); }
  Object.entries(KOLON).forEach(([k,K])=>{ const a=S.cek[k]||0; if(a>0.02){ const y=K.kotlar[S.cekI[k]]; s.push({ad:"açık çekmece "+k,b:[K.x0,K.x1,y,y+K.ic+30,0,a*K.acik]}); } });
  qrKapak.forEach((q,i)=>{ const a=S.qrk[i]||0; if(a>0.05) s.push({ad:"açık QR kapağı",b:[q.x-235,q.x+235,q.y-14,q.y,QR.z[0]-a*(QR.goz_h-10),QR.z[0]]}); });   // alttan menteşeli: açıkken öne yatar
  return s;
}
/* ================= IK — dirsek HEP yukarı (dal değişimi yok → eklem sürekliliği) ================= */
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
  if(n&&n.tip==='tepsi'){ for(let i=0;i<16;i++){ const a=i/16*Math.PI*2; pts.push({p:c.clone().addScaledVector(x,170*Math.cos(a)).addScaledVector(t,170*Math.sin(a)),r:5,parca:"tepsi"});
      if(n.icerik&&n.icerik!=='kutu') pts.push({p:c.clone().addScaledVector(x,150*Math.cos(a)).addScaledVector(t,150*Math.sin(a)).addScaledVector(u,12),r:6,parca:"pide"}); }
    for(const uu of [5,35]) for(const xx of [-15,15]) seg(pt(EL.BILEK+EL.AVUC+EL.PIM,uu-20,xx),pt(EL.BILEK+EL.AVUC+EL.PIM+EL.SAP,uu-20,xx),3,"sap");
    if(n.icerik==='kutu') for(const a of [-160,160]) for(const b of [-160,160]) for(const cc of [5,50]) pts.push({p:c.clone().addScaledVector(x,a).addScaledVector(t,b).addScaledVector(u,cc),r:3,parca:"kutu"}); }
  else if(n&&n.tip==='top') pts.push({p:c.clone(),r:EL.TOP_R,parca:"hamur topu"});
  else if(n&&n.tip==='kola'){ for(const tt of [-EL.KOLA_H/2+8,EL.KOLA_H/2-8]) for(let i=0;i<8;i++){ const a=i/8*Math.PI*2; pts.push({p:c.clone().addScaledVector(x,EL.KOLA_R*Math.cos(a)).addScaledVector(u,EL.KOLA_R*Math.sin(a)).addScaledVector(t,tt),r:3,parca:"kola"}); } }   // üstten kavrandı → eksen t
  else if(n&&n.tip==='tatli'){ for(const uu of [-EL.TATLI_H/2+8,EL.TATLI_H/2-8]) for(let i=0;i<8;i++){ const a=i/8*Math.PI*2; pts.push({p:c.clone().addScaledVector(x,EL.TATLI_R*Math.cos(a)).addScaledVector(t,EL.TATLI_R*Math.sin(a)).addScaledVector(u,uu),r:3,parca:"tatlı"}); } }
  return pts;
}
function carpisma(k){
  const sol=solids(), cav=cavities(), hits=[], ax=S.carX, az=railZ(), ust=omuzY()+60;
  for(const q of orneklem(k)){
    if(q.parca!=='üst kol'&&q.p.y<ust+q.r&&Math.hypot(q.p.x-ax,q.p.z-az)<q.r+(q.p.y<tabanY()?100:80)){ hits.push({p:q.p,parca:q.parca,engel:"KENDİ GÖVDESİ"}); continue; }   // kol / el / yük kendi kaidesine girmesin
    for(const s of sol){ if(!inside(q.p,s.b,q.r)) continue; let ex=false; for(const c of cav){ if(insideShrunk(q.p,c.b,q.r*0.6)){ ex=true; break; } } if(!ex){ hits.push({p:q.p,parca:q.parca,engel:s.ad}); break; } } }
  if(k.rr<140) hits.push({p:k.W,parca:"bilek",engel:"OMUZ EKSENİ (taban dönüşü sıçrar)"});
  return hits;
}
