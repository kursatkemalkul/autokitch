# -*- coding: utf-8 -*-
"""firin_tp10_cad_v4 → firin_tp10_cad_v5 (27 Eyl 2026): FIRIN 79 mm ÖNE (Kemal: "fırını taşı, hizalanma olsun, doğrusu öyle").
Gövde + konveyör + giriş bandı + çıkış ölü plakası +79 z'ye kayar (ekle() taşır): tünel ön duvarı ön yüzün ÖNÜNDE (0…+79 = ÇIKINTI,
x 2500–4000, y 956–1473), ürün fırında −170 = TOPPING tabla ekseni → kayma yok, K GİRİŞ ÇİTİ KALKAR. Raf, ışınım kalkanı, takozlar ve
F arka sacı yerinde (gövde üstü +79…−651 hâlâ takozların altında). Giriş ağzı (sol yüz) dünyada −341…−10 kalır (disk 0…−340)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "firin_tp10_cad_v4.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


def satir_degis(onek, yeni):
    """onek ile başlayan (tek) satırı tamamen yeni ile değiştir"""
    global s
    i = s.index(onek); assert s.count(onek) == 1, onek
    j = s.index("\n", i)
    s = s[:i] + yeni + s[j:]


def ekle_sonra(onek, metin):
    global s
    i = s.index(onek); assert s.count(onek) == 1, onek
    j = s.index("\n", i) + 1
    s = s[:j] + metin + s[j:]


d('"""AUTOKITCH · F FIRIN · Sveba Dahlen TP10 KESİTİ, GÖVDESİ F MODÜLÜNE (1500) UZATILMIŞ · 3B MODEL + HATTA UYARLAMA v3 (26 Eyl 2026 gece)',
  '"""AUTOKITCH · F FIRIN · TP10 KESİTİ · 1500 · v5 (27 Eyl 2026): FIRIN 79 mm ÖNE — Kemal "fırını taşı, hizalanma olsun". Gövde + konveyör +\n'
  'giriş bandı + ölü plaka +79 z (ekle() taşır): tünel ön duvarı ön yüzün ÖNÜNDE (0…+79 çıkıntı, y 956–1473), ürün fırında −170 (tabla ekseni),\n'
  'K giriş çiti KALKTI. Raf/kalkan/takoz/arka sac yerinde. Önceki: firin_tp10_cad_v4.py\n'
  'v3/v4 (26 Eyl 2026 gece): AUTOKITCH · F FIRIN · Sveba Dahlen TP10 KESİTİ, GÖVDESİ F MODÜLÜNE (1500) UZATILMIŞ · 3B MODEL + HATTA UYARLAMA')
ekle_sonra("Z_URUN_FIRIN = -249.0",
           "ZS = 79.0                                        # v5: gövde + konveyör + giriş bandı + ölü plaka ÖNE kayma (Kemal 27 Eyl) → tünel ön duvarı ön yüzün önünde (çıkıntı)\n"
           "KAYAN = (\"F_TP10_GOVDE\", \"F_TP10_KONVEYOR\", \"F_GIRIS_BANDI\", \"F_CIKIS_PLAKA\")   # ekle() bu birimleri +ZS z'ye taşır (raf, kalkan, arka sac yerinde)\n"
           "Z_URUN_FIRIN_D = Z_URUN_FIRIN + ZS               # −170 · DÜNYA: fırında ürün ekseni = tabla ekseni (kayma yok)\n"
           "TUNEL_Z_D = (TUNEL_Z[0] + ZS, TUNEL_Z[1] + ZS)   # −406 … 0 (dünya)\n"
           "BANT_Z_D = (BANT_Z[0] + ZS, BANT_Z[1] + ZS)      # −394,5 … −13,5 (dünya)\n"
           "CIKINTI = ((X_F0, X_F1), (0.0, ZS))              # ön yüzün önündeki gövde bandı (x · z); y = YG0…YG1\n")
d('''def ekle(ad, wp, mal, birim, grup="SABIT", kaynak="VARSAYIM", bom=None, yerel=False):
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, birim=birim, grup=grup, kaynak=kaynak, bom=bom, yerel=yerel))''',
  '''def ekle(ad, wp, mal, birim, grup="SABIT", kaynak="VARSAYIM", bom=None, yerel=False):
    if birim in KAYAN and ZS:                                                            # v5: fırın + giriş bandı + ölü plaka 79 öne (dünya)
        wp = wp.translate((0.0, 0.0, ZS))
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, birim=birim, grup=grup, kaynak=kaynak, bom=bom, yerel=yerel))''')
d("kab = kab.cut(kut(x0 - 1.0, x0 + 2.0, 1152.0, 1210.0, -420.0, -10.0))",
  "kab = kab.cut(kut(x0 - 1.0, x0 + 2.0, 1152.0, 1210.0, -341.0 - ZS, -10.0 - ZS))                # v5: dünyada −341…−10 kalır (disk 0…−340); çıkıntıya delik açılmaz")
# ürün yolu: düz
i0 = s.index("def urun_z(xc):"); i1 = s.index("# ================================================================ 3 · HATTA UYARLAMA")
s = s[:i0] + ('def urun_z(xc):\n    """v5: ürün fırına ve K\'ye −170\'te (tabla ekseni) DÜZ gider — diskte kayma yok, K giriş çiti yok."""\n    return ZT\n\n\n') + s[i1:]
d("# Ürün fırına −249'da gelir (kayma TOPPING'de, diskte). K bandı üstündeki 20° çit (ürünün ARKASINDA) −249 → −170'e geri iter.",
  "# v5: ürün baştan sona −170 (fırın 79 öne alındı). CC_A/CC_B yalnız eski montaj arayüzü için duruyor (çit YOK).")
# K giriş çiti parçaları kalkar
j0 = s.index("    # ---- 3.3 K GİRİŞ ÇİTİ"); j1 = s.index("    # ---- 3.4 FIRIN ÜSTÜ HAVALI RAF")
s = s[:j0] + "    # ---- 3.3 K GİRİŞ ÇİTİ YOK (v5: ürün −170'te düz gelir) ----\n" + s[j1:]
d('''    ("F_K_GIRIS_CITI", "K giriş çiti (bizim · K bandı üstünde) · 20° · ürünü −249'dan −170'e alır · K'nin parçaları değişmez"),\n''', "")
d('· ekran + teknik bölme arkada · ≈14 kW (VARSAYIM)"),', '· ekran + teknik bölme arkada · ≈14 kW (VARSAYIM) · v5: 79 mm ÖNE — ön yüzün önünde çıkıntı 1500 × 517 × 79, F modülü 909 derin"),')
d("· PTFE 320 · eksen −249 · F'ye köprü braketleriyle\"),", "· PTFE 320 · eksen −170 (v5) · F'ye köprü braketleriyle\"),")
# main
d('print("TP10-UZUN v2 ·', 'print("TP10-UZUN v5 ·')
satir_degis('    print("ÇİT (K bandında):', '    print("v5: gövde + konveyör + giriş bandı + ölü plaka +%.0f z → çıkıntı 0…+%.0f (x %.0f–%.0f, y %.0f–%.0f) · tünel %s · bant %s · ürün ekseni %.0f · K çiti YOK" % (ZS, ZS, X_F0, X_F1, YG0, YG1, TUNEL_Z_D, BANT_Z_D, Z_URUN_FIRIN_D))')
d("ton.setdefault((p[\"mal\"], p[\"birim\"]), Mesh()).ekle(ag(cq.Workplane(obj=dunya(p).translate(cq.Vector(-XC_TP, -YG0, 0.0)))))",
  "ton.setdefault((p[\"mal\"], p[\"birim\"]), Mesh()).ekle(ag(cq.Workplane(obj=dunya(p).translate(cq.Vector(-XC_TP, -YG0, -ZS)))))   # v5: tek başına GLB kaymasız")
d("YARIK_V2 = ((2492.0, 2498.5, 1145.0, 1210.0, -417.0, -13.0), (2491.0, 2499.5, 1155.0, 1206.0, -409.0, -21.0))",
  "YARIK_V2 = ((2492.0, 2498.5, 1145.0, 1210.0, -417.0, -5.0), (2491.0, 2499.5, 1155.0, 1206.0, -409.0, -13.0))     # v5: ön çıta −13…−5 (ürün −170'te ön kenarı −20: montaj v51 denetimi çıtayı 1 mm kesiyordu)")
d('"generator": "AUTOKITCH firin_tp10_cad_v4"', '"generator": "AUTOKITCH firin_tp10_cad_v5"')
d('"otonom", "hat3d", "firin_tp10_v4.glb")', '"otonom", "hat3d", "firin_tp10_v5.glb")')
d('"firin_tp10_v4", parca, _dk)', '"firin_tp10_v5", parca, _dk)')
d('print("firin_tp10_v4.glb %.0f KB', 'print("firin_tp10_v5.glb %.0f KB')
d('"uzatılmış fırın · AUTOKITCH v3"), "montaj": K3.doku_ad("TP10-UZUN", "ana makine v48", ok_sol=False)}',
  '"uzatılmış fırın · AUTOKITCH v5 (79 öne)"), "montaj": K3.doku_ad("TP10-UZUN", "ana makine v51", ok_sol=False)}')
io.open(os.path.join(U, "firin_tp10_cad_v5.py"), "w", encoding="utf-8").write(s)
print("firin_tp10_cad_v5.py yazildi")
