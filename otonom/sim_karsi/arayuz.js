/* ================================================================
   AUTOKITCH · TABLA – BANT karşılaştırma · ARAYÜZ
   ================================================================ */
let simA, simB, speed=1, playing=false, last=performance.now();
const cvA=document.getElementById('cvA'), cvB=document.getElementById('cvB');
const dk=s=>s===null||s===undefined?'–':(s/60).toFixed(1)+' dk', yuz=v=>Math.round(v*100)+'%';

const SEN_NOT={
  tek:'<b style="color:#F5F5F7">Boş hat</b> — 1 pide + 2 lahmacun. İki hat da aynı saniyede sipariş alır; adımları yan yana izle.',
  uc:'<b style="color:#F5F5F7">3 müşteri</b> — 1\'er dk arayla.',
  aksam:'<b style="color:#30d158">VERİYE DAYALI</b> — Yemeksepeti 2023: 17:00–20:00 toplamın %36\'sı. Günde 80 pide + 200 lahmacun → <b style="color:#F5F5F7">53 sipariş / 3 saat</b>.',
  cmt:'<b style="color:#30d158">VERİYE DAYALI</b> — hafta sonu ×1,4 → <b style="color:#F5F5F7">74 sipariş / 3 saat</b>, tepe 18:00. İki hatta aynı siparişler, aynı pide çeşitleri.',
  surekli:'<b style="color:#ff453a">SINIR TESTİ</b> — 1 saat durmadan sipariş. 90 sn = saatte 40 sipariş.',
  bos:'Boş hat — üstteki düğmelerle ikisine birden sipariş at.'};

function rebuild(){
  document.getElementById('senNot').innerHTML=SEN_NOT[CFG.scenario]||'';
  const ord=scenarioOrders(CFG); simA=new Sim(CFG, ord, 'tabla'); simB=new Sim(CFG, ord, 'bant');
  playing=false; document.getElementById('play').textContent='▶ Başlat';
  document.getElementById('v-bantHiz').textContent=`${(G.WIN/CFG.dose).toFixed(1)} mm/sn (300 mm / ${CFG.dose} sn)`;
  refreshCmp(); document.getElementById('adim').innerHTML=adimHTML(); render();
}
function miniHTML(s){
  const m=s.metrics(), dn=s.orders.filter(o=>o.doneT!==null), H=CFG.hedefDk*60, as=dn.filter(o=>o.doneT-o.arr>H).length, u=s.delivered;
  const tile=(k,v)=>`<div class="m"><div class="k">${k}</div><div class="v">${v}</div></div>`;
  return tile('teslim', `${m.delivered} <small>/ ${s.orders.length} sip.</small>`)
    + tile('çıkan ürün', `${u.pide+u.lahm} <small>${u.pide}P · ${u.lahm}L · ${u.drink}İ</small>`)
    + tile('ort. bekleme', dk(m.avg).replace(' dk',' <small>dk</small>'))
    + tile('en kötü', `<span style="color:${m.max!==null&&m.max>H?'#ff453a':'#30d158'}">${dk(m.max).replace(' dk','')}</span> <small>dk</small>`)
    + tile('hedefi aşan', `<span style="color:${as?'#ff453a':'#30d158'}">${as}</span> <small>/ ${dn.length}</small>`)
    + tile('çıkış hızı', `${m.thr?m.thr.toFixed(0):'–'} <small>ürün/saat</small>`)
    + tile('robot', yuz(m.robot))
    + tile('fırın', yuz(m.oven))
    + tile(s.mode==='tabla'?'tabla meşgul':'bantta ürün', yuz(m.tas))
    + tile(s.mode==='tabla'?'ort. tabla turu':'ort. bantta', m.tur?`${Math.round(m.tur)} <small>sn</small>`:'–');
}
function render(){
  drawSim(cvA, simA); drawSim(cvB, simB);
  const sa=simA.saat(simA.t); document.getElementById('clock').textContent=sa?sa:simA.fmt(simA.t);
  document.getElementById('mA').innerHTML=miniHTML(simA); document.getElementById('mB').innerHTML=miniHTML(simB);
  for(const [id,s] of [['logA',simA],['logB',simB]]){
    document.querySelector('#'+id+' div').innerHTML=s.log.slice(-40).reverse().map(e=>`<div>${s.fmt(e.t)} · ${e.s}</div>`).join(''); }
}
/* zaman: iki motor aynı dt ile ilerler (0,5 sn'lik alt adımlar) */
setInterval(()=>{ const now=performance.now(); let dt=Math.min(0.25,(now-last)/1000)*speed; last=now; if(!playing) return;
  while(dt>1e-9){ const h=Math.min(0.5,dt); simA.step(h); simB.step(h); dt-=h; } }, 33);
function loop(){ if(playing) render(); requestAnimationFrame(loop); }

function refreshCmp(){
  const el=document.getElementById('cmp'), a=headless(CFG,'tabla'), b=headless(CFG,'bant');
  if(!a||!b){ el.innerHTML='<div class="note">"Boş" senaryoda hesap yok — sipariş verip izle.</div>'; return; }
  const sat=(ad,va,vb,na,nb,az)=>{ let ca='',cb=''; if(na!==null&&nb!==null&&Math.abs(na-nb)>1e-6){ const aIyi=az?na<nb:na>nb; ca=aIyi?'iyi':''; cb=aIyi?'':'iyi'; }
    return `<tr><td>${ad}</td><td class="${ca}">${va}</td><td class="${cb}">${vb}</td></tr>`; };
  const ur=m=>`${m.urun.pide+m.urun.lahm} (${m.urun.pide}P · ${m.urun.lahm}L) + ${m.urun.drink} içecek`;
  el.innerHTML=`<table><tr><th></th><th>◀ TABLA</th><th>BANT ▶</th></tr>
    ${sat('ort. bekleme',dk(a.avg),dk(b.avg),a.avg,b.avg,true)}
    ${sat('%95 bunun altında',dk(a.p95),dk(b.p95),a.p95,b.p95,true)}
    ${sat('en kötü bekleme',dk(a.max),dk(b.max),a.max,b.max,true)}
    ${sat(`hedefi (${CFG.hedefDk} dk) aşan sipariş`,a.asan,b.asan,a.asan,b.asan,true)}
    ${sat('çıkan ürün',ur(a),ur(b),null,null)}
    ${sat('son teslim',a.span?simA.fmt(a.span):'–',b.span?simB.fmt(b.span):'–',a.span,b.span,true)}
    ${sat('robot doluluk',yuz(a.robot),yuz(b.robot),null,null)}
    ${sat('fırın doluluk',yuz(a.oven),yuz(b.oven),null,null)}
    ${sat('taşıyıcı (tabla meşgul / bantta ürün)',yuz(a.tas),yuz(b.tas),null,null)}
    ${sat('ort. tabla turu / bantta kalma',a.tur?Math.round(a.tur)+' sn':'–',b.tur?Math.round(b.tur)+' sn':'–',null,null)}</table>
    <div class="note">Yeşil = o satırda daha iyi olan. Hesap bu senaryonun tamamı (0,5 sn adım). Tabla turu = hamur tablaya düştüğü andan tabla pres altına boş döndüğü ana kadar.</div>`;
}
function adimHTML(){
  const c=CFG, T=T0, mv=(a,b)=>Math.abs(b-a)/c.vX, bake=(c.tekHiz==='lahm'&&c.lahm)?c.bakeLahm:c.bakePide, v=c.chamber/bake, bv=G.WIN/c.dose;
  const r=(ad,sn,not)=>`<tr><td>${ad}${not?` <span style="color:var(--gray)">· ${not}</span>`:''}</td><td class="sn">${typeof sn==='number'?sn.toFixed(1)+' sn':sn}</td></tr>`;
  const tabla=(adim)=>{ let rows='', top=0, x=G.P; const add=(ad,sn,not)=>{ rows+=r(ad,sn,not); if(typeof sn==='number') top+=sn; };
    add('tabla örse iner',c.zMove); add('pres tablanın üstüne basar',c.pressCycle); add('örsten kalkar',c.zMove);
    for(const a of adim){ add(`K${a.k+1} ${KASET[a.k].ad} altına gider`,mv(x,G.K[a.k]),`${Math.abs(G.K[a.k]-x)} mm`); x=G.K[a.k];
      add('ağıza kalkar',c.zMove); add(`dozaj: döner + kayar → tartı +${a.g} g`,c.dose); add('helezon geri emer, klape kapanır',c.sucBack); add('iner',c.zMove); }
    add('fırın ağzına gider',mv(x,G.F),`${Math.abs(G.F-x)} mm`); add('fırın sırası',`bekler (≤ ${Math.round(c.pitch/v)} sn)`);
    add('itici iner',c.stripDown); add('itici pideyi fırın bandına iter · tartı 0 g',c.push); add('pres altına boş döner',mv(G.F,G.P),`${G.F-G.P} mm`);
    const ek=Math.max(0,(c.atosaTur||0)-top); if(ek>0) rows+=r(`Atosa hızı: dozaja eklenen süre (ürün başına en az ${c.atosaTur} sn)`,ek);
    return rows+`<tr class="top"><td>tabla turu (fırın sırası hariç)</td><td class="sn">${(top+ek).toFixed(1)} sn</td></tr>`; };
  return `<table class="adim">
    <tr class="top"><td>ORTAK · robot</td><td></td></tr>
    ${r('robot rayda gider',`${c.rail} cm/sn`)}${r('çekmeceden hamur topunu kavrar',T.takeDough)}${r('pres altına bırakır (tablaya / prese)',T.pressDrop)}
    <tr class="top"><td>◀ TABLA · 1 lahmacun (K3 harç)</td><td></td></tr>${tabla([{k:2,g:108}])}
    <tr class="top"><td>◀ TABLA · 1 sucuklu pide (K1 kaşar + K2 sucuk)</td><td></td></tr>${tabla([{k:0,g:90},{k:1,g:70}])}
    <tr class="top"><td>BANT ▶ · her ürün</td><td></td></tr>
    ${r('pres basar',c.pressCycle)}${r('presten banda aktarım',c.toBelt)}${r('bant girişi: önceki ürün 350 mm ilerlemiş olmalı','bekler')}
    ${r(`bantta akış · ${G.XOUT-G.XIN} mm, ${bv.toFixed(1)} mm/sn`,(G.XOUT-G.XIN)/bv)}${r('↳ her başlığın altından geçerken dozaj (300 mm pencere)',c.dose,'akarken, aynı süre içinde')}
    ${r('bant sonu: fırın sırası yoksa bütün bant durur','bekler')}
    <tr class="top"><td>ORTAK · fırın → dolap</td><td></td></tr>
    ${r(`fırından geçiş · ${c.chamber+c.extra} mm, ${v.toFixed(2)} mm/sn`,(c.chamber+c.extra)/v,`haznede ${bake} sn`)}${r('fırın 1 ürünü şu aralıkla alır',c.pitch/v,`${c.pitch} mm adım`)}
    ${r('kesme plakası: pide sprey + 8 bıçak / lahmacun geçiş',`${c.cutPide} / ${c.cutLahm} sn`)}${r('kutu katlama (hep 1 kutu hazır)',c.fold)}
    ${r('robot kutuyu kavrar',T.boxTake)}${r('robot QR dolabına koyar',T.lockerPlace)}${r('içecek: çekmeceden al + dolaba koy',`${T.drinkTake} + ${T.drinkPlace} sn`)}</table>
    <div class="note"><b style="color:#F5F5F7">Varsayımlar:</b> kaset adımı 150 mm (son kaset fırın duvarından 180 mm geride, Ø340 tabla çarpmasın) · tabla fırına pideyi arkadan iterek verir (geri çekilirse pide ile bant arasında boşluk kalıp katlanır) · bantlı hatta başlık 300 mm, bant hızı = 300 mm / dozaj süresi · dozaj süresi iki hatta aynı · pide çeşidi 4 çeşit eşit (kaşarlı 130 g kaşar · sucuklu 90 g kaşar + 70 g sucuk · kıymalı 160 g · kuşbaşılı 145 g) · lahmacun harcı 108 g, iki harç kaseti sırayla · fırın tek bant, pide hızında · tabla turu Atosa verisine göre ürün başına en az ${c.atosaTur} sn (üretici: bir pizza en fazla 1 dk; kısa kalan süre dozaja eklenir) · robot sonraki hamuru tabla çalışırken getirip pres önünde bekler (ayarlardan kapatılabilir).</div>`;
}

/* --- panel --- */
document.querySelectorAll('#cfg .sw').forEach(sw=>{ sw.onclick=()=>{ sw.classList.toggle('on'); CFG[sw.dataset.k]=sw.classList.contains('on'); syncPanel(); rebuild(); }; });
document.querySelectorAll('#cfg select, #cfg input[type=number]').forEach(el=>{ el.onchange=()=>{ const v=el.value; CFG[el.dataset.k]=isNaN(parseFloat(v))?v:parseFloat(v); rebuild(); }; });
document.querySelectorAll('#cfg input[type=range]').forEach(el=>{
  el.oninput=()=>{ CFG[el.dataset.k]=parseFloat(el.value); document.getElementById('v-'+el.dataset.k).textContent= el.dataset.k==='robotK'?parseFloat(el.value).toFixed(2):(el.dataset.k==='drinkPct'?'%'+el.value:el.value); };
  el.onchange=()=>rebuild(); });
function syncPanel(){
  document.getElementById('injL').style.display=CFG.lahm?'':'none'; document.getElementById('injPL').style.display=CFG.lahm?'':'none';
  document.getElementById('rateWrap').style.display=CFG.scenario==='surekli'?'inline-flex':'none';
  document.getElementById('seedBtn').style.display=['tek','uc','bos'].includes(CFG.scenario)?'none':'';
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
document.querySelectorAll('[data-inj]').forEach(b=>b.onclick=()=>{ const it=b.dataset.inj.split(','); simA.addOrder(it, simA.t); simB.addOrder(it, simB.t); render(); });

/* KAPASİTE BUL — 5 farklı saatlik akış, hiçbir müşterinin hedefi aşmadığı en yüksek hız (iki hat ayrı ayrı) */
document.getElementById('kapBtn').onclick=()=>{
  const btn=document.getElementById('kapBtn'), eski=btn.textContent; btn.textContent='hesaplanıyor…'; btn.disabled=true;
  setTimeout(()=>{
    const bul=(mode)=>{ let iyi=null, sinir=null;
      for(const gap of [400,330,280,240,210,190,170,150,140,130,120,110,100,90,80,70,60]){
        let enKotu=0, urun=0, n=0;
        for(const sd of [1,2,3,4,5]){ const cf=Object.assign(JSON.parse(JSON.stringify(CFG)),{scenario:'surekli', gapSec:gap, seed:sd});
          const s=new Sim(cf, scenarioOrders(cf), mode); let g=0; while(!s.done && g++<30000) s.step(1);
          const w=s.orders.filter(o=>o.doneT!==null).map(o=>o.doneT-o.arr); if(!w.length) continue;
          enKotu=Math.max(enKotu, ...w); urun+=s.deliveredUnits; n++; }
        const r={gap, sip:Math.round(3600/gap), enKotu:enKotu/60, urun:n?urun/n:0};
        if(r.enKotu<=CFG.hedefDk) iyi=r; else { sinir=r; break; } }
      return {iyi, sinir}; };
    const a=bul('tabla'), b=bul('bant');
    const h=(ad,x)=>x.iyi?`<tr><td>${ad}</td><td><b>${x.iyi.sip} sipariş/saat</b> (her ${x.iyi.gap} sn)</td><td>~${Math.round(x.iyi.urun)} ürün/saat</td><td>en kötü ${x.iyi.enKotu.toFixed(1)} dk</td></tr>`:`<tr><td>${ad}</td><td colspan="3" style="color:#ff453a">en düşük hızda bile hedef tutmuyor</td></tr>`;
    document.getElementById('kap').innerHTML=`<table style="margin-top:10px"><tr><th>KAPASİTE · ${CFG.hedefDk} dk kuralı</th><th>sipariş hızı</th><th>çıkan ürün</th><th>5 akışın en kötüsü</th></tr>${h('◀ TABLA',a)}${h('BANT ▶',b)}</table>
      <div class="note">Her hız 5 farklı rastgele saatle denendi; bir sonraki hızda en kötü bekleme hedefi aşıyor${a.sinir?` (tabla: saatte ${a.sinir.sip} siparişte ${a.sinir.enKotu.toFixed(1)} dk)`:''}${b.sinir?` (bant: saatte ${b.sinir.sip} siparişte ${b.sinir.enKotu.toFixed(1)} dk)`:''}.</div>`;
    btn.textContent=eski; btn.disabled=false; }, 30);
};
/* TAM YÜK — sipariş hattın yetişemeyeceği hızda (20 sn'de bir), 60 dk sonunda kaç ürün çıktı */
document.getElementById('tamBtn').onclick=()=>{
  const btn=document.getElementById('tamBtn'), eski=btn.textContent; btn.textContent='hesaplanıyor…'; btn.disabled=true;
  setTimeout(()=>{
    const kos=(mode)=>{ let u=0, rob=0, ov=0, ts=0; const seeds=[1,2,3];
      for(const sd of seeds){ const cf=Object.assign(JSON.parse(JSON.stringify(CFG)),{scenario:'surekli', gapSec:20, seed:sd});
        const s=new Sim(cf, scenarioOrders(cf), mode); while(s.t<3600-1e-9) s.step(0.5); const m=s.metrics(); u+=s.deliveredUnits; rob+=m.robot; ov+=m.oven; ts+=m.tas; }
      const n=seeds.length; return {u:u/n, rob:rob/n, ov:ov/n, ts:ts/n}; };
    const a=kos('tabla'), b=kos('bant');
    const h=(ad,x)=>`<tr><td>${ad}</td><td><b>${Math.round(x.u)} ürün</b></td><td>${yuz(x.rob)}</td><td>${yuz(x.ov)}</td><td>${yuz(x.ts)}</td></tr>`;
    document.getElementById('kap').innerHTML=`<table style="margin-top:10px"><tr><th>TAM YÜK · 60 dk</th><th>çıkan ürün</th><th>robot</th><th>fırın</th><th>tabla / bant</th></tr>${h('◀ TABLA',a)}${h('BANT ▶',b)}</table>
      <div class="note">Sipariş 20 sn'de bir (hattın yetişemeyeceği hız), 3 farklı saatin ortalaması. İlk ürünler yolda olduğu için ilk ~6 dk teslim yok.</div>`;
    btn.textContent=eski; btn.disabled=false; }, 30);
};
function fit(){ for(const cv of [cvA,cvB]){ const w=cv.parentElement.clientWidth; cv.style.height=(w*cv.height/cv.width)+'px'; } }
window.addEventListener('resize', fit); fit();
syncPanel(); rebuild(); requestAnimationFrame(loop);
