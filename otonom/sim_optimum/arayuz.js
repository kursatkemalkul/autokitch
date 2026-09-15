/* ================================================================
   AUTOKITCH · OPTİMUM HAT · ARAYÜZ
   ================================================================ */
let sim, speed=1, playing=false, last=performance.now();
const cv=document.getElementById('cv');
const dk=s=>s===null||s===undefined?'–':(s/60).toFixed(1)+' dk', yuz=v=>Math.round(v*100)+'%';
const TR=s=>String(s).replace(/(\d)\.(\d)/g,'$1,$2');   // ekranda ondalık virgül

const SEN_NOT={
  tek3:'<b style="color:#F5F5F7">Tek sipariş · 3 lahmacun + içecek</b> — robot 3 hamuru sırayla getirir; lahmacunlar fırından arka arkaya çıkar ve aynı kutuya düşer, kutu 3. lahmacunla kapanır. Robot kutuyu ve içeceği aynı QR gözüne koyar.',
  uc:'<b style="color:#F5F5F7">3 müşteri · 30 sn arayla</b> — 3 lahmacun + içecek · 2 pide · 2 lahmacun + içecek.',
  aksam:'<b style="color:#30d158">VERİYE DAYALI</b> — Yemeksepeti 2023: 17:00–20:00 toplamın %36\'sı. Günde 80 pide + 200 lahmacun → <b style="color:#F5F5F7">53 sipariş / 3 saat</b>.',
  cmt:'<b style="color:#30d158">VERİYE DAYALI</b> — hafta sonu ×1,4 → <b style="color:#F5F5F7">74 sipariş / 3 saat</b>, tepe 18:00.',
  surekli:'<b style="color:#ff453a">SINIR TESTİ</b> — 1 saat durmadan sipariş.',
  bos:'Boş hat — üstteki düğmelerle sipariş ver.'};

function rebuild(){
  document.getElementById('senNot').innerHTML=SEN_NOT[CFG.scenario]||'';
  sim=new Sim(CFG, scenarioOrders(CFG));
  playing=false; document.getElementById('play').textContent='▶ Başlat';
  document.getElementById('kap').innerHTML='';
  document.getElementById('hesap').innerHTML=TR(hesapHTML());
  document.getElementById('adim').innerHTML=TR(adimHTML());
  refreshSonuc(); render();
}
function miniHTML(s){
  const m=s.metrics(), u=s.delivered, T=Math.max(s.t,1), U=s.u, H=CFG.hedefDk*60;
  const tile=(k,v)=>`<div class="m"><div class="k">${k}</div><div class="v">${v}</div></div>`;
  return tile('teslim', `${m.delivered} <small>/ ${s.orders.length} sipariş</small>`)
    + tile('çıkan ürün', `${u.pide+u.lahm} <small>${u.pide}P · ${u.lahm}L · ${u.drink}İ</small>`)
    + tile('kullanılan kutu', `${s.boxesUsed}`)
    + tile('ort. bekleme', dk(m.avg).replace(' dk',' <small>dk</small>'))
    + tile('en uzun bekleme', `<span style="color:${m.max!==null&&m.max>H?'#ff453a':'#30d158'}">${dk(m.max).replace(' dk','')}</span> <small>dk</small>`)
    + tile('tabla çalışıyor', yuz((U.tabla.calisir+U.tabla.birakma)/T))
    + tile('fırın dolu', yuz(U.firinDolu/T/(CFG.chamber/CFG.pitch)))
    + tile('robot iş (kol + ray)', yuz((U.robot.kol+U.robot.yol)/T))
    + tile('robot hamurla bekler', yuz(U.robot.bekle/T))
    + tile('ort. tabla turu', m.tur?`${Math.round(m.tur)} <small>sn</small>`:'–');
}
function render(){
  drawSim(cv, sim);
  const sa=sim.saat(sim.t); document.getElementById('clock').textContent=sa?sa:sim.fmt(sim.t);
  document.getElementById('m').innerHTML=TR(miniHTML(sim));
  document.querySelector('#log div').innerHTML=sim.log.slice(-60).reverse().map(e=>`<div>${sim.fmt(e.t)} · ${e.s}</div>`).join('');
}
/* zaman: 0,5 sn'lik alt adımlar */
setInterval(()=>{ const now=performance.now(); let dt=Math.min(0.25,(now-last)/1000)*speed; last=now; if(!playing) return;
  while(dt>1e-9){ const h=Math.min(0.5,dt); sim.step(h); dt-=h; } }, 33);
function loop(){ if(playing) render(); requestAnimationFrame(loop); }

/* ---------- HESAP (formül) ---------- */
function turHesap(adim){ const c=CFG; let top=2*c.zMove+c.pressCycle, x=G.P;
  for(const a of adim){ top+=Math.abs(G.K[a.k]-x)/c.vX+2*c.zMove+c.dose+c.sucBack; x=G.K[a.k]; }
  top+=Math.abs(G.F-x)/c.vX+c.stripDown+c.push+Math.abs(G.F-G.P)/c.vX; return Math.max(top, c.atosaTur||0); }
function hesapHTML(){
  const c=CFG, v=c.chamber/c.bake, tur=turHesap([{k:2,g:108}]), bir=T0.pressDrop*c.robotK, ara=tur+bir, alma=c.pitch/v, goz=c.chamber/c.pitch, bekler=alma>ara+1e-9, hat=Math.max(ara,alma);
  return `<table>
    <tr><td>tabla turu (Atosa) + robotun hamuru bırakması</td><td class="sn">${tur.toFixed(0)} + ${bir.toFixed(0)} = <b>${ara.toFixed(0)} sn</b></td><td>saatte ${(3600/ara).toFixed(1)}</td></tr>
    <tr><td>fırın ${c.chamber} mm = ${goz.toFixed(2)} göz · 1 ürünü şu aralıkla alır</td><td class="sn"><b>${alma.toFixed(1)} sn</b></td><td>saatte ${(3600/alma).toFixed(1)}</td></tr>
    <tr><td>fırın tablayı bekletir mi?</td><td class="sn ${bekler?'kotu':'iyi'}">${bekler?'evet · her üründe '+(alma-ara).toFixed(1)+' sn':'hayır ✓'}</td><td></td></tr>
    <tr><td>tabla hızına tam eş hazne</td><td class="sn">${Math.ceil(c.pitch*c.bake/ara)} mm</td><td>${(c.bake/ara).toFixed(2)} göz</td></tr>
    <tr><td><b>hat hızı · robot hep zamanında</b></td><td class="sn"><b>${hat.toFixed(1)} sn'de 1</b></td><td><b>saatte ${(3600/hat).toFixed(1)}</b></td></tr></table>`;
}
/* ---------- BU SENARYO ---------- */
function refreshSonuc(){
  const el=document.getElementById('sonuc'), s=headless(CFG);
  if(!s){ el.innerHTML='<div class="note">"Boş" senaryoda hesap yok — sipariş verip izle.</div>'; return; }
  const m=s.metrics(), u=m.urun, H=CFG.hedefDk*60;
  el.innerHTML=`<table>
    <tr><td>teslim edilen sipariş</td><td>${m.delivered} / ${s.orders.length}</td></tr>
    <tr><td>çıkan ürün</td><td>${u.pide+u.lahm} (${u.pide} pide · ${u.lahm} lahmacun) + ${u.drink} içecek</td></tr>
    <tr><td>kullanılan kutu</td><td>${m.kutu}${CFG.siparisKutu&&m.kutu<u.pide+u.lahm?` <span style="color:var(--gray)">(her ürün ayrı kutuda olsaydı ${u.pide+u.lahm})</span>`:''}</td></tr>
    <tr><td>ortalama bekleme</td><td>${dk(m.avg)}</td></tr>
    <tr><td>%95 bunun altında</td><td>${dk(m.p95)}</td></tr>
    <tr><td>en uzun bekleme</td><td class="${m.max!==null&&m.max>H?'kotu':'iyi'}">${dk(m.max)}</td></tr>
    <tr><td>hedefi (${CFG.hedefDk} dk) aşan sipariş</td><td class="${m.asan?'kotu':'iyi'}">${m.asan}</td></tr>
    <tr><td>son teslim</td><td>${s.fmt(m.span)}</td></tr>
    <tr><td>ortalama tabla turu</td><td>${m.tur?Math.round(m.tur)+' sn':'–'}</td></tr></table>`;
  el.innerHTML=TR(el.innerHTML);
}
/* ---------- ADIMLAR ---------- */
function adimHTML(){
  const c=CFG, T=T0, k=c.robotK, mv=(a,b)=>Math.abs(b-a)/c.vX, v=c.chamber/c.bake;
  const V='varsayım', A='Atosa: ürün başına en fazla 1 dk', F='satıcı: 3–4 dk';
  const r=(ad,sn,kay)=>`<tr><td>${ad}</td><td class="sn">${typeof sn==='number'?sn.toFixed(1)+' sn':sn}</td><td class="kay">${kay||''}</td></tr>`;
  const bas=(ad)=>`<tr class="top"><td>${ad}</td><td></td><td></td></tr>`;
  const tabla=(adim)=>{ let rows='', top=0, x=G.P; const add=(ad,sn,kay)=>{ rows+=r(ad,sn,kay); if(typeof sn==='number') top+=sn; };
    add('tabla örse iner',c.zMove,V); add('pres tablanın üstüne basar',c.pressCycle,V); add('örsten kalkar',c.zMove,V);
    for(const a of adim){ add(`K${a.k+1} ${KASET[a.k].ad} altına gider (${Math.abs(G.K[a.k]-x)} mm)`,mv(x,G.K[a.k]),V); x=G.K[a.k];
      add('ağıza kalkar',c.zMove,V); add(`dozaj: döner + kayar → tartı +${a.g} g`,c.dose,V); add('helezon geri emer, klape kapanır',c.sucBack,V); add('iner',c.zMove,V); }
    add(`fırın ağzına gider (${Math.abs(G.F-x)} mm)`,mv(x,G.F),V); add('fırın sırası (fırın 1 ürünü aldıysa bekler)',`≤ ${(c.pitch/v).toFixed(0)} sn`,'hesap');
    add('itici iner',c.stripDown,V); add('itici ürünü fırın bandına iter',c.push,V); add(`pres altına boş döner (${G.F-G.P} mm)`,mv(G.F,G.P),V);
    const ek=Math.max(0,(c.atosaTur||0)-top); if(ek>0) rows+=r('Atosa hızına tamamlama (dozaja eklenir)',ek,A);
    return rows+`<tr class="top"><td>tabla turu</td><td class="sn">${(top+ek).toFixed(1)} sn</td><td></td></tr>`; };
  return `<table class="adim"><tr><th>adım</th><th class="sn">süre</th><th>kaynak</th></tr>
    ${bas('1 · ROBOT · çekmeceden hamur → tabla')}
    ${r('robot rayda gider',`${c.rail} cm/sn`,V)}${r('çekmece açılır (robot yaklaşırken)','—',V)}${r('hamur topunu kavrar',T.takeDough*k,V)}
    ${r('pres önüne gelir · tabla dönene kadar hamur elde bekler','bekler',c.onceden?'önceden getirir':'')}${r('hamuru tablaya bırakır (pres altı)',T.pressDrop*k,V)}
    ${bas('2 · TABLA · 1 lahmacun (K3 harç 108 g)')}${tabla([{k:2,g:108}])}
    ${bas('2 · TABLA · 1 sucuklu pide (K1 kaşar 90 g + K2 sucuk 70 g)')}${tabla([{k:0,g:90},{k:1,g:70}])}
    ${bas('3 · FIRIN · tek sıra')}
    ${r(`hazne ${c.chamber} mm = ${(c.chamber/c.pitch).toFixed(2)} göz · adım ${c.pitch} mm (Ø300 ürün + ${c.pitch-300} mm boşluk)`,'—','hesap')}
    ${r('haznede pişme · pide ve lahmacun aynı',c.bake,F)}
    ${r(`bant hızı ${v.toFixed(2)} mm/sn · fırın 1 ürünü şu aralıkla alır`,c.pitch/v,'hesap')}
    ${r(`fırından geçiş (hazne + ${c.extra} mm duvar)`,(c.chamber+c.extra)/v,'hesap')}
    ${bas('4 · KESME PLAKASI')}
    ${r('pide: sprey + 8 bıçak',c.cutPide,V)}${r('lahmacun: geçiş',c.cutLahm,V)}
    ${bas('5 · KUTU')}
    ${r('kutu şarjörden katlanır (hep 1 kutu hazır)',c.fold,V)}
    ${r('pide: her pide kendi kutusunda','—','')}
    ${r(c.siparisKutu?`lahmacun: aynı siparişin lahmacunları aynı kutuya (en çok ${c.lahmKutu}) · kutu, siparişin son lahmacununu açık bekler`:'lahmacun: her lahmacun kendi kutusunda', c.siparisKutu?'~66 sn / lahmacun':'—', c.siparisKutu?'karar':'')}
    ${r('kapak kapanır',c.lid,V)}
    ${bas('6 · ROBOT · kutu ve içecek → QR dolabı')}
    ${r('kutuyu kavrar',T.boxTake*k,V)}${r('siparişin QR gözüne koyar',T.lockerPlace*k,V)}
    ${r('içecek: K5 çekmecesinden alır',T.drinkTake*k,V)}${r('içeceği aynı göze koyar',T.drinkPlace*k,V)}
    ${r(c.akilli?'iş sırası: kutu / içecek işini ancak sonraki hamuru tabla dönmeden getirebilecekse yapar, yoksa önce hamur':'iş sırası: önce kutu, sonra hamur, sonra içecek','—',c.akilli?'akıllı sıra':'basit sıra')}
    ${bas('7 · MÜŞTERİ')}
    ${r('sipariş tamamlanınca QR ile alır, göz boşalır',T.customerPickup,V)}
  </table>
  <div class="note"><b style="color:#F5F5F7">Kaynaklar:</b> Atosa tabla hızı üretici verisi (bir pizza en fazla 1 dk) · pişme süresi konveyörlü pide-lahmacun fırını satıcı sayfaları (3–4 dk → 3,5 dk alındı) · "varsayım" yazan süreler ölçülmedi; robot, kesme ve kutu seçilince güncellenecek.</div>`;
}

/* ---------- panel ---------- */
document.querySelectorAll('#cfg .sw').forEach(sw=>{ sw.onclick=()=>{ sw.classList.toggle('on'); CFG[sw.dataset.k]=sw.classList.contains('on'); rebuild(); }; });
document.querySelectorAll('#cfg select, #cfg input[type=number]').forEach(el=>{ el.onchange=()=>{ const v=el.value; CFG[el.dataset.k]=isNaN(parseFloat(v))?v:parseFloat(v); rebuild(); }; });
document.querySelectorAll('#cfg input[type=range]').forEach(el=>{
  el.oninput=()=>{ CFG[el.dataset.k]=parseFloat(el.value); document.getElementById('v-'+el.dataset.k).textContent= el.dataset.k==='robotK'?parseFloat(el.value).toFixed(2):(el.dataset.k==='drinkPct'?'%'+el.value:el.value); };
  el.onchange=()=>rebuild(); });
function syncPanel(){
  document.getElementById('rateWrap').style.display=CFG.scenario==='surekli'?'inline-flex':'none';
  document.getElementById('seedBtn').style.display=['tek3','uc','bos'].includes(CFG.scenario)?'none':'';
}
document.getElementById('scenario').onchange=e=>{ CFG.scenario=e.target.value; syncPanel(); rebuild(); };
const gapEl=document.getElementById('gap');
function gapTxt(){ document.getElementById('v-gap').textContent=CFG.gapSec+' sn'; document.getElementById('v-gaph').textContent='= saatte '+Math.round(3600/CFG.gapSec)+' sipariş'; }
gapEl.oninput=e=>{ CFG.gapSec=parseInt(e.target.value); gapTxt(); }; gapEl.onchange=()=>rebuild(); gapTxt();
document.getElementById('seedBtn').onclick=()=>{ CFG.seed=(CFG.seed||1)+1; rebuild(); };
document.getElementById('lahmPct').oninput=e=>{ CFG.lahmPct=parseInt(e.target.value); document.getElementById('v-lahmPct').textContent='%'+CFG.lahmPct; };
document.getElementById('lahmPct').onchange=()=>rebuild();
document.getElementById('play').onclick=()=>{ playing=!playing; last=performance.now(); document.getElementById('play').textContent=playing?'❚❚ Durdur':'▶ Başlat'; };
document.getElementById('reset').onclick=rebuild;
document.querySelectorAll('.spd').forEach(b=>b.onclick=()=>{ speed=parseFloat(b.dataset.s); document.querySelectorAll('.spd').forEach(x=>x.classList.toggle('on',x===b)); });
document.getElementById('injDrink').onclick=e=>e.currentTarget.classList.toggle('on');
document.querySelectorAll('[data-inj]').forEach(b=>b.onclick=()=>{ const it=b.dataset.inj.split(','), ic=document.getElementById('injDrink').classList.contains('on'); sim.addOrder(it, sim.t, undefined, ic); render(); });

/* HAT DOLU · 60 DK — kim yüzde kaç çalışıyor */
document.getElementById('tamBtn').onclick=()=>{
  const btn=document.getElementById('tamBtn'), eski=btn.textContent; btn.textContent='hesaplanıyor…'; btn.disabled=true;
  setTimeout(()=>{
    const r=tamYuk(CFG), p=v=>Math.round(v*100)+'%', tabla=r.tabla.calisir+r.tabla.birakma, robotIs=r.robot.kol+r.robot.yol;
    document.getElementById('kap').innerHTML=`<table style="margin-top:10px">
      <tr><th colspan="2">HAT DOLU · 60 DAKİKA ÖLÇÜM</th></tr>
      <tr><td><b>60 dakikada çıkan ürün</b></td><td><b>${r.urun.toFixed(1)}</b></td></tr>
      <tr><td>kullanılan kutu</td><td>${r.kutu.toFixed(1)}</td></tr>
      <tr><td>fırına iki ürün arası (ortalama)</td><td>${(3600/r.giris).toFixed(1)} sn</td></tr>
      <tr><td><b>TABLA çalışıyor</b></td><td><b>${p(tabla)}</b> <span style="color:var(--gray)">tur ${p(r.tabla.calisir)} + hamur bırakma ${p(r.tabla.birakma)}</span></td></tr>
      <tr><td>&nbsp;&nbsp;· fırın sırası bekler</td><td>${p(r.tabla.firin)}</td></tr>
      <tr><td>&nbsp;&nbsp;· hamur bekler</td><td>${p(r.tabla.hamur)}</td></tr>
      <tr><td><b>FIRIN dolu</b></td><td><b>${p(r.firin)}</b></td></tr>
      <tr><td><b>ROBOT iş yapıyor</b></td><td><b>${p(robotIs)}</b> <span style="color:var(--gray)">kol ${p(r.robot.kol)} + ray ${p(r.robot.yol)}</span></td></tr>
      <tr><td>&nbsp;&nbsp;· hamur elde tablayı bekler</td><td>${p(r.robot.bekle)}</td></tr>
      <tr><td>&nbsp;&nbsp;· boş</td><td>${p(r.robot.bos)}</td></tr>
      <tr><td><b>KESME</b> çalışıyor</td><td>${p(r.kesme)}</td></tr>
      <tr><td><b>KUTU</b> katlama · kapak</td><td>${p(r.katlama)} · ${p(r.kapak)}</td></tr></table>
      <div class="note">Sipariş 20 sn'de bir gelir (hattın yetişemeyeceği hız). İlk 60 dk hat dolsun diye sayılmaz; tablo sonraki 60 dakikanın ölçümü, ${r.n} farklı sipariş akışının ortalaması.</div>`;
    document.getElementById('kap').innerHTML=TR(document.getElementById('kap').innerHTML);
    btn.textContent=eski; btn.disabled=false; }, 30);
};
/* KAPASİTE — hiçbir müşterinin hedefi aşmadığı en yüksek sipariş hızı */
document.getElementById('kapBtn').onclick=()=>{
  const btn=document.getElementById('kapBtn'), eski=btn.textContent; btn.textContent='hesaplanıyor…'; btn.disabled=true;
  setTimeout(()=>{
    let iyi=null, sinir=null;
    for(const gap of [400,330,280,240,210,190,170,150,140,130,120,110,100,90,80,70,60]){
      let enKotu=0, urun=0, n=0;
      for(const sd of [1,2,3,4,5]){ const cf=Object.assign(JSON.parse(JSON.stringify(CFG)),{scenario:'surekli', gapSec:gap, seed:sd});
        const s=new Sim(cf, scenarioOrders(cf)); let g=0; while(!s.done && g++<30000) s.step(1);
        const w=s.orders.filter(o=>o.doneT!==null).map(o=>o.doneT-o.arr); if(!w.length) continue;
        enKotu=Math.max(enKotu, ...w); urun+=s.deliveredUnits; n++; }
      const r={gap, sip:Math.round(3600/gap), enKotu:enKotu/60, urun:n?urun/n:0};
      if(r.enKotu<=CFG.hedefDk) iyi=r; else { sinir=r; break; } }
    document.getElementById('kap').innerHTML = iyi ? `<table style="margin-top:10px"><tr><th colspan="2">KAPASİTE · ${CFG.hedefDk} dk kuralı · 1 saatlik sipariş akışı</th></tr>
      <tr><td>en yüksek sipariş hızı</td><td><b>saatte ${iyi.sip} sipariş</b> (her ${iyi.gap} sn)</td></tr>
      <tr><td>bu siparişlerdeki ürün</td><td>~${Math.round(iyi.urun)} ürün</td></tr>
      <tr><td>5 farklı saatin en uzun beklemesi</td><td>${iyi.enKotu.toFixed(1)} dk</td></tr></table>
      <div class="note">Her hız 5 farklı rastgele saatle denendi.${sinir?` Bir sonraki hızda (saatte ${sinir.sip} sipariş) en uzun bekleme ${sinir.enKotu.toFixed(1)} dk oluyor.`:''}</div>`
      : '<div class="note" style="color:#ff453a">En düşük hızda bile hedef tutmuyor.</div>';
    document.getElementById('kap').innerHTML=TR(document.getElementById('kap').innerHTML);
    btn.textContent=eski; btn.disabled=false; }, 30);
};
function fit(){ const w=cv.clientWidth; cv.style.height=(w*cv.height/cv.width)+'px'; }
window.addEventListener('resize', fit); fit();
syncPanel(); rebuild(); requestAnimationFrame(loop);
