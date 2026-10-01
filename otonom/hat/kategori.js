/* v1 · MONTAJ KATEGORİLERİ (Kemal 30 Eyl 2026): "dış kabuk deyince diğerlerini gizleyecek, elektrik tesisatı deyince sadece kabloları gösterecek,
   iki tane seçtiğimi birlikte gösterecek … bir elektrikçiye ya da servo motorları ayarlayacak firmaya bu kısmı atarım".
   Montaj (hat_montaj_v91+) her parçanın üçgen aralığını kategorisiyle GLB'ye yazar: primitive extras "kat" = [kategori, ilk indis, indis sayısı, …],
   sahne extras "kategoriler" = liste. Seçim yoksa her şey görünür; seçilen kategorilerin üçgenleri gösterilir (konumlar paylaşılır, yalnız indis değişir),
   kenar çizgileri seçime göre yeniden hesaplanır (önbellekli). "Sadece dış kabuk" ile aynı anda açık kalmaz. Animasyon, kesit, ölçü, etiket çalışır. */
(() => {
  'use strict';
  const mv = document.getElementById('mv'), kutu = document.getElementById('kat-dugmeler'), durum = document.getElementById('kat-durum');
  if (!mv || !kutu) return;
  const YEDEK = [['GOVDE', 'Gövde'], ['MEKANIZMA', 'Mekanizma'], ['MOTOR', 'Motor + sürücü'], ['GIDA', 'Gıda hattı'], ['HAVA', 'Hava (pnömatik)'], ['SOGUTMA', 'Soğutma'],
                 ['GUC', 'Elektrik güç'], ['KONTROL', 'Kontrol (beyin)'], ['ROBOT', 'Robot'], ['URUN', 'Ürün + sarf'], ['DUKKAN', 'Dükkân']].map(([kod, ad]) => ({kod, ad}));
  const RENK = ['#8f99a6', '#c9a227', '#7b61d6', '#d94a3a', '#2f8fd8', '#1fa3a0', '#e07b20', '#2f9e44', '#f08c00', '#a47551', '#6c757d'];
  const ESIK = Math.cos(30 * Math.PI / 180), Q = 1e4;
  let liste = YEDEK, kayit = [], secim = new Set(), dugmeler = new Map(), hazir = false, is = 0;
  const sahne = () => mv[Object.getOwnPropertySymbols(mv).find(s => s.description === 'scene')];
  const yaz = t => { if (durum) durum.textContent = t; };

  // kenar-cizgi.js ile AYNI kural (> 30° keskin + açık kenar) — yalnız verilen indislerin üçgenleri
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
  function altGeo(r, S) {
    const src = r.g0.index.array; let n = 0;
    for (let i = 0; i < r.k.length; i += 3) if (S.has(r.k[i])) n += r.k[i + 2];
    const out = new src.constructor(n); let o = 0;
    for (let i = 0; i < r.k.length; i += 3) if (S.has(r.k[i])) { out.set(src.subarray(r.k[i + 1], r.k[i + 1] + r.k[i + 2]), o); o += r.k[i + 2]; }
    const g = new r.g0.constructor();
    for (const ad of Object.keys(r.g0.attributes)) g.setAttribute(ad, r.g0.attributes[ad]);
    g.setIndex(new r.g0.index.constructor(out, 1));
    g.boundingBox = r.g0.boundingBox; g.boundingSphere = r.g0.boundingSphere;
    return {geo: g, ind: out, kenar: null};
  }
  function cizgi(r) { return r.m.children.find(c => c.userData && c.userData.kenarCizgi) || null; }

  function kur() {
    if (hazir || !mv.loaded) return;
    const sc = sahne(); if (!sc) return;
    const bul = []; let lst = null;
    sc.traverse(o => {
      if (!lst && o.userData && Array.isArray(o.userData.kategoriler)) lst = o.userData.kategoriler;
      if (!o.isMesh || !o.geometry || !o.geometry.index || (o.userData && (o.userData.kenarCizgi || o.userData.yalitimKesit))) return;
      const k = o.geometry.userData && o.geometry.userData.kat;
      if (!Array.isArray(k) || !k.length) return;
      const v = [...new Set(k.filter((_, i) => i % 3 === 0))].sort((a, b) => a - b);
      bul.push({m: o, g0: o.geometry, k, var: v, tam: v.join(','), onbellek: new Map(), cz0: undefined, benGizledim: false});
    });
    if (!bul.length) { yaz('Bu modelde kategori bilgisi yok (montaj v91 ve sonrası).'); return; }
    if (lst) liste = lst;
    kayit = bul; hazir = true;
    const say = new Map();
    for (const r of kayit) for (let i = 0; i < r.k.length; i += 3) say.set(r.k[i], (say.get(r.k[i]) || 0) + r.k[i + 2] / 3);
    kutu.textContent = ''; dugmeler.clear();
    const tum = document.createElement('button'); tum.type = 'button'; tum.textContent = 'Hepsi'; tum.title = 'Bütün kategoriler (seçimi temizle)';
    tum.onclick = () => { secim.clear(); guncelle(); };
    kutu.append(tum); dugmeler.set(-1, tum);
    liste.forEach((c, i) => {
      if (!say.get(i)) return;
      const b = document.createElement('button'); b.type = 'button'; b.textContent = c.ad || c.kod;
      b.title = (c.icerik ? c.icerik : '') + (c.kime ? ' · kime: ' + c.kime : '') + ' · ' + Math.round(say.get(i)).toLocaleString('tr-TR') + ' üçgen';
      b.dataset.kat = i; b.onclick = () => { if (secim.has(i)) secim.delete(i); else secim.add(i); guncelle(); };
      kutu.append(b); dugmeler.set(i, b);
    });
    boya(); yaz(kayit.length + ' ağ · ' + (dugmeler.size - 1) + ' kategori · seçim yok (hepsi görünür)');
  }
  function boya() {
    for (const [i, b] of dugmeler) {
      const ak = i === -1 ? secim.size === 0 : secim.has(i);
      b.setAttribute('aria-pressed', ak ? 'true' : 'false');
      b.style.background = ak ? (i === -1 ? '#d94a3a' : RENK[i % RENK.length]) : '';
      b.style.borderColor = ak ? (i === -1 ? '#d94a3a' : RENK[i % RENK.length]) : '';
      b.style.color = ak ? '#fff' : '';
    }
  }
  async function guncelle() {
    if (!hazir) return;
    const dk = document.getElementById('dis-kabuk');
    if (secim.size && dk && dk.getAttribute('aria-pressed') === 'true') dk.click();            // dış kabuk görünümünü önce kapat (geometriyi o geri yükler)
    boya();
    const S = secim, benim = ++is, sc = sahne();
    let hesap = 0;
    for (const r of kayit) {
      const cz = cizgi(r);
      if (cz && r.cz0 === undefined) r.cz0 = r.m.geometry === r.g0 ? cz.geometry : null;
      if (!S.size) {
        r.m.geometry = r.g0; if (r.benGizledim) { r.m.visible = true; r.benGizledim = false; }
        if (cz) { if (r.cz0 === null) r.cz0 = kenarGeo(r, r.g0.index.array); if (r.cz0) cz.geometry = r.cz0; }
        continue;
      }
      const key = r.var.filter(c => S.has(c)).join(',');
      if (!key) { if (r.m.visible) { r.m.visible = false; r.benGizledim = true; } continue; }
      if (r.benGizledim) { r.m.visible = true; r.benGizledim = false; }
      if (key === r.tam) {
        r.m.geometry = r.g0;
        if (cz) { if (r.cz0 === null) r.cz0 = kenarGeo(r, r.g0.index.array); if (r.cz0) cz.geometry = r.cz0; }
        continue;
      }
      let c = r.onbellek.get(key);
      if (!c) { c = altGeo(r, S); r.onbellek.set(key, c); }
      r.m.geometry = c.geo;
      if (cz) {
        if (!c.kenar) {
          c.kenar = kenarGeo(r, c.ind);
          if (++hesap % 6 === 0) { yaz('kenar çizgileri hesaplanıyor…'); if (sc && sc.queueRender) sc.queueRender(); await new Promise(res => setTimeout(res, 0)); if (benim !== is) return; }
        }
        cz.geometry = c.kenar;
      }
    }
    if (sc && sc.queueRender) sc.queueRender();
    yaz(S.size ? 'Gösterilen: ' + [...S].sort((a, b) => a - b).map(i => (liste[i] && (liste[i].ad || liste[i].kod)) || i).join(' + ') : 'seçim yok (hepsi görünür)');
  }
  // "Sadece dış kabuk" açılmadan ÖNCE kategori seçimi temizlenir (iki görünüm aynı ağları değiştirir)
  document.addEventListener('click', e => {
    const dk = e.target && e.target.closest && e.target.closest('#dis-kabuk');
    if (dk && secim.size && dk.getAttribute('aria-pressed') !== 'true') { secim.clear(); guncelle(); }
  }, true);
  // 'load' aynı model için ikinci kez gelebilir → ağlar hâlâ sahnedeyse seçim korunur; model değiştiyse eski kayıtlar bırakılır, yeniden kurulur
  mv.addEventListener('load', () => setTimeout(() => {
    const sc = sahne();
    const ayni = sc && kayit.length && kayit.every(r => { let o = r.m; while (o.parent) o = o.parent; return o === sc; });
    if (ayni) return;
    hazir = false; kayit = []; secim.clear(); kur();
  }, 300));
  const zaman = setInterval(() => { kur(); if (hazir) clearInterval(zaman); }, 400);
})();
