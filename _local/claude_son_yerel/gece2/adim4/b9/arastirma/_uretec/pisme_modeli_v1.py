# -*- coding: utf-8 -*-
"""AUTOKITCH · BASİT PİŞME MODELİ v1 (28 Eyl 2026 · Kemal: "pişmeyi simüle eden basit ısı modelini yaz")

Ne yapar: pideyi / lahmacunu / pizzayı alttan üste katmanlar halinde (hamur + malzeme) 1 boyutlu ısı iletimiyle ısıtır.
Fırın üstten ve alttan ısı verir (kızılötesi ışınım + sıcak hava). Su 100 °C'de buharlaşır (yüzeye yakın katmanlarda).
Her ürün için "piş" sayılma anını bulur:
  · hamurun ortası ≥ 95 °C           (hamur pişti)
  · alt yüz ≥ 150 °C                 (alt kızarmaya başladı)
  · et / harç katmanının ortası ≥ 72 °C (et güvenli)
  · kaşar ≥ 70 °C                    (eridi)
  · uyarı: üst yüz > 220 °C          (yanma riski) · lahmacunda su kaybı
Kalibrasyon: (1) Domino's sıcak hava jetli bant fırını ≈ 250 °C → pizza 6–7 dk · (2) taş fırın lahmacun 3–5 dk.
Bütün malzeme ve fırın değerleri VARSAYIM (literatür tipik değerleri) — kaba karşılaştırma verir, kesin süre değil.
Çalıştır: python pisme_modeli_v1.py  → pisme_modeli_v1.json + pisme_modeli_v1.png"""
import json, os, math
import numpy as np

SIG = 5.670e-8
U = os.path.dirname(os.path.abspath(__file__))
A_URUN = math.pi * 0.14 ** 2                       # Ø280 · m²

# ---- malzeme: k (W/mK), ρ (kg/m³), cp (J/kgK), su oranı ----
MAL = {"hamur": (0.45, 1050.0, 2800.0, 0.42), "harc": (0.45, 1050.0, 3300.0, 0.60), "kiyma": (0.45, 1050.0, 3300.0, 0.60),
       "kusbasi": (0.45, 1060.0, 3500.0, 0.70), "sucuk": (0.35, 1050.0, 2800.0, 0.35), "kasar": (0.30, 1000.0, 2600.0, 0.40),
       "sos": (0.50, 1050.0, 3800.0, 0.85)}


def kalinlik(g, mal):                             # gram → eşdeğer katman (mm), Ø280 alana yayılmış
    return g / 1000.0 / (MAL[mal][1] * A_URUN) * 1000.0


# ---- ürünler (alttan üste) · gramajlar hesap kaydından (kaşarlı 130 · sucuklu 90 + 70 · kıyma 160 · kuşbaşı 145 · lahmacun 110 · pizza 80 + 100 + 70) ----
# hamur: pide / pizza topu 250 g → ≈ 3,9 mm (açılmış) · lahmacun 110 g → ≈ 1,7 mm  [VARSAYIM]
URUN = {
    "Lahmacun":        [("hamur", kalinlik(110, "hamur")), ("harc", kalinlik(110, "harc"))],
    "Kaşarlı pide":    [("hamur", kalinlik(250, "hamur")), ("kasar", kalinlik(130, "kasar"))],
    "Kıymalı pide":    [("hamur", kalinlik(250, "hamur")), ("kiyma", kalinlik(160, "kiyma"))],
    "Kuşbaşılı pide":  [("hamur", kalinlik(250, "hamur")), ("kusbasi", 5.0)],        # 10 mm küp: 5 yüzden ısınır → ≈ 5 mm katman eşdeğeri [VARSAYIM]
    "Sucuklu pide":    [("hamur", kalinlik(250, "hamur")), ("kasar", kalinlik(90, "kasar")), ("sucuk", 4.0)],   # küp sucuk ≈ 8 mm → 4 mm eşdeğer
    "Pizza":           [("hamur", kalinlik(250, "hamur")), ("sos", kalinlik(80, "sos")), ("kasar", kalinlik(100, "kasar")), ("sucuk", 4.0)],
}
ET = ("harc", "kiyma", "kusbasi", "sucuk")

# ---- fırınlar: üst / alt ısı kaynakları ----
# her yüz: ışınım (kaynak sıcaklığı, etkin ε·görüş) + taşınım (hava sıcaklığı, h) + (alt) temas (taş sıcaklığı, h_temas)
FIRIN = {
    "Domino's tipi · sıcak hava jeti 250 °C (kalibrasyon: pizza 6–7 dk)":
        dict(ust=dict(Tr=250, er=0.7, Ta=250, h=90), alt=dict(Tr=250, er=0.5, Ta=250, h=70), sure_sinir=12),
    "Taş fırın 300 °C (kalibrasyon: lahmacun 3–5 dk)":
        dict(ust=dict(Tr=380, er=0.75, Ta=300, h=15), alt=dict(temas=300, htemas=250), sure_sinir=12),
    "Kızılötesi bant · eleman 400 °C · hava 250 °C":
        dict(ust=dict(Tr=400, er=0.75, Ta=250, h=20), alt=dict(Tr=400, er=0.55, Ta=250, h=20), sure_sinir=12),
    "Kızılötesi bant · eleman 450 °C · hava 270 °C":
        dict(ust=dict(Tr=450, er=0.75, Ta=270, h=20), alt=dict(Tr=450, er=0.55, Ta=270, h=20), sure_sinir=12),
    "Kızılötesi bant · eleman 500 °C · hava 290 °C":
        dict(ust=dict(Tr=500, er=0.75, Ta=290, h=20), alt=dict(Tr=500, er=0.55, Ta=290, h=20), sure_sinir=12),
}
T0 = 4.0                                          # dolaptan / kasetten gelir (+3…+5 °C)
L_BUHAR = 2.26e6
KABUK_MM = 1.5                                    # yüzeye bu kadar yakın katmanlar buharlaşabilir (kabuk / kuruyan üst)


def simule(urun, firin, dt=0.02, dx=0.25e-3):
    # ızgara
    k, rho, cp, w, mal, zmid = [], [], [], [], [], []
    for m_, t_ in URUN[urun]:
        n = max(2, int(round(t_ * 1e-3 / dx)))
        for _ in range(n):
            K_, R_, C_, W_ = MAL[m_]; k.append(K_); rho.append(R_); cp.append(C_); w.append(W_); mal.append(m_)
    k, rho, cp, w = map(np.array, (k, rho, cp, w)); N = len(k)
    T = np.full(N, T0); su = w * rho * dx                # kg/m² su her düğümde
    su0 = su.sum()
    derin = np.minimum(np.arange(N) + 0.5, N - np.arange(N) - 0.5) * dx * 1e3
    buhar_ok = derin <= KABUK_MM
    kf = 2 * k[:-1] * k[1:] / (k[:-1] + k[1:])           # arayüz iletkenliği
    C = rho * cp * dx
    iH = [i for i, m_ in enumerate(mal) if m_ == "hamur"]; hamur_orta = iH[len(iH) // 2]
    et = [i for i, m_ in enumerate(mal) if m_ in ET]; et_orta = et[len(et) // 2] if et else None
    ks = [i for i, m_ in enumerate(mal) if m_ == "kasar"]
    kriter = {"hamur ortası ≥ 95": None, "alt yüz ≥ 150": None}
    if et: kriter["et ortası ≥ 72"] = None
    if ks: kriter["kaşar ≥ 70"] = None
    iz = {"t": [], "alt": [], "hamur": [], "ust": [], "et": []}
    t, adim, f = 0.0, 0, firin

    def yuzey(Ts, d):
        q = 0.0
        if "Tr" in d: q += d["er"] * SIG * ((d["Tr"] + 273.15) ** 4 - (Ts + 273.15) ** 4)
        if "Ta" in d: q += d["h"] * (d["Ta"] - Ts)
        if "temas" in d: q += d["htemas"] * (d["temas"] - Ts)
        return q
    while t < f["sure_sinir"] * 60:
        q = np.zeros(N)
        fl = kf * (T[1:] - T[:-1]) / dx
        q[:-1] += fl; q[1:] -= fl
        q[0] += yuzey(T[0], f["alt"]); q[-1] += yuzey(T[-1], f["ust"])
        Tn = T + q * dt / C
        # buharlaşma: 100 °C'yi aşan enerji suya gider
        fazla = (Tn - 100.0) * C
        m = (Tn > 100.0) & (su > 0)
        evap_ok = m & buhar_ok
        buh = np.minimum(fazla[evap_ok] / L_BUHAR, su[evap_ok])
        su[evap_ok] -= buh; Tn[evap_ok] -= buh * L_BUHAR / C[evap_ok]
        ic = m & ~buhar_ok; Tn[ic] = 100.0                # içeride buhar kaçamaz → 100'de kalır
        T = Tn; t += dt; adim += 1
        tt = t / 60
        if kriter["hamur ortası ≥ 95"] is None and T[hamur_orta] >= 95: kriter["hamur ortası ≥ 95"] = tt
        if kriter["alt yüz ≥ 150"] is None and T[0] >= 150: kriter["alt yüz ≥ 150"] = tt
        if et and kriter["et ortası ≥ 72"] is None and T[et_orta] >= 72: kriter["et ortası ≥ 72"] = tt
        if ks and kriter["kaşar ≥ 70"] is None and T[ks].min() >= 70: kriter["kaşar ≥ 70"] = tt
        if adim % 50 == 0:
            iz["t"].append(tt); iz["alt"].append(T[0]); iz["hamur"].append(T[hamur_orta]); iz["ust"].append(T[-1])
            iz["et"].append(T[et_orta] if et else None)
        if all(v is not None for v in kriter.values()) and "t_piş" not in iz:
            iz["t_piş"] = tt; iz["ust_piste"] = float(T[-1]); iz["su_kaybi"] = float(1 - su.sum() / su0)
        if "t_piş" in iz and t > iz["t_piş"] * 60 + 30: break
    son = max(kriter, key=lambda k_: kriter[k_] if kriter[k_] is not None else 1e9)
    return dict(kriter={k_: (round(v, 2) if v is not None else None) for k_, v in kriter.items()},
                pis=round(iz.get("t_piş"), 2) if iz.get("t_piş") else None, son_kriter=son,
                ust_piste=round(iz.get("ust_piste", float("nan")), 0) if "ust_piste" in iz else None,
                su_kaybi=round(100 * iz.get("su_kaybi", float("nan")), 1) if "su_kaybi" in iz else None, iz=iz)


if __name__ == "__main__":
    SON = {}
    for fad, f in FIRIN.items():
        print("\n== " + fad)
        SON[fad] = {}
        for u in URUN:
            r = simule(u, f); SON[fad][u] = r
            uy = []
            if r["ust_piste"] and r["ust_piste"] > 220: uy.append("üst %d °C yanma riski" % r["ust_piste"])
            print("   %-15s piş %5s dk  (en son: %-17s) · üst yüz %s °C · su kaybı %%%s %s" % (
                u, ("%.1f" % r["pis"]) if r["pis"] else ">12", r["son_kriter"], r["ust_piste"], r["su_kaybi"], " · ".join(uy)))
    json.dump({f: {u: {k: v for k, v in r.items() if k != "iz"} for u, r in d.items()} for f, d in SON.items()},
              open(os.path.join(U, "pisme_modeli_v1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # grafik: kızılötesi 450 · her ürün için alt yüz / hamur ortası / et
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "Arial"
    fad = "Kızılötesi bant · eleman 450 °C · hava 270 °C"
    fig, axs = plt.subplots(2, 3, figsize=(14, 7.5), dpi=130, sharex=True, sharey=True)
    for ax, u in zip(axs.flat, URUN):
        iz = SON[fad][u]["iz"]
        ax.plot(iz["t"], iz["alt"], color="#8a5a2b", label="alt yüz")
        ax.plot(iz["t"], iz["hamur"], color="#d4a24c", label="hamur ortası")
        ax.plot(iz["t"], iz["ust"], color="#c0392b", label="üst yüz")
        if any(v is not None for v in iz["et"]): ax.plot(iz["t"], iz["et"], color="#6b2d20", ls="--", label="et / harç ortası")
        p = SON[fad][u]["pis"]
        if p: ax.axvline(p, color="#1f7a4d", lw=1.2); ax.text(p + 0.05, 20, "piş %.1f dk" % p, color="#1f7a4d", fontsize=9)
        ax.set_title(u, fontsize=11); ax.grid(alpha=.3); ax.set_ylim(0, 320)
    axs[0, 0].legend(fontsize=8, loc="upper left"); fig.supxlabel("dakika"); fig.supylabel("°C")
    fig.suptitle("Basit pişme modeli · " + fad + " (VARSAYIM değerler)", fontsize=12)
    plt.tight_layout(); plt.savefig(os.path.join(U, "pisme_modeli_v1.png")); print("\ngrafik: pisme_modeli_v1.png")
