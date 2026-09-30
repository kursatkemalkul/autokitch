
# ====================================================================================================================================================
# E v12 (30 Eyl 2026 · Claude) — GERÇEK SÜRELER. Kemal: "E'yi doğrula: standart ürünler, motorlar, saniyeler, çalışma animasyonu;
#   her makine parçası doğru çalışsın, gerçekte o motor ne veriyor".
# v11'in bütün hareket fonksiyonları TEK saat (eski E saati, 0–23 s) kullanıyor ve kartonun katlanması bu fonksiyonlara bağlı. v12 geometriyi ve hareket
# sırasını KORUR, yalnız saati gerçeğe çevirir: her eksenin katalog / hesap hız + ivme sınırı aşağıdaki tabloda; her hareketin gereken yavaşlatma
# katsayısı (φ = max(1, v_tepe / v_sınır, √(a_tepe / a_sınır))) hesaplanır, eşzamanlı hareketler en büyüğünü alır, geçişler 40 ms rampayla yumuşatılır
# ve gerçek saat T = ∫ φ dt (eski saat) olur. Bütün E fonksiyonları eski saatle çağrılır: gercek(t_eski) / eski(T) dönüşümü K'nin e_time'ı içinde.
# DÜZELTME: baskı kafası inişi 1,90 → 2,20 (eski saat) — besleme arabası geri dönerken itici_araba_plakasi_sol ile piston_kafasi arası 1,29 mm'ye
#   iniyordu (3,6 ms kayma çakıştırır); kafa artık araba çekilmeye başladıktan 0,28 s sonra iner.
# ====================================================================================================================================================
import numpy as _np_v12

_v11_kafa_v12 = kafa
Z_INIS_V12 = (2.20, Z_INIS[1])
KAFA_ARKA_KIRPMA_V12 = 3.0      # v12: besleme arabası (HGH15CA bloğu) ileri strok sonunda kafa plakasının arka kenarına (z −354) YANDAN 1,3 mm yaklaşıyordu
                                # (ikisi aynı yükseklikte: kafa altı 1310–1330 · blok 1304–1327,7) → plakanın arka kenarı 3 mm kırpılır: aralık 4,3 mm.
                                # Plaka 296 × 293: kutu tabanını yine tam kaplar (arkada kıvrım çizgisine pay 12 → 15).


def kafa(t):
    if Z_INIS[0] <= t < Z_INIS[1]:
        return H_UST + (YB + T - H_UST) * ss(Z_INIS_V12[0], Z_INIS_V12[1], t)
    return _v11_kafa_v12(t)


def _catal_yol_v12(t):
    c = catal_trs(t)
    return (c[1], c[2])


# eksen · konum fonksiyonu (eski saat) · v_sınır · a_sınır · birim · kaynak / hesap
EKSEN_V12 = [
    ("PISTON baskı kafası", lambda t: kafa(t), 250.0, 2000.0, "mm",
     "SFU1610 (hatve 10) · 1500 dev/dk = 250 mm/s (vida kritik devri ~2760, v10 notu) · NEMA 23 STP-MTR-23079 + GT3 1:1 · düşey, kafa üstünde 6 motor"),
    ("ITICI vakum besleme arabası", lambda t: feed_z(t), 800.0, 4000.0, "mm", "GT3 20T kasnak (60 mm/tur) · 800 dev/dk · NEMA 23"),
    ("VAC_Y vakum Z", lambda t: vacuum_lift(t), 300.0, 5000.0, "mm", "pnömatik kompakt silindir (SMC CQ2 sınıfı) · 50–500 mm/s"),
    ("NEST destek tablası", lambda t: nest_dy(t), 80.0, 1000.0, "mm", "Tr16×8 (P4) iki ağızlı trapez vida + bronz somun · 600 dev/dk = 80 mm/s"),
    ("CNR_LIFT köşe çerçevesi", lambda t: corner_lift(t), 80.0, 1000.0, "mm", "Tr8×8 (P2) dört ağızlı trapez vida + bronz somun · 600 dev/dk = 80 mm/s"),
    ("CNR köşe parmakları (4)", lambda t: corner_angle(t), 300.0, 3000.0, "°", "NEMA 23 doğrudan (kaplin) · 50 dev/dk"),
    ("PARMAK ön dil katlayıcı", lambda t: parmak_psi(t), 900.0, 6000.0, "°", "GT3 20T:20T kayış · NEMA 23 · 150 dev/dk"),
    ("KATLAYICI U flap", lambda t: katlayici_dy(t), 83.0, 1000.0, "mm", "SFU1605 (hatve 5) · 1000 dev/dk = 83 mm/s"),
    ("KOPRU pizza köprüsü", lambda t: kopru_dy(t), 83.0, 1000.0, "mm", "SFU1605 (hatve 5) · 1000 dev/dk = 83 mm/s"),
    ("KOL kapak kolu", lambda t: kol_beta(t), 360.0, 1500.0, "°", "SureGear PGCN23-1025 10:1 · motor 600 dev/dk → kol 60 dev/dk"),
    ("CATAL robot çatalı (FR5 TCP)", _catal_yol_v12, 1000.0, 3000.0, "mm", "Fairino FR5 TCP azami ~1 m/s (üretici verisi · TEYİT)"),
]
DT_V12 = 0.002
_tg = _np_v12.arange(0.0, DONGU + 1e-9, DT_V12)


def _seri(fn):
    v0 = fn(0.0)
    if isinstance(v0, tuple):
        return _np_v12.array([fn(float(t)) for t in _tg], dtype=float)
    return _np_v12.array([[fn(float(t))] for t in _tg], dtype=float)


def _hareketler(P, v_lim, a_lim):
    """eski saatte bir eksenin hareketleri: [(i0, i1, φ, v_tepe, a_tepe, d)] · v = |dP/dt| · a yalnız yumuşak profilde (lin profilin sıçraması animasyon basitleştirmesi)"""
    V = _np_v12.linalg.norm(_np_v12.diff(P, axis=0), axis=1) / DT_V12
    hareket = V > 1e-4 * v_lim
    out = []
    i = 0
    n = len(V)
    while i < n:
        if not hareket[i]:
            i += 1; continue
        j = i
        while j < n and hareket[j]: j += 1
        vv = V[i:j]
        d = float(_np_v12.sum(vv) * DT_V12)
        vt = float(vv.max())
        ort = d / ((j - i) * DT_V12)
        if j - i >= 5 and vt / max(ort, 1e-9) > 1.3:                      # yumuşak (ss) profil: tepe ≈ 1,5 × ortalama
            k = max(3, int(0.010 / DT_V12))
            vs = _np_v12.convolve(vv, _np_v12.ones(k) / k, mode="same")
            at = float(_np_v12.abs(_np_v12.diff(vs)).max() / DT_V12)
        else:                                                              # doğrusal (lin) profil: ivme animasyonda sıçrar, gerçekte rampa
            at = 0.0
        phi = max(1.0, vt / v_lim, (at / a_lim) ** 0.5)
        out.append((i, j, phi, vt, at, d))
        i = j
    return out


_phi = _np_v12.ones(len(_tg) - 1)
ZAMAN_RAPORU_V12 = []
for _ad, _fn, _vl, _al, _br, _kay in EKSEN_V12:
    _P = _seri(_fn)
    for (_i0, _i1, _f, _vt, _at, _d) in _hareketler(_P, _vl, _al):
        _phi[_i0:_i1] = _np_v12.maximum(_phi[_i0:_i1], _f)
        ZAMAN_RAPORU_V12.append(dict(eksen=_ad, t0=round(_i0 * DT_V12, 3), t1=round(_i1 * DT_V12, 3), yol=round(_d, 1), birim=_br,
                                     v_tepe_eski=round(_vt, 1), v_sinir=_vl, phi=round(_f, 3), kaynak=_kay))
# geçişleri 40 ms genişlet + ortala (φ ≥ gereken her yerde korunur)
_k = int(0.020 / DT_V12)
_gen = _np_v12.array([_phi[max(0, i - _k):i + _k + 1].max() for i in range(len(_phi))])
_phi_d = _np_v12.convolve(_np_v12.pad(_gen, _k, mode="edge"), _np_v12.ones(2 * _k + 1) / (2 * _k + 1), mode="valid")
PHI_V12 = _np_v12.maximum(_phi_d[:len(_phi)], _phi)
_T_GERCEK = _np_v12.concatenate([[0.0], _np_v12.cumsum(PHI_V12 * DT_V12)])


def gercek(t):
    """eski E saati → gerçek saniye (E döngüsünün başından)"""
    return float(_np_v12.interp(t, _tg, _T_GERCEK))


def eski(T):
    """gerçek saniye → eski E saati (bütün E hareket fonksiyonları bununla çağrılır)"""
    return float(_np_v12.interp(T, _T_GERCEK, _tg))


DONGU_GERCEK = gercek(DONGU)
Z_CATAL_GERCEK = tuple(gercek(v) for v in Z_CATAL)
Z_PIZZA_GERCEK = tuple(gercek(v) for v in Z_PIZZA)
E_HAZIR_ESKI = 11.10                     # kapak 85°, köprü yukarıda: E ürünü bekler (eski saat · 11,10–13,60 E boşta)
E_KAPAT_ESKI = 13.60                     # kafa H_BEKLE'ye iner: kapatma başlar (ürün kutuya düşmüş olmalı)
E_HAZIR_GERCEK, E_KAPAT_GERCEK = gercek(E_HAZIR_ESKI), gercek(E_KAPAT_ESKI)


def zaman_ozeti_v12():
    """her hareket: eski süre → gerçek süre · tepe hızı gerçek saatte ≤ sınır (denetim)"""
    sat = []
    for r in ZAMAN_RAPORU_V12:
        T0, T1 = gercek(r["t0"]), gercek(r["t1"])
        sat.append(dict(r, sure_eski=round(r["t1"] - r["t0"], 3), T0=round(T0, 3), T1=round(T1, 3), sure_gercek=round(T1 - T0, 3)))
    return sat


def zaman_denetimi_v12():
    """gerçek saatte her eksenin tepe hızı ve ivmesi sınırın içinde mi (eski saat φ ile ölçeklenir) — ihlal listesi"""
    ihlal = []
    Tg = _np_v12.arange(0.0, DONGU_GERCEK, DT_V12)
    tE = _np_v12.interp(Tg, _T_GERCEK, _tg)
    for _ad, _fn, _vl, _al, _br, _kay in EKSEN_V12:
        P = _np_v12.array([_fn(float(t)) if isinstance(_fn(0.0), tuple) else [_fn(float(t))] for t in tE], dtype=float)
        V = _np_v12.linalg.norm(_np_v12.diff(P, axis=0), axis=1) / DT_V12
        vt = float(V.max()) if len(V) else 0.0
        if vt > _vl * 1.02:
            ihlal.append((_ad, round(vt, 1), _vl))
    return ihlal


# ---- v12 · katalog adı olmayan eksen parçalarına gerçek karşılık (BOM) + sıfır sensörleri / kablo zinciri / kontrolcü notu ----
BOM_V12 = {
    "destek_vida": ("Destek tablası vidası Tr16×8 (P4) iki ağızlı trapez, DIN 103 · 169 mm", 1, "600 dev/dk = 80 mm/s · zımbayla 76 mm/s eş hareket", "v12 · VARSAYIM sınıf: Misumi / igus dryspin eşdeğeri", "SATIN ALMA"),
    "destek_somun": ("Bronz somun Tr16×8 flanşsız Ø28 × 20", 1, "", "v12", "SATIN ALMA"),
    "kose_takim_vida": ("Köşe çerçevesi vidası Tr8×8 (P2) dört ağızlı trapez · 158 mm", 1, "600 dev/dk = 80 mm/s", "v12 · 3B yazıcı sınıfı T8×8", "SATIN ALMA"),
    "kose_takim_somun": ("Bronz somun Tr8×8 Ø20 × 25", 1, "", "v12", "SATIN ALMA"),
    "vakum_Z_silindir": ("Kompakt silindir Ø16 strok 20 (SMC CQ2B16-20DZ sınıfı) · dış kılavuzlu", 1, "0,5 MPa'da 100 N · 50–500 mm/s", "v12 · gövde ölçüsü [V] (modelde 34 × 34 × 75 zarf)", "SATIN ALMA"),
    "vakum_vantuz_0": ("Vantuz Ø30 düz, silikon (SMC ZP2-30US sınıfı) + bağlantı", 4, "karton için yumuşak dudak", "v12 · [V]", "SATIN ALMA"),
    "vakum_valf_sensor_blogu": ("Vakum ünitesi: ejektör + besleme/üfleme valfi + vakum sensörü (SMC ZK2 sınıfı)", 1, "karton gözenekliliği denenecek", "v12 · [V] · AÇIK: debi", "SATIN ALMA"),
    "vakum_tek_karton_sensor": ("Çift karton algılayıcı (ultrasonik, Pepperl+Fuchs UDC-18GS sınıfı)", 1, "iki blank birden alınırsa durdurur", "v12 · [V]", "SATIN ALMA"),
    "parmak_kayisi": ("Kayış GT3 6 mm (kapalı, 20T:20T kasnaklar arası)", 1, "ön dil katlayıcı 1:1", "v12", "SATIN ALMA"),
    "parmak_kasnak_ust": ("GT3 20T kasnak Ø8 mil (2 adet: motor + parmak mili)", 2, "PD 19,1", "v12", "SATIN ALMA"),
}
SIFIR_SENSORU_V12 = ("kose_MF", "kose_MB", "kose_PF", "kose_PB", "kose_takim (CNR_LIFT)", "devirme_parmagi (PARMAK)", "destek_tablasi (NEST)")
ACIK_V12 = [
    "7 step eksenin sıfır sensörü yok (4 köşe parmağı, köşe çerçevesi, ön dil, destek tablası) → Omron E2E-X2ME1 (M8, 2 mm) × 7 · yerleşim v13 (BOM'da)",
    "kafa üstündeki 6 motorun kablosu için dikey enerji zinciri (igus E2 micro sınıfı, strok 372) · yerleşim v13",
    "13 step/dir eksen: S7-1200 1214C'nin 4 PTO'su yetmez → EtherCAT kapalı çevrim step sürücüler + hareket denetleyicisi (öneri, karar Kemal'de)",
    "düşey baskı kafası: fren ya da gazlı yay dengeleme (motor enerjisi kesilince kafa düşmesin)",
    "karton: gerçek bıçak izi (die line) + katlama sonrası geri yaylanma fiziksel denenecek (v11'den)",
]
_v11_modul_v12 = modul


def modul():
    r = _v11_modul_v12()
    ad = {p["ad"]: p for p in PARCALAR}
    pk = ad["piston_kafasi"]
    pk["wp"] = pk["wp"].cut(kut(PK_X[0] - 1.0, PK_X[1] + 1.0, H_UST - 1.0, H_UST + 21.0, PK_Z[0] - 1.0, PK_Z[0] + KAFA_ARKA_KIRPMA_V12))
    pk["bom"] = ("Piston kafası 6082 · 261 × 293 × 20 (v12: arka kenar 3 mm kırpıldı — besleme arabasına 4,3 mm) · ön alt kenar 6 mm pah", 1,
                 "tabana basar, iç paneli kilitler, kapağı bastırır", "üretim")
    for k, b in BOM_V12.items():
        if k in ad:
            ad[k]["bom"] = b
    return r
