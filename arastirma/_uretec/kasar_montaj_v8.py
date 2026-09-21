# -*- coding: utf-8 -*-
"""AUTOKITCH · KAŞAR KABI v8 — MONTAJ ANİMASYONU
Kemal: "bunu nasıl montajlıyorsun, içine vida nasıl giriyor, nereye takılıyor, kapak nasıl kapanıyor — tüm parçalar için."
Her parça KENDİ takılma yönünden gelir; helezon dönerek girer, yatak kapağı önce itilir sonra çeyrek tur döner.
Katılar kasar_cad_v8'den birebir alınır (ayrı model YOK) → otonom/kaset3d/kasar_v8_montaj.glb
"""
import math, os, sys
import cadquery as cq
import importlib
MODUL = sys.argv[1] if len(sys.argv) > 1 else "kasar_cad_v8"          # kullanım: python kasar_montaj_v8.py [üreteç modülü] [çıktı öneki]
ONEK = sys.argv[2] if len(sys.argv) > 2 else "kasar_v8"
V = importlib.import_module(MODUL)
GRUP_CALIS = dict(V.GRUP)                                            # kur() V.GRUP'u montaj gruplarıyla ezer; çalışma animasyonu için aslını sakla
from kaset_3d_v3 import Mesh, MM, doku_ad, doku_montaj, etiket_yuzu, usdz_yaz, OUT

BASLA, ADIM_SURE, HAREKET = 1.4, 1.6, 0.72      # sn · adım süresi · hareketin adım içindeki payı

# (adım adı, parça adları, geliş yönü mm, tur, önce-it-sonra-döndür)
ADIMLAR = [
    ("Arka plaka tezgâha konur",            ["plaka_arka"],                                   (0, 0, 0),     0.0, False),
    ("Gövde arka plakanın kanalına sürülür", ["govde", "etiket_ad", "etiket_montaj", "etiket_ad_arka", "etiket_montaj_arka"], (0, 0, 300), 0.0, False),
    ("Ön plaka öne geçirilir",              ["plaka_on"],                                     (0, 0, 340),   0.0, False),
    ("4 saplama arkadan geçirilir",         ["saplama_0", "saplama_1", "saplama_2", "saplama_3"], (0, 0, -300), 0.0, False),
    ("Kör somunlar sıkılır",                ["somun_arka_0", "somun_arka_1", "somun_arka_2", "somun_arka_3", "somun_on_0", "somun_on_1"], (0, 0, -150), 0.0, False),
    ("Kulp üst saplamalara vidalanır",      ["kulp"],                                         (0, 0, 220),   0.0, False),
    ("2 tahrik göbeği İÇERİDEN takılır",    ["gobek_helezon", "gobek_karistirici"],           (0, 0, 190),   0.0, False),
    ("Haç kavramalar arkadan geçer, pim kilitler", ["kavrama_helezon", "kavrama_karistirici", "yayli_pim_helezon", "yayli_pim_karistirici"], (0, 0, -170), 0.0, False),
    ("HELEZON önden sürülür (4 segment kare çubuğa dizili)", ["helezon_cekirdek", "helezon_A", "helezon_B", "helezon_C", "helezon_D"], (0, 0, 430), -2.0, False),
    ("Çıkış tüpü ön plakaya 2 × M4 ile",    ["cikis_tupu", "vida_tup_a", "vida_tup_b"],       (0, 0, 240),   0.0, False),
    ("Yatak kapağı itilir, ÇEYREK TUR döner", ["yatak_kapagi"],                               (0, 0, 130),   0.25, True),
    ("Besleme rotoru ÜSTTEN indirilir (2 sıyırıcı lama)" if "kiyma" in MODUL else "Karıştırıcı kafesi ÜSTTEN indirilir", ["orumcek_arka", "orumcek_orta", "orumcek_on", "cubuk_0", "cubuk_1", "cubuk_2", "cubuk_3"], (0, 430, 0), 0.0, False),
    ("Kare mil önden kafesin içinden geçer", ["kar_mil"],                                     (0, 0, 420),   0.0, False),
    ("Ön kovan takılır",                    ["on_kovan"],                                     (0, 0, 150),   0.0, False),
    ("Topuz mile geçer, setuskur sıkılır",  ["topuz", "setuskur"],                            (0, 0, 190),   0.0, False),
    ("Kilit pimi TEĞET geçer (mili delmez)", ["kilit_pimi"],                                  (190, 0, 0),   0.0, False),
    ("Kapak gövde ağzına oturur",           ["kapak"],                                        (0, 300, 0),   0.0, False),
    ("Taşıma tapası ağıza takılır",         ["tasima_tapasi"],                                (0, -200, 0),  0.0, False),
]


def ease(t, t0, t1):
    if t <= t0: return 0.0
    if t >= t1: return 1.0
    u = (t - t0) / (t1 - t0); return u * u * (3.0 - 2.0 * u)


def kur():
    V.kap()
    var = set(p["ad"] for p in V.PARCALAR) | set(["etiket_ad", "etiket_montaj", "etiket_ad_arka", "etiket_montaj_arka"])
    sure = BASLA + len(ADIMLAR) * ADIM_SURE + 2.6
    V.DONGU, V.DT = sure, 0.1
    GR, hangi = {}, {}
    for i, (ad, parcalar, off, tur, ayri) in enumerate(ADIMLAR):
        g = "a%02d" % i; t0 = BASLA + i * ADIM_SURE; tL = ADIM_SURE * HAREKET
        if ayri: kt0, kt1, at0, at1 = t0, t0 + tL * 0.55, t0 + tL * 0.55, t0 + tL
        else:    kt0, kt1, at0, at1 = t0, t0 + tL, t0, t0 + tL
        GR[g] = dict(pivot=(0, V.CY * MM, 0) if tur else (0, 0, 0), eksen="z",
                     aci=(lambda t, a=at0, b=at1, n=tur: n * (1.0 - ease(t, a, b))),
                     kay=(lambda t, a=kt0, b=kt1, o=off: tuple(c * MM * (1.0 - ease(t, a, b)) for c in o)))
        for p in parcalar:
            if p in var: hangi[p] = g                       # üreteçte olmayan parça adı (ör. kıymada cubuk_2/3) atlanır
    V.GRUP = GR

    # etiketler (gövdeyle birlikte hareket etsin)
    e0, e1 = (V.Y_UST - 56) * MM, (V.Y_UST - 8) * MM; ez = (V.D / 2 - V.TP - 6) * MM; xo = (V.RB + V.ET + 0.4) * MM
    EK = [("etiket_ad", etiket_yuzu(-xo, e0, e1, -ez, ez, -1), "etiket_ad"),
          ("etiket_montaj", etiket_yuzu(xo, e0, e1, ez, -ez, 1), "etiket_montaj")]
    for adi, xx, nx in (("etiket_ad_arka", -xo + 0.0002, 1), ("etiket_montaj_arka", xo - 0.0002, -1)):
        ar = Mesh(); ar.quad((xx, e0, -ez), (xx, e0, ez), (xx, e1, ez), (xx, e1, -ez), (nx, 0, 0)); EK.append((adi, ar.duzelt(), "sari_arka"))

    par = [(p["ad"], V.ag(p["wp"]), p["mal"], hangi.get(p["ad"])) for p in V.PARCALAR] + \
          [(a, m, mal, hangi.get(a)) for a, m, mal in EK]
    eksik = [p["ad"] for p in V.PARCALAR if p["ad"] not in hangi]
    assert not eksik, "adimi olmayan parca: %s" % eksik
    return par, sure


if __name__ == "__main__":
    par, sure = kur()
    V_ = V.v4.hacim_L(V.Y_DOLUM)
    dokular = {"ad": doku_ad("KIYMA KASETİ" if "kiyma" in MODUL else "KAŞAR KABI", "bu yönde tak  ·  %d × 325 × 360 mm" % V.W + "  ·  %s L  ·  çıkış ÖNDE alttan" % ("%.1f" % V_).replace(".", ","), ok_sol=True),
               "montaj": doku_montaj(["HELEZONU|ÖNDEN SÜR", "YATAK KAPAĞI|ÇEYREK TUR", ("ROTOR" if "kiyma" in MODUL else "KAFES") + " · MİL|TOPUZ · PİM", "TAPAYI ÇIKAR|YUVAYA SÜR"])}
    b = V.glb_yaz(os.path.join(OUT, ONEK + "_montaj.glb"), par, dokular)
    print(ONEK + "_montaj.glb · %d parca · %d adim · %.1f sn · %.0f KB" % (len(par), len(ADIMLAR), sure, b / 1024.0))

    # ---- AYNI ANİMASYON USDZ'YE (iPhone AR) ----
    anim = {}
    for i, (ad_, parcalar, off, tur, ayri) in enumerate(ADIMLAR):
        t0 = BASLA + i * ADIM_SURE; tL = ADIM_SURE * HAREKET
        kt0, kt1 = (t0, t0 + tL * 0.55) if ayri else (t0, t0 + tL)
        at0, at1 = (t0 + tL * 0.55, t0 + tL) if ayri else (t0, t0 + tL)
        anlar = sorted(set([0.0, kt0, at0, sure] + [kt0 + (kt1 - kt0) * k / 4.0 for k in range(5)] + [at0 + (at1 - at0) * k / 4.0 for k in range(5)]))
        keys = [(t, tuple(c * MM * (1.0 - ease(t, kt0, kt1)) for c in off), -360.0 * tur * (1.0 - ease(t, at0, at1))) for t in anlar]
        for p_ in parcalar:
            if p_ in set(a_ for a_, m_, mal_, g_ in par): anim[p_] = dict(pivot=(0.0, V.CY * MM, 0.0) if tur else None, keys=keys)
    b2, prim, sorun, uyari = usdz_yaz([os.path.join(OUT, ONEK + "_montaj.usdz")], ONEK + "_montaj",
                                      [(a_, m_, mal_) for a_, m_, mal_, g_ in par], dokular, anim=anim, fps=30.0, sure=sure)
    print(ONEK + "_montaj.usdz · %.0f KB · %d prim · USD denetimi: %s" % (b2 / 1024.0, prim, "GECTI" if not sorun else "KALDI"))
    for x in sorun: print("   HATA:", x)
    # ---- ÇALIŞMA ANİMASYONU USDZ (üretim / dozaj sekmelerinin iPhone AR dosyası): helezon + karıştırıcı/rotor döner ----
    # Quick Look animasyonu DÖNGÜYE alır → tur sayısı TAM olmalı ki başa sararken sıçramasın (kıymada −3,4 → −3 tur; yalnız görsel).
    T_, D_ = 10.0, 12.0; grp = {p_["ad"]: p_["grup"] for p_ in V.PARCALAR}; anim2 = {}
    for g_ in ("helezon", "karistirici"):
        tur_ = GRUP_CALIS[g_]["aci"](T_); tur_ = float(round(tur_)) if abs(round(tur_)) >= 1 else math.copysign(1.0, tur_)
        keys_ = [(0.0, (0, 0, 0), 0.0), (T_, (0, 0, 0), 360.0 * tur_), (D_, (0, 0, 0), 360.0 * tur_)]
        for a_, g2 in grp.items():
            if g2 == g_: anim2[a_] = dict(pivot=GRUP_CALIS[g_]["pivot"], keys=keys_)
    calis = [(a_, m_, mal_) for a_, m_, mal_, _ in par if a_ != "tasima_tapasi"]
    b3, prim3, sorun3, _u = usdz_yaz([os.path.join(OUT, ONEK + "_calis.usdz")], ONEK + "_calis", calis, dokular, anim=anim2, fps=30.0, sure=D_)
    print(ONEK + "_calis.usdz · %.0f KB · %d hareketli parca · USD denetimi: %s" % (b3 / 1024.0, len(anim2), "GECTI" if not sorun3 else "KALDI"))

    # ---- ADIM ADIM AR: iPhone'un AR görüntüleyicisinde sarma çubuğu YOK ve siteler ekleyemiyor → her adımın DURAĞAN hâli ayrı USDZ ----
    # k. dosya: 1..k adımların parçaları YERİNDE, sonrakiler geliş konumunda bekliyor (dönüşler dahil) — ofset/dönüş ağa gömülür.
    def donustur(m, off, tur, pivot):
        a = -2.0 * math.pi * tur; ca, sa = math.cos(a), math.sin(a); y = Mesh(); y.I = list(m.I); y.UV = m.UV
        for (px, py, pz), (nx, ny, nz) in zip(m.P, m.N):
            dx, dy = px - pivot[0], py - pivot[1]
            y.P.append((pivot[0] + ca * dx - sa * dy + off[0] * MM, pivot[1] + sa * dx + ca * dy + off[1] * MM, pz + off[2] * MM))
            y.N.append((ca * nx - sa * ny, sa * nx + ca * ny, nz))
        return y
    hangi_adim = {}
    for i, (ad_, parcalar, off, tur, ayri) in enumerate(ADIMLAR):
        for p_ in parcalar: hangi_adim[p_] = i
    top = 0
    for k in range(1, len(ADIMLAR) + 1):
        L = []
        for a_, m_, mal_, _g in par:
            i = hangi_adim.get(a_, 0)
            if i < k: L.append((a_, m_, mal_))
            else:
                _ad, _p, off, tur, _ay = ADIMLAR[i]; L.append((a_, donustur(m_, off, tur, (0.0, V.CY * MM, 0.0)), mal_))
        bk, _pr, sk, _uy = usdz_yaz([os.path.join(OUT, "%s_adim_%02d.usdz" % (ONEK, k))], "%s_adim_%02d" % (ONEK, k), L, dokular)
        assert not sk, sk; top += bk
    print("%s_adim_01..%02d.usdz · toplam %.1f MB" % (ONEK, len(ADIMLAR), top / 1048576.0))
    for i, (ad, p, o, t, a) in enumerate(ADIMLAR):
        print("  %2d  %5.1f sn  %-48s %d parca" % (i + 1, BASLA + i * ADIM_SURE, ad, len(p)))
