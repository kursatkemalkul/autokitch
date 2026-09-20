# -*- coding: utf-8 -*-
"""AUTOKITCH · KAŞAR KABI 3D v4 (20 Eyl 2026) — ARAŞTIRMAYA GÖRE YENİDEN TASARIM · dönen parçalar ANİMASYONLU
Kemal: "ölçüme dayalı yap, kaşarın davranışını internetten bul, tasarımı yeniden tüm detaylarıyla: nereden çıkacak, nasıl dönecek."

v3'ten FARKLAR (gerekçe = kaynaklı araştırma, bkz. otonom/kaset3d/akis.html):
  1 ÇIKIŞ ORTADA, ALTTAN. Paftada (HAT_ATOSA_TABLALI v2) hazne z −70…−470, tabla ekseni z −270 = kabın tam ortası.
    v3'teki ön uç tüpü tabla ekseninin 225 mm önüne döküyordu. Ortadan çıkış + üstünde köprü: Little Caesars US12508716B2.
  2 İKİ KARŞILIKLI HELEZON tek milde (arka yarı SOL, ön yarı SAĞ el) → ikisi de ortaya iter, kanat uçları 180° faz farklı.
  3 ARTAN HATVE 30-40-52 + KONİK MİL Ø42→Ø20: girişin her yerinden çeker (sabit hatve yalnız en uçtan çeker — KWS / Jenike).
  4 BOĞAZ ORTADA 146 mm KAPALI (köprü): ağza malzeme yalnız helezon dönünce gelir (kapalı 1 hatve).
  5 KADEH KESİT: kâse yarıçapı = karıştırıcı ekseni merkezli R134; karıştırıcı R129 tüm kâseyi süpürür, silikon sıyırıcı duvara değer.
    v3 kesitinde omuzlar 29–40° yatık ve süpürülmüyordu (≈ 6 L ölü bölge).
  6 HELEZON EKSENİ 72 → 48 (kâse + karıştırıcı kapağın altına sığsın diye).
  7 ÖNDE YATAK KAPAĞI (çeyrek tur): sökünce helezon öne çekilir. Çıkış tüpü yok.
  8 AĞIZ 50 × 45 + bilezik + menteşeli kapak (v27 kararı korunur).
MAKİNE TARAFI (dozaj modelinde gösterilir): ağzın altında PİMLİ DAĞITICI + huni + dönen-kayan tabla + pide.
  Helezon pide başına yalnız 1–3 tur atar → ince dozajı dağıtıcı yapar: üstündeki küçük yığını tarayıp sabit akışla döker
  (QTS US20120227865A1: dönen tırmıklar 'metering' için · Middleby US5244020A: çıkışta yıldız çark + terazi).
Zarf DEĞİŞMEDİ: 280 × 400 × 360 (16 Eyl kararı).  Çıktı: otonom/kaset3d/kasar_v4.glb/.usdz · kasar_v4_dozaj.glb
"""
import json, math, os, random, struct
from kaset_3d_v3 import (Mesh, MM, sub, add, mul, dot, cross, unit, kutu, silindir, halka_yuz, boru, torus, ekstruzyon, uc_plakasi,
                         rr_plaka, rr_cerceve, vida, hac_kaplin, doku_ad, doku_montaj, etiket_yuzu, MALZEME, usdz_yaz, OUT)
from kasar_akis_model_v1 import roberts, RHO

MALZEME.update({
    "kasar":   dict(renk=(0.99, 0.80, 0.26, 1.0), met=0.0, ruf=0.9),
    "kasar_dolgu": dict(renk=(0.99, 0.82, 0.32, 1.0), met=0.0, ruf=0.95),          # ayrı malzeme: sayfadaki "kaşarı gizle" tuşu bunu saydam yapar
    "hamur":   dict(renk=(0.93, 0.85, 0.68, 1.0), met=0.0, ruf=0.95),
    "silikon": dict(renk=(0.16, 0.50, 0.95, 1.0), met=0.0, ruf=0.7),
})

# ---------------- ANA ÖLÇÜLER (mm) ----------------
W_, D_, H_ = 280.0, 400.0, 360.0
ET, TP, FLANS = 3.0, 5.0, 3.0
CY = 48.0                          # helezon ekseni
RT_I, RT_O = 31.0, 34.0            # tekne iç / dış yarıçap (helezon Ø56, boşluk 3)
HW_O = W_ / 2 - FLANS; HW_I = HW_O - ET            # 137 / 134
YC = 216.0                         # karıştırıcı = kâse merkezi
RS = 129.0                         # karıştırıcı süpürme yarıçapı (duvara 5)
RF_I = 8.0                         # boğaz dudağı radyusu (iç)
Y_UST = H_ - 8.0
Y_DOLUM = Y_UST - 20.0
ZF, ZB = D_ / 2, -D_ / 2
KOPRU = 73.0                       # köprü yarı boyu (ağız 25 + kapalı hatve 48)
AGIZ_Z, AGIZ_X = 25.0, 22.5        # ağız yarı ölçüleri (50 × 45)
R_KANAT = 28.0
GIRIS = [(195.0, 165.0, 30.0), (165.0, 125.0, 40.0), (125.0, 73.0, 52.0), (73.0, 25.0, 52.0)]   # |z| bas, son, hatve (akış yönünde)
def r_mil(az):                     # konik mil: |z| 195'te Ø42 → |z| 110'da Ø20
    return 10.0 if az <= 110.0 else 10.0 + 11.0 * (az - 110.0) / 85.0


# ---------------- KADEH KESİT ----------------
def kesit(hw, rt, rf, y_ust=None, ag=None):
    """saat yönünde açık profil (sağ üst → tekne altı → sol üst). ag=(x_agiz) verilirse İKİ parça döner (ağız kesik)."""
    Rb = hw; yj_c = None
    F = (rt + rf, YC - math.sqrt((Rb + rf) ** 2 - (rt + rf) ** 2))            # dudak radyusu merkezi (duvarın içinde)
    sag = [(hw, Y_UST if y_ust is None else y_ust), (hw, YC)]
    a_bit = math.atan2(YC - F[1], F[0])                                       # kâse yayında dudağa teğet noktanın açısı
    n = 44
    for i in range(1, n + 1):
        a = a_bit * i / n                                                     # 0 (kâse üst kenarı) → dudağa teğet nokta
        sag.append((Rb * math.cos(a), YC - Rb * math.sin(a)))
    b0 = math.atan2(YC - F[1], -F[0]); b1 = math.pi                           # dudak yayı: F çevresinde, kâse teğetinden dik duvara
    for i in range(1, 11):
        b = b0 + (b1 - b0) * i / 10.0
        sag.append((F[0] + rf * math.cos(b), F[1] + rf * math.sin(b)))
    sag.append((rt, CY))
    sol = [(-x, y) for x, y in reversed(sag)]
    if ag is None:
        yay = [(rt * math.cos(-math.pi * i / 48), CY + rt * math.sin(-math.pi * i / 48)) for i in range(1, 48)]
        return sag + yay + sol
    a1 = -math.acos(ag / rt)
    y1 = [(rt * math.cos(a1 * i / 14), CY + rt * math.sin(a1 * i / 14)) for i in range(1, 15)]
    y2 = [(-x, y) for x, y in reversed(y1)]
    return sag + y1, y2 + sol


def yari_ic(y):
    if y < CY - RT_I: return 0.0
    if y < CY: return math.sqrt(max(0.0, RT_I ** 2 - (y - CY) ** 2))
    yj = YC - math.sqrt(HW_I ** 2 - RT_I ** 2)
    if y < yj: return RT_I
    if y < YC: return math.sqrt(max(0.0, HW_I ** 2 - (y - YC) ** 2))
    return HW_I


def hacim_L(y_son):
    a, dy, y = 0.0, 0.25, CY - RT_I
    while y < y_son:
        a += 2 * yari_ic(y + dy / 2) * dy; y += dy
    return a * (D_ - 2 * TP) / 1e6


def dolum_kotu(litre):
    y = CY - RT_I
    while hacim_L(y) < litre and y < Y_DOLUM: y += 1.0
    return y


def S(m):
    """mm → m"""
    m.P = [(p[0] * MM, p[1] * MM, p[2] * MM) for p in m.P]; return m


def cizgi_yuz(pts_a, pts_b, n):
    m = Mesh()
    for i in range(len(pts_a) - 1):
        m.quad(pts_a[i], pts_a[i + 1], pts_b[i + 1], pts_b[i], n)
    return m.duzelt()


def govde():
    P = []
    for adi, hw, rt, rf, isr in (("govde_dis", HW_O, RT_O, RF_I - ET, 1.0), ("govde_ic", HW_I, RT_I, RF_I, -1.0)):
        tam = kesit(hw, rt, rf); sag, sol = kesit(hw, rt, rf, ag=AGIZ_X)
        m = ekstruzyon(tam, ZB + TP, -AGIZ_Z, isr); m.ekle(ekstruzyon(tam, AGIZ_Z, ZF - TP, isr))
        m.ekle(ekstruzyon(sag, -AGIZ_Z, AGIZ_Z, isr)); m.ekle(ekstruzyon(sol, -AGIZ_Z, AGIZ_Z, isr))
        P.append((adi, S(m), "cam"))
    # ağız kesit yüzleri (cidar kalınlığı görünür)
    k = Mesh(); N = 12
    for z, nz in ((AGIZ_Z, -1.0), (-AGIZ_Z, 1.0)):
        for i in range(N):
            x0 = -AGIZ_X + 2 * AGIZ_X * i / N; x1 = -AGIZ_X + 2 * AGIZ_X * (i + 1) / N
            yi = lambda x: CY - math.sqrt(RT_I ** 2 - x * x); yo = lambda x: CY - math.sqrt(RT_O ** 2 - x * x)
            k.quad((x0, yo(x0), z), (x1, yo(x1), z), (x1, yi(x1), z), (x0, yi(x0), z), (0, 0, nz))
    for s in (1.0, -1.0):
        x = s * AGIZ_X; yi = CY - math.sqrt(RT_I ** 2 - x * x); yo = CY - math.sqrt(RT_O ** 2 - x * x)
        k.quad((x, yo, -AGIZ_Z), (x, yo, AGIZ_Z), (x, yi, AGIZ_Z), (x, yi, -AGIZ_Z), (-s, 0, 0))
    P.append(("agiz_kesit", S(k.duzelt()), "cam"))
    return P


def kopru():
    """boğazın üstünü ortada kapatan yay plaka: üst yüzü kâse dairesinin devamı (sıyırıcı üstünden kayar)"""
    m = Mesh(); N = 16; xk = 40.0
    ust = lambda x: YC - math.sqrt(HW_I ** 2 - x * x); alt = lambda x: YC - math.sqrt((HW_I + ET) ** 2 - x * x)
    for i in range(N):
        x0 = -xk + 2 * xk * i / N; x1 = -xk + 2 * xk * (i + 1) / N
        n0 = unit((-x0, YC - ust(x0), 0)); n1 = unit((-x1, YC - ust(x1), 0))
        m.quad((x0, ust(x0), -KOPRU), (x0, ust(x0), KOPRU), (x1, ust(x1), KOPRU), (x1, ust(x1), -KOPRU), n0, n0, n1, n1)
        m.quad((x0, alt(x0), -KOPRU), (x1, alt(x1), -KOPRU), (x1, alt(x1), KOPRU), (x0, alt(x0), KOPRU), mul(n0, -1), mul(n1, -1), mul(n1, -1), mul(n0, -1))
        for z, nz in ((KOPRU, 1.0), (-KOPRU, -1.0)):
            m.quad((x0, alt(x0), z), (x1, alt(x1), z), (x1, ust(x1), z), (x0, ust(x0), z), (0, 0, nz))
    return S(m.duzelt())


def kanat(z_a, z_b, el, faz_son, kal=3.0):
    """değişken hatveli, konik mile oturan kanat · z_a → z_b akış yönü DEĞİL, küçükten büyüğe z · el=+1 SAĞ el
    faz_son: kanadın AĞIZ tarafındaki ucunun açısı"""
    def hatve(az):
        for b, s, p in GIRIS:
            if s <= az <= b: return p
        return GIRIS[-1][2]
    dz = 1.0; n = int(round((z_b - z_a) / dz)); zs = [z_a + (z_b - z_a) * i / n for i in range(n + 1)]
    th = [0.0]
    for i in range(n):
        zm = (zs[i] + zs[i + 1]) / 2; th.append(th[-1] + el * 2 * math.pi * (zs[i + 1] - zs[i]) / hatve(abs(zm)))
    uc = 0 if abs(zs[0]) < abs(zs[-1]) else n                                 # ağız tarafındaki uç
    th = [t - th[uc] + faz_son for t in th]
    m = Mesh(); k = kal / 2.0; on, arka, ken = [], [], []
    for i in range(n + 1):
        z, t = zs[i], th[i]; ca, sa = math.cos(t), math.sin(t); c = el * hatve(abs(z)) / (2 * math.pi)
        so, sk = [], []
        for r in (r_mil(abs(z)), R_KANAT):
            nn = unit((c * sa, -c * ca, r))
            so.append(m.v((r * ca, CY + r * sa, z + k), nn)); sk.append(m.v((r * ca, CY + r * sa, z - k), mul(nn, -1)))
        on.append(so); arka.append(sk)
        ken.append((m.v((R_KANAT * ca, CY + R_KANAT * sa, z + k), (ca, sa, 0)), m.v((R_KANAT * ca, CY + R_KANAT * sa, z - k), (ca, sa, 0))))
    for i in range(n):
        m.I += [on[i][0], on[i][1], on[i + 1][1], on[i][0], on[i + 1][1], on[i + 1][0]]
        m.I += [arka[i][0], arka[i + 1][1], arka[i][1], arka[i][0], arka[i + 1][0], arka[i + 1][1]]
        m.I += [ken[i][0], ken[i][1], ken[i + 1][1], ken[i][0], ken[i + 1][1], ken[i + 1][0]]
    return S(m.duzelt())


def cubuk(p0, p1, r, seg=10):
    return S(silindir(p0, p1, r, seg=seg))


def kasar_dolgu(y_dol):
    """kabın içindeki rende kaşar: iç kesit − 0,6 mm, düz üst yüz"""
    pts = [(max(0.0, yari_ic(y) - 0.6), y) for y in [CY - RT_I + 0.6 + (y_dol - CY + RT_I - 0.6) * i / 90.0 for i in range(91)]]
    sag = list(reversed(pts)); tam = sag + [(-x, y) for x, y in pts]
    z0, z1 = ZB + TP + 0.6, ZF - TP - 0.6
    m = ekstruzyon(tam, z0, z1, 1.0)
    for i in range(len(pts) - 1):
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        m.quad((-xa, ya, z1), (xa, ya, z1), (xb, yb, z1), (-xb, yb, z1), (0, 0, 1)); m.quad((xa, ya, z0), (-xa, ya, z0), (-xb, yb, z0), (xb, yb, z0), (0, 0, -1))
    x = pts[-1][0]; m.quad((-x, y_dol, z1), (x, y_dol, z1), (x, y_dol, z0), (-x, y_dol, z0), (0, 1, 0))
    return S(m.duzelt())


def model(dozaj=False):
    P = []
    def ekle(adi, mesh, mal, grup=None): P.append((adi, mesh, mal, grup))
    for adi, m, mal in govde(): ekle(adi, m, mal)
    ekle("kopru", kopru(), "cam")

    # uç plakaları · flanş · kapak
    for adi, za, zc in (("plaka_on", ZF, ZF - TP), ("plaka_arka", ZB + TP, ZB)):
        ekle(adi, uc_plakasi(W_ * MM, Y_UST * MM, za * MM, zc * MM, rc=12 * MM, rb=8 * MM, ayak=34 * MM, kemer_h=12 * MM), "cam")
    ekle("flans", rr_cerceve(W_ * MM, D_ * MM, 12 * MM, 2 * HW_I * MM, (D_ - 2 * TP) * MM, 6 * MM, (Y_UST - 4) * MM, Y_UST * MM), "cam")
    ekle("kapak", rr_plaka(W_ * MM, D_ * MM, 12 * MM, Y_UST * MM, (Y_UST + 4) * MM), "cam")
    ekle("kapak_tutamak", rr_plaka(120 * MM, 22 * MM, 9 * MM, (Y_UST + 4) * MM, (Y_UST + 8) * MM), "cam")

    # ---- HELEZON (grup: döner) ----
    G = "helezon"
    ekle("mil_orta", cubuk((0, CY, -110), (0, CY, 110), 10.0, 24), "pom", G)
    ekle("mil_konik_arka", S(silindir((0, CY, -195), (0, CY, -110), 21.0, 10.0, seg=28)), "pom", G)
    ekle("mil_konik_on", S(silindir((0, CY, 110), (0, CY, 195), 10.0, 21.0, seg=28)), "pom", G)
    ekle("mil_arka_uc", cubuk((0, CY, -204), (0, CY, -195), 10.0, 24), "pom", G)
    ekle("mil_on_uc", cubuk((0, CY, 195), (0, CY, 206), 8.0, 24), "pom", G)
    ekle("kanat_on_SAG_el", kanat(AGIZ_Z, 195.0, +1, 0.0), "pom", G)                       # ön yarı: SAĞ el → −z'ye (ortaya) iter
    ekle("kanat_arka_SOL_el", kanat(-195.0, -AGIZ_Z, -1, math.pi), "pom", G)               # arka yarı: SOL el → +z'ye (ortaya) iter · uç 180° farklı
    for a in (0.0, 90.0):                                                                  # ağız üstü itici kanatçıklar (haç)
        t = math.radians(a + 45.0); ca, sa = math.cos(t), math.sin(t); pm = Mesh()
        for s in (1, -1):
            p = [(s * (10 * ca) - 2 * sa, s * (10 * sa) + 2 * ca), (s * (27 * ca) - 2 * sa, s * (27 * sa) + 2 * ca),
                 (s * (27 * ca) + 2 * sa, s * (27 * sa) - 2 * ca), (s * (10 * ca) + 2 * sa, s * (10 * sa) - 2 * ca)]
            for z, nz in ((20.0, 1.0), (-20.0, -1.0)):
                pm.quad((p[0][0], CY + p[0][1], z), (p[1][0], CY + p[1][1], z), (p[2][0], CY + p[2][1], z), (p[3][0], CY + p[3][1], z), (0, 0, nz))
            for i in range(4):
                q, r = p[i], p[(i + 1) % 4]; nn = unit((r[1] - q[1], -(r[0] - q[0]), 0))
                pm.quad((q[0], CY + q[1], -20.0), (r[0], CY + r[1], -20.0), (r[0], CY + r[1], 20.0), (q[0], CY + q[1], 20.0), nn)
        ekle("itici_%d" % int(a), S(pm.duzelt()), "pom", G)
    ekle("kaplin_helezon", hac_kaplin(0, CY * MM, ZB * MM, -1, 15 * MM, 24 * MM, 21 * MM), "pom", G)

    # arka yatak flanşı + vidalar (sabit)
    ekle("kaplin_flans", S(silindir((0, CY, ZB), (0, CY, ZB - 5), 27.0, seg=30)), "pom")
    for a in (45, 135, 225, 315):
        b, y = vida(24 * MM * math.cos(math.radians(a)) * 0.82, CY * MM + 24 * MM * math.sin(math.radians(a)) * 0.82, (ZB - 5) * MM, -1)
        ekle("vida_kaplin_%d" % a, b, "celik"); ekle("yiv_kaplin_%d" % a, y, "koyu")

    # ön YATAK KAPAĞI (çeyrek tur bayonet) — sökünce helezon öne çekilir
    ekle("yatak_kapagi", S(silindir((0, CY, ZF), (0, CY, ZF + 9), 39.0, 36.0, seg=36)), "pom")
    ekle("yatak_gobek", S(silindir((0, CY, ZF + 9), (0, CY, ZF + 16), 16.0, 14.0, seg=28)), "pom")
    ekle("yatak_tutamak", S(kutu(-30, 30, CY - 4, CY + 4, ZF + 9, ZF + 20)), "pom")
    for a in (30, 150, 270):
        t = math.radians(a)
        ekle("bayonet_%d" % a, S(silindir((41 * math.cos(t), CY + 41 * math.sin(t), ZF), (41 * math.cos(t), CY + 41 * math.sin(t), ZF + 6), 5.0, seg=16)), "celik")

    # ---- KARIŞTIRICI KAFESİ (grup: ters yöne döner) ----
    K = "karistirici"
    ekle("kar_mil", cubuk((0, YC, ZB - 6), (0, YC, ZF + 8), 6.0, 16), "celik", K)
    CUB = [(0.0, RS), (180.0, RS), (90.0, 86.0), (270.0, 43.0)]                            # (açı, yarıçap) boyuna çubuklar
    for i, (a, r) in enumerate(CUB):
        t = math.radians(a); x, y = r * math.cos(t), YC + r * math.sin(t)
        ekle("kar_cubuk_%d" % i, cubuk((x, y, -186), (x, y, 186), 3.0), "celik", K)
        for z in (-186.0, 0.0, 186.0): ekle("kar_kol_%d_%d" % (i, int(z)), cubuk((0, YC, z), (x, y, z), 3.5), "celik", K)
    for i, a in enumerate((0.0, 180.0)):                                                   # silikon sıyırıcılar dış çubuklarda
        s = 1.0 if a == 0.0 else -1.0
        ekle("siyirici_%d" % i, S(kutu(min(s * (RS - 1), s * (HW_I - 0.5)), max(s * (RS - 1), s * (HW_I - 0.5)), YC - 1.2, YC + 1.2, -184, 184)), "silikon", K)
    ekle("kar_kaplin", hac_kaplin(0, YC * MM, ZB * MM, -1, 12 * MM, 20 * MM, 17 * MM), "pom", K)
    ekle("kar_tutamak", S(silindir((0, YC, ZF + 12), (0, YC, ZF + 62), 10.5, seg=26)), "pom", K)
    ekle("kar_tutamak_uc", S(silindir((0, YC, ZF + 62), (0, YC, ZF + 66), 10.5, 8.0, seg=26)), "pom", K)
    ekle("kar_gobek_on", S(silindir((0, YC, ZF), (0, YC, ZF + 12), 14.0, 12.0, seg=26)), "pom")
    for s in (1, -1):
        ekle("gobek_kulak_%s" % ("a" if s > 0 else "b"), S(silindir((s * 19, YC, ZF), (s * 19, YC, ZF + 4), 6.0, seg=18)), "pom")
        b, y = vida(s * 19 * MM, YC * MM, (ZF + 4) * MM, 1); ekle("vida_gobek_%s" % ("a" if s > 0 else "b"), b, "celik"); ekle("yiv_gobek_%s" % ("a" if s > 0 else "b"), y, "koyu")
    zp = ZF + 20.0
    ekle("pim", cubuk((-15, YC, zp), (15, YC, zp), 2.4, 12), "pom", K); ekle("pim_bas", cubuk((15, YC, zp), (19, YC, zp), 4.5, 14), "pom", K)
    ekle("ip_halka", S(torus((-6, YC - 42, zp + 2), (0.2, 0.1, 1), 12.0, 1.3)), "pom")
    ekle("ip", cubuk((14, YC - 10, zp), (4, YC - 34, zp + 2), 0.9, 8), "pom")

    # ---- AĞIZ bileziği + menteşeli kapak ----
    yb0, yb1 = 8.5, CY - RT_O + 0.8
    for s in (1, -1):
        ekle("agiz_bilezik_x%s" % ("a" if s > 0 else "b"), S(kutu(min(s * AGIZ_X, s * (AGIZ_X + 3)), max(s * AGIZ_X, s * (AGIZ_X + 3)), yb0, CY - math.sqrt(RT_O ** 2 - AGIZ_X ** 2), -AGIZ_Z - 3, AGIZ_Z + 3)), "cam")
        ekle("agiz_bilezik_z%s" % ("a" if s > 0 else "b"), S(kutu(-AGIZ_X, AGIZ_X, yb0, yb1, min(s * AGIZ_Z, s * (AGIZ_Z + 3)), max(s * AGIZ_Z, s * (AGIZ_Z + 3)))), "cam")
    ekle("mentese", cubuk((-AGIZ_X - 8, 6.0, AGIZ_Z + 6), (AGIZ_X + 8, 6.0, AGIZ_Z + 6), 2.5, 12), "celik")
    if dozaj: ekle("agiz_kapagi_ACIK", S(kutu(-AGIZ_X - 4, AGIZ_X + 4, -50.0, 6.0, AGIZ_Z + 5, AGIZ_Z + 8)), "cam")
    else:     ekle("agiz_kapagi", S(kutu(-AGIZ_X - 4, AGIZ_X + 4, 5.0, 8.0, -AGIZ_Z - 5, AGIZ_Z + 8)), "cam")
    ekle("kapak_kolu", S(kutu(AGIZ_X + 5, AGIZ_X + 9, 1.0, 7.0, 8.0, AGIZ_Z + 8)), "celik")

    # asma deliği · uyarı etiketleri · yazılı bantlar
    ekle("asma_deligi", S(torus((-W_ / 2 + 30, Y_UST - 34, ZF - TP / 2), (0, 0, 1), 15.0, 3.2)), "cam")
    e0, e1 = (Y_UST - 56) * MM, (Y_UST - 8) * MM; ez = (D_ / 2 - TP - 3) * MM
    ekle("bant_ad", etiket_yuzu(-(HW_O + 0.4) * MM, e0, e1, -ez, ez, -1), "etiket_ad")
    ekle("bant_montaj", etiket_yuzu((HW_O + 0.4) * MM, e0, e1, ez, -ez, 1), "etiket_montaj")
    for adi, xx, nx in (("bant_ad_arka", -(HW_O + 0.2) * MM, 1), ("bant_montaj_arka", (HW_O + 0.2) * MM, -1)):
        ar = Mesh(); ar.quad((xx, e0, -ez), (xx, e0, ez), (xx, e1, ez), (xx, e1, -ez), (nx, 0, 0)); ekle(adi, ar.duzelt(), "sari_arka")
    ekle("uyari_1", S(kutu(-34, -12, YC + 24, YC + 46, ZF, ZF + 0.4)), "sari")
    ekle("uyari_2", S(kutu(-W_ / 2 + 8, -W_ / 2 + 28, CY + 50, CY + 70, ZF, ZF + 0.4)), "sari")

    if dozaj:
        # ---- MAKİNE TARAFI: pimli dağıtıcı + huni + tabla + pide (kotlar pafta HAT_ATOSA_TABLALI v2: kaset tabanı 1627, tabla dozajda 1440) ----
        yd = -42.0
        for adi, x0, x1, z0, z1 in (("dag_govde_sag", 33, 36, -36, 40), ("dag_govde_sol", -36, -33, -36, 40), ("dag_govde_on", -36, 36, 37, 40), ("dag_govde_arka", -36, 36, -36, -33)):
            ekle(adi, S(kutu(x0, x1, -82.0, 2.0, z0, z1)), "cam")
        DG = "dagitici"
        ekle("dag_gobek", cubuk((0, yd, -30), (0, yd, 30), 11.0, 22), "pom", DG)
        ekle("dag_mil", cubuk((0, yd, -92), (0, yd, -30), 4.0, 12), "celik", DG)
        for sira in range(4):
            t = math.radians(90.0 * sira)
            for j in range(5):
                z = -24.0 + 12.0 * j + (6.0 if sira % 2 else 0.0)
                if z > 28: continue
                ekle("dag_pim_%d_%d" % (sira, j), cubuk((11 * math.cos(t), yd + 11 * math.sin(t), z), (29 * math.cos(t), yd + 29 * math.sin(t), z), 2.5, 10), "celik", DG)
        ekle("dag_motor", cubuk((0, yd, -142), (0, yd, -92), 18.0, 24), "koyu")
        ekle("huni", S(silindir((0, -82.0, 0), (0, -134.0, 0), 38.0, 27.0, seg=40, kapak=False)), "celik")
        xt, yt = 70.0, -187.0                                                  # tabla merkezi nozulun 70 mm yanında (spiralin o anı)
        T = "tabla"
        ekle("tabla", S(silindir((xt, yt - 12, 0), (xt, yt, 0), 170.0, seg=64)), "celik", T)
        ekle("pide", S(silindir((xt, yt, 0), (xt, yt + 7, 0), 140.0, seg=64)), "hamur", T)
        ekle("pide_kenar", S(torus((xt, yt + 7, 0), (0, 1, 0), 133.0, 6.0, seg=64, kes=10)), "hamur", T)
        ekle("tabla_kolon", cubuk((xt, yt - 80, 0), (xt, yt - 12, 0), 20.0, 24), "koyu")
        rnd = random.Random(7); ks = Mesh(); r0, r1, N = 12.0, 122.0, 260                  # pide üstünde spiral: %60'ı dökülmüş an
        for i in range(N):
            t = 0.60 * i / N; r = math.sqrt(r0 * r0 + (r1 * r1 - r0 * r0) * (1 - t)); a = 2 * math.pi * 7.0 * t + rnd.uniform(-0.25, 0.25)
            rr = r + rnd.uniform(-16, 16); x, z = xt + rr * math.cos(a), rr * math.sin(a); L, w = rnd.uniform(8, 16), 1.5; b = rnd.uniform(0, math.pi)
            dx, dz = L * math.cos(b), L * math.sin(b); nx_, nz_ = -w * math.sin(b), w * math.cos(b); y = yt + 7.4 + rnd.uniform(0, 4)
            ks.quad((x - dx - nx_, y, z - dz - nz_), (x + dx - nx_, y, z + dz - nz_), (x + dx + nx_, y, z + dz + nz_), (x - dx + nx_, y, z - dz + nz_), (0, 1, 0))
        ekle("kasar_pide_ustu", S(ks.duzelt()), "kasar", T)
        dk = Mesh()                                                                         # düşen kaşar (sabit ipucu)
        for i in range(34):
            y = rnd.uniform(-178, 10); x, z = rnd.uniform(-14, 14), rnd.uniform(-14, 14); L = rnd.uniform(6, 12); b = rnd.uniform(0, math.pi)
            dk.ekle(kutu(x - L * math.cos(b) / 2 - 1, x + L * math.cos(b) / 2 + 1, y, y + L * abs(math.sin(b)) + 2, z - 1, z + 1))
        ekle("kasar_dusen", S(dk), "kasar")
        ydol = dolum_kotu(8.8 / RHO)
        ekle("kasar_dolgu", kasar_dolgu(ydol), "kasar_dolgu")
    return P


# ---------------- GLB (gruplar + animasyon) ----------------
DONGU = 8.0                                        # sn · tek döngüde: helezon +1 tur (7,5 dev/dk) · karıştırıcı −1 · dağıtıcı +20 (150 dev/dk) · tabla +4 (30 dev/dk)
GRUP = {"helezon": dict(pivot=(0, CY * MM, 0), eksen="z", tur=1), "karistirici": dict(pivot=(0, YC * MM, 0), eksen="z", tur=-1),
        "dagitici": dict(pivot=(0, -42 * MM, 0), eksen="z", tur=20), "tabla": dict(pivot=(70 * MM, -187 * MM, 0), eksen="y", tur=4)}


def glb_yaz(yol, parcalar, dokular):
    adlar = list(MALZEME.keys()); blob, views, accs, meshes, nodes = [], [], [], [], []; off = [0]

    def gomu(b, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(b)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(b); off[0] += len(b); return len(views) - 1

    cocuk = {}; kok = []
    for adi, m, mal, grup in parcalar:
        vp = gomu(b"".join(struct.pack("<3f", *p) for p in m.P), 34962); vn = gomu(b"".join(struct.pack("<3f", *n) for n in m.N), 34962)
        vi = gomu(b"".join(struct.pack("<I", i) for i in m.I), 34963)
        mn = [min(p[k] for p in m.P) for k in range(3)]; mx = [max(p[k] for p in m.P) for k in range(3)]
        accs.append({"bufferView": vp, "componentType": 5126, "count": len(m.P), "type": "VEC3", "min": mn, "max": mx})
        accs.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"})
        accs.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
        attr = {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}; ind = len(accs) - 1
        if m.UV:
            vu = gomu(b"".join(struct.pack("<2f", *u) for u in m.UV), 34962)
            accs.append({"bufferView": vu, "componentType": 5126, "count": len(m.UV), "type": "VEC2"}); attr["TEXCOORD_0"] = len(accs) - 1
        meshes.append({"name": adi, "primitives": [{"attributes": attr, "indices": ind, "material": adlar.index(mal)}]})
        nd = {"mesh": len(meshes) - 1, "name": adi}
        if grup:
            pv = GRUP[grup]["pivot"]; nd["translation"] = [-pv[0], -pv[1], -pv[2]]; cocuk.setdefault(grup, []).append(len(nodes))
        else: kok.append(len(nodes))
        nodes.append(nd)
    kanallar, samplerlar = [], []
    for g, c in cocuk.items():
        bil = GRUP[g]; nodes.append({"name": "GRUP_" + g, "translation": list(bil["pivot"]), "children": c}); gi = len(nodes) - 1; kok.append(gi)
        n = abs(bil["tur"]) * 8; ts, qs = [], []
        for i in range(n + 1):
            t = DONGU * i / n; a = 2 * math.pi * bil["tur"] * i / n; s, co = math.sin(a / 2), math.cos(a / 2)
            ts.append(t); qs.append((0.0, 0.0, s, co) if bil["eksen"] == "z" else (0.0, s, 0.0, co))
        vt = gomu(b"".join(struct.pack("<f", t) for t in ts)); accs.append({"bufferView": vt, "componentType": 5126, "count": len(ts), "type": "SCALAR", "min": [0.0], "max": [DONGU]})
        vq = gomu(b"".join(struct.pack("<4f", *q) for q in qs)); accs.append({"bufferView": vq, "componentType": 5126, "count": len(qs), "type": "VEC4"})
        samplerlar.append({"input": len(accs) - 2, "output": len(accs) - 1, "interpolation": "LINEAR"})
        kanallar.append({"sampler": len(samplerlar) - 1, "target": {"node": gi, "path": "rotation"}})
    images, textures, doku_idx = [], [], {}
    for k, veri in dokular.items():
        images.append({"bufferView": gomu(veri), "mimeType": "image/png"}); textures.append({"source": len(images) - 1, "sampler": 0}); doku_idx[k] = len(textures) - 1
    mats = []
    for k in adlar:
        d = MALZEME[k]; pbr = {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]}
        if d.get("doku"): pbr["baseColorTexture"] = {"index": doku_idx[d["doku"]]}
        mm = {"name": k, "pbrMetallicRoughness": pbr, "doubleSided": not d.get("tekyuz", False)}
        if d.get("saydam"): mm["alphaMode"] = "BLEND"
        mats.append(mm)
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH kaset_3d_v4"}, "scene": 0, "scenes": [{"nodes": kok}], "nodes": nodes, "meshes": meshes,
         "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}], "images": images, "textures": textures,
         "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}],
         "animations": [{"name": "calis", "channels": kanallar, "samplers": samplerlar}]}
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb)))
        f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js); f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    return len(bb) + len(js)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    V = hacim_L(Y_DOLUM); ydol = dolum_kotu(8.8 / RHO)
    print("KESIT: eksen %g · bogaz birlesimi y %.1f · kase R%g merkez y %g · karistirici R%g (alt %g, ust %g) · helezon ustu %g · kopru alti %.1f"
          % (CY, YC - math.sqrt(HW_I ** 2 - RT_I ** 2), HW_I, YC, RS, YC - RS, YC + RS, CY + R_KANAT, YC - HW_I - ET))
    print("HACIM: dolum cizgisine kadar %.1f L · 2 gunluk 8,8 kg @ %.2f g/mL = %.1f L → dolum kotu y %.0f (%%%.0f)" % (V, RHO, 8.8 / RHO, ydol, 100 * 8.8 / RHO / V))
    for b, s, p in GIRIS:
        dm = 2 * r_mil((b + s) / 2); Vt, eta, a = roberts(56.0, dm, p)
        print("  kanat |z| %3.0f→%3.0f · hatve %2.0f · mil O%.0f · Vt %.0f mL · etaVR %.2f · kapasite %.0f mL/tur (tam dolu, fi_s 30)" % (b, s, p, dm, Vt, eta, Vt * eta))
    MONTAJ = ["HELEZONU|ÖNDEN SÜR", "YATAK KAPAĞI|ÇEYREK TUR", "KARIŞTIRICIYI|TAK · PİMLE", "KABI YUVAYA|SÜR"]
    dokular = {"ad": doku_ad("KAŞAR KABI", "bu yönde tak  ·  280 × 400 × 360 mm  ·  %s L  ·  çıkış ORTADA alttan" % ("%.1f" % V).replace(".", ","), ok_sol=True), "montaj": doku_montaj(MONTAJ)}
    for dosya, doz in (("kasar_v4", False), ("kasar_v4_dozaj", True)):
        par = model(doz); b1 = glb_yaz(os.path.join(OUT, dosya + ".glb"), par, dokular)
        print("%s · %d parca · %d ucgen · glb %.0f KB" % (dosya, len(par), sum(len(m.I) // 3 for _, m, _, _ in par), b1 / 1024.0))
        if not doz:
            b2, prim, sorun, uyari = usdz_yaz([os.path.join(OUT, dosya + ".usdz")], dosya, [(a, m, mal) for a, m, mal, _ in par], dokular)
            print("   usdz %.0f KB · geri acildi %d prim · USD denetimi: %s" % (b2 / 1024.0, prim, "GECTI" if not sorun else "KALDI"))
            for x in sorun: print("   HATA:", x)
