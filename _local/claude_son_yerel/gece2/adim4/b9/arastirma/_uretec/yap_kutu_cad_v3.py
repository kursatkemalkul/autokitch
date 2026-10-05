# -*- coding: utf-8 -*-
"""kutu_cad_v2 -> v3 (25 Eyl 2026): ALT TABAN ÇİZGİSİ 123
Kemal: "üstte bant istasyonları hizalı, alt taraf da öyle olmalı; en alt çekmecenin altındaki gereksiz alanı kaldır,
diğer istasyonların alt tabanını ona hizala" → "yap".
  · Gövde tabanı 80 → 123 (B: 167,5 çekmece önü − 3 aralık − 41,5 yalıtımlı taban). Üst kenar 2030 ve bütün çalışma
    kotları (besleme 1500, kalıp 1148, tepsi 1104) AYNI; modül alttan 43 mm kısalır.
  · Asansör tahriki (NEMA 23 + GT3 40/20 kasnak + kayış) tabanın ALTINA, ayak boşluğuna iner: kasnaklar 108–121,
    motor 3 mm askı plakasına cıvatalı (2 kulakla tabana), çevresi 1 mm sabit koruyucu (alttan motor geçer).
    Vidanın Ø12 alt ucu tabandaki Ø16 delikten geçip kasnağı taşır. Alt yatak/sensör/platform yerinde → şarjör 567 korunur.
  · Süpürgelik B ile aynı çekilme (60); ön ayaklar süpürgeliğin arkasına (z −110). Dikey kablo kanalı tabandan başlar.
  · Ölçüm: tabanın altında yalnız ayak, süpürgelik ve (koruyuculu) asansör tahriki kalabilir — denetlenir.
  · Çıktı kutu_modulu_v3.glb, BOM 5_PACK_kutu_v3 (eski SolidWorks 5_PACK_v3 klasörüyle karışmasın).
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kutu_cad_v2.py"), encoding="utf-8").read()


def degis(a, b):
    global s
    assert s.count(a) == 1, "YOK/COK (%d): %s" % (s.count(a), a[:90])
    s = s.replace(a, b, 1)


degis('''"""AUTOKITCH · E · KUTU KATLAMA MODÜLÜ — ÜRETİM MODELİ v2 (25 Eyl 2026)''',
      '''"""AUTOKITCH · E · KUTU KATLAMA MODÜLÜ — ÜRETİM MODELİ v3 (25 Eyl 2026)
v3: ALT TABAN ÇİZGİSİ 123 (Kemal): gövde tabanı 80 → 123, asansör tahriki koruyuculu olarak tabanın altına,
    süpürgelik 60 geride. Çalışma kotları aynı, şarjör 567. Önceki: kutu_cad_v2.py''')
degis('''Y_PLINT = 80.0''', '''Y_PLINT = 123.0                 # v3 (Kemal 25 Eyl): ALT TABAN ÇİZGİSİ — bütün istasyon gövdeleri yerden 123'te başlar (v2: 80)
Y_TK = Y_PLINT - 14.0           # v3: asansör kasnak düzlemi tabanın ALTINDA (kasnak 108–121, taban 123–126)''')

degis('''    for i, (ax, az) in enumerate(((60.0, -60.0), (770.0, -60.0), (60.0, -770.0), (770.0, -770.0))):''',
      '''    for i, (ax, az) in enumerate(((60.0, -110.0), (770.0, -110.0), (60.0, -770.0), (770.0, -770.0))):   # v3: ön ayaklar süpürgeliğin arkasında''')
degis('''    taban = kut(SAC, W - SAC, Y_PLINT, Y_PLINT + 3.0, -D + SAC, -SAC).cut(kut(445.0, 515.0, Y_PLINT - 1, Y_PLINT + 4, -425.0, -359.0))   # asansör motoru deliği''',
      '''    taban = kut(SAC, W - SAC, Y_PLINT, Y_PLINT + 3.0, -D + SAC, -SAC).cut(sily(405.0, -392.0, 8.0, Y_PLINT - 1, Y_PLINT + 4))   # v3: yalnız vida alt ucu (Ø12) için Ø16 delik''')
degis('''    ekle("plint_on", kut(40.0, W - 40.0, 10.0, Y_PLINT, -41.5, -40.0), "sac")''',
      '''    ekle("plint_on", kut(40.0, W - 40.0, 10.0, Y_PLINT, -61.5, -60.0), "sac")                # v3: B ile aynı çekilme (60)''')

degis('''    ekle("asansor_vidasi_Tr16x4", sily(405.0, -392.0, 8.0, 150.0, 1125.0), "celik",
         bom=("Trapez vida Tr16×4 (DIN 103) + bronz blok somun", 1, "boy 975 · kendinden kilitli (η≈0,35): güç kesilince yığın düşmez", "katalog"))''',
      '''    ekle("asansor_vidasi_Tr16x4", sily(405.0, -392.0, 8.0, 150.0, 1125.0), "celik",
         bom=("Trapez vida Tr16×4 (DIN 103) + bronz blok somun", 1, "boy 975 + Ø12 alt uç 42 (tabandan geçer, kasnağı taşır) · kendinden kilitli (η≈0,35): güç kesilince yığın düşmez", "katalog"))
    ekle("asansor_vidasi_alt_ucu", sily(405.0, -392.0, 6.0, Y_TK - 1.0, 150.0), "celik")          # v3: işlenmiş Ø12 uç, tabanın altına iner''')

degis('''    pd1 = kasnak("asansor_kasnak_40", 405.0, 120.0, -392.0, 40)
    pd2 = kasnak("asansor_kasnak_20", 480.0, 120.0, -392.0, 20)
    kayis_y("asansor_kayisi", 405.0, -392.0, 480.0, -392.0, 121.0, pd1, pd2)
    nema23("asansor_motoru", (480.0, 118.0, -392.0), (0, 1, 0), (0, 0, 1))''',
      '''    # v3: TAHRİK TABANIN ALTINDA (ayak boşluğu 0–123): kasnaklar Y_TK−1 … Y_TK+12 = 108–121 · kayış 110–119
    pd1 = kasnak("asansor_kasnak_40", 405.0, Y_TK, -392.0, 40)
    pd2 = kasnak("asansor_kasnak_20", 480.0, Y_TK, -392.0, 20)
    kayis_y("asansor_kayisi", 405.0, -392.0, 480.0, -392.0, Y_TK + 1.0, pd1, pd2)
    # motor askı plakası 3 mm (104–107) + iki kulak tabanın altına; NEMA 23 flanşı alttan 4 × M5 · Ø39 pilot deliği
    mp = kut(455.0, 505.0, Y_TK - 5.0, Y_TK - 2.0, -427.0, -357.0).cut(sily(480.0, -392.0, 19.5, Y_TK - 6.0, Y_TK - 1.0))
    mp = mp.union(kut(455.0, 505.0, Y_TK - 2.0, Y_PLINT, -427.0, -424.0)).union(kut(455.0, 505.0, Y_TK - 2.0, Y_PLINT, -360.0, -357.0))
    ekle("asansor_motor_plakasi", mp, "celik", bom=("Motor askı plakası 3 mm", 1, "304 lazer + 2 büküm · tabanın altına 4 × M5 · NEMA 23 flanşı 4 × M5", "v3: tahrik tabanın altında"))
    nema23("asansor_motoru", (480.0, Y_TK - 5.0, -392.0), (0, 1, 0), (0, 0, 1))
    # kayış koruyucu 1 mm: tepesi açık kutu, tabanın altına 4 × M4 · alt yüzünde motor geçiş deliği
    kor = kut(374.0, 516.0, Y_TK - 9.0, Y_PLINT, -430.0, -354.0).cut(kut(375.0, 515.0, Y_TK - 8.0, Y_PLINT + 1.0, -429.0, -355.0))
    kor = kor.cut(kut(450.0, 510.0, Y_TK - 10.0, Y_TK - 7.0, -422.0, -362.0))
    ekle("asansor_kayis_koruyucu", kor, "sac", bom=("Kayış koruyucu 1 mm", 1, "304 büküm · tabanın altına 4 × M4 · kasnaklar ve kayış kapalı, motor alttan geçer", "v3: sabit koruyucu"))''')

degis('''    ekle("kablo_kanali_dikey_alt", kut(801.0, 826.0, 100.0, 1325.0, -50.0, -25.0), "plastik")''',
      '''    ekle("kablo_kanali_dikey_alt", kut(801.0, 826.0, Y_PLINT + 3.0, 1325.0, -50.0, -25.0), "plastik")   # v3: tabandan başlar''')

degis('''    ("ayak_", "taban_sac"),''',
      '''    ("ayak_", "taban_sac"),
    ("motor_plakasi", "_motoru"), ("motor_plakasi", "taban_sac"), ("kayis_koruyucu", "taban_sac"),   # v3: cıvatalı yüzey temasları''')

degis('''    print("ZARF (modul %.0f x %.0f x %.0f, tutamaklar haric): %s" % (W, H, D, "hepsi icinde" if not tasan else "TASAN: " + ", ".join(tasan)))
    assert not tasan, "modul zarfini asan parca var"''',
      '''    print("ZARF (modul %.0f x %.0f x %.0f, tutamaklar haric): %s" % (W, H, D, "hepsi icinde" if not tasan else "TASAN: " + ", ".join(tasan)))
    assert not tasan, "modul zarfini asan parca var"
    # v3 · ALT TABAN ÇİZGİSİ: tabanın altında yalnız ayak, süpürgelik ve koruyuculu asansör tahriki kalabilir
    ALTTA_SERBEST = ("ayak_", "plint_on", "asansor_kasnak_", "asansor_kayisi", "asansor_motoru", "asansor_motor_plakasi", "asansor_kayis_koruyucu", "asansor_vidasi_alt_ucu")
    alta = [p["ad"] for p in PARCALAR if p["grup"] not in ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF") and not p["grup"].startswith("B_")
            and p["wp"].val().BoundingBox().ymin < Y_PLINT - 0.5 and not p["ad"].startswith(ALTTA_SERBEST)]
    tah = [p["wp"].val().BoundingBox() for p in PARCALAR if p["ad"].startswith(("asansor_kasnak_", "asansor_kayisi"))]
    print("ALT TABAN %.0f: govde tabani %.0f-%.0f · tabanin altinda yalniz ayak + supurgelik + asansor tahriki (kasnak/kayis %.0f-%.0f, koruyuculu) · baska parca %s"
          % (Y_PLINT, Y_PLINT, Y_PLINT + 3.0, min(b.ymin for b in tah), max(b.ymax for b in tah), "YOK" if not alta else ", ".join(alta)))
    assert not alta, "tabanin altina inen govde parcasi var"
    assert max(b.ymax for b in tah) <= Y_PLINT - 1.0, "kasnak/kayis tabana degiyor"''')

degis('''    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH kutu_cad_v2"}''', '''    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH kutu_cad_v3"}''')
degis('''    print("E KUTU MODULU v2: %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()''',
      '''    print("E KUTU MODULU v3: %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()''')
degis('''        glb_yaz(os.path.join(KOK, "otonom", "hat3d", "kutu_modulu_v2.glb")); sys.stdout.flush()''',
      '''        glb_yaz(os.path.join(KOK, "otonom", "hat3d", "kutu_modulu_v3.glb")); sys.stdout.flush()''')
degis('''        bom_yaz(os.path.join(KOK, "arastirma", "5_PACK_v2"))''', '''        bom_yaz(os.path.join(KOK, "arastirma", "5_PACK_kutu_v3"))   # v3: eski SolidWorks 5_PACK_v3 klasoruyle karismasin''')
degis('''ALT_KURAL = [r"^ayak_[1-3]$",''', '''ALT_KURAL = [r"^asansor_vidasi_alt_ucu$", r"^ayak_[1-3]$",''')
io.open(os.path.join(U, "kutu_cad_v3.py"), "w", encoding="utf-8").write(s)
print("kutu_cad_v3.py yazildi")
