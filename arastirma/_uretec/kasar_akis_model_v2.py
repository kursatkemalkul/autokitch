# -*- coding: utf-8 -*-
"""AUTOKITCH · KAŞAR AKIŞ MODELİ v2 (20 Eyl 2026) — KAP v5: UÇTAN ÇIKIŞ (Picnic / Atosa gibi), kap 280 × 325 × 360
Kemal kararları: çıkış uçtan · kap 325 derin · peynir KISA KESİM pidelik rende · porsiyon 55 g · dağıtıcı YOK, terazi YOK ·
kaşar şelale gibi sürekli akar, tabla pidenin DIŞINDAN başlar, dönerek İÇERİ ilerler, ortada biter.

KAYNAKLI: yoğunluk 0,48 rende / 0,56 küp (USDA) · katı 1,10 · Roberts helezon verimi · NMRV030 ve 5840-31ZY katalog ölçüleri ·
          pafta HAT_ATOSA_TABLALI v2 kotları (kaset tabanı 1627, tabla dozajda 1440, modül z +40…−790, iç arka sınır −740, tabla ekseni −270)
VARSAYIM (ölçülecek): parça 4 × 4 × 10 mm · dökme yoğunluk 0,50 · fi_s 30° · kanat doluluğu 0,60 · sekme saçılması 5 mm · erime yayılması 12 mm
"""
import math, random

# ---------------- ÜRÜN ----------------
PORS, GUN_KG = 55.0, 4.4                       # g/pide · kg/gün (80 pide) → 2 gün 8,8 kg
RHO, RHO_KATI = 0.50, 1.10                     # g/mL
PARCA = (4.0, 4.0, 10.0)                       # mm · VARSAYIM (fotoğraftan)
M_PARCA = PARCA[0] * PARCA[1] * PARCA[2] / 1000.0 * RHO_KATI       # g

# ---------------- KAP v5 (iç ölçüler mm) ----------------
K = dict(W=280.0, D=325.0, H=360.0, et=3.0, tp=5.0, hw=134.0, rt=22.0, cy=40.0, yc=195.0, Rs=129.0, y_dolum=332.0)
K["boy"] = K["D"] - 2 * K["tp"]; K["yj"] = K["yc"] - math.sqrt(K["hw"] ** 2 - K["rt"] ** 2)
HELEZON = dict(D=40.0, mil=14.0, ts=3.0, C=2.0)
KANAT = [(-155.0, -45.0, 22.0), (-45.0, 59.0, 26.0), (59.0, 162.5, 30.0)]      # z_bas, z_son, hatve (tek ağızlı, SAĞ el)
UC = dict(z0=162.5, z1=194.5, hatve=36.0, agiz=2)                               # tüp içi kapalı bölüm: çift ağızlı
AGIZ = dict(z0=194.5, z1=230.5, x=19.0)                                         # alt ağız 36 × 38, merkez = ön plaka + 50


def mil_cap(z): return 14.0 if z >= -97.5 else 14.0 + 12.0 * (-97.5 - z) / 60.0   # arka 60 mm konik Ø26 → Ø14


def roberts(D, Dc, p, ts=3.0, C=2.0, fi_s=30.0, agiz=1):
    Ro, Ri = D / 2.0, Dc / 2.0
    Vt = math.pi / 4.0 * ((D + 2 * C) ** 2 - Dc ** 2) * (p - agiz * ts) / 1000.0
    Re = (2.0 / 3.0) * (Ro ** 3 - Ri ** 3) / (Ro ** 2 - Ri ** 2)
    a = math.atan(p / (2 * math.pi * Re))
    return Vt, 1.0 / (1.0 + math.tan(a) * math.tan(math.radians(fi_s) + a)), Re, math.degrees(a)


def yari(y, g=K):
    if y < g["cy"] - g["rt"]: return 0.0
    if y < g["cy"]: return math.sqrt(max(0.0, g["rt"] ** 2 - (y - g["cy"]) ** 2))
    if y < g["yj"]: return g["rt"]
    if y < g["yc"]: return math.sqrt(max(0.0, g["hw"] ** 2 - (y - g["yc"]) ** 2))
    return g["hw"]


def hacim(y_son, g=K):
    a, dy, y = 0.0, 0.25, g["cy"] - g["rt"]
    while y < y_son: a += 2 * yari(y + dy / 2) * dy; y += dy
    return a * g["boy"] / 1e6


def dolum_kotu(litre):
    y = K["cy"] - K["rt"]
    while hacim(y) < litre and y < K["y_dolum"]: y += 1.0
    return y


# ---------------- TABLA + DÜŞME ----------------
KOT = dict(kaset_taban=1627.0, tabla_dozaj=1440.0, hamur=8.0)
PIDE_R, KENAR = 140.0, 15.0                        # pide Ø280 · kaşarsız kenar 15 → kaşarlı bölge R125
ETEK_R, ETEK_T = 40.0, 50.0                        # etek alt ağzı: 40 (yarıçap yönü, x) × 50 (teğet yön, z)
T_DOK = 10.0
SIG = math.sqrt(5.0 ** 2 + 12.0 ** 2)              # sekme 5 ⊕ erime 12 mm (VARSAYIM)
YASA = dict(r_dis=105.0, r_ic=20.0, t_dis=2.5, t_ic=0.3)      # yasa_ara() 162 seçenek taradı: halka profili sapması %39 → %13


def r_t(t, Y=None):
    """tabla kayması: önce dış kenarda t_dis bekle → r² zamanla doğrusal azalarak içeri → ortada t_ic bekle"""
    Y = Y or YASA
    if t <= Y["t_dis"]: return Y["r_dis"]
    if t >= T_DOK - Y["t_ic"]: return Y["r_ic"]
    tm = T_DOK - Y["t_dis"] - Y["t_ic"]
    return math.sqrt(Y["r_dis"] ** 2 - (Y["r_dis"] ** 2 - Y["r_ic"] ** 2) * (t - Y["t_dis"]) / tm)


def radyal_profil(Y, n=4000, seed=5):
    """pide dönerken ortalama gram/cm² profili (5 mm'lik halkalar) — akış sabit kabul"""
    R = random.Random(seed); dr = 5.0; nb = 30; m = [0.0] * nb
    for k in range(n):
        r = r_t(T_DOK * (k + .5) / n, Y)
        for _ in range(6):
            x = r + R.uniform(-ETEK_R / 2, ETEK_R / 2) + R.gauss(0, SIG); z = R.uniform(-ETEK_T / 2, ETEK_T / 2) + R.gauss(0, SIG)
            b = int(math.hypot(x, z) / dr)
            if b < nb: m[b] += 1.0
    top = sum(m); yog = [m[b] / ((b + 1) ** 2 - b ** 2) for b in range(nb)]
    ic = list(range(0, int((PIDE_R - KENAR - 10) / dr))); alan = [(b + 1) ** 2 - b ** 2 for b in ic]
    ort = sum(yog[b] * a for b, a in zip(ic, alan)) / sum(alan)
    cv = math.sqrt(sum(a * (yog[b] - ort) ** 2 for b, a in zip(ic, alan)) / sum(alan)) / ort
    return cv, sum(m[int((PIDE_R - KENAR) / dr):]) / top, [y / ort for y in yog]


def yasa_ara():
    en = None
    for rd in (100.0, 105.0, 110.0):
        for ri in (0.0, 10.0, 20.0):
            for td in (0.0, 0.5, 1.0, 1.5, 2.0, 2.5):
                for ti in (0.0, 0.3, 0.6):
                    Y = dict(r_dis=rd, r_ic=ri, t_dis=td, t_ic=ti); cv, tasan, _ = radyal_profil(Y, n=600)
                    puan = cv + 2.0 * max(0.0, tasan - 0.04)
                    if en is None or puan < en[0]: en = (puan, Y, cv, tasan)
    return en


def dagilim(n_tabla, n_helezon, agiz=2, doluluk=0.5, seed=1, NG=58, HC=5.0, Y=None):
    """pide üstüne düşen parçaların haritası → (sapma, boş alan oranı, ortalama)"""
    R = random.Random(seed); g = [0.0] * (NG * NG); L = NG * HC / 2.0
    fp = agiz * n_helezon / 60.0; w = 2 * math.pi * n_tabla / 60.0
    n_parca = int(round(PORS / M_PARCA)); t_dus = 0.20; n = int(math.ceil(3 * 12.0 / HC))
    for _ in range(n_parca):
        while True:                                   # bırakılma anı: yalnız kanat yığınının ağza geldiği pencerede
            t = R.random() * T_DOK
            if (fp * t) % 1.0 < doluluk: break
        tl = t + t_dus + R.uniform(-0.015, 0.015); r = r_t(min(T_DOK, tl), Y); a = -w * tl
        x = r + R.uniform(-ETEK_R / 2, ETEK_R / 2) + R.gauss(0, 5.0); z = R.uniform(-ETEK_T / 2, ETEK_T / 2) + R.gauss(0, 5.0)
        px, pz = x * math.cos(a) - z * math.sin(a), x * math.sin(a) + z * math.cos(a)
        i0, j0 = int((px + L) / HC), int((pz + L) / HC); hu = []; top = 0.0
        for i in range(i0 - n, i0 + n + 1):
            for j in range(j0 - n, j0 + n + 1):
                if 0 <= i < NG and 0 <= j < NG:
                    dx, dz = (i + .5) * HC - L - px, (j + .5) * HC - L - pz; wg = math.exp(-(dx * dx + dz * dz) / 288.0); hu.append((i * NG + j, wg)); top += wg
        for k, wg in hu: g[k] += M_PARCA * wg / top
    ic = []
    for i in range(NG):
        for j in range(NG):
            dx, dz = (i + .5) * HC - L, (j + .5) * HC - L
            if dx * dx + dz * dz <= (PIDE_R - KENAR - 10) ** 2: ic.append(g[i * NG + j])
    ort = sum(ic) / len(ic); cv = math.sqrt(sum((v - ort) ** 2 for v in ic) / len(ic)) / ort
    return cv, sum(1 for v in ic if v < 0.5 * ort) / float(len(ic)), ort



if __name__ == "__main__":
    print("=== 1 · ÜRÜN ===")
    print("porsiyon %.0f g · 2 gunluk %.1f kg · parca %g x %g x %g mm = %.3f g (VARSAYIM) · pide basina ~%d parca" % (PORS, 2 * GUN_KG, PARCA[0], PARCA[1], PARCA[2], M_PARCA, round(PORS / M_PARCA)))
    print("\n=== 2 · KAP 280 x 325 x 360 ===")
    V = hacim(K["y_dolum"]) - 0.12
    print("kesit: helezon ekseni y %g · bogaz-kase birlesimi y %.1f · kase R%g merkez y %g · karistirici R%g (alt %g / ust %g) · helezon ustu y %g" % (K["cy"], K["yj"], K["hw"], K["yc"], K["Rs"], K["yc"] - K["Rs"], K["yc"] + K["Rs"], K["cy"] + 20))
    print("kullanilabilir hacim %.1f L (dolum cizgisi ust kenardan 20 asagi; helezon+karistirici 0,12 L dusuldu)" % V)
    for rho in (0.45, 0.48, 0.50, 0.55):
        print("   yogunluk %.2f → 8,8 kg = %.1f L = %%%.0f dolu (dolum kotu y %.0f)" % (rho, 8.8 / rho, 100 * 8.8 / rho / V, dolum_kotu(8.8 / rho)))
    print("\n=== 3 · HELEZON O40 / mil O14 · SAG el · onden bakinca SAAT YONUNDE ===")
    onceki = 0.0
    for z0, z1, p in KANAT:
        dm = mil_cap((z0 + z1) / 2); Vt, eta, Re, a = roberts(40.0, dm, p)
        print("   z %6.1f → %6.1f · hatve %2.0f · mil O%.0f · aralik %2.0f mm (parca boyunun %.1f kati) · Vt %.1f mL · verim %.2f · kapasite %.1f mL/tur  (+%.1f)" % (z0, z1, p, dm, p - 3, (p - 3) / PARCA[2], Vt, eta, Vt * eta, Vt * eta - onceki)); onceki = Vt * eta
    Vt, eta, Re, a = roberts(40.0, 14.0, 30.0); Q = Vt * eta
    Vu, etau, _, _ = roberts(40.0, 14.0, UC["hatve"], agiz=2); Qu = Vu * etau
    print("   TUP (kapali 32 mm, CIFT agizli, hatve 36): aralik %.0f mm · kapasite %.1f mL/tur → besleme kapasitesinin %.2f kati (sikisma yok)" % (UC["hatve"] / 2 - 3, Qu, Qu / Q))
    print("   mil-tekne arasi %.0f mm = parca kalinliginin %.1f kati (CEMA esigi 1,75-4,5)" % (22 - 7, (22 - 7) / PARCA[0]))
    for ef in (0.45, 0.60, 0.75):
        gt = Q * ef * RHO; print("   doluluk %.2f → %.1f g/tur · %.1f tur/pide · %.0f dev/dk (10 sn) · tupteki doluluk %.2f · cikis darbesi %.2f Hz" % (ef, gt, PORS / gt, PORS / gt / T_DOK * 60, Q * ef / Qu, 2 * PORS / gt / T_DOK))
    EF = 0.60; GT = Q * EF * RHO; N_H = PORS / GT / T_DOK * 60; DOL_UC = Q * EF / Qu
    print("\n=== 4 · TORK (kaba hesap, x3 emniyetle sec) ===")
    sig = RHO * 1000 * 9.81 * 0.26; F = sig * 0.044 * 0.305; Th = F * Re / 1000.0 * math.tan(math.radians(a + 30.0))
    print("   helezon: dusey basinc %.0f Pa x giris alani 44x305 = %.0f N → tork ~ %.2f N·m calisirken · kalkista x2,5 = %.2f N·m" % (sig, F, Th, 2.5 * Th))
    Fc = 4 * sig * (0.006 * 0.296); Tk = Fc * (2 * 0.129 + 0.086 + 0.043)
    print("   karistirici: cubuk basina ~%.1f N (pasif basinc ~4x) → ~%.1f N·m · 48 saat keklesmis x3 = %.1f N·m" % (Fc, Tk, 3 * Tk))
    print("   KATALOG: 5840-31ZY 24V i=100: 60 dev/dk'da 1,57 N·m (bloke 2,45) · i=505: 12 dev/dk'da 6,9 N·m  |  NMRV030: i=30 24 N·m, i=80 14 N·m (1400 dev/dk giris)")
    print("\n=== 5 · DERINLIK BUTCESI (modul z +40 … -790, ic arka sinir -740, tabla ekseni -270) ===")
    on = -270.0 - 50.0; arka = on - K["D"]
    print("   agiz merkezi z -270 · on plaka z %.0f · arka plaka z %.0f · arkada kalan %.0f mm" % (on, arka, arka + 740))
    print("   NMRV030: kaplin 20 + bosluk 6 + reduktor 63 = 89 mm ≤ %.0f  ✓   |   5840-31ZY: 20 + 6 + 36 = 62 mm ✓   |   duz (eksenel) motor ~175 mm ✗" % (arka + 740))
    print("   motor govdesi yana uzanir: NMRV030 giris flansi eksenden 55 + NEMA23 76 = 131 mm < kabin yari genisligi 140 ✓ (kendi govdesi icinde)")
    print("\n=== 6 · DUSME ===")
    y_agiz = KOT["kaset_taban"] + K["cy"] - K["rt"]; y_pide = KOT["tabla_dozaj"] + KOT["hamur"]; h = (y_agiz - y_pide) / 1000.0
    t = math.sqrt(2 * h / 9.81); v = math.sqrt(2 * 9.81 * h)
    vt = math.sqrt(2 * (M_PARCA / 1000.0) * 9.81 / (1.2 * 1.0 * PARCA[0] * PARCA[2] * 1e-6))
    print("   agiz alti kot %.0f · pide ustu kot %.0f · dusme %.0f mm · sure %.2f sn · carpma hizi %.2f m/s · hava direnci agirligin %%%.0f'i (ihmal)" % (y_agiz, y_pide, h * 1000, t, v, 100 * (v / vt) ** 2))
    print("   etek: ust ic 42x52 → alt ic 40x50, boy %.0f mm, alt ucu pidenin 25 mm ustunde" % (y_agiz - 10 - y_pide - 25))
    print("\n=== 7 · TABLA ===")
    print("   pide O%.0f · kasarli bolge R%.0f · etek izi %.0f (yaricap yonu) x %.0f (teget) · sekme+erime yayilmasi %.0f mm (VARSAYIM)" % (2 * PIDE_R, PIDE_R - KENAR, ETEK_R, ETEK_T, SIG))
    puan, Yb, cvb, tb = yasa_ara()
    print("   EN IYI HAREKET YASASI (162 secenek tarandi): dis r %.0f · ic r %.0f · dista bekleme %.1f sn · icte bekleme %.1f sn → halka profili sapmasi %%%.1f · kenara tasan %%%.1f" % (Yb["r_dis"], Yb["r_ic"], Yb["t_dis"], Yb["t_ic"], 100 * cvb, 100 * tb))
    D0 = dict(r_dis=100.0, r_ic=12.0, t_dis=0.0, t_ic=0.0); cv0, t0, _ = radyal_profil(D0, n=600)
    print("   karsilastirma · beklemesiz duz spiral (r 100 → 12): halka profili sapmasi %%%.1f" % (100 * cv0))
    YASA.update(Yb); cvs, ts, prof = radyal_profil(YASA)
    print("   halka profili (ortalamaya oran, 5 mm'lik halkalar 0→150): " + " ".join("%.2f" % v for v in prof))
    tm = T_DOK - YASA["t_dis"] - YASA["t_ic"]; k2 = (YASA["r_dis"] ** 2 - YASA["r_ic"] ** 2) / tm
    print("   kayma hizi: basta %.1f mm/s · r 50'de %.1f · sonda %.1f mm/s" % (k2 / (2 * YASA["r_dis"]), k2 / 100.0, k2 / (2 * max(YASA["r_ic"], 10.0))))
    for n in (30, 34, 40, 45, 60):
        wq = 2 * math.pi * n / 60; print("   %2d dev/dk: %.1f tur · kenarda cizgisel hiz %.2f m/s · merkezkac %.2f g · tegetsel kayma ~%.0f mm" % (n, n * T_DOK / 60, wq * YASA["r_dis"] / 1000, wq * wq * (PIDE_R - KENAR) / 1000 / 9.81, (wq * YASA["r_dis"] / 1000) ** 2 / (2 * 0.5 * 9.81) * 1000))
    print("\n=== 8 · DAGILIM (helezon %.0f dev/dk · cift agiz → %.2f Hz · tupte doluluk %.2f) — 3 kosu ort. ===" % (N_H, 2 * N_H / 60, DOL_UC))
    print("   tabla dev/dk : bos alan %  / sapma %")
    for n in range(24, 47, 2):
        c = [dagilim(n, N_H, 2, DOL_UC, sd) for sd in (1, 2, 3)]
        print("   %2d : %4.1f / %4.1f   (darbe/tabla orani %.2f)" % (n, 100 * sum(q[1] for q in c) / 3, 100 * sum(q[0] for q in c) / 3, 2 * N_H / n))
    for ad, kw in (("TEK agizli uc", dict(agiz=1, doluluk=EF)), ("kusursuz surekli akis (alt sinir)", dict(agiz=2, doluluk=1.0)), ("beklemesiz duz spiral", dict(agiz=2, doluluk=DOL_UC, Y=D0))):
        c = [dagilim(34, N_H, seed=sd, **kw) for sd in (1, 2, 3)]
        print("   karsilastirma · %s, tabla 34: bos %.1f / sapma %.1f" % (ad, 100 * sum(q[1] for q in c) / 3, 100 * sum(q[0] for q in c) / 3))
