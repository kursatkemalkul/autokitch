# -*- coding: utf-8 -*-
"""hat_montaj_v64 → hat_montaj_v65 (28 Eyl 2026) — SİPARİŞ ANİMASYONLARI (Kemal: "simülasyon tuşu olmasın, hepsi simülasyon olsun; ana istasyonda
kaşarlı sipariş veriyorum o gözüksün, bilmem ne sipariş veriyorum o gözüksün — çekmece açılıyor … dolaba kutu koyana kadar").
  · yolculuk(parcalar, urun, cekmece, urun_ekle): tarif topping_v2_hesap_v1.RECETE[urun] · çekmece siparişe göre (pide/pizza K3 hamur · lahmacun K2 lahm_6)
  · 6 sipariş = GLB'de 6 animasyon (siparis_kasarli … siparis_pizza); aynı düğüm kümesi her animasyonda (siparişte olmayan üst malzeme gizli + durağan)
  · yeni ürün katmanları: harç (yayıcı, 6 dilim) · kıyma (4 halka) · kuşbaşı (küp) — renkleri MU_URUN__*
  · kare sadeleştirme (_sade): öteleme 0,2 mm · ölçek 1e-3 (Ramer–Douglas–Peucker) · dönüş yalnız durağan aralıklar → dosya boyu
  · durum.json: animasyon (ilk sipariş, geriye uyum) + siparis [kod, ad, sure, adim]
Çıktılar hat_v65. Tesisat + raf yükleri ayrı sürümü artık v66."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v64.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


# ---------------- başlık / metin / çıktılar ----------------
degis('"""v64 (28 Eyl 2026):',
      '"""v65 (28 Eyl 2026): SİPARİŞ ANİMASYONLARI — ana montaj GLB\'sinde 6 sipariş (kaşarlı · kıymalı · kuşbaşılı · sucuklu pide · lahmacun · pizza),' + NL +
      '  her biri çekmeceden QR gözüne tam yolculuk (Kemal: "simülasyon tuşu olmasın, ana istasyonda sipariş verince gözüksün") · kare sadeleştirme · çıktılar hat_v65.' + NL +
      'v64 (28 Eyl 2026):')
degis('pafta="HAT v64 (28 Eyl) ·', 'pafta="HAT v65 (28 Eyl) · SIPARIS ANIMASYONLARI (6 siparis: kasarli · kiymali · kusbasili · sucuklu pide · lahmacun · pizza; cekmeceden QR gozune) · v64:')
degis('print("ALCAK HAT SOZLESMESI (v64 ·', 'print("ALCAK HAT SOZLESMESI (v65 ·')
for a_ in ("hat_v64.glb", "hat_v64.usdz", '"hat_v64"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v64", "v65"))

# ---------------- sipariş listesi (modül düzeyi) ----------------
degis('YOL_CEKMECE = "CEK_K3_hamur_3"',
      'SIPARIS = [("kasarli", "Kaşarlı pide", "CEK_K3_hamur_3"), ("kiymali", "Kıymalı pide", "CEK_K3_hamur_3"), ("kusbasili", "Kuşbaşılı pide", "CEK_K3_hamur_3"),' + NL +
      '           ("sucuklu", "Sucuklu pide", "CEK_K3_hamur_3"), ("lahmacun", "Lahmacun", "CEK_K2_lahm_6"), ("pizza", "Pizza", "CEK_K3_hamur_3")]   # v65: kod (RECETE) · ad · çekmece' + NL +
      'CEK_TUM = sorted(set(c_ for _k, _a, c_ in SIPARIS))' + NL +
      'YOL_CEKMECE = "CEK_K3_hamur_3"')

# ---------------- kare sadeleştirme + çok animasyonlu GLB ----------------
degis("def glb_yaz(yol, parcalar, dokular, ozel=None, anim=True, liste=None):",
      "def _sade(T, V, yol):" + NL +
      '    """v65 · kare sadeleştirme: öteleme / ölçek Ramer–Douglas–Peucker (0,2 mm · 1e-3), dönüş yalnız durağan aralıklar (slerp yönü bozulmasın)"""' + NL +
      "    import numpy as _np" + NL +
      "    n = len(T)" + NL +
      "    if n <= 2: return list(T), [tuple(float(c) for c in v_) for v_ in V]" + NL +
      "    Va = _np.asarray(V, float)" + NL +
      "    if yol == 'rotation':" + NL +
      "        d_ = _np.max(_np.abs(_np.diff(Va, axis=0)), axis=1) > 1e-7" + NL +
      "        tut = _np.zeros(n, bool); tut[0] = tut[-1] = True; tut[1:] |= d_; tut[:-1] |= d_" + NL +
      "    else:" + NL +
      "        eps = 2e-4 if yol == 'translation' else 1e-3" + NL +
      "        Ta = _np.asarray(T, float); tut = _np.zeros(n, bool); tut[0] = tut[-1] = True; yig = [(0, n - 1)]" + NL +
      "        while yig:" + NL +
      "            a, b = yig.pop()" + NL +
      "            if b - a < 2: continue" + NL +
      "            u = (Ta[a + 1:b] - Ta[a]) / (Ta[b] - Ta[a])" + NL +
      "            e_ = _np.max(_np.abs(Va[a + 1:b] - (Va[a] + (Va[b] - Va[a]) * u[:, None])), axis=1)" + NL +
      "            k = int(_np.argmax(e_))" + NL +
      "            if e_[k] > eps:" + NL +
      "                m = a + 1 + k; tut[m] = True; yig.append((a, m)); yig.append((m, b))" + NL +
      "    ix = _np.nonzero(tut)[0]" + NL +
      "    return [float(T[i]) for i in ix], [tuple(float(c) for c in Va[i]) for i in ix]" + NL + NL + NL +
      "def glb_yaz(yol, parcalar, dokular, ozel=None, anim=True, liste=None, animler=None):")
i0 = s.index("    anim_sm, anim_ch = [], []                                                            # v37")
k_ = 'anim_ch.append({"sampler": len(anim_sm) - 1, "target": {"node": ad2node[ad_], "path": yol_}})'
assert s.count(k_) == 1
i1 = s.index(k_) + len(k_) + 1
YENI = NL.join([
    "    ANIMLER_ = []                                                                        # v65: birden çok animasyon (siparişler) · v37 çekmece · v38 kutu",
    "    _AL = animler if animler else [(\"hat_calisma\", ANIM if liste is None else liste)]",
    "    ad2node = {n[\"name\"]: i for i, n in enumerate(nodes)}",
    "    for _ai, (_anad, _A) in enumerate(_AL):",
    "        if not _A:",
    "            continue",
    "        anim_sm, anim_ch = [], []",
    "        for kayit in _A:",
    "            ad_, T, V = kayit[0], kayit[1], kayit[2]",
    "            yol_ = kayit[3] if len(kayit) > 3 else \"translation\"",
    "            if ad_ not in ad2node:",
    "                continue",
    "            if _ai == 0:",
    "                nodes[ad2node[ad_]][yol_] = [float(c) for c in V[0]]                       # v45: durağan duruş = ilk kare (v65: ilk animasyonun)",
    "            if not anim:                                                                  # v40: animasyonsuz yazım",
    "                continue",
    "            T, V = _sade(T, V, yol_)                                                       # v65: kare sadeleştirme",
    "            n_el = 4 if yol_ == \"rotation\" else 3",
    "            vi = gomu(struct.pack(\"<%df\" % len(T), *T))",
    "            accs.append({\"bufferView\": vi, \"componentType\": 5126, \"count\": len(T), \"type\": \"SCALAR\", \"min\": [min(T)], \"max\": [max(T)]})",
    "            vo = gomu(struct.pack(\"<%df\" % (n_el * len(V)), *[c for v_ in V for c in v_]))",
    "            accs.append({\"bufferView\": vo, \"componentType\": 5126, \"count\": len(V), \"type\": \"VEC4\" if n_el == 4 else \"VEC3\"})",
    "            anim_sm.append({\"input\": len(accs) - 2, \"output\": len(accs) - 1, \"interpolation\": \"LINEAR\"})",
    "            anim_ch.append({\"sampler\": len(anim_sm) - 1, \"target\": {\"node\": ad2node[ad_], \"path\": yol_}})",
    "        if anim_ch:",
    "            ANIMLER_.append({\"name\": _anad, \"samplers\": anim_sm, \"channels\": anim_ch})",
    ""])
s = s[:i0] + YENI + s[i1:]
degis('    if anim_ch:' + NL + '        g["animations"] = [{"name": "hat_calisma", "samplers": anim_sm, "channels": anim_ch}]',
      '    if ANIMLER_:' + NL + '        g["animations"] = ANIMLER_')

# ---------------- yolculuk: sipariş parametresi ----------------
degis("def yolculuk(parcalar):", "def yolculuk(parcalar, urun=\"pizza\", cekmece=None, urun_ekle=True):")
degis('    DOZ = TH2.RECETE["pizza"]["doz"]', '    DOZ = TH2.RECETE[urun]["doz"]                                    # v65: sipariş tarifi')
degis('    _cb = [b for b in B if b["kod"] == YOL_CEKMECE][0]', '    CEK_KOD = cekmece or YOL_CEKMECE                                    # v65: siparişin çekmecesi' + NL +
      '    _cb = [b for b in B if b["kod"] == CEK_KOD][0]')
degis('            ADIM.append((t - 1.5, k, "Tabla sos yayıcısının altına gelir:', '            ADIM.append((t - 1.5, k, "Tabla %s yayıcısının altına gelir:')
degis('                         % (g, h["ml"], i["sil"],', '                         % ({"SOS": "sos", "HARC": "harç"}.get(k, k.lower()), g, h["ml"], i["sil"],')
degis('            for j in range(6): REV.append(("URUN__sos_%d" % j,', '            for j in range(6): REV.append(("URUN__%s_%d" % (k.lower(), j),')
degis('("sucuk", (0.55, 0.12, 0.10, 1.0)), ("kesik", (0.30, 0.18, 0.10, 1.0))):',
      '("sucuk", (0.55, 0.12, 0.10, 1.0)), ("kesik", (0.30, 0.18, 0.10, 1.0)),' + NL +
      '                   ("harc", (0.60, 0.24, 0.15, 1.0)), ("kiyma", (0.42, 0.24, 0.16, 1.0)), ("kusbasi", (0.48, 0.27, 0.19, 1.0))):   # v65')
degis("    def ekle_u(ad, sh, mal):" + NL, "    def ekle_u(ad, sh, mal):" + NL + "        if not urun_ekle: return                                                      # v65: ürün ağları yalnız ilk siparişte" + NL)
degis("    th_s = TH_SOS[1]" + NL,
      "    th_s = 0.5 * 6.0 * TH2.RPM_YAYICI * TH2.RAMPA_SN                                  # v65: yayıcı hep ilk üst malzeme → tabla açısı siparişten bağımsız" + NL +
      "    assert TH_SOS is None or abs(TH_SOS[1] - th_s) < 1e-6, (TH_SOS, th_s)" + NL)
degis("    ks_ = None" + NL,
      "    for j in range(6):                                                                # v65: harç (lahmacun) · yayıcı dilimleri" + NL +
      "        ekle_u(\"harc_%d\" % j, halka(10.0, 125.0, 8.0, 10.5, -th_s - 60.0 * (j + 1), -th_s - 60.0 * j, 24), \"harc\")" + NL +
      "    for j, (r0, r1) in enumerate(((95.0, 125.0), (65.0, 95.0), (35.0, 65.0), (0.0, 35.0))):   # v65: kıyma halkaları" + NL +
      "        ekle_u(\"kiyma_%d\" % j, halka(r0, r1, 9.5, 12.5), \"kiyma\")" + NL +
      "    for j, (rr, n) in enumerate(((110.0, 22), (80.0, 16), (50.0, 10), (22.0, 4))):  # v65: kuşbaşı küpleri" + NL +
      "        kup = None" + NL +
      "        for m in range(n):" + NL +
      "            a = 2 * math.pi * (m + 0.4 * j) / n" + NL +
      "            b_ = cq.Workplane(\"XY\").box(12, 12, 12).translate((rr * math.cos(a), 15.5, -rr * math.sin(a)))" + NL +
      "            kup = b_ if kup is None else kup.union(b_)" + NL +
      "        ekle_u(\"kusbasi_%d\" % j, kup, \"kusbasi\")" + NL +
      "    ks_ = None" + NL)
degis('    u_adlar = ["URUN__hamur"] + ["URUN__sos_%d" % j for j in range(6)] + ["URUN__kasar_%d" % j for j in range(4)] + ["URUN__sucuk_%d" % j for j in range(4)] + ["URUN__kesik"]',
      '    u_adlar = (["URUN__hamur"] + ["URUN__sos_%d" % j for j in range(6)] + ["URUN__harc_%d" % j for j in range(6)] + ["URUN__kasar_%d" % j for j in range(4)]' + NL +
      '               + ["URUN__sucuk_%d" % j for j in range(4)] + ["URUN__kiyma_%d" % j for j in range(4)] + ["URUN__kusbasi_%d" % j for j in range(4)] + ["URUN__kesik"])   # v65')
degis("    for ad in u_adlar:" + NL +
      "        kanal(ad, lambda t: tuple(c * MM for c in urun_C(t)))" + NL +
      "        kanal(ad, lambda t: qy(th_urun(t)), \"rotation\")" + NL +
      "        KONTROL.append((ad, lambda t: tuple(c * MM for c in urun_C(t)), lambda t: qy(th_urun(t)), {\"_\": _UAG[ad]}))" + NL,
      "    for ad in u_adlar:" + NL +
      "        if ad in (\"URUN__hamur\", \"URUN__kesik\") or ad in rv:" + NL +
      "            kanal(ad, lambda t: tuple(c * MM for c in urun_C(t)))" + NL +
      "            kanal(ad, lambda t: qy(th_urun(t)), \"rotation\")" + NL +
      "            KONTROL.append((ad, lambda t: tuple(c * MM for c in urun_C(t)), lambda t: qy(th_urun(t)), {\"_\": _UAG[ad]}))" + NL +
      "        else:                                                                         # v65: bu siparişte olmayan üst malzeme · gizli + durağan" + NL +
      "            kanal(ad, lambda t: tuple(c * MM for c in urun_C(0.0)))" + NL +
      "            kanal(ad, lambda t: qy(0.0), \"rotation\")" + NL)
degis("        kanal(ad, vis(rv[ad], GIZLE), \"scale\")", "        kanal(ad, vis(rv[ad], GIZLE) if ad in rv else (lambda t: (1e-4,) * 3), \"scale\")")
degis('        if a_.startswith(YOL_CEKMECE + "__") and a_.endswith("__CEKMECE"):', '        if a_.startswith(CEK_KOD + "__") and a_.endswith("__CEKMECE"):')
degis('        elif a_.startswith(YOL_CEKMECE + "__") and a_.endswith("__CEKMECE_ARA"):' + NL +
      '            kanal(a_, lambda t: (0.0, 0.0, CEK(t) * SC.RAY_ARA_ORAN * MM))' + NL,
      '        elif a_.startswith(CEK_KOD + "__") and a_.endswith("__CEKMECE_ARA"):' + NL +
      '            kanal(a_, lambda t: (0.0, 0.0, CEK(t) * SC.RAY_ARA_ORAN * MM))' + NL +
      '        elif a_.split("__")[0] in CEK_TUM and a_.endswith(("__CEKMECE", "__CEKMECE_ARA")):   # v65: öbür siparişlerin çekmecesi bu animasyonda kapalı' + NL +
      '            kanal(a_, lambda t: (0.0, 0.0, 0.0))' + NL)
degis("    ADIM.sort(key=lambda a: a[0])" + NL,
      "    if urun == \"lahmacun\":                                                            # v65: lahmacun metinleri" + NL +
      "        ADIM = [(a[0], a[1], a[2].replace(\"hamur çekmecesi\", \"lahmacun çekmecesi (K2)\")) if a[1] == \"ÇEKMECE\" else" + NL +
      "                (a[0], a[1], a[2] + \" Lahmacunda kutu 2. lahmacunu bekler; animasyonda tek lahmacun gösteriliyor.\") if a[1] == \"KUTU\" else a for a in ADIM]" + NL +
      "    ADIM.sort(key=lambda a: a[0])" + NL)

# ---------------- çağrı: 6 sipariş ----------------
degis("    ANIM_HAT, ADIM_HAT, T_J, OZEL_T, HARIC_T, SAPMA = yolculuk(parcalar)" + NL,
      "    ANIM_SIP, SIP_DURUM = [], []                                                       # v65: sipariş animasyonları" + NL +
      "    for _i, (_kod, _ad, _cek) in enumerate(SIPARIS):" + NL +
      "        _A, _ADIM, _T, _OZ, _HAR, _SAP = yolculuk(parcalar, urun=_kod, cekmece=_cek, urun_ekle=(_i == 0))" + NL +
      "        if _i == 0:" + NL +
      "            ANIM_HAT, ADIM_HAT, T_J, OZEL_T, HARIC_T, SAPMA = _A, _ADIM, _T, _OZ, _HAR, list(_SAP)" + NL +
      "        else:" + NL +
      "            assert [o[\"ad\"] for o in _OZ] == [o[\"ad\"] for o in OZEL_T] and set(_HAR) == set(HARIC_T), \"v65: siparisler arasinda donen dugumler farkli\"" + NL +
      "            SAPMA = sorted(SAPMA + list(_SAP), key=lambda r: -r[0])" + NL +
      "        ANIM_SIP.append((\"siparis_\" + _kod, _A)); SIP_DURUM.append(dict(kod=_kod, ad=_ad, sure=_T, adim=_ADIM))" + NL +
      "        print(\"   v65 · SIPARIS %-10s %5.1f sn · %4d kanal · %2d adim · cekmece %s\" % (_kod, _T, len(_A), len(_ADIM), _cek))" + NL +
      "    assert len(set(tuple(sorted((k_[0], k_[3] if len(k_) > 3 else 'translation') for k_ in a_)) for _n, a_ in ANIM_SIP)) == 1, \"v65: siparis animasyonlarinin dugum kumesi ayni olmali\"" + NL)
degis('ozel=OZEL + OZEL_T, liste=ANIM_HAT)', 'ozel=OZEL + OZEL_T, animler=ANIM_SIP)')
degis("animasyon=dict(sure=T_J, adim=ADIM_HAT),", "animasyon=dict(sure=T_J, adim=ADIM_HAT), siparis=SIP_DURUM,")

# ---------------- v65b · UNO nokta ağzı (kıyma / kuşbaşı): helezon değil piston + valf ----------------
degis('· ağız r %.0f → %.0f · helezon %.0f dev/dk · katman %.1f mm."', '· ağız r %.0f → %.0f · %s · katman %.1f mm."')
degis('d["r_dis"], d["r_ic"], i.get("rpm", 0), d["katman"])))',
      'd["r_dis"], d["r_ic"], ("helezon %.0f dev/dk" % i["rpm"]) if i.get("rpm") else ("UNO Ø%.0f pistonu · nokta ağzı" % i["sil"]), d["katman"])))')
degis('            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h0"); t += TH2.RAMPA_SN' + NL + '            ts = t' + NL,
      '            if k not in HEL: VAL[k].git(t, t + TH2.RAMPA_SN, 1.0, "ss")                        # v65b: UNO nokta ağzı valfi açılır' + NL +
      '            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h0"); t += TH2.RAMPA_SN' + NL + '            ts = t' + NL)
degis('            HEL[k].git(t, t + d["sure"], HEL[k].son + i["rpm"] * 6.0 * d["sure"], "l"); KAR[k].git(t, t + d["sure"], KAR[k].son + 24.0 * d["sure"], "l")' + NL,
      '            if k in HEL:' + NL +
      '                HEL[k].git(t, t + d["sure"], HEL[k].son + i["rpm"] * 6.0 * d["sure"], "l"); KAR[k].git(t, t + d["sure"], KAR[k].son + 24.0 * d["sure"], "l")' + NL +
      '            else:                                                                     # v65b: UNO pistonu dozu spiral boyunca basar' + NL +
      '                PIS[k].git(t, t + d["sure"], 0.0, "l")' + NL)
degis('            tg = 15.0 / i["rpm"]' + NL + '            HEL[k].git(t, t + tg, HEL[k].son - 90.0, "l"); TH.git(t, t + tg, TH.son + w * tg, "l"); t += tg' + NL,
      '            if k in HEL:' + NL +
      '                tg = 15.0 / i["rpm"]' + NL +
      '                HEL[k].git(t, t + tg, HEL[k].son - 90.0, "l"); TH.git(t, t + tg, TH.son + w * tg, "l"); t += tg' + NL +
      '            else:' + NL +
      '                VAL[k].git(t, t + TH2.VALF_SN, 0.0, "ss")                                # v65b: valf kapanır' + NL)

compile(s, "hat_montaj_v65.py", "exec")
io.open(os.path.join(U, "hat_montaj_v65.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v65.py yazildi · %d satir" % s.count(NL))
