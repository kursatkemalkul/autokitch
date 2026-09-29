// AUTOKITCH · hat/model3d.js v20 (kesit yüzü dolu) · v2 — gerçek üretim modelini gösterir + KESİT + ÖLÇÜ araçları.
// model-viewer'ın materialFromPoint'i malzeme adını verir; her birim kendi malzemesini taşır (hat_montaj_v7.py),
// eşleşme durum.json'daki "mal" alanından kurulur. Ayrı bir tıklama katmanı yok — model neyse o.
//
// ÜÇ TUZAK (üçü de ölçülerek bulundu):
//  1 materialFromPoint ve positionAndNormalFromPoint PENCERE koordinatı ister (içeride kendi
//    getBoundingClientRect'ini çıkarır). Eleman koordinatı verilince seçim rect.top kadar kayıyor.
//  2 model-viewer'ın 'load' olayı ve mv.model geç geliyor (~13 sn) → yoklayarak kurulur.
//  3 Sürüklerken bırakılan tıklama parçayı açıyordu (Kemal, 22 Eyl) → 6 px'ten fazla hareket varsa
//    tıklama sayılmaz; açma artık ÇİFT TIKLA.
//
// KESİT: model-viewer three.js kullanıyor ama renderer'ı dışarı vermiyor. Sahnedeki ilk mesh'in
// onBeforeRender kancasıyla renderer yakalanıp localClippingEnabled açılıyor. Kesme düzlemi için
// THREE.Plane gerekmiyor — WebGLClipping içeride kendi düzlemine copy() yapıyor, {normal,constant}
// düz nesnesi yetiyor (canlı sayfada ölçüldü). Yakalanamazsa kesit düğmeleri kapanır, sayfa kırılmaz.
(function () {
  'use strict';
  const SAHNE = mv => { const s = Object.getOwnPropertySymbols(mv).find(x => x.description === 'scene'); return s ? mv[s] : null; };
  const EKSEN = { x: ['X', 'en'], y: ['Y', 'yükseklik'], z: ['Z', 'derinlik'] };

  window.model3d = function (opt) {
    const mv = document.getElementById(opt.mv), etiket = document.getElementById(opt.etiket);
    const kap = mv.closest('.m3') || mv.parentNode;
    let BIRIM = {}, ASIL = {}, GRUP = {}, secili = null, kilit = null, gercekVar = false;

    const MN = (x, y) => mv.materialFromPoint(x, y);                 // PENCERE koordinatı (1. tuzak; getNDC her seferinde taze rect okur)
    const PN = (x, y) => mv.positionAndNormalFromPoint(x, y);
    const anahtar = ad => ad.split('__')[0];                        // M<modül>_<kod>__<ton> → birim anahtarı
    const gercek = b => b && b.durum && b.durum.indexOf('GERCEK') === 0;
    function grupAnahtari(b) { return opt.grup === 'modul' ? b.modul : b.kod; }

    function kur() {
      if (!mv.model) return;
      GRUP = {}; ASIL = {};
      gercekVar = Object.keys(BIRIM).some(k => gercek(BIRIM[k]));
      mv.model.materials.forEach(m => {
        const b = BIRIM[anahtar(m.name)];
        ASIL[m.name] = 1;                                           // yalnız "kuruldu" işareti; renge dokunulmuyor
        if (!b) return;
        const k = grupAnahtari(b);
        (GRUP[k] = GRUP[k] || { birimler: [], mat: [] }).mat.push(m);
        if (GRUP[k].birimler.indexOf(b) < 0) GRUP[k].birimler.push(b);
      });
      araclariKur();
      if (opt.hazir) opt.hazir(GRUP);
    }

    function vurgula(k) {
      if (secili === k) return;
      secili = k;
      const g = k && GRUP[k];
      if (etiket) { etiket.innerHTML = g ? opt.yazi(g) : ''; etiket.style.display = g ? 'block' : 'none'; }
      document.querySelectorAll('[data-k]').forEach(e => e.classList.toggle('on', e.dataset.k === k));
      mv.style.cursor = olcModu ? 'crosshair' : ((g && opt.hedef(g)) ? 'pointer' : 'grab');
    }

    function noktada(ev) {
      const m = MN(ev.clientX, ev.clientY);                         // PENCERE koordinatı (1. tuzak)
      if (!m) return null;
      const b = BIRIM[anahtar(m.name)];
      if (!b) return null;
      // Kutular seçimi çalmasın — YALNIZ birim seçilen sayfalarda (istasyon). Makine sayfasında modül seçilir,
      // orada kutu modüllerin de seçilebilmesi gerekir.
      if (opt.grup === 'kod' && gercekVar && !gercek(b)) return null;
      return grupAnahtari(b);
    }

    // ------------------------------------------------------------------ SÜRÜKLEME KORUMASI (3. tuzak)
    let bas = null, surukledi = false;
    mv.addEventListener('pointerdown', e => { bas = [e.clientX, e.clientY]; surukledi = false; });
    window.addEventListener('pointerup', () => { bas = null; });
    mv.addEventListener('pointermove', e => {
      if (bas && Math.hypot(e.clientX - bas[0], e.clientY - bas[1]) > 6) surukledi = true;
      if (kilit || !mv.model) return;
      if (!Object.keys(ASIL).length) kur();      // yoklama kaçırdıysa ilk harekette kur (sekme arka plandayken model-viewer bekliyor)
      if (!olcModu) vurgula(noktada(e));
    });
    mv.addEventListener('pointerleave', () => { if (!kilit && !olcModu) vurgula(null); });

    mv.addEventListener('click', e => {
      if (surukledi || !mv.model) return;
      if (olcModu) { olcNokta(e); return; }
      vurgula(noktada(e));                       // tek tık yalnız SEÇER
    });
    mv.addEventListener('dblclick', e => {       // açmak için ÇİFT TIK
      if (surukledi || !mv.model || olcModu) return;
      const k = noktada(e); if (!k) return;
      const h = opt.hedef(GRUP[k]); if (h) location.href = h;
    });

    mv.addEventListener('load', kur);
    const yokla = setInterval(() => {
      if (mv.model && mv.model.materials.length && !Object.keys(ASIL).length) kur();
      if (Object.keys(ASIL).length) clearInterval(yokla);
    }, 250);

    // ================================================================== ARAÇLAR (kesit + ölçü)
    let cubuk = null, R = null, eksen = '', yon = 1, kaydirici = null, degerYazi = null;
    const duzlem = { normal: { x: 0, y: 0, z: 0 }, constant: 0 };
    let olcModu = false, nokta = [], svg = null, sonucYazi = null, olcDugme = null;

    function el(etiketAdi, sinif, icerik) {
      const e = document.createElement(etiketAdi);
      if (sinif) e.className = sinif;
      if (icerik != null) e.innerHTML = icerik;
      return e;
    }

    function araclariKur() {
      if (cubuk) return;
      const sc = SAHNE(mv);
      cubuk = el('div', 'm3ar');

      const gK = el('div', 'grp');
      gK.appendChild(el('b', null, 'Kesit'));
      ['', 'x', 'y', 'z'].forEach(a => {
        const d = el('button', a === '' ? 'on' : null, a === '' ? 'yok' : EKSEN[a][0]);
        d.dataset.eks = a;
        d.title = a === '' ? 'kesiti kapat' : EKSEN[a][0] + ' — ' + EKSEN[a][1];
        d.onclick = () => { eksen = a; cubukTazele(); kesitKur(); };
        gK.appendChild(d);
      });
      const dYon = el('button', 'ic', '⇄');
      dYon.title = 'kesilen tarafı değiştir';
      dYon.onclick = () => { yon = -yon; kesitKur(); };
      gK.appendChild(dYon);
      kaydirici = el('input'); kaydirici.type = 'range'; kaydirici.min = 0; kaydirici.max = 1000; kaydirici.value = 500;
      kaydirici.oninput = kesitKur;
      gK.appendChild(kaydirici);
      degerYazi = el('span', 'deg', '—');
      gK.appendChild(degerYazi);
      cubuk.appendChild(gK);

      const gO = el('div', 'grp');
      olcDugme = el('button', null, 'Ölçü al');
      olcDugme.title = 'iki noktaya tıkla — arası ölçülür';
      olcDugme.onclick = () => {
        olcModu = !olcModu; nokta = []; olcCiz();
        olcDugme.classList.toggle('on', olcModu);
        olcDugme.textContent = olcModu ? 'Ölçüyü bitir' : 'Ölçü al';
        sonucYazi.textContent = olcModu ? 'birinci noktaya tıkla' : '';
        if (olcModu) { vurgula(null); }
        mv.style.cursor = olcModu ? 'crosshair' : 'grab';
      };
      gO.appendChild(olcDugme);
      sonucYazi = el('span', 'snc', '');
      gO.appendChild(sonucYazi);
      cubuk.appendChild(gO);

      // v19 · ÖN KAPAKLAR KAYDIRICISI (Kemal): tam sağ = düz metal sac kapak (304 fırçalı, opak, cam tonu yok) · sola çektikçe saydamlaşır · tam sol = görünmez
      const kapMat = mv.model ? mv.model.materials.filter(m => /__on_seffaf$/.test(m.name)) : [];
      if (kapMat.length) {
        const gC = el('div', 'grp');
        gC.appendChild(el('b', null, 'Ön kapaklar'));
        const kb = el('input'); kb.type = 'range'; kb.min = 0; kb.max = 100; kb.step = 1;
        kb.title = 'sağ: metal kapak · sol: görünmez (içerisi)';
        const ky = el('span', 'deg', '');
        const kapak = v => {
          v = +v; const a = v / 100;
          kapMat.forEach(m => {
            m.pbrMetallicRoughness.setBaseColorFactor([0.80, 0.82, 0.85, a]);       // SAC tonu (montaj MALZEME 'sac'): metal, cam tonu yok
            m.pbrMetallicRoughness.setMetallicFactor(0.85);
            m.pbrMetallicRoughness.setRoughnessFactor(0.32);
            m.setAlphaMode(v >= 100 ? 'OPAQUE' : 'BLEND');
          });
          ky.textContent = v >= 100 ? 'metal' : (v <= 0 ? 'gizli' : '%' + v);
          kesitUygula();                                                    // v20: kapak saydamlaşınca kesit yüzü boyası kalkar / opaklaşınca gelir
          try { localStorage.setItem('ak_kapak_saydam', String(v)); } catch (e) {}
        };
        kb.oninput = () => kapak(kb.value);
        gC.appendChild(kb); gC.appendChild(ky);
        cubuk.appendChild(gC);
        let _v = 100;
        try { const _s = localStorage.getItem('ak_kapak_saydam'); if (_s !== null) _v = +_s; } catch (e) {}
        kb.value = _v; kapak(_v);
      }

      const ip = kap.querySelector('.ip');                    // "sürükle: döndür ..." yazısı çubuğun içine girer;
      if (ip) cubuk.appendChild(ip);                          // mutlak konumdayken mobilde düğmelerin üstüne biniyordu
      kap.appendChild(cubuk);

      svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('class', 'm3olc');
      kap.appendChild(svg);
      mv.addEventListener('camera-change', () => { kesitTazele(); cizgiTazele(); });
      window.addEventListener('resize', olcCiz);

      if (!sc) { gK.classList.add('yok'); gK.title = 'kesit bu tarayıcıda açılamadı'; }
      cubukTazele();
    }

    function cubukTazele() {
      if (!cubuk) return;
      cubuk.querySelectorAll('[data-eks]').forEach(d => d.classList.toggle('on', d.dataset.eks === eksen));
      kaydirici.disabled = !eksen;
      if (!eksen) degerYazi.textContent = '—';
    }

    // KESİTİN KOORDİNATI — ölçülerek bulunan tuzak (Kemal: "sadece Z düzgün çalışıyor"):
    // scene.boundingBox modelin KENDİ (GLB) koordinatını verir, ama kesme düzlemi DÜNYA koordinatında
    // uygulanır. model-viewer modeli sahneye yerleştirirken kaydırıyor: bu modülde x −1,60 · y −1,52 · z +0,25 m.
    // Z'de kayma küçük olduğu için kesit az çok tutuyordu, X ve Y'de düzlem modelin tamamen dışında kalıyordu.
    // Çözüm: sınırları parçaların matrixWorld'ünden hesapla. model-viewer'ın kendi gölge düzlemi ADSIZ mesh,
    // onu dışarıda bırakmak gerekiyor — yoksa kutu şişiyor.
    // Model DÜNYADA sabit değil: model-viewer modeli bir "target" grubunun içine koyup kaydırıyor
    // (bu modülde −1,60 / −1,52 / +0,25 m) ve SAĞ TIK PAN bu ofseti değiştiriyor. Kesme düzlemi dünya
    // koordinatında olduğu için pan yapınca kesit yüzeyi modelin içinde ileri geri kayıyordu
    // (Kemal: "sağ clickle hareket ederken kesitin yüzeyi ileri geri gidiyor").
    // Çözüm: sınır kutusu HER SEFERİNDE model bbox + güncel target ofseti olarak hesaplanıyor ve
    // camera-change'te düzlem tazeleniyor → kesit modele yapışık kalıyor, yalnız alt çubuktan değişiyor.
    function dunyaKutu() {
      const sc = SAHNE(mv);
      if (!sc || !sc.boundingBox) return null;
      const b = sc.boundingBox;
      if (!isFinite(b.min.x)) return null;
      const t = (sc.target && sc.target.position) || { x: 0, y: 0, z: 0 };
      return { min: { x: b.min.x + t.x, y: b.min.y + t.y, z: b.min.z + t.z },
               max: { x: b.max.x + t.x, y: b.max.y + t.y, z: b.max.z + t.z } };
    }

    // camera-change'te YALNIZ düzlemin sayısı güncellenir; malzemelere dokunulmaz
    // (needsUpdate her karede shader'ı yeniden derletirdi).
    function kesitTazele() {
      if (!eksen) return;
      const bb = dunyaKutu();
      if (!bb) return;
      const a0 = bb.min[eksen], a1 = bb.max[eksen];
      duzlem.normal[eksen] = -yon;
      duzlem.constant = yon * (a0 + (a1 - a0) * (kaydirici.value / 1000));
    }

    // Renderer'ı sahnedeki ilk mesh'in onBeforeRender kancasıyla yakalıyoruz. Kanca ancak bir KARE
    // çizilince çalışır; sekme arka plandayken kare çizilmiyor, o yüzden "bekle ve vazgeç" yanlıştı
    // (kesit "açılamadı" deyip kapanıyordu). Artık kanca R'yi yakaladığı anda bekleyen kesiti kendisi uyguluyor.
    let kancaKurulu = false, uyariZaman = null;
    function rendererKanca() {
      if (R || kancaKurulu) return;
      const sc = SAHNE(mv);
      if (!sc) return;
      let n = 0;
      sc.traverse(o => {
        if (!o.isMesh) return;
        n++;
        o.onBeforeRender = function (r) { delete o.onBeforeRender; if (!R) { R = r; kesitUygula(); } };
      });
      if (n) kancaKurulu = true;
      if (sc.queueRender) sc.queueRender();
      clearTimeout(uyariZaman);
      uyariZaman = setTimeout(() => { if (!R && eksen) degerYazi.textContent = 'kesit açılamadı'; }, 8000);
    }

    // KESİT YÜZÜ DOLU (v20 · Kemal: "parçalar solid mi, içi boş sac mı?"): tarayıcı yalnız parçaların DIŞ YÜZEYİNİ çizer; kesit düzlemi parçayı
    // kesince içi boş görünüyordu. Kesit açıkken opak malzemeler iki yüzlü çizilir ve ARKA yüzler (kesilen katının içi) düz koyu tonda boyanır →
    // kesilen her katı dolu görünür. Şeffaf malzemelere (ön kapak saydamken, PC kaset) dokunulmaz. Kesit kapanınca eski hale döner.
    const KAPAK = '__kesitKapak';
    function kapakAyarla(m, acik) {
      // v21: foam gets an actual planar section, not a dark back-face illusion.
      if (/^(MC_TOPPING_MODUL__yalitim_gorunur|MB_B_KASA__pu)$/.test(m.name)) return;
      const saydam = m.transparent && m.opacity < 0.999;              // ön kapak saydamken / PC kaset: kesit yüzü boyanmaz
      if (acik && !saydam) {
        if (m.userData[KAPAK]) return;
        m.userData[KAPAK] = { side: m.side, obc: m.onBeforeCompile };
        m.side = 2;                                                     // THREE.DoubleSide
        m.onBeforeCompile = function (sh, r) {
          if (m.userData[KAPAK] && m.userData[KAPAK].obc) m.userData[KAPAK].obc.call(this, sh, r);
          sh.fragmentShader = sh.fragmentShader.replace('#include <dithering_fragment>',
            '#include <dithering_fragment>\n  if (!gl_FrontFacing) { gl_FragColor = vec4(diffuseColor.rgb * 0.45, 1.0); }  // kesitKapak');
        };
        m.needsUpdate = true;
      } else if (m.userData[KAPAK]) {
        const u = m.userData[KAPAK];
        m.side = u.side; m.onBeforeCompile = u.obc; delete m.userData[KAPAK]; m.needsUpdate = true;
      }
    }

    function kesitUygula() {
      const sc = SAHNE(mv);
      if (!sc || !R) return;
      R.localClippingEnabled = !!eksen;
      const P = eksen ? [duzlem] : null;
      sc.traverse(o => {
        if (!o.isMesh || !o.material || o.userData.yalitimKesit) return;
        (Array.isArray(o.material) ? o.material : [o.material]).forEach(m => {
          if (m.clippingPlanes !== P) { m.clippingPlanes = P; m.needsUpdate = true; }
          kapakAyarla(m, !!eksen);
        });
      });
      if (sc.queueRender) sc.queueRender();
    }

    function kesitKur() {
      const bb = dunyaKutu();
      if (!bb) return;
      if (eksen) {
        const a0 = bb.min[eksen], a1 = bb.max[eksen];
        const v = a0 + (a1 - a0) * (kaydirici.value / 1000);
        duzlem.normal = { x: 0, y: 0, z: 0 };
        duzlem.normal[eksen] = -yon;                       // yon=+1 → düzlemin ALTINDA kalan görünür
        duzlem.constant = yon * v;
        degerYazi.textContent = Math.round((v - a0) * 1000) + ' / ' + Math.round((a1 - a0) * 1000) + ' mm';
      }
      cubukTazele();
      rendererKanca();
      kesitUygula();
    }

    function eksenSec(a) { eksen = a; cubukTazele(); kesitKur(); }

    // ------------------------------------------------------------------ ÖLÇÜ
    function olcNokta(ev) {
      const p = PN(ev.clientX, ev.clientY);   // PENCERE koordinatı (1. tuzak)
      if (!p) { sonucYazi.textContent = 'boşluğa tıkladın — parçanın üstüne tıkla'; return; }
      if (nokta.length >= 2) nokta = [];
      nokta.push([p.position.x, p.position.y, p.position.z]);
      olcCiz();
    }

    // Nokta yerlerini model-viewer'in KENDI hotspot'u tasiyor (data-position). Kendi projeksiyonumuz
    // denendi (Vector3.project + scene.camera) ama model-viewer modeli kendi hedefine gore olcekleyip
    // tasidigi icin ekran yeri tutmadi. Hotspot'lar render sirasinda yerlesiyor, o yuzden aralarindaki
    // cizgi 'camera-change'te ve ilk birkac karede yeniden ciziliyor.
    function olcNoktalari() {
      Array.prototype.slice.call(mv.querySelectorAll('.m3hs')).forEach(e => e.remove());
      nokta.forEach((n, i) => {
        const b = document.createElement('button');
        b.className = 'm3hs'; b.slot = 'hotspot-olc' + i;
        b.setAttribute('data-position', n[0] + 'm ' + n[1] + 'm ' + n[2] + 'm');
        b.setAttribute('data-normal', '0m 1m 0m');
        b.textContent = String(i + 1);
        mv.appendChild(b);
      });
    }

    function cizgiTazele() {
      if (!svg) return;
      const r = kap.getBoundingClientRect();
      svg.setAttribute('viewBox', '0 0 ' + Math.round(r.width) + ' ' + Math.round(r.height));
      const h = mv.querySelectorAll('.m3hs');
      if (h.length < 2 || nokta.length < 2) { svg.innerHTML = ''; return; }
      const a = h[0].getBoundingClientRect(), b = h[1].getBoundingClientRect();
      if (!a.width || !b.width) { svg.innerHTML = ''; return; }
      const ax = a.left + a.width / 2 - r.left, ay = a.top + a.height / 2 - r.top;
      const bx = b.left + b.width / 2 - r.left, by = b.top + b.height / 2 - r.top;
      const d = Math.hypot(nokta[1][0] - nokta[0][0], nokta[1][1] - nokta[0][1], nokta[1][2] - nokta[0][2]) * 1000;
      svg.innerHTML = '<line x1="' + ax.toFixed(1) + '" y1="' + ay.toFixed(1) + '" x2="' + bx.toFixed(1) + '" y2="' + by.toFixed(1) + '"/>' +
                      '<text class="ol" x="' + ((ax + bx) / 2).toFixed(1) + '" y="' + ((ay + by) / 2 - 11).toFixed(1) + '">' + d.toFixed(1) + ' mm</text>';
    }

    function olcCiz() {
      if (!svg) return;
      olcNoktalari();
      if (nokta.length === 2) {
        const d = Math.hypot(nokta[1][0] - nokta[0][0], nokta[1][1] - nokta[0][1], nokta[1][2] - nokta[0][2]) * 1000;
        const dx = Math.abs(nokta[1][0] - nokta[0][0]) * 1000, dy = Math.abs(nokta[1][1] - nokta[0][1]) * 1000, dz = Math.abs(nokta[1][2] - nokta[0][2]) * 1000;
        sonucYazi.innerHTML = '<b>' + d.toFixed(1) + ' mm</b> · X ' + dx.toFixed(0) + ' · Y ' + dy.toFixed(0) + ' · Z ' + dz.toFixed(0);
      } else if (nokta.length === 1) {
        sonucYazi.textContent = 'ikinci noktaya tıkla';
      } else if (olcModu) {
        sonucYazi.textContent = 'birinci noktaya tıkla';
      }
      let k = 0;
      (function bekle() { cizgiTazele(); if (++k < 12) requestAnimationFrame(bekle); })();   // hotspot'lar yerleşene kadar
    }

    // ================================================================== v17 · FARE ETİKETİ: fare ~0,45 sn durunca yanında PARÇA ADI
    // GLB parçaları birim + malzemeye göre birleşik → parça adı parca_kutulari.json'daki sınır kutularından bulunur (hat_montaj_v62).
    // Şeffaf ön kapağa değerse ışın boyunca arkasındaki ilk parçaya geçilir (büyük kabuk kutuları atlanır).
    let PK = null, PB = {}, M2K = {}, tip = null, tipZam = null;
    if (opt.parca) fetch(opt.parca).then(r => r.json()).then(D => {
      PK = D.parca; PB = D.birim; Object.keys(PB).forEach(k => { M2K[PB[k].mal] = k; });
    }).catch(() => {});
    const icinde = (k, p, pay) => p[0] >= k[2] - pay && p[0] <= k[3] + pay && p[1] >= k[4] - pay && p[1] <= k[5] + pay && p[2] >= k[6] - pay && p[2] <= k[7] + pay;
    const hacim = k => (k[3] - k[2]) * (k[5] - k[4]) * (k[7] - k[6]);
    function enKucuk(liste, p, pay, secici) {
      let en = null;
      liste.forEach(([kod, k]) => { if (secici(k) && icinde(k, p, pay) && (!en || hacim(k) < hacim(en[1]))) en = [kod, k]; });
      return en;
    }
    function parcaBul(ev) {
      if (!PK) return null;
      const m = MN(ev.clientX, ev.clientY), h = PN(ev.clientX, ev.clientY);
      if (!m || !h) return null;
      const P = [h.position.x * 1000, h.position.y * 1000, h.position.z * 1000];
      if (m.name.indexOf('insan') === 0) return ['INSAN_180cm', PK.INSAN_180cm[0]];
      const kod = M2K[m.name.split('__')[0]];
      const hepsi = []; Object.keys(PK).forEach(kd => PK[kd].forEach(k => hepsi.push([kd, k])));
      if (!m.name.endsWith('__on_seffaf')) {
        const kendi = kod && PK[kod] ? PK[kod].map(k => [kod, k]) : hepsi;
        return enKucuk(kendi, P, 3, () => true) || enKucuk(hepsi, P, 3, () => true);
      }
      // şeffaf kapak: kameradan geçen ışın boyunca ilerle, ilk dolu (şeffaf olmayan, dev kabuk olmayan) parçayı bul
      const o = mv.getCameraOrbit(), t = mv.getCameraTarget();
      const C = [t.x + o.radius * Math.sin(o.phi) * Math.sin(o.theta), t.y + o.radius * Math.cos(o.phi), t.z + o.radius * Math.sin(o.phi) * Math.cos(o.theta)].map(v => v * 1000);
      let d = [P[0] - C[0], P[1] - C[1], P[2] - C[2]]; const n = Math.hypot(...d); d = d.map(v => v / n);
      for (let s = 2; s < 2000; s += 5) {
        const Q = [P[0] + d[0] * s, P[1] + d[1] * s, P[2] + d[2] * s];
        const bul = enKucuk(hepsi, Q, 0, k => !k[1] && hacim(k) < 3e7);   // 0,03 m³ üstü kabuk / PU atlanır (çekmece kutusu 1,7e7)
        if (bul) return bul;
      }
      return enKucuk(hepsi, P, 3, () => true);
    }
    function tipGizle() { clearTimeout(tipZam); if (tip) tip.style.display = 'none'; }
    mv.addEventListener('pointermove', e => {
      tipGizle();
      if (!opt.parca || bas || olcModu) return;
      const cx = e.clientX, cy = e.clientY;
      tipZam = setTimeout(() => {
        const b = parcaBul({ clientX: cx, clientY: cy }); if (!b) return;
        if (!tip) { tip = document.createElement('div'); tip.className = 'pet'; document.body.appendChild(tip); }
        const [kod, k] = b, ba = PB[kod] ? PB[kod].ad : '';
        tip.innerHTML = '<b>' + k[0].replace(/_/g, ' ') + '</b>' + (ba ? '<span>' + (ba.length > 90 ? ba.slice(0, 90) + '…' : ba) + '</span>' : '');
        tip.style.left = Math.min(cx + 14, innerWidth - 300) + 'px'; tip.style.top = (cy + 16) + 'px'; tip.style.display = 'block';
      }, 450);
    });
    mv.addEventListener('pointerleave', tipGizle);
    mv.addEventListener('pointerdown', tipGizle);

    return {
      veri(birimler) { birimler.forEach(b => { BIRIM[b.mal] = b; }); kur(); },
      sec(k) { kilit = k; vurgula(k); },
      birak() { kilit = null; vurgula(null); },
      icini() {}                                                  // eski arayüz korunuyor (sayfa çağırıyorsa kırılmasın)
    };
  };
})();
