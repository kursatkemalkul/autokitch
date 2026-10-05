# -*- coding: utf-8 -*-
"""hat_montaj_v86 → v87 (30 Eyl 2026 · Claude · base 4ae5cd0 = v86 b1fb5c9 + Codex K400 hazırlığı). Yalnız kayıtlı montaj worktree'sinde çalıştır.
Kemal (30 Eyl): K (Codex'in kesme-sprey tasarımı) standart / gerçek parçalarla · bulaşık personel tezgâhının altında, üstünde el evyesi ·
E'yi doğrula (standart ürün, motor, saniye) · animasyonları gerçek motor değerleriyle yeniden çalıştır · sayfa düzeni · sitede yayınla.
1 · Codex'in _local/k400-v7/promote.py yaması AYNEN (W_K 400 · X_E 4400 · HAT 5230 · bulaşık K'dan kalkar · K/E saat bağı)
2 · kesme_cad_v7 → kesme_cad_v8 (üretim modeli) · kutu_cad_v11 → kutu_cad_v12 (gerçek süre) · tezgah_cad_v1 → tezgah_cad_v2 (bulaşık tezgâh altında + el evyesi)
3 · K birimleri v8 adlarıyla · fırın → K ürün yolu denetimi K'da KS.urun_merkez'i (çit sınırlı z) izler (v87 WIP: düz yol K400 çitine çarpıyordu)
4 · YOLCULUK GERÇEK SÜRELERLE: trapez profil ("tr") · FR5 TCP 800 mm/s + 0,4 s rampa · yer rayı 800 mm/s + 0,8 s [V] · TOPPING X 200 mm/s + 0,3 s rampa (s2 profili
    tepe hızı 2 katına çıkarıyordu) · tabla hizalama ≤ 35 d/dk · kaset spirali r_ic 22 (20'de tabla x hızı sonsuz) · FIRIN GERÇEK (6,27 mm/s · 3,5 dk pişme,
    fırın bandı sürekli döner) · K v8 + E v12 saatleri · robot E'ye çataldan önce gider · QR sırası çatal çekişinden (CATAL_K)
5 · İSTASYON DÖNGÜSÜ: periyot = K + E periyodu (KS.DONGU 37 s) · E saati KS.e_time (periyodik) · E pizzası K ürün yolunu izler · çekmece turu 37 s'ye sığar
6 · İKİ LAHMACUN: bekleme anı KS.K_DUSTU · robot/tabla anları yolculuktan (YOL_ZAMAN) · fırın ruloları sürekli (tekrar değil)"""
import importlib.util, re
from pathlib import Path
U = Path(__file__).resolve().parent
_sp = importlib.util.spec_from_file_location("k400_promote", U.parent.parent / "_local" / "k400-v7" / "promote.py")
PR = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(PR)
s = PR.build((U / "hat_montaj_v86.py").read_text(encoding="utf-8-sig"))


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:110], s.count(a), n)
    s = s.replace(a, b)


def blok(a, b, yeni):
    """a'dan b'ye (b hariç) değiştir"""
    global s
    i = s.index(a); j = s.index(b, i)
    s = s[:i] + yeni + s[j:]


# ---------------------------------------------------------------- 0 · başlık + sürüm ----------------------------------------------------------------
rep('"""hat_montaj_v86 (29 Eyl 2026 gece · YEREL · Codex v85 üstüne)',
    '"""hat_montaj_v87 (30 Eyl 2026 · Claude · base 4ae5cd0): K v8 ÜRETİM (Codex K400 v7 üstüne: Festo DGRF-C-63-125 · PulsaJet -03 + TG-W · MY1B10G + RB0805 ·\n'
    'EC5000 · Habasit · E3Z · MDG 3 · S7-1200) + E v12 GERÇEK SÜRE + tezgâh v2 (bulaşık tezgâh altında + el evyesi) + GERÇEK SÜRELİ ANİMASYON — yap_hat_montaj_v87.py\n'
    'hat_montaj_v86 (29 Eyl 2026 gece · YEREL · Codex v85 üstüne)')
rep('pafta="HAT v86 (29 Eyl gece · YEREL)',
    'pafta="HAT v87 (30 Eyl · Claude · YEREL): K v8 URETIM (Codex K400) + E v12 GERCEK SURE + TEZGAH v2 (BULASIK TEZGAH ALTINDA, EL EVYESI) + GERCEK SURELI ANIMASYON; HAT 5230 · v86 (29 Eyl gece · YEREL)')

# ---------------------------------------------------------------- 1 · istasyon sürümleri ----------------------------------------------------------------
n7 = s.count("kesme_cad_v7"); assert n7 >= 2, n7
s = s.replace("kesme_cad_v7", "kesme_cad_v8")
n11 = s.count("kutu_cad_v11"); assert n11 >= 2, n11
s = s.replace("kutu_cad_v11", "kutu_cad_v12")
nt = s.count("tezgah_cad_v1"); assert nt >= 2, nt
s = s.replace("tezgah_cad_v1", "tezgah_cad_v2")

# ---------------------------------------------------------------- 2 · K birimleri (v8 adları) ----------------------------------------------------------------
blok('K_BIRIM = [', 'K_HARIC_GRUP = ', '''K_BIRIM = [                                                  # v87: kesme_cad_v8 (Codex K400 v7 üstüne üretim modeli) adlarıyla
    ("K_GOVDE", "KESME istasyonu gövdesi K400: 304 kabuk · köşe dikmeleri · taban 123 · istasyon tabanı 892 · 3 ön kapak (tava 20, ön düzlem +79) · v87: tank ALT dolapta",
     ("ayak_", "taban_sac", "taban_hortum_rakoru", "plint_on", "istasyon_tabani", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "kose_dikmesi", "onyuz_")),
    ("K_BANT", "K bandı: Interroll RollerDrive EC5000 ø50 IP66 24 V 49:1 (0,02–0,37 m/s) + avara ø50 · Habasit CD.F20-A-UW 2 mm beyaz TPU 380 · UHMW kayma tablası · POM çitler (36 mm içeri) · 2 çift Omron E3Z-T61 ışın · ölü plaka",
     ("bant_", "kayma_tablasi", "tahrik_rulosu", "avara_", "olu_plaka", "cit_", "urun_sensoru_")),
    ("K_KESICI", "Kesici + sprey kafası: Festo DGRF-C-GF-63-125-PPV-A-R (6 bar 1870 N · 16,5 mm bağlantı plakası arka kirişe) · yıldız bıçak Ø296 × 6 · koruma halkası · göbekte PulsaJet AAB10000AUH-03 + UniJet TG-W 2.8W (dik)",
     ("kopru_kirisi", "DGRF", "kafa_adaptoru", "ara_dikme", "kafa_plakasi", "bicak_", "koruma_", "kelebek_", "PulsaJet", "isitmali_hortum_kafa", "hortum_baglantisi_")),
    ("K_YAG", "Tereyağı sistemi (ALT dolap): Walther Pilot MDG 3 paslanmaz basınçlı tank 3,2 L (2 gün 1,41 L) + ısıtıcı ceket + regülatör + seviye sensörü · ısıtmalı hortum arkadan kafaya", ("yag_", "isitmali_hortum_", "hava_hortumu_tank")),
    ("K_ITICI", "İtici: SMC MY1B10G-250 (X) + MY1B10G-350 (Z) rodless · MY-J10 yüzer bağlantı · HIWIN MGN15 · 2 × RB0805 şok emici · X arabası 4,7 kg (6082) · Z 2,92 s / X 1,67 s (katalog tampon sınırı)",
     ("itici_", "eksen_ayagi")),
    ("K_ELEKTRIK", "Pano (arka üst): Siemens S7-1200 1214C · Mean Well NDR-240-24 · 2 × E5DC + 2 × G3PE (tank + hortum ısısı) · SMC SS5Y3-20-04 + 3 × SY3120 · AW20-F02-A şartlandırıcı · hortumlar",
     ("pano_", "din_rayi", "plc_", "sicaklik", "SSR_", "sigorta_", "guc_", "klemens", "sartlandirici", "valf_", "hava_")),
]
''')
rep('''raise AssertionError("kesme_cad_v8 parcasi birimsiz kaldi: " + _p["ad"])''', '''raise AssertionError("kesme_cad_v8 parcasi birimsiz kaldi: " + _p["ad"])''')

# ---------------------------------------------------------------- 3 · fırın → K ürün yolu: K'da KS.urun_merkez (çit sınırlı z) ----------------------------------------------------------------
rep('''    _kon = [(float(x_), FT.urun_z(float(x_)), R_) for R_ in (139.5, 149.5) for x_ in range(int(math.ceil(BT.AKT)), 4301, 10)]   # v70: kasetten (aktarma) başlar''',
    '''    _kz87 = {}                                                                     # v87: K400'de ürün z'si çitlerle −170 → −206 (KS.urun_merkez · GELİŞ + TAŞI)
    for _i87 in range(0, int(KS.Z_TASI[1] * 50) + 1):
        _x87, _y87, _z87 = KS.urun_merkez(_i87 / 50.0)
        _xw87 = int(round(X_K + _x87))
        _kz87[_xw87] = min(_kz87.get(_xw87, 9e9), _z87)
    def _zk87(xw):
        if xw < X_K - 60.0: return FT.urun_z(xw)
        ks_ = [k_ for k_ in _kz87 if abs(k_ - xw) <= 5]
        return min(_kz87[k_] for k_ in ks_) if ks_ else FT.urun_z(xw)
    _kon = [(float(x_), _zk87(float(x_)), R_) for R_ in (139.5, 149.5) for x_ in range(int(math.ceil(BT.AKT)), int(X_K + 421), 10)]   # v70: kasetten · v87: K boyunca 4420'ye (bekleme yeri)''')
rep('''    print("FIRIN URUN YOLU (O280 %d konum + O300 zarf %d konum · 28 yuksek · 10 mm adim · DUZ −170: kaset (aktarma) + yarik + yukleme bandi + firin + K → 4300): %s"''',
    '''    print("FIRIN URUN YOLU (O280 %d konum + O300 zarf %d konum · 28 yuksek · 10 mm adim · −170 düz, K'da çitle −206: kaset (aktarma) + yarik + yukleme bandi + firin + K → 4420): %s"''')

# ---------------------------------------------------------------- 3b · hava ana hattının K dalı: K v8 sol duvar rakoru ----------------------------------------------------------------
rep('''ANA_K48 = [(3090, 1977, -432), (3090, 1977, -780), (3385, 1977, -780), (3385, 1870, -780)]''',
    '''ANA_K48 = [(3090, 1977, -432), (3090, 1977, -770), (3294, 1977, -770)]   # v87: K v8 sol duvar rakoruna (KS.Y_HAVA_GIRIS 1809 · z −770 · dış ucu K x −6); istasyon kendi içinde AW20'ye bağlar · v86: MS4 tepesine''')
rep('''_ms4 = [p for p in KS.PARCALAR if p["ad"] == "sartlandirici_MS4"]
assert len(_ms4) == 1, "kesme_cad_v8: sartlandirici_MS4 parcasi yok"
_ms4_ust = _ms4[0]["wp"].val().BoundingBox().ymax''', '''_hgk = [p for p in KS.PARCALAR if p["ad"] == "hava_giris_rakoru"]                  # v87: K v8 hava girişi sol duvarda (MS4 kalktı → SMC AW20)
assert len(_hgk) == 1, "kesme_cad_v8: hava_giris_rakoru yok"
_hgk_b = _hgk[0]["wp"].val().BoundingBox()''')
rep('''    ("hava K dali: ANA_K48 ucu = MS4 ustu + 10 = 1702", (ANA_K48[-1][1], _ms4_ust + 10.0, 1702.0)),''',
    '''    ("v87 · hava K dali ucu y = K sol duvar rakoru ekseni = KS.Y_HAVA_GIRIS = 1809", (ANA_K48[-1][1], round((_hgk_b.ymin + _hgk_b.ymax) / 2.0, 3), KS.Y_HAVA_GIRIS, 1809.0)),
    ("v87 · hava K dali ucu x = K sol duvar rakorunun dis ucu (X_K - 6)", (ANA_K48[-1][0] + X_BC, X_K + _hgk_b.xmin, X_K - 6.0)),
    ("v87 · hava K dali ucu z = rakor ekseni = -770", (ANA_K48[-1][2], round((_hgk_b.zmin + _hgk_b.zmax) / 2.0, 3), KS.Z_HAVA_GIRIS, -770.0)),''')

# ---------------------------------------------------------------- 4 · YOLCULUK: gerçek süreler ----------------------------------------------------------------
blok('''    class Iz:''', '''    def gecis(x0, x1):''', '''    class Iz:
        """zaman → değer: parça parça (s2 · ss · l doğrusal · h0/h1 · tr = TRAPEZ: rampa ta s, tepe hız = yol / (T − ta) · f fonksiyon)"""
        def __init__(s, v0): s.v0 = v0; s.son = v0; s.seg = []
        def git(s, t0, t1, v1, egri="s2", ta=None):
            s.seg.append((t0, t1, s.son, v1, egri, ta)); s.son = v1; return t1
        def f(s, t0, t1, fn):
            s.seg.append((t0, t1, None, fn, "f", None)); s.son = fn(t1); return t1
        def __call__(s, t):
            v = s.v0
            for t0, t1, a, b, e, ta in s.seg:
                if t < t0: return v
                if e == "f":
                    if t < t1: return b(t)
                    v = b(t1); continue
                if t >= t1: v = b; continue
                T_ = t1 - t0; u = (t - t0) / T_
                if e == "s2": u = 2 * u * u if u < 0.5 else 1 - 2 * (1 - u) * (1 - u)
                elif e == "ss": u = u * u * (3 - 2 * u)
                elif e == "h0": u = u * u
                elif e == "h1": u = 1 - (1 - u) * (1 - u)
                elif e == "tr":
                    r_ = min(0.5, (ta or 0.0) / T_)
                    if r_ > 1e-9:
                        vp_ = 1.0 / (1.0 - r_)
                        if u < r_: u = 0.5 * vp_ * u * u / r_
                        elif u > 1.0 - r_: w_ = 1.0 - u; u = 1.0 - 0.5 * vp_ * w_ * w_ / r_
                        else: u = 0.5 * vp_ * r_ + vp_ * (u - r_)
                return a + (b - a) * u
            return v

    # v87 · GERÇEK SÜRE sabitleri (kaynak / [V])
    V_TCP, TA_TCP = 800.0, 0.4                     # Fairino FR5 TCP ≤ 1 m/s (%80) · 0,4 s rampa ≈ 2 m/s² [V: Fairino veri sayfası teyit]
    V_RAY, TA_RAY = 800.0, 0.8                     # FR5 yer rayı ≤ 1 m/s (%80) · 0,8 s rampa ≈ 1 m/s² [V]
    FIRIN_V = FT.ODA / 210.0                       # fırın bandı 1316 mm / 3,5 dk pişme = 6,27 mm/s (firin_tp10_cad_v10 · bant tahriki BOM)
    def sure_tr(d, v, ta):
        """trapez süre: d/v + ta (kısa yolda üçgen: 2·√(d·ta/v))"""
        d = abs(d)
        return d / v + ta if d >= v * ta else 2.0 * math.sqrt(d * ta / v)
    for _i in TH2.IST:                                                              # v87: kaset (KASET ağzı, dz 20) spirali r_ic 20'de tabla x hızı sonsuz → 22
        if _i["tip"] not in ("NOKTA", "YAYICI"):
            TH2.R_IC_IST[_i["kod"]] = max(22.0, TH2.R_IC_IST.get(_i["kod"], TH2.R_IC))

''')
rep('''    CEK = Iz(0.0); CEK.git(0.0, CEK_T, SC.STROK, "l"); CEK.git(5.0, 5.0 + CEK_T, 0.0, "l")''',
    '''    CEK = Iz(0.0); CEK.git(0.0, CEK_T, SC.STROK, "tr", SC.RAMPA_SN)          # v87: 700 mm · Transmotec PD3665 127 d/dk × GT3 Ø28,65 = 190,5 mm/s + 0,3 s rampa (store_cad_v14)''')
rep('''    TOPZ.f(0.0, CEK_T, lambda t: top_z0 + CEK(t))
    T_AL = max(3.5, CEK_T + 0.1)                                        # v76: strok 700 → 3,7 s
    TOPZ.git(CEK_T, T_AL, top_z0 + SC.STROK, "l")
    TOPY.git(T_AL, 4.2, 650.0); TOPX.git(4.2, 5.6, X_AC); TOPY.git(4.2, 5.6, P + 47.0); TOPZ.git(4.2, 5.6, 150.0)
    TOPZ.git(5.6, 6.4, ZT); TOPY.git(6.4, 6.9, P + TOP_H + 0.5, "ss")
    X_PARK = _cb["x"][0] - 110.0                                        # v58: robot çekmecenin AÇICI TARAFINDA, açık çekmeceye girmez (kaide yarı genişliği 90 + pay 20)
    X_ROB_AC = 700.0                                                   # v58: topu açıcıya bırakırken robot x (açıcı 350'ye erişim ≤ 915 · zincir yüzünden ≥ 508)
    ROB = Iz(RX0); ROB.git(0.3, 3.0, X_PARK); ROB.git(4.2, 5.6, X_ROB_AC)   # v58: top–robot birlikte gider (TOPX 4,2–5,6 ile aynı aralık)
    _ey = max(math.sqrt((TOPX(t_ / 20.0) - ROB(t_ / 20.0)) ** 2 + (TOPY(t_ / 20.0) - OMUZ) ** 2 + (TOPZ(t_ / 20.0) - RZ) ** 2) for t_ in range(70, 139))
    print("   v58 · ROBOT TOPU TASIR: park x %.1f (cekmece %.1f-%.1f disinda) → aciciya x %.0f · top–omuz en uzak %.0f mm (3,5–6,9 s) ≤ pratik erisim %.0f  %s"
          % (X_PARK, _cb["x"][0], _cb["x"][1], X_ROB_AC, _ey, ERISIM, _gk(_ey <= ERISIM)))''',
    '''    TOPZ.f(0.0, CEK_T, lambda t: top_z0 + CEK(t))
    X_PARK = _cb["x"][0] - 110.0                                        # v58: robot çekmecenin AÇICI TARAFINDA, açık çekmeceye girmez (kaide yarı genişliği 90 + pay 20)
    X_ROB_AC = 700.0                                                   # v58: topu açıcıya bırakırken robot x (açıcı 350'ye erişim ≤ 915 · zincir yüzünden ≥ 508)
    ROB = Iz(RX0)
    T_PARK = ROB.git(0.3, 0.3 + sure_tr(X_PARK - RX0, V_RAY, TA_RAY), X_PARK, "tr", TA_RAY)       # v87: ray trapez (v86 2,7 s → s2 tepesi 1040 mm/s)
    T_AL = max(CEK_T, T_PARK) + 0.3 + 0.4 + 0.3                          # v87: çekmece açık + robot yanaşır (0,4) + tutar (0,3)
    TOPZ.git(CEK_T, T_AL, top_z0 + SC.STROK, "l")
    T_KALK = TOPY.git(T_AL, T_AL + sure_tr(650.0 - top_y0, V_TCP, TA_TCP), 650.0, "tr", TA_TCP)  # v87: kaldırma (v86 0,13 s → 3,2 m/s)
    _dtr = math.sqrt((X_AC - top_x) ** 2 + (P + 47.0 - 650.0) ** 2 + (150.0 - top_z0 - SC.STROK) ** 2)
    T_TR0 = T_KALK; T_TR1 = T_TR0 + max(sure_tr(_dtr, V_TCP, TA_TCP), sure_tr(X_ROB_AC - X_PARK, V_RAY, TA_RAY))
    TOPX.git(T_TR0, T_TR1, X_AC, "tr", TA_TCP); TOPY.git(T_TR0, T_TR1, P + 47.0, "tr", TA_TCP); TOPZ.git(T_TR0, T_TR1, 150.0, "tr", TA_TCP)
    ROB.git(T_TR0, T_TR1, X_ROB_AC, "tr", TA_RAY)                         # v58: top–robot birlikte gider
    T_IN = TOPZ.git(T_TR1, T_TR1 + sure_tr(150.0 - ZT, V_TCP, TA_TCP), ZT, "tr", TA_TCP)
    T_TOP_IN = TOPY.git(T_IN, T_IN + 0.5, P + TOP_H + 0.5, "tr", 0.2)
    T_BIRAK = T_TOP_IN + 0.3 + 0.4                                       # bırakır (0,3) + geri çekilir (0,4)
    CEK.git(T_KALK + 0.3, T_KALK + 0.3 + CEK_T, 0.0, "tr", SC.RAMPA_SN)   # top çıkınca çekmece kapanır
    _ey = max(math.sqrt((TOPX(t_) - ROB(t_)) ** 2 + (TOPY(t_) - OMUZ) ** 2 + (TOPZ(t_) - RZ) ** 2) for t_ in [T_AL + (T_TOP_IN - T_AL) * i_ / 80.0 for i_ in range(81)])
    print("   v58 · ROBOT TOPU TASIR: park x %.1f (cekmece %.1f-%.1f disinda) → aciciya x %.0f · top–omuz en uzak %.0f mm (%.1f–%.1f s) ≤ pratik erisim %.0f  %s"
          % (X_PARK, _cb["x"][0], _cb["x"][1], X_ROB_AC, _ey, T_AL, T_TOP_IN, ERISIM, _gk(_ey <= ERISIM)))''')
rep('''    ADIM += [(0.0, "ÇEKMECE", "B'nin hamur çekmecesi açılır (strok %.0f, %.1f s); FR5 rayda çekmecenin yanına (açıcı tarafına) gelir; topu alıp açıcıya taşır." % (SC.STROK, CEK_T)),
             (T_AL, "ROBOT", "FR5 hamur topunu alır, açıcının ağzından tablaya bırakır. Top 80 mm yüksek: açıcı kafası bu sırada 90 mm'ye kalkar (60 yetmiyor — AÇIK NOKTA).")]''',
    '''    ADIM += [(0.0, "ÇEKMECE", "B'nin hamur çekmecesi açılır: strok %.0f mm, %.2f s (Transmotec PD3665 24 V · 127 d/dk × GT3 Ø28,65 = 190 mm/s, 0,3 s yumuşak rampa, ≈60 N). FR5 rayda çekmecenin yanına (açıcı tarafına) gelir (%.1f s)." % (SC.STROK, CEK_T, T_PARK - 0.3)),
             (T_AL, "ROBOT", "FR5 topu tutar, %.1f s'de kaldırır, %.1f s'de açıcının ağzına taşır (TCP ≤ 800 mm/s [V]), tablaya bırakır. Top 80 mm yüksek: açıcı kafası bu sırada 90 mm'ye kalkar (60 yetmiyor — AÇIK NOKTA)." % (T_KALK - T_AL, T_TR1 - T_TR0))]''')
rep('''    KAFA.git(5.0, 5.6, 1.5, "ss")                                     # top girerken ek kalkış
    t = 7.2''', '''    KAFA.git(T_TR0, T_TR0 + 0.6, 1.5, "ss")                           # top girerken ek kalkış (v87: taşıma başında)
    t = math.ceil((T_BIRAK + 0.3) * FPS - 1e-6) / FPS                  # v87: kare sınırı (koniler 686°/s başlar — kare ortasında başlarsa glTF ara değeri eksenden kayar)''')
rep('''        PIS[k].git(7.4, 8.2, TH2.uno(k, IS[k]["sil"], DOZ[k])["strok"], "l")''',
    '''        PIS[k].git(T_ACMA + 0.2, T_ACMA + 1.0, TH2.uno(k, IS[k]["sil"], DOZ[k])["strok"], "l")''')
rep('''    ADIM.append((7.2, "AÇICI", "Konili açıcı iner, topu Ø280'e açar (3 s, tabla kilitli). Bu sırada sos UNO'su emer."))''',
    '''    ADIM.append((T_BIRAK + 0.3, "AÇICI", "Konili açıcı iner (0,8 s), topu Ø280'e açar (3 s, tabla kilitli). Bu sırada sos UNO'su emer."))''')
n_g = s.count('X.git(t, t + gecis(X.son, i["x"]), i["x"])') + s.count('X.git(t, t + gecis(X.son, x0), x0)') + s.count('X.git(t, t + gecis(X.son, TH2.X_AKTARMA), TH2.X_AKTARMA)')
assert n_g == 3, n_g
s = s.replace('X.git(t, t + gecis(X.son, i["x"]), i["x"])', 'X.git(t, t + gecis(X.son, i["x"]), i["x"], "tr", TH2.RAMPA_X)')
s = s.replace('X.git(t, t + gecis(X.son, x0), x0)', 'X.git(t, t + gecis(X.son, x0), x0, "tr", TH2.RAMPA_X)')
s = s.replace('X.git(t, t + gecis(X.son, TH2.X_AKTARMA), TH2.X_AKTARMA)', 'X.git(t, t + gecis(X.son, TH2.X_AKTARMA), TH2.X_AKTARMA, "tr", TH2.RAMPA_X)')
rep('''        _dt = _kalan / (6.0 * TH2.RPM_NOKTA) + TH2.RAMPA_SN
        TH.git(t, t + _dt, TH.son + _kalan, "ss"); t += _dt''', '''        _dt = sure_tr(_kalan, 6.0 * TH2.RPM_NOKTA, TH2.RAMPA_SN)                          # v87: trapez ≤ 35 d/dk (v86 ss tepesi 1,5 kat)
        TH.git(t, t + _dt, TH.son + _kalan, "tr", TH2.RAMPA_SN); t += _dt''')
rep('''    X.git(T_B1 + 0.2, T_B1 + 0.2 + gecis(TH2.X_AKTARMA, TH2.X_PARK), TH2.X_PARK)
    T_F0, T_F1 = T_B1, T_B1 + 10.0
    BANT.git(T_F0, T_F1, (3940.0 - X_B1), "l")''', '''    X.git(T_B1 + 0.2, T_B1 + 0.2 + gecis(TH2.X_AKTARMA, TH2.X_PARK), TH2.X_PARK, "tr", TH2.RAMPA_X)
    T_F0, T_F1 = T_B1, T_B1 + (3940.0 - X_B1) / FIRIN_V                                        # v87: GERÇEK — 6,27 mm/s (v86: 10 s hızlandırılmış)
    BANT_F = lambda t: FIRIN_V * t                                                                 # fırın bandı hiç durmaz
    _ek_y = BT.H.S["zaman"]["yol_mm"] - FIRIN_V * (T_B1 - T_B0)                                     # yükleme bandının aktarma atılımı
    def BANT_Y(t, T0=T_B0, T1=T_B1):
        u = min(1.0, max(0.0, (t - T0) / (T1 - T0)))
        return FIRIN_V * t + _ek_y * u''')
rep('''    ADIM.append((T_F0, "FIRIN", "Yükleme bandı ısıtılan bölgenin başındadır: pideyi kasetten hızlı alır, sonra fırın bandı hızında taşıyıp fırın bandına verir (fırın bandı hiç durmaz, hızı değişmez). TP10 kesitli fırın, gövde 1500: ısıtılan %.0f mm, aynı anda %d ürün. Ürün düz −170 ekseninde K bandına geçer. Animasyonda HIZLANDIRILMIŞ: gerçekte 3,5 dk, burada 10 s." % (FT.ODA, FT.N_URUN)))''',
    '''    ADIM.append((T_F0, "FIRIN", "Yükleme bandı ısıtılan bölgenin başındadır: pideyi kasetten hızlı alır, sonra fırın bandı hızında taşıyıp fırın bandına verir (fırın bandı hiç durmaz, %.2f mm/s). TP10 kesitli fırın, gövde 1500: ısıtılan %.0f mm = 3,5 dk pişme, aynı anda %d ürün. GERÇEK SÜRE: ürün %.0f s'de K bandına gelir (izlerken hızlandırın)." % (FIRIN_V, FT.ODA, FT.N_URUN, T_F1 - T_F0)))''')
rep('''    ADIM += [(T0K + KS.Z_GELIS[0], "KESME", "K bandı ürünü fırın bandından alıp kesme merkezine getirir. Kafa iner, 6 dilim keser (bıçak bandın 0,5 mm üstünde durur). Pizzada sprey yok; pidede aynı kafadaki nozül tereyağı püskürtür."),
             (T0K + KS.Z_TASI[0], "K BANDI + İTİCİ", "K bandı 220 mm ön besler; kısa düz itici yandan arkaya gelir ve 240 mm kutuya iter."),
             (T0K + KS.Z_ITME[0], "KUTU", "İtici ürünü katlanmış kutuya sürer (2,5 s); ürün tabana düşer, kol + piston kapağı kapatıp bastırır."),
             (T0K + KC.Z_CATAL[0] + 0.4, "ROBOT → QR", "FR5 kutuyu tepsinin aralıklarından çatalla alır, rayda QR dolabının önüne (x %.0f) gider." % QR.ROBOT_X)]
    ROB.git(T0K + 5.0, T0K + 9.0, X_E + 260.0)''',
    '''    ADIM += [(T0K + KS.Z_GELIS[0], "KESME", "K bandı (Interroll EC5000, ≤ 0,37 m/s) ürünü fırın bandından alır, 2 s'de kesme merkezine getirir (E3Z ışını durdurur). Pidede kafanın göbeğindeki PulsaJet 1,2 s tereyağı püskürtür. Festo DGRF-C-63 kafayı 1,4 s'de indirir, 6 dilim keser (bıçak bandın 0,5 mm üstünde durur), 0,8 s'de kaldırır."),
             (T0K + KS.Z_TASI[0], "K BANDI + İTİCİ", "K bandı ürünü 220 mm ileri taşır (ön kenarı E'ye girer; E hazır bekler). SMC MY1B10G-350 Z itici arkadan %.1f s'de gelir (lastik tampon sınırı)." % (KS.Z_IN[1] - KS.Z_IN[0])),
             (T0K + KS.Z_ITME[0], "KUTU", "MY1B10G-250 X itici (RB0805 şok emicili) ürünü %.2f s'de katlanmış kutuya sürer; ürün tabana oturur, kol + piston kapağı kapatıp bastırır." % (KS.Z_ITME[1] - KS.Z_ITME[0])),
             (T0K + KS.CATAL_K[0], "ROBOT → QR", "FR5 kutuyu tepsinin aralıklarından çatalla alır, çekip QR dolabının önüne getirir.")]
    _T_ERAY = sure_tr(X_E + 260.0 - X_ROB_AC, V_RAY, TA_RAY)
    ROB.git(T0K + KS.CATAL_K[0] - 1.0 - _T_ERAY, T0K + KS.CATAL_K[0] - 1.0, X_E + 260.0, "tr", TA_RAY)   # v87: çatal girmeden 1 s önce E'nin önünde''')
rep('''    TAS = Iz(0.0); TAS.git(T0K + 20.9, T0K + 22.0, 1.0, "s2")                                    # v57: 1) kutu QR yüzünün önünde x + y'de göz ağzına hizalanır (ön yüzü 650'de, gövdeye girmez)
    TAS_Z = Iz(0.0); TAS_Z.git(T0K + 22.0, T0K + 23.3, 1.0, "s2")                                # v57: 2) sonra düz z'de açık kapak ağzından göze girer (açık kapağın altından)
    KAPAK_QR = Iz(0.0); KAPAK_QR.git(T0K + 20.2, T0K + 20.9, 1.0, "ss"); KAPAK_QR.git(T0K + 24.0, T0K + 24.7, 0.0, "ss")   # göz robot kapağı: kutu girmeden açılır, robot çekilince kapanır
    ROB.git(T0K + 20.9, T0K + 23.3, QH["robot_x"]); ROB.git(T0K + 23.9, T0K + 27.9, RX0)''',
    '''    T_Q0 = T0K + KS.CATAL_K[3] + 0.2                                                              # v87: çatal çekişi bitti (E v12 gerçek saat)
    _dxy = math.hypot(QH["dx"], QH["dy"])
    T_Q1 = T_Q0 + sure_tr(_dxy, V_TCP, TA_TCP); T_Q2 = T_Q1 + sure_tr(QH["dz"], V_TCP, TA_TCP)
    TAS = Iz(0.0); TAS.git(T_Q0, T_Q1, 1.0, "tr", TA_TCP)                                           # v57: 1) kutu QR yüzünün önünde x + y'de göz ağzına hizalanır
    TAS_Z = Iz(0.0); TAS_Z.git(T_Q1, T_Q2, 1.0, "tr", TA_TCP)                                       # v57: 2) sonra düz z'de açık kapak ağzından göze girer
    KAPAK_QR = Iz(0.0); KAPAK_QR.git(T_Q0 - 0.7, T_Q0, 1.0, "ss"); KAPAK_QR.git(T_Q2 + 0.3 + 0.8, T_Q2 + 0.3 + 0.8 + 0.7, 0.0, "ss")   # kutu girmeden açılır, robot çekilince kapanır
    ROB.git(T_Q0, max(T_Q2, T_Q0 + sure_tr(QH["robot_x"] - X_E - 260.0, V_RAY, TA_RAY)), QH["robot_x"], "tr", TA_RAY)
    T_DON0 = T_Q2 + 0.3 + 0.8                                                                        # bırakır + çatal geri çekilir
    T_DON1 = ROB.git(T_DON0, T_DON0 + sure_tr(QH["robot_x"] - RX0, V_RAY, TA_RAY), RX0, "tr", TA_RAY)''')
rep('''    ADIM.append((T0K + 20.2, "QR DOLABI",''', '''    ADIM.append((T_Q0 - 0.7, "QR DOLABI",''')
rep('''    T_J = math.ceil(T0K + 28.9)''', '''    T_J = math.ceil(max(T_DON1, KAPAK_QR.seg[-1][1], T0K + KS.E_BITIS_K) + 0.5)                  # v87: robot geri döndü + E döngüsü bitti''')
rep('''    QR_YOL.update(t=(T0K + KC.Z_CATAL[2] + 0.4, T0K + 24.7), kapak=KAPAK_QR,''', '''    QR_YOL.update(t=(T0K + KS.CATAL_K[2], KAPAK_QR.seg[-1][1]), kapak=KAPAK_QR,''')
rep('''        if tK < 13.2:''', '''        if tK < KS.K_DUSTU:''')
rep('''x, y, z = KS.urun_merkez(max(0.0, tK)); xw = X_K + x; return (xw, y, FT.urun_z(xw) if xw < FT.CC_B[0] + 1.0 else z)''',
    '''x, y, z = KS.urun_merkez(max(0.0, tK)); xw = X_K + x; return (xw, y, z)          # v87: z K v8 çit yolundan (−170 → −206 sürekli; FT.CC_B'de 36 mm sıçrama vardı)''')
# fırın + yükleme bandı ruloları: sürekli bantlar
rep('''    for g, (P_, r_) in ROL_F.items():
        ton = {}''', '''    for g, (P_, r_) in ROL_F.items():
        _BF = BANT_Y if "_GB_" in g else BANT_F                                                     # v87: fırın bandı sürekli · yükleme bandı + aktarma atılımı
        SUREKLI[ "F_DONER__" + g] = (r_, "GB" if "_GB_" in g else "TP")
        ton = {}''')
rep('''        fR = lambda t, r_=r_: qax((0, 0, 1), -math.degrees(BANT(t) / r_))
        OZEL_T.append(dict(ad=ad, ebeveyn=None, T=tuple(c * MM for c in P_), tonlar=ton))''',
    '''        fR = lambda t, r_=r_, _BF=_BF: qax((0, 0, 1), -math.degrees(_BF(t) / r_))
        OZEL_T.append(dict(ad=ad, ebeveyn=None, T=tuple(c * MM for c in P_), tonlar=ton))''')
rep('''    YOL_ZAMAN.clear(); YOL_ZAMAN.update(T0K=T0K, T_J=float(T_J), FPS=FPS)                         # v66''',
    '''    YOL_ZAMAN.clear(); YOL_ZAMAN.update(T0K=T0K, T_J=float(T_J), FPS=FPS, T_PARK=T_PARK, T_BIRAK=T_BIRAK, T_TR0=T_TR0, FIRIN_V=FIRIN_V,
                                        T_B0=T_B0, T_B1=T_B1, EK_Y=_ek_y, T_F0=T_F0, T_F1=T_F1)                       # v66 · v87: iki lahmacun anları
    # v87 · HIZ DENETİMİ (sayısal türev · katalog / [V] sınırları)
    _HZ = []
    def _tepe(fn, t0_, t1_, n_=600):
        vs_ = [fn(t0_ + (t1_ - t0_) * i_ / n_) for i_ in range(n_ + 1)]
        return max(abs(vs_[i_ + 1] - vs_[i_]) / ((t1_ - t0_) / n_) for i_ in range(n_))
    _tcp = lambda t: math.sqrt(TOPX(t) ** 2 + TOPY(t) ** 2 + TOPZ(t) ** 2)
    _v_tcp = 0.0
    for i_ in range(1200):
        a_, b_ = T_AL + (T_TOP_IN - T_AL) * i_ / 1200.0, T_AL + (T_TOP_IN - T_AL) * (i_ + 1) / 1200.0
        _v_tcp = max(_v_tcp, math.sqrt((TOPX(b_) - TOPX(a_)) ** 2 + (TOPY(b_) - TOPY(a_)) ** 2 + (TOPZ(b_) - TOPZ(a_)) ** 2) / (b_ - a_))
    _HZ.append(("FR5 TCP (top)", _v_tcp, 1000.0, "mm/s"))
    _HZ.append(("FR5 yer rayı", _tepe(ROB, 0.0, float(T_J), 4000), 1000.0, "mm/s"))
    _HZ.append(("B çekmecesi (Transmotec 127 d/dk)", _tepe(CEK, 0.0, T_BIRAK, 2000), 127.0 / 60.0 * math.pi * SC.KAS_PD + 0.5, "mm/s"))
    _HZ.append(("TOPPING X arabası", _tepe(X, T_BIRAK, T_B1 + 8.0, 6000), TH2.X_HIZ + 0.5, "mm/s"))
    _HZ.append(("TOPPING tabla (d/dk)", _tepe(TH, T_BIRAK, T_B1 + 8.0, 6000) / 6.0, max(TH2.RPM_NOKTA, TH2.RPM_YAYICI) + 0.2, "d/dk"))
    _HZ.append(("Fırın bandı", FIRIN_V, FIRIN_V + 1e-6, "mm/s"))
    for ad_, v_, lim_, bi_ in _HZ:
        print("   v87 · HIZ %-34s tepe %8.1f %s ≤ %.1f  %s" % (ad_, v_, bi_, lim_, _gk(v_ <= lim_)))
    assert all(v_ <= lim_ for _a, v_, lim_, _b in _HZ), "v87: hareket katalog / [V] hız sınırını aşıyor: %s" % [h_ for h_ in _HZ if h_[1] > h_[2]]''')
rep('''YOL_ZAMAN = {}''', '''YOL_ZAMAN = {}
SUREKLI = {}                                                                                    # v87: sürekli dönen düğümler (fırın / yükleme bandı ruloları) → iki lahmacunda tekrar değil süreklilik''')

# ---------------------------------------------------------------- 5 · İSTASYON DÖNGÜSÜ (K + E periyodu) ----------------------------------------------------------------
rep('''T_HAT = 40.0                                                                             # v38: ortak animasyon dongusu (cekmece turu 34,8 · kutu modulu 2 × 20)''',
    '''T_HAT = float(KS.DONGU)                                                                  # v87: K + E bir ürün periyodu (kesme_cad_v8 · E v12 gerçek saat) · v38: 40''')
rep('''    _bek, _ara = 1.5, 0.6''', '''    _bek, _ara = 0.8, 0.4                                                            # v87: çekmece turu periyoda (37 s) sığar''')
rep('''    def _te(t):
        return KS.e_time(t % (KS.DONGU + 3.0) - 3.0)''', '''    def _tk(t):
        return t % KS.DONGU
    def _te(t):                                                                     # v87: E saati K'ya bağlı · E bir sonraki ürün için K periyodunun sonunda başlar
        tk_ = _tk(t)
        return KS.e_time(tk_ if tk_ < KS.DONGU + KS.E_BASLA_K else tk_ - KS.DONGU)
    def _pizza87(t):                                                                # v87: E pizzası K ürün yolunu izler (K'da çit + itici · E'de çatal)
        tk_ = _tk(t)
        if tk_ < KS.K_DUSTU:
            x_, y_, z_ = KS.urun_merkez(tk_)
            return (x_ - (X_E - X_K) - KC.PIZZA_X0, y_ - KC.PLAKA_K, z_ - KC.PIZZA_Z0)
        return KC.pizza_trs(_te(t))
    def _gor87(t):
        tk_ = _tk(t)
        return (1.0 if tk_ >= KS.Z_GELIS[0] else 1e-4) if tk_ < KS.K_DUSTU else KC.gorunur(_te(t))''')
rep('''"FRONT_Y": lambda t: (0,KC.front_dy(t),0), "PIZZA": KC.pizza_trs}
    _say0 = len(ANIM)''', '''"FRONT_Y": lambda t: (0,KC.front_dy(t),0)}
    _say0 = len(ANIM)''')
rep('''            ANIM.append((a_, _TT, [_mm(f_(_te(t))) for t in _TT]))
            if a_.endswith("__PIZZA"):
                ANIM.append((a_, _TT, [(max(1e-4, KC.gorunur(_te(t))),) * 3 for t in _TT], "scale"))''',
    '''            ANIM.append((a_, _TT, [_mm(f_(_te(t))) for t in _TT]))
        elif a_.startswith("E_") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] == "PIZZA":              # v87
            ANIM.append((a_, _TT, [_mm(_pizza87(t)) for t in _TT]))
            ANIM.append((a_, _TT, [(max(1e-4, _gor87(t)),) * 3 for t in _TT], "scale"))''')
rep('''            ANIM.append((a_, _TT, [_mm(KS.grup_trs(g_, max(0.0, t % (KS.DONGU + 3.0) - 3.0))) for t in _TT]))''',
    '''            ANIM.append((a_, _TT, [_mm(KS.grup_trs(g_, _tk(t))) for t in _TT]))''')
rep('''    _n = int(round(T_HAT * 15.0)) + 1
    _TT = [min(T_HAT, i_ / 15.0) for i_ in range(_n)]''', '''    _n = int(round(T_HAT * 30.0)) + 1                                                  # v87: 30 fps (E ve K gerçek hızları)
    _TT = [min(T_HAT, i_ / 30.0) for i_ in range(_n)]''')

# ---------------------------------------------------------------- 6 · İKİ LAHMACUN ----------------------------------------------------------------
rep('''    def iki_lahmacun(A, Z, TE_H=13.3):''', '''    def iki_lahmacun(A, Z, TE_H=KS.K_DUSTU + 0.05):''')
rep('''        def grup(ad):
            if ad.startswith("URUN__L2_"): return "urun2"''', '''        def grup(ad):
            if ad in SUREKLI: return "surekli"                                          # v87: fırın / yükleme bandı ruloları
            if ad.startswith("URUN__L2_"): return "urun2"''')
rep('''        D = max(D, e_tabla - 3.9)                                                         # 2. top diske inmeden (4,2 s) tabla açıcıya dönmüş olmalı''',
    '''        D = max(D, e_tabla - (Z["T_TR0"] - 0.3))                                          # 2. top taşınmaya başlamadan tabla açıcıya dönmüş olmalı (v87: yolculuktan)''')
rep('''                t_b = 6.9''', '''                t_b = Z["T_BIRAK"]                                                          # v87: robot topu bıraktı''')
rep('''                        out.append(samp(V, t_b, yol) + (samp(V, 3.0, yol) - samp(V, t_b, yol)) * u_)''',
    '''                        out.append(samp(V, t_b, yol) + (samp(V, Z["T_PARK"], yol) - samp(V, t_b, yol)) * u_)''')
rep('''            elif g_ == "qr":
                out = [samp(V, max(0.0, t - D), yol) for t in TT2]''', '''            elif g_ == "qr":
                out = [samp(V, max(0.0, t - D), yol) for t in TT2]
            elif g_ == "surekli" and yol != "rotation":                                # v87: rulo düğümünün yeri sabit
                out = [V[0]] * len(TT2)
            elif g_ == "surekli":                                                        # v87: bant hiç durmaz · 2. ürünün yükleme bandı atılımı D sonra
                r_, tip_ = SUREKLI[ad]
                for t in TT2:
                    b_ = Z["FIRIN_V"] * t
                    if tip_ == "GB":
                        for d_ in (0.0, D):
                            b_ += Z["EK_Y"] * min(1.0, max(0.0, (t - d_ - Z["T_B0"]) / (Z["T_B1"] - Z["T_B0"])))
                    a_ = -b_ / r_
                    out.append(_np.array([0.0, 0.0, _m.sin(a_ / 2.0), _m.cos(a_ / 2.0)]))''')

compile(s, "hat_montaj_v87.py", "exec")
(U / "hat_montaj_v87.py").write_text(s, encoding="utf-8")
# sayfa bağlantısı (makine.html / index.html): v86 → v87
for name in ("makine.html", "index.html"):
    p = U.parent.parent / "otonom" / "hat" / name
    data = p.read_bytes()
    if b"hat_v87" in data:
        continue
    assert b"hat_v86" in data, name
    data = re.sub(rb"hat_v86\.(glb|usdz)\?v=86[\w-]*", rb"hat_v87.\1?v=87", data)
    assert b"hat_v86" not in data, name
    p.write_bytes(data)
print("v87 montaj üreteci yazıldı (v86 + Codex K400 + K v8 + E v12 + tezgâh v2 + gerçek süreler) · makine.html / index.html model bağlantısı v87")
