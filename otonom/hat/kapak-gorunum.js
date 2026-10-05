/* kapak-gorunum.js · v1 (1 Eki 2026) — "YALNIZ KAPAKLAR" görünümü (makine_v3.html)
   Kemal: "sadece kapakları gösteren bir gizleme modu ekle".
   Gösterilen: ön kapaklar, kanatlar, servis kapakları, düşer kapaklar, çekmece önleri, QR göz kapıları + bunların menteşe / basaç /
   gazlı yay / TIP-ON parçaları. Kablo kanalı kapakları, ray örtüleri, kutu (karton) kapağı, kapak motoru / sensörü gösterilmez.
   Kaynak: GLB "kpk" etiketi (montaj yap_mek_v1 sonrası) ya da ../hat3d/v3/mekanizma_v3.json "kapak" aralıkları; saydam ön kapak
   malzemesi (…__on_seffaf) her zaman kapaktır. Açıkken ön kapaklar metal (opak) yapılır, kapanınca kaydırıcı eski değerine döner.
   Motor mekanizma-v3.js (window.MEK3); bu dosya yalnız düğmeyi kurar. */
(() => {
  'use strict';
  function kur() {
    const M = window.MEK3;
    if (!M || !M.kapakYeri || !M.kapakYeri()) { setTimeout(kur, 200); return; }
    const b = document.createElement('button');
    b.type = 'button'; b.id = 'kapaklar'; b.textContent = 'Kapaklar';
    b.title = 'yalnız kapakları göster (ön kapaklar · kanatlar · servis / düşer kapaklar · çekmece önleri) — tekrar bas: geri';
    b.setAttribute('aria-pressed', 'false');
    b.onclick = () => {
      const m = M.mod();
      if (m && m.tip === 'kapak') M.hepsi(); else M.ayarla({tip: 'kapak'});
    };
    M.dinle(m => b.setAttribute('aria-pressed', String(!!(m && m.tip === 'kapak'))));
    M.kapakYeri().appendChild(b);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', kur); else kur();
})();
