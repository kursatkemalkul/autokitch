# -*- coding: utf-8 -*-
"""v87 sayfa düzeni (30 Eyl 2026 · Claude) — Kemal: "3d model sayfasını daha büyük yap, üst kısımdaki açıklamayı aşağı taşı, modelin altındaki seçenekleri
sol tarafa koy ama açılır kapanır pencere olsun … tüm alt montajları da düzenle". python sayfa_v87.py <worktree_kok>
· her 3B sayfaya yan-panel.js (model ekran boyunda en üstte, seçenekler solda gizlenir/açılır panelde, başlık + açıklama aşağıda)
· model / durum / parça bağlantıları v87 · istasyon başlıkları güncel sürüm · K sayfası kesme_v8.json · E sayfası kutu_v12.json
· makine.html: hız seçici (1× 2× 5× 10× 20× — fırın gerçek süre) · güncel kart v87"""
import re, sys
from pathlib import Path
KOK = Path(sys.argv[1]); H = KOK / "otonom" / "hat"
YAN = '<script src="yan-panel.js?v=2"></script>'


def oku(ad): return (H / ad).read_text(encoding="utf-8")
def yaz(ad, s): (H / ad).write_text(s, encoding="utf-8")


def rep(s, a, b, n=1):
    assert s.count(a) == n, (a[:90], s.count(a), n)
    return s.replace(a, b)


def ortak(s):
    s = re.sub(r"(\.\./hat3d/modul_[A-Z]\.(?:glb|usdz))\?v=\d+", r"\1?v=87", s)
    s = re.sub(r"(\.\./hat3d/(?:durum|parca_kutulari)\.json)\?v=[\w-]+", r"\1?v=87", s)
    s = re.sub(r"GÜNCEL · MONTAJ v\d+ \([^)]*\)\.", "GÜNCEL · MONTAJ v87 (30 Eyl 2026).", s)
    if "yan-panel.js" not in s:
        s = rep(s, "</body></html>", YAN + "</body></html>")
    return s


# ---------------------------------------------------------------- makine.html ----------------------------------------------------------------
s = oku("makine.html")
s = rep(s, '<span class="tag" style="background:#d94a3a">5430 &times; 909 &times; 1862</span>', '<span class="tag" style="background:#d94a3a">5230 &times; 909 &times; 1862 · montaj v87</span>')
i = s.index('<div class="card" style="border-left:4px solid #d94a3a;background:#fdf3f2;margin:12px 0"><b style="color:#a3281c">GÜNCEL · MONTAJ v71')
j = s.index("</div>", i) + len("</div>")
s = s[:i] + ('<div class="card" style="border-left:4px solid #d94a3a;background:#fdf3f2;margin:12px 0"><b style="color:#a3281c">GÜNCEL · MONTAJ v87 (30 Eyl 2026).</b> '
             '<b>K kesme + sprey (K400, Codex\'in tasarımı) gerçek parçalarla:</b> Festo DGRF-C-63-125 kılavuzlu silindir · Spraying Systems PulsaJet + UniJet TG-W geniş açı nozül bıçak göbeğinde · '
             'SMC MY1B10G rodless iticiler + RB0805 şok emici · Interroll EC5000 bant motoru + Habasit gıda bandı · Omron E3Z fotoseller · Siemens S7-1200 pano · tereyağı tankı (Walther Pilot MDG 3) alt dolapta. '
             '<b>E kutu katlama gerçek sürelerle</b> (her eksen katalog hız sınırında: 1 kutu 32 s). <b>Bulaşık makinesi personel tezgâhının altında,</b> üstünde el yıkama evyesi (S). '
             '<b>Animasyonlar gerçek saniyelerle:</b> çekmece 3,97 s (Transmotec 127 d/dk), robot ≤ 800 mm/s, TOPPING X 200 mm/s, fırın 3,5 dk pişme (6,27 mm/s) — hız düğmeleriyle hızlandır. Hat 5230 × 909 × 1862.</div>') + s[j:]
s = rep(s, '<div class="zc"><button id="oy">duraklat</button><input id="tz" type="range" min="0" max="84" step="0.05" value="0"><span class="sn" id="sn">0,0 / 84 sn</span></div>',
        '<div class="zc"><button id="oy">duraklat</button><input id="tz" type="range" min="0" max="84" step="0.05" value="0"><span class="sn" id="sn">0,0 / 84 sn</span></div>\n'
        '  <div class="zc hz" id="hz"><span style="color:#8d97a4;font:700 12px system-ui,sans-serif">HIZ</span><button data-h="1" class="ak">1×</button><button data-h="2">2×</button><button data-h="5">5×</button><button data-h="10">10×</button><button data-h="20">20×</button><span class="sn" id="hzn">gerçek süre</span></div>')
s = rep(s, "</style></head>", ".zc.hz button.ak{background:#4f86ff;border-color:#4f86ff;color:#fff}</style></head>")
s = rep(s, "Her hareket makinenin kendi kinematiğinden ve dozaj hesabından (topping_v2_hesap_v1) gelir; fırın hızlandırıldı. İstasyon sayfalarında animasyon yok.",
        "Her hareket makinenin kendi kinematiğinden, dozaj hesabından ve motorun katalog hızından gelir — GERÇEK SÜRE (fırın 3,5 dk). İzlerken <b>HIZ</b> düğmeleriyle 2×–20× hızlandır. İstasyon sayfalarında animasyon yok.")
s = rep(s, "<b>Toplam hat</b><span>5430 &times; 909 &times; 1862 mm (montaj v71 · teknik resim HAT ATOSA TABLALI v20)</span>",
        "<b>Toplam hat</b><span>5230 &times; 909 &times; 1862 mm (montaj v87 · K400 · teknik resim HAT ATOSA TABLALI v20 = v71 geometrisi, K 600 iken)</span>")
s = rep(s, "F FIRIN 1500 &middot; K KESME + SPREY 600 &middot; E KUTU 830.", "F FIRIN 1500 &middot; K KESME + SPREY 400 &middot; E KUTU 830.")
s = rep(s, "Personel tezgâhı 600 × 450 × 900: temizlik bidonları, bez / eldiven / poşet, 10 L çöp, kilitli kişisel çekmece; üstünde duvar askısı",
        "Personel tezgâhı v2: altında bulaşık makinesi (MEIKO M-iClean US, kapağı bekleme alanına açılır), üstünde el yıkama evyesi (batarya + termosifon + sabunluk + havluluk), çekmece, temizlik, sarf, çöp; ince duvarda askı")
s = rep(s, "Her hareket makinenin kendi kinematiğinden geliyor; fırın hızlandırıldı (gerçekte ~4 dk).", "Her hareket makinenin kendi kinematiğinden ve motor / katalog hızından geliyor; GERÇEK SÜRE (fırın 3,5 dk) — HIZ düğmeleri.")
s = rep(s, "K kesme_cad_v6 + bulasik_cad_v2 · E kutu_cad_v8 · S qr_cad_v1 + tezgah_cad_v1", "K kesme_cad_v8 · E kutu_cad_v12 · S qr_cad_v1 + tezgah_cad_v2 (+ bulasik_cad_v3)")
s = rep(s, " &middot; bulaşık K'nin içinde; kapağı için önce K alt kapağı açılır, robot x 3868–4808 dışında olmalı (servis modu kilidi)", "")
s = rep(s, "model: arastirma/_uretec/hat_montaj_v71.py &middot; 29 Eyl 2026", "model: arastirma/_uretec/hat_montaj_v87.py &middot; 30 Eyl 2026")
s = rep(s, "  setInterval(() => { if (!mv.paused && mv.loaded) { tz.value = mv.currentTime; goster(mv.currentTime); } }, 150);",
        "  setInterval(() => { if (!mv.paused && mv.loaded) { tz.value = mv.currentTime; goster(mv.currentTime); } }, 150);\n"
        "  const hz = document.getElementById('hz'), hzn = document.getElementById('hzn');                                   // v87: hız (gerçek süre)\n"
        "  if (hz) hz.querySelectorAll('button').forEach(b => b.onclick = () => { const h = +b.dataset.h; mv.timeScale = h;\n"
        "    hz.querySelectorAll('button').forEach(x => x.classList.toggle('ak', x === b)); hzn.textContent = h === 1 ? 'gerçek süre' : h + ' kat hızlı'; });")
s = ortak(s)
yaz("makine.html", s)

# ---------------------------------------------------------------- istasyon sayfaları ----------------------------------------------------------------
for ad in ("store.html", "press.html", "topping_v2.html", "oven.html", "robot.html"):
    yaz(ad, ortak(oku(ad)))

# K
s = oku("kesme.html")
s = rep(s, '<h1>4b · KESME + SPREY — K istasyonu v6<span class="tag" style="background:#d94a3a">600 × 909 × 1862 · kapaklı · bulaşık altta</span></h1>',
        '<h1>4b · KESME + SPREY — K istasyonu v8<span class="tag" style="background:#d94a3a">400 × 909 × 1862 · Festo + PulsaJet · tank alt dolapta</span></h1>')
i = s.index('<div class="card" style="border-left:4px solid #d94a3a;background:#fdf3f2;margin:12px 0">', s.index("<h1>4b"))
j = s.index("</div>", i) + len("</div>")
s = s[:i] + ('<div class="card" style="border-left:4px solid #d94a3a;background:#fdf3f2;margin:12px 0"><b style="color:#a3281c">K v8 · ÜRETİM MODELİ (30 Eyl 2026).</b> '
             'Codex\'in K400 tasarımı (kısa düz itici, bant 220 ön besler, itici 240 kutuya sürer) standart parçalarla: <b>Festo DGRF-C-GF-63-125</b> (gerçek ölçü, 16,5 mm bağlantı plakasıyla köprüye) · '
             '<b>PulsaJet AAB10000AUH-03 + UniJet TG-W 2.8W</b> bıçak göbeğinde dik (gıda sürümü 104210 tam koni uç almıyor) · <b>SMC MY1B10G-250/350</b> + MY-J10 + D-M9N + AS1201F + <b>2 × RB0805</b> · '
             'HIWIN MGN15 · <b>Interroll EC5000</b> + avara · <b>Habasit CD.F20-A-UW</b> · <b>Omron E3Z-T61</b> · tank <b>Walther Pilot MDG 3</b> alt dolapta (üst bölmeye sığmıyor) · '
             '<b>Siemens S7-1200</b> + NDR-240 + SMC SS5Y3 valf adası + AW20. Codex zarfındaki 32 durağan kesişim giderildi; X arabası 9,6 → 4,7 kg. '
             'Süreler katalog sınırından (aşağıda). Denetim: çakışma 0 · havada 0 · ürün yolu temiz.</div>') + s[j:]
s = rep(s, "Parçalar katalog ürünü (Festo, Spraying Systems, Interroll, igus, SMC, Siemens)", "Parçalar katalog ürünü (Festo, Spraying Systems, Interroll, Habasit, SMC, HIWIN, Omron, Siemens, Walther Pilot)")
i = s.index("const ADIM = ["); j = s.index("];", i) + 2
s = s[:i] + "let ADIM = [];" + s[j:]
s = rep(s, "document.getElementById('adim').innerHTML = ADIM.map(a => '<li><b>' + a[1] + '</b> — ' + a[2] + '</li>').join('');   // v65: animasyon yok, sıra metin", "")
i = s.index("fetch('../hat3d/kesme_v6.json?v=6')"); j = s.index("});\n</script>", i) + len("});\n")
s = s[:i] + """fetch('../hat3d/kesme_v8.json?v=87').then(r => r.json()).then(D => {                      // v87: K v8 (üretim modeli)
  const f = (v, n = 1) => (+v).toFixed(n).replace('.', ',');
  document.getElementById('adim').innerHTML = D.adim.map(a => '<li><b>' + f(a.t) + ' s · ' + a.ad + '</b> — ' + a.not_ + '</li>').join('') +
    '<li><b>DÖNGÜ</b> — K istasyon periyodu ' + f(D.dongu, 0) + ' s (K + E bir ürün ' + f(D.dongu_KE) + ' s; E, K saatine göre ' + f(-D.E_basla_K) + ' s önce başlar; robot çatalı ' + D.catal_K.map(c => f(c)).join(' · ') + ' s).</li>';
  const H = D.hesap;
  document.getElementById('hes').innerHTML = '<b>Kesme</b><span>' + H.kesme + '</span><b>Hava</b><span>' + H.hava + '</span><b>Tereyağı</b><span>' + H.yag + '</span>' +
    '<b>İtici</b><span>' + H.itici + '</span><b>Bant</b><span>' + H.bant + '</span><b>Pano</b><span>' + H.pano + '</span><b>Kotlar</b><span>' + H.kot + '</span>' +
    '<b>Açık</b><span>' + D.acik.join(' · ') + '</span>';
  document.getElementById('den').innerHTML += D.denetim.map(d => '<tr><td>' + d.ad + (d.deger ? ' · ' + d.deger : '') + '</td><td><span class="st ' + (d.sonuc === 'GEÇTİ' ? 'ok' : 'ac') + '">' + d.sonuc + '</span></td></tr>').join('');
  const c = document.getElementById('cak'); if (c) c.innerHTML = '<b>' + D.surum + '</b>';
});
""" + s[j:]
s = rep(s, "model: arastirma/_uretec/kesme_cad_v6.py (ön düzlem +79 · 3 kapak · bulaşık tablada) · montaj v69 · 28 Eyl 2026",
        "model: arastirma/_uretec/kesme_cad_v8.py (Codex K400 v7 üstüne üretim modeli) · montaj v87 · 30 Eyl 2026")
yaz("kesme.html", ortak(s))

# E
s = oku("pack.html")
s = rep(s, '<h1>5 · PACK — kutu katlama modülü v7<span class="tag" style="background:#d9b43a">830 × 909 × 1862 · kapaklı · içecek yedeği altta</span></h1>',
        '<h1>5 · PACK — kutu katlama modülü v12<span class="tag" style="background:#d9b43a">830 × 909 × 1862 · 1 kutu 32 s (gerçek) · içecek yedeği altta</span></h1>')
i = s.index("const ADIM = ["); j = s.index("];", i) + 2
s = s[:i] + "let ADIM = [];" + s[j:]
k = s.index("document.getElementById('adim')", s.index("let ADIM = [];"))
kk = s.index("\n", k)
s = s[:k] + """fetch('../hat3d/kutu_v12.json?v=87').then(r => r.json()).then(D => {                    // v87: E v12 gerçek süreler (her eksen katalog sınırında)
  const f = (v, n = 1) => (+v).toFixed(n).replace('.', ',');
  document.getElementById('adim').innerHTML = D.hareket.map(h => '<li><b>' + f(h.t) + ' s · ' + h.eksen + '</b> — ' + f(h.sure, 2) + ' s · tepe ' + f(h.v, 0) + ' ' + h.birim + '/s (sınır ' + f(h.sinir, 0) + ')</li>').join('') +
    '<li><b>DÖNGÜ</b> — ' + f(D.dongu_gercek, 2) + ' s (v11 kinematiğinde ' + f(D.dongu_eski, 1) + ' s idi) · çakışma ' + D.denetim.kesisim + ' · makine↔karton ' + D.denetim.makine_karton +
    ' · kafa↔besleme en kısa ' + f(D.denetim.kafa_besleme_mm, 2) + ' mm · açık: ' + D.acik.join(' · ') + '</li>';
});""" + s[kk:]
yaz("pack.html", ortak(s))

# S
s = oku("service.html")
s = rep(s, '<span class="tag" style="background:#c47c18">QR 860 × 520 × 2050 · tezgâh 600 × 450 × 900</span>',
        '<span class="tag" style="background:#c47c18">QR 860 × 520 × 2050 · tezgâh v2 663 × 830 · bulaşık + el evyesi</span>')
s = rep(s, "qr_cad_v1.py + tezgah_cad_v1.py (+ ray_ek_cad_v1.py) → hat_montaj_v69.py · 28 Eyl 2026", "qr_cad_v1.py + tezgah_cad_v2.py (+ bulasik_cad_v3.py + ray_ek_cad_v1.py) → hat_montaj_v87.py · 30 Eyl 2026")
yaz("service.html", ortak(s))
print("sayfalar güncellendi: makine + 8 istasyon (yan-panel.js, v87 bağlantıları)")

# ---------------------------------------------------------------- dükkân (index.html) ----------------------------------------------------------------
s = oku("index.html")
if "MONTAJ v87" not in s:
    i = s.index('<b style="color:#2456c8">GÜNCEL DURUM · MONTAJ v71'); j = s.index("<br>Sayfalar:", i)
    s = s[:i] + ('<b style="color:#2456c8">GÜNCEL DURUM · MONTAJ v87 (30 Eyl 2026)</b><br>'
                 'Makine <b>5230 × 909 × 1862</b> (K kesme + sprey 600 → <b>400</b>, Codex\'in K400 tasarımı): K gerçek parçalarla — Festo DGRF-C-63-125 kesici, PulsaJet sprey nozülü bıçak göbeğinde, '
                 'SMC rodless iticiler + şok emici, Interroll bant motoru, Habasit gıda bandı, tereyağı tankı alt dolapta. E kutu katlama gerçek sürelerle (1 kutu 32 s). '
                 '<b>Bulaşık makinesi artık personel tezgâhının altında</b> (MEIKO M-iClean US, kapağı bekleme alanına açılır); tezgâhın üstünde el yıkama evyesi + batarya + termosifon, duvarda sabunluk ve havluluk. '
                 'Sipariş animasyonları <b>gerçek saniyelerle</b> (fırın 3,5 dk) — MAKİNE sayfasında hız düğmeleri. Altta tek parça çekmeceli soğuk dolap (0–4000); üstünde A 700 · C 1800 · F 1500; yanında K 400 · E 830. '
                 'Tek Fairino FR5 yer rayında; koridorun karşısında S: QR dolabı + personel tezgâhı v2. Dükkân iç <b>570 × 271</b>.') + s[j:]
    s = rep(s, "(montaj v71 · 543 × 90,9 × 186 cm ·", "(montaj v87 · 523 × 90,9 × 186 cm ·")
    s = rep(s, "MAKİNE 543 × 90,9 × 186: altta tek parça çekmeceli dolap 400 × 78,8; üstünde A açıcı 70 · C TOPPING 180 · F fırın 150; K kesme 60 · E kutu 83 yerden tavana.",
            "MAKİNE 523 × 90,9 × 186 (v87): altta tek parça çekmeceli dolap 400 × 78,8; üstünde A açıcı 70 · C TOPPING 180 · F fırın 150; K kesme 40 · E kutu 83 yerden tavana.")
    s = rep(s, "personel tezgâhı 60 × 45 × 90 ·", "personel tezgâhı v2 66 × 83 (altında bulaşık makinesi, üstünde el evyesi) ·")
    s = rep(s, "<td>önünde ince duvara 390 mm kalıyor (tek kapak 41° açılır), tablası niş duvarına 4 cm biniyor · <a href=\"service.html#tezgah\">TEZGÂH</a></td>",
            "<td>v2: bulaşık makinesi tezgâhın altında, üstte el evyesi; tezgâh niş cebini doldurur (x 384–450) · <a href=\"service.html#tezgah\">TEZGÂH</a></td>")
    s = rep(s, "<td>önce K alt kapağı açılır; robot x 3868–4808 arasındayken kapak açılmaz (servis modu kilidi)</td>",
            "<td>v87: bulaşık K'dan çıktı, personel tezgâhının altında; kapağı bekleme alanı tarafına (−x) açılır, robot koridoruyla ilişkisi yok</td>")
    s = rep(s, "name:'MAKİNE v71 · gerçek üretim modeli (QR dolabı, personel tezgâhı, robot + ray dahil)'", "name:'MAKİNE v87 · gerçek üretim modeli (QR dolabı, personel tezgâhı v2 + bulaşık, robot + ray dahil)'")
    s = rep(s, "Üretici: arastirma/_uretec/dukkan_plani15.py</figcaption>",
            "Üretici: arastirma/_uretec/dukkan_plani15.py. <b>Not (v87):</b> bu çizim v64 geometrisini gösterir — hat artık 523 (K 400), bulaşık personel tezgâhının altında; 3B sahne günceldir.</figcaption>")
    s = rep(s, "· 28 Eyl 2026 · montaj v69 · dükkân v15</div>", "· 30 Eyl 2026 · montaj v87 · dükkân v15 (3B güncel)</div>")
    s = re.sub(r"(\.\./hat3d/parca_kutulari\.json)\?v=[\w-]+", r"\1?v=87", s)
    yaz("index.html", s)
    print("index.html (dükkân) güncellendi")

# ---------------------------------------------------------------- K sayfası: gerekçe + "ne nerede" (v8) ----------------------------------------------------------------
s = oku("kesme.html")
if "K v8 · NEDEN BÖYLE" not in s:
    i = s.index('<div class="card" style="border-left:4px solid #2456c8;background:#f4f7fd;margin:14px 0"><b style="color:#2456c8">NEDEN BÖYLE')
    j = s.index('<h2>2 · Hesap (modelden)</h2>', i)
    s = s[:i] + '''<div class="card" style="border-left:4px solid #2456c8;background:#f4f7fd;margin:14px 0"><b style="color:#2456c8">K v8 · NEDEN BÖYLE · TASARIM GEREKÇESİ</b><br>
<b>Neden bant:</b> fırın bandı PTFE (kayganlık ≈ 0,15), düz çelik plaka ≈ 0,35 — ürün plakada durur, arkası fırında kalır. Kesme yeri kısa bir gıda bandı (üstü 996, fırın bandının 2 mm altı); iki bant da tahrikli, aktarma güvenilir (Q-T-S PC5000 aynı ilke).<br>
<b>Neden bıçak bandı kesmiyor:</b> DGRF strok sonunda bıçak bandın 0,5 mm üstünde; kesim yükünü bandın altındaki UHMW kayma tablası ve 2 travers taşır.<br>
<b>Neden K400 (Codex'in tasarımı):</b> bant ürünü 220 mm ileri taşır (ön kenarı E'ye girer), kısa düz itici arkadan boşalan yere girer ve 240 mm kutuya sürer; eksenler 400 mm modüle sığar, bulaşık makinesi K'dan çıkıp personel tezgâhının altına gitti.<br>
<b>Neden şok emici:</b> X arabasında Z ekseni taşınır (4,7 kg). SMC MY1B10'un lastik tamponu bu kütlede ancak 100 mm/s altını kaldırır (katalog s. 8-11-19) — silindirin alt hız sınırı 100 → iki uçta RB0805 şok emici (1,0 J). Z (1,4 kg) tamponla çalışır ama 2,9 s'de gider.<br>
<b>Neden PulsaJet -03:</b> gıda sürümü 104210 yalnız düz fan uç alır; duran yuvarlak ürüne göbekten tek nozülle püskürtmek için tam koni gerekir → UniJet uç alan -03 gövdesi + TG-W 120° (gıda uygunluğu üreticiye sorulacak).<br>
<b>Neden tank altta:</b> 3 L sınıfında teyitli paslanmaz basınçlı tank Walther Pilot MDG 3 (Ø173 × 454) üst bölmeye (388 mm) sığmıyor; alt dolap bulaşık çıkınca boş kaldı — damlama tavasında, ısıtıcı ceketli; ısıtmalı hortum arkadan kafaya.<br>
<b>Neden çit:</b> kutu ekseni z −206; ürün −170'te gelir, eğik giriş çiti onu 36 mm içeri kaydırır (modelde ürün yolu çite göre hesaplanır).</div>

<h2>1 · Makine — ne nerede</h2>
<div class="card"><div class="kv">
<b>K bandı</b><span><b>Interroll RollerDrive EC5000 AI ø50 IP66</b> 24 V 35 W 49:1 (0,02–0,37 m/s, anma 2,42 N·m, motor rulonun içinde) + avara ø50 · <b>Habasit CD.F20-A-UW</b> 2 mm beyaz TPU (EU 10/2011 + FDA, min kasnak Ø25) 380 geniş · UHMW kayma tablası · POM çitler (braketli) · ölü plaka · 2 çift <b>Omron E3Z-T61</b> karşılıklı ışın (giriş x 105 · duruş x 350)</span>
<b>Kesici</b><span><b>Festo DGRF-C-GF-63-125-PPV-A-R</b> (katalog ölçüsü: boyunduruk 162 × 81 × 20, gövde 105, silindir 75 × 75, miller Ø25 / 125): 16,5 mm bağlantı plakasına 4 × M10 + 2 × ZBH-12, plaka arka köprü kirişine 2 × M8 · adaptör Ø170 → 3 ara dikme Ø16 × 70 → kafa plakası → yıldız bıçak Ø296 × 6 · koruma halkası · 2 × SMT-8M sensör</span>
<b>Sprey (aynı kafa)</b><span><b>Spraying Systems PulsaJet AAB10000AUH-03-EPR</b> (24 V 0,36 A, ≤ 7 bar) kafa plakasının üstünde DİK, <b>UniJet TG-W 2.8W</b> tam koni 120° + CP1325 somunu göbekten aşağı bakar · silikon ısıtıcı ceket · M8 90° kablo · ısıtmalı hortum (strok boyunca serbest halka)</span>
<b>Tereyağı sistemi</b><span>ALT dolapta <b>Walther Pilot MDG 3</b> (3,2 L / 2,5 L kullanılır, paslanmaz) damlama tavasında · ısıtıcı ceket 150 W + PT100 · regülatör + manometre · emniyet valfi · seviye sensörü · ısıtmalı Ø6 gıda hortumu arkadan (x 380) SKINTOP rakorla istasyon tabanından geçer, köprünün altından kafaya</span>
<b>İtici</b><span><b>SMC MY1B10G-250</b> (X) + <b>MY1B10G-350</b> (Z) merkezi borulu rodless · <b>MY-J10</b> yüzer bağlantı · 4 × D-M9N · 4 × AS1201F · <b>2 × RB0805</b> şok emici · <b>HIWIN MGN15</b> ray + MGN15H blok (X ve Z) · X arabası 6082 cepli (4,7 kg) · POM itici yüzü (pasif 15 mm yüzer)</span>
<b>Pano (arka duvarda, üstte)</b><span><b>Siemens S7-1200 CPU 1214C DC/DC/DC</b> (14 DI / 10 DO / 2 AI · Q0.0 PWM → PulsaJet) · <b>Mean Well NDR-240-24</b> · 2 × Omron E5DC + 2 × G3PE SSR (tank + hortum ısısı) · C10 sigorta · klemens</span>
<b>Hava</b><span>hattın ana hava dalı fırın üstü kabinden K'nın sol duvarındaki rakora (y 1809) → <b>SMC AW20-F02-A</b> (5 µm) → <b>SMC SS5Y3-20-04</b> valf adası + 3 × SY3120 (X · Z · kesici) + kör plaka · DGRF Ø6, X Ø4, tank Ø6 hortumları (Z'ninki X arabasıyla gider — spiral hortum [V])</span>
<b>Malzeme listesi</b><span><a href="../hat3d/kesme_v8_bom.csv">kesme_v8_bom.csv</a> (modeldeki kalemler, kaynaklı; teyit edilmeyenler [V])</span>
</div></div>

''' + s[j:]
    yaz("kesme.html", s)
    print("kesme.html gerekçe + ne nerede v8")

# ---------------------------------------------------------------- S sayfası: tezgâh v2 ----------------------------------------------------------------
s = oku("service.html")
if "Personel tezgâhı v2 (tezgah_cad_v2" not in s:
    i = s.index('<h2 id="tezgah">2 · Personel tezgâhı (tezgah_cad_v1)</h2>'); j = s.index('<h2>3 · Robot kablosu', i)
    s = s[:i] + '''<h2 id="tezgah">2 · Personel tezgâhı v2 (tezgah_cad_v2 + bulasik_cad_v3 · 30 Eyl 2026)</h2>
<div class="card"><div class="kv">
<b>Yer</b><span>ön zondaki niş cebini doldurur: x 3842–4505 · z 1044–1874 (ince duvar ile sokak duvarı arası), QR dolabının solunda. Kemal: "bulaşık makinesini personel tezgâhının altına koy, tezgâhı ona göre ayarla, üstüne elini yıkamak için küçük evye".</span>
<b>Bulaşık makinesi</b><span><b>MEIKO M-iClean US</b> (460 × 600 × 700, sepet 400 × 400, giriş 315) tezgâhın altında; ön yüzü bekleme alanına (−x) bakar, kapak açılınca x 3402–3857 arasını kullanır. Bağlantıları (su, tahliye, elektrik) tezgâhın arkasında.</span>
<b>El yıkama evyesi</b><span>küçük paslanmaz hazne (300 × 300 × 150) tablada · <b>GROHE 36271000</b> batarya · tezgâh altında <b>Stiebel Eltron EIL 3 Premium</b> anlık su ısıtıcı · sifon · sokak duvarında <b>Tork S4</b> sabunluk ve <b>Tork H2</b> havluluk.</span>
<b>Çekmece + bölmeler</b><span>çekmece (strok 500) · temizlik, sarf, çöp bölmeleri · ince duvarda askı.</span>
<b>Denetim</b><span>tezgah_cad_v2: 14/14 GEÇTİ (97 parça, bulaşık zarfı, kapak açılma zarfı, evye ↔ ısıtıcı ↔ bulaşık çakışması 0).</span>
</div></div>
''' + s[j:]
    s = s.replace("(qr_cad_v1 + tezgah_cad_v1 + ray ekleri)", "(qr_cad_v1 + tezgah_cad_v2 + bulaşık + ray ekleri)")
    k = s.find("<tr><td>Tezgâh önü 390 mm</td>")
    if k >= 0:
        kk = s.index("</tr>", k) + len("</tr>")
        s = s[:k] + '<tr><td>Bulaşık kapağı (tezgâh v2)</td><td><span class="st ac">AÇIK</span></td><td>Kapak bekleme alanına açılır (x 3402–3857): yıkama sırasında o bölge boş olmalı — kullanım kuralı Kemal\'de.</td></tr>' + s[kk:]
    yaz("service.html", s)
    print("service.html tezgâh v2")
