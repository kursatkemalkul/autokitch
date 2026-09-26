# ---------------------------------------------------------------- v45 · 1 TAM ANİMASYON: ÜRÜN YOLCULUĞU ----------------------------------------------------------------
# Bu parça hat_montaj_v45.py'ye yap_hat_montaj_v45.py tarafından gömülür (tek başına çalışmaz).
def yolculuk(parcalar):
    """Kemal (25 Eyl): "ürün montajına 1 tam animasyon ekle". Bir PİZZA (sos 80 g · kaşar 100 g · küp sucuk 70 g):
    B çekmecesi → FR5 → açıcı → TOPPING (sos yayıcıda tam 1 tur, kaşar + sucuk spirali) → bant → fırın (HIZLANDIRILMIŞ) →
    K (kesme, çit, itici) → E (kutu) → FR5 → QR dolabı. Her hareket makinenin KENDİ kinematiğinden:
    TOPPING = makine_kodu_v2 sırası + topping_v2_hesap_v1 · K = kesme_cad_v1 · E = kutu_cad_v3 · B = store_cad_v5 stroku."""
    import math
    import topping_v2_hesap_v1 as TH2
    FPS = 30.0                                                        # v46: hızlı dönen makaralar karede ≤ 31°
    OX, OY = X_BC, H_B

    class Iz:
        """zaman → değer: parça parça (s2 = sürücü S-rampası · ss · l doğrusal · h0/h1 hızlanma/yavaşlama · f fonksiyon)"""
        def __init__(s, v0): s.v0 = v0; s.son = v0; s.seg = []
        def git(s, t0, t1, v1, egri="s2"):
            s.seg.append((t0, t1, s.son, v1, egri)); s.son = v1; return t1
        def f(s, t0, t1, fn):
            s.seg.append((t0, t1, None, fn, "f")); s.son = fn(t1); return t1
        def __call__(s, t):
            v = s.v0
            for t0, t1, a, b, e in s.seg:
                if t < t0: return v
                if e == "f":
                    if t < t1: return b(t)
                    v = b(t1); continue
                if t >= t1: v = b; continue
                u = (t - t0) / (t1 - t0)
                if e == "s2": u = 2 * u * u if u < 0.5 else 1 - 2 * (1 - u) * (1 - u)
                elif e == "ss": u = u * u * (3 - 2 * u)
                elif e == "h0": u = u * u
                elif e == "h1": u = 1 - (1 - u) * (1 - u)
                return a + (b - a) * u
            return v

    def gecis(x0, x1): return abs(x1 - x0) / TH2.X_HIZ + TH2.RAMPA_X

    # ================= ZAMAN ÇİZELGESİ =================
    DOZ = TH2.RECETE["pizza"]["doz"]
    SIRA = sorted(DOZ, key=lambda k: [i["x"] for i in TH2.IST if i["kod"] == k][0])
    IS = {i["kod"]: i for i in TH2.IST}
    ADIM = []
    # B + robot + top
    CEK_T = SC.STROK / (127.0 / 60.0 * math.pi * SC.KAS_PD)           # 3,3 s (çekmece motoru)
    CEK = Iz(0.0); CEK.git(0.0, CEK_T, SC.STROK, "l"); CEK.git(5.0, 5.0 + CEK_T, 0.0, "l")
    _rb = [b for b in B if b["kod"] == "ROBOT_1"][0]; RX0 = (_rb["x"][0] + _rb["x"][1]) / 2.0
    _cb = [b for b in B if b["kod"] == "CEK_K1_hamur_3"][0]
    TOP_R, TOP_K = 49.0, 0.82
    _tm = [m_ for a_, m_, _x in parcalar if a_ == "URUN__top"]
    TOP_H = (-min(q[1] for q in _tm[0].P) / MM) if _tm else TOP_R * TOP_K   # v47: topun GERÇEK yarı yüksekliği (ağdan · 34,8)
    top_x, top_y0, top_z0 = (_cb["x"][0] + _cb["x"][1]) / 2.0, _cb["y"][0] + 5.0 + TOP_H, (_cb["z"][0] + _cb["z"][1]) / 2.0
    X_AC = OX + TC.XC_TABLA
    TOPX, TOPY, TOPZ = Iz(top_x), Iz(top_y0), Iz(top_z0)
    TOPZ.f(0.0, CEK_T, lambda t: top_z0 + CEK(t))
    TOPZ.git(CEK_T, 3.5, top_z0 + SC.STROK, "l")
    TOPY.git(3.5, 4.2, 650.0); TOPX.git(4.2, 5.6, X_AC); TOPY.git(4.2, 5.6, 1215.0); TOPZ.git(4.2, 5.6, 150.0)
    TOPZ.git(5.6, 6.4, ZT); TOPY.git(6.4, 6.9, H_B + 108.0 + TOP_H + 0.5, "ss")
    ROB = Iz(RX0); ROB.git(0.3, 3.0, top_x)
    ADIM += [(0.0, "ÇEKMECE", "B'nin hamur çekmecesi açılır (strok %.0f, %.1f s); FR5 rayda çekmecenin önüne gelir." % (SC.STROK, CEK_T)),
             (3.5, "ROBOT", "FR5 hamur topunu alır, açıcının ağzından tablaya bırakır. Top 80 mm yüksek: açıcı kafası bu sırada 90 mm'ye kalkar (60 yetmiyor — AÇIK NOKTA).")]
    # TOPPING
    X = Iz(TC.XC_TABLA); TH = Iz(0.0); KAFA = Iz(1.0); ACMA = Iz(0.0); KONI = Iz(0.0); BANT = Iz(0.0)
    PIS = {k: Iz(0.0) for k in IS if "sil" in IS[k]}; VAL = {k: Iz(0.0) for k in PIS}
    HEL = {k: Iz(0.0) for k in ("KASAR", "SUCUK")}; KAR = {k: Iz(0.0) for k in HEL}
    KAFA.git(5.0, 5.6, 1.5, "ss")                                     # top girerken ek kalkış
    t = 7.2
    KAFA.git(t, t + 0.8, 0.0, "ss"); t += 0.8
    T_ACMA = t
    ACMA.git(t, t + 3.0, 1.0, "l"); KONI.git(t, t + 3.0, 35.0 / math.sin(math.radians(17.82)) * 6.0 * 3.0, "l")
    for k in [k for k in SIRA if k in PIS]:
        PIS[k].git(7.4, 8.2, TH2.uno(k, IS[k]["sil"], DOZ[k])["strok"], "l")
    t += 3.0; KAFA.git(t, t + 0.6, 1.0, "ss"); t += 0.6
    ADIM.append((7.2, "AÇICI", "Konili açıcı iner, topu Ø280'e açar (3 s, tabla kilitli). Bu sırada sos UNO'su emer."))
    REV = []                                                          # (düğüm, zaman) — üst malzeme görünür olur
    TH_SOS = None
    for k in SIRA:
        i = IS[k]; g = DOZ[k]
        if i["tip"] == "YAYICI":
            h = TH2.yayici(k, g)
            t = X.git(t, t + gecis(X.son, i["x"]), i["x"])
            ADIM.append((t - 1.5, k, "Tabla sos yayıcısının altına gelir: borunun iç ucu merkezde. %.0f g = %.1f ml · UNO Ø%.0f pistonu %.1f mm · tabla TAM 1 TUR (%.1f s, %.0f dev/dk) · katman %.2f mm · kama yarık %.1f→%.1f mm."
                         % (g, h["ml"], i["sil"], h["strok"], h["sure"], TH2.RPM_YAYICI, h["katman"], TH2.yarik_genisligi(k, 10.0), TH2.yarik_genisligi(k, 121.0))))
            VAL[k].git(t, t + TH2.VALF_SN, 1.0, "ss"); t += TH2.VALF_SN
            w = 6.0 * TH2.RPM_YAYICI
            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h0"); t += TH2.RAMPA_SN
            TH_SOS = (t, TH.son)
            TH.git(t, t + h["sure"], TH.son + 360.0, "l"); PIS[k].git(t, t + h["sure"], 0.0, "l")
            for j in range(6): REV.append(("URUN__sos_%d" % j, t + (j + 0.5) / 6.0 * h["sure"]))
            t += h["sure"]
            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h1"); t += TH2.RAMPA_SN + TH2.KESME_VALF_SN
            VAL[k].git(t, t + TH2.VALF_SN, 0.0, "ss")
        else:
            d = TH2.spiral(i, g); x0 = TH2.tabla_x(i, d["r_dis"])
            t = X.git(t, t + gecis(X.son, x0), x0)
            ADIM.append((t - 1.0, k, "%s: %.0f g · tabla %.0f dev/dk, %.2f tur spiral (%.1f s) · ağız r %.0f → %.0f · helezon %.0f dev/dk · katman %.1f mm."
                         % (i["ad"], g, TH2.RPM_NOKTA, d["tur"], d["sure"], d["r_dis"], d["r_ic"], i.get("rpm", 0), d["katman"])))
            w = 6.0 * TH2.RPM_NOKTA
            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h0"); t += TH2.RAMPA_SN
            ts = t
            X.f(t, t + d["sure"], lambda tt, ts=ts, d=d, i=i: TH2.tabla_x(i, TH2.r_yasa(d, tt - ts)))
            TH.git(t, t + d["sure"], TH.son + w * d["sure"], "l")
            HEL[k].git(t, t + d["sure"], HEL[k].son + i["rpm"] * 6.0 * d["sure"], "l"); KAR[k].git(t, t + d["sure"], KAR[k].son + 24.0 * d["sure"], "l")
            for j, rm in enumerate((110.0, 80.0, 50.0, 17.5)):
                rm = min(d["r_dis"], max(d["r_ic"], rm))
                REV.append(("URUN__%s_%d" % (k.lower(), j), ts + d["sure"] * (d["r_dis"] ** 2 - rm ** 2) / (d["r_dis"] ** 2 - d["r_ic"] ** 2)))
            t += d["sure"]
            tg = 15.0 / i["rpm"]
            HEL[k].git(t, t + tg, HEL[k].son - 90.0, "l"); TH.git(t, t + tg, TH.son + w * tg, "l"); t += tg
            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h1"); t += TH2.RAMPA_SN
    t = X.git(t, t + gecis(X.son, TH2.X_AKTARMA), TH2.X_AKTARMA)
    T_AKT = t
    ADIM.append((T_AKT - 0.5, "AKTARMA", "Tabla sağ uca gider, bıçak burunlu bant ürünü fırın bandına alır; tabla açıcının altına döner."))
    X.git(T_AKT + 0.5, T_AKT + 0.5 + gecis(TH2.X_AKTARMA, TH2.X_PARK), TH2.X_PARK)
    T_F0, T_F1 = T_AKT + 0.5, T_AKT + 10.5
    BANT.git(T_AKT, T_F1, (3940.0 - (OX + TH2.X_AKTARMA)), "l")
    ADIM.append((T_F0, "FIRIN", "Konveyör fırın — animasyonda HIZLANDIRILMIŞ: gerçekte ~4 dk pişer, burada 10 s."))
    T0K = T_F1 - KS.Z_GELIS[0]
    ADIM += [(T0K + KS.Z_GELIS[0], "KESME", "K bandı ürünü fırın bandından alıp kesme merkezine getirir. Kafa iner, 6 dilim keser (bıçak bandın 0,5 mm üstünde durur). Pizzada sprey yok; pidede aynı kafadaki nozül tereyağı püskürtür."),
             (T0K + KS.Z_TASI[0], "ÇİT + İTİCİ", "Bant ürünü 200 mm taşır, 20° çit 36 mm içeri kaydırır (kutu ekseni); itici ürünün üstünden geri gelip arkasına iner."),
             (T0K + KS.Z_ITME[0], "KUTU", "İtici ürünü katlanmış kutuya sürer (1,6 s); ürün tabana düşer, kol + piston kapağı kapatıp bastırır."),
             (T0K + KC.Z_CATAL[0], "ROBOT → QR", "FR5 kutuyu tepsinin aralıklarından çatalla alır, QR teslim dolabına koyar.")]
    ROB.git(T0K + 5.0, T0K + 9.0, X_E + 260.0)
    QR_X = QRX[0] + 15.0 + 240.0; QR_DZ = (QRZ[0] + 220.0) - (KC.ZB + KC.CATAL_DIS + 200.0); QR_DY = 1215.0 - (KC.TEPSI + KC.T + 55.0)   # 1. sütun, 1210 gözü
    TAS = Iz(0.0); TAS.git(T0K + 17.5, T0K + 19.9, 1.0, "s2")
    ROB.git(T0K + 17.5, T0K + 19.9, QR_X); ROB.git(T0K + 20.5, T0K + 24.5, RX0)
    T_J = math.ceil(T0K + 25.5)
    GIZLE = T_J - 0.6
    TT = [i_ / FPS for i_ in range(int(round(T_J * FPS)) + 1)]
    te = lambda t: min(19.5, max(0.0, t - T0K))
    tk = lambda t: min(KS.DONGU, max(0.0, t - T0K))
    tas = lambda t: ((QR_X - (X_E + 260.0)) * TAS(t), QR_DY * TAS(t), QR_DZ * TAS(t))

    # ================= ÜRÜN (düğümler, ürün merkezine göre ağ) =================
    for k_, r_ in (("hamur", (0.93, 0.78, 0.52, 1.0)), ("sos", (0.74, 0.17, 0.10, 1.0)), ("kasar", (0.97, 0.87, 0.50, 1.0)),
                   ("sucuk", (0.55, 0.12, 0.10, 1.0)), ("kesik", (0.30, 0.18, 0.10, 1.0))):
        MALZEME["MU_URUN__" + k_] = dict(renk=r_, met=0.0, ruf=0.8)
    def ekle_u(ad, sh, mal):
        parcalar.append(("URUN__" + ad, TC_AG(sh if isinstance(sh, cq.Workplane) else cq.Workplane(obj=sh)), "MU_URUN__" + mal))
    def halka(r0, r1, y0, y1, a0=None, a1=None, n=48):
        if a0 is None:
            s_ = cq.Workplane("XZ", origin=(0, y0, 0)).circle(r1).extrude(-(y1 - y0))
            return s_.cut(cq.Workplane("XZ", origin=(0, y0 - 1, 0)).circle(r0).extrude(-(y1 - y0 + 2))) if r0 > 0 else s_
        dis = [(r1 * math.cos(math.radians(a0 + (a1 - a0) * j / n)), -r1 * math.sin(math.radians(a0 + (a1 - a0) * j / n))) for j in range(n + 1)]
        ic = [(r0 * math.cos(math.radians(a1 - (a1 - a0) * j / n)), -r0 * math.sin(math.radians(a1 - (a1 - a0) * j / n))) for j in range(n + 1)]
        return cq.Workplane("XZ", origin=(0, y0, 0)).polyline(dis + ic).close().extrude(-(y1 - y0))
    ekle_u("top", cq.Workplane(obj=cq.Solid.makeSphere(TOP_R, angleDegrees1=-90, angleDegrees2=90).scale(1.0)).val().transformGeometry(cq.Matrix([[1, 0, 0, 0], [0, TOP_K, 0, 0], [0, 0, 1, 0]])), "hamur")
    ekle_u("hamur", halka(0.0, 140.0, 0.0, 8.0), "hamur")
    th_s = TH_SOS[1]
    for j in range(6):
        ekle_u("sos_%d" % j, halka(10.0, 125.0, 8.0, 9.5, -th_s - 60.0 * (j + 1), -th_s - 60.0 * j, 24), "sos")
    for j, (r0, r1) in enumerate(((95.0, 125.0), (65.0, 95.0), (35.0, 65.0), (0.0, 35.0))):
        ekle_u("kasar_%d" % j, halka(r0, r1, 9.5, 14.5), "kasar")
    for j, (rr, n) in enumerate(((110.0, 18), (80.0, 13), (50.0, 8), (22.0, 3))):
        kup = None
        for m in range(n):
            a = 2 * math.pi * (m + 0.3 * j) / n
            b_ = cq.Workplane("XY").box(14, 14, 14).translate((rr * math.cos(a), 21.5, -rr * math.sin(a)))
            kup = b_ if kup is None else kup.union(b_)
        ekle_u("sucuk_%d" % j, kup, "sucuk")
    ks_ = None
    for a in (0.0, 60.0, 120.0):
        b_ = cq.Workplane("XY").box(270.0, 1.2, 2.0).translate((0, 15.0, 0)).rotate((0, 0, 0), (0, 1, 0), a)
        ks_ = b_ if ks_ is None else ks_.union(b_)
    ekle_u("kesik", ks_, "kesik")

    def urun_C(t):
        """ürün (hamur alt yüzü merkezi) hatta: tabla → aktarma → fırın → K → kutu → robot → QR"""
        if t < T_AKT:
            return (OX + X(t), OY + 108.0, ZT)
        if t < T_F0:
            u = (t - T_AKT) / (T_F0 - T_AKT); return (OX + TH2.X_AKTARMA + 60.0 * u, OY + 108.0 - 2.0 * u, ZT)
        if t < T_F1:
            u = (t - T_F0) / (T_F1 - T_F0); x0 = OX + TH2.X_AKTARMA + 60.0; return (x0 + (3940.0 - x0) * u, KS.FIRIN_BANDI, ZT)
        tK = t - T0K
        if tK < KC.Z_PIZZA[1]:
            x, y, z = KS.urun_merkez(max(0.0, tK)); return (X_K + x, y, z)
        p = KC.pizza_trs(te(t)); c = tas(t)
        return (X_E + KC.PIZZA_X0 + p[0] + c[0], KC.PLAKA_K + p[1] + c[1], KC.PIZZA_Z0 + p[2] + c[2])
    def qy(d): a = math.radians(d) / 2.0; return (0.0, math.sin(a), 0.0, math.cos(a))
    def qax(ax, d):
        L = math.sqrt(sum(c * c for c in ax)); a = math.radians(d) / 2.0; s_ = math.sin(a) / L
        return (ax[0] * s_, ax[1] * s_, ax[2] * s_, math.cos(a))
    def qrot(q, v):
        x, y, z, w = q; vx, vy, vz = v
        tx, ty, tz = 2 * (y * vz - z * vy), 2 * (z * vx - x * vz), 2 * (x * vy - y * vx)
        return (vx + w * tx + (y * tz - z * ty), vy + w * ty + (z * tx - x * tz), vz + w * tz + (x * ty - y * tx))
    def pivotlu(P, q, ek=(0.0, 0.0, 0.0)):
        r = qrot(q, P); return ((P[0] + ek[0] - r[0]) * MM, (P[1] + ek[1] - r[1]) * MM, (P[2] + ek[2] - r[2]) * MM)
    A = []; KONTROL = []
    def kanal(ad, fn, yol="translation"):
        A.append((ad, TT, [fn(t) for t in TT], yol))
    th_urun = lambda t: TH(min(t, T_AKT))
    vis = lambda a, b: (lambda t: (1.0,) * 3 if a <= t < b else (1e-4,) * 3)
    # top
    kanal("URUN__top", lambda t: (TOPX(t) * MM, (TOPY(t) - TOP_H * ACMA(t)) * MM, TOPZ(t) * MM))   # v47: açılırken alt yüzü diskte
    kanal("URUN__top", lambda t: (1e-4,) * 3 if t >= T_ACMA + 3.0 else (1 + 1.4 * ACMA(t), max(0.02, 1 - ACMA(t)), 1 + 1.4 * ACMA(t)), "scale")
    # hamur + üstü
    u_adlar = ["URUN__hamur"] + ["URUN__sos_%d" % j for j in range(6)] + ["URUN__kasar_%d" % j for j in range(4)] + ["URUN__sucuk_%d" % j for j in range(4)] + ["URUN__kesik"]
    rv = dict(REV)
    _UAG = {}
    for a_, m_, _x in parcalar:
        if a_.startswith("URUN__"): _UAG[a_] = m_
    for ad in u_adlar:
        kanal(ad, lambda t: tuple(c * MM for c in urun_C(t)))
        kanal(ad, lambda t: qy(th_urun(t)), "rotation")
        KONTROL.append((ad, lambda t: tuple(c * MM for c in urun_C(t)), lambda t: qy(th_urun(t)), {"_": _UAG[ad]}))
    kanal("URUN__hamur", lambda t: ((0.18 + 0.82 * ACMA(t)), 1.0, (0.18 + 0.82 * ACMA(t))) if T_ACMA <= t < GIZLE else (1e-4,) * 3, "scale")
    for ad in u_adlar[1:-1]:
        kanal(ad, vis(rv[ad], GIZLE), "scale")
    kanal("URUN__kesik", vis(T0K + KS.Z_KES[0] + 0.3, GIZLE), "scale")
    # TOPPING düğümleri — v46: DÖNEN parçalar KENDİ EKSENİNDE duran ayrı düğüm (ağ pivota göre yerel).
    # v45'te dünya ağına "dönüş + telafi ötelemesi" veriliyordu; kareler arasında öteleme doğrusal, dönüş yay boyunca
    # ara değerlendiği için parça ekseninden kayıyordu (ölçüldü: bant burun makarası 350 mm, koniler 96, sos valfi 94).
    P_T = (OX + TC.XC_TABLA, OY + 108.0, ZT); A_K = (OX + TC.XC_TABLA, OY + 116.0, ZT); ya = math.radians(17.82)
    ROL = {"BANT_BURUN": ((OX + 1815.0, OY + 106.0 - 1.5 - 10.0, 0.0), 10.0), "BANT_TAHRIK": ((OX + 2195.0, OY + 106.0 - 1.5 - 30.0, 0.0), 30.0)}
    DONER = {"TABLA": (P_T, lambda t: (P_T[0] + X(t) - TC.XC_TABLA, P_T[1], P_T[2]), lambda t: qy(TH(t)))}
    for g, yon in (("KONI_ON", 1.0), ("KONI_ARKA", -1.0)):
        ax = (0.0, math.sin(ya), yon * math.cos(ya))
        DONER[g] = (A_K, lambda t: (A_K[0], A_K[1] + 60.0 * KAFA(t), A_K[2]), lambda t, ax=ax, yon=yon: qax(ax, yon * KONI(t)))
    for g, (P_, r_) in ROL.items():
        DONER[g] = (P_, lambda t, P_=P_: P_, lambda t, r_=r_: qax((0, 0, 1), -math.degrees(BANT(t) / r_)))
    for k in VAL:
        g = "VALF_" + k; P_ = (OX + TU.GRUP[g][0], TU.GRUP[g][1], TU.GRUP[g][2])
        DONER[g] = (P_, lambda t, P_=P_: P_, lambda t, k=k: qax((1, 0, 0), -90.0 * VAL[k](t)))
    for k in HEL:
        for on_, Z_ in (("HELEZON_", HEL[k]), ("KARISTIRICI_", KAR[k])):
            g = on_ + k; P_ = (OX + TU.GRUP[g][0], TU.GRUP[g][1], 0.0)
            DONER[g] = (P_, lambda t, P_=P_: P_, lambda t, Z_=Z_: qax((0, 0, 1), -Z_(t)))
    OZEL_T, HARIC = [], set()
    for g, (P_, fT, fR) in DONER.items():
        ton = {}
        for a_, m_, mal_ in parcalar:
            if a_.startswith("TOPPING_MODUL__") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] == g:
                y_ = Mesh(); y_.P = [(q[0] - P_[0] * MM, q[1] - P_[1] * MM, q[2] - P_[2] * MM) for q in m_.P]; y_.N = list(m_.N); y_.I = list(m_.I)
                ton.setdefault(mal_, Mesh()).ekle(y_); HARIC.add(a_)
        if not ton:
            continue
        ad = "TOPPING_DONER__" + g
        OZEL_T.append(dict(ad=ad, ebeveyn=None, T=tuple(c * MM for c in fT(0.0)), tonlar=ton))
        kanal(ad, lambda t, fT=fT: tuple(c * MM for c in fT(t)))
        kanal(ad, fR, "rotation")
        KONTROL.append((ad, lambda t, fT=fT: tuple(c * MM for c in fT(t)), fR, ton))
    for ad in sorted({a_ for a_, _m, _x in parcalar if a_.startswith("TOPPING_MODUL__") and a_.count("__") == 2}):
        g = ad.rsplit("__", 1)[1]
        if g == "ARABA":
            kanal(ad, lambda t: ((X(t) - TC.XC_TABLA) * MM, 0.0, 0.0))
        elif g == "ACICI":
            kanal(ad, lambda t: (0.0, 60.0 * KAFA(t) * MM, 0.0))
        elif g.startswith("PISTON_") and g[7:] in PIS:
            k = g[7:]; kanal(ad, lambda t, k=k: (0.0, 0.0, -PIS[k](t) * MM))
    # B çekmecesi + robot
    for a_, _m, _x in parcalar:
        if a_.startswith("CEK_K1_hamur_3__") and a_.endswith("__CEKMECE"):
            kanal(a_, lambda t: (0.0, 0.0, CEK(t) * MM))
        elif a_.startswith("CEK_K1_hamur_3__") and a_.endswith("__CEKMECE_ARA"):
            kanal(a_, lambda t: (0.0, 0.0, CEK(t) * SC.RAY_ARA_ORAN * MM))
        elif a_ in ("ROBOT_1", "ROBOT_1_KOL"):
            kanal(a_, lambda t: ((ROB(t) - RX0) * MM, 0.0, 0.0))
    # K
    for a_, _m, _x in parcalar:
        if a_.startswith("K_") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] in ("KESICI", "ITICI_ARABA", "ITICI_KOL"):
            g_ = a_.rsplit("__", 1)[1]
            kanal(a_, lambda t, g_=g_: tuple(c * MM for c in KS.grup_trs(g_, tk(t))))
    # E (kutu modülü aynı saatte; kendi pizzası gizli — ürün kendi düğümüyle kutuya girer)
    _trs = {"ITICI": lambda t: (0.0, 0.0, KC.itici_dz(t)), "PISTON": lambda t: (0.0, KC.kafa(t) - KC.H_UST, 0.0),
            "KOPRU": lambda t: (0.0, KC.kopru_dy(t), 0.0), "KATLAYICI": lambda t: (0.0, KC.katlayici_dy(t), 0.0)}
    for a_, _m, _x in parcalar:
        if a_.startswith("E_") and a_.count("__") == 2:
            g_ = a_.rsplit("__", 1)[1]
            if g_ in _trs:
                kanal(a_, lambda t, f_=_trs[g_]: tuple(c * MM for c in f_(te(t))))
            elif g_ == "PIZZA":
                kanal(a_, lambda t: (1e-4,) * 3, "scale")
    for o in OZEL:
        g = o["ad"].split("__", 1)[1]
        if g == "KOL":
            kanal(o["ad"], lambda t: KC.quat("z", KC.kol_beta(te(t))), "rotation")
            KONTROL.append((o["ad"], lambda t, T_=o["T"]: T_, lambda t: KC.quat("z", KC.kol_beta(te(t))), o["tonlar"]))
        elif g == "PARMAK":
            kanal(o["ad"], lambda t: KC.quat("z", KC.parmak_psi(te(t))), "rotation")
            KONTROL.append((o["ad"], lambda t, T_=o["T"]: T_, lambda t: KC.quat("z", KC.parmak_psi(te(t))), o["tonlar"]))
        elif g == "B_ROOT":
            T0 = o["T"]
            kanal(o["ad"], lambda t, T0=T0: tuple(T0[j] + (KC.blank_acilar(te(t))[0][j] + tas(t)[j]) * MM for j in range(3)))
            kanal(o["ad"], lambda t: (1e-4,) * 3 if t >= GIZLE else (1.0,) * 3, "scale")
        elif g.startswith("B_"):
            kanal(o["ad"], lambda t, g=g: KC.quat(KC.DUGUM[g][2], KC.blank_acilar(te(t))[1][g]), "rotation")
            KONTROL.append((o["ad"], lambda t, T_=o["T"]: T_, lambda t, g=g: KC.quat(KC.DUGUM[g][2], KC.blank_acilar(te(t))[1][g]), o["tonlar"]))
    ADIM.sort(key=lambda a: a[0])
    # ---- v46 · ÖZ-DENETİM: her dönen düğümün kareler arasında (glTF doğrusal öteleme + slerp) TAM kinematikten sapması ----
    import numpy as _np
    def _qm(q):
        x, y, z, w = q
        return _np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                          [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    def _slerp(a, b, u):
        a = _np.array(a, float); b = _np.array(b, float); d_ = float(_np.dot(a, b))
        if d_ < 0: b = -b; d_ = -d_
        if d_ > 0.99995: r_ = a + u * (b - a); return r_ / _np.linalg.norm(r_)
        th = math.acos(min(1.0, d_)); return (math.sin((1 - u) * th) * a + math.sin(u * th) * b) / math.sin(th)
    RAPOR = []
    for ad, fT, fR, ton in KONTROL:
        pts = []
        for m_ in ton.values():
            P_ = _np.array(m_.P, float); lo, hi = P_.min(0), P_.max(0)
            pts += [(x_, y_, z_) for x_ in (lo[0], hi[0]) for y_ in (lo[1], hi[1]) for z_ in (lo[2], hi[2])]
        pts = _np.array(pts); en, en_t = 0.0, 0.0
        for i in range(len(TT) - 1):
            t0, t1 = TT[i], TT[i + 1]; tm = 0.5 * (t0 + t1)
            qi = _slerp(fR(t0), fR(t1), 0.5); Ti = 0.5 * (_np.array(fT(t0)) + _np.array(fT(t1)))
            e = float(_np.max(_np.linalg.norm((pts @ _qm(qi).T + Ti) - (pts @ _qm(fR(tm)).T + _np.array(fT(tm))), axis=1)))
            if e > en: en, en_t = e, tm
        RAPOR.append((en / MM, en_t, ad))
    RAPOR.sort(key=lambda r: -r[0])
    return A, [dict(t=round(a[0], 2), ad=a[1], not_=a[2]) for a in ADIM], float(T_J), OZEL_T, HARIC, RAPOR
