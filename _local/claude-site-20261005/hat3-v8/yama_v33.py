# -*- coding: utf-8 -*-
"""v3.3: X ekseni motoru + 2 açıcı motoru (G9 çok delikli rakor) · yükleme bandı kablosu motora tam dayalı · montaj v3 (hat3_v3)."""
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


yama("h3_elk_ist_v1.py", [
    ('''    sabit("F_yukleme_bandi_motoru", [(2780.0, 1121.5, -495.8), (2780.0, 1121.5, -651.0),''',
     '''    sabit("F_yukleme_bandi_motoru", [(2780.0, 1121.5, -495.5), (2780.0, 1121.5, -651.0),'''),
    ('''
    # ======================================================= K =======================================================''',
     '''    # v3.3 · X ekseni motoru + açıcı motorları (sabit; açıcı başı pnömatik strokla iner → esnek PUR + servis halkası) → A|TOPPING duvarı G9 (çok delikli conta) → pano
    gecis("G9_A_TOPPING_motor", (1436.0, 1640.0, -720.0), "x", [("TC", "dis_yan_sol")], "A", r=5.5, t=31.5, yon="-",
          bom=("Rakor M32 çok delikli conta (3 motor kablosu) · A|TOPPING duvarı", 1, "Lapp SKINTOP MS-SC", ""))
    BOLGE_A9 = (737.5, 1436.0, 893.5, 1860.5, -828.5, 60.0)
    for j, (nm, S, it, T_, via) in enumerate((("x_motoru", (876.0, 924.5, -462.0), (2, -6.0), (1423.7, 1634.0, -720.0),
                                                  [(876.0, 924.5, -775.0), (1388.5, 924.5, -775.0), (1388.5, 1634.0, -775.0)]),
                                                 ("acici_motoru_arka", (1086.0, 1103.5, -506.6), (2, -6.0), (1423.7, 1646.0, -714.0), ()),
                                                 ("acici_motoru_on", (1116.0, 1184.6, -30.0), (1, 6.0), (1423.7, 1646.0, -726.0), ()))):
        cihaz("TOPPING_%s" % nm, S, T_, 3.0, "C", itme=it, via=via, on=(T_[0] - 25.0, T_[1], T_[2]), bolge=BOLGE_A9, h=5.0,
              bom=("Motor kablosu esnek PUR 4 × 0,75 + fren (X ekseni / açıcı · açıcıda 150 mm servis halkası)", 3, "", "sürücüleri TOPPING panosunda") if j == 0 else None)
    sabit("TOPPING_A_motor_demeti", [(1440.0, 1640.0, -720.0), (1530.0, 1640.0, -720.0), (1530.0, 1879.8, -720.0)], 5.5, "C", haric=("TOPPING_MODUL|dis_yan_sol",),
          bom=("Motor demeti (X ekseni + 2 açıcı) G9 → TOPPING panosu", 1, "", ""))

    # ======================================================= K ======================================================='''),
])
print("tamam")
