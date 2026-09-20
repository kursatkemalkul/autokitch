# -*- coding: utf-8 -*-
"""AUTOKITCH · KAŞAR KABI 3D v5 (20 Eyl 2026) — UÇTAN ÇIKIŞ (Picnic / Atosa gibi) · kap 280 × 325 × 360 · ÜRETİM / DENEME İÇİN
Kemal kararları: çıkış uçtan · kap 325 derin (830 derinliğe standart motorla sığsın diye) · peynir kısa kesim · dağıtıcı ve terazi YOK.

KAP
  · kadeh kesit: helezon ekseni y 40 · tekne Ø44 (iç) · boğaz dudağı R8 · kâse R134 merkez y 195 = karıştırıcı ekseni · dik duvar 352'ye kadar
  · HELEZON Ø40 / mil Ø14 (arkada 60 mm konik Ø26) · SAĞ el · hatve 22 → 26 → 30 (kapasite akış yönünde artar, sıkışma olmaz)
    önden bakınca SAAT YÖNÜNDE döner → kaşarı öne, tüpe iter
  · ÇIKIŞ TÜPÜ ön plakadan 76 mm öne: ilk 32 mm KAPALI (çift ağızlı hatve 36 → darbe sayısı iki katı) → alt AĞIZ 36 × 38
    (merkezi ön plakadan 50 mm) → çeyrek tur YATAK KAPAĞI (sökünce helezon öne çekilir). Ağzın üstünde milde 6 çırpıcı PİM.
  · KARIŞTIRICI kafes R129 + 2 silikon sıyırıcı · helezonun TERSİNE döner · 6 dev/dk
  · ağız altında menteşeli kapak (v27 kararı): kap yuvaya girince makinedeki pim açar
MAKİNE (dozaj modelinde): ETEK (42×52 → 40×50, alt ucu pidenin 25 mm üstünde) · 2 × NMRV030 i=30 + NEMA23 (arka 95 mm'ye sığar:
  kaplin 20 + boşluk 6 + redüktör 63 = 89) · arka duvar · tabla Ø340 + pide Ø280: dış kenarda 2,5 sn bekler, dönerek içeri yürür.
Çıktı: otonom/kaset3d/kasar_v5.glb/.usdz · kasar_v5_dozaj.glb
"""
import json, math, os, random, struct
import kaset_3d_v4 as v4
from kaset_3d_v3 import (Mesh, MM, mul, unit, kutu, silindir, torus, ekstruzyon, uc_plakasi, rr_plaka, rr_cerceve, vida, hac_kaplin,
                         doku_ad, doku_montaj, etiket_yuzu, MALZEME, usdz_yaz, OUT)
from kasar_akis_model_v2 import roberts, RHO, YASA, T_DOK, r_t, KANAT, UC, AGIZ, mil_cap

W_, D_, H_ = 280.0, 325.0, 360.0
ET, TP = 3.0, 5.0
CY, RT_I, RT_O = 40.0, 22.0, 25.0
HW_O, HW_I = 137.0, 134.0
YC, RS, RF_I = 195.0, 129.0, 8.0
Y_UST, Y_DOLUM = 352.0, 332.0
ZF, ZB = D_ / 2, -D_ / 2
TUP = 76.0
R_KANAT = 20.0
for k, v in dict(CY=CY, RT_I=RT_I, RT_O=RT_O, YC=YC, RS=RS, D_=D_, ZF=ZF, ZB=ZB, HW_I=HW_I, HW_O=HW_O, Y_UST=Y_UST, Y_DOLUM=Y_DOLUM).items(): setattr(v4, k, v)
S, cubuk = v4.S, v4.cubuk


def hatve(z):
    for a, b, p in KANAT:
        if a <= z <= b: return p
    return UC["hatve"] if z > KANAT[-1][1] else KANAT[0][2]


def teta(z, z0=-155.0):
    t, n = 0.0, max(1, int(abs(z - z0)))
    for i in range(n):
        zm = z0 + (z - z0) * (i + .5) / n; t += 2 * math.pi * ((z - z0) / n) / hatve(zm)
    return t


def kanat(z_a, z_b, faz, kal=3.0):
    """SAĞ el, değişken hatveli kanat · faz = z_a'daki açı"""
    n = int(round(z_b - z_a)); zs = [z_a + (z_b - z_a) * i / n for i in range(n + 1)]; th = [faz]
    for i in range(n): th.append(th[-1] + 2 * math.pi * (zs[i + 1] - zs[i]) / hatve((zs[i] + zs[i + 1]) / 2))
    m = Mesh(); k = kal / 2.0; on, arka, ken = [], [], []
    for i in range(n + 1):
        z, t = zs[i], th[i]; ca, sa = math.cos(t), math.sin(t); c = hatve(z) / (2 * math.pi); so, sk = [], []
        for r in (mil_cap(z) / 2.0, R_KANAT):
            nn = unit((c * sa, -c * ca, r)); so.append(m.v((r * ca, CY + r * sa, z + k), nn)); sk.append(m.v((r * ca, CY + r * sa, z - k), mul(nn, -1)))
        on.append(so); arka.append(sk)
        ken.append((m.v((R_KANAT * ca, CY + R_KANAT * sa, z + k), (ca, sa, 0)), m.v((R_KANAT * ca, CY + R_KANAT * sa, z - k), (ca, sa, 0))))
    for i in range(n):
        m.I += [on[i][0], on[i][1], on[i + 1][1], on[i][0], on[i + 1][1], on[i + 1][0]]
        m.I += [arka[i][0], arka[i + 1][1], arka[i][1], arka[i][0], arka[i + 1][0], arka[i + 1][1]]
        m.I += [ken[i][0], ken[i][1], ken[i + 1][1], ken[i][0], ken[i + 1][1], ken[i + 1][0]]
    return S(m.duzelt())


def tup():
    """şeffaf çıkış tüpü: ağız bölümünde alt tarafı açık"""
    def yay(r, a0, a1, n=40): return [(r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), CY + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    P = []
    for adi, r, isr in (("tup_dis", RT_O, 1.0), ("tup_ic", RT_I, -1.0)):
        d = math.degrees(math.asin(AGIZ["x"] / r)); tam = yay(r, 90, -270, 64)
        m = ekstruzyon(tam, ZF, AGIZ["z0"], isr); m.ekle(ekstruzyon(tam, AGIZ["z1"], ZF + TUP, isr))
        m.ekle(ekstruzyon(yay(r, 90, -90 + d, 28), AGIZ["z0"], AGIZ["z1"], isr)); m.ekle(ekstruzyon(yay(r, -90 - d, -270, 28), AGIZ["z0"], AGIZ["z1"], isr))
        P.append((adi, S(m), "cam"))
    return P


def etek(y_ust, y_alt, ust, alt, kal=2.0, zc=0.0):
    """ağız altındaki dikdörtgen etek (hafif daralan/açılan) · ust/alt = (x yarı, z yarı) iç ölçü"""
    m = Mesh()
    for ek, isr in ((0.0, -1.0), (kal, 1.0)):
        a = [(-ust[0] - ek, y_ust, zc - ust[1] - ek), (ust[0] + ek, y_ust, zc - ust[1] - ek), (ust[0] + ek, y_ust, zc + ust[1] + ek), (-ust[0] - ek, y_ust, zc + ust[1] + ek)]
        b = [(-alt[0] - ek, y_alt, zc - alt[1] - ek), (alt[0] + ek, y_alt, zc - alt[1] - ek), (alt[0] + ek, y_alt, zc + alt[1] + ek), (-alt[0] - ek, y_alt, zc + alt[1] + ek)]
        for i in range(4):
            j = (i + 1) % 4; ort = ((a[i][0] + a[j][0]) / 2, 0, (a[i][2] + a[j][2]) / 2 - zc); nn = mul(unit((ort[0], 0, ort[2])), isr)
            m.quad(a[i], a[j], b[j], b[i], nn)
    return S(m.duzelt())


def reduktor(adi, y_eks, yon, ekle, zk):
    """NMRV030 (katalog: 81 × 97 × 63, çıkış ekseni tabandan 40, giriş ekseni +30, flanş yüzü eksenden 55) + NEMA23 57 × 57 × 76"""
    z1 = zk - 26.0; z0 = z1 - 63.0
    ekle(adi + "_govde", S(kutu(-40.5, 40.5, y_eks - 40, y_eks + 57, z0, z1)), "koyu")
    ekle(adi + "_flans", S(kutu(min(yon * 41, yon * 55), max(yon * 41, yon * 55), y_eks + 2, y_eks + 58, z0 + 3, z1 - 3)), "celik")
    ekle(adi + "_motor", S(kutu(min(yon * 55, yon * 131), max(yon * 55, yon * 131), y_eks + 1.5, y_eks + 58.5, z0 + 3, z1 - 3)), "koyu")
    ekle(adi + "_mil", cubuk((0, y_eks, z1), (0, y_eks, z1 + 8), 7.0, 16), "celik")
    ekle(adi + "_yuva", S(silindir((0, y_eks, z1 + 6), (0, y_eks, zk - 4), 19.0, seg=26)), "celik")


def model(dozaj=False):
    P = []
    def ekle(adi, mesh, mal, grup=None): P.append((adi, mesh, mal, grup))
    for adi, hw, rt, rf, isr in (("govde_dis", HW_O, RT_O, RF_I - ET, 1.0), ("govde_ic", HW_I, RT_I, RF_I, -1.0)):
        ekle(adi, S(ekstruzyon(v4.kesit(hw, rt, rf), ZB + TP, ZF - TP, isr)), "cam")
    for adi, za, zc in (("plaka_on", ZF, ZF - TP), ("plaka_arka", ZB + TP, ZB)):
        ekle(adi, uc_plakasi(W_ * MM, Y_UST * MM, za * MM, zc * MM, rc=12 * MM, rb=8 * MM, ayak=34 * MM, kemer_h=10 * MM), "cam")
    ekle("flans", rr_cerceve(W_ * MM, D_ * MM, 12 * MM, 2 * HW_I * MM, (D_ - 2 * TP) * MM, 6 * MM, (Y_UST - 4) * MM, Y_UST * MM), "cam")
    ekle("kapak", rr_plaka(W_ * MM, D_ * MM, 12 * MM, Y_UST * MM, (Y_UST + 4) * MM), "cam")
    ekle("kapak_tutamak", rr_plaka(120 * MM, 22 * MM, 9 * MM, (Y_UST + 4) * MM, (Y_UST + 8) * MM), "cam")
    for adi, m, mal in tup(): ekle(adi, m, mal)

    # ---- HELEZON (grup) ----
    G = "helezon"
    ekle("mil_konik", S(silindir((0, CY, -157.5), (0, CY, -97.5), 13.0, 7.0, seg=26)), "pom", G)
    ekle("mil", cubuk((0, CY, -97.5), (0, CY, 232.0), 7.0, 22), "pom", G)
    ekle("mil_arka", cubuk((0, CY, ZB - 2), (0, CY, -157.5), 9.0, 22), "pom", G)
    ekle("mil_on_muylu", cubuk((0, CY, 232.0), (0, CY, ZF + TUP + 5), 5.0, 18), "celik", G)
    ekle("kanat_ana_SAG_el", kanat(-155.0, ZF, 0.0), "pom", G)
    t_uc = teta(ZF)
    ekle("kanat_uc_A", kanat(ZF, AGIZ["z0"], t_uc), "pom", G); ekle("kanat_uc_B", kanat(ZF, AGIZ["z0"], t_uc + math.pi), "pom", G)
    for sira, a0 in enumerate((20.0, 200.0)):
        for j, z in enumerate((201.0, 212.5, 224.0)):
            t = math.radians(a0 + 55.0 * j)
            ekle("pim_%d_%d" % (sira, j), cubuk((7 * math.cos(t), CY + 7 * math.sin(t), z), (19 * math.cos(t), CY + 19 * math.sin(t), z), 2.0, 10), "celik", G)
    ekle("kaplin_helezon", hac_kaplin(0, CY * MM, ZB * MM, -1, 13 * MM, 20 * MM, 18 * MM), "pom", G)
    ekle("kaplin_flans", S(silindir((0, CY, ZB), (0, CY, ZB - 4), 24.0, seg=30)), "pom")
    for a in (45, 135, 225, 315):
        b, y = vida(21 * MM * math.cos(math.radians(a)) * 0.82, CY * MM + 21 * MM * math.sin(math.radians(a)) * 0.82, (ZB - 4) * MM, -1)
        ekle("vida_kaplin_%d" % a, b, "celik"); ekle("yiv_kaplin_%d" % a, y, "koyu")

    # ön yatak kapağı (çeyrek tur) + tüp bileziği
    zt = ZF + TUP
    ekle("yatak_kapagi", S(silindir((0, CY, zt), (0, CY, zt + 8), 29.0, 27.0, seg=36)), "pom")
    ekle("yatak_tutamak", S(kutu(-24, 24, CY - 3.5, CY + 3.5, zt + 8, zt + 18)), "pom")
    for a in (30, 150, 270):
        t = math.radians(a); ekle("bayonet_%d" % a, S(silindir((29 * math.cos(t), CY + 29 * math.sin(t), zt - 6), (29 * math.cos(t), CY + 29 * math.sin(t), zt), 3.5, seg=14)), "celik")
    ekle("tup_bilezik", S(silindir((0, CY, ZF), (0, CY, ZF + 6), 33.0, 30.0, seg=36)), "pom")

    # ---- KARIŞTIRICI (grup) ----
    Kg = "karistirici"; zk = ZF - TP - 9.5
    ekle("kar_mil", cubuk((0, YC, ZB - 6), (0, YC, ZF + 8), 6.0, 16), "celik", Kg)
    for i, (a, r) in enumerate([(0.0, RS), (180.0, RS), (90.0, 86.0), (270.0, 43.0)]):
        t = math.radians(a); x, y = r * math.cos(t), YC + r * math.sin(t)
        ekle("kar_cubuk_%d" % i, cubuk((x, y, -zk), (x, y, zk), 3.0), "celik", Kg)
        for z in (-zk, 0.0, zk): ekle("kar_kol_%d_%d" % (i, int(z)), cubuk((0, YC, z), (x, y, z), 3.5), "celik", Kg)
    for i, s in enumerate((1.0, -1.0)):
        ekle("siyirici_%d" % i, S(kutu(min(s * (RS - 1), s * (HW_I - 0.5)), max(s * (RS - 1), s * (HW_I - 0.5)), YC - 1.2, YC + 1.2, -zk + 2, zk - 2)), "silikon", Kg)
    ekle("kar_kaplin", hac_kaplin(0, YC * MM, ZB * MM, -1, 12 * MM, 20 * MM, 17 * MM), "pom", Kg)
    ekle("kar_tutamak", S(silindir((0, YC, ZF + 12), (0, YC, ZF + 58), 10.5, seg=26)), "pom", Kg)
    ekle("kar_tutamak_uc", S(silindir((0, YC, ZF + 58), (0, YC, ZF + 62), 10.5, 8.0, seg=26)), "pom", Kg)
    ekle("kar_gobek_on", S(silindir((0, YC, ZF), (0, YC, ZF + 12), 14.0, 12.0, seg=26)), "pom")
    for s in (1, -1):
        h = "a" if s > 0 else "b"
        ekle("gobek_kulak_" + h, S(silindir((s * 19, YC, ZF), (s * 19, YC, ZF + 4), 6.0, seg=18)), "pom")
        b, y = vida(s * 19 * MM, YC * MM, (ZF + 4) * MM, 1); ekle("vida_gobek_" + h, b, "celik"); ekle("yiv_gobek_" + h, y, "koyu")
    zp = ZF + 20.0
    ekle("pim", cubuk((-15, YC, zp), (15, YC, zp), 2.4, 12), "pom", Kg); ekle("pim_bas", cubuk((15, YC, zp), (19, YC, zp), 4.5, 14), "pom", Kg)
    ekle("ip_halka", S(torus((-6, YC - 42, zp + 2), (0.2, 0.1, 1), 12.0, 1.3)), "pom"); ekle("ip", cubuk((14, YC - 10, zp), (4, YC - 34, zp + 2), 0.9, 8), "pom")

    # kap çekme tutamağı (sabit)
    for s in (1, -1): ekle("tutamak_ayak_%s" % ("a" if s > 0 else "b"), cubuk((s * 55, 300, ZF), (s * 55, 300, ZF + 32), 5.0, 14), "pom")
    ekle("tutamak_cubuk", cubuk((-62, 300, ZF + 32), (62, 300, ZF + 32), 7.0, 18), "pom")

    # ---- AĞIZ bileziği + menteşeli kapak ----
    ax, az0, az1 = AGIZ["x"], AGIZ["z0"], AGIZ["z1"]; yb1 = CY - math.sqrt(RT_O ** 2 - ax ** 2); yb0 = CY - RT_O - 5.0
    for s in (1, -1):
        h = "a" if s > 0 else "b"
        ekle("agiz_bilezik_x" + h, S(kutu(min(s * ax, s * (ax + 3)), max(s * ax, s * (ax + 3)), yb0, yb1, az0 - 3, az1 + 3)), "cam")
    ekle("agiz_bilezik_za", S(kutu(-ax, ax, yb0, CY - RT_O + 0.8, az1, az1 + 3)), "cam"); ekle("agiz_bilezik_zb", S(kutu(-ax, ax, yb0, CY - RT_O + 0.8, az0 - 3, az0)), "cam")
    ekle("mentese", cubuk((-ax - 8, yb0 - 2.5, az1 + 5), (ax + 8, yb0 - 2.5, az1 + 5), 2.2, 12), "celik")
    if dozaj: ekle("agiz_kapagi_ACIK", S(kutu(-ax - 4, ax + 4, yb0 - 46, yb0 - 2, az1 + 3.5, az1 + 6.5)), "cam")
    else:     ekle("agiz_kapagi", S(kutu(-ax - 4, ax + 4, yb0 - 4, yb0 - 1, az0 - 5, az1 + 6)), "cam")
    ekle("kapak_kolu", S(kutu(ax + 5, ax + 9, yb0 - 8, yb0 - 1, az1 - 12, az1 + 6)), "celik")

    # asma deliği · etiketler
    ekle("asma_deligi", S(torus((-W_ / 2 + 30, Y_UST - 34, ZF - TP / 2), (0, 0, 1), 15.0, 3.2)), "cam")
    e0, e1 = (Y_UST - 56) * MM, (Y_UST - 8) * MM; ez = (D_ / 2 - TP - 3) * MM
    ekle("bant_ad", etiket_yuzu(-(HW_O + 0.4) * MM, e0, e1, -ez, ez, -1), "etiket_ad")
    ekle("bant_montaj", etiket_yuzu((HW_O + 0.4) * MM, e0, e1, ez, -ez, 1), "etiket_montaj")
    for adi, xx, nx in (("bant_ad_arka", -(HW_O + 0.2) * MM, 1), ("bant_montaj_arka", (HW_O + 0.2) * MM, -1)):
        ar = Mesh(); ar.quad((xx, e0, -ez), (xx, e0, ez), (xx, e1, ez), (xx, e1, -ez), (nx, 0, 0)); ekle(adi, ar.duzelt(), "sari_arka")
    ekle("uyari_1", S(kutu(-34, -12, YC + 24, YC + 46, ZF, ZF + 0.4)), "sari"); ekle("uyari_2", S(kutu(-W_ / 2 + 8, -W_ / 2 + 28, CY + 60, CY + 80, ZF, ZF + 0.4)), "sari")

    if dozaj:
        zc = (az0 + az1) / 2.0; y_pide = -(1627.0 - 1448.0); y_tabla = y_pide - 8.0            # kotlar paftadan: kaset tabanı 1627, tabla dozajda 1440
        ekle("etek", etek(yb0 - 8.0, y_pide + 25.0, (21.0, 26.0), (20.0, 25.0), 2.0, zc + 1.0), "cam")
        reduktor("red_helezon", CY, 1, ekle, ZB); reduktor("red_karistirici", YC, -1, ekle, ZB)
        ekle("arka_duvar", S(kutu(-140, 140, -20, 360, ZB - 97, ZB - 95)), "cam")
        T = "tabla"; xt = -YASA["r_dis"]
        ekle("tabla", S(silindir((xt, y_tabla - 12, zc), (xt, y_tabla, zc), 170.0, seg=64)), "celik", T)
        ekle("pide", S(silindir((xt, y_tabla, zc), (xt, y_pide - 1, zc), 140.0, seg=64)), "hamur", T)
        ekle("pide_kenar", S(torus((xt, y_pide - 1, zc), (0, 1, 0), 133.0, 6.0, seg=64, kes=10)), "hamur", T)
        ekle("tabla_kolon", cubuk((xt, y_tabla - 70, zc), (xt, y_tabla - 12, zc), 20.0, 24), "koyu", "kolon")
        rnd = random.Random(11); ks = Mesh()
        for i in range(330):                                                                   # bitmiş pide: R105'e kadar düz, 125'e doğru incelir
            while True:
                rr = 125.0 * math.sqrt(rnd.random())
                if rr < 100 or rnd.random() < (125.0 - rr) / 25.0: break
            a = rnd.uniform(0, 2 * math.pi); x, z = xt + rr * math.cos(a), zc + rr * math.sin(a); b = rnd.uniform(0, math.pi)
            dx, dz = 5 * math.cos(b), 5 * math.sin(b); nx_, nz_ = -2 * math.sin(b), 2 * math.cos(b); y = y_pide + rnd.uniform(0, 3)
            ks.quad((x - dx - nx_, y, z - dz - nz_), (x + dx - nx_, y, z + dz - nz_), (x + dx + nx_, y, z + dz + nz_), (x - dx + nx_, y, z - dz + nz_), (0, 1, 0))
        ekle("kasar_pide_ustu", S(ks.duzelt()), "kasar", T)
        dk = Mesh()
        for i in range(40):
            y = rnd.uniform(y_pide + 4, CY - RT_I); x, z = rnd.uniform(-15, 15), zc + rnd.uniform(-16, 16); dk.ekle(kutu(x - 2, x + 2, y, y + rnd.uniform(4, 9), z - 2, z + 2))
        ekle("kasar_dusen", S(dk), "kasar")
        ekle("kasar_dolgu", v4.kasar_dolgu(v4.dolum_kotu(8.8 / RHO)), "kasar_dolgu")
    return P


# ---------------- GLB: gruplar + dönme + kayma animasyonu ----------------
DONGU, DT = 12.0, 0.1                                   # 10 sn dökme + 2 sn geri dönüş
def _don(tur, sure=T_DOK): return lambda t: tur * min(t, sure) / sure
GRUP = {"helezon": dict(pivot=(0, CY * MM, 0), eksen="z", aci=_don(-7.0)),                     # 42 dev/dk · önden SAAT YÖNÜNDE
        "karistirici": dict(pivot=(0, YC * MM, 0), eksen="z", aci=_don(1.0)),                   # 6 dev/dk · ters
        "tabla": dict(pivot=(-YASA["r_dis"] * MM, -0.187, 0.2125), eksen="y", aci=lambda t: 7.0 * t / DONGU,       # 35 dev/dk
                      kay=lambda t: ((YASA["r_dis"] - r_t(t)) * MM if t <= T_DOK else (YASA["r_dis"] - YASA["r_ic"]) * MM * (DONGU - t) / (DONGU - T_DOK), 0.0, 0.0)),
        "kolon": dict(pivot=(0, 0, 0), eksen="y", aci=lambda t: 0.0,
                      kay=lambda t: ((YASA["r_dis"] - r_t(t)) * MM if t <= T_DOK else (YASA["r_dis"] - YASA["r_ic"]) * MM * (DONGU - t) / (DONGU - T_DOK), 0.0, 0.0))}


def glb_yaz(yol, parcalar, dokular):
    adlar = list(MALZEME.keys()); blob, views, accs, meshes, nodes = [], [], [], [], []; off = [0]

    def gomu(b, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(b)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(b); off[0] += len(b); return len(views) - 1

    cocuk, kok = {}, []
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
    n = int(round(DONGU / DT)); ts = [DONGU * i / n for i in range(n + 1)]
    vt = gomu(b"".join(struct.pack("<f", t) for t in ts)); accs.append({"bufferView": vt, "componentType": 5126, "count": len(ts), "type": "SCALAR", "min": [0.0], "max": [DONGU]}); a_t = len(accs) - 1
    kanallar, samplerlar = [], []
    for g, c in cocuk.items():
        bil = GRUP[g]; nodes.append({"name": "DON_" + g, "translation": list(bil["pivot"]), "children": c}); gi = len(nodes) - 1
        qs = []
        for t in ts:
            a = 2 * math.pi * bil["aci"](t); s, co = math.sin(a / 2), math.cos(a / 2); qs.append((0.0, 0.0, s, co) if bil["eksen"] == "z" else (0.0, s, 0.0, co))
        vq = gomu(b"".join(struct.pack("<4f", *q) for q in qs)); accs.append({"bufferView": vq, "componentType": 5126, "count": len(qs), "type": "VEC4"})
        samplerlar.append({"input": a_t, "output": len(accs) - 1, "interpolation": "LINEAR"}); kanallar.append({"sampler": len(samplerlar) - 1, "target": {"node": gi, "path": "rotation"}})
        if bil.get("kay"):
            nodes.append({"name": "KAY_" + g, "children": [gi]}); ki = len(nodes) - 1; kok.append(ki)
            vk = gomu(b"".join(struct.pack("<3f", *bil["kay"](t)) for t in ts)); accs.append({"bufferView": vk, "componentType": 5126, "count": len(ts), "type": "VEC3"})
            samplerlar.append({"input": a_t, "output": len(accs) - 1, "interpolation": "LINEAR"}); kanallar.append({"sampler": len(samplerlar) - 1, "target": {"node": ki, "path": "translation"}})
        else: kok.append(gi)
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
    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH kaset_3d_v5"}, "scene": 0, "scenes": [{"nodes": kok}], "nodes": nodes, "meshes": meshes, "materials": mats,
         "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}], "images": images, "textures": textures,
         "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}], "animations": [{"name": "calis", "channels": kanallar, "samplers": samplerlar}]}
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    return len(bb) + len(js)


if __name__ == "__main__":
    V = v4.hacim_L(Y_DOLUM); yd = v4.dolum_kotu(8.8 / RHO)
    print("KAP v5 · 280 x 325 x 360 · hacim (dolum cizgisine) %.1f L · 8,8 kg @ %.2f = %.1f L → dolum kotu y %.0f (%%%.0f)" % (V, RHO, 8.8 / RHO, yd, 100 * 8.8 / RHO / V))
    print("helezon toplam donus: ana kanat %.1f tur · uc acisi %.0f° · zarf: govde 325 + tup %.0f + kapak 18 + kaplin 20 = %.0f mm" % (teta(ZF) / (2 * math.pi), math.degrees(teta(ZF)) % 360, TUP, 325 + TUP + 18 + 20))
    MONTAJ = ["HELEZONU|ÖNDEN SÜR", "YATAK KAPAĞI|ÇEYREK TUR", "KARIŞTIRICIYI|TAK · PİMLE", "KABI YUVAYA|SÜR"]
    dokular = {"ad": doku_ad("KAŞAR KABI", "bu yönde tak  ·  280 × 325 × 360 mm  ·  %s L  ·  çıkış ÖNDE alttan" % ("%.1f" % V).replace(".", ","), ok_sol=True), "montaj": doku_montaj(MONTAJ)}
    for dosya, doz in (("kasar_v5", False), ("kasar_v5_dozaj", True)):
        par = model(doz); b1 = glb_yaz(os.path.join(OUT, dosya + ".glb"), par, dokular)
        print("%s · %d parca · %d ucgen · glb %.0f KB" % (dosya, len(par), sum(len(m.I) // 3 for _, m, _, _ in par), b1 / 1024.0))
        if not doz:
            b2, prim, sorun, uyari = usdz_yaz([os.path.join(OUT, dosya + ".usdz")], dosya, [(a, m, mal) for a, m, mal, _ in par], dokular)
            print("   usdz %.0f KB · geri acildi %d prim · USD denetimi: %s" % (b2 / 1024.0, prim, "GECTI" if not sorun else "KALDI"))
            for x in sorun: print("   HATA:", x)
