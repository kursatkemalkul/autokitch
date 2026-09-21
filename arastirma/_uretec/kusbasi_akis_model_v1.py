# -*- coding: utf-8 -*-
"""AUTOKITCH · KUŞBAŞI AKIŞ MODELİ v1 (22 Eyl 2026) — kaşar modelinin (kasar_akis_model_v2) kuşbaşı karşılığı.
Kuşbaşı ne toz ne macun: ISLAK, YUMUŞAK, İRİ TANE. Tasarımı tek sayı yönetir: KÜP KENARI d.

KAYNAKLI
  · porsiyon 145 g · 20 kuşbaşılı pide/gün → 2,9 kg/gün → 2 gün 5,8 kg (pafta HAT v19 + tedarikçi yazışması)
  · pidelik kuşbaşı "olabildiğince minik" doğranır (yemek.com, Kevser'in Mutfağı) — SAYI YOK → d VARSAYIM, ölçülecek
  · çiğ küp et: 1 cup (236,6 mL) = 170–198 g → dökme 0,72–0,84 g/mL (thesmokypan / thehungryskillet) · katı et ≈ 1,06 g/mL
  · iri tanede KÖPRÜ: düşey açıklık ≥ 4 × en iri tane (tek boy malzeme), karışıkta 2–3 × (BulkInside · Ten Steps to an Effective Bin Design)
  · helezonda TOPAK kuralı (CEMA 350 / KWS): mil ile tekne arası radyal boşluk ≥ R × topak · R = 1,75 (%10 topak) · 2,5 (%25) · 4,5 (%95)
  · helezon verimi: Roberts (kaşar modelindeki aynı formül) · duvar sürtünmesi kas dokusu 0,29–0,36 (PubMed 20670064 — kemik/kas; ete en yakın ölçüm)
VARSAYIM (denemede ölçülecek): d = 10 mm (8–15) · dökme 0,80 g/mL · doluluk ηF 0,60 · Janssen K 0,5
"""
import json, math, os, random
from kasar_akis_model_v2 import roberts, r_t, YASA, T_DOK, PIDE_R, KENAR

PORS, KG2 = 145.0, 5.8
RHO_KATI, RHO_DOKME = 1.06, 0.80
MU = 0.35; FI_S = math.degrees(math.atan(MU))
D_NOM, D_ARALIK = 10.0, (8.0, 10.0, 12.0, 15.0, 20.0)

# ---- seçilen geometri (kusbasi_cad_v1 ile AYNI sayılar) ----
G = dict(RT=36.0, C=2.0, R_MIL=8.0, R_KOK=14.0, T=4.0, P0=40.0, P1=50.48, L=304.0, W_IC=134.0,
         AGIZ=(48.0, 44.0), ESIK=6.0, TIKAC=12.0, ROTOR_BOSLUK=18.0, LAMA_DUVAR=2.4)
G["D"] = 2 * (G["RT"] - G["C"])


def kup(d): return d ** 3 / 1000.0 * RHO_KATI                       # g


def kurallar(d):
    """tane boyundan zorunlu ölçüler"""
    return dict(bogaz=4.0 * d, kanal_R175=1.75 * d, kanal_R25=2.5 * d, kanal_R45=4.5 * d, hatve_bosluk=3.0 * d, agiz=4.0 * d,
                aralik_kucuk=d / 3.0, aralik_buyuk=1.5 * d)


def degerlendir(d):
    k = kurallar(d); kanal = G["RT"] - G["R_MIL"]; kanal_kok = G["RT"] - G["R_KOK"]
    return dict(d=d, m_kup=kup(d), n_kup=PORS / kup(d),
                bogaz=(2 * G["RT"], k["bogaz"], 2 * G["RT"] >= k["bogaz"]),
                R_on=kanal / d, R_arka=kanal_kok / d,
                hatve=(G["P0"] - G["T"], k["hatve_bosluk"], G["P0"] - G["T"] >= k["hatve_bosluk"]),
                agiz=(min(G["AGIZ"]), k["agiz"], min(G["AGIZ"]) >= k["agiz"]),
                rotor=(G["ROTOR_BOSLUK"], k["aralik_buyuk"], G["ROTOR_BOSLUK"] >= k["aralik_buyuk"]),
                lama=(G["LAMA_DUVAR"], k["aralik_kucuk"], G["LAMA_DUVAR"] <= k["aralik_kucuk"]))


def kapasite(z_oran, fi=FI_S):
    """z_oran 0 = arka, 1 = ön · hatve doğrusal, mil konik kökten (ilk %20) düz mile"""
    p = G["P0"] + (G["P1"] - G["P0"]) * z_oran
    rm = G["R_KOK"] - (G["R_KOK"] - G["R_MIL"]) * min(1.0, z_oran / 0.1875)          # 57 mm / 304
    Vt, eta, Re, alfa = roberts(G["D"], 2 * rm, p, ts=G["T"], C=G["C"], fi_s=fi)
    return p, 2 * rm, Vt, eta, Vt * eta


def doz_belirsizligi(d, etaF=0.60):
    """Hacimsel dozda alt sınır: kesme düzlemindeki küpler 'içeride mi dışarıda mı' belirsiz.
    Kesit A'da düzleme basan küp sayısı n_k = A·φ/d² ; her biri [0,1] düzgün → varyans 1/12 ; iki kesme (başla + bitir)."""
    A = math.pi * (G["RT"] ** 2 - G["R_MIL"] ** 2) * etaF; fi_p = RHO_DOKME / RHO_KATI
    n_k = A * fi_p / d ** 2; sig = math.sqrt(2.0 * n_k / 12.0); N = PORS / kup(d)
    return n_k, sig, 100.0 * sig / N, 100.0 / N


def janssen(L=None, mu=MU, K=0.5):
    """tıkaç bölgesinde itme basıncı artışı · σ_it = σ_uç · exp(4 μ K L / D)"""
    L = G["TIKAC"] + G["ESIK"] if L is None else L
    return math.exp(4.0 * mu * K * L / (2 * G["RT"]))


# ---------------- TABLA YASASI: kuşbaşı için AYRI çözülür ----------------
# Kaşarın yasası (dışta 2,5 sn bekle + r² doğrusal) burada tutmuyor: kaşar eriyip ≈ 13 mm yayılır, küp yayılmaz → halkalar arası ±%25.
# Doğru soru: ağız merkezi her yarıçapta NE KADAR SÜRE kalmalı ki her halkaya cm² başına aynı gram düşsün?
# Ağız izi (48 × 44 + 4 mm sekme) her r_j istasyonu için halkalara bir pay dağıtır → A matrisi. A·w = sabit (negatif olmayan w) çözülür.
IST = [110.0 - 5.0 * j for j in range(21)]                          # ağız merkezi istasyonları: 110 → 10 mm
DR_H, NB_H = 10.0, int((PIDE_R - KENAR) / 10.0)                      # 10 mm'lik halkalar, r ≤ 125


def _cekirdek(n=6000, seed=4):
    R = random.Random(seed); ax, az = G["AGIZ"][0] / 2.0, G["AGIZ"][1] / 2.0; A = [[0.0] * len(IST) for _ in range(NB_H)]; tas = [0.0] * len(IST)
    for j, rj in enumerate(IST):
        for _ in range(n):
            x = rj + R.uniform(-ax, ax) + R.gauss(0, 4.0); z = R.uniform(-az, az) + R.gauss(0, 4.0); b = int(math.hypot(x, z) / DR_H)
            if b < NB_H: A[b][j] += 1.0 / n / (((b + 1) * DR_H) ** 2 - (b * DR_H) ** 2)
            else: tas[j] += 1.0 / n
    return A, tas


def yasa_coz(r_max=110.0, puruz=0.02):
    """scipy NNLS: min ‖√alan · (A w − 1)‖² + pürüz · ‖Δw‖²  ,  w ≥ 0 · ağız merkezi r_max'tan dışarı çıkmaz.
    Pürüz terimi komşu istasyonların süresini birbirine yaklaştırır (tabla sarsılmadan yürüsün)."""
    import numpy as np
    from scipy.optimize import nnls
    A, tas = _CEK; A = np.array(A); A = A / A.max(); m = len(IST); acik = [j_ for j_ in range(m) if IST[j_] <= r_max + 1e-9]
    alan = np.array([((b + 1) * DR_H) ** 2 - (b * DR_H) ** 2 for b in range(NB_H)], dtype=float); kok = np.sqrt(alan / alan.sum())
    M = A[:, acik] * kok[:, None]; y = kok.copy()
    Dm = np.zeros((len(acik) - 1, len(acik)))
    for k_ in range(len(acik) - 1): Dm[k_, k_], Dm[k_, k_ + 1] = -puruz, puruz
    w, _ = nnls(np.vstack([M, Dm]), np.concatenate([y, np.zeros(len(acik) - 1)]))
    W = [0.0] * m
    for k_, j_ in enumerate(acik): W[j_] = float(w[k_])
    top = sum(W); return [v / top for v in W]


def _kur(W):
    K = [0.0]
    for v in W: K.append(K[-1] + v)
    return K


_CEK = _cekirdek(); W_IST, _KUM, YASA_TARAMA = None, None, []
for _rm in (95.0, 100.0, 105.0, 110.0):
    W_IST = yasa_coz(_rm); _KUM = _kur(W_IST)
    YASA_TARAMA.append((_rm, W_IST))


def r_t_k(t):
    """kuşbaşı tabla yasası: istasyonlarda W_IST payı kadar oyalanarak DIŞTAN İÇE sürekli hareket"""
    u = min(1.0, max(0.0, t / T_DOK)); son = IST[-1]
    for j in range(len(IST)):
        if W_IST[j] <= 1e-9: continue
        son = IST[j] - 2.5
        if u <= _KUM[j + 1]: return IST[j] + 2.5 - 5.0 * (u - _KUM[j]) / W_IST[j]
    return son


def tabla_tur(t, n_tabla=35.0):
    """kuşbaşında tabla SABİT devirde döner (taneler serpiliyor, şerit yok)"""
    return n_tabla * t / 60.0


def halka_profili(rt, n=80000, seed=2):
    R = random.Random(seed); ax, az = G["AGIZ"][0] / 2.0, G["AGIZ"][1] / 2.0; m = [0] * (NB_H + 6)
    for k in range(n):
        r = rt(T_DOK * (k + R.random()) / n); x = r + R.uniform(-ax, ax) + R.gauss(0, 4.0); z = R.uniform(-az, az) + R.gauss(0, 4.0); b = int(math.hypot(x, z) / DR_H)
        if b < len(m): m[b] += 1
    alan = [((b + 1) * DR_H) ** 2 - (b * DR_H) ** 2 for b in range(NB_H)]; ort = sum(m[:NB_H]) / float(sum(alan)); yog = [m[b] / alan[b] / ort for b in range(NB_H)]
    cv = math.sqrt(sum(a * (y - 1.0) ** 2 for a, y in zip(alan, yog)) / sum(alan))
    return 100 * cv, 100.0 * sum(m[NB_H:]) / n, [int(round(100 * y)) for y in yog]


def _yasa_sec():
    """taşan ≤ %8 olanlardan halka sapması en küçük olanı seç; tablo S['yasa_tarama'] için saklanır"""
    global W_IST, _KUM
    sonuc = []
    for rm, W in YASA_TARAMA:
        W_IST, _KUM = W, _kur(W); cv, tas, pr = halka_profili(r_t_k, n=40000); sonuc.append((rm, cv, tas, pr, W))
    uygun = [x for x in sonuc if x[2] <= 8.0] or sonuc
    en = min(uygun, key=lambda x: x[1]); W_IST, _KUM = en[4], _kur(en[4])
    return sonuc, en[0]


YASA_SONUC, R_MAX = _yasa_sec()


def dagilim(d, n_tabla=35.0, seed=1, HC=25.0, obek=0, pencere=0.25):
    """sürekli akış (eşikten tek tek düşen küpler) → pide üstünde 25 mm'lik hücrelerde küp sayısı"""
    R = random.Random(seed); N = int(round(PORS / kup(d))); NG = int(2 * PIDE_R / HC) + 2; L = NG * HC / 2.0
    g = [0] * (NG * NG); w = 2 * math.pi * n_tabla / 60.0; ax, az = G["AGIZ"][0] / 2.0, G["AGIZ"][1] / 2.0
    for k in range(N):
        if obek: t = T_DOK * (R.randrange(obek) + pencere * R.random()) / obek       # ÖBEK: doz k parçada, her biri kısa sürede boşalır
        else: t = T_DOK * (k + R.random()) / N                         # SÜREKLİ: küpler zamana düzgün yayılı
        r = r_t_k(t); a = -w * t
        x = r + R.uniform(-ax, ax) + R.gauss(0, 4.0); z = R.uniform(-az, az) + R.gauss(0, 4.0)
        px, pz = x * math.cos(a) - z * math.sin(a), x * math.sin(a) + z * math.cos(a)
        i, j = int((px + L) / HC), int((pz + L) / HC)
        if 0 <= i < NG and 0 <= j < NG: g[i * NG + j] += 1
    ic = []
    for i in range(NG):
        for j in range(NG):
            dx, dz = (i + .5) * HC - L, (j + .5) * HC - L
            if math.hypot(dx, dz) <= PIDE_R - KENAR - HC * 0.7: ic.append(g[i * NG + j])
    ort = sum(ic) / float(len(ic)); cv = math.sqrt(sum((v - ort) ** 2 for v in ic) / len(ic)) / ort
    return N, ort, 100 * cv, 100 / math.sqrt(ort), 100.0 * sum(1 for v in ic if v == 0) / len(ic)


if __name__ == "__main__":
    S = {}
    print("=== 1 · URUN ===")
    print("porsiyon %.0f g · 2 gun %.1f kg · dokme %.2f g/mL → %.2f L · duvar surtunmesi mu %.2f (fi_s %.0f°)" % (PORS, KG2, RHO_DOKME, KG2 / RHO_DOKME, MU, FI_S))
    print("\n=== 2 · TANE BOYU HER SEYI BELIRLER (secilen geometri: tekne O%.0f · kanat O%.0f · mil O%.0f · kok O%.0f · hatve %.0f → %.1f) ===" % (2 * G["RT"], G["D"], 2 * G["R_MIL"], 2 * G["R_KOK"], G["P0"], G["P1"]))
    print("  d   kup g  adet/pide | bogaz>=4d   | R on / arka (CEMA 1,75·2,5·4,5) | hatve boslugu>=3d | agiz>=4d  | rotor-kanat>=1,5d | lama-duvar<=d/3")
    S["tane"] = []
    for d in D_ARALIK:
        e = degerlendir(d); tik = lambda t: "%4.0f/%-4.0f %s" % (t[0], t[1], "OK " if t[2] else "YOK")
        print("%4.0f  %5.2f   %5.0f    | %s | %4.2f / %4.2f %-18s | %s   | %s | %s  | %4.1f/%-4.1f %s" % (
            d, e["m_kup"], e["n_kup"], tik(e["bogaz"]), e["R_on"], e["R_arka"], "(sinif %s)" % ("2+" if e["R_on"] >= 2.5 else "1" if e["R_on"] >= 1.75 else "YETMEZ"),
            tik(e["hatve"]), tik(e["agiz"]), tik(e["rotor"]), e["lama"][0], e["lama"][1], "OK" if e["lama"][2] else "YOK"))
        S["tane"].append(dict(d=d, m=round(e["m_kup"], 2), n=round(e["n_kup"]), bogaz=e["bogaz"][2], R_on=round(e["R_on"], 2), R_arka=round(e["R_arka"], 2),
                              hatve=e["hatve"][2], agiz=e["agiz"][2], rotor=e["rotor"][2], lama=e["lama"][2]))
    print("\n=== 3 · HELEZON KAPASITESI · Roberts (arka → on) ===")
    S["kapasite"] = []
    for zo in (0.0, 0.1, 0.1875, 0.4, 0.7, 1.0):
        p, dm, Vt, eta, q = kapasite(zo); print("  z %%%3.0f  hatve %4.1f  mil O%4.1f  Vt %5.1f mL/tur  verim %.2f  → %5.1f mL/tur" % (100 * zo, p, dm, Vt, eta, q))
        S["kapasite"].append(dict(z=round(100 * zo), p=round(p, 1), mil=round(dm, 1), Vt=round(Vt, 1), eta=round(eta, 2), q=round(q, 1)))
    q_on = kapasite(1.0)[4]
    print("  surtunme duyarliligi (on uc): " + " · ".join("fi %d° → %.1f" % (f, kapasite(1.0, f)[4]) for f in (15, 19, 25, 30, 40)))
    S["duyarlilik"] = [dict(fi=f, q=round(kapasite(1.0, f)[4], 1)) for f in (15, 19, 25, 30, 40)]
    print("\n=== 4 · DOZ ===")
    S["doz"] = []
    for etaF in (0.45, 0.60, 0.75):
        g_tur = q_on * etaF * RHO_DOKME; tur = PORS / g_tur; rpm = tur * 60.0 / T_DOK
        print("  doluluk %.2f → %5.1f g/tur · %.0f g = %.2f tur · 10 sn'de %4.1f dev/dk · kanat ucu %.3f m/s · ±%%5 doz = ±%.0f° mil acisi" % (etaF, g_tur, PORS, tur, rpm, math.pi * G["D"] / 1000 * rpm / 60, 0.05 * tur * 360))
        S["doz"].append(dict(etaF=etaF, g_tur=round(g_tur, 1), tur=round(tur, 2), rpm=round(rpm, 1), uc=round(math.pi * G["D"] / 1000 * rpm / 60, 3), aci=round(0.05 * tur * 360)))
    print("  AKIS SUREKLI: kanat agizdan %.0f mm once biter, yatak TIKAC olarak esigin (%.0f mm) ustunden itilir → kupler tek tek duser, tur basina obek YOK" % (G["TIKAC"] + G["ESIK"], G["ESIK"]))
    print("  tikacta itme basinci artisi (Janssen, L %.0f): x%.2f → sikisma/ezilme riski dusuk" % (G["TIKAC"] + G["ESIK"], janssen()))
    S["janssen"] = round(janssen(), 2)
    print("\n=== 5 · HACIMSEL DOZUN ALT SINIRI (kesme duzlemi belirsizligi) ===")
    S["belirsizlik"] = []
    for d in D_ARALIK:
        nk, sig, yuzde, bir = doz_belirsizligi(d); print("  d %4.0f · duzlemde %4.1f kup · sigma %.2f kup = ±%%%.1f · (1 kup = %%%.1f)" % (d, nk, sig, yuzde, bir))
        S["belirsizlik"].append(dict(d=d, nk=round(nk, 1), sig=round(sig, 2), yuzde=round(yuzde, 1), bir=round(bir, 1)))
    print("\n=== 6 · PIDE USTUNDE DAGILIM (tabla 35 dev/dk, distan ice, surekli akis · 25 mm hucre) ===")
    S["dagilim"] = []
    for d in D_ARALIK:
        r = [dagilim(d, seed=s) for s in range(1, 9)]; N = r[0][0]; ort = sum(x[1] for x in r) / 8; cv = sum(x[2] for x in r) / 8; po = sum(x[3] for x in r) / 8; bos = sum(x[4] for x in r) / 8
        print("  d %4.0f · %3d kup · hucre basina %4.1f · sapma %%%4.0f (rastgele serpmenin siniri %%%3.0f) · bos hucre %%%4.1f" % (d, N, ort, cv, po, bos))
        S["dagilim"].append(dict(d=d, N=N, ort=round(ort, 1), cv=round(cv), poisson=round(po), bos=round(bos, 1)))
    print("\n=== 6b · TABLA YASASI + 'PAT DIYE DOKERSE' ===")
    e_cv, e_tas, e_pr = halka_profili(r_t); y_cv, y_tas, y_pr = halka_profili(r_t_k)
    print("  kasardan alinan yasa : halka sapmasi %%%.0f · kenara tasan %%%.1f · profil %s" % (e_cv, e_tas, e_pr))
    print("  KUSBASI ICIN COZULEN : halka sapmasi %%%.0f · kenara tasan %%%.1f · profil %s" % (y_cv, y_tas, y_pr))
    for rm, cv, tas, pr, W in YASA_SONUC: print("     agiz merkezi en dista r%3.0f → halka sapmasi %%%2.0f · tasan %%%4.1f%s" % (rm, cv, tas, "   ← SECILEN" if rm == R_MAX else ""))
    S["yasa_tarama"] = [dict(r_max=rm, cv=int(round(cv)), tas=round(tas, 1), secilen=(rm == R_MAX)) for rm, cv, tas, pr, W in YASA_SONUC]
    print("  istasyonlarda oyalanma (sn): " + " · ".join("r%d %.2f" % (IST[j], W_IST[j] * T_DOK) for j in range(len(IST)) if W_IST[j] * T_DOK >= 0.05))
    S["yasa"] = dict(eski=dict(cv=int(round(e_cv)), tas=round(e_tas, 1), profil=e_pr), yeni=dict(cv=int(round(y_cv)), tas=round(y_tas, 1), profil=y_pr),
                     ist=[dict(r=IST[j], sn=round(W_IST[j] * T_DOK, 2)) for j in range(len(IST))])
    S["obek"] = []
    for ad, ob in (("sürekli (eşik + tıkaç çalışıyor)", 0), ("4 öbek", 4), ("2 öbek (tur başına bir boşalma)", 2), ("tek seferde", 1)):
        v = [dagilim(D_NOM, seed=s_, obek=ob)[4] for s_ in range(1, 41)]; print("  %-34s bos hucre %%%4.1f" % (ad, sum(v) / len(v))); S["obek"].append(dict(ad=ad, bos=round(sum(v) / len(v), 1)))
    print("\n=== 7 · TORK (kaba) ===")
    A_k = math.pi * (G["RT"] ** 2 - G["R_MIL"] ** 2) / 100.0; m_yatak = A_k * G["L"] / 10.0 * RHO_DOKME / 1000.0
    F_bas = RHO_DOKME * 1000 * 9.81 * 0.17 * (2 * G["RT"] / 1000.0) * (G["L"] / 1000.0); F = MU * (m_yatak * 9.81 + F_bas)
    Re = (2.0 / 3.0) * ((G["D"] / 2) ** 3 - G["R_MIL"] ** 3) / ((G["D"] / 2) ** 2 - G["R_MIL"] ** 2) / 1000.0
    alfa = math.atan(G["P1"] / (2 * math.pi * Re * 1000)); T = F * Re * math.tan(alfa + math.radians(FI_S))
    print("  yatak %.2f kg · hazne basinci kuvveti %.0f N · surtunme %.1f N · calisma torku ≈ %.2f N·m (NMRV030 i=30: 24 N·m) → sinir SIKISMADA: akim siniri ≈ 3 N·m oner" % (m_yatak, F_bas, F, T))
    S["tork"] = dict(yatak=round(m_yatak, 2), F=round(F, 1), T=round(T, 2))
    S["giris"] = dict(PORS=PORS, KG2=KG2, RHO=RHO_DOKME, MU=MU, FI=round(FI_S), G=G, q_on=round(q_on, 1))
    cik = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "otonom", "kaset3d", "kusbasi_model.json")
    json.dump(S, open(cik, "w", encoding="utf-8"), ensure_ascii=False, indent=1); print("\n→", cik)
