// AUTOKITCH · hat/model3d.js — gerçek üretim modelini gösterir, üstüne gelince parça PARLAR, tıklayınca sayfası açılır.
// model-viewer'ın materialFromPoint'i malzeme adını verir; her birim kendi malzemesini taşır (hat_montaj_v2.py),
// eşleşme durum.json'daki "mal" alanından kurulur. Ayrı bir tıklama katmanı yok — model neyse o.
(function () {
  const VURGU = [1.0, 0.72, 0.16, 1.0];           // parlayan birim
  const SOLUK = 0.16;                              // seçim varken ötekiler

  window.model3d = function (opt) {
    const mv = document.getElementById(opt.mv), etiket = document.getElementById(opt.etiket);
    let BIRIM = {}, ASIL = {}, GRUP = {}, secili = null, kilit = null;

    function grupAnahtari(b) { return opt.grup === 'modul' ? b.modul : b.kod; }

    function kur() {
      if (!mv.model) return;
      GRUP = {};                                   // kur() iki kez calisabilir (load + yoklama) -> sayaclar ikilenmesin
      mv.model.materials.forEach(m => {
        const f = m.pbrMetallicRoughness.baseColorFactor;
        ASIL[m.name] = [f[0], f[1], f[2], f[3]];
        const b = BIRIM[m.name]; if (!b) return;
        (GRUP[grupAnahtari(b)] = GRUP[grupAnahtari(b)] || { birimler: [], mat: [] }).mat.push(m);
        GRUP[grupAnahtari(b)].birimler.push(b);
      });
      if (opt.hazir) opt.hazir(GRUP);
    }

    function boya(m, renk, alfa) {
      const c = renk ? renk.slice() : ASIL[m.name].slice();
      if (alfa != null) c[3] = alfa;
      m.pbrMetallicRoughness.setBaseColorFactor(c);
      m.setAlphaMode(c[3] >= 0.999 ? 'OPAQUE' : 'BLEND');
    }

    function vurgula(k) {
      if (secili === k) return;
      secili = k;
      mv.model.materials.forEach(m => {
        if (!ASIL[m.name]) return;
        const b = BIRIM[m.name];
        if (!k) { boya(m, null); return; }
        if (b && grupAnahtari(b) === k) boya(m, VURGU);
        else boya(m, null, Math.min(ASIL[m.name][3], SOLUK));
      });
      const g = k && GRUP[k];
      if (etiket) {
        etiket.innerHTML = g ? opt.yazi(g) : '';
        etiket.style.display = g ? 'block' : 'none';
      }
      document.querySelectorAll('[data-k]').forEach(e => e.classList.toggle('on', e.dataset.k === k));
      mv.style.cursor = (g && opt.hedef(g)) ? 'pointer' : 'grab';
    }

    function noktada(ev) {
      const r = mv.getBoundingClientRect();
      const m = mv.materialFromPoint(ev.clientX - r.left, ev.clientY - r.top);
      const b = m && BIRIM[m.name];
      return b ? grupAnahtari(b) : null;
    }

    mv.addEventListener('load', kur);
    // 'load' olayi src degisince guvenilir tetiklenmiyor (kaset sayfasinda da ayni sorun vardi) -> yoklayarak kur
    const yokla = setInterval(() => { if (mv.model && mv.model.materials.length && !Object.keys(ASIL).length) { kur(); } if (Object.keys(ASIL).length) clearInterval(yokla); }, 250);
    mv.addEventListener('pointermove', e => { if (!kilit && mv.model) vurgula(noktada(e)); });
    mv.addEventListener('pointerleave', () => { if (!kilit) vurgula(null); });
    mv.addEventListener('click', e => {
      if (!mv.model) return;
      const k = noktada(e); if (!k) return;
      const h = opt.hedef(GRUP[k]); if (h) location.href = h;
    });

    return {
      veri(birimler) { birimler.forEach(b => { BIRIM[b.mal] = b; }); kur(); },
      sec(k) { kilit = k; vurgula(k); },
      birak() { kilit = null; vurgula(null); }
    };
  };
})();
