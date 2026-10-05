# -*- coding: utf-8 -*-
"""topping_uno_cad_v18 → v19 (30 Eyl 2026 · YEREL · Claude).
Kemal: "tamam önerdiğini yap toppinge" (evaporatörü soğuk odadan çıkar, soğutma grubunun tam üstüne, arka kuru bölmeye; delik tabanda değil arka duvarda).
  · SOĞUK ODADAN KALKAN: evaporatör gövdesi + yarıklı kapak + lamel paketi + 2 fan + damlama tavası + tahliye hortumu (+ duvar deliği) + elektrikli buharlaştırma kabı +
    soğutma hatları + hat geçiş bloğu (+ duvar deliği) → hepsi topping_cad_v31'in KURU BÖLMEDEKİ yalıtımlı kasetinde
  · KASET YUVASI (plug-in): arka dış sac kasetin önünde 496 × 338 KESİK · PU'nun açık yüzü ABS 1,5 (sacla aynı düzlem) → kutuyla kaset arasında metal ısı köprüsü yok
  · 2 POM HAVA KANALI arka duvarı boydan geçer (üst: üfleme · alt: dönüş) · iç yüzde yarıklı paslanmaz ızgara, iç kaplamayla AYNI DÜZLEMDE (çıkıntı yok)
Yalnız okur: topping_uno_cad_v18.py · yazar: topping_uno_cad_v19.py"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v18.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a), n)
    s = s.replace(a, b)


def blok(bas, son, yeni):
    """bas'tan (dahil) son'a (hariç) kadar olan bölümü yeni ile değiştirir"""
    global s
    assert s.count(bas) == 1, ("bas", bas[:90], s.count(bas))
    i = s.index(bas)
    assert s.count(son, i) >= 1, ("son", son[:90])
    j = s.index(son, i)
    s = s[:i] + yeni + s[j:]


# ---------------------------------------------------------------- 0 · başlık
degis('"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v18 · 29 Eyl 2026 gece · YEREL (',
      '"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v19 · 30 Eyl 2026 · YEREL (v18 + EVAPORATÖR KUTUDAN ÇIKTI → KURU BÖLMEDE YALITIMLI KASET (topping_cad_v31) · '
      'ARKA DUVARDA 2 POM HAVA KANALI + YARIKLI IZGARA · yap_topping_uno_cad_v19.py)\n'
      'v19: Kemal 30 Eyl "önerdiğini yap": evaporatör, fanlar, tava, tahliye, hatlar, elektrikli kap soğuk odadan kalktı → grubun tam üstünde kuru bölmede kaset ·\n'
      '    arka dış sac kasetin önünde kesik (PU yüzü ABS, metal köprü yok) · üst kanal üfler (tavan boyunca kapağa) · alt kanal döner (haznelerin üstünden) · tabanda delik yok\n'
      'v18: topping_uno_cad_v18 · 29 Eyl 2026 gece · YEREL (')

# ---------------------------------------------------------------- 1 · soğutma bölümü: evaporatör + hatlar + tahliye + elektrikli kap → kaset yuvası + 2 kanal + 2 ızgara
YENI_3C = '''# ================================================================ 3c · v19 · SOĞUTMA: EVAPORATÖR KUTUDAN ÇIKTI → KURU BÖLMEDE YALITIMLI KASET (topping_cad_v31)
#   v19 (Kemal 30 Eyl: "önerdiğini yap"): evaporatör + kapak + fanlar + damlama tavası + tahliye hortumu + hatlar + hat bloğu + elektrikli buharlaştırma kabı SOĞUK
#   ODADAN KALKTI → kuru bölmede, soğutma grubunun TAM ÜSTÜNDE yalıtımlı kaset (topping_cad_v31 · dünya x 1470–2010 · y 1473–1855 · z −826…−630). Kaset arka duvara
#   TAKILIR (plug-in, monoblok düzeni): arka dış sac kasetin önünde KESİLİR, kutunun 57,5 PU'su kasetin ön yalıtımı olur (arada metal yok → ısı köprüsü yok), PU'nun
#   kesikte açıkta kalan yüzü ABS 1,5 ile kaplı (sacla aynı düzlem). İki POM hava kanalı PU'yu boydan geçer: ÜST kanal kasetten ÜFLER (tavan boyunca kapağa),
#   ALT kanal DÖNÜŞ (haznelerin üstünden, dolumda 15 kalkınca bile açık) · tabanda delik yok, kanal yok, mile değmez · soğuk odadan yalnız 2 düz yarıklı ızgara görünür
#   v18 (tarihçe): evaporatör sağ üstte odanın İÇİNDE 400 × 208 × 500 · hatlar arka duvar bloğundan · yoğuşma suyu hortumla kuru bölmedeki elektrikli kaba
KASET_KESIK = (xu(1492.0), xu(1988.0), yu(1495.0), yu(1833.0))                        # arka dış sac kesiği (dünya x 1492–1988 · y 1495–1833) · kasetin POM çerçevesi kesiğin iki yanına basar
AGIZ = {"ust": (xu(1520.0), xu(1900.0), yu(1682.0), yu(1792.0)), "alt": (xu(1520.0), xu(1900.0), yu(1540.0), yu(1662.0))}   # kanal DIŞ ölçüsü (dünya x 1520–1900 · üst y 1682–1792 · alt 1540–1662)
KANAL_ET = 3.0                                                                        # POM-C kanal cidarı (ısı köprüsü yok: yalnız soğuk iç kaplamaya ve PU'ya değer)
IZ_YARIK = dict(boy=68.0, en=6.0, hatve=8.0, kolon=5, ara=6.0, pay=5.0)               # ızgara yarığı 68 × 6 · hatve 8 (ara 2 = 2 × sac) · 5 kolon (ara 6) · kenar payı 5
IZGARA_ACIK = {}                                                                      # mm² · yarık açık alanı (topping_cad_v31 hava hızını fan debisiyle buradan hesaplar)
KUTU["soguk_arka_dis_sac"] = KUTU["soguk_arka_dis_sac"].cut(kut(*KASET_KESIK, Z_BOLME[1] - 1.0, Z_BOLME[1] + T_DIS + 1.0))
_abs = kut(*KASET_KESIK, Z_BOLME[1], Z_BOLME[1] + T_DIS)
for _k, (_x0, _x1, _y0, _y1) in AGIZ.items():
    kutu_delik(kut(_x0, _x1, _y0, _y1, Z_BOLME[1] - 1.0, Z_BOLME[0] + 1.0), ("soguk_ic_kaplama", "yalitim_blogu"))
    _abs = _abs.cut(kut(_x0, _x1, _y0, _y1, Z_BOLME[1] - 1.0, Z_BOLME[1] + T_DIS + 1.0))
    _kn = kut(_x0, _x1, _y0, _y1, Z_BOLME[1], Z_BOLME[0]).cut(kut(_x0 + KANAL_ET, _x1 - KANAL_ET, _y0 + KANAL_ET, _y1 - KANAL_ET, Z_BOLME[1] - 1.0, Z_BOLME[0] + 1.0))
    ekle("arka_hava_kanali_%s" % _k, _kn, "pom", "V",
         not_="v19 · hava kanalı POM-C %.0f cidar · %.0f × %.0f dış (geçit %.0f × %.0f) · arka duvarı boydan geçer (z −630…−570) · PU köpüklenirken kalıp: köpük kanalın dış yüzüne yapışır, "
              "iç kaplama kanala silikonla · metal değil → soğuk hava ile kuru bölme arasında köprü yok · %s"
              % (KANAL_ET, _x1 - _x0, _y1 - _y0, _x1 - _x0 - 2 * KANAL_ET, _y1 - _y0 - 2 * KANAL_ET,
                 "ÜST kanal: kasetten ÜFLEME (tavan boyunca kapağa)" if _k == "ust" else "ALT kanal: DÖNÜŞ (haznelerin üstünden kasete)"))
    _gi0, _gi1, _gj0, _gj1 = _x0 + KANAL_ET, _x1 - KANAL_ET, _y0 + KANAL_ET, _y1 - KANAL_ET
    _iz = kut(_gi0, _gi1, _gj0, _gj1, Z_SOGUK[1] - T_IC, Z_SOGUK[1])                     # iç kaplamayla AYNI DÜZLEM (z −571…−570)
    _Y = IZ_YARIK
    _gw = _Y["kolon"] * _Y["boy"] + (_Y["kolon"] - 1) * _Y["ara"]
    _nr = int((_gj1 - _gj0 - 2.0 * _Y["pay"] - _Y["en"]) // _Y["hatve"]) + 1
    _ry0 = _gj0 + ((_gj1 - _gj0) - ((_nr - 1) * _Y["hatve"] + _Y["en"])) / 2.0
    _rx0 = _gi0 + ((_gi1 - _gi0) - _gw) / 2.0
    assert _rx0 - _gi0 >= _Y["pay"] - 0.01, ("ızgara kenar payı", _rx0 - _gi0)
    for _c in range(_Y["kolon"]):
        for _r in range(_nr):
            _xa = _rx0 + _c * (_Y["boy"] + _Y["ara"]); _ya = _ry0 + _r * _Y["hatve"]
            _iz = _iz.cut(kut(_xa, _xa + _Y["boy"], _ya, _ya + _Y["en"], Z_SOGUK[1] - T_IC - 1.0, Z_SOGUK[1] + 1.0))
    IZGARA_ACIK[_k] = _Y["kolon"] * _nr * _Y["boy"] * _Y["en"]
    ekle("arka_hava_izgarasi_%s" % _k, _iz, "paslanmaz", "V",
         not_="v19 · %s ızgarası AISI 304 1,0 · %.0f × %.0f · lazer yarık %.0f × %.0f hatve %.0f · %d kolon × %d sıra = %d yarık · açık alan %.0f mm² · iç kaplamayla AYNI DÜZLEM "
              "(z −571…−570, odaya çıkıntı yok) · kanalın içindeki 4 kulakçığa 4 × M4 (sökülür, bulaşıkta yıkanır)"
              % ("ÜST (üfleme)" if _k == "ust" else "ALT (dönüş)", _gi1 - _gi0, _gj1 - _gj0, _Y["boy"], _Y["en"], _Y["hatve"], _Y["kolon"], _nr, _Y["kolon"] * _nr, IZGARA_ACIK[_k]))
ekle("arka_duvar_kaset_yuzu", _abs, "pom", "V",
     not_="v19 · kaset yuvası yüzü ABS 1,5 (beyaz) · arka dış sacın %.0f × %.0f kesiğini doldurur (sacla aynı düzlem, z −630…−628,5) · PU'ya köpükle yapışık · 2 kanal ağzı · "
          "kasetin POM çerçevesi kesiğin kenarına basar (conta) → kaset içi soğuk hava ile kutu PU'su arasında metal yok"
          % (KASET_KESIK[1] - KASET_KESIK[0], KASET_KESIK[3] - KASET_KESIK[2]))
'''
blok("# ================================================================ 3c · v16/v18 · SOĞUTMA: EVAPORATÖR KUTUNUN İÇİNDE", "for _k, _mal, _not in (", YENI_3C)

# kutu parça notları
degis('tabanı raf · kovan / blok / tahliye delikleri"),', 'tabanı raf · kovan / blok delikleri · v19: 2 hava kanalı ağzı (ızgara aynı düzlemde)"),')
degis('4 kaset + 4 UNO kovanı + geçiş bloğu + hat bloğu + tahliye delikleri"),', '4 kaset + 4 UNO kovanı + geçiş bloğu · v19: 2 POM hava kanalı (kaset), hat bloğu + tahliye delikleri kalktı"),')
degis('alt sacdan TC tavanına kadar DİKDÖRTGEN · kovan / blok / tahliye delikleri")):',
      'alt sacdan TC tavanına kadar DİKDÖRTGEN · kovan / blok delikleri · v19: kasetin önünde 496 × 338 KESİK (kaset yuvası, PU yüzü ABS)")):')

# ---------------------------------------------------------------- 2 · temas denetimi: evaporatör çiftleri → kanal / ızgara / ABS yüz çiftleri
blok('                ("evaporator_govdesi", "soguk_ic_kaplama"),',
     '                ("kasar_boru_kulagi_sag", "kasar_inis_borusu"),',
     '                ("arka_hava_kanali_ust", "yalitim_blogu"), ("arka_hava_kanali_alt", "yalitim_blogu"), ("arka_hava_kanali_ust", "soguk_ic_kaplama"), ("arka_hava_kanali_alt", "soguk_ic_kaplama"),\n'
     '                ("arka_hava_kanali_ust", "arka_duvar_kaset_yuzu"), ("arka_hava_kanali_alt", "arka_duvar_kaset_yuzu"), ("arka_duvar_kaset_yuzu", "yalitim_blogu"), ("arka_duvar_kaset_yuzu", "soguk_arka_dis_sac"),\n'
     '                ("arka_hava_izgarasi_ust", "arka_hava_kanali_ust"), ("arka_hava_izgarasi_alt", "arka_hava_kanali_alt"),\n')

# ---------------------------------------------------------------- 3 · soğutma denetimleri
YENI_DEN = '''# ---------------------------------------------------------------- v19 · SOĞUK KUTU + SOĞUTMA (evaporatör kuru bölmede · topping_cad_v31 kaseti)
_esk = [p["ad"] for p in P if p["ad"].startswith(("evaporator", "sogutma_", "yogusma_"))]
kontrol("v19 · soğuk odada ve arka duvarda SOĞUTMA PARÇASI YOK (evaporatör, kapak, lamel, fan, damlama tavası, tahliye hortumu, hat + hat bloğu, elektrikli buharlaştırma kabı → topping_cad_v31 kaseti): %d" % len(_esk),
        not _esk, str(_esk[:6]))
_uh_ = [a_.lower() for a_, cx_, hw_, *_r in UNO if cx_ + hw_ / 2.0 > AGIZ["alt"][0] and cx_ - hw_ / 2.0 < AGIZ["alt"][1]]
_hz_ = [bb("%s_hazne_bizim" % a_) for a_ in _uh_]
_kn_ = {k_: bb("arka_hava_kanali_%s" % k_) for k_ in AGIZ}; _iz_ = {k_: bb("arka_hava_izgarasi_%s" % k_) for k_ in AGIZ}
_gc_ = max(p["sh"].BoundingBox().ymax for p in P if p["ad"].endswith("_mil_gecis_kovani") or p["ad"].startswith(("kovan_", "gecis_blogu_yalitim")))
kontrol("v19 · arka duvarda 2 HAVA KANALI (POM %.0f · dünya x %.0f–%.0f · üst y %.0f–%.0f · alt y %.0f–%.0f): duvarı boydan geçer (z %.0f…%.0f) · ızgaralar iç kaplamayla aynı düzlemde (z %.0f…%.0f) · "
        "alt kanal altı %.0f > altındaki hazneler (%s) dolumda 15 kalkınca %.0f · üst kanal üstü %.0f ≤ tavan − 10 (%.0f) · aralarında %.0f mm duvar · en üstteki mil / hortum geçişi %.0f (≥ 100 aşağıda)"
        % (KANAL_ET, AGIZ["ust"][0] + DX_DUNYA, AGIZ["ust"][1] + DX_DUNYA, AGIZ["ust"][2] + DY_DUNYA, AGIZ["ust"][3] + DY_DUNYA, AGIZ["alt"][2] + DY_DUNYA, AGIZ["alt"][3] + DY_DUNYA,
           min(b_.zmin for b_ in _kn_.values()), max(b_.zmax for b_ in _kn_.values()), min(b_.zmin for b_ in _iz_.values()), max(b_.zmax for b_ in _iz_.values()),
           AGIZ["alt"][2] + DY_DUNYA, ", ".join(_uh_), max(b_.ymax for b_ in _hz_) + 15.0 + DY_DUNYA, AGIZ["ust"][3] + DY_DUNYA, TAVAN_A - 10.0 + DY_DUNYA,
           AGIZ["ust"][2] - AGIZ["alt"][3], _gc_ + DY_DUNYA),
        all(abs(b_.zmin - Z_BOLME[1]) < 0.01 and abs(b_.zmax - Z_BOLME[0]) < 0.01 for b_ in _kn_.values())
        and all(abs(b_.zmin - (Z_SOGUK[1] - T_IC)) < 0.01 and abs(b_.zmax - Z_SOGUK[1]) < 0.01 for b_ in _iz_.values())
        and bool(_hz_) and AGIZ["alt"][2] > max(b_.ymax for b_ in _hz_) + 15.0 and AGIZ["ust"][3] <= TAVAN_A - 10.0 and AGIZ["ust"][2] - AGIZ["alt"][3] >= 15.0 and AGIZ["alt"][2] - _gc_ >= 100.0)
_ab_ = bb("arka_duvar_kaset_yuzu"); _rs_ = [p for p in P if p["ad"] == "soguk_arka_dis_sac"][0]["sh"]
_ksk_ = kut(*KASET_KESIK, Z_BOLME[1] - 1.0, Z_BOLME[1] + T_DIS + 1.0).val()
_ksv_ = _rs_.intersect(_ksk_).Volume()
kontrol("v19 · KASET YUVASI: arka dış sac kasetin önünde KESİK (dünya x %.0f–%.0f · y %.0f–%.0f · kesikte sac hacmi %.1f mm³ = 0) · PU'nun açık yüzü ABS 1,5 (z %.1f…%.1f, sacla aynı düzlem) → kasetle kutu arasında "
        "METAL KÖPRÜ YOK · ızgara açık alanı üst %.0f · alt %.0f mm² (hava hızı topping_cad_v31'de fan debisiyle)"
        % (KASET_KESIK[0] + DX_DUNYA, KASET_KESIK[1] + DX_DUNYA, KASET_KESIK[2] + DY_DUNYA, KASET_KESIK[3] + DY_DUNYA, _ksv_, _ab_.zmin, _ab_.zmax, IZGARA_ACIK["ust"], IZGARA_ACIK["alt"]),
        _ksv_ < 0.01 and abs(_ab_.zmin - Z_BOLME[1]) < 0.01 and abs(_ab_.zmax - Z_BOLME[1] - T_DIS) < 0.01 and min(IZGARA_ACIK.values()) > 20000.0)
'''
blok("# ---------------------------------------------------------------- v16 · SOĞUK KUTU + SOĞUTMA", 'for _u in ("sos", "harc"):', YENI_DEN)

# ---------------------------------------------------------------- 4 · boşluk denetimi: kanal geçitleri hava yoludur (kovan içi = mil gibi ölçüm dışı)
degis('startswith(("kovan_", "gecis_blogu_yalitim", "sogutma_hat_gecis_blogu", "raf_askisi_burclari", "evaporator_tahliye_hortumu", "sogutma_emis_hatti", "sogutma_sivi_hatti"))',
      'startswith(("kovan_", "gecis_blogu_yalitim", "raf_askisi_burclari", "arka_hava_kanali_", "arka_hava_izgarasi_", "arka_duvar_kaset_yuzu"))')
_kv = '    _b = _p["sh"].BoundingBox(); _kal = _kal.cut(silz((_b.xmin + _b.xmax) / 2.0, (_b.ymin + _b.ymax) / 2.0, 11.5, _b.zmin - 1.0, _b.zmax + 1.0).val())\n'
degis(_kv, _kv + 'for _ag in AGIZ.values():                                                                              # v19 · hava kanalı geçidi (kasete giden hava yolu, ölçüm dışı)\n'
                  '    _kal = _kal.cut(kut(_ag[0] + KANAL_ET, _ag[1] - KANAL_ET, _ag[2] + KANAL_ET, _ag[3] - KANAL_ET, Z_BOLME[1] - 1.0, Z_BOLME[0] + 1.0).val())\n')

# ---------------------------------------------------------------- 5 · sürüm adları
degis('"topping_uno_cad_v18 denetimi KALDI: %s"', '"topping_uno_cad_v19 denetimi KALDI: %s"')
degis('"generator": "AUTOKITCH topping_uno_cad_v18"', '"generator": "AUTOKITCH topping_uno_cad_v19"')
degis('"topping_uno_v18.glb"', '"topping_uno_v19.glb"')
degis('"topping_uno_v18.json"', '"topping_uno_v19.json"')
degis('surum="topping_uno_cad_v18 · %s"', 'surum="topping_uno_cad_v19 · %s"')

# ---------------------------------------------------------------- 6 · artık referans kalmasın
import re
for _yasak in ("EVAP", "_ex0", "EV_Q", "EV_KOL", "EV_ON_Y", "EV_DON_Z", "EV_ACIK", "TAH_X", "TAHLIYE", "HAT_X", "HAT_GECIS", "HAT_Y_UNITE", "HAT_Z_KURU", "HAT",
               "evaporator_govdesi", "evaporator_kapagi", "yogusma_buharlastirma_kabi", "sogutma_hat_gecis_blogu", "sogutma_emis_hatti", "sogutma_sivi_hatti"):
    _rx = re.compile(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(_yasak))          # yalnız TAM tanımlayıcı (EVAPORATÖR / HATTI gibi sözcükler sayılmaz)
    _kal = [l_ for l_ in s.split('"""', 2)[2].splitlines() if _rx.search(l_) and not l_.lstrip().startswith("#")]   # modül açıklaması (tarihçe) hariç
    assert not _kal, (_yasak, _kal[:3])
compile(s, "topping_uno_cad_v19.py", "exec")
io.open(os.path.join(U, "topping_uno_cad_v19.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v19.py yazıldı · %d satır" % s.count("\n"))
