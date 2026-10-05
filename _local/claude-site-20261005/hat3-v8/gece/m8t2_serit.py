# -*- coding: utf-8 -*-
"""m8t2 · ANA HAT KABLO ŞERİTLEME — sabit şerit sırası + kademeli (stagger) geçişler.
Yol = bas (sabit port noktaları) + bacaklar [(eksen, kesit konumu)] + son (sabit port noktaları).
Geçiş parametreleri (düzlem konumu + L sırası) arama ile seçilir; denetim: kapsül-kapsül (m8t2_kontrol)."""
import math, json, os, sys, random, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m8t2_rota_eski as RE
EKS = "xyz"; IX = {"x": 0, "y": 1, "z": 2}
G = 1.0                     # şerit aralığı (kablo-kablo)
RR = RE.RR


def dig(a):
    return [e for e in EKS if e != a]


# ------------------------------------------------------------------ kesit yerleşimleri
def sira(bas, adlar, yon=+1, g=G):
    """adlar sırayla, bas kenarından (duvar + g) yon yönünde: {ad: merkez}"""
    out = {}; c = bas
    for a in adlar:
        r = RR[a]; m = c + yon * (g + r); out[a] = m; c = m + yon * r
    return out


L = {}            # bölüm -> {ad: {eksen: değer}}
def koy(bol, ad, **kw):
    L.setdefault(bol, {})[ad] = dict(kw)


# ===== ÜST HAT M (UF1 batı · UF2 · UF3 · UF4 doğu) · eksen x · (y, z)
ZB = -824.5                                   # kanal iç arka yüz
R1 = ["F_veri", "F_guc", "DOLAP_guc", "DOLAP_veri", "modem", "ROBOT_veri", "QR_veri"]
R2 = ["A_veri", "A_guc", "TOPPING_guc", "TOPPING_veri"]
Y1 = 2140.0; Y2 = 2153.5                       # R1 / R2 tabanı
for a, z in sira(ZB, R1).items(): koy("M", a, y=Y1 + RR[a], z=z)
for a, z in sira(ZB, R2).items(): koy("M", a, y=Y2 + RR[a], z=z)
ZT_ARKA = -786.1                               # UF3 oluk arka duvarı iç yüzü
c1 = ZT_ARKA + 0.5 + RR["QR_guc"]; c2 = c1 + RR["QR_guc"] + G + RR["bina"]
koy("M", "bina", y=2107.0 + RR["bina"], z=c2)                    # alt bölge ön sütun (T'de en batı)
koy("M", "QR_guc", y=2107.0 + RR["QR_guc"], z=c1)
koy("M", "ROBOT_guc", y=2107.0 + 2 * RR["QR_guc"] + G + RR["ROBOT_guc"], z=c1)
# ===== GV dizisi (UF4'te iniş öncesi + GV içi) · tek z sırası
GVS = R1 + ["QR_guc", "ROBOT_guc", "bina"]
GVZ = sira(ZB, GVS)
for a in GVS:
    koy("U4", a, y=L["M"][a]["y"], z=GVZ[a])                        # UF4 iniş öncesi (y aynı, z GV)
    koy("GV", a, x=2452.0 + 0.5 + RR[a], z=GVZ[a])
# ===== UF1 doğu (T doğusu): K/E alt-ön bant · A/F girişleri
KE_ORDER = ["K_guc", "K_veri", "E_guc", "E_veri"]                   # arka->ön = batı->doğu (T)
for a, z in sira(-760.0 - 1.0, KE_ORDER, yon=+1).items(): koy("UK", a, y=2107.0 + RR[a], z=z)
# ===== KE (pencere) + UST_KE: eski şeritler
for a, d in {"K_guc": (2151.2, -817.2), "K_veri": (2149.3, -805.6), "E_guc": (2151.2, -794.0), "E_veri": (2149.3, -782.4)}.items():
    koy("KE", a, y=d[0], z=d[1])
# ===== T içi yeni konumlar (x, y) — kurallar: batıya giden + y örtüşen: derin -> doğu · K/E: tüm örtüşen batı kablolarının doğusunda
TX0 = 3327.5
xb = TX0 + 0.5 + 9.95
koy("T", "bina", x=xb, y=L["M"]["bina"]["y"])
xq = xb + 9.95 + G + 6.25
koy("T", "QR_guc", x=xq, y=L["M"]["QR_guc"]["y"])
koy("T", "ROBOT_guc", x=xq, y=L["M"]["ROBOT_guc"]["y"])
xf = xq + 6.25 + G + 2.4
koy("T", "fan24", x=xf, y=2107.0 + 2.4)
xk = xf + 2.4 + G
for a in KE_ORDER:
    r = RR[a]; xk += r; koy("T", a, x=xk, y=L["UK"][a]["y"]); xk += r + G
# R1 (T kabloları): derin -> doğu ; R1 sırası arka->ön: DOLAP_guc (en derin) ... QR_veri (en sığ)
R1T = ["QR_veri", "ROBOT_veri", "modem", "DOLAP_veri", "DOLAP_guc"]   # batı -> doğu
xx = float(os.environ.get("R1X0", TX0 + 0.5))
for a in R1T:
    r = RR[a]; xx += r; koy("T", a, x=xx, y=L["M"][a]["y"]); xx += r + G
R2T = ["TOPPING_veri", "TOPPING_guc"]                                   # batı->doğu (TOPPING_guc daha derin)
xx = float(os.environ.get("R2X0", TX0 + 0.5 + 30.0))
for a in R2T:
    r = RR[a]; xx += r; koy("T", a, x=xx, y=L["M"][a]["y"]); xx += r + G

if __name__ == "__main__":
    for b, d in L.items():
        print(b)
        for a, p in d.items(): print("   %-13s %s" % (a, {k: round(v, 2) for k, v in p.items()}))


# ===== BÖLGE 2 (GV altı): eski bölümler, AYNI sabit sıra (GVS) ile raf yerleşimi
def bolge2():
    K2 = RE.kesitler()
    for nm in ("FB", "RU", "RL", "FA", "TS", "ZT", "ZF", "ZK", "ZB1", "ZB2", "BV"):
        kes = K2[nm]
        icinde = [(a, RR[a]) for a in GVS if nm in RE.ROTA[a]]
        try:
            kes.yerlestir(icinde, sirali=True, bosluk=0.8)
        except AssertionError as e:
            print("   sığmadı (sıralı):", nm, e)
            kes.poz = {}; kes.yerlestir(icinde, sirali=False, bosluk=0.8)
        for a, p in kes.poz.items(): L.setdefault(nm, {})[a] = dict(p)
    return K2


K2 = bolge2()


# ===== ZEMİN (elle): ZK alt sıra = QR çıkış x'leri · üst sıra QR_veri + bina · ZF/ZT köşe kuralına göre sıra
YB = 1.5 + 0.5                                              # zemin kanal tabanı + aralık
ZKX = {"modem": 5354.85, "ROBOT_veri": 5370.0, "QR_guc": 5386.0, "ROBOT_guc": 5400.75, "QR_veri": 5354.85, "bina": 5370.15}
ALT = ["ROBOT_guc", "QR_guc", "ROBOT_veri", "modem"]       # ZF arka -> ön
UST = ["bina", "QR_veri"]
YU = YB + 12.5 + 1.0                                        # üst sıra tabanı (15.5)
for a in ALT: L["ZK"][a] = {"x": ZKX[a], "y": YB + RR[a]}
for a in UST: L["ZK"][a] = {"x": ZKX[a], "y": YU + RR[a]}
for a, z in sira(-193.5, ALT, g=0.5).items(): L["ZF"][a] = {"z": z, "y": L["ZK"][a]["y"]}
for a, z in sira(-193.5, UST, g=0.5).items(): L["ZF"][a] = {"z": z, "y": L["ZK"][a]["y"]}
for a, x in sira(4041.5, ALT[::-1], g=0.5).items(): L["ZT"][a] = {"x": x, "y": L["ZK"][a]["y"]}
for a, x in sira(4041.5, UST[::-1], g=0.5).items(): L["ZT"][a] = {"x": x, "y": L["ZK"][a]["y"]}
L["ZB1"]["bina"] = {"z": L["ZB1"]["bina"]["z"], "y": L["ZK"]["bina"]["y"]}
L["ZB2"]["bina"] = {"x": L["ZB2"]["bina"]["x"], "y": L["ZK"]["bina"]["y"]}
