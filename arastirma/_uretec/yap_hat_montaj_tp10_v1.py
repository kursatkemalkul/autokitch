# -*- coding: utf-8 -*-
"""hat_montaj_v47 → hat_montaj_tp10_v1 · AYRI SÜRÜM (Kemal 26 Eyl: "ayrı versiyon olarak modelle, adapte et bizim 3D'ye ama
istemezsem geri alınacak şekilde"). Ana makine (hat_v47 · modul_* · durum.json) DEĞİŞMEZ; bu üreteç yalnız
hat_tp10_v1.glb/usdz · modul_D_tp10_v1.glb/usdz · durum_tp10_v1.json yazar. Geri almak = sayfadaki kartı kaldırmak.

UYARLAMA (yalnız bu sürümde):
  F  · özel fırın kutuları (D_FIRIN_GOVDE · D_HAZNE · D_BANT) → Sveba Dahlen TP10 (firin_tp10_cad_v1) · taban dolabı 1060 → 956 ·
       pizza kutusu yedeği 553 → 505 · davlumbaz 1483'ten · giriş bandı + 2 çit + 2 destek sacı + arka sac (bizim)
  C  · TOPPING'in 420 mm'lik aktarma bandı çıkar (yerine 70 mm giriş bandı) · X motoru kaidesinin sağ üst köşesi pahlanır (TP10 rulo sarımı)
  K  · bant yan levhaları 10 → 18'den başlar (TP10 bandı K'ye 14 girer) · itici motoru eksenin sağ ucuna (TP10 sağ uç kutusu) ·
       sol sacta ürün penceresi −480'e kadar + uç kutusu cebi
"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v47.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


degis('"""v47 (26 Eyl 2026):', '"""TP10 SÜRÜMÜ v1 (26 Eyl 2026) · AYRI SÜRÜM — ana makine v47 aynen durur. F = Sveba Dahlen TP10 (gerçek katalog fırını) +\n'
      '  uyarlama parçaları (firin_tp10_cad_v1) · TOPPING aktarma bandı yerine giriş bandı · K bant girişi + itici motoru yer değiştirir.\n'
      '  Çıktı: hat_tp10_v1.glb/usdz · modul_D_tp10_v1 · durum_tp10_v1.json (hat_v47 ve modul_* dosyalarına DOKUNMAZ).\n'
      'v47 (26 Eyl 2026):')
# ---- FT (TOPPING malzemeleri yazıldıktan SONRA: TOPPING'in renkleri v47 ile aynı kalsın) ----
degis('''for _k, (_r, _m, _ru, _say) in TU.M.items():
    MALZEME.setdefault(_k, dict(renk=_r, met=_m, ruf=_ru, saydam=_say))
''', '''for _k, (_r, _m, _ru, _say) in TU.M.items():
    MALZEME.setdefault(_k, dict(renk=_r, met=_m, ruf=_ru, saydam=_say))
import firin_tp10_cad_v1 as FT                                                          # TP10 SÜRÜMÜ: gerçek katalog fırını + uyarlama parçaları
AKTARMA_TP10 = ("bant_burun_silindiri", "bant_tahrik_silindiri", "bant", "bant_tasiyici_saci", "bant_yan_saci_0", "bant_yan_saci_1", "bant_motoru", "bant_ayagi")
KAIDE_PAH = cq.Workplane("XY").box(40.0, 28.0, 15.0, centered=False).translate((2560.0, 1112.0, -400.0)).val()   # X motoru kaidesi sağ üst köşe (TP10 rulo sarımı)
''')
# ---- F · taban dolabı 956 · içerik · davlumbaz · özel fırın kutuları çıkar · TP10 birimleri ----
degis('birim("D_TABAN_KABIN", "F taban dolabı 123–1060 · önde bulaşık',
      'birim("D_TABAN_KABIN", "F taban dolabı 123–956 (TP10 SÜRÜMÜ: fırın gövdesi bant 1166 için 956\'ya iner · istasyon tabanı kuralı 1060\'tan 104 aşağı) · önde bulaşık')
degis('"D", "KUTU", (X_D, X_D + W_D), (Y_ALT, H_B), (-DZ, 0.0), "kabin", "v44 alt kısım v3")',
      '"D", "KUTU", (X_D, X_D + W_D), (Y_ALT, FT.YG0), (-DZ, 0.0), "kabin", "v44 alt kısım v3 · TP10 sürümünde üstü 956")')
degis('(510.0, 656.0), (130.0, 1045.0), (-210.0, -20.0), False, "B\'nin K4 nişinden taşındı',
      '(510.0, 656.0), (130.0, 950.0), (-210.0, -20.0), False, "TP10 sürümü: üstü 950 · B\'nin K4 nişinden taşındı')
degis('("D_PIZZA_YEDEK", "Pizza kutusu yedeği · 553 kutu düz (804 × 404 × 885 + taban 15) · şarjör 567 + 553 = 1120 = 4 gün · önde", (666.0, 1470.0), (130.0, 1030.0),',
      '("D_PIZZA_YEDEK", "Pizza kutusu yedeği · TP10 SÜRÜMÜ: 505 kutu düz (804 × 404 × 808 + taban 15) · şarjör 567 + 505 = 1072 = 3,8 gün — 4 gün için 48 kutu eksik (KARAR)", (666.0, 1470.0), (130.0, 953.0),')
_d0 = s.index('birim("D_FIRIN_GOVDE",'); _d1 = s.index('birim("D_DAVLUMBAZ",')
s = s[:_d0] + s[_d1:]
degis('''birim("D_DAVLUMBAZ", "Egzoz davlumbazı · fan · yağ + karbon filtre · fırın kartı + SSR + kontaktör", "D", "KUTU", (X_D, X_D + W_D), (F_G1 + 10.0, H_MAK), (-DZ, 0.0), "kutu", "pafta v7")''',
      '''birim("D_DAVLUMBAZ", "Egzoz davlumbazı (bizim) · fan · yağ + karbon filtre · TP10 üstünden 1483'ten · komşu modüllere asılı (dikme yok)", "D", "KUTU", (X_D, X_D + W_D), (FT.YG1 + 10.0, H_MAK), (-DZ, 0.0), "kutu", "pafta v7 · TP10 sürümü")
FT.kur(ayak=False, plaka=False, uyarla=True)
for _k, _a in FT.BIRIMLER:
    _bb = [FT.dunya(_p).BoundingBox() for _p in FT.PARCALAR if _p["birim"] == _k]
    birim(_k, _a, "D", "GERCEK_FIRIN", (min(q.xmin for q in _bb), max(q.xmax for q in _bb)), (min(q.ymin for q in _bb), max(q.ymax for q in _bb)),
          (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", "firin_tp10_cad_v1.py", "hat/firin_tp10.html")''')
# ---- K · bant girişi + itici motoru + sol sac ----
degis('''import kesme_cad_v1 as KS
KS.modul()
''', '''import kesme_cad_v1 as KS
KS.modul()
# TP10 SÜRÜMÜ · K uyarlaması (yalnız bu sürüm): TP10 bandı K'ye 14 mm girer (x 4014), sağ uç kutusu arkada 64 mm (z −493…−730)
K_UYARLAMA = []
for _p in KS.PARCALAR:
    if _p["ad"].startswith("bant_yan_levhasi_"):
        _p["wp"] = _p["wp"].cut(KS.kut(-5.0, 18.0, 1000.0, 1300.0, -500.0, 5.0)); K_UYARLAMA.append(_p["ad"] + " · 10 → 18'den başlar")
    elif _p["ad"].startswith("itici_motoru"):
        _p["wp"] = _p["wp"].translate((KS.EKSEN_X[1] - KS.EKSEN_X[0] - 55.0, 0.0, 0.0)); K_UYARLAMA.append(_p["ad"] + " · eksenin sağ ucuna (+%.0f)" % (KS.EKSEN_X[1] - KS.EKSEN_X[0] - 55.0))
    elif _p["ad"] == "sol_sac_urun_girisi":
        _p["wp"] = _p["wp"].cut(KS.kut(-1.0, KS.SAC + 1.0, 1100.0, 1240.0, -485.0, -415.0)).cut(KS.kut(-1.0, KS.SAC + 1.0, FT.YG0 + FT.UC_Y[0] - 3.0, FT.YG0 + FT.UC_Y[1] + 3.0, FT.UC_Z[1] - 3.0, FT.UC_Z[0] + 3.0))
        K_UYARLAMA.append("sol sac · ürün penceresi z −485'e · uç kutusu cebi")
assert len(K_UYARLAMA) >= 4, K_UYARLAMA
''')
# ---- TOPPING: aktarma bandı çıkar · kaide pahı ----
degis('''            ps = [p for p in TC.PARCALAR if v1_kalir(p["ad"]) and p["ad"] not in KAPAK]
            ton = {}''', '''            ps = [p for p in TC.PARCALAR if v1_kalir(p["ad"]) and p["ad"] not in KAPAK and p["ad"] not in AKTARMA_TP10]   # TP10 SÜRÜMÜ: aktarma bandı yok
            ton = {}''')
degis('''                sh = p["wp"].val().translate(cq.Vector(b["x"][0] + _d[0], b["y"][0] + _d[1], _d[2]))
''', '''                sh = p["wp"].val().translate(cq.Vector(b["x"][0] + _d[0], b["y"][0] + _d[1], _d[2]))
                if p["ad"] == "x_motor_kaidesi": sh = sh.cut(KAIDE_PAH)                   # TP10 SÜRÜMÜ
''')
# ---- yeni birim türü: GERCEK_FIRIN ----
degis('''        elif b["durum"] == "GERCEK":
            V, ps = kaset_parcalari(b["kaynak"][:-3]); AG = AG or V''', '''        elif b["durum"] == "GERCEK_FIRIN":                                                   # TP10 SÜRÜMÜ
            ps = [p for p in FT.PARCALAR if p["birim"] == b["kod"]]
            ton = {}
            for p in ps:
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(cq.Workplane(obj=FT.dunya(p)), p["ad"].startswith("giris_bandi_motoru")))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(ps)
        elif b["durum"] == "GERCEK":
            V, ps = kaset_parcalari(b["kaynak"][:-3]); AG = AG or V''')
# ---- denetimler ----
degis('''    for k_ in ("A_KABIN", "TOPPING_MODUL", "D_FIRIN_GOVDE"):''', '''    for k_ in ("A_KABIN", "TOPPING_MODUL"):''')
degis('''    for k_ in ("B_KASA", "D_TABAN_KABIN"):
        assert abs(_bk[k_]["y"][1] - H_B) < 0.01, "%s ustu %.1f" % (k_, _bk[k_]["y"][1])''', '''    for k_ in ("B_KASA",):
        assert abs(_bk[k_]["y"][1] - H_B) < 0.01, "%s ustu %.1f" % (k_, _bk[k_]["y"][1])
    assert abs(_bk["D_TABAN_KABIN"]["y"][1] - FT.YG0) < 0.01, "TP10 surumu: F taban dolabi ustu %.1f" % _bk["D_TABAN_KABIN"]["y"][1]''')
degis('''        if p["ad"].startswith("_bom") or p["ad"] in KAPAK:
            continue
        bb = p["wp"].val().BoundingBox()''', '''        if p["ad"].startswith("_bom") or p["ad"] in KAPAK or p["ad"] in AKTARMA_TP10:
            continue
        bb = p["wp"].val().BoundingBox()''')
# ---- animasyon: yolculuk_tp10_v1 ----
_y47 = io.open(os.path.join(U, "yolculuk_v47.py"), encoding="utf-8").read()
_yt = io.open(os.path.join(U, "yolculuk_tp10_v1.py"), encoding="utf-8").read()
assert s.count(_y47) == 1, "hat_montaj_v47 icindeki yolculuk yolculuk_v47.py ile birebir degil"
s = s.replace(_y47, _yt)
degis('    print("ANA MONTAJ ANIMASYONU (v47):', '    print("ANA MONTAJ ANIMASYONU (TP10 SURUMU v1):')
degis('''    assert not _kotu, "TOPPING donen dugumu ekseninden kayiyor: %s" % _kotu[:3]
''', '''    assert not _kotu, "TOPPING donen dugumu ekseninden kayiyor: %s" % _kotu[:3]
    _kotu = [r for r in SAPMA if r[2].startswith("F_DONER__") and r[0] > 3.0]
    assert not _kotu, "TP10 / giris bandi rulosu ekseninden kayiyor: %s" % _kotu[:3]
''')
# ---- TP10 DENETİMİ (gerçek katı kesişimi) · çıktılardan ÖNCE ----
degis('''    # ---- çıktılar ----
''', '''    # ================= TP10 SÜRÜMÜ · DENETİM: gerçek katı kesişimi (mm³) + ürün yolu taraması =================
    def _hacim(a_, b_):
        try: return a_.intersect(b_).Volume()
        except Exception: return -1.0
    def _bbk(a_, b_):
        A_, B_ = a_.BoundingBox(), b_.BoundingBox()
        return A_.xmin < B_.xmax and B_.xmin < A_.xmax and A_.ymin < B_.ymax and B_.ymin < A_.ymax and A_.zmin < B_.zmax and B_.zmin < A_.zmax
    def _tek(wp):
        v = wp.vals() if hasattr(wp, "vals") else [wp]
        return v[0] if len(v) == 1 else cq.Compound.makeCompound([o for o in v if isinstance(o, cq.Shape)])
    _F = [(p["birim"] + ":" + p["ad"], FT.dunya(p)) for p in FT.PARCALAR]
    _DG = []
    TC.PARCALAR[:] = []; TC.modul()
    for p in TC.PARCALAR:
        if p["ad"].startswith("_bom") or p["ad"] in KAPAK or p["ad"] in AKTARMA_TP10 or not v1_kalir(p["ad"]):
            continue
        _d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
        sh = p["wp"].val().translate(cq.Vector(X_BC + _d[0], H_B + _d[1], _d[2]))
        if p["ad"] == "x_motor_kaidesi": sh = sh.cut(KAIDE_PAH)
        if sh.BoundingBox().xmax > 2440.0: _DG.append(("TOPPING:" + p["ad"], sh))
    _TABLA = [p for p in TC.PARCALAR if grup_modul(p["ad"]) == "TABLA"]
    for p in _TABLA:                                                                     # tabla AKTARMA KONUMUNDA (dinamik)
        _DG.append(("TOPPING(aktarmada):" + p["ad"], p["wp"].val().translate(cq.Vector(X_BC + TH.X_AKTARMA - TC.XC_TABLA, H_B, 0.0))))
    for q in TU.P:
        if q["ad"].startswith(V3_CIKAN): continue
        sh = q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))
        if sh.BoundingBox().xmax > 2440.0: _DG.append(("TOPPING2:" + q["ad"], sh))
    _KSH = []
    for p in KS.PARCALAR:
        if p["grup"] in K_HARIC_GRUP: continue
        sh = _tek(p["wp"]).translate(cq.Vector(X_K, 0.0, 0.0))
        _KSH.append(("K:" + p["ad"], sh))
        if sh.BoundingBox().xmin < 4160.0: _DG.append(("K:" + p["ad"], sh))
    _an = TU.boru(ANA_V44, 5.0); _an = _an.val() if hasattr(_an, "val") else _an
    _DG.append(("HAVA:ana_hat", _an.translate(cq.Vector(X_BC, 0.0, 0.0))))
    for b in B:
        if b["modul"] == "D" and b["durum"] in ("KUTU", "KATALOG") and not b["kod"].startswith("D_SUPURGELIK"):
            _DG.append(("D:" + b["kod"], kutu_kat(b).val()))
    _cak = []
    for a_, sa in _F:
        for c_, sc in _DG:
            if _bbk(sa, sc):
                v_ = _hacim(sa, sc)
                if v_ > 1.0 or v_ < 0: _cak.append((round(v_, 1), a_, c_))
    for i_, (a_, sa) in enumerate(_F):
        for c_, sc in _F[i_ + 1:]:
            if _bbk(sa, sc):
                v_ = _hacim(sa, sc)
                if v_ > 1.0 or v_ < 0: _cak.append((round(v_, 1), a_, c_))
    # K'de yeri değişen parçalar K'nin kendi parçalarına çarpıyor mu
    _TAS = [x_ for x_ in _KSH if x_[0].startswith(("K:itici_motoru", "K:bant_yan_levhasi_", "K:sol_sac"))]
    for a_, sa in _TAS:
        for c_, sc in _KSH:
            if c_ == a_ or c_.startswith(("K:itici_motoru",)) and a_.startswith("K:itici_motoru"): continue
            if KS._ist(a_[2:], c_[2:]): continue                                       # K'nin kendi izinli temasları (mil ↔ yan levha …)
            if _bbk(sa, sc):
                v_ = _hacim(sa, sc)
                if v_ > 1.0 or v_ < 0: _cak.append((round(v_, 1), a_, c_))
    print("TP10 CAKISMA (gercek kati kesisimi > 1 mm3 · TOPPING + tabla aktarmada + K + hava + F kutulari + kendi arasinda): %s"
          % ("TEMIZ" if not _cak else "%d BULGU" % len(_cak)))
    for x_ in sorted(_cak, reverse=True)[:40]: print("   %10.1f mm3  %s  <->  %s" % x_)
    # ürün yolu: Ø299 × 28,5 ürün zarfı giriş bandı → TP10 → K girişi, 10 mm adımla (bant/sac üstüne temas hariç)
    _YOL = []
    _stat = [(a_, sa) for a_, sa in _F] + [(c_, sc) for c_, sc in _DG if c_.startswith(("K:", "TOPPING:"))]
    for xc, R_ in [(x_, 139.5) for x_ in range(2380, 4041, 10)] + [(x_, 149.5) for x_ in range(2600, 4041, 10)]:   # Ø280 gerçek ürün · Ø300 zarf (çit kuralı)
        zc = FT.urun_z(float(xc))
        cyl = cq.Solid.makeCylinder(R_, 28.0, cq.Vector(xc, FT.BANT_UST_HAT + 0.5, zc), cq.Vector(0, 1, 0))
        for a_, sa in _stat:
            if _bbk(cyl, sa):
                v_ = _hacim(cyl, sa)
                if v_ > 5.0: _YOL.append((xc, round(zc, 1), round(v_, 1), "Ø%.0f %s" % (2 * R_ + 1, a_)))
    print("TP10 URUN YOLU (O280 x 2380-4040 + O300 zarf x 2600-4040 · 28 yuksek · 10 mm adim · z = cit yolu): %s" % ("TEMIZ" if not _YOL else "%d BULGU" % len(_YOL)))
    for x_ in _YOL[:40]: print("   x %d  z %.1f  %.1f mm3  %s" % x_)
    print("K UYARLAMASI: " + " · ".join(K_UYARLAMA))
    TP10_OZET = ("gerçek katı kesişimi %s (%d TP10/uyarlama parçası × %d komşu parça) · ürün yolu %s (Ø280 167 konum + Ø300 145 konum)"
                 % ("TEMİZ" if not _cak else "%d BULGU" % len(_cak), len(_F), len(_DG), "TEMİZ" if not _YOL else "%d BULGU" % len(_YOL)))
    assert not _cak and not _YOL, "TP10 surumu: cakisma / urun yolu bulgusu var"
    print("TP10 YERLESIM: gövde x %.0f–%.0f · bant %.0f–%.0f (üst %.0f) · ısıtılan %.0f–%.0f · gövde y %.0f–%.0f · uç kutuları %.0f–%.0f ve %.0f–%.0f (arka z %.0f…%.0f)"
          % (FT.GOV_X[0], FT.GOV_X[1], FT.BANT_X[0], FT.BANT_X[1], FT.BANT_UST_HAT, FT.ODA_X[0], FT.ODA_X[1], FT.YG0, FT.YG1, FT.X0, FT.GOV_X[0], FT.GOV_X[1], FT.X0 + FT.L_TOP, FT.UC_Z[0], FT.UC_Z[1]))

    # ---- çıktılar ----
''')
# ---- çıktılar: yalnız TP10 dosyaları ----
degis('b1 = glb_yaz(os.path.join(OUT, "hat_v47.glb")', 'b1 = glb_yaz(os.path.join(OUT, "hat_tp10_v1.glb")')
degis('print("hat_v47.glb · %d dugum', 'print("hat_tp10_v1.glb · %d dugum')
degis('usdz_yaz([os.path.join(OUT, "hat_v47.usdz")], "hat_v47", _usd + E_USDZ, dokular)', 'usdz_yaz([os.path.join(OUT, "hat_tp10_v1.usdz")], "hat_tp10_v1", _usd + E_USDZ, dokular)')
degis('print("hat_v47.usdz · %.0f KB', 'print("hat_tp10_v1.usdz · %.0f KB')
degis('    for mk in ("A", "B", "C", "D", "K", "E", "-"):', '    for mk in ("D",):                                                              # TP10 SÜRÜMÜ: yalnız F (modul_* ana dosyalarına dokunmaz)')
degis('        dosya = "modul_%s" % hrf', '        dosya = "modul_%s_tp10_v1" % hrf')
degis('    with io.open(os.path.join(OUT, "durum.json"), "w", encoding="utf-8") as f:', '    with io.open(os.path.join(OUT, "durum_tp10_v1.json"), "w", encoding="utf-8") as f:')
degis('pafta="HAT_ATOSA_TABLALI v12 · v47 (on yuzden tasan parcalar iceri, animasyon v46 duzeltmesi) ·',
      'pafta="TP10 SURUMU v1 (ayri) · FIRIN_TP10 v2 · ana makine v47 + F = Sveba Dahlen TP10 + giris bandi + 2 cit · K bant girisi + itici motoru uyarlandi ·')
degis('print("durum.json yazildi', 'print("durum_tp10_v1.json yazildi')
degis('dosya=MODUL_DOSYA, birim=[', 'dosya=MODUL_DOSYA, tp10_denetim=TP10_OZET, birim=[')
assert "hat_v47.glb" not in s and '"durum.json"' not in s, "ana dosya adi kaldi"
io.open(os.path.join(U, "hat_montaj_tp10_v1.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_tp10_v1.py yazildi")
