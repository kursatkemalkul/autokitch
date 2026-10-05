/* mekanizma-v3.js · v3 (3 Eki 2026: üç kademe dükkân › makine › istasyon + sol menüde göz) · v2 (3 Eki 2026: disiplin vurgusu + MEK3_JSON) · v1 (1 Eki 2026) — MEKANİZMA AĞACI · İSTASYON ALT MONTAJI (makine_v3.html)
   Kemal: "istasyon → mekanizma → alt kırılım: K → Sprey (motoru, kablosu, hava parçaları dahil) · Bıçak · E → Kutu katlama …
   istasyonlar ayrı alt montaj ama tıklayınca açılmıyor".
   · Panel: istasyon → mekanizma ağacı. Mekanizmaya basınca yalnız o görünür (diğerleri gizli ya da soluk), altında tür süzgeci
     (Motor + sürücü · Elektrik güç · Kontrol · Hava · Gıda · Mekanizma · Gövde) GLB'deki üçgen başına "kat" etiketinden.
   · İstasyon kartına ya da 3B'de istasyona tıklayınca o istasyonun alt montajı açılır (yalnız o istasyon + mekanizma ağacı).
     Açıkken 3B'de bir parçaya tıklamak o parçanın mekanizmasını seçer. Esc / "Tüm hat" geri döner.
   · Üçgen → mekanizma: GLB "mek" etiketi (montaj yap_mek_v1 ile) varsa o; yoksa ../hat3d/v3/mekanizma_v3.json "aralik" tablosu
     (mevcut GLB için parça kutularından çıkarıldı). GLB ve paylaşılan betikler (kategori.js, dis-kabuk.js, model3d) değişmez;
     geometri kategori.js gibi yalnız indis alt kümesiyle değiştirilir, kenar çizgileri seçime göre yeniden hesaplanır.
   · Motor: window.MEK3 (kapak-gorunum.js de bunu kullanır). */
(() => {
  'use strict';
  const mv = document.getElementById('mv');
  if (!mv) return;
  const JSON_YOL = window.MEK3_JSON || '../hat3d/v3/mekanizma_v3.json?v=1';
  // v2 (3 Eki 2026 · Kemal "tamam yap" — gruplama düzeni): window.MEK3_DISIPLIN = true olan sayfada DİSİPLİN düğmeleri modelin üstünde.
  //   Basılan disiplin(ler) tam renk, geri kalan her şey soluk (gizlenmez); çoklu seçim; ana görünümde ve istasyon görünümünde çalışır.
  //   Sol menü yalnız montaj ağacı (TÜR süzgeci gizlenir). Ayar yoksa (eski sayfalar) davranış v1 ile aynı.
  const DISIPLIN = !!window.MEK3_DISIPLIN;
  const DSP_RENK = {GOVDE: '#8f99a6', MEKANIZMA: '#c9a227', MOTOR: '#7b61d6', SENSOR: '#e0479e', HAVA: '#2f8fd8', SOGUTMA: '#1fa3a0',
                    ELEKTRIK: '#e07b20', GUC: '#e07b20', KONTROL: '#2f9e44', GIDA: '#d94a3a', ROBOT: '#f08c00', URUN: '#a47551', DUKKAN: '#6c757d'};
  const vurgu = new Set();            // seçili disiplin (kat indisi) — boşsa vurgu yok
  // v4 (3 Eki 2026 · Kemal): "soluk | yalnız" anahtarı. YALNIZ (varsayılan): seçilmeyen her şey tamamen gizli → ör. Elektrik'e basınca
  //   bütün makinenin kablo tesisatı tek başına görünür. Tür seçiliyken sol menüdeki göz gizlemeleri yok sayılır (kademe kapsamı kalır);
  //   seçim kalkınca göz ayarları geri gelir. SOLUK: v2 davranışı (seçilmeyen yarı saydam).
  let yalniz = true;
  try { if (localStorage.getItem('mek3_tur_mod') === 'soluk') yalniz = false; } catch (e) {}
  const gozEtkin = () => !vurgu.size;  // tür seçiliyken göz yok sayılır
  const ESIK = Math.cos(30 * Math.PI / 180), Q = 1e4;
  const KAT_RENK = ['#8f99a6', '#c9a227', '#7b61d6', '#d94a3a', '#2f8fd8', '#1fa3a0', '#e07b20', '#2f9e44', '#f08c00', '#a47551', '#6c757d'];
  const KAT_SUZGEC = ['MOTOR', 'GUC', 'KONTROL', 'HAVA', 'GIDA', 'SOGUTMA', 'MEKANIZMA', 'GOVDE', 'ROBOT', 'URUN', 'DUKKAN'];
  const sahne = () => mv[Object.getOwnPropertySymbols(mv).find(s => s.description === 'scene')];

  let D = null, LISTE = [], KATL = [], kayit = [], hazir = false, kuruluyor = null, is = 0;
  let mod = null;                     // null | {tip:'mek', mek:Set, kat:Set, ist:[…]} | {tip:'kapak'}
  let hayalet = 'gizle', hayaletMalz = null, kamera0 = null;
  // v3 (3 Eki 2026 · Kemal): ÜÇ KADEME (JSON'da 'kademe' + MEK3_DISIPLIN olan sayfada) — Dükkân (her şey) › Makine (istasyonlar + makine içi
  //   elektrik, zemin kalır) › İstasyon (üniteler). 3B'de çift tık bir alt kademeye, '←' / Esc / üst satırdaki yol bir üste. Sol menüde GÖZ:
  //   satıra tek bas = gizle / göster (çoklu, bağımsız), çift bas = yalnız o; '›' = aç. Ayar yoksa (eski sayfalar) davranış v2 ile aynı.
  let gizli = new Set();              // gözle gizlenen ünite indisleri
  const KAD = () => !!(DISIPLIN && D && D.kademe);
  const kademe = () => !mod ? 'dukkan' : mod.tip === 'kapak' ? 'kapak' : mod.kademe === 'makine' ? 'makine' : 'istasyon';
  const MAK_IST = () => (D && D.kademe && D.kademe.makine && D.kademe.makine.ist) || [];
  function makineMek(ekli = true) {
    const ist = MAK_IST(), ek = ekli ? (D.kademe.makine.ek || []) : [];
    return LISTE.map((m, i) => [m, i]).filter(([m]) => ist.indexOf(m.istasyon) >= 0 || ek.indexOf(m.kod) >= 0).map(([, i]) => i);
  }
  const dinleyici = [];
  const bildir = () => dinleyici.forEach(f => { try { f(mod); } catch (e) { console.error(e); } });

  // ------------------------------------------------------------------ kenar çizgileri (kenar-cizgi.js / kategori.js ile AYNI kural)
  function kenarlar(P, ind) {
    const anahtar = new Array(P.count), harita = new Map(), out = [];
    const k = i => anahtar[i] !== undefined ? anahtar[i] : (anahtar[i] = Math.round(P.getX(i) * Q) + ',' + Math.round(P.getY(i) * Q) + ',' + Math.round(P.getZ(i) * Q));
    for (let f = 0; f + 2 < ind.length; f += 3) {
      const a = ind[f], b = ind[f + 1], c = ind[f + 2];
      const ax = P.getX(a), ay = P.getY(a), az = P.getZ(a), ux = P.getX(b) - ax, uy = P.getY(b) - ay, uz = P.getZ(b) - az,
            wx = P.getX(c) - ax, wy = P.getY(c) - ay, wz = P.getZ(c) - az;
      let nx = uy * wz - uz * wy, ny = uz * wx - ux * wz, nz = ux * wy - uy * wx; const L = Math.hypot(nx, ny, nz);
      if (L < 1e-14) continue; nx /= L; ny /= L; nz /= L;
      const kk = [k(a), k(b), k(c)], iv = [a, b, c];
      for (let e = 0; e < 3; e++) {
        const i0 = iv[e], i1 = iv[(e + 1) % 3], k0 = kk[e], k1 = kk[(e + 1) % 3];
        if (k0 === k1) continue;
        const h = k0 < k1 ? k0 + '|' + k1 : k1 + '|' + k0, s = harita.get(h);
        if (s === undefined) harita.set(h, [i0, i1, nx, ny, nz]);
        else if (s !== null) {
          if (s[2] * nx + s[3] * ny + s[4] * nz < ESIK) out.push(P.getX(s[0]), P.getY(s[0]), P.getZ(s[0]), P.getX(s[1]), P.getY(s[1]), P.getZ(s[1]));
          harita.set(h, null);
        }
      }
    }
    for (const s of harita.values()) if (s) out.push(P.getX(s[0]), P.getY(s[0]), P.getZ(s[0]), P.getX(s[1]), P.getY(s[1]), P.getZ(s[1]));
    return out;
  }
  function kenarGeo(r, ind) {
    const P = r.g0.attributes.position, d = kenarlar(P, ind), g = new r.g0.constructor(), A = P.constructor;
    g.setAttribute('position', new A(new Float32Array(d), 3));
    const nrm = new Float32Array(d.length); for (let j = 1; j < nrm.length; j += 3) nrm[j] = 1;
    g.setAttribute('normal', new A(nrm, 3)); g.computeBoundingSphere();
    return g;
  }
  const cizgi = r => r.m.children.find(c => c.userData && c.userData.kenarCizgi) || null;

  // ------------------------------------------------------------------ kayıtlar (her ağ: üçgen başına mekanizma · kategori · kapak)
  function dugumAnahtari(o) {
    const ad = x => x && x.userData && typeof x.userData.name === 'string' ? x.userData.name : null;
    if (ad(o)) return ad(o) + '#0';
    const p = o.parent;
    if (ad(p) && !p.isMesh) {
      const prim = p.children.filter(c => c.isMesh && !ad(c) && !(c.userData.kenarCizgi || c.userData.yalitimKesit || c.userData.mekHayalet));
      return ad(p) + '#' + Math.max(0, prim.indexOf(o));
    }
    return (o.name || '') + '#0';
  }
  function birimOf(m) {
    const mm = Array.isArray(m.material) ? m.material[0] : m.material, ad = (mm && mm.name) || '';
    const r = /^M[A-Z]_(.+?)__/.exec(ad); return [r ? r[1] : '', ad];
  }
  function mekIndisi(kod) {
    let i = LISTE.findIndex(x => x.kod === kod);
    if (i < 0) { const p = kod.split('/'); LISTE.push({kod, istasyon: p[0], ad: p.slice(1).join('/') || p[0]}); i = LISTE.length - 1; }
    return i;
  }
  function kur() {
    if (hazir || !D || !mv.loaded) return false;
    const sc = sahne(); if (!sc) return false;
    let glbListe = null;
    sc.traverse(o => { if (!glbListe && o.userData && Array.isArray(o.userData.mekanizmalar)) glbListe = o.userData.mekanizmalar; });
    const glbMap = glbListe ? glbListe.map(x => mekIndisi(x.kod)) : null;
    let katListe = null;
    sc.traverse(o => { if (!katListe && o.userData && Array.isArray(o.userData.kategoriler)) katListe = o.userData.kategoriler; });
    KATL = katListe || KAT_SUZGEC.map(k => ({kod: k, ad: k}));
    const bul = []; let glbEtiket = 0, tablo = 0, varsay = 0;
    sc.traverse(o => {
      if (!o.isMesh || !o.geometry || !o.geometry.index || (o.userData && (o.userData.kenarCizgi || o.userData.yalitimKesit || o.userData.mekHayalet))) return;
      const g0 = o.geometry, n = g0.index.count / 3 | 0, gu = g0.userData || {};
      const mek = new Uint16Array(n), kat = new Uint8Array(n).fill(255), kpk = new Uint8Array(n);
      const [birim, malAd] = birimOf(o), key = dugumAnahtari(o);
      if (!birim && !D.aralik[key] && !Array.isArray(gu.mek)) return;    // GLB etiketli her ağ modelin parçasıdır (robot / insan kutuları dahil)                                   // model-viewer'ın kendi ağları (gölge vb.) — modelin parçası değil
      if (Array.isArray(gu.mek) && glbMap) {                                  // GLB etiketi (montaj yap_mek_v1 sonrası)
        for (let i = 0; i + 2 < gu.mek.length; i += 3) mek.fill(glbMap[gu.mek[i]], gu.mek[i + 1] / 3, (gu.mek[i + 1] + gu.mek[i + 2]) / 3);
        if (Array.isArray(gu.kpk)) for (let i = 0; i + 1 < gu.kpk.length; i += 2) kpk.fill(1, gu.kpk[i] / 3, (gu.kpk[i] + gu.kpk[i + 1]) / 3);
        glbEtiket++;
      } else if (D.aralik[key]) {                                             // sayfa tablosu (mevcut GLB)
        const a = D.aralik[key];
        for (let i = 0; i + 2 < a.length; i += 3) mek.fill(a[i], a[i + 1] / 3, (a[i + 1] + a[i + 2]) / 3);
        const k = D.kapak[key]; if (k) for (let i = 0; i + 1 < k.length; i += 2) kpk.fill(1, k[i] / 3, (k[i] + k[i + 1]) / 3);
        tablo++;
      } else {                                                                // birim varsayılanı
        mek.fill(mekIndisi(D.birim[birim] || 'Çevre/Diğer'));
        if (/__on_seffaf$/.test(malAd)) kpk.fill(1);
        varsay++;
      }
      if (Array.isArray(gu.kat)) for (let i = 0; i + 2 < gu.kat.length; i += 3) kat.fill(gu.kat[i], gu.kat[i + 1] / 3, (gu.kat[i + 1] + gu.kat[i + 2]) / 3);
      const varMek = new Set(mek);
      bul.push({m: o, g0, n, mek, kat, kpk, varMek, onbellek: new Map(), cz0: undefined, gizli: false, hay: null});
    });
    if (!bul.length) return false;
    kayit = bul; hazir = true;
    console.info('mekanizma-v3: %d ağ · GLB etiketi %d · tablo %d · birim varsayılanı %d', bul.length, glbEtiket, tablo, varsay);
    return true;
  }
  function bekle() {
    if (hazir) return Promise.resolve(true);
    if (kuruluyor) return kuruluyor;
    kuruluyor = new Promise(res => {
      const t = setInterval(() => { if (kur()) { clearInterval(t); res(true); } }, 300);
    });
    return kuruluyor;
  }

  // ------------------------------------------------------------------ uygula
  function altKume(r, sec) {
    const src = r.g0.index.array; let c = 0;
    for (let t = 0; t < r.n; t++) if (sec[t]) c++;
    if (c === r.n) return {tam: true};
    if (c === 0) return {bos: true};
    const out = new src.constructor(c * 3), orig = new Uint32Array(c); let o = 0;
    for (let t = 0; t < r.n; t++) if (sec[t]) { out[o * 3] = src[t * 3]; out[o * 3 + 1] = src[t * 3 + 1]; out[o * 3 + 2] = src[t * 3 + 2]; orig[o++] = t; }
    const g = new r.g0.constructor();
    for (const ad of Object.keys(r.g0.attributes)) g.setAttribute(ad, r.g0.attributes[ad]);
    g.setIndex(new r.g0.index.constructor(out, 1));
    g.boundingBox = r.g0.boundingBox; g.boundingSphere = r.g0.boundingSphere;
    return {geo: g, ind: out, orig, kenar: null};
  }
  function tersKume(r, sec) {                                               // soluk görünüm için kalan üçgenler
    const inv = new Uint8Array(r.n); for (let t = 0; t < r.n; t++) inv[t] = sec[t] ? 0 : 1;
    const a = altKume(r, inv); return a.tam ? {geo: r.g0} : a;
  }
  let vurguMalz = null;
  function hayaletMalzemesi(r) {
    if (vurgu.size) {                                                       // disiplin vurgusunda bağlam biraz daha görünür (yarı saydam)
      if (vurguMalz) return vurguMalz;
      const m0 = Array.isArray(r.m.material) ? r.m.material[0] : r.m.material, m = m0.clone();
      Object.assign(m, {transparent: true, opacity: 0.05, depthWrite: false, side: 0, map: null, normalMap: null, roughnessMap: null, metalnessMap: null, emissiveMap: null, aoMap: null, metalness: 0, roughness: 1});
      if (m.color) m.color.setRGB(0.2, 0.23, 0.27); if (m.emissive) m.emissive.setRGB(0, 0, 0);
      m.name = 'MEK_VURGU_SOLUK'; m.needsUpdate = true; vurguMalz = m; return m;
    }
    if (hayaletMalz) return hayaletMalz;
    const m0 = Array.isArray(r.m.material) ? r.m.material[0] : r.m.material, m = m0.clone();
    Object.assign(m, {transparent: true, opacity: 0.045, depthWrite: false, side: 0, map: null, normalMap: null, roughnessMap: null, metalnessMap: null, emissiveMap: null, aoMap: null, metalness: 0, roughness: 1});
    if (m.color) m.color.setRGB(0.42, 0.47, 0.54); if (m.emissive) m.emissive.setRGB(0, 0, 0);
    m.name = 'MEK_HAYALET'; m.needsUpdate = true; hayaletMalz = m; return m;
  }
  function hayaletKoy(r, geo) {
    if (!geo) { if (r.hay) r.hay.visible = false; return; }
    if (!r.hay) {
      const h = new r.m.constructor(geo, hayaletMalzemesi(r));
      h.userData.mekHayalet = true; h.raycast = () => {}; h.renderOrder = 2; h.name = 'HAYALET_' + (r.m.name || '');
      r.m.add(h); r.hay = h;
    }
    r.hay.material = hayaletMalzemesi(r);
    r.hay.geometry = geo; r.hay.visible = true;
  }
  let kapakGizli = false;                                                   // Kemal 2 Eki: "Ön kapaklar" kaydırıcısı tam solda → kapakla HAREKET EDEN her şey (ön sac, iç sac, fitil, menteşe kanadı, bas-aç) gizlenir; gövde kalır
  function secimDizisi(r) {
    const sec = new Uint8Array(r.n);
    if (mod && mod.tip === 'kapak') { for (let t = 0; t < r.n; t++) sec[t] = r.kpk[t]; return sec; }
    if (!mod) sec.fill(1);
    else { const M = mod.mek, K = mod.kat; for (let t = 0; t < r.n; t++) if (M.has(r.mek[t]) && (!K.size || K.has(r.kat[t]))) sec[t] = 1; }
    if (kapakGizli) for (let t = 0; t < r.n; t++) if (r.kpk[t]) sec[t] = 0;
    if (gizli.size && gozEtkin()) for (let t = 0; t < r.n; t++) if (sec[t] && gizli.has(r.mek[t])) sec[t] = 0;
    return sec;
  }
  // görünür kümeden: tam renk (vurgulanan disiplin) + soluk (vurgulanmayan görünür parçalar · 'soluk' modunda seçim dışı)
  function diziler(r) {
    const sec = secimDizisi(r);
    let tam = sec, sol = null;
    if (vurgu.size) {
      tam = new Uint8Array(r.n); sol = new Uint8Array(r.n);
      for (let t = 0; t < r.n; t++) if (sec[t]) { if (vurgu.has(r.kat[t])) tam[t] = 1; else sol[t] = 1; }
      if (yalniz) return {tam, sol: null};                                  // yalnız modu: seçilmeyen hiç çizilmez
    }
    if (hayalet === 'soluk' && mod) { sol = sol || new Uint8Array(r.n); for (let t = 0; t < r.n; t++) if (!sec[t]) sol[t] = 1; }
    return {tam, sol};
  }
  function anahtarMod() { return (gizli.size && gozEtkin() ? 'g' + [...gizli].sort((a, b) => a - b).join(',') + '|' : '') + anahtarMod0(); }
  function anahtarMod0() {
    const v = vurgu.size ? (yalniz ? 'y' : 'v') + [...vurgu].sort((a, b) => a - b).join(',') + '|' : '';
    if (!mod) return v + (kapakGizli ? 'tum|kapaksiz' : '');
    if (mod.tip === 'kapak') return v + 'kapak|' + hayalet;
    return v + (kapakGizli ? 'kapaksiz|' : '') + [...mod.mek].sort((a, b) => a - b).join(',') + '|' + [...mod.kat].sort((a, b) => a - b).join(',') + '|' + hayalet;
  }
  async function guncelle() {
    if (!hazir) return;
    const benim = ++is, sc = sahne(), key = anahtarMod(); let hesap = 0;
    for (const r of kayit) {
      const cz = cizgi(r);
      if (cz && r.cz0 === undefined) r.cz0 = r.m.geometry === r.g0 ? cz.geometry : null;
      r.cur = null;
      if (!mod && !kapakGizli && !vurgu.size && !gizli.size) {
        r.m.geometry = r.g0; if (r.gizli) { r.m.visible = true; r.gizli = false; }
        if (r.hay) r.hay.visible = false;
        if (cz) { if (r.cz0 === null) r.cz0 = kenarGeo(r, r.g0.index.array); if (r.cz0) cz.geometry = r.cz0; }
        continue;
      }
      let c = r.onbellek.get(key);
      if (!c) {
        // hızlı yol: ağda seçilen mekanizma hiç yoksa
        const hic = (!!mod && mod.tip === 'mek' && ![...r.varMek].some(x => mod.mek.has(x))) || (gizli.size > 0 && gozEtkin() && [...r.varMek].every(x => gizli.has(x)));
        if (hic) { c = {bos: true}; if (hayalet === 'soluk' && mod && !(yalniz && vurgu.size)) c.hay = {geo: r.g0}; }
        else {
          const d = diziler(r);
          c = altKume(r, d.tam);
          if (d.sol) { const h = altKume(r, d.sol); c.hay = h.bos ? null : (h.tam ? {geo: r.g0} : h); }
        }
        r.onbellek.set(key, c);
      }
      if (c.bos) {
        if (c.hay) {                                                            // ağ görünür kalır ama yalnız soluk kopyası çizilir
          if (r.gizli) { r.m.visible = true; r.gizli = false; }
          r.m.geometry = BOS(r); if (cz) cz.geometry = BOS(r);
          hayaletKoy(r, c.hay.geo);
        } else { if (r.m.visible) { r.m.visible = false; r.gizli = true; } hayaletKoy(r, null); }
        continue;
      }
      if (r.gizli) { r.m.visible = true; r.gizli = false; }
      if (c.tam) {
        r.m.geometry = r.g0; hayaletKoy(r, null);
        if (cz) { if (r.cz0 === null) r.cz0 = kenarGeo(r, r.g0.index.array); if (r.cz0) cz.geometry = r.cz0; }
        continue;
      }
      r.m.geometry = c.geo; r.cur = c;
      hayaletKoy(r, c.hay ? c.hay.geo : null);
      if (cz) {
        if (!c.kenar) {
          c.kenar = kenarGeo(r, c.ind);
          if (++hesap % 6 === 0) { yazDurum('kenar çizgileri hesaplanıyor…'); if (sc && sc.queueRender) sc.queueRender(); await new Promise(res => setTimeout(res, 0)); if (benim !== is) return; }
        }
        cz.geometry = c.kenar;
      }
    }
    if (sc && sc.queueRender) sc.queueRender();
    yazDurum('');
  }
  const bosGeo = new WeakMap();
  function BOS(r) {
    let g = bosGeo.get(r.g0);
    if (!g) {
      g = new r.g0.constructor(); for (const ad of Object.keys(r.g0.attributes)) g.setAttribute(ad, r.g0.attributes[ad]);
      g.setIndex(new r.g0.index.constructor(new r.g0.index.array.constructor(0), 1)); g.boundingSphere = r.g0.boundingSphere; g.boundingBox = r.g0.boundingBox;
      bosGeo.set(r.g0, g);
    }
    return g;
  }
  let durumEl = null;
  const yazDurum = t => { if (durumEl) durumEl.textContent = t || ozetYazi(); };

  // diğer görünümleri kapat (aynı ağları değiştiriyorlar)
  function digerleriniKapat() {
    const dk = document.getElementById('dis-kabuk');
    if (dk && dk.getAttribute('aria-pressed') === 'true') dk.click();
    const hepsi = document.querySelector('#kat-dugmeler button');
    if (hepsi && hepsi.getAttribute('aria-pressed') === 'false') hepsi.click();
  }
  let kapiDurumu = null;
  function kapiSaydamligi(ac) {                                            // kapak görünümünde ön kapaklar metal (opak) olsun
    const k = [...document.querySelectorAll('.m3ar input[type="range"]')].find(e => (e.title || '').includes('metal kapak'));
    if (!k) return;
    k.disabled = !!ac;                                                     // kapak görünümünde kaydırıcı kilitli: kapaklar hep opak görünür
    if (ac) { if (kapiDurumu === null) kapiDurumu = k.value; k.value = '100'; k.dispatchEvent(new Event('input', {bubbles: true})); }
    else if (kapiDurumu !== null) { k.value = kapiDurumu; kapiDurumu = null; k.dispatchEvent(new Event('input', {bubbles: true})); }
  }
  let golge0 = null;
  function golge(ac) {
    if (golge0 === null) golge0 = mv.shadowIntensity;
    mv.shadowIntensity = ac ? golge0 : 0;
  }
  async function ayarla(yeni) {
    await bekle();
    if (yeni) digerleriniKapat();
    const eskiKapak = mod && mod.tip === 'kapak';
    mod = yeni;
    if (KAD()) gizli.clear();                                               // her kademe değişiminde göz ayarı sıfırlanır
    golge(!mod || (mod.tip === 'mek' && mod.kademe === 'makine'));          // Kemal 2 Eki: istasyon/mekanizma görünümünde zemin yok → gölge düzleminin kenarı boşlukta çizgi gibi görünüyordu (makine kademesinde zemin var → gölge açık)
    if (eskiKapak && !(mod && mod.tip === 'kapak')) kapiSaydamligi(false);
    if (mod && mod.tip === 'kapak') kapiSaydamligi(true);
    bildir();
    await guncelle();
  }
  // kategori / dış kabuk düğmesine basılınca önce bu görünüm kapanır
  document.addEventListener('click', e => {
    if (!(mod || vurgu.size || gizli.size) || !e.target || !e.target.closest) return;
    if (e.target.closest('#kat-dugmeler button') || e.target.closest('#dis-kabuk')) { mod = null; vurgu.clear(); gizli.clear(); golge(true); kapiSaydamligi(false); bildir(); disiplinBoya(); guncelle(); }
  }, true);
  // model-viewer 'load' aynı model için ikinci kez gelebiliyor; dis-kabuk.js o anda ağların geometrisini "asıl" diye saklıyor →
  // seçim/vurgu açıksa önce asıl geometriler geri konur (yakalama evresi = dis-kabuk'tan önce), görünüm hemen ardından yeniden uygulanır.
  document.addEventListener('load', e => {
    if (e.target !== mv || !hazir || !(mod || kapakGizli || vurgu.size || gizli.size)) return;
    const sc = sahne();
    if (!(sc && kayit.length && kayit.every(r => { let o = r.m; while (o.parent) o = o.parent; return o === sc; }))) return;
    for (const r of kayit) { r.m.geometry = r.g0; if (r.gizli) { r.m.visible = true; r.gizli = false; } if (r.hay) r.hay.visible = false; }
    setTimeout(() => guncelle(), 0);
  }, true);

  // ------------------------------------------------------------------ DİSİPLİN düğmeleri (yalnız MEK3_DISIPLIN sayfalarında)
  const DSP_CSS = `
  .dsp{position:absolute;top:12px;left:150px;right:150px;z-index:5;display:flex;flex-wrap:wrap;justify-content:center;gap:4px;
       margin:0 auto;width:fit-content;padding:5px;border-radius:14px;background:rgba(21,24,29,.62);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}
  .dsp button{display:inline-flex;align-items:center;gap:6px;border:1px solid #39424f;background:rgba(35,41,50,.92);color:#dce3ea;border-radius:999px;
       padding:4px 10px;font:600 11.5px/1.2 system-ui,sans-serif;cursor:pointer;white-space:nowrap;transition:background .12s,border-color .12s}
  .m3 .et{top:76px}
  .dsp button:hover{border-color:#6b7889;color:#fff}
  .dsp button i{width:8px;height:8px;border-radius:50%;flex:none;background:var(--r)}
  .dsp button[aria-pressed=true]{background:var(--r);border-color:var(--r);color:#fff}
  .dsp button[aria-pressed=true] i{background:#fff}
  .dsp button.hep[aria-pressed=true]{background:#e6ebf0;border-color:#e6ebf0;color:#15181d}
  .dsp .mod{display:inline-flex;flex:none;padding:2px;margin-right:4px;border-radius:999px;background:rgba(0,0,0,.28);border:1px solid #39424f}
  .dsp .mod button{border:0;background:transparent;color:#9aa5b1;padding:3px 9px;font-weight:500;font-size:11px}
  .dsp .mod button:hover{color:#fff}
  .dsp .mod button[aria-pressed=true]{background:#e6ebf0;color:#15181d;font-weight:600}
  @media (max-width:760px){.dsp{top:auto;bottom:10px;left:8px;right:62px;width:auto;flex-wrap:nowrap;justify-content:flex-start;
       overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}.dsp::-webkit-scrollbar{display:none}.dsp button{padding:7px 12px}}`;
  let DSP = null;
  function disiplinKur() {
    if (!DISIPLIN || !hazir) return;
    if (!DSP) {
      const st = el('style'); st.textContent = DSP_CSS; document.head.appendChild(st);
      DSP = el('div', 'dsp'); DSP.id = 'disiplin'; DSP.setAttribute('role', 'toolbar'); DSP.setAttribute('aria-label', 'Disiplin vurgusu');
      DSP.addEventListener('pointerdown', e => e.stopPropagation()); DSP.addEventListener('dblclick', e => e.stopPropagation());
      mv.appendChild(DSP);
    }
    const say = new Map();
    for (const r of kayit) for (let t = 0; t < r.n; t++) say.set(r.kat[t], (say.get(r.kat[t]) || 0) + 1);
    DSP.textContent = '';
    const md = el('span', 'mod'); md.setAttribute('role', 'group'); md.setAttribute('aria-label', 'Seçilmeyen parçalar');
    [['soluk', 'seçilmeyen parçalar soluk (yarı saydam) görünür'], ['yalnız', 'seçilmeyen parçalar tamamen gizli · seçili tür tüm hatta tek başına görünür']].forEach(([ad, ip], j) => {
      const b = el('button', null, ad); b.type = 'button'; b.dataset.m = String(j); b.title = ip;
      b.onclick = () => modSec(j === 1); md.append(b);
    });
    DSP.append(md);
    const h = el('button', 'hep', 'Hepsi'); h.type = 'button'; h.title = 'vurguyu kaldır (her şey normal renk)'; h.dataset.k = '-1';
    h.onclick = () => disiplinSec(-1); DSP.append(h);
    KATL.forEach((k, i) => {
      if (!say.get(i)) return;
      const b = el('button', null, '<i></i>' + (k.ad || k.kod)); b.type = 'button'; b.dataset.k = String(i);
      b.style.setProperty('--r', DSP_RENK[k.kod] || '#4f86ff');
      b.title = (k.icerik || '') + (k.kime ? ' · kime: ' + k.kime : '') + ' · ' + say.get(i).toLocaleString('tr-TR') + ' üçgen · bas: bu tür tam renk, diğerleri soluk ya da gizli (soldaki anahtar) · birden çok seçilebilir';
      b.onclick = () => disiplinSec(i); DSP.append(b);
    });
    disiplinBoya();
  }
  function disiplinBoya() {
    if (!DSP) return;
    DSP.querySelectorAll('button[data-k]').forEach(b => { const i = +b.dataset.k; b.setAttribute('aria-pressed', String(i === -1 ? !vurgu.size : vurgu.has(i))); });
    DSP.querySelectorAll('.mod button').forEach(b => b.setAttribute('aria-pressed', String((b.dataset.m === '1') === yalniz)));
  }
  async function modSec(y) {
    if (y === yalniz) return;
    yalniz = y; try { localStorage.setItem('mek3_tur_mod', y ? 'yalniz' : 'soluk'); } catch (e) {}
    disiplinBoya(); await bekle(); yazDurum(''); await guncelle();
  }
  async function disiplinSec(i) {
    await bekle();
    if (i === -1) vurgu.clear(); else if (vurgu.has(i)) vurgu.delete(i); else vurgu.add(i);
    const dk = document.getElementById('dis-kabuk');
    if (vurgu.size && dk && dk.getAttribute('aria-pressed') === 'true') dk.click();   // dış kabuk aynı ağları değiştirir → önce kapanır
    disiplinBoya(); yazDurum(''); await guncelle();
  }

  // ------------------------------------------------------------------ kamera
  function cerceve(kodlar) {
    if (!D || !D.kutu) return;
    let b = null;
    kodlar.forEach(k => { const x = D.kutu[k]; if (!x) return; b = b ? [Math.min(b[0], x[0]), Math.max(b[1], x[1]), Math.min(b[2], x[2]), Math.max(b[3], x[3]), Math.min(b[4], x[4]), Math.max(b[5], x[5])] : x.slice(); });
    if (!b) return;
    if (!kamera0) kamera0 = {t: mv.getAttribute('camera-target'), o: mv.getAttribute('camera-orbit'), min: mv.getAttribute('min-camera-orbit')};
    const c = [(b[0] + b[1]) / 2, (b[2] + b[3]) / 2, (b[4] + b[5]) / 2];
    const cap = Math.hypot(b[1] - b[0], b[3] - b[2], b[5] - b[4]);
    const fov = (parseFloat(mv.getAttribute('field-of-view')) || 30) * Math.PI / 180;
    const d = Math.max(0.5, cap * 0.62 / Math.tan(fov / 2));
    const o = mv.getCameraOrbit();
    mv.minCameraOrbit = 'auto auto 0.2m';
    mv.cameraTarget = c[0].toFixed(3) + 'm ' + c[1].toFixed(3) + 'm ' + c[2].toFixed(3) + 'm';
    mv.cameraOrbit = o.theta + 'rad ' + o.phi + 'rad ' + d.toFixed(2) + 'm';
  }
  function kameraGeri() {
    if (!kamera0) return;
    mv.cameraTarget = kamera0.t || 'auto auto auto';
    const o = mv.getCameraOrbit();
    const r = (kamera0.o || '').split(/\s+/)[2] || 'auto';
    mv.cameraOrbit = o.theta + 'rad ' + o.phi + 'rad ' + r;
  }

  // ------------------------------------------------------------------ seçim (istasyon / mekanizma / tür)
  const istAd = k => { const s = D && D.istasyon.find(x => x.kod === k); return s ? s.ad : k; };
  const mekleri = ist => LISTE.map((m, i) => [m, i]).filter(([m]) => ist.indexOf(m.istasyon) >= 0).map(([, i]) => i);
  function istasyonAc(ist, kamera = true, ust = null) {
    ist = [].concat(ist);
    const mek = new Set(mekleri(ist));
    if (!ust) ust = ist.every(k => MAK_IST().indexOf(k) >= 0) ? 'makine' : 'dukkan';   // geri düğmesinin gideceği kademe
    ayarla({tip: 'mek', mek, kat: new Set(), ist, sec: null, ust});
    if (kamera) cerceve(LISTE.filter((m, i) => mek.has(i)).map(m => m.kod));
    hashYaz('ist=' + ist.join(','));
  }
  function makineAc(kamera = true) {                                        // kademe 2: yalnız makine (+ zemin yüzeyi)
    const mek = new Set(makineMek());
    ayarla({tip: 'mek', kademe: 'makine', mek, kat: new Set(), ist: MAK_IST().slice(), sec: null});
    if (kamera) cerceve(LISTE.filter((m, i) => mek.has(i) && MAK_IST().indexOf(m.istasyon) >= 0).map(m => m.kod));
    hashYaz('k=makine');
  }
  function geri() {                                                         // bir üst kademe
    const k = kademe();
    if (k === 'istasyon' && mod.ust === 'makine') makineAc();
    else if (k !== 'dukkan') hepsi();
  }
  function mekanizmaSec(i, kamera = true) {
    const m = LISTE[i]; if (!m) return;
    const ist = mod && mod.tip === 'mek' && mod.ist ? mod.ist : [m.istasyon];
    ayarla({tip: 'mek', mek: new Set([i]), kat: new Set(), ist: ist.indexOf(m.istasyon) >= 0 ? ist : [m.istasyon], sec: i});
    if (kamera) cerceve([m.kod]);
    hashYaz('mek=' + m.kod);
  }
  function katSec(k) {
    if (!mod || mod.tip !== 'mek') return;
    const kat = new Set(mod.kat); if (k === -1) kat.clear(); else if (kat.has(k)) kat.delete(k); else kat.add(k);
    ayarla(Object.assign({}, mod, {kat}));
  }
  function hepsi() { ayarla(null); kameraGeri(); hashYaz(''); }
  function hashYaz(h) { try { history.replaceState(null, '', h ? '#' + encodeURI(h) : location.pathname + location.search); } catch (e) {} }

  function ozetYazi() {
    const v = vurgu.size ? (yalniz ? ' · yalnız: ' : ' · vurgu: ') + [...vurgu].map(i => (KATL[i] && (KATL[i].ad || KATL[i].kod)) || i).join(' + ') : '';
    return ozetYazi0() + v;
  }
  function ozetYazi0() {
    if (KAD()) {
      const k = kademe(), g = '';                                        // gizli sayısı satırlarda (soluk göz) görünür; yazı boyu sabit kalsın
      if (k === 'dukkan') return 'Makineye çift tıkla: yalnız makine · QR / tezgâha çift tıkla: o birim' + g;
      if (k === 'makine') return 'İstasyona çift tıkla: istasyon tam montajıyla açılır' + g;
      if (k === 'istasyon') return 'Üniteye bas: gizle / göster · çift bas: yalnız o' + g;
    }
    if (!mod) return DISIPLIN ? 'İstasyon başlığına bas ya da 3B\'de istasyona çift tıkla.' : 'Bir istasyona ya da mekanizmaya bas · 3B\'de istasyona tıkla.';
    if (mod.tip === 'kapak') return 'Yalnız kapaklar: ön kapaklar · kanatlar · servis / düşer kapaklar · çekmece önleri (menteşe + basaç dahil).';
    const ad = mod.sec != null ? istAd(LISTE[mod.sec].istasyon) + ' › ' + LISTE[mod.sec].ad : mod.ist.map(istAd).join(' + ') + ' · alt montaj';
    const k = mod.kat.size ? ' · ' + [...mod.kat].map(i => (KATL[i] && (KATL[i].ad || KATL[i].kod)) || i).join(' + ') : '';
    return ad + k;
  }

  // ------------------------------------------------------------------ PANEL
  const CSS = `
  .mk{padding:0 16px 6px;color:#dce3ea;font:13px/1.4 system-ui,sans-serif}
  .mk .mk-ust{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:0 0 8px}
  .mk button{border:1px solid #39424f;background:#232932;color:#cfd6df;border-radius:8px;padding:5px 10px;font:600 12.5px system-ui,sans-serif;cursor:pointer}
  .mk button:hover{border-color:#4f86ff;color:#fff}
  .mk button[aria-pressed=true]{background:#4f86ff;border-color:#4f86ff;color:#fff}
  .mk .mk-hay{display:inline-flex;gap:0;margin-left:auto}.mk .mk-hay button{border-radius:0;padding:5px 8px;font-size:11.5px}
  .mk .mk-hay button:first-child{border-radius:8px 0 0 8px}.mk .mk-hay button:last-child{border-radius:0 8px 8px 0;border-left:0}
  .mk .mk-yol{min-height:18px;margin:2px 0 8px;color:#ffd978;font-weight:600}
  .mk .mk-tur{display:none;flex-wrap:wrap;gap:5px;margin:0 0 10px}.mk .mk-tur.on{display:flex}
  .mk .mk-tur button{border-radius:999px;padding:3px 9px;font-size:11.5px}
  .mk .mk-tur span{color:#8d97a4;font:700 11px system-ui;letter-spacing:.05em;align-self:center;margin-right:2px}
  .mk details{border:1px solid #2f3742;border-radius:10px;margin:0 0 6px;background:#1f252d}
  .mk details[open]{border-color:#3d4a5c}
  .mk summary{list-style:none;cursor:pointer;padding:8px 10px;display:flex;align-items:center;gap:8px;font-weight:700;color:#e6ebf0}
  .mk summary::-webkit-details-marker{display:none}
  .mk summary i{font-style:normal;color:#8d97a4;transition:transform .15s}.mk details[open] summary i{transform:rotate(90deg)}
  .mk summary small{margin-left:auto;color:#8d97a4;font-weight:500;font-size:11.5px}
  .mk summary.ak{color:#ffd978}
  .mk .mk-l{display:flex;flex-direction:column;gap:3px;padding:0 8px 8px 26px}
  .mk .mk-l button{display:flex;justify-content:space-between;gap:8px;text-align:left;border-color:#2f3742;background:#232932;font-weight:600}
  .mk .mk-l button small{color:#8d97a4;font-weight:500}
  .mk .mk-l button[aria-pressed=true]{background:#4f86ff;border-color:#4f86ff;color:#fff}
  .mk .mk-l button[aria-pressed=true] small{color:#e6ecff}
  .mk .mk-not{color:#6d7682;font-size:11.5px;margin:6px 0 0}
  @media (max-width:760px){.mk button{padding:7px 11px}}`;
  const CSS_K = `
  .mk .mk-geri[hidden],.mk #mk-tum[hidden]{display:none}
  .mk .mk-kir{display:flex;flex-wrap:wrap;align-items:center;gap:2px 6px;margin:2px 0 4px;color:#e6ebf0;font:700 13.5px/1.4 system-ui,sans-serif}
  .mk .mk-kir:empty{display:none}
  .mk .mk-kir .mk-kb{border:0;background:none;padding:0;border-radius:4px;color:#8fb3ff;font:700 13.5px/1.4 system-ui,sans-serif;cursor:pointer}
  .mk .mk-kir .mk-kb:hover{color:#fff;text-decoration:underline;border:0}
  .mk .mk-kir .mk-ok{color:#5d6672;font-weight:500}
  .mk .mk-bas{display:flex;align-items:center;gap:4px;margin:8px 0 6px;color:#8d97a4;font:700 11px system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase}
  .mk .mk-bas>span{margin-right:auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .mk .mk-bas button{white-space:nowrap;flex:none;padding:3px 8px;border-radius:999px;font:600 11px system-ui,sans-serif;letter-spacing:0;text-transform:none;color:#aab4c0;background:#1f252d;border-color:#2f3742}
  .mk .mk-s{display:flex;gap:4px;margin:0 0 4px}
  .mk .mk-alt{margin:0 0 6px 14px;padding-left:8px;border-left:1px solid #2f3742}
  .mk .mk-r{flex:1;min-width:0;display:flex;align-items:center;gap:9px;text-align:left;border:1px solid #2f3742;background:#1f252d;color:#e6ebf0;
       padding:7px 10px;border-radius:10px;font:600 12.5px system-ui,sans-serif;cursor:pointer;user-select:none;-webkit-user-select:none;transition:opacity .12s,background .12s}
  .mk button.mk-r[aria-pressed]{background:#1f252d;border-color:#2f3742;color:#e6ebf0}
  .mk .mk-r:hover,.mk button.mk-r[aria-pressed]:hover{border-color:#4a5768;background:#232a33}
  .mk .mk-r>span{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .mk .mk-r small{color:#8d97a4;font-weight:500;font-size:11.5px;white-space:nowrap}
  .mk .mk-goz{display:inline-flex;flex:none;color:#8fb3ff}
  .mk .mk-goz svg{width:16px;height:16px}
  .mk .mk-goz .k{display:none}
  .mk .mk-r[data-d=off]{opacity:.45}
  .mk .mk-r[data-d=off] .mk-goz{color:#7d8794}
  .mk .mk-r[data-d=off] .mk-goz .a{display:none}.mk .mk-r[data-d=off] .mk-goz .k{display:inline}
  .mk .mk-r[data-d=yarim] .mk-goz{color:#c9a227}
  .mk .mk-r.ana{font-weight:700;font-size:13px}
  .mk .mk-ac{flex:none;display:inline-flex;align-items:center;justify-content:center;min-width:34px;border-radius:10px;padding:0 10px;font:600 17px/1 system-ui,sans-serif;color:#cfd6df;background:#232932;border:1px solid #2f3742}
  .mk .mk-ac:hover{background:#4f86ff;border-color:#4f86ff;color:#fff}
  .mk3-geri{position:absolute;top:46px;left:12px;z-index:6;display:none;align-items:center;gap:6px;border:1px solid #39424f;background:rgba(21,24,29,.8);color:#e6ebf0;
       border-radius:999px;padding:6px 13px 6px 10px;font:600 12.5px system-ui,sans-serif;cursor:pointer;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}
  .mk3-geri.on{display:inline-flex}
  .mk3-geri:hover{border-color:#6b7889;background:rgba(35,41,50,.95)}
  @media (max-width:760px){.mk .mk-r{padding:9px 11px}.mk .mk-ac{min-width:40px}}`;
  const GOZ = '<i class="mk-goz" aria-hidden="true"><svg class="a" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>' +
              '<svg class="k" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3l18 18"/><path d="M10.6 5.1A10.4 10.4 0 0 1 12 5c6.4 0 10 7 10 7a17.6 17.6 0 0 1-3.2 4.1M6.6 6.6C3.9 8.3 2 12 2 12s3.6 7 10 7a9.7 9.7 0 0 0 5.4-1.6"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/></svg></i>';
  const MONTAJ = {A: 'a-montaj.html', B: 'b-montaj.html', TOPPING: 'topping-montaj.html', F: 'f-montaj.html', K: '../../../claude-k-montaj-v1/otonom/hat/k-montaj.html', E: 'e-montaj.html', U: 'u-montaj.html'};   // Kemal 4 Eki: her istasyonun montaj animasyonu
  function montajLink(kod, uzun) {
    const h = MONTAJ[String(kod).toUpperCase()]; if (!h) return null;
    const m = document.createElement('a'); m.href = h; m.target = '_blank'; m.rel = 'noopener';
    m.textContent = uzun ? '▶ Montaj animasyonunu aç' : '▶ Montaj animasyonu'; m.title = 'bu istasyonun montaj animasyonu (yeni sekme)';
    m.style.cssText = 'display:block;margin:2px 0 8px 34px;color:#ffd978;font:600 12.5px system-ui,sans-serif;text-decoration:none';
    m.addEventListener('click', e => e.stopPropagation());
    return m;
  }
  function el(t, c, h) { const e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; }
  let P = {};
  function panelKur() {
    if (P.kok) return;
    const st = el('style'); st.textContent = CSS + (DISIPLIN ? CSS_K : ''); document.head.appendChild(st);
    const kok = el('div', 'mk'); kok.id = 'mek-panel';
    const ust = el('div', 'mk-ust');
    const tum = el('button', null, 'Tüm hat'); tum.type = 'button'; tum.id = 'mk-tum'; tum.title = 'seçimi kaldır, bütün hattı göster (Esc)'; tum.onclick = hepsi;
    const gr = el('button', 'mk-geri', '← Dükkân'); gr.type = 'button'; gr.hidden = true; gr.title = 'bir üst kademe (Esc)'; gr.onclick = () => geri();
    P.geri = gr; ust.append(gr);
    const hay = el('span', 'mk-hay');
    const hg = el('button', null, 'diğerleri gizli'), hs = el('button', null, 'soluk');
    hg.type = hs.type = 'button'; hg.title = 'seçilmeyen parçalar görünmez'; hs.title = 'seçilmeyen parçalar soluk (yer algısı için)';
    const hayBoya = () => { hg.setAttribute('aria-pressed', String(hayalet === 'gizle')); hs.setAttribute('aria-pressed', String(hayalet === 'soluk')); };
    hg.onclick = () => { hayalet = 'gizle'; hayBoya(); if (mod) guncelle(); };
    hs.onclick = () => { hayalet = 'soluk'; hayBoya(); if (mod) guncelle(); };
    hayBoya(); hay.append(hg, hs); hay.style.display = "none";   // Kemal: göz düğmeleri varken gereksiz; seçilmeyen hep gizli
    ust.append(tum); P.kapakYeri = el('span'); ust.append(P.kapakYeri, hay);
    const yol = el('div', 'mk-yol'); yol.setAttribute('role', 'status');
    const kir = el('nav', 'mk-kir'); kir.setAttribute('aria-label', 'kademe yolu'); P.kir = kir;
    const tur = el('div', 'mk-tur');
    const agac = el('div', 'mk-agac', '<div class="mk-not">Mekanizma tablosu yükleniyor…</div>');
    const not = el('div', 'mk-not', DISIPLIN ? 'İstasyon başlığına bas ya da 3B\'de istasyona çift tıkla: istasyon tam montajıyla açılır. Üniteye bas: yalnız o ünite (motoru, sensörü, silindiri içinde; kablosu istasyonun Elektrik ünitesinde). Disiplin vurgusu (Motor · Sensör · Hava · Elektrik …) modelin üstündeki düğmelerden.' : 'İstasyon başlığına bas: alt montaj açılır. Mekanizmaya bas: yalnız o (motoru, kablosu, hava parçaları dahil). Açık istasyonda 3B\'de parçaya tıkla: mekanizması seçilir.');
    kok.append(ust, kir, yol, tur, agac, not);
    P = Object.assign(P, {kok, yol, tur, agac, tum, not});
    durumEl = yol;
    // yerleşim: yan panel varsa "Görünüm"den sonra kendi bölümü, yoksa kategori çubuğunun altına
    const yerlestir = () => {
      const ic = document.querySelector('#yan .yan-ic');
      if (ic) {
        const s = el('section', 'yan-grp'); s.id = 'mek-grp';
        s.append(el('h3', null, DISIPLIN ? 'Montaj ağacı · istasyon → ünite' : 'Mekanizma · istasyon alt montajı'), kok);
        const gor = [...ic.querySelectorAll('.yan-grp')].find(x => (x.querySelector('h3') || {}).textContent === 'Görünüm');
        if (gor && gor.nextSibling) ic.insertBefore(s, gor.nextSibling); else ic.appendChild(s);
        return true;
      }
      return false;
    };
    if (!yerlestir()) {
      const kc = document.getElementById('kat-cubuk');
      (kc ? kc.parentNode : mv.parentNode).insertBefore(kok, kc ? kc.nextSibling : mv.nextSibling);
      setTimeout(() => { if (!document.getElementById('mek-grp') && document.querySelector('#yan .yan-ic')) { kok.remove(); yerlestir(); } }, 500);
    }
    dinleyici.push(panelBoya);
    yazDurum('');
  }
  // ------------------------------------------------------------------ KADEME AĞACI (göz satırları)
  const kapsam = () => { const k = kademe(); return (k === 'makine' || k === 'istasyon') ? [...mod.mek] : LISTE.map((m, i) => i); };
  function gozBoya() {
    (P.satir || []).forEach(({b, uyeler}) => {
      const h = uyeler.filter(i => gizli.has(i)).length, d = h === 0 ? 'on' : h === uyeler.length ? 'off' : 'yarim';
      b.dataset.d = d; b.setAttribute('aria-pressed', String(d !== 'off'));
    });
  }
  async function gozUygula() { gozBoya(); yazDurum(''); await bekle(); await guncelle(); }
  function gozDegis(uyeler) { const acik = uyeler.some(i => !gizli.has(i)); uyeler.forEach(i => acik ? gizli.add(i) : gizli.delete(i)); gozUygula(); }
  function solo(uyeler) { gizli = new Set(kapsam().filter(i => uyeler.indexOf(i) < 0)); gozUygula(); }
  function hepsiGoz(goster) { gizli = goster ? new Set() : new Set(kapsam()); gozUygula(); }
  function satir(kap, ad, sag, uyeler, ac, ana) {
    const w = el('div', 'mk-s');
    const b = el('button', 'mk-r' + (ana ? ' ana' : ''), GOZ + '<span>' + ad + '</span><small>' + sag + '</small>');
    b.type = 'button'; b.title = ad + ' · bas: gizle / göster · çift bas: yalnız bu';
    let tmr = null;
    b.addEventListener('click', () => { clearTimeout(tmr); tmr = setTimeout(() => gozDegis(uyeler), 230); });
    b.addEventListener('dblclick', e => { e.preventDefault(); clearTimeout(tmr); solo(uyeler); });
    w.append(b);
    if (ac) { const o = el('button', 'mk-ac', '›'); o.type = 'button'; o.title = ad + ' · aç'; o.setAttribute('aria-label', ad + ' aç'); o.onclick = ac; w.append(o); }
    kap.append(w); P.satir.push({b, uyeler});
    return w;
  }
  function baslik(kap, ad) {
    const h = el('div', 'mk-bas', '<span>' + ad + '</span>');
    const g = el('button', null, 'hepsini göster'), s = el('button', null, 'hepsini gizle');
    g.type = s.type = 'button'; g.onclick = () => hepsiGoz(true); s.onclick = () => hepsiGoz(false);
    h.append(g, s); kap.append(h);
  }
  function agacKurK() {
    const k = kademe(), imza = k + '|' + (mod && mod.ist ? mod.ist.join(',') : '');
    if (P.imza === imza && P.agac.querySelector('.mk-s')) { gozBoya(); return; }
    P.imza = imza; P.agac.textContent = ''; P.satir = [];
    if (!P.parcaSay) { P.parcaSay = {}; Object.values(D.parca).forEach(x => { P.parcaSay[x] = (P.parcaSay[x] || 0) + 1; }); }
    const IST = D.istasyon.filter(s => mekleri([s.kod]).length), ist = c => IST.find(s => s.kod === c);
    const mak = MAK_IST().filter(c => ist(c));
    const istSatir = (kap, s, ust) => {
      const u = mekleri([s.kod]);
      satir(kap, s.ad, u.length + ' ünite', u, () => { istasyonAc(s.kod, true, ust); odakla(s.kod); });
      const ml = montajLink(s.kod); if (ml) kap.append(ml);
    };
    if (k === 'istasyon') {
      baslik(P.agac, mod.ist.map(istAd).join(' + ') + ' · üniteler');
      if (mod.ist.length === 1) { const ml = montajLink(mod.ist[0], true); if (ml) { ml.style.margin = '4px 0 10px 4px'; ml.style.fontSize = '14px'; P.agac.append(ml); } }
      [...mod.mek].sort((a, b) => a - b).forEach(i => { const m = LISTE[i]; satir(P.agac, m.ad, P.parcaSay[m.kod] ? P.parcaSay[m.kod] + ' parça' : '', [i], null); });
    } else if (k === 'makine') {
      baslik(P.agac, 'Makine · istasyonlar');
      mak.forEach(c => istSatir(P.agac, ist(c), 'makine'));
      (D.kademe.makine.ek || []).forEach(kod => { const i = LISTE.findIndex(m => m.kod === kod); if (i >= 0) satir(P.agac, LISTE[i].ad, 'dükkân', [i], null); });
    } else {
      baslik(P.agac, 'Dükkân');
      const makU = makineMek(false);
      satir(P.agac, 'Makine', mak.length + ' istasyon', makU, () => makineAc(), true);
      const alt = el('div', 'mk-alt'); P.agac.append(alt);
      mak.forEach(c => istSatir(alt, ist(c), 'makine'));
      IST.filter(s => mak.indexOf(s.kod) < 0).forEach(s => istSatir(P.agac, s, 'dukkan'));
    }
    gozBoya();
  }
  function kirintiBoya() {
    if (!P.kir) return;
    const k = kademe(), yol = [['Dükkân', k !== 'dukkan' ? () => hepsi() : null]];
    if (k === 'makine' || (k === 'istasyon' && mod.ust === 'makine')) yol.push(['Makine', k !== 'makine' ? () => makineAc() : null]);
    if (k === 'istasyon') yol.push([mod.ist.map(istAd).join(' + '), null]);
    if (k === 'kapak') yol.push(['Kapaklar', null]);
    P.kir.textContent = '';
    yol.forEach(([ad, f], i) => {
      if (i) P.kir.append(el('span', 'mk-ok', '›'));
      const x = el(f ? 'button' : 'span', f ? 'mk-kb' : null); x.textContent = ad;
      if (f) { x.type = 'button'; x.title = ad + ' kademesine dön'; x.onclick = f; }
      P.kir.append(x);
    });
    if (k === 'istasyon' && mod.ist.length === 1 && MONTAJ[String(mod.ist[0]).toUpperCase()]) {
      const m = el('a', 'mk-kb'); m.href = MONTAJ[String(mod.ist[0]).toUpperCase()]; m.target = '_blank'; m.rel = 'noopener';
      m.textContent = '▶ Montaj animasyonu'; m.title = 'bu istasyonun montaj animasyonu (yeni sekme)'; m.style.marginLeft = '10px'; m.style.textDecoration = 'none';
      P.kir.append(m);
    }
    const ust = k === 'istasyon' && mod.ust === 'makine' ? 'Makine' : 'Dükkân';
    if (P.geri) { P.geri.hidden = k === 'dukkan'; P.geri.textContent = '← ' + ust; }
    if (P.geri3) { P.geri3.classList.toggle('on', k !== 'dukkan'); P.geri3.textContent = '← ' + ust; }
    if (P.tum) P.tum.hidden = true;
  }
  function geri3BKur() {
    if (P.geri3 || !KAD()) return;
    const b = el('button', 'mk3-geri'); b.type = 'button'; b.title = 'bir üst kademe (Esc)';
    b.addEventListener('pointerdown', e => e.stopPropagation()); b.addEventListener('dblclick', e => e.stopPropagation());
    b.onclick = () => geri(); mv.appendChild(b); P.geri3 = b; kirintiBoya();
  }
  function agacKur() {
    if (KAD()) {
      if (P.not) P.not.textContent = 'Satıra bas: gizle / göster (birkaç şeyi birlikte görmek için) · çift bas: yalnız o · › : aç. 3B\'de çift tık bir alt kademeyi açar (dükkân › makine › istasyon); ← , Esc ya da üstteki yol bir üst kademeye döner. Disiplin vurgusu modelin üstündeki düğmelerden.';
      geri3BKur(); agacKurK(); kirintiBoya(); return;
    }
    const parcaSay = {};
    Object.values(D.parca).forEach(k => { parcaSay[k] = (parcaSay[k] || 0) + 1; });
    P.agac.textContent = '';
    P.det = {}; P.mekBtn = {};
    D.istasyon.forEach(s => {
      const ids = mekleri([s.kod]); if (!ids.length) return;
      const d = el('details'); d.dataset.ist = s.kod;
      const sm = el('summary', null, '<i>›</i>' + s.ad + '<small>' + ids.length + (DISIPLIN ? ' ünite' : ' mekanizma') + '</small>');
      sm.title = s.ad + ' alt montajını aç';
      sm.onclick = e => { e.preventDefault(); const acik = mod && mod.tip === 'mek' && mod.sec == null && mod.ist.length === 1 && mod.ist[0] === s.kod; if (acik) { d.open = !d.open; return; } istasyonAc(s.kod); };
      const l = el('div', 'mk-l');
      ids.forEach(i => {
        const m = LISTE[i], b = el('button', null, '<span>' + m.ad + '</span><small>' + (parcaSay[m.kod] ? parcaSay[m.kod] + ' parça' : '') + '</small>');
        b.type = 'button'; b.dataset.mek = m.kod; b.title = m.kod;
        b.onclick = () => { if (mod && mod.tip === 'mek' && mod.sec === i) istasyonAc(mod.ist); else mekanizmaSec(i); };
        l.appendChild(b); P.mekBtn[i] = b;
      });
      d.append(sm, l); P.agac.appendChild(d); P.det[s.kod] = d;
    });
    panelBoya();
  }
  function panelBoya() {
    if (!P.kok) return;
    yazDurum('');
    if (KAD()) { if (P.agac && LISTE.length) { agacKurK(); kirintiBoya(); } return; }
    const mm = mod && mod.tip === 'mek' ? mod : null;
    Object.entries(P.det || {}).forEach(([k, d]) => {
      const ak = !!(mm && mm.ist.indexOf(k) >= 0);
      if (ak) d.open = true; else if (mm) d.open = false;
      d.querySelector('summary').classList.toggle('ak', ak && mm.sec == null);
    });
    Object.entries(P.mekBtn || {}).forEach(([i, b]) => b.setAttribute('aria-pressed', String(!!(mm && mm.sec === +i))));
    P.tum.setAttribute('aria-pressed', String(!mod));
    // tür süzgeci: seçimdeki kategoriler (üçgen sayısıyla)
    P.tur.classList.toggle('on', !!mm && !DISIPLIN);                         // disiplin düğmeli sayfada sol menü yalnız montaj ağacı
    if (mm && !DISIPLIN) {
      const say = new Map();
      for (const r of kayit) {
        if (![...r.varMek].some(x => mm.mek.has(x))) continue;
        for (let t = 0; t < r.n; t++) if (mm.mek.has(r.mek[t])) say.set(r.kat[t], (say.get(r.kat[t]) || 0) + 1);
      }
      P.tur.textContent = '';
      P.tur.append(el('span', null, 'TÜR'));
      const h = el('button', null, 'Hepsi'); h.type = 'button'; h.setAttribute('aria-pressed', String(!mm.kat.size)); h.onclick = () => katSec(-1); P.tur.append(h);
      KAT_SUZGEC.forEach(kod => {
        const i = KATL.findIndex(x => x.kod === kod); if (i < 0 || !say.get(i)) return;
        const b = el('button', null, (KATL[i].ad || kod)); b.type = 'button';
        const ak = mm.kat.has(i); b.setAttribute('aria-pressed', String(ak));
        if (ak) { b.style.background = KAT_RENK[i % KAT_RENK.length]; b.style.borderColor = KAT_RENK[i % KAT_RENK.length]; }
        b.title = (KATL[i].icerik || '') + ' · ' + say.get(i).toLocaleString('tr-TR') + ' üçgen';
        b.onclick = () => katSec(i); P.tur.append(b);
      });
    }
  }

  // ------------------------------------------------------------------ "Ön kapaklar" kaydırıcısı: tam solda kapak takımları tamamen gizli
  document.addEventListener('input', async e => {
    const k = e.target; if (!k || k.type !== 'range' || !((k.title || '').includes('metal kapak'))) return;
    const yeni = +k.value <= 0; if (yeni === kapakGizli) return;
    kapakGizli = yeni; await bekle(); guncelle();
  }, true);
  // ------------------------------------------------------------------ istasyon kartları + 3B tıklama
  function kartlar() {
    document.querySelectorAll('.secim a[data-k]').forEach(a => {
      if (a.dataset.mekKur) return; a.dataset.mekKur = '1';
      a.style.cursor = 'pointer'; a.title = 'tıkla: istasyon alt montajını aç';
      a.addEventListener('click', e => {
        e.preventDefault();
        const ist = D.istasyon.filter(s => s.modul.indexOf(a.dataset.k) >= 0).map(s => s.kod);
        if (ist.length) { istasyonAc(ist); odakla(ist[0]); }
      });
    });
  }
  let bas = null, surukle = false;
  mv.addEventListener('pointerdown', e => { bas = [e.clientX, e.clientY]; surukle = false; });
  mv.addEventListener('pointermove', e => { if (bas && Math.hypot(e.clientX - bas[0], e.clientY - bas[1]) > 6) surukle = true; });
  function olcuAcik() { return [...document.querySelectorAll('.m3ar button')].some(b => b.classList.contains('on') && /Ölçü/.test(b.textContent)); }
  function isabet(x, y) {
    const sc = sahne(); if (!sc || !sc.getNDC || !sc.hitFromPoint) return null;
    try { const h = sc.hitFromPoint(sc.getNDC(x, y)); return h && h.object && h.object.isMesh ? h : null; } catch (e) { return null; }
  }
  mv.addEventListener('dblclick', async e => {                               // Kemal 2 Eki: ÇİFT tık = istasyonu tam alt montajıyla aç; açıkken tık bir şey gizlemez (gizle/aç sol menüden)
    if (surukle || !D || olcuAcik()) return;
    await bekle();
    if (KAD()) {                                                            // 3 kademe: dükkân → makine (ya da QR / tezgâh) → istasyon
      const k = kademe(); if (k === 'istasyon' || k === 'kapak') return;
      let i = null;
      const h = isabet(e.clientX, e.clientY);
      if (h) {
        const r = kayit.find(x => x.m === h.object);
        if (r && h.faceIndex != null) { const f = r.m.geometry === r.g0 ? h.faceIndex : (r.cur && r.cur.orig ? r.cur.orig[h.faceIndex] : null); if (f != null) i = r.mek[f]; }
      }
      let ist = i != null && LISTE[i] ? LISTE[i].istasyon : null;
      if (!ist && !h) {                                                     // dış kabuk açıkken: malzeme adından birim
        const m = mv.materialFromPoint(e.clientX, e.clientY), rr = m && /^M[A-Z]_(.+?)__/.exec(m.name || ''), b = rr && D.birim[rr[1]];
        if (b) ist = b.split('/')[0];
      }
      if (!ist) return;
      const mak = MAK_IST().indexOf(ist) >= 0;
      if (k === 'dukkan') { if (mak) makineAc(); else if (ist !== 'Çevre') { istasyonAc(ist, true, 'dukkan'); odakla(ist); } }
      else if (k === 'makine' && mak) { istasyonAc(ist, true, 'makine'); odakla(ist); }
      return;
    }
    if (mod && mod.tip === 'mek') return;
    if (mod) return;                                                        // kapak görünümünde tıklama bir şey açmaz
    let istasyon = null;
    const h = isabet(e.clientX, e.clientY);
    if (h) { const r = kayit.find(x => x.m === h.object); if (r && h.faceIndex != null && r.m.geometry === r.g0) istasyon = LISTE[r.mek[h.faceIndex]] && LISTE[r.mek[h.faceIndex]].istasyon; }
    if (!istasyon) {
      const m = mv.materialFromPoint(e.clientX, e.clientY);
      const rr = m && /^M[A-Z]_(.+?)__/.exec(m.name || '');
      const k = rr && D.birim[rr[1]]; if (k) istasyon = k.split('/')[0];
    }
    if (istasyon && istasyon !== 'Çevre') { istasyonAc(istasyon); odakla(istasyon); }
  });
  function odakla(ist) {                                                    // panelde açılan istasyonun ağacı görünsün
    setTimeout(() => { const d = P.det && P.det[ist]; if (d && d.scrollIntoView) d.scrollIntoView({block: 'nearest', behavior: 'smooth'}); }, 60);
  }
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && mod && !/INPUT|TEXTAREA/.test((e.target || {}).tagName || '')) { if (KAD()) geri(); else hepsi(); } });

  // ------------------------------------------------------------------ yükleme
  mv.addEventListener('load', () => setTimeout(() => {
    const sc = sahne();
    const ayni = sc && kayit.length && kayit.every(r => { let o = r.m; while (o.parent) o = o.parent; return o === sc; });
    if (ayni) return;
    hazir = false; kuruluyor = null; kayit = []; mod = null; vurgu.clear(); bildir(); bekle().then(() => { if (P.agac && D) agacKur(); disiplinKur(); });
  }, 350));
  function basla() {
    panelKur();
    fetch(JSON_YOL).then(r => { if (!r.ok) throw Error('mekanizma tablosu yüklenemedi'); return r.json(); }).then(d => {
      D = d; LISTE = d.liste.slice();
      agacKur(); kartlar(); new MutationObserver(kartlar).observe(document.body, {childList: true, subtree: true});
      bekle().then(() => {
        agacKur(); disiplinKur();
        const ks = [...document.querySelectorAll('.m3ar input[type="range"]')].find(e => (e.title || '').includes('metal kapak'));
        if (ks && +ks.value <= 0) { kapakGizli = true; guncelle(); }
        const h = decodeURI((location.hash || '').slice(1));
        if (/^mek=/.test(h)) { const i = LISTE.findIndex(m => m.kod === h.slice(4)); if (i >= 0) mekanizmaSec(i); }
        else if (/^ist=/.test(h)) istasyonAc(h.slice(4).split(','));
        else if (h === 'k=makine' && KAD()) makineAc();
      });
    }).catch(err => { P.agac.innerHTML = '<div class="mk-not">' + err.message + '</div>'; });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', basla); else basla();

  window.MEK3 = {
    bekle, ayarla, hepsi, istasyonAc, mekanizmaSec, makineAc, geri, kademe, gizli: () => [...gizli],
    mod: () => mod, dinle: f => dinleyici.push(f),
    kapakYeri: () => P.kapakYeri,
    _kayit: () => kayit, _liste: () => LISTE, vurgu: () => [...vurgu], disiplinSec
  };
})();
