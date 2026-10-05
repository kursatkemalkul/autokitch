# -*- coding: utf-8 -*-
"""kaide_cad_v2 → kaide_cad_v3 (29 Eyl 2026 · YEREL) — Kemal: "ayak neden sıfırında bitmiyor" + A|C köşesi "iki istasyonun birleşimi gibi düşün".
KAİDELER İSTASYON YÜZLERİYLE AYNI HİZADA (v2'de A 8–692 · C 708–2492: istasyon yüzlerinden 8 mm içeride, A|C arasında 16 mm boşluk):
  · C: x 700–2500 (TOPPING dış yan sacları ve fırın gövdesiyle aynı çizgi) · arka z −830 (TOPPING arka sacıyla aynı düzlem)
  · A: x 1,5–700 (sol yan sac ve arka sac A kabininin kendi gövdesi, kaide onların içinde; sağ ucu C ile uç uca x 700) · arka z −828,5 (A arka sacının iç yüzü)
  · ön +35 aynı (önünde ön çerçeve +39…+59 ve paneller). Profil, plaka, enine / boyuna düzen aynı.
Önceki: kaide_cad_v2.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kaide_cad_v2.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""AUTOKITCH · A + C · MEKANİZMA KAİDESİ 104 · CAD v2 (27 Eyl 2026 gece)',
      '"""AUTOKITCH · A + C · MEKANİZMA KAİDESİ 104 · CAD v3 (29 Eyl 2026 · yap_kaide_cad_v3.py): KAİDELER İSTASYON YÜZLERİYLE AYNI HİZADA — A 1,5–700 · C 700–2500 · C arka −830' + NL +
      'v2: AUTOKITCH · A + C · MEKANİZMA KAİDESİ 104 · CAD v2 (27 Eyl 2026 gece)')
degis('A_X, C_X = (8.0, 692.0), (708.0, 2492.0)  # SPEC / resim',
      'A_X, C_X = (1.5, 700.0), (700.0, 2500.0)  # v3: istasyon yüzleriyle aynı hiza (v2 8–692 · 708–2492, Kemal: "sıfırında bitmiyor")')
degis('KZ = (-826.0, 35.0)                       # v2 (SPEC v63 §2.2)',
      'KZ_A, KZ_C = (-828.5, 35.0), (-830.0, 35.0)   # v3: A arka = A arka sacının iç yüzü · C arka = TOPPING arka sacıyla aynı düzlem (v2 −826)' + NL +
      'KZ = KZ_C                                # v2 (SPEC v63 §2.2)')
degis('def cerceve(b, on, x0, x1, enine, boyuna_z):' + NL + '    bw = PR["b"]; zf, zb = KZ[1] - bw, KZ[0] + bw',
      'def cerceve(b, on, x0, x1, enine, boyuna_z, kz=None):' + NL + '    kz = kz or KZ; bw = PR["b"]; zf, zb = kz[1] - bw, kz[0] + bw                # v3: birim başına z (A / C)')
degis('    ekle(on + "_on_profil", profil_x(x0, x1, zf, KZ[1]), "paslanmaz", b, bom=bom_())' + NL +
      '    ekle(on + "_arka_profil", profil_x(x0, x1, KZ[0], zb), "paslanmaz", b)',
      '    ekle(on + "_on_profil", profil_x(x0, x1, zf, kz[1]), "paslanmaz", b, bom=bom_())' + NL +
      '    ekle(on + "_arka_profil", profil_x(x0, x1, kz[0], zb), "paslanmaz", b)')
degis('    ekle(on + "_ust_plaka_4", kut(x0, x1, Y_DUZ + PR["h"], Y_MEK, KZ[0], KZ[1]), "paslanmaz", b,' + NL +
      '         bom=("Üst plaka AISI 304 4 mm · %s" % b, 1, "%.0f × %.0f" % (x1 - x0, KZ[1] - KZ[0]),',
      '    ekle(on + "_ust_plaka_4", kut(x0, x1, Y_DUZ + PR["h"], Y_MEK, kz[0], kz[1]), "paslanmaz", b,' + NL +
      '         bom=("Üst plaka AISI 304 4 mm · %s" % b, 1, "%.0f × %.0f" % (x1 - x0, kz[1] - kz[0]),')
degis('    cerceve("KAIDE_A", "kaide_A", A_X[0], A_X[1], ((KOLON["x"][0] + KOLON["x"][1]) / 2.0,), A_BOYUNA_Z)',
      '    cerceve("KAIDE_A", "kaide_A", A_X[0], A_X[1], ((KOLON["x"][0] + KOLON["x"][1]) / 2.0,), A_BOYUNA_Z, kz=KZ_A)')
degis('    cerceve("KAIDE_C", "kaide_C", C_X[0], C_X[1], C_ENINE, C_BOYUNA_Z)',
      '    cerceve("KAIDE_C", "kaide_C", C_X[0], C_X[1], C_ENINE, C_BOYUNA_Z, kz=KZ_C)')
degis('''        z0_bek, z1_bek = (A_SAC_Z[0], A_SAC_Z[1]) if kod == "KAIDE_A" else KZ  # v2: A taban sacı −828,5…+39 (profiller −826…+35)''',
      '''        z0_bek, z1_bek = (A_SAC_Z[0], A_SAC_Z[1]) if kod == "KAIDE_A" else KZ_C  # v3: C arka −830 (A taban sacı −828,5…+39)''')
degis('("KAIDE_A", "A mekanizma kaidesi 104 · x 8–692 (taban sacı 1,5–700)', '("KAIDE_A", "A mekanizma kaidesi 104 · x 1,5–700 (v3: istasyon yüzüyle aynı hiza · taban sacı 1,5–700)')
degis('("KAIDE_C", "C mekanizma kaidesi 104 · x 708–2492 · y 788–892 · z −826…+35',
      '("KAIDE_C", "C mekanizma kaidesi 104 · x 700–2500 (v3: TOPPING yan sacları ve fırınla aynı hiza) · y 788–892 · z −830…+35')
degis('BOM_KLASOR = os.path.join(KOK, "arastirma", "3_KAIDE_v2")', 'BOM_KLASOR = os.path.join(KOK, "arastirma", "3_KAIDE_v3")')
degis('    print("KAİDE v2 · %d parça', '    print("KAİDE v3 · %d parça')
degis('    print("DENETİM (kaide_cad_v2)")', '''    print("DENETİM (kaide_cad_v3)")
    for kod_, x_, z_ in (("KAIDE_A", A_X, KZ_A), ("KAIDE_C", C_X, KZ_C)):                    # v3 · istasyon yüzleriyle aynı hiza
        q_ = [dunya(p).BoundingBox() for p in ps if p["birim"] == kod_ and not p["ad"].endswith("taban_saci")]
        kontrol("v3 · %s profil + plaka x %.1f–%.1f (istasyon %.1f–%.1f) · arka z %.1f (%.1f) — sıfırında biter"
                % (kod_, min(v.xmin for v in q_), max(v.xmax for v in q_), x_[0], x_[1], min(v.zmin for v in q_), z_[0]),
                abs(min(v.xmin for v in q_) - x_[0]) < 0.01 and abs(max(v.xmax for v in q_) - x_[1]) < 0.01 and abs(min(v.zmin for v in q_) - z_[0]) < 0.01)
    kontrol("v3 · A kaidesi sağ ucu = C kaidesi sol ucu = 700 (A|C arasında boşluk yok)", abs(A_X[1] - C_X[0]) < 0.01 and abs(C_X[0] - 700.0) < 0.01)''')
compile(s, "kaide_cad_v3.py", "exec")
io.open(os.path.join(U, "kaide_cad_v3.py"), "w", encoding="utf-8").write(s)
print("kaide_cad_v3.py yazildi")
