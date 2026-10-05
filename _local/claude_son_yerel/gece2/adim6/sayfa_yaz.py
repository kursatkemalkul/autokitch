# -*- coding: utf-8 -*-
"""adım 6 · istasyon montaj sayfaları (K kabuk montajı sayfasıyla aynı arayüz) → <W>/otonom/hat/<ist>-montaj.html"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
WT = r'C:/Users/Kemal/Desktop/Kemal/WEBSİTE/AUTOKITCH_COORDINATION/worktrees/claude-hat3-v8'
SAY = {
    'a': ('A Montajı', 'A · HAMUR AÇMA — kabuk + açıcı montajı', 'h3_a_sac_v1',
          "A istasyonunun üretim sacı gövdesi (kaynaklı kaide, iskelet, 4 bükümlü panel, çift cidarlı kapak) atölyede hangi sırayla, hangi yönden, neyle birleşir; sonra satın alınan açıcı (dönme kafası) kaidedeki M8 PEM'lere oturur. A içine kablo / hava girmez."),
    'b': ('B Montajı', 'B · ÇEKMECELİ SOĞUK DOLAP — gövde + çekmece montajı', 'h3_b_sac_v1',
          "B dolabının sandviç gövdesi (alt şase → dış kabuk → iç kabuk + bölmeler → PU köpükleme → ön çerçeve) ve ardından soğutma, elektrik kutusu, kanallar, kablolar, çekmece rayları, çekmeceler ve ürün."),
    'e': ('E Montajı', 'E · KUTU KATLAMA — gövde + mekanizma montajı', 'h3_e_sac_v1',
          "E istasyonunun üretim sacı gövdesi (kaynaklı kaide, taban, ön kasa, yan / arka / üst saclar) ve ardından şarjör, asansör, besleyici, kutu katlama mekanizmaları, elektrik kutusu, kablolar, hava, kapaklar ve ürün."),
    'topping': ('TOPPING Montajı', 'TOPPING · MALZEME SERPME — gövde + soğuk oda + dozaj montajı', 'h3_topping_sac_v1',
                "TOPPING istasyonunun üretim sacı gövdesi (menfezli kaide, dış kabuk, soğuk oda astarı + raflar, PU köpük, sökülür arka servis sacı) ve ardından soğutma grubu + evaporatörler, elektrik, valf adası, 4 UNO, kaşar + sucuk kasetleri, tabla + X ekseni ve kanatlar."),
    'f': ('F Montajı', 'F · FIRIN — davlumbaz, baca, ön kapaklar + TP10 yerleşimi', 'h3_f_sac_v1',
          "F'nin üretim sacı parçaları (davlumbaz atış kanalı, çift cidarlı baca, iki ön kapak) ve ardından satın alınan TP10 fırının yerine oturması, yükleme bandı, F kutusu + kablolar, kompresör + hava ve kapaklar. F üst kabin sacı U sayfasında, F kaidesi yok (B tavanına oturur)."),
    'u': ('U Montajı', 'U · ÜST KABİNLER — U_F, U_KE, F üst kabini + ana pano', 'h3_u_sac_v1',
          "Hattın üst kabinleri: F üstündeki U_F (ana pano burada), K + E üstündeki U_KE ve F'nin üst kabini (davlumbaz bölmesi, panjur, taban yalıtımı). Önce sac kabuklar, sonra ana pano, kanallar, kablolar, havalandırma ve yedek stok."),
}
CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sayfa.css'), encoding='utf-8').read()
for ist, (baslik, h1, uretec, lead) in SAY.items():
    html = f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{baslik}</title>
<link rel="icon" href="data:,"><link rel="stylesheet" href="hat.css?v=12">
<script type="importmap">{{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}}}</script>
<style>
{CSS}</style></head><body data-ist="{ist}">
<div class="top"><div class="in"><div class="crumb"><a href="../">Store</a><span>&rsaquo;</span><a href="index.html">HAT</a><span>&rsaquo;</span><a href="makine_v3_8.html">Makine v3</a><span>&rsaquo;</span><b>{ist.upper()} montajı</b></div><div><a href="makine_v3_8.html">&larr; Makineye dön</a></div></div></div>
<div class="wrap"><h1>{h1}<span class="tag" style="background:#c47c18">üretim sacı v1 · adım adım</span></h1>
<p class="lead">{lead}</p>
<p class="ist">Diğer istasyonlar: <a href="a-montaj.html">A</a> · <a href="b-montaj.html">B</a> · <a href="topping-montaj.html">TOPPING</a> · <a href="f-montaj.html">F</a> · <a href="e-montaj.html">E</a> · <a href="u-montaj.html">U</a></p>
<div class="km" id="km"><div class="yuk" id="yuk">Model yükleniyor…</div>
  <div class="acn" id="acn"><div class="sec" id="acnsec"></div><svg id="acnsvg" xmlns="http://www.w3.org/2000/svg"></svg><div class="bil" id="acnbil"></div></div>
  <div class="no" id="no"></div>
  <div class="kamtus"><button id="kam" aria-pressed="true" title="Kamera adımı takip etsin">Kamera: otomatik</button></div>
  <div class="olay" id="olay"></div></div>
<div class="zc"><button id="geri" aria-label="Önceki adım">&#9664;&#9664;</button><button id="oy" aria-label="Oynat / duraklat">&#10074;&#10074;</button><button id="ileri" aria-label="Sonraki adım">&#9654;&#9654;</button>
  <input id="tz" type="range" min="0" max="100" step="0.01" value="0" aria-label="Zaman"><span class="sn" id="sn">0,0 / 0 sn</span></div>
<div class="zc" id="hz"><span class="et">HIZ</span><button data-h="0.5">0,5×</button><button data-h="1" class="ak">1×</button><button data-h="2">2×</button><button data-h="4">4×</button>
  <span class="et" style="margin-left:8px">GÖRÜNÜM</span><button id="kenar" aria-pressed="true">Kenar çizgileri</button>
  <span class="kes"><button id="kesit" aria-pressed="false">Kesit</button><select id="kesx" aria-label="Kesit ekseni" style="min-height:34px;border-radius:8px"><option value="x">X</option><option value="y">Y</option><option value="z" selected>Z</option></select><input id="kesd" type="range" min="0" max="1" step="0.002" value="0.5" style="width:120px" aria-label="Kesit konumu"></span></div>
<div class="adim" id="adim"></div>
<div class="kart"><h2 id="bas"></h2><p id="met"></p><div class="ls" id="lis"></div>
<div class="ren"><span><i style="background:#cfd4da"></i>sac</span><span><i style="background:#c8893a"></i>kaynak dikişi</span><span><i style="background:#6c7480"></i>bağlantı elemanı</span><span><i style="background:#9aa3ad"></i>mekanizma</span><span><i style="background:#d0262b"></i>güç kablosu</span><span><i style="background:#2463c9"></i>bilgi kablosu</span><span><i style="background:#1f9d55"></i>hava</span><span><i style="background:#f2c94c"></i>PU köpük</span><span><i style="background:#d9a35b"></i>ürün</span></div>
<div class="dog" id="dog"></div></div>
<h2>Atölye sırası</h2>
<ol id="sira" style="font-size:13.5px;color:#44505c;padding-left:20px"></ol>
<p class="note" id="dis" style="font-size:13px;color:#68758a"></p>
</div>
<div class="foot">AUTOKITCH &middot; {ist.upper()} montajı v1 &middot; model: gece2/adim5/{ist.upper()}_sac_v1.glb ({uretec}) + hat3_v8zq (gövde dışı parçalar) &middot; 4 Eki 2026 · yerel</div>
<script type="module" src="ist_montaj/ist-montaj.js?v=1"></script>
</body></html>
'''
    open(os.path.join(WT, 'otonom', 'hat', '%s-montaj.html' % ist), 'w', encoding='utf-8', newline='\n').write(html)
    print('yazıldı', ist)
