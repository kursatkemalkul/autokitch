// AUTOKITCH · hat/model3d.js — gerçek üretim modelini gösterir, üstüne gelince parça PARLAR, tıklayınca sayfası açılır.
// model-viewer'ın materialFromPoint'i malzeme adını verir; her birim kendi malzemesini taşır (hat_montaj_v4.py),
// eşleşme durum.json'daki "mal" alanından kurulur. Ayrı bir tıklama katmanı yok — model neyse o.
//
// İKİ TUZAK (ikisi de ölçülerek bulundu):
//  1 materialFromPoint PENCERE koordinatı ister (içeride kendi getBoundingClientRect'ini çıkarır).
//    Eleman koordinatı verilince seçim rect.top kadar kayıyor — "tam üstündeyim ama seçmiyor".
//  2 model-viewer'ın 'load' olayı ve mv.model geç geliyor (~13 sn) → yoklayarak kurulur.
(function () {
  const VURGU = [1.0, 0.72, 0.16, 1.0];           // parlayan birim
  const SOLUK = 0.14;                              // seçim varken ötekiler
  const ZARF = 0.055;                              // henüz modellenmemiş kutular: bağlam olarak dursun, önde durmasın

  window.model3d = function (opt) {
    const mv = document.getElementById(opt.mv), etiket = document.getElementById(opt.etiket);
    let BIRIM = {}, ASIL = {}, GRUP = {}, secili = null, kilit = null, gercekVar = false, ici = false;

    const anahtar = ad => ad.split('__')[0];                        // M<modül>_<kod>__<ton> → birim anahtarı
    const gercek = b => b && b.durum && b.durum.indexOf('GERCEK') === 0;
    function grupAnahtari(b) { return opt.grup === 'modul' ? b.modul : b.kod; }

    function boya(m, renk, alfa) {
      const c = renk ? renk.slice() : ASIL[m.name].slice();
      if (alfa != null) c[3] = alfa;
      if (ici && !renk && m.name.indexOf('__cam') > 0) c[3] = 0.28;   // "içini gör": PC gövde saydamlaşır
      m.pbrMetallicRoughness.setBaseColorFactor(c);
      m.setAlphaMode(c[3] >= 0.999 ? 'OPAQUE' : 'BLEND');
    }

    function kur() {
      if (!mv.model) return;
      GRUP = {}; ASIL = {};
      gercekVar = Object.keys(BIRIM).some(k => gercek(BIRIM[k]));
      mv.model.materials.forEach(m => {
        const b = BIRIM[anahtar(m.name)];
        const f = m.pbrMetallicRoughness.baseColorFactor;
        let a = f[3];
        if (b && !gercek(b)) a = Math.min(a, ZARF);                 // kutu / katalog: soluk bağlam
        ASIL[m.name] = [f[0], f[1], f[2], a];
        boya(m, null);
        if (!b) return;
        const k = grupAnahtari(b);
        (GRUP[k] = GRUP[k] || { birimler: [], mat: [] }).mat.push(m);
        if (GRUP[k].birimler.indexOf(b) < 0) GRUP[k].birimler.push(b);
      });
      if (opt.hazir) opt.hazir(GRUP);
    }

    function vurgula(k) {
      if (secili === k) return;
      secili = k;
      mv.model.materials.forEach(m => {
        if (!ASIL[m.name]) return;
        const b = BIRIM[anahtar(m.name)];
        if (!k) { boya(m, null); return; }
        if (b && grupAnahtari(b) === k) boya(m, VURGU);
        else boya(m, null, Math.min(ASIL[m.name][3], SOLUK));
      });
      const g = k && GRUP[k];
      if (etiket) { etiket.innerHTML = g ? opt.yazi(g) : ''; etiket.style.display = g ? 'block' : 'none'; }
      document.querySelectorAll('[data-k]').forEach(e => e.classList.toggle('on', e.dataset.k === k));
      mv.style.cursor = (g && opt.hedef(g)) ? 'pointer' : 'grab';
    }

    function noktada(ev) {
      const m = mv.materialFromPoint(ev.clientX, ev.clientY);        // PENCERE koordinatı (1. tuzak)
      if (!m) return null;
      const b = BIRIM[anahtar(m.name)];
      if (!b) return null;
      // Kutular seçimi çalmasın — YALNIZ birim seçilen sayfalarda (istasyon). Makine sayfasında modül seçilir,
      // orada kutu modüllerin de seçilebilmesi gerekir.
      if (opt.grup === 'kod' && gercekVar && !gercek(b)) return null;
      return grupAnahtari(b);
    }

    mv.addEventListener('load', kur);
    const yokla = setInterval(() => { if (mv.model && mv.model.materials.length && !Object.keys(ASIL).length) kur(); if (Object.keys(ASIL).length) clearInterval(yokla); }, 250);
    mv.addEventListener('pointermove', e => {
      if (kilit || !mv.model) return;
      if (!Object.keys(ASIL).length) kur();        // yoklama kacirdiysa ilk harekette kur (sekme arka plandayken model-viewer bekliyor)
      vurgula(noktada(e));
    });
    mv.addEventListener('pointerleave', () => { if (!kilit) vurgula(null); });
    mv.addEventListener('click', e => {
      if (!mv.model) return;
      const k = noktada(e); if (!k) return;
      const h = opt.hedef(GRUP[k]); if (h) location.href = h;
    });

    return {
      veri(birimler) { birimler.forEach(b => { BIRIM[b.mal] = b; }); kur(); },
      sec(k) { kilit = k; vurgula(k); },
      birak() { kilit = null; vurgula(null); },
      icini(ac) { ici = ac; const s = secili; secili = null; vurgula(s); }
    };
  };
})();
