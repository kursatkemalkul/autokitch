# -*- coding: utf-8 -*-
"""AUTOKITCH · FIRIN → B YÜK YOLU + B AĞIRLIK ZARFI · hesap v1 (29 Eyl 2026)

Kemal 29 Eyl: "her dediğini yap" → Codex Modüler v1'in 7 kiriş hesabında olmayan iki konu:
  1) Fırın (F) B'nin sağ 1,5 m'sine oturuyor; taşıyıcısı (store_cad 40×40×2 çerçeve) yalnız
     fırın 200 + raf 99 kg ile hesaplanmıştı, üst kabin kabukları hesapta yoktu.
  2) B'nin taşıma zarfı 1000 kg VARSAYIM; CAD'de bilinen 843 kg + bilinmeyen malzemeli parçalar.

CAD DEĞİŞMEZ. Girdi: Codex Modüler v1 (otonom/hat/moduler-v1: GLB + parts.json + checks.json)
ve store_cad_v9 sabitleri (aşağıda kaynak satırlarıyla). Çıktı: firin_b_yuk_hesap_v1.json.
"""
import io
import json
import math
import os
import struct

import numpy as np

KOK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
MOD = os.path.join(KOK, "otonom", "hat", "moduler-v1")
g = 9.81

# ---------------------------------------------------------------- KAYNAKLI SABİTLER
# store_cad_v9.py satır 201–213 (fırın taşıyıcı çerçevesi, B içinde)
TD_X = (2517.5, 3172.5, 3792.5)      # dikme ekseni x
TD_Z = (-110.0, -620.0)              # ön / arka kiriş ekseni z
TK_X = (2502.5, 3996.5)              # kiriş boyu (fırın 2500–4000 altı)
TK_Y = (746.5, 786.5)                # kiriş alt / üst
Y_PLINT = 123.0                      # store_cad_v9 · dikme alt ucu Y_PLINT + 1,5
L_DIKME = TK_Y[0] - (Y_PLINT + 1.5)  # 622
E304 = 193000.0                      # MPa · store_cad_v9 ve Codex ile aynı
AKMA = 205.0                         # MPa · 304 akma (store_cad_v9 ölçütü)
IZIN = AKMA / 1.5                    # 137 MPa · store_cad_v9 ölçütü
KIRIS = (40.0, 40.0, 2.0)            # "Taşıyıcı kiriş 40 × 40 × 2" (store_cad_v6 BOM satır 433)
DIKME = (30.0, 30.0, 2.0)            # "Taşıyıcı dikme 30 × 30 × 2" (satır 437)
EMN = 1.5                            # store_cad_v9 yük katsayısı [VARSAYIM] — aynen korunur

# Fırın ve raf yükü: store_cad_v9 satır 209–212 (firin_tp10_cad_v6 kaynaklı)
M_FIRIN, ZG_FIRIN = 200.0, -286.0    # [VARSAYIM] uzatılmış TP10 1500 ≈ 200 (katalog TP10 160 kg)
RAF = {                               # firin_tp10_cad_v6 RAF YÜKÜ = 99 kg
    "raf": (19.0, (2510.0, 3990.0), -217.5),
    "isi_kalkani": (3.8, (2510.0, 3990.0), -217.5),
    "pizza_kutusu_320": (51.2, (2520.0, 3324.0), -222.0),   # Bekar Ambalaj 100 adet 16 kg → 0,16 kg/kutu
    "kompresor_JUNAIR_OF302_15B": (25.0, None, -230.0),     # 4 ayak x 3625 / 3955 (parts.json f_komp_urun_ayagi)
}
KOMP_AYAK_X = (3625.0, 3955.0)

# Üst kabin (fırının üstü, F modülü): Codex checks.json mass_parts (CAD hacim × yoğunluk)
UST_KABIN_ADLAR = ["f_davlumbaz_kutusu", "f_ust_arka_sac", "f_ust_tavan_sac", "f_ust_yan_sol", "f_ust_yan_sag",
                   "onyuz_f_ust_kapak_sol", "onyuz_f_ust_kapak_sag", "onyuz_f_ust_kayit", "f_komp_tavasi"]
UST_KABIN_KUCUK = 10.0   # [VARSAYIM] listede olmayan küçük parçalar: menteşe, gazlı yay, omega, burulma kutusu, dikme, askı
UST_KABIN_Z = {"f_davlumbaz_kutusu": -633.5, "f_ust_arka_sac": -829.0, "f_ust_tavan_sac": -384.5, "f_ust_yan_sol": -384.5,
               "f_ust_yan_sag": -384.5, "onyuz_f_ust_kapak_sol": 69.0, "onyuz_f_ust_kapak_sag": 69.0,
               "onyuz_f_ust_kayit": 42.0, "f_komp_tavasi": -230.0}   # parts.json bounds orta z


# ---------------------------------------------------------------- GLB (grup hacmi)
def glb_oku(yol):
    with open(yol, "rb") as f:
        v = f.read()
    jl = struct.unpack_from("<I", v, 12)[0]
    gl = json.loads(v[20:20 + jl].decode("utf-8"))
    bo = 20 + jl
    bl = struct.unpack_from("<I", v, bo)[0]
    return gl, memoryview(v)[bo + 8: bo + 8 + bl]


TIP = {5121: np.uint8, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
BOY = {"SCALAR": 1, "VEC3": 3}


def erisim(gl, ik, i):
    a = gl["accessors"][i]
    bv = gl["bufferViews"][a["bufferView"]]
    dt = np.dtype(TIP[a["componentType"]])
    k = BOY[a["type"]]
    bas = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
    adim = bv.get("byteStride", 0) or dt.itemsize * k
    assert adim == dt.itemsize * k
    return np.frombuffer(ik, dtype=dt, count=a["count"] * k, offset=bas).reshape(a["count"], k)


def grup_hacimleri(gl, ik):
    """Her malzeme grubunun kapalı ağ hacmi (L). Düğüm dönüşümü yok varsayılır (Codex GLB: düz düğümler)."""
    for n in gl.get("nodes", []):
        assert not any(k in n for k in ("matrix", "rotation", "scale")), "düğüm dönüşümü var"
    out = {}
    for m in gl["meshes"]:
        for p in m["primitives"]:
            ad = gl["materials"][p["material"]]["name"]
            P = erisim(gl, ik, p["attributes"]["POSITION"]).astype(np.float64)
            I = erisim(gl, ik, p["indices"]).reshape(-1, 3).astype(np.int64)
            a, b, c = P[I[:, 0]], P[I[:, 1]], P[I[:, 2]]
            hac = np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6.0
            olc = 1e3 if np.abs(P).max() < 50 else 1e-6       # m³→L veya mm³→L
            out[ad] = out.get(ad, 0.0) + hac * olc
    return out


# ---------------------------------------------------------------- KİRİŞ (1B sonlu eleman)
def kutu(b, h, t):
    I = (b * h ** 3 - (b - 2 * t) * (h - 2 * t) ** 3) / 12.0
    return I, I / (h / 2.0), b * h - (b - 2 * t) * (h - 2 * t)


def surekli_kiris(x0, x1, destek_x, yayili, tekil, EI, dx=2.5):
    """Euler-Bernoulli. yayili: [(xa, xb, N toplam)], tekil: [(x, N)]. Destekler v=0 (mafsallı)."""
    n = int(round((x1 - x0) / dx))
    xs = np.linspace(x0, x1, n + 1)
    h = xs[1] - xs[0]
    N = 2 * (n + 1)
    K = np.zeros((N, N))
    F = np.zeros(N)
    ke = EI / h ** 3 * np.array([[12, 6 * h, -12, 6 * h], [6 * h, 4 * h * h, -6 * h, 2 * h * h],
                                  [-12, -6 * h, 12, -6 * h], [6 * h, 2 * h * h, -6 * h, 4 * h * h]])
    q = np.zeros(n)                      # eleman başına yayılı yük N/mm (aşağı +)
    xm = (xs[:-1] + xs[1:]) / 2.0
    for xa, xb, Wt in yayili:
        sec = (xm >= xa) & (xm <= xb)
        q[sec] += Wt / (xb - xa)
    for e in range(n):
        d = [2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3]
        K[np.ix_(d, d)] += ke
        fe = q[e] * np.array([h / 2, h * h / 12, h / 2, -h * h / 12])
        F[d] += fe
    for xp, P in tekil:
        i = int(round((xp - x0) / h))
        F[2 * i] += P
    sabit = sorted({2 * int(round((xd - x0) / h)) for xd in destek_x})
    serbest = [i for i in range(N) if i not in sabit]
    u = np.zeros(N)
    u[serbest] = np.linalg.solve(K[np.ix_(serbest, serbest)], F[serbest])
    R = K @ u - F
    # eğilme momenti (eleman ortasında) = EI · v''
    M = np.zeros(n)
    for e in range(n):
        v1, t1, v2, t2 = u[2 * e: 2 * e + 4]
        xi = 0.5
        B = np.array([(-6 + 12 * xi) / h ** 2, (-4 + 6 * xi) / h, (6 - 12 * xi) / h ** 2, (-2 + 6 * xi) / h])
        M[e] = EI * (B @ np.array([v1, t1, v2, t2]))
    tepki = {round(xd, 1): float(-R[2 * int(round((xd - x0) / h))]) for xd in destek_x}
    return xs, u[0::2], xm, M, tepki


def main():
    C = json.load(io.open(os.path.join(MOD, "checks.json"), encoding="utf-8"))
    P = json.load(io.open(os.path.join(MOD, "parts.json"), encoding="utf-8"))
    kg = {(m["module"], m["name"]): m["kg"] for m in C["mass_parts"]}
    S = {"surum": "firin_b_yuk_hesap_v1", "tarih": "2026-09-29", "cad_degisti": False, "kaynaklar": {}}

    # ===================== 1 · F ÜST KABİN + FIRIN YÜKÜ
    kabin = {a: kg[("F", a)] for a in UST_KABIN_ADLAR}
    m_kabin = sum(kabin.values()) + UST_KABIN_KUCUK
    zg_kabin = (sum(kabin[a] * UST_KABIN_Z[a] for a in kabin) + UST_KABIN_KUCUK * -384.5) / m_kabin
    m_raf = sum(v[0] for v in RAF.values())
    m_F = M_FIRIN + m_raf + m_kabin
    S["F_kutle"] = {"firin_VARSAYIM": M_FIRIN, "raf_yuku": m_raf, "raf_kalemleri": {k: v[0] for k, v in RAF.items()},
                    "ust_kabin_cad": round(sum(kabin.values()), 2), "ust_kabin_kucuk_VARSAYIM": UST_KABIN_KUCUK,
                    "ust_kabin_toplam": round(m_kabin, 1), "ust_kabin_zg": round(zg_kabin, 0),
                    "F_kullanimda_toplam": round(m_F, 1),
                    "eski_hesap_store_cad_v9": M_FIRIN + 99.0,
                    "eski_hesapta_olmayan": round(m_kabin, 1)}

    # ===================== 2 · TAŞIYICI KİRİŞLER (ön / arka) · sürekli kiriş, 3 dikme + sağ konsol
    Ik, Wk, Ak = kutu(*KIRIS)
    Id, Wd, Ad = kutu(*DIKME)
    EI = E304 * Ik

    def pay(zg):          # kaldıraç: ön kiriş payı
        on = (zg - TD_Z[1]) / (TD_Z[0] - TD_Z[1])
        return on, 1.0 - on

    sonuc_kiris = {}
    tepkiler = {}
    for k_ad, ki in (("on", 0), ("arka", 1)):
        yay, tek = [], []
        s = pay(ZG_FIRIN)[ki]
        yay.append((TK_X[0], TK_X[1], EMN * M_FIRIN * g * s))
        for ad, (m, xr, zg) in RAF.items():
            s = pay(zg)[ki]
            if xr is None:
                for xa in KOMP_AYAK_X:
                    tek.append((xa, EMN * m * g * s / len(KOMP_AYAK_X)))
            else:
                yay.append((xr[0], xr[1], EMN * m * g * s))
        s = pay(zg_kabin)[ki]
        for xu in (2508.0, 3992.0):          # üst kabin yan duvarları iki uçta oturur (parts.json f_ust_yan_*)
            tek.append((xu, EMN * m_kabin * g * s / 2.0))
        xs, v, xm, M, R = surekli_kiris(TK_X[0], TK_X[1], TD_X, yay, tek, EI)
        imax = int(np.argmax(np.abs(M)))
        acik_max = max(TD_X[1] - TD_X[0], TD_X[2] - TD_X[1])
        konsol = TK_X[1] - TD_X[2]
        sehim_acik = float(np.abs(v[(xs > TD_X[0]) & (xs < TD_X[2])]).max())
        sehim_konsol = float(abs(v[-1]))
        sonuc_kiris[k_ad] = {"yuk_toplam_N": round(sum(w[2] for w in yay) + sum(t[1] for t in tek), 0),
                             "M_max_Nmm": round(float(M[imax]), 0), "M_max_x": round(float(xm[imax]), 1),
                             "gerilme_MPa": round(abs(float(M[imax])) / Wk, 1), "izin_MPa": round(IZIN, 0),
                             "sehim_aciklik_mm": round(sehim_acik, 3), "sinir_L500_mm": round(acik_max / 500.0, 2),
                             "sehim_konsol_ucu_mm": round(sehim_konsol, 3), "sinir_konsol_a250_mm": round(konsol / 250.0, 2),
                             "dikme_tepkileri_N": {str(k): round(v_, 0) for k, v_ in R.items()},
                             "gecti": bool(abs(M[imax]) / Wk <= IZIN and sehim_acik <= acik_max / 500.0
                                           and sehim_konsol <= konsol / 250.0)}
        tepkiler[k_ad] = R

    # ===================== 3 · DİKMELER 30×30×2 (Euler, iki uç mafsallı)
    Pcr = math.pi ** 2 * E304 * Id / L_DIKME ** 2
    Rmax = max(max(r.values()) for r in tepkiler.values())
    S["dikme"] = {"profil": "30×30×2 AISI 304", "boy_mm": L_DIKME, "en_yuklu_N": round(Rmax, 0),
                  "eksenel_MPa": round(Rmax / Ad, 1), "Euler_Pcr_N": round(Pcr, 0),
                  "burkulma_guvenligi": round(Pcr / Rmax, 1), "gecti": bool(Pcr / Rmax >= 3.0 and Rmax / Ad <= IZIN)}

    # ===================== 4 · B AĞIRLIĞI (taşıma = gıda yok) · bilinmeyen malzemeler
    gl, ik = glb_oku(os.path.join(MOD, "moduler_v1.glb"))
    hac = grup_hacimleri(gl, ik)
    Bh = {}
    for ad, L in hac.items():
        mod, tur, mal, _ = ad.split("__")
        if mod == "B":
            Bh[mal] = Bh.get(mal, 0.0) + L
    # yoğunluk aralıkları [VARSAYIM, g/cm³ = kg/L]; katalog ağırlığı olan kalemler ayrıca
    YOG = {"motor": (2.5, 5.0), "kart": (0.6, 1.5), "siemens": (0.5, 0.9), "koyu": (1.1, 1.6), "plastik": (0.95, 1.45),
           "bakir": (0.4, 1.2), "kanal": (0.4, 1.4), "silikon": (1.1, 1.3), "conta": (1.0, 1.3)}
    GIDA = {"hamur": 1.15, "kutu_icecek": 1.0, "poset": 0.3}          # kullanımda; taşımada boşaltılır
    parca_say = {}
    for p in P:
        if p["module"] == "B":
            parca_say[p["material"]] = parca_say.get(p["material"], 0) + 1
    B_bilinen = C["masses"]["B"]["known_material_kg"]
    alt = ust = 0.0
    kalem = {}
    for mal, (a, b) in YOG.items():
        L = Bh.get(mal, 0.0)
        kalem[mal] = {"hacim_L": round(L, 2), "parca": parca_say.get(mal, 0), "kg_alt": round(L * a, 1), "kg_ust": round(L * b, 1)}
        alt += L * a
        ust += L * b
    # Secop NLE8.8CN kompresör: üretici föyü 10,9 kg (koyu grubu içinde modelli; aralığın üst ucu en az bunu kapsasın)
    KOMP_SECOP = 10.9
    gida = {m: round(Bh.get(m, 0.0) * d, 1) for m, d in GIDA.items()}
    # evaporatör lamel blokları CAD'de dolu alüminyum sayılmış (Codex: 30,84 + 20,43 kg)
    evap_cad = kg.get(("B", "evaporator_sol_lamel"), 0.0) + kg.get(("B", "evaporator_sag_lamel"), 0.0)
    evap_gercek = (0.15 * evap_cad, 0.35 * evap_cad)        # [VARSAYIM] lamel+boru dolu hacmin %15–35'i
    B_tasima = (B_bilinen + alt + KOMP_SECOP - (evap_cad - evap_gercek[1]),
                B_bilinen + ust + KOMP_SECOP)               # üst uçta evaporatör düzeltmesi yok (muhafazakâr)
    S["B_agirlik"] = {"codex_bilinen_kg": round(B_bilinen, 1), "bilinmeyen_kalemler": kalem,
                      "secop_NLE8_8CN_katalog_kg": KOMP_SECOP, "evaporator_cad_kg": round(evap_cad, 1),
                      "evaporator_gercek_tahmin_kg": [round(x, 1) for x in evap_gercek],
                      "B_tasima_bos_kg": [round(x, 0) for x in B_tasima], "gida_kullanimda_kg": gida,
                      "codex_zarfi_kg": 1000.0}
    # Codex B boş taşıma kirişi (60×80×3 × 2, L 1000, ortada tekil, ×2): σ = 133,2 × m/1000
    I6, W6, _ = kutu(60.0, 80.0, 3.0)
    def sig_B(m, L):
        return (m * g * 2.0 / 2.0) * L / 4.0 / W6
    m_sinir_1000 = 140.0 / sig_B(1.0, 1000.0)
    L_oneri = None
    for L in range(1000, 400, -50):
        if sig_B(B_tasima[1], L) <= 140.0:
            L_oneri = L
            break
    S["B_tasima_kirisi"] = {"sigma_1000mm_ust_uc_MPa": round(sig_B(B_tasima[1], 1000.0), 1),
                            "1000mm_icin_en_fazla_kg": round(m_sinir_1000, 0),
                            "ust_uc_icin_destek_araligi_mm": L_oneri,
                            "sigma_800mm_1200kg_MPa": round(sig_B(1200.0, 800.0), 1)}

    # ===================== 5 · AYAKLAR (fırın dikmelerinin altı) · hizmet yükü (katsayısız)
    x_ayak = [60.0, 1000.0, 1960.0, 2517.5, 3172.5, 3792.5, 3940.0]
    ayak = {}
    for i, xa in enumerate(x_ayak):
        if xa not in TD_X:
            continue
        sol = (x_ayak[i - 1] + xa) / 2.0
        sag = (x_ayak[i + 1] + xa) / 2.0 if i + 1 < len(x_ayak) else 4000.0
        B_pay = 1000.0 * (sag - sol) / 4000.0 / 2.0              # B zarfı 1000 kg, boyca düzgün, ön/arka yarı
        for k_ad in ("on", "arka"):
            F_pay = tepkiler[k_ad][round(xa, 1)] / EMN / g         # katsayısız kg
            ayak["%s_%s" % (xa, k_ad)] = {"firindan_kg": round(F_pay, 1), "B_payi_kg": round(B_pay, 1),
                                          "toplam_kg": round(F_pay + B_pay, 1), "toplam_N": round((F_pay + B_pay) * g, 0)}
    S["ayaklar_firin_alti"] = ayak
    S["ayak_kapasitesi"] = "Elesa LV.A-SST M12: statik yük KATALOGDAN TEYİT (elesa-ganter.com sayfasında tablo çıkmadı)"

    S["kirisler"] = sonuc_kiris
    S["kesit"] = {"kiris_40x40x2": {"I_mm4": round(Ik, 0), "W_mm3": round(Wk, 0)},
                  "dikme_30x30x2": {"I_mm4": round(Id, 0), "A_mm2": round(Ad, 0)}}
    S["denetim"] = {
        "D1 fırın taşıyıcı ön kiriş": sonuc_kiris["on"]["gecti"],
        "D2 fırın taşıyıcı arka kiriş": sonuc_kiris["arka"]["gecti"],
        "D3 dikme burkulma ≥ 3": S["dikme"]["gecti"],
        "D4 B taşıma ağırlığı üst ucu ≤ 1000 kg zarfı": bool(B_tasima[1] <= 1000.0),
    }
    S["kaynaklar"] = {
        "tasiyici_cerceve": "arastirma/_uretec/store_cad_v9.py satır 201–213 (TD_X, TD_Z, TK_X, TK_Y, M_FIRIN, M_RAF, EMN) + store_cad_v6 BOM satır 433–437",
        "raf_yuku": "firin_tp10_cad_v6 RAF YÜKÜ 99 kg (raf 19 + 320 kutu 51,2 + kompresör 25 + kalkan 3,8)",
        "ust_kabin": "otonom/hat/moduler-v1/checks.json mass_parts (Codex, CAD hacim × yoğunluk)",
        "B_bilinmeyen_hacim": "otonom/hat/moduler-v1/moduler_v1.glb grup ağları (kapalı ağ hacmi)",
        "secop": "https://www.secop.com/fileadmin/user_upload/SEPS/datasheets/en/nle88cn_105h6880_r290_220v_50hz_05-2026_ds.pdf (10,9 kg)",
    }
    yol = os.path.join(KOK, "arastirma", "_uretec", "firin_b_yuk_hesap_v1.json")
    with io.open(yol, "w", encoding="utf-8") as f:
        json.dump(S, f, ensure_ascii=False, indent=1)
    # ---- özet
    print("F kullanımda: fırın %.0f (VARSAYIM) + raf yükü %.0f + üst kabin %.1f = %.1f kg (eski hesap %.0f; eksik %.1f kg)"
          % (M_FIRIN, m_raf, m_kabin, m_F, M_FIRIN + 99.0, m_kabin))
    for k_ad, r in sonuc_kiris.items():
        print("kiriş %-4s yük %6.0f N · M %7.0f N·mm @x %.0f · σ %5.1f / %.0f MPa · sehim açıklık %.3f (≤%.2f) konsol ucu %.3f (≤%.2f) · dikme %s · %s"
              % (k_ad, r["yuk_toplam_N"], r["M_max_Nmm"], r["M_max_x"], r["gerilme_MPa"], IZIN, r["sehim_aciklik_mm"],
                 r["sinir_L500_mm"], r["sehim_konsol_ucu_mm"], r["sinir_konsol_a250_mm"], r["dikme_tepkileri_N"],
                 "GEÇTİ" if r["gecti"] else "KALDI"))
    d = S["dikme"]
    print("dikme 30×30×2 · en yüklü %.0f N · %.1f MPa · Euler %.0f N · güvenlik %.0f" % (d["en_yuklu_N"], d["eksenel_MPa"], d["Euler_Pcr_N"], d["burkulma_guvenligi"]))
    b = S["B_agirlik"]
    print("B bilinen %.0f kg · bilinmeyen kalemler: %s" % (b["codex_bilinen_kg"], {k: (v["hacim_L"], v["kg_alt"], v["kg_ust"]) for k, v in b["bilinmeyen_kalemler"].items()}))
    print("B boş taşıma tahmini %s kg (Secop föy 10,9 dahil; evaporatör CAD %.1f → gerçek %s) · gıda kullanımda %s"
          % (b["B_tasima_bos_kg"], b["evaporator_cad_kg"], b["evaporator_gercek_tahmin_kg"], b["gida_kullanimda_kg"]))
    t = S["B_tasima_kirisi"]
    print("B taşıma kirişi: üst uçta 1000 mm'de σ %.1f MPa · 1000 mm için en fazla %.0f kg · önerilen destek aralığı %s mm"
          % (t["sigma_1000mm_ust_uc_MPa"], t["1000mm_icin_en_fazla_kg"], t["ust_uc_icin_destek_araligi_mm"]))
    for k, v in ayak.items():
        print("ayak %-12s fırından %5.1f + B %5.1f = %5.1f kg (%.0f N)" % (k, v["firindan_kg"], v["B_payi_kg"], v["toplam_kg"], v["toplam_N"]))
    print("DENETİM:", S["denetim"])


if __name__ == "__main__":
    main()
