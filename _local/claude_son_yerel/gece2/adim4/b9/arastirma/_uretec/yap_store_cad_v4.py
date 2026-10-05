# -*- coding: utf-8 -*-
"""store_cad_v3 -> v4 (25 Eyl 2026): ALT TABAN ÇİZGİSİ 123
Kemal: "en alt çekmecenin altında gereksiz bir alan var; o alanı kaldır, en alt çekmecenin altında yalnız kalınlığı ver,
en alt taban çizgisini bulmuş olursun; sağdaki istasyonların alt tabanını ona hizala" → "yap".
  · Çekmeceler YERİNDE (robot kotları, raylar, kapasite aynı). Yalıtımlı taban (1,5 sac + 39 PU + 1 sac = 41,5) en alt
    çekmece önünün 3 mm altına çıkar (3 = önler arası aralık): Y_TABAN = 167,5 − 3 = 164,5 · Y_PLINT = 164,5 − 41,5 = 123.
    Kalkan: tabanla en alt çekmece önü arasındaki 46 mm'lik boş çerçeve bandı. Ayak + süpürgelik 0–123.
  · K4 alt bölmesi SICAK (yoğuşturucu): altına yalıtım gerekmiyor → orada taban yalnız dış sac (123–124,5), Secop ünitesi
    128,5'e oturur (v3: 125,5) → depo ve niş kotları 3 mm oynar, 5 L bidonlar sığar. Yalıtımlı taban K1–K3 altında biter,
    ucu kademe sacıyla kapanır; K4 arkasında arka PU + iç sac, sağda yan iç sac tabana iner. Havalandırma kovanı gereksiz (PU yok).
  · K4 soğutma kapağının alt kenarı çekmece önleriyle aynı çizgiye gelir (167,5).
  · Denetim: alt taban çizgisi, taban–çekmece aralığı, K4 bidon payı ölçülüp assert edilir; kapalı + açılma yolu taraması.
  · BOM 1_STORE_v7.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "store_cad_v3.py"), encoding="utf-8").read()


def degis(a, b):
    global s
    assert s.count(a) == 1, "YOK/COK (%d): %s" % (s.count(a), a[:90])
    s = s.replace(a, b, 1)


degis('''"""AUTOKITCH · B ÇEKMECE MODÜLÜ — ÜRETİM MODELİ v3 (25 Eyl 2026)''',
      '''"""AUTOKITCH · B ÇEKMECE MODÜLÜ — ÜRETİM MODELİ v4 (25 Eyl 2026)
v4: ALT TABAN ÇİZGİSİ 123 (Kemal) — yalıtımlı taban en alt çekmecenin 3 mm altına çıktı, gövde yerden 123'te başlar;
    K4 sıcak bölmesinin altı tek sac. Çekmeceler yerinde. Önceki: store_cad_v3.py''')
degis('''Y_PLINT, Y_TABAN, Y_TAVAN = 80.0, 121.5, 1000.0''',
      '''TABAN_T = 41.5                         # yalıtımlı taban: dış sac 1,5 + PU 39 + iç sac 1,0
Y_TABAN = YUZ0 - FUGA                  # v4: 164,5 — en alt çekmece önünün (167,5) 3 mm altı (v3: 121,5)
Y_PLINT = Y_TABAN - TABAN_T            # v4: 123 = ALT TABAN ÇİZGİSİ, bütün istasyon gövdeleri buradan başlar (v3: 80)
Y_TAVAN = 1000.0''')
degis('''             bom=("Ayarlı ayak Elesa+Ganter LV.A-SST · M12", 6, "paslanmaz AISI 304 · taban Ø40", "elesa-ganter.com LV.A-SST") if i == 0 else None)''',
      '''             bom=("Ayarlı ayak Elesa+Ganter LV.A-SST · M12", 6, "paslanmaz AISI 304 · taban Ø40 · yükseklik 123 (v4)", "elesa-ganter.com LV.A-SST · 123'e uygun diş boyu katalogdan seçilecek") if i == 0 else None)''')
degis('''        ekle("yan_ic_sac_" + ad_, kut(ic_x[0], ic_x[1], Y_TABAN, Y_TAVAN, Z_ARKA, -1.5), "sac", B)''',
      '''        ekle("yan_ic_sac_" + ad_, kut(ic_x[0], ic_x[1], Y_TABAN if ad_ == "sol" else Y_PLINT + 1.5, Y_TAVAN, Z_ARKA, -1.5), "sac", B)   # v4: sağda K4 sıcak bölmesinin tabanına iner''')
degis('''    ekle("taban_pu", kut(29.0, W_ - 29.0, Y_PLINT + 1.5, Y_TABAN - 1.0, -DZ + 1.5, -1.5).cut(kut(VENT[0] - 20, VENT[1] + 20, Y_PLINT, Y_TABAN, VENT[2] - 20, VENT[3] + 20)), "pu", B)
    ekle("taban_ic_sac", kut(X_IC0, X_IC1, Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -1.5).cut(kut(VENT[0], VENT[1], Y_TABAN - 2, Y_TABAN + 1, VENT[2], VENT[3])), "sac", B)
    ekle("taban_vent_kovani", kut(VENT[0] - 20, VENT[1] + 20, Y_PLINT + 1.5, Y_TABAN - 1.0, VENT[2] - 20, VENT[3] + 20).cut(kut(VENT[0], VENT[1], Y_PLINT, Y_TABAN, VENT[2], VENT[3])), "sac", "B_SOGUTMA",
         bom=("Yoğuşturucu hava çıkış kovanı", 1, "304 1,0 · PU'yu kapatır", "sıcak hava plinte"))''',
      '''    # v4: yalıtımlı taban yalnız K1–K3 (soğuk kolonlar) altında; K4 sıcak bölmesinde taban = dış sac (delikli), PU yok → kovan gereksiz
    ekle("taban_pu", kut(29.0, K4X - 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, -DZ + 1.5, -1.5), "pu", B)
    ekle("taban_ic_sac", kut(X_IC0, K4X - 1.0, Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -1.5), "sac", B)
    ekle("taban_k4_kademe_saci", kut(K4X - 1.0, K4X, Y_PLINT + 1.5, Y_TABAN, Z_ARKA, -1.5), "sac", B,
         bom=("Taban kademe sacı 1,0", 1, "304 · yalıtımlı tabanın K4 tarafındaki ucunu kapatır", "v4: K4 sıcak bölmesi 40 mm alçak"))''')
degis('''    ekle("arka_ic_sac", kut(X_IC0, X_IC1, Y_TABAN, Y_TAVAN, Z_ARKA - 1.0, Z_ARKA), "sac", B)''',
      '''    ekle("arka_ic_sac", kut(X_IC0, X_IC1, Y_TABAN, Y_TAVAN, Z_ARKA - 1.0, Z_ARKA), "sac", B)
    # v4: K4 sıcak bölmesi tabana kadar iner → arka PU ve iç sac orada da tabana iner
    ekle("arka_pu_k4_alt", kut(K4X - 1.0, W_ - 29.0, Y_PLINT + 1.5, Y_TABAN - 1.0, -DZ + 1.5, Z_ARKA - 1.0), "pu", B)
    ekle("arka_ic_sac_k4_alt", kut(K4X, X_IC1, Y_PLINT + 1.5, Y_TABAN, Z_ARKA - 1.0, Z_ARKA), "sac", B)''')
degis('''    cx0, cy0, cz1 = kx0 + 25.0, Y_TABAN + 4.0, Z_CER0 - 10.0''',
      '''    cx0, cy0, cz1 = kx0 + 25.0, Y_PLINT + 1.5 + 4.0, Z_CER0 - 10.0            # v4: ünite sıcak bölmenin tek sac tabanında (128,5)''')
degis('''    print("B CEKMECE MODULU v3 · %d parca · %d cekmece" % (len(PARCALAR), len(CEK)))''',
      '''    print("B CEKMECE MODULU v4 · %d parca · %d cekmece" % (len(PARCALAR), len(CEK)))
    # v4 · ALT TABAN ÇİZGİSİ (katılardan ölçülür)
    yb = lambda ad: [p for p in PARCALAR if p["ad"] == ad][0]["wp"].val().BoundingBox()
    alt = yb("taban_dis_sac").ymin
    ic_ust = yb("taban_ic_sac").ymax
    on_alt = min(p["wp"].val().BoundingBox().ymin for p in PARCALAR if p["ad"].endswith("_on_dis_sac_1.5") and p["grup"] == "CEKMECE")
    k4_alt = yb("k4_kapak_sogutma_dis_sac").ymin
    govde_alt = min(p["wp"].val().BoundingBox().ymin for p in PARCALAR if not p["ad"].startswith(("ayak_", "plint_on")))
    bidon = max(yb("bidon_5L_0").ymax, yb("bidon_5L_1").ymax)
    print("ALT TABAN CIZGISI: govde alti %.1f (en alcak govde parcasi %.1f) · ic taban ustu %.1f · en alt cekmece onu %.1f (aralik %.1f) · K4 kapagi alti %.1f · bidon ustu %.1f / tavan %.1f"
          % (alt, govde_alt, ic_ust, on_alt, on_alt - ic_ust, k4_alt, bidon, Y_TAVAN))
    assert abs(alt - 123.0) < 0.05 and abs(govde_alt - alt) < 0.05, "govde alti 123 degil"
    assert abs(on_alt - ic_ust - FUGA) < 0.05 and abs(k4_alt - on_alt) < 0.05, "on alt kenarlari hizali degil"
    assert bidon <= Y_TAVAN - 3.0, "K4 nisinde bidon tavana degiyor"''')
degis('''(r"^(yan_pu_(sol|sag)|arka_pu_37\\.5|taban_pu|bolme_\\d_pu|k1_teknik_raf_pu_38|k4_ara_pu)$", "PU köpük gövde"),''',
      '''(r"^(yan_pu_(sol|sag)|arka_pu_37\\.5|arka_pu_k4_alt|taban_pu|bolme_\\d_pu|k1_teknik_raf_pu_38|k4_ara_pu)$", "PU köpük gövde"),''')
degis('''    print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v6")))''',
      '''    print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v7")))''')
io.open(os.path.join(U, "store_cad_v4.py"), "w", encoding="utf-8").write(s)
print("store_cad_v4.py yazildi")
