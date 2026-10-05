# -*- coding: utf-8 -*-
"""topping_hesap_v6 → topping_hesap_v7 (29 Eyl 2026) — BANTLI TABLA (bantli_tabla_hesap_v1 · ayar d, e):
  · aktarma 1637 → 1665,4 (+28,4: kaset burnu yükleme bandına 3 mm) · ray sağ ucu 1785 → 1798 · limit+ 1660 → 1688
  · hareketli kütle: tabla grubu (göbek + Ø340 tabla + disk ≈ 6,256 kg) yerine kaset 8,45 kg → X torku yeniden hesaplanır
Başka hiçbir sayı değişmez."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_hesap_v6.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


import bantli_tabla_hesap_v1 as BH
AKT_YEREL = round(BH.AKT - 700.0, 1)                     # 1665,4 (dünya 2365,4)
KASET_KG = 8.45                                           # bantli_tabla_cad_v1 D10
degis("X_AKTARMA = 1637.0                                                           # disk kenari x=1807, bant burnu x=1815 -> 8 mm [CAD v21]",
      "X_AKTARMA = %.1f                                                           # v7 BANTLI TABLA: kaset burnu yükleme bandı burnuna 3 mm (dünya %.1f) [bantli_tabla_hesap_v1]" % (AKT_YEREL, BH.AKT))
degis("X_LIMIT_SOL, X_LIMIT_SAG = -380.0, 1660.0                                   # yazilimdan once donanim limitleri [V]",
      "X_LIMIT_SOL, X_LIMIT_SAG = -380.0, 1688.0                                   # v7: limit+ +28 (aktarma +28,4) [V]")
degis("RAY_X0, RAY_X1 = -500.0, 1785.0                                             # HGR15 ray gercek boyu = 2285 mm [CAD v21]",
      "RAY_X0, RAY_X1 = -500.0, 1798.0                                             # v7: sağ uç 1785 → 1798 (dünya 2498; blok aktarmada 1796,1'e kadar) · HGR15 2298 mm")
degis("X_HAREKET_KUTLE = 22.52                                                     # kg [K: topping_fizik_ihrac_v16]",
      "X_HAREKET_KUTLE = round(22.52 - 6.256 + %.2f, 2)                            # v7: tabla grubu 6,256 kg yerine kaset %.2f kg (bantli_tabla_cad_v1 D10) [K: topping_fizik_ihrac_v16]" % (KASET_KG, KASET_KG))
s = s.replace('"""', '"""topping_hesap_v7 (29 Eyl 2026): BANTLI TABLA — aktarma %.1f, ray sağ ucu 1798, limit+ 1688, hareketli kütle kasetle (yap_topping_hesap_v7.py).\n' % AKT_YEREL, 1)
compile(s, "topping_hesap_v7.py", "exec")
io.open(os.path.join(U, "topping_hesap_v7.py"), "w", encoding="utf-8").write(s)
print("topping_hesap_v7.py yazildi")
