/* AUTOKITCH 3D robot simülasyonu v2 — 17 Eyl 2026. mm; x hat boyu, y kot, z: hat yüzü 0, hat içi −, koridor + */
const V = (x,y,z)=>new THREE.Vector3(x,y,z);
const ROBOT = {
  FR5:  {ad:"FR5 · 922 · 8.490 €",      d1:152, a2:425,  a3:395, taban:149},
  FR10: {ad:"FR10 · 1400 · 13.590 €",   d1:228, a2:700,  a3:536, taban:190},
  FR20: {ad:"FR20 · 1854 · 15.490 €",   d1:240, a2:1000, a3:813, taban:240},
  FR5WML:{ad:"FR5 WML · 1900 · 12.000 €", d1:152, a2:900, a3:850, taban:149}
};
/* uç geometrisi (varsayım): W bilek merkezi; t çatal ekseni, u tepsi tarafı (yukarı) */
const U = {BILEK:120, FORK:600, FORK_W:200, FORK_T:12, FORK_U:-40, TEPSI_AT:540, TEPSI_R:170, TABAN_R:150, TOP_R:47.5, KUTU:320, KUTU_H:45};
const YUK = { // W'den yük merkezine: tcp = W + L t + P u
  tepsi:{L:540, P:-27.5}, top:{L:787.5, P:-40}, topAlt:{L:695, P:-93.5}, kutu:{L:540, P:-11.5}, bos:{L:540, P:-27.5}
};
const HAT = {yuk:2030, derin:830, B_yuk:1060};
const MOD = [["A · PRESS",0,700,1060,2030],["B · ÇEKMECE",0,2100,0,1060],["C · TOPPING",700,2100,1060,2030],["D · FIRIN",2100,2800,0,2030],["E · KUTU",2800,3500,0,2030],["F · TEPSİ + KARTON",3500,3900,0,2030]];
const KOLON = {
  K1:{x0:62.5, x1:682.5, kotlar:[287.5,395.5,503.5,611.5,719.5,827.5], ic:75},
  K2:{x0:717.5,x1:1337.5,kotlar:[167.5,275.5,383.5,476.5,569.5,662.5,755.5,848.5], ic:60},
  K3:{x0:1372.5,x1:1992.5,kotlar:[167.5,260.5,353.5,446.5,539.5,632.5], ic:60}
};
const CEK_ACIK=700;
const T_AGZ=[1070,1180], NOZ={x:1710, z:-310, alt:1183};                    // topping ağzı · kaşar nozulu
const FIR=[[1065,1380],[1385,1700],[1705,2028.5]];                          // kapak; iç taban y0+100, tavan y1-100
const KES={x:[2153,2747], y:[800,935], z:[-540,0], cx:2450, cz:-270};
const YAG={x:[2153,2520], y:[580,755], z:[-440,0], cx:2337, cz:-220};
const KUT={x:[2830,3470], y:[430,680], z:[-768,0], cx:3150, cz:-390, plaka:460};
const RAF={x:[3510,3890], y:[870,1400], z:[-540,0], cx:3700, cz:-270, taban:870};   // F nişi: tepsi yığını
const QR ={x:[3040,3900], y:[400,2000], z:[900,1420], kol:[[3080,3460],[3480,3860]], satir:[410,610,810,1010,1210,1410], derin:440};
const KOR=900, RAY_X=[200,3300];
function PRES(){ const p=+plaka.value; return {x:[53,647], y:[p,p+220], z:[-650,0], cx:350, cz:-440, plaka:p}; }

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
// zemin + koridor duvarı
aabb(-600,4500,-10,0,-1000,2400,0x1a1f28,1,false);
aabb(-600,4500,0,2400,KOR,KOR+60,0x1c212b,.5,false);
// modüller (yarı saydam gövde)
MOD.forEach(([ad,x0,x1,y0,y1],i)=>aabb(x0+2,x1-2,y0,y1,-HAT.derin,0,i%2?0x2a3140:0x2f3748,.42));
// ağızlar (boşluk kutuları, kırmızı çerçeve)
const agizMesh=[];
function agiz(x0,x1,y0,y1,z0,z1,ad){ const m=aabb(x0,x1,y0,y1,z0,z1,0xff5c5c,.10,0xff5c5c); m.userData.ad=ad; agizMesh.push(m); return m; }
function cavities(){ // her karede: pres (plaka kotuna bağlı) + sabitler + açık çekmeceler
  const P=PRES(), c=[{ad:"pres ağzı",b:[P.x[0],P.x[1],P.y[0],P.y[1],P.z[0],100]},
    {ad:"topping ağzı",b:[730,2070,T_AGZ[0],T_AGZ[1],-768,100]},
    {ad:"kesim ağzı",b:[KES.x[0],KES.x[1],KES.y[0],KES.y[1],KES.z[0],100]},
    {ad:"sprey ağzı",b:[YAG.x[0],YAG.x[1],YAG.y[0],YAG.y[1],YAG.z[0],100]},
    {ad:"kutulama ağzı",b:[KUT.x[0],KUT.x[1],KUT.y[0],KUT.y[1],KUT.z[0],100]},
    {ad:"tepsi nişi",b:[RAF.x[0],RAF.x[1],RAF.y[0],RAF.y[1],RAF.z[0],100]}];
  FIR.forEach((f,i)=>{ c.push({ad:"fırın kapağı "+(i+1),b:[2133,2767,f[0]+40,f[1]-40,-200,100]}); c.push({ad:"fırın iç "+(i+1),b:[2250,2650,f[0]+100,f[1]-100,-560,-160]}); });
  QR.kol.forEach((k,ci)=>QR.satir.forEach((y,ri)=>c.push({ad:"QR göz",b:[k[0],k[1],y-15,y+180,QR.z[0]-100,QR.z[0]+QR.derin]})));
  Object.entries(KOLON).forEach(([k,K])=>{ const a=S.cek[k]||0; if(a>0.02) c.push({ad:"açık "+k,b:[K.x0+20,K.x1-20,K.kotlar[S.cekI[k]]+12,K.kotlar[S.cekI[k]]+2000,20,a*CEK_ACIK-20]}); });
  return c;
}
function solids(){
  const s=MOD.map(([ad,x0,x1,y0,y1])=>({ad,b:[x0,x1,y0,y1,-HAT.derin,0]}));
  s.push({ad:"zemin",b:[-9000,9000,-500,0,-9000,9000]}, {ad:"koridor duvarı",b:[-9000,9000,0,3000,KOR,KOR+300]}, {ad:"QR dolabı",b:[QR.x[0],QR.x[1],QR.y[0],QR.y[1],QR.z[0],QR.z[1]]},
    {ad:"ray + araba",b:[S.carX-200,S.carX+200,0,260,railZ()-150,railZ()+150]}, {ad:"robot kaidesi",b:[S.carX-100,S.carX+100,0,tabanY(),railZ()-100,railZ()+100]});
  Object.entries(KOLON).forEach(([k,K])=>{ const a=S.cek[k]||0; if(a>0.02){ const y=K.kotlar[S.cekI[k]]; s.push({ad:"açık çekmece "+k,b:[K.x0,K.x1,y,y+K.ic+30,0,a*CEK_ACIK]}); } });
  return s;
}
// sabit ağız görselleri
agiz(730,2070,T_AGZ[0],T_AGZ[1],-768,0,"topping"); agiz(KES.x[0],KES.x[1],KES.y[0],KES.y[1],KES.z[0],KES.z[1],"kesim");
agiz(YAG.x[0],YAG.x[1],YAG.y[0],YAG.y[1],YAG.z[0],YAG.z[1],"sprey"); agiz(KUT.x[0],KUT.x[1],KUT.y[0],KUT.y[1],KUT.z[0],KUT.z[1],"kutu");
agiz(RAF.x[0],RAF.x[1],RAF.y[0],RAF.y[1],RAF.z[0],RAF.z[1],"tepsi nişi");
FIR.forEach(f=>{ agiz(2133,2767,f[0]+40,f[1]-40,-160,0,"fırın kapak"); agiz(2250,2650,f[0]+100,f[1]-100,-560,-160,"fırın iç"); aabb(2250,2650,f[0]+100-12,f[0]+100,-560,-160,0x8a6a4a,1); });
const presAgiz=agiz(53,647,1650,1860,-650,0,"pres");
QR.kol.forEach(k=>QR.satir.forEach(y=>aabb(k[0],k[1],y,y+180,QR.z[0],QR.z[0]+QR.derin,0x2997ff,.12,0x3b6ea8)));
aabb(QR.x[0],QR.x[1],QR.y[0],QR.y[1],QR.z[0],QR.z[1],0x4a5568,.35);
// çekmece önleri + açık çekmece kutuları
const cekMesh={};
Object.entries(KOLON).forEach(([k,K])=>{ K.kotlar.forEach(y=>{ const f=box(K.x1-K.x0-16,K.ic+26,24,0x3f9c7a); f.position.set((K.x0+K.x1)/2,y+(K.ic+30)/2,-12); scene.add(f); });
  const a=box(K.x1-K.x0-4,K.ic+26,CEK_ACIK,0x5fd3a8,.75); a.visible=false; scene.add(a); cekMesh[k]=a; });
// pres plakaları, nozul, bıçak, kutu plakası, ray, araba, kaide, kol
const altPlaka=new THREE.Mesh(new THREE.CylinderGeometry(170,170,12,32),M(0xc0c6d0)); scene.add(altPlaka);
const ustPlaka=new THREE.Mesh(new THREE.CylinderGeometry(145,145,50,32),M(0x9aa3b2)); scene.add(ustPlaka);
const nozul=new THREE.Mesh(new THREE.CylinderGeometry(30,18,120,16),M(0xd0a040)); nozul.position.set(NOZ.x,NOZ.alt+60,NOZ.z); scene.add(nozul);
const bicak=new THREE.Mesh(new THREE.CylinderGeometry(150,150,20,32),M(0xb0b8c4,.9)); bicak.position.set(KES.cx,KES.y[1]+100,KES.cz); scene.add(bicak);
aabb(KUT.cx-200,KUT.cx+200,KUT.plaka-10,KUT.plaka,KUT.cz-200,KUT.cz+200,0x8a94a4,1);
const ray=box(3700,120,120,0x2997ff); scene.add(ray);
const araba=box(400,140,300,0x3a4250); scene.add(araba);
const kaide=new THREE.Mesh(new THREE.CylinderGeometry(100,100,1,24),M(0x596273)); scene.add(kaide);
const tabanM=new THREE.Mesh(new THREE.CylinderGeometry(75,75,120,24),M(0x9aa3b2)); scene.add(tabanM);
const ustKol=new THREE.Mesh(new THREE.CylinderGeometry(45,45,1,16),M(0xe8eaed)); scene.add(ustKol);
const onKol=new THREE.Mesh(new THREE.CylinderGeometry(40,40,1,16),M(0xe8eaed)); scene.add(onKol);
const bilekM=new THREE.Mesh(new THREE.CylinderGeometry(35,35,1,16),M(0xb8bfc9)); scene.add(bilekM);
const eklem=[0,0,0].map(()=>{ const s=new THREE.Mesh(new THREE.SphereGeometry(50,16,12),M(0x2997ff)); scene.add(s); return s; });
const kokM=box(120,40,100,0x2997ff); scene.add(kokM);
const catalM=box(U.FORK_W,U.FORK_T,U.FORK,0x7fb8ff); scene.add(catalM);
const kepce=box(60,40,20,0xffb340); const altPed=box(60,4,60,0xffb340); scene.add(altPed); scene.add(kepce);
const tepsiM=new THREE.Mesh(new THREE.CylinderGeometry(U.TEPSI_R,U.TEPSI_R,10,40),M(0xd8dde6)); scene.add(tepsiM);
const tabanMesh=new THREE.Mesh(new THREE.CylinderGeometry(U.TABAN_R,U.TABAN_R,8,40),M(0xf0d9a8)); scene.add(tabanMesh);
const kasarM=new THREE.Mesh(new THREE.CylinderGeometry(140,140,5,40),M(0xffd24a)); scene.add(kasarM);
const topM=new THREE.Mesh(new THREE.SphereGeometry(U.TOP_R,18,14),M(0xf0d9a8)); scene.add(topM);
const kutuM=box(U.KUTU,U.KUTU_H,U.KUTU,0xe0c890,.55); edge(kutuM,0xa08a5a); scene.add(kutuM);
const rafTepsi=[]; for(let i=0;i<6;i++){ const m=new THREE.Mesh(new THREE.CylinderGeometry(U.TEPSI_R,U.TEPSI_R,10,32),M(0xd8dde6)); m.position.set(RAF.cx,RAF.taban+20+25*i,RAF.cz); scene.add(m); rafTepsi.push(m); }
const temasM=[]; for(let i=0;i<24;i++){ const m=new THREE.Mesh(new THREE.SphereGeometry(22,10,8),new THREE.MeshBasicMaterial({color:0xff2d2d})); m.visible=false; scene.add(m); temasM.push(m); }
const erisimW=new THREE.LineSegments(new THREE.WireframeGeometry(new THREE.SphereGeometry(1,18,12)),new THREE.LineBasicMaterial({color:0x2997ff,transparent:true,opacity:.12})); scene.add(erisimW);

/* ================= DURUM ================= */
const S={carX:1100, tcp:V(1100,1300,200), t:V(0,0,-1), u:V(0,1,0), yuk:'bos', tasi:null,
  cek:{K1:0,K2:0,K3:0}, cekI:{K1:0,K2:0,K3:0},
  dunya:{tepsi:null, top:null, kutu:null, kutuKapali:false, tepsiUst:'', pideKutuda:false, rafN:6, ustPlakaY:0, bicakY:0}, sonIK:null, temas:[]};
const $=id=>document.getElementById(id);
const model=$('model'), omuz=$('omuz'), railz=$('railz'), pay=$('pay'), hiz=$('hiz'), plaka=$('plaka'), goz=$('goz'), cekS=$('cek'), siraS=$('sira'), topS=$('top'), out=$('out'), step=$('step'), log=$('log');
Object.entries(ROBOT).forEach(([k,r])=>{ const o=document.createElement('option'); o.value=k; o.textContent=r.ad; model.appendChild(o); });
const R=()=>ROBOT[model.value], railZ=()=>+railz.value, omuzY=()=>+omuz.value, tabanY=()=>omuzY()-R().d1;
const xAxis=()=>V(0,0,0).crossVectors(S.u,S.t).normalize();
function Wof(st){ const y=YUK[st.yuk]; return st.tcp.clone().addScaledVector(st.t,-y.L).addScaledVector(st.u,-y.P); }
function tcpOf(W,st,yuk){ const y=YUK[yuk]; return W.clone().addScaledVector(st.t,y.L).addScaledVector(st.u,y.P); }

/* ================= IK (düzlemsel, dirsek yukarı) ================= */
function ik(W){
  const r=R(), Sh=V(S.carX,omuzY(),railZ());
  const dx=W.x-Sh.x, dz=W.z-Sh.z, h=W.y-Sh.y, rr=Math.hypot(dx,dz), D=Math.hypot(rr,h);
  const maxD=(r.a2+r.a3)*(+pay.value), minD=Math.abs(r.a2-r.a3)+20, ok=D<=maxD&&D>=minD;
  const Duse=Math.min(Math.max(D,minD),r.a2+r.a3-1), dir=rr>1?V(dx,0,dz).normalize():V(0,0,-1);
  const cosE=(r.a2*r.a2+Duse*Duse-r.a3*r.a3)/(2*r.a2*Duse), acs=Math.acos(Math.max(-1,Math.min(1,cosE))), base=Math.atan2(h,rr);
  const Wg=ok?W.clone():Sh.clone().addScaledVector(V(dx,h,dz).normalize(),Duse);
  const sol=[base+acs,base-acs].map(th=>{ const E=Sh.clone().addScaledVector(dir,r.a2*Math.cos(th)); E.y=Sh.y+r.a2*Math.sin(th);
    const Wr=ok?W.clone():E.clone().add(Wg.clone().sub(E).normalize().multiplyScalar(r.a3)); return {E,W:Wr,hits:kolTemas(Sh,E,Wr)}; });
  sol.sort((a,b)=>a.hits-b.hits||b.E.y-a.E.y);                     // önce temassız çözüm, sonra dirsek yukarı
  return {ok,D,maxD,Sh,E:sol[0].E,W:sol[0].W,dirsek:sol[0]===undefined?'':(sol[0].E.y>=Sh.y?'yukarı':'aşağı')};
}
function kolTemas(Sh,E,W){ const sol=solids(), cav=cavities(); let n=0;
  const test=(a,b,r,skip)=>{ const m=Math.max(2,Math.ceil(a.distanceTo(b)/50)); for(let i=0;i<=m;i++){ const p=a.clone().lerp(b,i/m); if(p.distanceTo(a)<skip) continue; for(const s of sol){ if(s.ad==='robot kaidesi'||!inside(p,s.b,r)) continue; let ex=false; for(const c of cav){ if(insideShrunk(p,c.b,r*0.6)){ ex=true; break; } } if(!ex){ n++; break; } } } };
  test(Sh,E,45,120); test(E,W,40,0); return n; }   // kaide hariç: gerçek kolda omuz yan ofseti (138) kolu kolonun yanından geçirir

/* ================= ÇARPIŞMA ================= */
function inside(p,b,r){ return p.x>b[0]-r&&p.x<b[1]+r&&p.y>b[2]-r&&p.y<b[3]+r&&p.z>b[4]-r&&p.z<b[5]+r; }
function insideShrunk(p,b,r){ return p.x>b[0]+r&&p.x<b[1]-r&&p.y>b[2]+r&&p.y<b[3]-r&&p.z>b[4]+r&&p.z<b[5]-r; }
function orneklem(k){ // {p,r,parca}
  const pts=[], seg=(a,b,r,ad,skip=0)=>{ const n=Math.max(2,Math.ceil(a.distanceTo(b)/40)); for(let i=0;i<=n;i++){ const p=a.clone().lerp(b,i/n); if(p.distanceTo(a)<skip) continue; pts.push({p,r,parca:ad}); } };
  const W=k.W, t=S.t, u=S.u, x=xAxis();
  const pt=(tt,uu,xx)=>W.clone().addScaledVector(t,tt).addScaledVector(u,uu).addScaledVector(x,xx);
  seg(k.Sh,k.E,45,"üst kol",120); seg(k.E,k.W,40,"ön kol"); seg(W,pt(U.BILEK,0,0),35,"bilek");
  for(const uu of [-34,6]) for(const xx of [-60,60]) seg(pt(U.BILEK,uu,xx),pt(U.BILEK+100,uu,xx),3,"kavrama bloğu");
  for(const xx of [-100,0,100]) seg(pt(U.BILEK,U.FORK_U,xx),pt(U.BILEK+U.FORK,U.FORK_U,xx),6,"çatal");
  pts.push({p:pt(U.BILEK+U.FORK+10,U.FORK_U,0),r:10,parca:"vakum ped"}); pts.push({p:pt(690,-42,0),r:4,parca:"alt ped"});
  if(S.tasi==='tepsi'||S.tasi==='kutu'){ const c=S.tcp; if(S.tasi==='tepsi'){ for(let i=0;i<16;i++){ const a=i/16*Math.PI*2; pts.push({p:c.clone().addScaledVector(x,170*Math.cos(a)).addScaledVector(t,170*Math.sin(a)),r:5,parca:"tepsi"}); if(S.dunya.tepsiUst) pts.push({p:c.clone().addScaledVector(x,150*Math.cos(a)).addScaledVector(t,150*Math.sin(a)).addScaledVector(u,12),r:6,parca:"pide"}); } }
    else for(const a of [-160,160]) for(const b of [-160,160]) for(const cc of [-22,22]) pts.push({p:c.clone().addScaledVector(x,a).addScaledVector(t,b).addScaledVector(u,cc),r:3,parca:"kutu"}); }
  if(S.tasi==='top') pts.push({p:S.tcp.clone(),r:U.TOP_R,parca:"hamur topu"});
  return pts;
}
function carpisma(k){
  const sol=solids(), cav=cavities(), hits=[];
  for(const q of orneklem(k)){ for(const s of sol){ if(s.ad==='robot kaidesi'&&(q.parca==='üst kol'||q.parca==='ön kol')) continue; if(!inside(q.p,s.b,q.r)) continue; let ex=false; for(const c of cav){ if(insideShrunk(q.p,c.b,q.r*0.6)){ ex=true; break; } } if(!ex){ hits.push({p:q.p,parca:q.parca,engel:s.ad}); break; } } }
  return hits;
}
