# -*- coding: utf-8 -*-
"""h3_f_sac_v1 — F (FIRIN) İSTASYONU · ÜRETİM SACI v1 — U'NUN YAPMADIĞI F PARÇALARI (4 Eki 2026 · Claude · GECE 2 ADIM 5c · YEREL · montaja bağlı DEĞİL)

KAPSAM (koordinatör notu 5b: F üst kabinin yan + arka sacları, y 788–1862, fırın bölgesi dahil h3_u_sac_v1'de — burada YENİDEN YAPILMAZ):
  1 · F ÖN KAPAKLARI (KAPAK_F_SOL 2500–3248,5 · KAPAK_F_SAG 3251,5–4000 · y 1308–2197 · z 59–79): dış tava 1,5 (4 dönüş, bindirme köşe) · ön yüzde 2 × 3 sıra
      lazer panjur yarığı 90 × 5 (v8zq ile aynı) · 2 dikey hazır haddeli OMEGA 40 × 15 × 1,5 · alt + üst kayıt = U 1,5 (aralıklı TIG) · alt kayıtta menteşe kanadı için 2 × 2 PEM SP-M5 ·
      bas-aç karşılık sacı. Menteşe (gövde + kanat), gazlı yay ve yay bilyeli braketi satın alınan parça → v8zq'dan KALIR (kpk aynı pivot).
  2 · DAVLUMBAZ ATIŞ KANALI (fan → baca, 296 × 196 · 1,5 · iki L, boyuna TIG) · 30 mm teleskopik geçmeyle baca iç kanalına girer (yüksek sıcaklık silikonu).
  3 · BACA (U_F içinden, y 1862–2198,5): iç kanal 300 × 200 · 1,5 (iki L) · taş yünü 25 (A1, görünmez) · dış kılıf 0,8 (iki L) + alt kapama halkası 0,8 ·
      üst bağlantı flanşı 3 mm (bina bacasına 8 × M8 · Ø9).
  4 · ARAYÜZ: TOPPING ↔ F 4 × M8 — F sol yan sacında Ø9 (h3_u_sac_v1 sahibi, h3_topping_sac_v1.M8_F ile eş) · J1 F tarafı U'da hazır.
F'DE BU ÜRETEÇTE OLMAYANLAR (bilerek): TP10 fırın gövdesi (satın alınan cihaz, kendi kabuğu = F_TP10_GOVDE) · yükleme bandı (TP10 girişi içinde, mekanizma) ·
  F kutusu (ELK_ISTASYON__pano, elektrik üreteci) · kompresör ayakları (U üst kabin tabanında PEM hazır) · KAIDE YOK: F, B'nin tavanına (B_TASIYICI üstü) oturur, y < 788 B'dir.
KOORDİNAT: DÜNYA. Çalıştır: gece2/adim5/f_sac_denetim_v1.py (scratchpad)."""
import math, os, sys, re, time
H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import numpy as np
import cadquery as cq
import h3_sac_v1 as S

SURUM = "h3_f_sac_v1"
V = cq.Vector
X_A = 0.0
BIRIM = "F_GOVDE"
KAPAK = {"SOL": dict(x0=2500.0, x1=3248.5, omega=(2730.0, 2978.5), alt=(2518.5, 3244.5), ust=(2504.5, 3244.5), mentese=(2611.0, 3099.5), basac=(2504.5, 2518.0),
                     panjur=[2555.0 + 110.0 * i for i in range(6)]),
         "SAG": dict(x0=3251.5, x1=4000.0, omega=(3481.5, 3730.0), alt=(3255.5, 3981.5), ust=(3255.5, 3995.5), mentese=(3362.5, 3851.0), basac=(3982.0, 3995.5),
                     panjur=[3306.5 + 110.0 * i for i in range(6)])}
KY0, KY1, KZ0, KZ1 = 1308.0, 2197.0, 59.0, 79.0
PANJUR_Y = [1405.0, 1417.0, 1429.0, 1810.0, 1822.0, 1834.0]
DAV = (2952.0, 3248.0, -718.0, -522.0, 1361.5, 1892.0)
BACA_IC = (2950.0, 3250.0, -720.0, -520.0)
BACA_DIS = (2924.5, 3275.5, -745.5, -494.5)
BY0, BY1 = 1862.0, 2198.5
FLANS = (2920.0, 3280.0, -750.0, -490.0, 2195.5, 2198.5)
M8_F = [(1000.0, -760.0), (1250.0, -700.0), (1700.0, -780.0), (1950.0, -780.0)]
DEGISEN = {"F_UST_KAPAK__on_seffaf__KAPAK_F_SOL": [0, 1, 2, 3, 5, 8], "F_UST_KAPAK__on_seffaf__KAPAK_F_SAG": [0, 1, 2, 3, 5, 8], "F_DAVLUMBAZ__sac": [1],
           "U_F_BACA__sac": "hepsi", "U_F_BACA__yalitim_gorunur": "hepsi", "U_F_BACA__paslanmaz": "hepsi"}
S._RENK.update({"yalitim": ((0.85, 0.80, 0.55, 1.0), 0.0, 0.9), "arayuz": ((0.90, 0.22, 0.15, 1.0), 0.3, 0.5), "kapak": ((0.70, 0.82, 0.95, 1.0), 0.2, 0.25)})


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


class G:
    SAC, PROFIL, ELEMAN, KAYNAK, ARAYUZ, PU, KAYNAK_ETIKET, NOT = [], [], [], [], [], [], [], []
    PANEL = {}
    kuruldu = False


def _sac(ad, rol, **k):
    s = S.Sac(ad, rol=rol, birim=BIRIM, kaynak=SURUM, **k); G.SAC.append(s); return s


def _eleman(p, mal="celik"):
    p["mal"] = p.get("mal") if p.get("mal") not in (None, "katalog", "paslanmaz") else mal
    p["birim"] = BIRIM; G.ELEMAN.append(p); return p


def _arayuz(p, karsi, gerek, not_=""):
    p["tur"] = "arayuz"; p["arayuz"] = dict(karsi=karsi, gerek=gerek, not_=not_); p["birim"] = BIRIM; G.ARAYUZ.append(p); return p


def _etiket(ad, yontem, olcu, not_):
    G.KAYNAK_ETIKET.append(dict(ad=ad, yontem=yontem, olcu=olcu, not_=not_))


def kaynak_kutu(ad, sh, boy, not_):
    p = S._bp(ad, sh, "TIG 141 · ER308LSi", not_, "%.0f mm" % boy, "AISI 304", birim=BIRIM, meta=dict(tur="kaynak", tip="kose", boy=boy, yontem="TIG 141"), uretim=True, mal="sac")
    p["tur"] = "kaynak"; G.ELEMAN.append(p)


# =====================================================================================================================================
# 1 · KAPAKLAR
# =====================================================================================================================================
def kapak(kod):
    k = KAPAK[kod]; x0, x1 = k["x0"], k["x1"]; ad = "onyuz_kapak_F_%s" % kod.lower()
    kd = _sac(ad + "_dis_tava", "kapak_dis", mal="on_seffaf"); g = kd.R + kd.t
    D = kd.taban([(x0 + g, KY0 + g), (x1 - g, KY0 + g), (x1 - g, KY1 - g), (x0 + g, KY1 - g)], O=(0, 0, KZ1 - kd.t), ex=(1, 0, 0), ey=(0, 1, 0), ad="on_yuz")
    fa = [D.flans(i, KZ1 - KZ0, yon=-1, ad=a) for i, a in enumerate(("alt_donus", "sag_donus", "ust_donus", "sol_donus"))]
    kd.kose(fa[0], fa[1], "bindirme", ustte=fa[0]); kd.kose(fa[1], fa[2], "bindirme", ustte=fa[2])
    kd.kose(fa[2], fa[3], "bindirme", ustte=fa[2]); kd.kose(fa[3], fa[0], "bindirme", ustte=fa[0])
    for x in k["panjur"]:
        for y in PANJUR_Y:
            D.dikdortgen(x + 45.0, y + 2.5, 90.0, 5.0, r=2.49, tip="havalandirma", parca="kapak havalandırma yarığı 90 × 5 (v8zq)")
    G.PANEL[ad] = dict(dis=D, s=kd)
    zt = KZ1 - kd.t                                                          # ön yüz iç yüzü 77,5
    # dikey omegalar: HAZIR HADDELİ omega 40 × 15 × 1,5 (taç 16 düz bıçakla bükülemez → h3_u_sac_v1 ile aynı karar) · boy kesim · kanatlar ön yüze punta
    for j, xo in enumerate(k["omega"]):
        s = S.Sac("%s_omega_%d" % (ad, j), rol="kapak_ic", t=1.5, birim=BIRIM, kaynak=SURUM); gs = s.R + s.t
        W_ = s.taban([(xo + 12.0 + gs, 1445.0), (xo + 28.0 - gs, 1445.0), (xo + 28.0 - gs, 1795.0), (xo + 12.0 + gs, 1795.0)], O=(0, 0, 62.5), ex=(1, 0, 0), ey=(0, 1, 0), ad="tac")
        b1 = W_.flans(1, zt - 62.5, yon=+1, ad="bacak_sag"); b2 = W_.flans(3, zt - 62.5, yon=+1, ad="bacak_sol")
        b1.flans(1, 12.0 + s.t, yon=-1, ad="kanat_sag"); b2.flans(1, 12.0 + s.t, yon=-1, ad="kanat_sol")
        p = S._bp("%s_omega_%d" % (ad, j), s.kati(), "hazır haddeli omega profil (EN 10162 sınıfı)", "Omega 40 × 15 × 1,5 AISI 304 · taç 16 · kanat 12 · boy kesim, kanatlar ön yüze 2 × 3 punta",
                  "L 350", "AISI 304", birim=BIRIM, meta=dict(tur="profil", kapakla_doner=True), uretim=True, mal="on_seffaf")
        p["tur"] = "baglanti"; _eleman(p, mal="on_seffaf")
    # alt + üst kayıt: U 1,5 (gövde z 60,5 · bacaklar ön yüze, uçları aralıklı TIG)
    for nm, (xa, xb), (ya, yb) in (("alt_kayit", k["alt"], (1312.0, 1395.0)), ("ust_kayit", k["ust"], (1863.5, 1905.0))):
        s = _sac("%s_%s" % (ad, nm), "kapak_ic", t=1.5, mal="on_seffaf"); gs = s.R + s.t
        W_ = s.taban([(xa, ya + gs), (xb, ya + gs), (xb, yb - gs), (xa, yb - gs)], O=(0, 0, 60.5), ex=(1, 0, 0), ey=(0, 1, 0), ad="govde")
        c1 = W_.flans(0, zt - 60.5, yon=+1, ad="bacak_alt"); c2 = W_.flans(2, zt - 60.5, yon=+1, ad="bacak_ust")
        _etiket("%s_%s_dikisi" % (ad, nm), "TIG 141 aralıklı 20 / 150 (iç yüz, görünmez)", "2 × %.0f mm" % (xb - xa), "U kayıt bacak uçları ↔ kapak ön yüzü iç yüzü")
        if nm == "alt_kayit":
            for xm in k["mentese"]:
                for dx in (8.0, 30.0):
                    ps, c, ms = S.pem_somun("SP", "M5", (xm + dx, 1323.5, 62.0), (0, 0, 1.0), s.t, ad="%s_mentese_%d_pem_%d" % (ad, int(xm), int(dx)), birim=BIRIM)
                    ps["meta"]["kapakla_doner"] = True
                    W_.delik(xm + dx, 1323.5, c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
                    _eleman(ps)
                    vd = S.vida("ISO7380", "M5", 6, (xm + dx, 1323.5, 59.0), (0, 0, 1.0), ad="%s_mentese_%d_vida_%d" % (ad, int(xm), int(dx)), birim=BIRIM)
                    _arayuz(vd, "F_UST_KAPAK menteşe kanadı (v8zq, satın alınan)", "menteşe kanadında Ø5,5 (2 adet, x %.0f / %.0f · y 1323,5)" % (xm + 8, xm + 30), "menteşe teyidi")
    # bas-aç karşılık sacı
    xa, xb = k["basac"]
    dp = _sac("%s_basac_karsilik" % ad, "dis", t=1.0, mal="on_seffaf")
    dp.taban([(xa, 2130.0), (xb, 2130.0), (xb, 2150.0), (xa, 2150.0)], O=(0, 0, zt - 1.0), ex=(1, 0, 0), ey=(0, 1, 0), ad="plaka")
    dp.punta(kd, [((xa + xb) / 2.0, 2140.0, zt)], not_="karşılık → ön yüz")


# =====================================================================================================================================
# 2 · KANALLAR (iki L)
# =====================================================================================================================================
def kanal_y(ad, x0, x1, z0, z1, y0, y1, t, mal="sac", rol="ic"):
    s1 = _sac(ad + "_L1", rol, t=t); g = s1.R + s1.t
    A = s1.taban([(x0 + g, -y1), (x1 - t, -y1), (x1 - t, -y0), (x0 + g, -y0)], O=(0, 0, z1), ex=(1, 0, 0), ey=(0, -1, 0), ad="on")
    A.flans(3, z1 - (z0 + t), yon=+1, ad="sol")
    s2 = _sac(ad + "_L2", rol, t=t)
    B = s2.taban([(x0 + t, y0), (x1 - g, y0), (x1 - g, y1), (x0 + t, y1)], O=(0, 0, z0), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
    B.flans(1, (z1 - t) - z0, yon=+1, ad="sag")
    for kk, (xa, za) in enumerate(((x1 - t, z1 - t), (x0, z0))):
        kaynak_kutu("%s_boyuna_kaynak_%d" % (ad, kk), kutu(xa, xa + t, y0, y1, za, za + t), y1 - y0, "Kanal boyuna köşe dikişi (sürekli, duman sızdırmaz)")
    return s1, s2


def kanallar():
    x0, x1, z0, z1, y0, y1 = DAV
    kanal_y("davlumbaz_atis_kanali", x0, x1, z0, z1, y0, y1, 1.5)
    G.NOT.append("davlumbaz atış kanalı üstü 1862 → 1892 (30 mm baca iç kanalına teleskopik geçme, 0,5 boşluk yüksek sıcaklık silikonuyla)")
    x0, x1, z0, z1 = BACA_IC
    kanal_y("baca_ic_kanal", x0, x1, z0, z1, BY0, FLANS[4], 1.5)
    a0, a1, b0, b1 = BACA_DIS; tk = 0.8
    kanal_y("baca_dis_kilif", a0, a1, b0, b1, 1863.5, FLANS[4], tk, rol="dis")
    # alt kapama halkası (taş yünü altta görünmesin): 4 lama 0,8 (dar halka tek parça kesilir ama 4 lama ile fire az) · köşe cepleri gıda dışı silikon
    c_ = 2.0
    for nm in ("on", "arka", "sol", "sag"):
        q = _sac("baca_alt_kapama_lamasi_%s" % nm, "dis", t=tk)
        if nm in ("on", "arka"):
            za, zb = (z1, b1 - tk) if nm == "on" else (b0 + tk, z0)
            u0, u1 = a0 + tk, a1 - tk
            if nm == "on": pts = [(u0, -zb + c_), (u0 + c_, -zb), (u1 - c_, -zb), (u1, -zb + c_), (u1, -za), (u0, -za)]
            else: pts = [(u0, -zb), (u1, -zb), (u1, -za - c_), (u1 - c_, -za), (u0 + c_, -za), (u0, -za - c_)]
        else:
            xa, xb = (a0 + tk, x0) if nm == "sol" else (x1, a1 - tk)
            pts = [(xa, -z1), (xb, -z1), (xb, -z0), (xa, -z0)]
        q.taban(pts, O=(0, 1863.5, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="lama")
    for k_, (xa, za) in enumerate(((a0 + tk, b0 + tk), (a1 - tk - c_, b0 + tk), (a0 + tk, b1 - tk - c_), (a1 - tk - c_, b1 - tk - c_))):
        kb_ = kutu(xa, xa + c_, 1863.5, 1863.5 + tk, za, za + c_)
        kil = [q.kati() for q in G.SAC if q.ad.startswith(("baca_dis_kilif", "baca_alt_kapama"))]
        sh = kb_.cut(*kil).clean()
        p_ = S._bp("baca_alt_kose_silikonu_%d" % k_, sh, "yüksek sıcaklık silikonu (300 °C)", "Kılıf alt köşe cebi dolgusu", "2 × 2 × 0,8", "VMQ", birim=BIRIM, mal="conta")
        p_["tur"] = "baglanti"; _eleman(p_, mal="conta")
        kes_sil = G.ELEMAN[-1]["sh"]
    # üst flanş 3 mm = 4 lama (kanal flanşı) · köşeler alın TIG + taşlama
    fx0, fx1, fz0, fz1, fy0, fy1 = FLANS
    s = None
    lam = {}
    for nm, xa, xb, za, zb in (("on", fx0, fx1, z1, fz1), ("arka", fx0, fx1, fz0, z0), ("sol", fx0, x0, z0, z1), ("sag", x1, fx1, z0, z1)):
        q = _sac("baca_ust_flansi_%s" % nm, "braket", t=3.0)
        lam[nm] = q.taban([(xa, -zb), (xb, -zb), (xb, -za), (xa, -za)], O=(0, fy0, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="lama")
        s = q
    _etiket("baca_flans_lama_dikisi", "TIG 141 alın + taşlama", "4 × 30 mm", "flanş lamaları köşe birleşimi")
    kes = []
    for i, (x, z) in enumerate([(2937.0, -620.0), (3263.0, -620.0), (3100.0, -505.0), (3100.0, -735.0), (2937.0, -505.0), (3263.0, -505.0), (2937.0, -735.0), (3263.0, -735.0)]):
        Q = lam["on"] if z > z1 else (lam["arka"] if z < z0 else (lam["sol"] if x < x0 else lam["sag"]))
        ps, c, ms = S.pem_somun("SP", "M6", (x, fy0, z), (0, -1.0, 0), 3.0, ad="baca_flans_pem_M6_%d" % i, birim=BIRIM)
        Q.delik(x, -z, c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
        _eleman(ps)
        Lb = ps["meta"]["T"] - ps["meta"]["sap"]; p0 = np.array([x, fy0, z]); e = np.array([0, -1.0, 0])
        cap = cq.Solid.makeCylinder(c["E"] / 2.0 + 0.8, Lb + 0.8, V(*p0), V(*e)).cut(cq.Solid.makeCylinder(c["E"] / 2.0, Lb, V(*p0), V(*e)))
        kp = S._bp("baca_flans_pem_M6_%d_kapak" % i, cap, "AISI 304 kör başlık (derin çekme)", "PEM gövdesi kapağı (taş yünü tarafı) · flanşa punta", "Ø%.1f × %.1f" % (c["E"] + 1.6, Lb + 0.8),
                   "AISI 304", birim=BIRIM, mal="celik")
        kp["tur"] = "baglanti"; _eleman(kp)
        kes.append(cq.Solid.makeCylinder(c["E"] / 2.0 + 0.8, Lb + 0.8, V(*p0), V(*e)))
        vd = S.vida("ISO4762", "M6", 12, (x, 2200.0, z), (0, -1.0, 0), ad="arayuz_baca_flans_M6_%d" % i, birim=BIRIM)
        _arayuz(vd, "U_F tavan sacı (h3_u_sac_v1 ust_f_tavan_sac)", "U_F tavanında Ø6,6 (dünya x %.0f z %.0f) · ISO 4762 M6 × 12 üstten (bina bacası adaptörü ile birlikte)" % (x, z), "h3_u_sac_v1 sahibi")
    kes += [p_["sh"] for p_ in G.ELEMAN if p_["ad"].startswith("baca_alt_kose_silikonu")]
    G.NOT.append("baca flanşı → U_F tavanı: 8 × PEM SP-M6 (gövde aşağıda, paslanmaz kör başlıkla kapalı → taş yünü görünmez) · cıvata U_F tavanının üstünden (ARAYÜZ)")
    _etiket("baca_flans_dikisi", "TIG 141 sürekli", "2 × (300 + 200) mm", "iç kanal + dış kılıf üst ucu ↔ flanş alt yüzü")
    # taş yünü (A1 ≥ 100 kg/m³) · iç kanal ile kılıf arası: bölge − saclar − PEM kapakları (yerinde kesilir, boşluk yok)
    yy0, yy1 = 1863.5 + tk, fy0
    b_ = kutu(a0 + tk, a1 - tk, yy0, yy1, b0 + tk, b1 - tk).cut(kutu(x0, x1, yy0 - 1.0, yy1 + 1.0, z0, z1))
    saclar = [q.kati() for q in G.SAC if q.ad.startswith("baca")]
    sh = b_.cut(*(saclar + kes)).clean()
    for i, so in enumerate(sh.Solids()):
        if so.Volume() < 20.0: continue
        p = dict(ad="yalitim_baca_%d" % i, wp=cq.Workplane("XY").add(so), sh=so, mal="yalitim", birim=BIRIM, grup="SABIT", kaynak=SURUM, tur="pu",
                 bom=("Taş yünü A1 ≥ 100 kg/m³ (EN 13162) · baca kılıfı", 1, "%.1f dm³" % (so.Volume() / 1e6), "4 levha kesim, kılıf içine", "ÜRETİM"), meta=dict(tur="yalitim"))
        G.PU.append(p)


def arayuz_F():
    for y, z in M8_F:
        sh = cq.Solid.makeCylinder(4.5, 1.5, V(2500.0, y, z), V(1, 0, 0))
        p = S._bp("arayuz_M8_TOPPING_F_delik_%d_%d" % (int(y), int(-z)), sh, "ISO 273 orta", "F sol yan sacında Ø9 delik (TOPPING ↔ F M8)", "Ø9", "—", birim=BIRIM)
        _arayuz(p, "F sol yan sacı (h3_u_sac_v1 f_ust_yan_sol)", "Ø9 delik dünya x 2500 · y %.0f · z %.0f (cıvata F içinden → TOPPING sağ yanında PEM SP-M8)" % (y, z),
                "h3_u_sac_v1 sahibi")


# =====================================================================================================================================
def kur(log=print):
    if G.kuruldu: return G
    t0 = time.time()
    for a in ("SAC", "PROFIL", "ELEMAN", "KAYNAK", "ARAYUZ", "PU", "KAYNAK_ETIKET", "NOT"): setattr(G, a, [])
    G.PANEL = {}
    kapak("SOL"); kapak("SAG"); kanallar(); arayuz_F()
    _etiket("kapak_kose_dikisleri", "TIG 141 + taşlama (bindirme köşe)", "8 köşe × 20 mm", "dış tava köşeleri")
    G.kuruldu = True
    log("%s · kuruldu: %d sac · %d yalıtım · %d eleman · %d arayüz · %.1f sn" % (SURUM, len(G.SAC), len(G.PU), len(G.ELEMAN), len(G.ARAYUZ), time.time() - t0))
    return G


def kapakla_doner(ad):
    return ad.startswith("onyuz_kapak_F")


def _mal(p):
    if p.get("tur") == "pu": return "yalitim"
    if kapakla_doner(p["ad"]): return "on_seffaf"
    if p.get("tur") in ("sac", "profil", "kaynak"): return "sac"
    return p.get("mal") if p.get("mal") in ("celik", "conta", "siyah", "sac") else "celik"


def govde_parcalari():
    kur()
    L = []
    for s in G.SAC: L += s.parcalar()
    L += G.ELEMAN + G.PU
    out = []
    for p in L:
        sh = p.get("sh") if p.get("sh") is not None else p["wp"].val()
        q = dict(ad=p["ad"], wp=cq.Workplane("XY").add(sh), sh=sh, mal=_mal(p), grup="SABIT", bom=tuple(p["bom"]) if p.get("bom") else None, kaynak=SURUM,
                 birim=BIRIM, tur=p.get("tur", "sac"))
        if p.get("sac"): q["sac"] = p["sac"]
        if p.get("meta"): q["meta"] = p["meta"]
        out.append(q)
    adlar = [q["ad"] for q in out]
    assert len(adlar) == len(set(adlar)), "çift ad"
    return out


ZARF = (2500.0, 4000.0, 1308.0, 2198.5, -750.0, 79.0)


def dunya_listesi(L):
    out = []
    for p in L:
        q = dict(p); s = p.get("sh") if p.get("sh") is not None else p["wp"].val()
        q["sh"] = s; q["wp"] = cq.Workplane("XY").add(s); out.append(q)
    return out


def pu_ortu():
    return []


if __name__ == "__main__":
    kur(); print(len(govde_parcalari()), "parça")
    sys.stdout.flush(); os._exit(0)
