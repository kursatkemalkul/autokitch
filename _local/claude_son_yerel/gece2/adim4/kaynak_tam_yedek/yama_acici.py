# -*- coding: utf-8 -*-
"""Kemal 1 Eki: açıcı motoru yok, açıcı hazır alınacak, yalnız görsel → açıcı motor kabloları kalkar; X ekseni motoru tek kablo G9'dan doğrudan panoya."""
import io
D3 = r"@@KOK_W@@\b3\arastirma\_uretec\h3\h3_elk_ist_v1.py"
D2 = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat2-v4\arastirma\_uretec\h2\h2_elk_ist_v1.py"


def yama(P, ciftler):
    s = io.open(P, encoding="utf-8").read()
    for a, b in ciftler:
        assert s.count(a) == 1, (P[-20:], a[:90], s.count(a))
        s = s.replace(a, b)
    io.open(P, "w", encoding="utf-8").write(s)
    print("yamalandı", P[-18:], len(ciftler))


ZN = ('''bom=("Enerji zinciri demeti (araba: dönüş motoru · tabla sıfır sensörü · açıcı) · zincir sabit ucundan KD1'e"''',
      '''bom=("Enerji zinciri demeti (araba: dönüş motoru · tabla sıfır sensörü) · zincir sabit ucundan KD1'e"''')
for P, gx, bolge, x0, xv in ((D3, 1436.0, "BOLGE_A9 = (737.5, 1436.0, 893.5, 1860.5, -828.5, 60.0)", 876.0, 1388.5),
                             (D2, 1207.5, "BOLGE_A = (507.5, 1207.5, 893.5, 1860.5, -828.5, 60.0)", 647.5, 1160.0)):
    s = io.open(P, encoding="utf-8").read()
    i0 = s.index("    # v3.3 · X ekseni motoru" if P == D3 else "    # X ekseni motoru + açıcı motorları")
    i1 = s.index('bom=("Motor demeti (X ekseni + 2 açıcı) G9 → TOPPING panosu", 1, "", ""))\n') + len('bom=("Motor demeti (X ekseni + 2 açıcı) G9 → TOPPING panosu", 1, "", ""))\n')
    bn = bolge.split(" = ")[0]
    yeni = '''    # X ekseni motoru (sabit) → A arka duvarı → A|TOPPING duvarı G9 rakoru → TOPPING panosu · açıcı HAZIR ALINIR (yalnız görsel, motor kablosu yok · Kemal 1 Eki)
    gecis("G9_A_TOPPING_motor", (%.1f, 1640.0, -720.0), "x", [("TC", "dis_yan_sol")], "A", r=3.0, t=31.5, yon="-", bom=RK_BOM(1))
    %s
    cihaz("TOPPING_x_motoru", (%.1f, 924.5, -462.0), (%.1f, 1879.8, -720.0), 3.0, "C", itme=(2, -6.0),
          via=[(%.1f, 924.5, -775.0), (%.1f, 924.5, -775.0), (%.1f, 1640.0, -775.0), (%.1f, 1640.0, -720.0),
               ((%.1f, 1640.0, -720.0), ("TOPPING_MODUL|dis_yan_sol",))],
          on=(%.1f, 1862.0, -720.0), bolge=%s, h=5.0,
          bom=("Motor kablosu esnek PUR 4 × 0,75 + fren (X ekseni)", 1, "", "sürücüsü TOPPING panosunda"))
''' % (gx, bolge, x0, gx + 94.0, x0, xv, xv, gx - 37.3, gx + 24.0, gx + 94.0, bn)
    s = s[:i0] + yeni + s[i1:]
    io.open(P, "w", encoding="utf-8").write(s)
    yama(P, [ZN])
print("tamam")
