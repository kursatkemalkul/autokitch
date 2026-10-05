# -*- coding: utf-8 -*-
"""TOPPING PAKETI · TEK OLCU KAYNAGI (dunya mm: x hat, y yukari, z koridora).
EVAPORATOR YAN YANA: harc UNO pnomatik takimi (kuru bolmede x 1696-1748, y 1534-1632) iki kasetin ARASINDAN gecer.
 L kaset (sol)  x 1446-1670 · y 1282-1682  -> harc takimina net 26 (arada 2 harc hortumu + KLF + L fan kablosu seridi x 1678-1686)
 R kaset (sag)  x 1758-2223 · y 1383-1835  -> harc takimina net 10 · sos takimina (2233,5) net 10,5
Her kaset: dis sac 1 + PU 39 + ic sac 1 (W 41) · on yuzde POM isi kesici cerceve (z -640..-630) · serpantin z -731..-646 (85 derin, eskiyle ayni).
Hava yolu (eski tek kasetle ayni mantik): donus = alt bolmeden serpantin onu (y <= 1530, ust raf arka bukumu 1534-1572 kapatir) ->
serpantin -> arka plenum (z -785..-731) -> fan -> fan onu bolmesi -> ufleme = ust bolmeye (y >= 1578)."""
W = 41.0
Z0, Z1 = -826.0, -640.0          # kaset dis arka / on (POM cerceve -640..-630)
ZI0 = -785.0                     # ic arka yuz
SER_Z = (-731.0, -646.0)
FAN_PZ = (-701.5, -700.0)        # fan paneli
KAS = {
    "L": dict(x=(1446.0, 1670.0), y=(1282.0, 1682.0),
              ser=(1487.0, 1629.0, 1324.0, 1500.0),        # serpantin x0 x1 y0 y1 (yuz 142 x 176, ic yuzlere + tavaya oturur)
              perde_y=1504.0,                              # on bolme ayirma perdesi (1 mm) 1504-1505
              fan=(1558.0, 1573.5)),                       # fan merkezi x, y
    "R": dict(x=(1758.0, 2223.0), y=(1383.0, 1835.0),
              ser=(1799.0, 2126.0, 1425.0, 1565.0),        # 327 x 140 (ic yuz + tava + kollektor perdesi)
              perde_y=1569.0, kol_x=2126.0,                # kollektor seridi ayirma perdesi 2126-2127 (on bolme, y < 1569)
              fan=(1860.5, 1682.0)),
}
def ic(k):
    d = KAS[k]; return (d["x"][0] + W, d["x"][1] - W, d["y"][0] + W, d["y"][1] - W)
# soguk oda arka duvari pencereleri: KAN = hava kanali (kovan dis olcusu) · PEN = astar/lazer sac penceresi (KAN + 4)
KAN = {"Ld": (1503.0, 1623.0, 1338.0, 1497.0),   # donus L  (serpantin onu)
       "Lu": (1503.0, 1623.0, 1582.0, 1637.0),   # ufleme L (fan onu, ust raf ustu)
       "Rd": (1807.0, 2121.0, 1434.0, 1530.0),   # donus R
       "Ru": (1807.0, 2174.0, 1582.0, 1786.0)}   # ufleme R
PEN = {k: (a - 4.0, b + 4.0, c - 4.0, d + 4.0) for k, (a, b, c, d) in KAN.items()}
AGIZ = {k: (a + 3.0, b - 3.0, c + 3.0, d - 3.0) for k, (a, b, c, d) in KAN.items()}
BOLGE = {"L": (1497.0, 1640.0, 1325.0, 1645.0), "R": (1790.0, 2190.0, 1420.0, 1800.0)}   # duvar yenileme bolgeleri
# bakir hatlar (eski uclar y 1383'te: sivi x 2134 / emis x 2156, z -700)
XS, XE, ZH = 2134.0, 2156.0, -700.0
RS, RE, RT = 3.2, 6.35, 5.0
Y_SIVI_KOL, Z_SIVI_KOL = 1446.0, -742.0           # L kolu sivi
Y_EMIS_KOL, Z_EMIS_KOL = 1440.0, -775.0           # L kolu emis
XK_R, ZK_R = 2172.0, -745.0                       # R emis kollektoru
XTXV_L = (1598.0, 1626.0); YTXV_L = (1452.0, 1482.0); ZTXV_L = (-767.0, -747.0)
XK_L = 1616.0                                     # L emis kollektoru (dikey, z -775)
# tahliye
XT_R, ZT_R = 2126.0, -760.0
XT_L, ZT_L = 1625.0, -722.0
Y_TAH = 1140.0
# KLF kablosu + L fan kablosu seridi
X_SERIT = 1684.0
Z_KLF = -804.85
Z_FAN = -714.0
Y_PANO = 1879.8
# surucu kartlari: +804 x, +268 y (DIN rayi 2262-2409 x 1705-1740)
D_KART = (804.0, 268.0, 0.0)
# yayici aktuatoru SMC CRB2BW10-90S (SMC CAT.ES20-159 s.10): govde O29 x 15 (B) · on mil O4 D=14 (G1 3, O9 gobek) · arka mil C=8 (G2 1)
# yan portlar M5, arka yuzden M=5, iki port arasi N=25 · on yuz 3-M3 P=24 · tork 0,18 N.m (0,5 MPa)
SPR = {"harc": dict(x=1722.0, port_yon=+1, serit_x=1745.0), "sos": dict(x=2259.5, port_yon=-1, serit_x=2239.0)}
SPR_Y = 1194.05
SPR_ZF, SPR_ZB = -130.0, -115.0   # govde on (mil tarafi) / arka
Y_HAT_A, Y_HAT_B = 1158.0, 1169.0  # soguk oda tabanindaki hortum seritleri
