/* AUTOKITCH hat/yan-panel.js v2 (30 Eyl 2026 · v2: hız şeridi Oynatma'da) — Kemal: "3d model sayfasını daha büyük yap, üst kısımdaki açıklamayı aşağı taşı,
   modelin altındaki seçenekleri sol tarafa koy ama açılır kapanır pencere olsun: sol köşeye basarsam gizlensin, açılsın".
   Her 3B sayfada (makine + istasyon sayfaları) aynı düzen:
     · model sahnesi sayfanın en üstünde, üst çubuğun hemen altında, ekran boyunda ve tam genişlikte;
     · modelin altındaki bütün seçenek şeritleri (kesit / ölçü / ön kapaklar · kenar çizgileri · dış kabuk · sipariş · oynatma · adımlar)
       SOLDA bir panelde; panel modelin sol üst köşesindeki düğmeyle gizlenir / açılır (tercih tarayıcıda hatırlanır);
     · sayfa başlığı ve açıklamalar sahnenin ALTINDA.
   Sayfanın kendi betikleri değişmez: düğmeler ve şeritler yalnız yerinden taşınır (id'leri, olayları aynen kalır). */
(function () {
  'use strict';
  const ANAHTAR = 'ak_yan_panel_kapali';
  const CSS = [
    '.sahne{display:flex;position:relative;width:100%;height:calc(100vh - var(--ust-h,50px));min-height:520px;background:#15181d;overflow:hidden}',
    '.yan{flex:0 0 340px;width:340px;height:100%;overflow-y:auto;background:#1b1f26;border-right:1px solid #2a3039;color:#dce3ea;transition:margin-left .25s ease,transform .25s ease;z-index:6}',
    '.sahne.kapali .yan{margin-left:-341px}',
    '.yan-ic{padding:10px 0 28px}',
    '.yan-bas{padding:4px 16px 12px 16px;color:#eef2f6;font:700 14.5px/1.35 system-ui,sans-serif}',
    '.yan-bas b{font:inherit}.yan-bas .tag{display:inline-block;margin:6px 0 0;font-size:11.5px}',
    '.yan-grp{border-top:1px solid #2a3039;padding:10px 0 4px}.yan-grp.bos{display:none}',
    '.yan-grp h3{margin:0 16px 8px;color:#8d97a4;font:700 11.5px system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase}',
    '.sahne .m3{flex:1 1 auto;min-width:0;width:auto;height:100%;margin:0}',
    '.sahne .m3 model-viewer{height:100%;min-height:0}',
    '.sahne .m3 .et{left:66px}',
    '.yan .zc,.yan .sip,.yan .adim,.yan .anlat,.yan .m3ar{background:transparent;border-top:0;padding:2px 16px 8px}',
    '.yan .m3ar{flex-direction:column;align-items:stretch;gap:10px}',
    '.yan .m3ar .grp{flex-wrap:wrap}.yan .m3ar input[type=range]{flex:1 1 140px;width:auto;min-width:120px}',
    '.yan .zc input[type=range]{flex:1 1 150px}',
    '.yan .ip{position:static;display:block;padding:2px 16px 6px;color:#6d7682;font-size:11.5px;line-height:1.4}',
    '.yan .anlat{min-height:0;font-size:13.5px}',
    '.yan .secim{flex-direction:column;padding:0 16px;margin:0}',
    '.yan .secim a{flex:none;background:#232932;border-color:#2f3742;color:#e6ebf0;font-size:13px}',
    '.yan .secim a span{color:#8d97a4}',
    '.yan-dugme{position:absolute;left:12px;top:12px;z-index:7;padding:7px 11px;border:1px solid #39424f;border-radius:9px;background:rgba(27,31,38,.92);color:#e6ebf0;font:700 14px/1 system-ui,sans-serif;cursor:pointer}',
    '.yan-dugme:hover{border-color:#4f86ff;color:#fff}',
    '@media (max-width:760px){.yan{position:absolute;left:0;top:0;bottom:0;width:min(340px,88vw);flex-basis:auto}',
    '.sahne.kapali .yan{margin-left:0;transform:translateX(-101%)}.sahne .m3 .et{left:14px;top:56px;max-width:80%}}'
  ].join('\n');
  (function () { const s = document.createElement('style'); s.id = 'yan-panel-css'; s.textContent = CSS; document.head.appendChild(s); })();
  function oku() { try { return localStorage.getItem(ANAHTAR); } catch (e) { return null; } }
  function yaz(v) { try { localStorage.setItem(ANAHTAR, v); } catch (e) {} }

  function kur() {
    const ust = document.querySelector('.top');
    if (ust) document.documentElement.style.setProperty('--ust-h', ust.offsetHeight + 'px');
    const m3 = document.querySelector('.m3');
    if (!m3 || m3.closest('.sahne')) return;
    const wrap = m3.closest('.wrap') || document.querySelector('.wrap');
    const sahne = document.createElement('div'); sahne.className = 'sahne'; sahne.id = 'sahne';
    const yan = document.createElement('aside'); yan.className = 'yan'; yan.id = 'yan'; yan.setAttribute('aria-label', 'Model seçenekleri');
    const ic = document.createElement('div'); ic.className = 'yan-ic'; yan.appendChild(ic);

    // başlık: sayfanın h1'i (etiketiyle) panelin tepesine kısa hali
    const h1 = document.querySelector('.wrap h1');
    const bas = document.createElement('div'); bas.className = 'yan-bas';
    if (h1) {
      const kopya = h1.cloneNode(true); kopya.removeAttribute('id');
      bas.innerHTML = '<b>' + kopya.innerHTML + '</b>';
    }
    ic.appendChild(bas);

    function bolum(baslik, sinif) {
      const s = document.createElement('section'); s.className = 'yan-grp' + (sinif ? ' ' + sinif : '');
      if (baslik) { const h = document.createElement('h3'); h.textContent = baslik; s.appendChild(h); }
      ic.appendChild(s); return s;
    }
    const gGorunum = bolum('Görünüm'), gArac = bolum('Kesit · ölçü · ön kapaklar', 'arac');
    const gSip = bolum('Sipariş'), gOyn = bolum('Oynatma');
    const gDiger = bolum('');

    // .m3 içindeki seçenek şeritlerini panele taşı (model, etiket, AR, ölçü katmanı yerinde kalır)
    const KALIR = el => el.tagName === 'MODEL-VIEWER' || el.classList.contains('et') || el.classList.contains('ar') ||
                        el.classList.contains('m3olc') || el.classList.contains('yan-dugme') || el.classList.contains('simv') ||
                        el.tagName === 'svg' || el.tagName === 'SVG' || el.tagName === 'CANVAS' || el.tagName === 'SCRIPT';
    function yerlestir(el) {
      if (KALIR(el)) return;
      if (el.classList.contains('m3ar')) { gArac.appendChild(el); return; }
      if (el.classList.contains('ip')) { gDiger.appendChild(el); return; }
      if (el.id === 'sip' || el.classList.contains('sip')) { gSip.appendChild(el); return; }
      if (el.classList.contains('adim') || el.classList.contains('anlat') || el.classList.contains('hz') || (el.classList.contains('zc') && el.querySelector('#oy'))) { gOyn.appendChild(el); return; }
      if (el.classList.contains('zc')) { gGorunum.appendChild(el); return; }
      gDiger.appendChild(el);
    }
    Array.prototype.slice.call(m3.children).forEach(yerlestir);
    // model3d araç çubuğu model yüklenince eklenir → geldiği an panele al
    new MutationObserver(ms => ms.forEach(m => Array.prototype.slice.call(m.addedNodes).forEach(n => { if (n.nodeType === 1 && n.parentNode === m3) yerlestir(n); })))
      .observe(m3, { childList: true });
    // makine sayfasının istasyon seçimi (varsa) panelin sonuna
    const secim = document.getElementById('secim');
    if (secim) { const g = bolum('İstasyonlar'); g.appendChild(secim); }

    // sahneyi üst çubuğun hemen altına al; başlık + açıklamalar aşağıda kalır
    if (wrap && wrap.parentNode) wrap.parentNode.insertBefore(sahne, wrap); else m3.parentNode.insertBefore(sahne, m3);
    sahne.appendChild(yan); sahne.appendChild(m3);
    const bos = () => Array.prototype.slice.call(ic.querySelectorAll('.yan-grp')).forEach(s => s.classList.toggle('bos', s.children.length <= (s.querySelector('h3') ? 1 : 0)));
    bos(); new MutationObserver(bos).observe(ic, { childList: true, subtree: true });

    // sol üst köşe düğmesi: gizle / aç
    const d = document.createElement('button'); d.type = 'button'; d.className = 'yan-dugme'; d.id = 'yanDugme';
    m3.appendChild(d);
    function durum(kapali) {
      sahne.classList.toggle('kapali', kapali);
      d.innerHTML = kapali ? '&#9776;&nbsp;Seçenekler' : '&#8249;';
      d.title = kapali ? 'seçenek panelini aç' : 'seçenek panelini gizle';
      d.setAttribute('aria-expanded', String(!kapali));
      yaz(kapali ? '1' : '0');
      setTimeout(() => window.dispatchEvent(new Event('resize')), 280);
    }
    d.onclick = () => durum(!sahne.classList.contains('kapali'));
    const kayit = oku();
    durum(kayit === null ? window.matchMedia('(max-width: 760px)').matches : kayit === '1');
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', kur); else kur();
})();
