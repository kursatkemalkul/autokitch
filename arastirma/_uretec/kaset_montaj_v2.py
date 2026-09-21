# -*- coding: utf-8 -*-
"""AUTOKITCH · KASET MONTAJ ANİMASYONU v2 (22 Eyl 2026) — BİRLEŞİM DETAYLARI v1 ile (kaset_birlesim_v1.py)
Kemal: "çubuk plastiğe nasıl takılıyor, kulp nasıl takılıyor, kapak nasıl click ediyor — çözülmemiş."  v1 animasyonunda (kasar_montaj_v8.py) kulp iki SABİT
saplamaya 'vidalanıyordu' — tek parça kulpla bu yapılamaz. DOĞRU SIRA: üst iki saplama önce KULPA vidalanır (saplama döner), sonra kulp + saplamalar önden
geçirilir, arkadan pul + kör somun sıkılır. Ayrıca: contalar, O-ringler, pullar kendi adımlarında; yatak kapağı İT → 35° ÇEVİR (çeyrek tur değil).
Katılar üreteçten birebir alınır (ayrı model YOK). Kullanım: python kaset_montaj_v2.py <üreteç modülü> <çıktı öneki>"""
import math, os, sys
import cadquery as cq
import importlib
MODUL = sys.argv[1] if len(sys.argv) > 1 else "kasar_cad_v9"
ONEK = sys.argv[2] if len(sys.argv) > 2 else "kasar_v9"
V = importlib.import_module(MODUL)
GRUP_CALIS = dict(V.GRUP)                                            # kur() V.GRUP'u montaj gruplarıyla ezer; çalışma animasyonu için aslını sakla
from kaset_3d_v3 import Mesh, MM, doku_ad, doku_montaj, etiket_yuzu, usdz_yaz, OUT
import kaset_birlesim_v1 as BR

BASLA, ADIM_SURE, HAREKET = 1.4, 1.6, 0.72      # sn · adım süresi · hareketin adım içindeki payı
KASAR = "kasar" in MODUL
KULP_BEKLE = 480.0                              # kulp önde bu kadar açıkta bekler; üst saplamalar ona orada vidalanır

# (adım adı, parça adları, geliş yönü mm, tur, önce-it-sonra-döndür, ek)   ek: pivot="kendi" → parça KENDİ ekseninde döner · tasi=k → k. adımın kaymasını da yapar
ADIMLAR = [
    ("Arka plaka tezgâha konur",                                   ["plaka_arka"],                                        (0, 0, 0),    0.0, False, {}),
    ("Arka CONTA plakanın kanalına yerleştirilir",                 ["conta_arka"],                                        (0, 0, 120),  0.0, False, {}),
    ("Gövde kanala, contanın üstüne sürülür",                      ["govde", "etiket_ad", "etiket_montaj", "etiket_ad_arka", "etiket_montaj_arka"], (0, 0, 300), 0.0, False, {}),
    ("Ön conta + ön plaka (M4 insertleri çakılı) öne geçirilir",   ["conta_on", "plaka_on", "insert_a", "insert_b"],      (0, 0, 340),  0.0, False, {}),
    ("2 ALT saplama arkadan geçirilir (gövdenin dışından)",        ["saplama_0", "saplama_1"],                            (0, 0, -300), 0.0, False, {}),
    ("Alt saplamalara arkadan pul + kör somun",                    ["pul_arka_0", "pul_arka_1", "somun_arka_0", "somun_arka_1"], (0, 0, -150), 0.0, False, {}),
    ("Önden pul + kör somun: alt saplamalar sıkılır",              ["pul_on_0", "pul_on_1", "somun_on_0", "somun_on_1"],  (0, 0, 150),  0.0, False, {}),
    ("2 ÜST saplama KULPUN ayağına dibe kadar vidalanır (saplama döner)", ["saplama_2", "saplama_3"],                     (0, 0, -120), 4.0, False, dict(pivot="kendi", tasi="kulp")),
    ("Kulp + 2 saplama ÖNDEN plakalardan geçirilir",               ["kulp"],                                              (0, 0, KULP_BEKLE), 0.0, False, {}),
    ("Arkadan pul + kör somun: kulp ayakları ön plakaya çekilir",  ["pul_arka_2", "pul_arka_3", "somun_arka_2", "somun_arka_3"], (0, 0, -150), 0.0, False, {}),
    ("2 tahrik göbeği (O-ringi kanalında) İÇERİDEN takılır",       ["gobek_helezon", "gobek_karistirici", "oring_gobek_helezon", "oring_gobek_karistirici"], (0, 0, 190), 0.0, False, {}),
    ("Haç kavramalar arkadan geçer, yaylı pim kilitler",           ["kavrama_helezon", "kavrama_karistirici", "yayli_pim_helezon", "yayli_pim_karistirici"], (0, 0, -170), 0.0, False, {}),
    ("HELEZON önden sürülür (4 segment kare çubuğa dizili)",       ["helezon_cekirdek", "helezon_A", "helezon_B", "helezon_C", "helezon_D"], (0, 0, 430), -2.0, False, {}),
    ("O-ring faturaya · çıkış tüpü 2 × M4 ile insertlere",         ["oring_tup", "cikis_tupu", "vida_tup_a", "vida_tup_b"], (0, 0, 240), 0.0, False, {}),
    ("Yatak kapağı (O-ringi içinde): İT → 35° ÇEVİR → KLİK",       ["yatak_kapagi", "oring_kapak"],                       (0, 0, 130),  BR.KILIT_ACI / 360.0, True, {}),
    ("Karıştırıcı kafesi ÜSTTEN indirilir" if KASAR else "Besleme rotoru ÜSTTEN indirilir (2 sıyırıcı lama)", ["orumcek_arka", "orumcek_orta", "orumcek_on", "cubuk_0", "cubuk_1", "cubuk_2", "cubuk_3"], (0, 430, 0), 0.0, False, {}),
    ("Kare mil önden, göbeklerin içinden geçer",                   ["kar_mil"],                                           (0, 0, 420),  0.0, False, {}),
    ("Ön kovan (O-ringi kanalında) takılır",                       ["on_kovan", "oring_on_kovan"],                        (0, 0, 150),  0.0, False, {}),
    ("Topuz mile geçer, setuskur sıkılır",                         ["topuz", "setuskur"],                                 (0, 0, 190),  0.0, False, {}),
    ("Kilit pimi TEĞET geçer (mili delmez)",                       ["kilit_pimi"],                                        (190, 0, 0),  0.0, False, {}),
    ("Kapak gövde ağzına oturur",                                  ["kapak"],                                             (0, 300, 0),  0.0, False, {}),
    ("Taşıma tapası ağıza takılır",                                ["tasima_tapasi"],                                     (0, -200, 0), 0.0, False, {}),
]


def ease(t, t0, t1):
    if t <= t0: return 0.0
    if t >= t1: return 1.0
    u = (t - t0) / (t1 - t0); return u * u * (3.0 - 2.0 * u)


def pencere(i):
    ayri = ADIMLAR[i][4]; t0 = BASLA + i * ADIM_SURE; tL = ADIM_SURE * HAREKET
    return (t0, t0 + tL * 0.55, t0 + tL * 0.55, t0 + tL) if ayri else (t0, t0 + tL, t0, t0 + tL)      # kayma başı/sonu · dönme başı/sonu


def hareket(i, parca):
    """bir parçanın montaj hareketi → (pivot mm ya da None, kay(t) mm, tur(t), hareket pencereleri)"""
    ad, parcalar, off, tur, ayri, ek = ADIMLAR[i]; kt0, kt1, at0, at1 = pencere(i); P = [(kt0, kt1), (at0, at1)]
    if ek.get("pivot") == "kendi": x, y = V.SAPLAMA[int(parca.rsplit("_", 1)[1])]; pivot = (x, y, 0.0)
    else: pivot = (0.0, V.CY, 0.0) if tur else None
    kaymalar = [(off, kt0, kt1)]
    if "tasi" in ek: j = [k_ for k_, a_ in enumerate(ADIMLAR) if ek["tasi"] in a_[1]][0]; jt0, jt1, _a, _b = pencere(j); kaymalar.append((ADIMLAR[j][2], jt0, jt1)); P.append((jt0, jt1))
    kay = lambda t, K=kaymalar: tuple(sum(o[c] * (1.0 - ease(t, a, b)) for o, a, b in K) for c in range(3))
    don = lambda t, a=at0, b=at1, n=tur: n * (1.0 - ease(t, a, b))
    return pivot, kay, don, P


def kur():
    V.kap()
    var = set(p["ad"] for p in V.PARCALAR) | set(["etiket_ad", "etiket_montaj", "etiket_ad_arka", "etiket_montaj_arka"])
    ADIMLAR[:] = [a for a in ADIMLAR if any(p in var for p in a[1])]      # üreteçte olmayan parçanın adımı düşer (ör. kapak kalktı) → boş adım kalmaz
    sure = BASLA + len(ADIMLAR) * ADIM_SURE + 2.6
    V.DONGU, V.DT = sure, 0.1
    GR, hangi, H = {}, {}, {}
    for i, (ad, parcalar, off, tur, ayri, ek) in enumerate(ADIMLAR):
        for p in parcalar:
            if p not in var: continue                        # üreteçte olmayan parça adı (ör. kıymada cubuk_2/3) atlanır
            pivot, kay, don, P = hareket(i, p); g = "a%02d" % i + ("_" + p if ek.get("pivot") == "kendi" else "")
            GR[g] = dict(pivot=tuple(c * MM for c in pivot) if pivot else (0, 0, 0), eksen="z", aci=don, kay=(lambda t, f=kay: tuple(c * MM for c in f(t))))
            hangi[p] = g; H[p] = (pivot, kay, don, P)
    V.GRUP = GR

    # etiketler (gövdeyle birlikte hareket etsin)
    e0, e1 = (V.Y_UST - 56) * MM, (V.Y_UST - 8) * MM; ez = (V.D / 2 - V.TP - 6) * MM; xo = (V.RB + V.ET + 0.4) * MM
    EK = [("etiket_ad", etiket_yuzu(-xo, e0, e1, -ez, ez, -1), "etiket_ad"),
          ("etiket_montaj", etiket_yuzu(xo, e0, e1, ez, -ez, 1), "etiket_montaj")]
    for adi, xx, nx in (("etiket_ad_arka", -xo + 0.0002, 1), ("etiket_montaj_arka", xo - 0.0002, -1)):
        ar = Mesh(); ar.quad((xx, e0, -ez), (xx, e0, ez), (xx, e1, ez), (xx, e1, -ez), (nx, 0, 0)); EK.append((adi, ar.duzelt(), "sari_arka"))

    par = [(p["ad"], BR.web_ag(V.ag, p), p["mal"], hangi.get(p["ad"])) for p in V.PARCALAR] + \
          [(a, m, mal, hangi.get(a)) for a, m, mal in EK]
    eksik = [p["ad"] for p in V.PARCALAR if p["ad"] not in hangi]
    assert not eksik, "adimi olmayan parca: %s" % eksik
    return par, sure, H


if __name__ == "__main__":
    par, sure, H = kur()
    V_ = V.v4.hacim_L(V.Y_DOLUM)
    baslik = "KIYMA KASETİ" if "kiyma" in MODUL else "KUŞBAŞI KASETİ" if "kusbasi" in MODUL else "KÜP SUCUK KASETİ" if "sucuk" in MODUL else "KAŞAR KABI"
    dokular = {"ad": doku_ad(baslik, "bu yönde tak  ·  %d × 325 × 360 mm" % V.W + "  ·  %s L  ·  çıkış ÖNDE alttan" % ("%.1f" % V_).replace(".", ","), ok_sol=True),
               "montaj": doku_montaj(["HELEZONU|ÖNDEN SÜR", "YATAK KAPAĞI|İT · 35° ÇEVİR · KLİK", ("KAFES" if KASAR else "ROTOR") + " · MİL|TOPUZ · PİM", "TAPAYI ÇIKAR|YUVAYA SÜR"])}
    b = V.glb_yaz(os.path.join(OUT, ONEK + "_montaj.glb"), par, dokular)
    print(ONEK + "_montaj.glb · %d parca · %d adim · %.1f sn · %.0f KB" % (len(par), len(ADIMLAR), sure, b / 1024.0))

    # ---- AYNI ANİMASYON USDZ'YE (iPhone AR): iPhone yalnız YAZILI örnekleri okur → hareket pencerelerinde HER KARE yazılır ----
    kare = lambda a, b_: [a + j / 30.0 for j in range(int(round((b_ - a) * 30.0)) + 1)] + [b_]
    anim = {}; adlar = set(a_ for a_, m_, mal_, g_ in par)
    for p_, (pivot, kay, don, P) in H.items():
        if p_ not in adlar: continue
        anlar = sorted(set([0.0, sure] + [t for a, b_ in P for t in kare(a, b_)]))
        keys = [(t, tuple(c * MM for c in kay(t)), -360.0 * don(t)) for t in anlar]
        anim[p_] = dict(pivot=tuple(c * MM for c in pivot) if pivot else None, keys=keys)
    b2, prim, sorun, uyari = usdz_yaz([os.path.join(OUT, ONEK + "_montaj.usdz")], ONEK + "_montaj",
                                      [(a_, m_, mal_) for a_, m_, mal_, g_ in par], dokular, anim=anim, fps=30.0, sure=sure)
    print(ONEK + "_montaj.usdz · %.0f KB · %d prim · USD denetimi: %s" % (b2 / 1024.0, prim, "GECTI" if not sorun else "KALDI"))
    for x in sorun: print("   HATA:", x)
    # ---- ÇALIŞMA ANİMASYONU USDZ (üretim / dozaj sekmelerinin iPhone AR dosyası): helezon + karıştırıcı/rotor döner ----
    # Quick Look animasyonu DÖNGÜYE alır → tur sayısı TAM olmalı ki başa sararken sıçramasın (yalnız görsel).
    T_, D_ = 10.0, 12.0; grp = {p_["ad"]: p_["grup"] for p_ in V.PARCALAR}; anim2 = {}
    for g_ in ("helezon", "karistirici"):
        tur_ = GRUP_CALIS[g_]["aci"](T_); tur_ = float(round(tur_)) if abs(round(tur_)) >= 1 else math.copysign(1.0, tur_)
        keys_ = [(j / 30.0, (0, 0, 0), 360.0 * tur_ * (j / 30.0) / T_) for j in range(int(T_ * 30) + 1)] + [(D_, (0, 0, 0), 360.0 * tur_)]   # her kare
        for a_, g2 in grp.items():
            if g2 == g_: anim2[a_] = dict(pivot=GRUP_CALIS[g_]["pivot"], keys=keys_)
    calis = [(a_, m_, mal_) for a_, m_, mal_, _ in par if a_ != "tasima_tapasi"]
    b3, prim3, sorun3, _u = usdz_yaz([os.path.join(OUT, ONEK + "_calis.usdz")], ONEK + "_calis", calis, dokular, anim=anim2, fps=30.0, sure=D_)
    print(ONEK + "_calis.usdz · %.0f KB · %d hareketli parca · USD denetimi: %s" % (b3 / 1024.0, len(anim2), "GECTI" if not sorun3 else "KALDI"))

    import io, json
    with io.open(os.path.join(OUT, ONEK + "_adimlar.json"), "w", encoding="utf-8") as f:                 # sayfadaki adım listesi buradan okunur (elle yazılmaz)
        json.dump([[round(BASLA + i * ADIM_SURE, 1), a[0]] for i, a in enumerate(ADIMLAR)], f, ensure_ascii=False)
    for i, a in enumerate(ADIMLAR):
        print("  %2d  %5.1f sn  %-62s %d parca" % (i + 1, BASLA + i * ADIM_SURE, a[0], len([p for p in a[1] if p in H])))
    sys.stdout.flush(); os._exit(0)
