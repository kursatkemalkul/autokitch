# -*- coding: utf-8 -*-
"""yolculuk_v45 → v46: dönen TOPPING parçaları pivot-yerel düğüm · 30 kare/s · öz-denetim (kareler arası sapma)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "yolculuk_v45.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)


d("    FPS = 15.0\n", "    FPS = 30.0                                                        # v46: hızlı dönen makaralar karede ≤ 31°\n")
a0 = s.index("    # TOPPING düğümleri\n"); a1 = s.index("    # B çekmecesi + robot\n")
YENI = '''    # TOPPING düğümleri — v46: DÖNEN parçalar KENDİ EKSENİNDE duran ayrı düğüm (ağ pivota göre yerel).
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
'''
s = s[:a0] + YENI + s[a1:]
d('    A = []\n    def kanal(ad, fn, yol="translation"):\n', '    A = []; KONTROL = []\n    def kanal(ad, fn, yol="translation"):\n')
d('''    for ad in u_adlar:
        kanal(ad, lambda t: tuple(c * MM for c in urun_C(t)))
        kanal(ad, lambda t: qy(th_urun(t)), "rotation")''', '''    _UAG = {}
    for a_, m_, _x in parcalar:
        if a_.startswith("URUN__"): _UAG[a_] = m_
    for ad in u_adlar:
        kanal(ad, lambda t: tuple(c * MM for c in urun_C(t)))
        kanal(ad, lambda t: qy(th_urun(t)), "rotation")
        KONTROL.append((ad, lambda t: tuple(c * MM for c in urun_C(t)), lambda t: qy(th_urun(t)), {"_": _UAG[ad]}))''')
d('''        if g == "KOL": kanal(o["ad"], lambda t: KC.quat("z", KC.kol_beta(te(t))), "rotation")
        elif g == "PARMAK": kanal(o["ad"], lambda t: KC.quat("z", KC.parmak_psi(te(t))), "rotation")''', '''        if g == "KOL":
            kanal(o["ad"], lambda t: KC.quat("z", KC.kol_beta(te(t))), "rotation")
            KONTROL.append((o["ad"], lambda t, T_=o["T"]: T_, lambda t: KC.quat("z", KC.kol_beta(te(t))), o["tonlar"]))
        elif g == "PARMAK":
            kanal(o["ad"], lambda t: KC.quat("z", KC.parmak_psi(te(t))), "rotation")
            KONTROL.append((o["ad"], lambda t, T_=o["T"]: T_, lambda t: KC.quat("z", KC.parmak_psi(te(t))), o["tonlar"]))''')
d('''        elif g.startswith("B_"):
            kanal(o["ad"], lambda t, g=g: KC.quat(KC.DUGUM[g][2], KC.blank_acilar(te(t))[1][g]), "rotation")''', '''        elif g.startswith("B_"):
            kanal(o["ad"], lambda t, g=g: KC.quat(KC.DUGUM[g][2], KC.blank_acilar(te(t))[1][g]), "rotation")
            KONTROL.append((o["ad"], lambda t, T_=o["T"]: T_, lambda t, g=g: KC.quat(KC.DUGUM[g][2], KC.blank_acilar(te(t))[1][g]), o["tonlar"]))''')
d('''    ADIM.sort(key=lambda a: a[0])
    return A, [dict(t=round(a[0], 2), ad=a[1], not_=a[2]) for a in ADIM], float(T_J)''', '''    ADIM.sort(key=lambda a: a[0])
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
    return A, [dict(t=round(a[0], 2), ad=a[1], not_=a[2]) for a in ADIM], float(T_J), OZEL_T, HARIC, RAPOR''')
io.open(os.path.join(U, "yolculuk_v46.py"), "w", encoding="utf-8").write(s)
print("yolculuk_v46.py yazildi")
