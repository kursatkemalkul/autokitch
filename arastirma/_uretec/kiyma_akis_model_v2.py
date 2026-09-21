# -*- coding: utf-8 -*-
"""AUTOKITCH · KIYMA AKIŞ MODELİ v2 (22 Eyl 2026) · ORTAK GÖVDE (tekne Ø72 / kanat Ø68): vida büyüdü, devir düştü
(v1) — macun TANE DEĞİL: serpilmez, ŞERİT olarak serilir. Matematiği süreklilik:
    şeridin çıkış hızı = altındaki hamurun yüzey hızı   (hızlıysa şerit kopar/sıvanır, yavaşsa yığılır)
    şerit kesiti × serilen boy = doz hacmi
KAYNAKLI: porsiyon 160 g · 20 pide/gün · 2 gün 6,4 kg (pafta HAT v19 + tedarikçi yazışması) · pide Ø280, dolu bölge R125 · doz süresi 10 sn
VARSAYIM: yoğunluk 1,0 g/mL · doluluk 0,40 · karışımdaki en iri parça (soğan/domates) 5 mm → şerit kalınlığı ≥ 2 × 5 = 10 mm
"""
import json, math, os
from kasar_akis_model_v2 import T_DOK, PIDE_R, KENAR

PORS, KG2, RHO = 160.0, 6.4, 1.0
AGIZ = (30.0, 30.0)                                  # kiyma_cad_v1: meme 30 × 30 (genişlik x · boy z)
PARCA_MAX, KALINLIK_KATI = 5.0, 2.0                  # VARSAYIM
R_DOLU = PIDE_R - KENAR                              # 125
G = dict(RT=36.0, C=2.0, R_MIL=9.0, R_KOK=15.0, T=4.0, P0=36.0, P1=48.48, ETAF=0.40)      # v2: ORTAK GÖVDE → tekne Ø72, kanat Ø68, kanat 4 mm

V_DOZ = PORS / RHO * 1000.0                          # mm³
Q = V_DOZ / T_DOK                                    # mm³/s
ALAN = math.pi * R_DOLU ** 2
H_GEREK = V_DOZ / ALAN                               # pideyi TAM kaplayan katman kalınlığı


def serit(w, h):
    """w × h kesitli şerit: çıkış hızı, serilen boy, kapladığı alan oranı"""
    v = Q / (w * h); L = v * T_DOK; return v, L, 100.0 * L * w / ALAN


def spiral(w, h, r0=None):
    """süreklilik spirali: turlar yan yana (tur başına içeri w), yüzey hızı = çıkış hızı → θ(t), r(t), tur sayısı"""
    v, L, _ = serit(w, h); r0 = (R_DOLU - w / 2.0) if r0 is None else r0; s, r, th, dt, P = 0.0, r0, 0.0, 0.01, []
    t = 0.0
    while t <= T_DOK + 1e-9:
        P.append((t, r, th)); dth = v * dt / max(r, 5.0); th += dth; r = max(w / 2.0, r - w * dth / (2 * math.pi)); t += dt
    return P


_SP = spiral(*AGIZ)


def r_t_k(t):
    i = min(len(_SP) - 1, max(0, int(round(t / 0.01)))); return _SP[i][1]


def tabla_tur(t):
    """tablanın o ana kadar attığı tur (kıymada SABİT DEVİR DEĞİL: yüzey hızı şerit hızına eşit)"""
    i = min(len(_SP) - 1, max(0, int(round(min(t, T_DOK) / 0.01)))); return _SP[i][2] / (2 * math.pi)


if __name__ == "__main__":
    S = {}
    print("=== KIYMA · MACUN SERIT OLARAK SERILIR ===")
    print("doz %.0f g = %.0f mL · %.0f sn → %.1f mL/s · dolu bolge R%.0f = %.0f cm2 → TAM kaplama icin katman %.2f mm" % (PORS, V_DOZ / 1000, T_DOK, Q / 1000, R_DOLU, ALAN / 100, H_GEREK))
    v, L, kap = serit(*AGIZ)
    print("SIMDIKI MEME %g x %g: cikis hizi %.1f mm/s · serilen boy %.0f mm · pidenin %%%.0f'ini kaplar (kalinlik %g mm)" % (AGIZ[0], AGIZ[1], v, L, kap, AGIZ[1]))
    v35 = 2 * math.pi * 35.0 / 60.0 * 105.0
    print("tabla 35 dev/dk donerse r105'te yuzey hizi %.0f mm/s = serit hizinin %.0f kati → serit KOPAR / SIVANIR (kasar ve kusbasi icin dogru olan devir, macun icin yanlis)" % (v35, v35 / v))
    print("sureklilik icin tabla devri: r105'te %.1f · r60'ta %.1f · r30'da %.1f dev/dk · 10 sn'de toplam %.2f tur" % (v / 105 * 60 / (2 * math.pi), v / 60 * 60 / (2 * math.pi), v / 30 * 60 / (2 * math.pi), tabla_tur(T_DOK)))
    hmin = PARCA_MAX * KALINLIK_KATI
    print("PARCA SINIRI: en iri parca %.0f mm (VARSAYIM) → serit kalinligi >= %.0f mm → ne kadar genis olursa olsun serit pidenin en cok %%%.0f'ini kaplar" % (PARCA_MAX, hmin, 100 * H_GEREK / hmin))
    print("   → TAM kaplama icin serilen serit %.1f kat YAYILMALI (%.0f mm → %.2f mm): YAYICI (siyirma bicagi / rulo) ya da elle yayma gerekir. Spiral tek basina YETMEZ." % (hmin / H_GEREK, hmin, H_GEREK))
    S["secenek"] = []
    for ad, w, h in (("şimdiki meme 30 × 30", 30.0, 30.0), ("yarık 60 × 10", 60.0, 10.0), ("yarık 90 × 10", 90.0, 10.0), ("kuramsal 60 × 3,3 (parça geçmez)", 60.0, H_GEREK)):
        v_, L_, k_ = serit(w, h); print("   %-34s cikis %5.1f mm/s · boy %5.0f mm · kaplama %%%3.0f" % (ad, v_, L_, k_)); S["secenek"].append(dict(ad=ad, w=w, h=round(h, 2), v=round(v_, 1), L=round(L_), kap=round(k_)))
    Vt = math.pi / 4.0 * ((2 * (G["RT"] - G["C"]) + 2 * G["C"]) ** 2 - (2 * G["R_MIL"]) ** 2) * (G["P1"] - G["T"]) / 1000.0
    g_tur = Vt * G["ETAF"] * RHO
    print("HELEZON: kuramsal %.0f mL/tur · doluluk %.2f VARSAYIM → %.0f g/tur · %.0f g = %.1f tur · %.0f dev/dk (macunda Roberts gecersiz; doluluk ancak denemeyle)" % (Vt, G["ETAF"], g_tur, PORS, PORS / g_tur, PORS / g_tur * 6))
    S.update(dict(PORS=PORS, KG2=KG2, RHO=RHO, Q=round(Q / 1000, 1), H_GEREK=round(H_GEREK, 2), AGIZ=AGIZ, v=round(v, 1), L=round(L), kap=round(kap), v35=round(v35), kat35=round(v35 / v),
                  tur10=round(tabla_tur(T_DOK), 2), hmin=hmin, kap_max=round(100 * H_GEREK / hmin), yay=round(hmin / H_GEREK, 1), Vt=round(Vt), g_tur=round(g_tur), tur=round(PORS / g_tur, 1), rpm=round(PORS / g_tur * 6), G=G))
    cik = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "otonom", "kaset3d", "kiyma_model.json")
    json.dump(S, open(cik, "w", encoding="utf-8"), ensure_ascii=False, indent=1); print("→", cik)
