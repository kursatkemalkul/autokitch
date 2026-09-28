# -*- coding: utf-8 -*-
"""hat_montaj_v65 → hat_montaj_v66 (28 Eyl 2026) — İKİ LAHMACUN BİR KUTUDA (Kemal: "iki lahmacun olmalı, kutuya girmeli").
Lahmacun animasyonu iki çevrim: 1. lahmacun kutuya girer, kutu KAPAĞI AÇIK bekler (E, te 10,4'te durur) → robot 2. topu alır (tabla açıcıya
döndükten sonra) → açıcı · harç · aktarma · fırın · K → 2. lahmacun ilkinin üstüne girer (+3 mm) → kutu kapanır → robot QR gözüne.
Yöntem: tek lahmacun çevrimi (yolculuk) örneklenir, kanallar zamanla birleştirilir:
  makine düğümleri (çekmece, top, TOPPING, itici, fırın bandı, K) iki çevrim (ikinci çevrim D kaydırmalı, dönüşler ilk çevrimin bitiş açısına eklenir) ·
  robot: 1. topu bırakınca bekler, D'de çekmeceye döner · E ve 1. ürün: te 10,4'te bekler, 2. çevrimde devam eder · QR yalnız 2. çevrimde ·
  2. ürün yeni düğümler URUN__L2_* (hamur · harç 6 · kesik; öteki siparişlerde gizli + durağan).
Çıktılar hat_v66. Tesisat + raf yükleri ayrı sürümü artık v67."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v65.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""v65 (28 Eyl 2026):',
      '"""v66 (28 Eyl 2026): İKİ LAHMACUN BİR KUTUDA — lahmacun siparişi iki çevrim (kutu açık bekler, 2. lahmacun ilkinin üstüne girer, sonra kapanır) · çıktılar hat_v66.' + NL +
      'v65 (28 Eyl 2026):')
degis('pafta="HAT v65 (28 Eyl) ·', 'pafta="HAT v66 (28 Eyl) · IKI LAHMACUN BIR KUTUDA (lahmacun siparisi iki cevrim, kutu acik bekler) · v65:')
degis('print("ALCAK HAT SOZLESMESI (v65 ·', 'print("ALCAK HAT SOZLESMESI (v66 ·')
for a_ in ("hat_v65.glb", "hat_v65.usdz", '"hat_v65"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v65", "v66"))

degis("QR_YOL = {}", "QR_YOL = {}" + NL +
      "YOL_ZAMAN = {}                                                                           # v66: yolculuk() son çevrimin zamanları (T0K, T_J, FPS)" + NL +
      "L2_ADLAR = [\"hamur\"] + [\"harc_%d\" % j for j in range(6)] + [\"kesik\"]                         # v66: 2. lahmacunun düğümleri (URUN__L2_*)")
degis("    return A, [dict(t=round(a[0], 2), ad=a[1], not_=a[2]) for a in ADIM], float(T_J), OZEL_T, HARIC, RAPOR",
      "    YOL_ZAMAN.clear(); YOL_ZAMAN.update(T0K=T0K, T_J=float(T_J), FPS=FPS)                         # v66" + NL +
      "    return A, [dict(t=round(a[0], 2), ad=a[1], not_=a[2]) for a in ADIM], float(T_J), OZEL_T, HARIC, RAPOR")
degis("        _A, _ADIM, _T, _OZ, _HAR, _SAP = yolculuk(parcalar, urun=_kod, cekmece=_cek, urun_ekle=(_i == 0))" + NL,
      "        _A, _ADIM, _T, _OZ, _HAR, _SAP = yolculuk(parcalar, urun=_kod, cekmece=_cek, urun_ekle=(_i == 0))" + NL +
      "        if _kod == \"lahmacun\": LAH_Z = dict(YOL_ZAMAN)                                   # v66" + NL)

ESKI_ASSERT = ("    assert len(set(tuple(sorted((k_[0], k_[3] if len(k_) > 3 else 'translation') for k_ in a_)) for _n, a_ in ANIM_SIP)) == 1, "
               "\"v65: siparis animasyonlarinin dugum kumesi ayni olmali\"" + NL)
YENI = r'''    # ---- v66 · İKİ LAHMACUN BİR KUTUDA ----
    for _ad in L2_ADLAR:                                                                  # 2. ürünün düğümleri: 1. ürünün ağları, ayrı düğüm
        _src = [x_ for x_ in parcalar if x_[0] == "URUN__" + _ad][0]
        parcalar.append(("URUN__L2_" + _ad, _src[1], _src[2]))
    def iki_lahmacun(A, Z, TE_H=10.4):
        """tek lahmacun çevrimini (A, 30 fps) iki çevrime çevirir · TE_H: E'nin beklediği an (ürün düştü 10,35 · kafa hazırlığı 10,6)"""
        import numpy as _np, math as _m
        FPS, T0K, TJ = Z["FPS"], Z["T0K"], Z["T_J"]
        ch = [(a_[0], a_[3] if len(a_) > 3 else "translation", _np.asarray(a_[2], float)) for a_ in A]
        def qn(q):
            n_ = float(_np.linalg.norm(q)); return q / n_ if n_ > 0 else q
        def samp(V, t, yol):
            x_ = min(max(t, 0.0), (len(V) - 1) / FPS) * FPS; i_ = int(x_)
            if i_ >= len(V) - 1: return V[-1].copy()
            a0, a1 = V[i_], V[i_ + 1]
            if yol == "rotation" and float(_np.dot(a0, a1)) < 0: a1 = -a1
            v_ = a0 + (a1 - a0) * (x_ - i_)
            return qn(v_) if yol == "rotation" else v_
        def qmul(a, b):
            ax, ay, az, aw = a; bx, by, bz, bw = b
            return _np.array([aw * bx + ax * bw + ay * bz - az * by, aw * by - ax * bz + ay * bw + az * bx, aw * bz + ax * by - ay * bx + az * bw, aw * bw - ax * bx - ay * by - az * bz])
        def qinv(q): return _np.array([-q[0], -q[1], -q[2], q[3]])
        def fark(a, b, yol):
            return (1.0 - abs(float(_np.dot(qn(a), qn(b))))) > 1e-8 if yol == "rotation" else float(_np.max(_np.abs(a - b))) > 1e-7
        def aralik(V, yol):
            ix_ = [i_ for i_ in range(1, len(V)) if fark(V[i_], V[i_ - 1], yol)]
            return (None, None) if not ix_ else ((ix_[0] - 1) / FPS, ix_[-1] / FPS)
        def grup(ad):
            if ad.startswith("URUN__L2_"): return "urun2"
            if ad.startswith("URUN__") and ad != "URUN__top": return "urun1"
            if ad.startswith("ROBOT_1"): return "robot"
            if ad.startswith("QR_"): return "qr"
            if ad.startswith("E_"): return "e"
            return "mak"
        D, e_tabla, en = 0.0, 0.0, ("", 0.0)
        for ad, yol, V in ch:
            if grup(ad) != "mak": continue
            m_, e_ = aralik(V, yol)
            if m_ is None: continue
            if e_ - m_ > en[1]: en = (ad, e_ - m_)
            D = max(D, e_ - m_ + 0.5)
            if ad.startswith("TOPPING_DONER__TABLA") and yol == "translation": e_tabla = max(e_tabla, e_)
        D = max(D, e_tabla - 3.9)                                                         # 2. top diske inmeden (4,2 s) tabla açıcıya dönmüş olmalı
        D = _m.ceil(D * 2.0) / 2.0
        T2 = TJ + D; TT2 = [i_ / FPS for i_ in range(int(round(T2 * FPS)) + 1)]; T_H1 = T0K + TE_H
        print("   v66 · IKI LAHMACUN: ikinci cevrim D = %.1f sn (en uzun makine hareketi %s %.1f sn · tabla aciciya %.1f sn) · toplam %.1f sn · kutu %.1f–%.1f sn acik bekler"
              % (D, en[0], en[1], e_tabla, T2, T_H1, T_H1 + D))
        yeni, uyari = [], []
        for ad, yol, V in ch:
            g_ = grup(ad); out = []
            if g_ == "mak":
                m_, e_ = aralik(V, yol)
                if m_ is None:
                    out = [V[0]] * len(TT2)
                else:
                    s_ = D + m_
                    if e_ > s_ + 1e-6: uyari.append("%s %s: 1. cevrim %.1f sn'de bitiyor, 2. cevrim %.1f sn'de basliyor" % (ad, yol, e_, s_))
                    q1 = samp(V, s_, yol); q0i = qinv(qn(V[0])) if yol == "rotation" else None
                    if yol != "rotation" and float(_np.max(_np.abs(q1 - samp(V, s_ - D, yol)))) > 1e-3:
                        uyari.append("%s %s: gecis aninda %.1f mm sicrama" % (ad, yol, 1000.0 * float(_np.max(_np.abs(q1 - samp(V, s_ - D, yol))))))
                    for t in TT2:
                        if t < s_: out.append(samp(V, t, yol))
                        elif yol == "rotation": out.append(qn(qmul(qmul(samp(V, t - D, yol), q0i), q1)))
                        else: out.append(samp(V, t - D, yol))
            elif g_ == "robot":
                t_b = 6.9
                for t in TT2:
                    if t < t_b: out.append(samp(V, t, yol))
                    elif t < D: out.append(samp(V, t_b, yol))
                    elif t - D < 3.0:
                        u_ = (t - D) / 3.0; u_ = u_ * u_ * (3.0 - 2.0 * u_)
                        out.append(samp(V, t_b, yol) + (samp(V, 3.0, yol) - samp(V, t_b, yol)) * u_)
                    else: out.append(samp(V, t - D, yol))
            elif g_ == "qr":
                out = [samp(V, max(0.0, t - D), yol) for t in TT2]
            elif g_ in ("e", "urun1"):
                out = [samp(V, t if t < T_H1 else (T_H1 if t < T_H1 + D else t - D), yol) for t in TT2]
            else:
                continue
            yeni.append((ad, TT2, [tuple(float(c) for c in v_) for v_ in out], yol))
        src = {(ad, yol): V for ad, yol, V in ch}
        for l2 in L2_ADLAR:
            for yol in ("translation", "rotation", "scale"):
                V = src[("URUN__" + l2, yol)]; out = []
                for t in TT2:
                    if t < D:
                        out.append(_np.array([1e-4] * 3) if yol == "scale" else V[0])
                    else:
                        v_ = samp(V, t - D, yol).copy()
                        if yol == "translation" and t - D >= T_H1 - 2.0: v_[1] += 0.003     # 2. lahmacun kutuda 1.'nin 3 mm üstünde
                        out.append(v_)
                yeni.append(("URUN__L2_" + l2, TT2, [tuple(float(c) for c in v_) for v_ in out], yol))
        print("   v66 · IKI LAHMACUN uyari %d%s" % (len(uyari), (": " + " | ".join(uyari[:6])) if uyari else ""))
        assert not [u_ for u_ in uyari if "basliyor" in u_], "v66: iki cevrim ust uste biniyor: %s" % uyari[:3]
        return yeni, D, T2
    def iki_adim(adim, D):
        a1, a2 = [], []
        for a in adim:
            if a["ad"] in ("ROBOT → QR", "QR DOLABI"):
                a2.append(dict(t=round(a["t"] + D, 2), ad=a["ad"], not_=a["not_"])); continue
            n1 = n2 = a["not_"]
            if a["ad"] == "KUTU":
                n1 = "1. lahmacun katlanmış kutuya girer; kutunun kapağı AÇIK kalır, kutu makinesi 2. lahmacunu bekler."
                n2 = "2. lahmacun ilkinin üstüne girer; kol + piston kapağı kapatıp bastırır. Kutuda 2 lahmacun."
            if a["ad"] == "ÇEKMECE":
                n2 = "Robot 2. lahmacun topunu aynı çekmeceden alır (tabla açıcıya dönmüş)."
            a1.append(dict(t=a["t"], ad=a["ad"] + " (1)", not_=n1)); a2.append(dict(t=round(a["t"] + D, 2), ad=a["ad"] + " (2)", not_=n2))
        return sorted(a1 + a2, key=lambda x_: x_["t"])
    for _n, (_nm, _A) in enumerate(ANIM_SIP):
        if _nm == "siparis_lahmacun":
            _A2, _D, _T2 = iki_lahmacun(_A, LAH_Z)
            ANIM_SIP[_n] = (_nm, _A2)
            _sd = [s_ for s_ in SIP_DURUM if s_["kod"] == "lahmacun"][0]
            _sd["adim"] = iki_adim(_sd["adim"], _D); _sd["sure"] = _T2; _sd["ad"] = "Lahmacun (2 adet)"
        else:
            _TT = _A[0][1]
            _h0 = [a_ for a_ in _A if a_[0] == "URUN__hamur" and (a_[3] if len(a_) > 3 else "translation") == "translation"][0][2][0]
            for _ad in L2_ADLAR:
                _A.append(("URUN__L2_" + _ad, _TT, [_h0] * len(_TT), "translation"))
                _A.append(("URUN__L2_" + _ad, _TT, [(0.0, 0.0, 0.0, 1.0)] * len(_TT), "rotation"))
                _A.append(("URUN__L2_" + _ad, _TT, [(1e-4,) * 3] * len(_TT), "scale"))
'''
degis(ESKI_ASSERT, YENI + ESKI_ASSERT)
compile(s, "hat_montaj_v66.py", "exec")
io.open(os.path.join(U, "hat_montaj_v66.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v66.py yazildi · %d satir" % s.count(NL))
