# -*- coding: utf-8 -*-
import io, os
H3 = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\b3\arastirma\_uretec\h3"


def yama(dosya, ciftler):
    P = os.path.join(H3, dosya)
    s = io.open(P, encoding="utf-8").read()
    for a, b in ciftler:
        assert s.count(a) == 1, (dosya, a[:100], s.count(a))
        s = s.replace(a, b)
    io.open(P, "w", encoding="utf-8").write(s)
    print("yamalandı:", dosya, len(ciftler))


yama("h3_elk_qr_v1.py", [
    # güç taban rakoru: gövde taban plakasının ALTINDA, kontra somun taban kanalının içinde (kanal tabanı somun çapında açık)
    ('''    g = g.cut(sil((GUC_RAKOR[0], 20.0, GUC_RAKOR[1]), (GUC_RAKOR[0], 23.0, GUC_RAKOR[1]), 14.0))''',
     '''    g = g.cut(sil((GUC_RAKOR[0], 20.0, GUC_RAKOR[1]), (GUC_RAKOR[0], 26.0, GUC_RAKOR[1]), 19.5))'''),
    ('''    rk, d_ = rakor((GUC_RAKOR[0], 17.0, GUC_RAKOR[1]), "y", 12.0, 3.0, yon="+", disli=16.0)''',
     '''    rk, d_ = rakor((GUC_RAKOR[0], 17.0, GUC_RAKOR[1]), "y", 12.0, 3.0, yon="-", disli=16.0)          # taban plakası 17–20 · gövde altta'''),
    # üst sıra (5): kelepçeler üst rafın altına (göz yüz sacı yerine) · sensör kablosu raftan uzak
    ('''            yg = kb.ymax + 2.5; mx = (mb.xmin + mb.xmax) / 2.0''',
     '''            yg = kb.ymax + (3.2 if sat == 5 else 2.5); mx = (mb.xmin + mb.xmax) / 2.0'''),
    ('''                ekle("goz_%s_motor_kablosu_kelepce_%d" % (g_, j), EO.kelepce((xk, yg, 691.0), "x", 2.0, 672.0, "-z"), "celik", B2)''',
     '''                ekle("goz_%s_motor_kablosu_kelepce_%d" % (g_, j), EO.kelepce((xk, yg, 691.0), "x", 2.0, *((1650.0, "+y") if sat == 5 else (672.0, "-z"))), "celik", B2)'''),
    ('''            yg = kb.ymax + 8.0; sx = 5397.0''', '''            yg = kb.ymax + (6.0 if sat == 5 else 8.0); sx = 5397.0'''),
    ('''                ekle("goz_%s_sensor_kablosu_kelepce_%d" % (g_, j), EO.kelepce(p_, ax, 1.75, 672.0, "-z"), "celik", B2)''',
     '''                ekle("goz_%s_sensor_kablosu_kelepce_%d" % (g_, j), EO.kelepce(p_, ax, 1.75, *((1650.0, "+y") if (sat == 5 and ax == "x") else (672.0, "-z"))), "celik", B2)'''),
])
yama("h3_elk_hat_v1.py", [
    ('''    rk, d_ = rakor((rx, 123.0, rz), "y", 9.0, 1.0, yon="-", disli=12.0)''', '''    rk, d_ = rakor((rx, 123.0, rz), "y", 9.0, 1.5, yon="-", disli=12.0)          # taban dış sacı 123–124,5'''),
    ('''    DELIKLER.append(("UD", "ust_ke_yan_sag", kut(5210.0, 5233.0, 2112.0, 2158.0, z0 + 3.0, z1 - 3.0), "dış dikey kanal girişi"))''',
     '''    DELIKLER.append(("UD", "ust_ke_yan_sag", kut(5210.0, 5233.0, 2110.0, 2158.0, z0 + 3.0, z1 - 3.0), "dış dikey kanal girişi (kapak dahil)"))'''),
])
yama("h3_elk_ist_v1.py", [
    # fan rakorları: duvar 1765 → iç sacın iç yüzü 1722,5 (42,5)
    ('''              "C", r=2.5, t=41.0, yon="+", bom=RK_BOM(2) if i == 0 else None)''', '''              "C", r=2.5, t=42.5, yon="+", bom=RK_BOM(2) if i == 0 else None)'''),
    # zincir kanalının arkası açık (ölçüldü: y 923,5'te yalnız ön duvar −418…−415) → rakor yok, demet açık arkadan çıkar
    ('''    gecis("TOPPING_enerji_zinciri_sabit_ucu", (2459.0, 923.5, -475.0), "z", [("TC", "enerji_zinciri_kanali")], "C", r=6.0, t=1.5, yon="-", bom=RK_BOM(1))
    sabit("TOPPING_enerji_zinciri_demeti", [(2459.0, 923.5, -470.0), (2459.0, 923.5, -808.0), KD1(923.5)], 6.0, "C", haric=("TOPPING_MODUL|enerji_zinciri_kanali",),''',
     '''    sabit("TOPPING_enerji_zinciri_demeti", [(2459.0, 923.5, -470.0), (2459.0, 923.5, -808.0), KD1(923.5)], 6.0, "C",'''),
])
print("tamam")
