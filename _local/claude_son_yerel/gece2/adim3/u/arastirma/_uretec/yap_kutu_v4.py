# -*- coding: utf-8 -*-
"""kutu_cad_v3 → kutu_cad_v4 (27 Eyl 2026): UZUN AYAKLAR BİR RAFIN ÜSTÜNDE BİTER (Kemal: "katlama kutu istasyonunun alt kısmında uzun ayaklar
var, o ayakları bir rafın üstünde bitir, yeterli alanı kullan, geri kalanını boş yap, o alanı kullanırız").
Kalıp ayakları (4 × 40×40 alu, 126–1080) ve kapak alt plakası ayakları (2 × 20×20, 126–994) artık 790'da biten ALT RAFIN üstünde (en alt parça U flap motoru 797,5):
raf 4 mm AISI 304 · x 4–800 · z −372…−24 (asansör plakasının 2 mm önü · sağda kablo kanalının solu) · y 786–790; sol duvara ve sağ duvara
30×30×3 köşebent, ön ve arka kenarda 30×30×3 köşebent (sehim: 100 N katlama kuvvetinde 0,2 mm; köşebentsiz 3,2 mm).
Rafın altı BOŞ: x 4–800 · y 126–756 · z −372…−24 (≈ 796 × 630 × 348). Önceki: kutu_cad_v3.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kutu_cad_v3.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


NL = chr(10)
i = s.index('"""') + 3
s = s[:i] + "AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v4 (27 Eyl 2026): kalıp + kapak plakası ayakları y 790'daki ALT RAFTA biter, rafın altı boş (Kemal). Önceki: kutu_cad_v3.py" + NL + s[i:]
d('''        ekle("kalip_ayagi_%d" % i, kut(xp - 20.0, xp + 20.0, Y_PLINT + 3.0, 1080.0, zp - 20.0, zp + 20.0).cut(kut(xp - 17.8, xp + 17.8, Y_PLINT + 2, 1081, zp - 17.8, zp + 17.8)), "aluminyum",
             bom=("Alüminyum profil 40 × 40 (kalıp ayağı)", 4, "boy 997", "item / Bosch Rexroth 40×40") if i == 0 else None)''',
  '''        ekle("kalip_ayagi_%d" % i, kut(xp - 20.0, xp + 20.0, ALT_RAF_Y[1], 1080.0, zp - 20.0, zp + 20.0).cut(kut(xp - 17.8, xp + 17.8, ALT_RAF_Y[1] - 1, 1081, zp - 17.8, zp + 17.8)), "aluminyum",
             bom=("Alüminyum profil 40 × 40 (kalıp ayağı)", 4, "boy %.0f (v4: alt rafta biter)" % (1080.0 - ALT_RAF_Y[1]), "item / Bosch Rexroth 40×40") if i == 0 else None)
    # v4 · ALT RAF (Kemal): ayaklar burada biter, altı boş
    ekle("kalip_alt_rafi", kut(4.0, 800.0, ALT_RAF_Y[0], ALT_RAF_Y[1], -372.0, -24.0), "sac",
         bom=("Alt raf 304 · 4 mm", 1, "796 × 348", "v4: kalıp + kapak plakası ayakları üstünde · altı boş (≈ 796 × 630 × 348)"))
    _y0 = ALT_RAF_Y[0]
    ekle("kalip_alt_rafi_koseben_sol", kut(2.0, 32.0, _y0 - 30.0, _y0, -372.0, -24.0).cut(kut(5.0, 33.0, _y0 - 31.0, _y0 - 3.0, -373.0, -23.0)), "sac",
         bom=("Köşebent 30 × 30 × 3 AISI 304 (alt raf)", 4, "sol/sağ duvar + ön/arka kenar", "M6 ile duvara"))
    ekle("kalip_alt_rafi_koseben_sag", kut(770.0, 800.0, _y0 - 30.0, _y0, -372.0, -55.0).cut(kut(769.0, 797.0, _y0 - 31.0, _y0 - 3.0, -373.0, -54.0)), "sac")
    ekle("kalip_alt_rafi_koseben_on", kut(32.0, 770.0, _y0 - 30.0, _y0, -54.0, -24.0).cut(kut(31.0, 771.0, _y0 - 31.0, _y0 - 3.0, -55.0, -27.0)), "sac")
    ekle("kalip_alt_rafi_koseben_arka", kut(32.0, 770.0, _y0 - 30.0, _y0, -372.0, -342.0).cut(kut(31.0, 771.0, _y0 - 31.0, _y0 - 3.0, -369.0, -341.0)), "sac")''')
d('    ekle("kapak_alt_plaka_ayagi_0", kut(780.0, 800.0, Y_PLINT + 3.0, 994.0, -368.0, -348.0), "aluminyum")',
  '    ekle("kapak_alt_plaka_ayagi_0", kut(780.0, 800.0, ALT_RAF_Y[1], 994.0, -368.0, -348.0), "aluminyum")   # v4: alt rafta biter')
d('    ekle("kapak_alt_plaka_ayagi_1", kut(780.0, 800.0, Y_PLINT + 3.0, 994.0, BZ1, BZ1 + 20.0), "aluminyum")',
  '    ekle("kapak_alt_plaka_ayagi_1", kut(780.0, 800.0, ALT_RAF_Y[1], 994.0, BZ1, BZ1 + 20.0), "aluminyum")')
d('BZ0, BZ1 = ZB - 160.0, ZB + 160.0     # −366 … −46', 'BZ0, BZ1 = ZB - 160.0, ZB + 160.0     # −366 … −46' + NL + 'ALT_RAF_Y = (786.0, 790.0)            # v4: alt raf — mekanizmanın en alt parçası flap katlayıcı motoru 797,5 altında')
s = s.replace('"generator": "AUTOKITCH kutu_cad_v3"', '"generator": "AUTOKITCH kutu_cad_v4"')
d('"otonom", "hat3d", "kutu_modulu_v3.glb")', '"otonom", "hat3d", "kutu_modulu_v4.glb")')
d('"arastirma", "5_PACK_kutu_v3")', '"arastirma", "5_PACK_kutu_v4")')
io.open(os.path.join(U, "kutu_cad_v4.py"), "w", encoding="utf-8").write(s)
print("kutu_cad_v4.py yazildi")
