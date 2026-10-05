# -*- coding: utf-8 -*-
"""hat_montaj_v47 → hat_montaj_tp10_v2 · AYRI SÜRÜM v2 (Kemal 26 Eyl akşam: "gerçek fırının sadece önünü arkasını istediğimiz ölçüye uzat,
bant boş olmasın önünde arkada, ona göre yeniden düzenle, son bir kontrol yap"). Ana makine (hat_v47 · modul_* · durum.json) DEĞİŞMEZ;
bu üreteç yalnız hat_tp10_v2.glb/usdz · modul_D_tp10_v2.glb/usdz · durum_tp10_v2.json yazar. Geri almak = sayfadaki kartı kaldırmak.

UYARLAMA (yalnız bu sürümde):
  F  · özel fırın kutuları (D_FIRIN_GOVDE · D_HAZNE · D_BANT) → TP10 kesitli, gövdesi 1500'e uzatılmış fırın (firin_tp10_cad_v2) · taban dolabı 1060 → 956 ·
       pizza kutusu yedeği 553 → 505 · davlumbaz 1483'ten · giriş bandı (ön odada) + çıkış ölü plakası + K giriş çiti + arka sac (bizim)
  C  · TOPPING'in 420 mm'lik aktarma bandı çıkar · X motoru kaidesinin sağ üst köşesi pahlanır · çıkış yarığı çerçevesi genişler (−417…−13) ve
       alt çıtası 1155'in altına iner (tabla 1157 + disk 1168 aktarmada 2507'ye kadar girer → v47'deki tabla ↔ çerçeve çakışması da kalkar)
  K  · parça DEĞİŞMEZ (v1'deki bant levhası / itici motoru / sol sac uyarlamaları kalktı; fırın 4000'de biter) · K bandı üstünde giriş çiti + 2 braket (F'nin parçası)
"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v47.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


degis('"""v47 (26 Eyl 2026):', '"""TP10 SÜRÜMÜ v2 (26 Eyl 2026) · AYRI SÜRÜM — ana makine v47 aynen durur. F = TP10 kesitli fırın, gövdesi 1500\'e uzatılmış\n'
      '  (firin_tp10_cad_v2: bant gövde dışına çıkmaz, ısıtılan 1316, aynı anda 4 ürün) · giriş bandı ön odada · K bandında giriş çiti · K parçaları değişmez.\n'
      '  Çıktı: hat_tp10_v2.glb/usdz · modul_D_tp10_v2 · durum_tp10_v2.json (hat_v47 ve modul_* dosyalarına DOKUNMAZ).\n'
      'v47 (26 Eyl 2026):')
# ---- FT (TOPPING malzemeleri yazıldıktan SONRA: TOPPING'in renkleri v47 ile aynı kalsın) ----
degis('''for _k, (_r, _m, _ru, _say) in TU.M.items():
    MALZEME.setdefault(_k, dict(renk=_r, met=_m, ruf=_ru, saydam=_say))
''', '''for _k, (_r, _m, _ru, _say) in TU.M.items():
    MALZEME.setdefault(_k, dict(renk=_r, met=_m, ruf=_ru, saydam=_say))
import firin_tp10_cad_v2 as FT                                                          # TP10 SÜRÜMÜ v2: uzatılmış fırın + uyarlama parçaları
AKTARMA_TP10 = ("bant_burun_silindiri", "bant_tahrik_silindiri", "bant", "bant_tasiyici_saci", "bant_yan_saci_0", "bant_yan_saci_1", "bant_motoru", "bant_ayagi")
KAIDE_PAH = cq.Workplane("XY").box(40.0, 28.0, 15.0, centered=False).translate((2560.0, 1112.0, -400.0)).val()   # X motoru kaidesi sağ üst köşe (fırın rulo sarımı 1114)
YARIK_V2 = FT.kut(*FT.YARIK_V2[0]).cut(FT.kut(*FT.YARIK_V2[1])).val()                          # TOPPING çıkış yarığı çerçevesi v2 (dünya)
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
      '''birim("D_DAVLUMBAZ", "Egzoz davlumbazı (bizim) · fan · yağ + karbon filtre · fırın üstünden 1483'ten · komşu modüllere asılı (dikme yok)", "D", "KUTU", (X_D, X_D + W_D), (FT.YG1 + 10.0, H_MAK), (-DZ, 0.0), "kutu", "pafta v7 · TP10 sürümü v2")
FT.kur(ayak=False, plaka=False, uyarla=True)
for _k, _a in FT.BIRIMLER:
    _bb = [FT.dunya(_p).BoundingBox() for _p in FT.PARCALAR if _p["birim"] == _k]
    birim(_k, _a, "D", "GERCEK_FIRIN", (min(q.xmin for q in _bb), max(q.xmax for q in _bb)), (min(q.ymin for q in _bb), max(q.ymax for q in _bb)),
          (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", "firin_tp10_cad_v2.py", "hat/firin_tp10.html")''')
# ---- K · parça değişmez ----
degis('''import kesme_cad_v1 as KS
KS.modul()
''', '''import kesme_cad_v1 as KS
KS.modul()
# TP10 SÜRÜMÜ v2 · K parçaları DEĞİŞMEZ (fırın 4000'de biter, uç kutusu yok). K bandı üstündeki giriş çiti + ölü plaka F'nin parçası (FT.adaptor).
K_UYARLAMA = ["K parçaları değişmedi · K bandı üstünde giriş çiti + 2 braket ve çıkış ölü plakası F'nin parçası"]
''')
# ---- TOPPING: aktarma bandı çıkar · kaide pahı · çıkış yarığı çerçevesi v2 ----
degis('''            ps = [p for p in TC.PARCALAR if v1_kalir(p["ad"]) and p["ad"] not in KAPAK]
            ton = {}''', '''            ps = [p for p in TC.PARCALAR if v1_kalir(p["ad"]) and p["ad"] not in KAPAK and p["ad"] not in AKTARMA_TP10]   # TP10 SÜRÜMÜ: aktarma bandı yok
            ton = {}''')
degis('''                sh = p["wp"].val().translate(cq.Vector(b["x"][0] + _d[0], b["y"][0] + _d[1], _d[2]))
''', '''                sh = p["wp"].val().translate(cq.Vector(b["x"][0] + _d[0], b["y"][0] + _d[1], _d[2]))
                if p["ad"] == "x_motor_kaidesi": sh = sh.cut(KAIDE_PAH)                   # TP10 SÜRÜMÜ
                if p["ad"] == "cikis_yarigi_contasi": sh = YARIK_V2                       # TP10 SÜRÜMÜ v2: çerçeve −417…−13, alt çıta 1145–1155
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
degis('''b["durum"] not in ("GERCEK_KUTU", "GERCEK_KESME")]   # v45''', '''b["durum"] not in ("GERCEK_KUTU", "GERCEK_KESME", "GERCEK_FIRIN")]   # TP10 v2: fırın parçaları gerçek katıyla taranır · v45''')
# ---- animasyon: yolculuk_tp10_v2 ----
_y47 = io.open(os.path.join(U, "yolculuk_v47.py"), encoding="utf-8").read()
_yt = io.open(os.path.join(U, "yolculuk_tp10_v2.py"), encoding="utf-8").read()
assert s.count(_y47) == 1, "hat_montaj_v47 icindeki yolculuk yolculuk_v47.py ile birebir degil"
s = s.replace(_y47, _yt)
degis('    print("ANA MONTAJ ANIMASYONU (v47):', '    print("ANA MONTAJ ANIMASYONU (TP10 SURUMU v2):')
degis('''    assert not _kotu, "TOPPING donen dugumu ekseninden kayiyor: %s" % _kotu[:3]
''', '''    assert not _kotu, "TOPPING donen dugumu ekseninden kayiyor: %s" % _kotu[:3]
    _kotu = [r for r in SAPMA if r[2].startswith("F_DONER__") and r[0] > 3.0]
    assert not _kotu, "firin / giris bandi rulosu ekseninden kayiyor: %s" % _kotu[:3]
''')
# ---- TP10 DENETİMİ (gerçek katı kesişimi + ürün yolu) · çıktılardan ÖNCE ----
degis('''    # ---- çıktılar ----
''', '''    # ================= TP10 SÜRÜMÜ v2 · DENETİM: gerçek katı kesişimi (mm³) + ürün yolu taraması =================
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
        if p["ad"] == "cikis_yarigi_contasi": sh = YARIK_V2
        if sh.BoundingBox().xmax > 2440.0: _DG.append(("TOPPING:" + p["ad"], sh))
    _TABLA = [p for p in TC.PARCALAR if grup_modul(p["ad"]) == "TABLA"]
    for p in _TABLA:                                                                     # tabla AKTARMA KONUMUNDA (dinamik)
        _DG.append(("TOPPING(aktarmada):" + p["ad"], p["wp"].val().translate(cq.Vector(X_BC + TH.X_AKTARMA - TC.XC_TABLA, H_B, 0.0))))
    for q in TU.P:
        if q["ad"].startswith(V3_CIKAN): continue
        sh = q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))
        if sh.BoundingBox().xmax > 2440.0: _DG.append(("TOPPING2:" + q["ad"], sh))
    for p in KS.PARCALAR:
        if p["grup"] in K_HARIC_GRUP: continue
        sh = _tek(p["wp"]).translate(cq.Vector(X_K, 0.0, 0.0))
        if sh.BoundingBox().xmin < 4330.0: _DG.append(("K:" + p["ad"], sh))
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
    # yeni TOPPING çerçevesi (v2) tabla aktarmadayken ve TOPPING'in kendi parçalarına
    _CER = [x_ for x_ in _DG if x_[0] == "TOPPING:cikis_yarigi_contasi"][0]
    for c_, sc in _DG:
        if c_ == _CER[0] or not c_.startswith("TOPPING"): continue
        if _bbk(_CER[1], sc):
            v_ = _hacim(_CER[1], sc)
            if v_ > 1.0 or v_ < 0: _cak.append((round(v_, 1), _CER[0] + "(v2)", c_))
    print("TP10 CAKISMA (gercek kati kesisimi > 1 mm3 · TOPPING + tabla aktarmada + K + hava + F kutulari + kendi arasinda + yeni cerceve): %s"
          % ("TEMIZ" if not _cak else "%d BULGU" % len(_cak)))
    for x_ in sorted(_cak, reverse=True)[:40]: print("   %10.1f mm3  %s  <->  %s" % x_)
    # ürün yolu: Ø280 gerçek ürün + Ø300 zarf · 28 yüksek · diskte 79 mm kayma (x 2337) → yarık → giriş bandı → fırın → ölü plaka → K bandı (çit) → kesme merkezi 4300
    _YOL = []
    _stat = [(a_, sa) for a_, sa in _F] + [(c_, sc) for c_, sc in _DG if c_.startswith(("K:", "TOPPING"))]
    _kon = [(X_BC + TH.X_AKTARMA, ZT + (FT.Z_URUN_FIRIN - ZT) * k_ / 8.0, 139.5) for k_ in range(9)]                       # diskte kayma (Ø280)
    _kon += [(float(x_), FT.urun_z(float(x_)), R_) for R_ in (139.5, 149.5) for x_ in range(2340, 4301, 10)]
    def _alt(xc, R_):                                                               # rijit ürün diski: ayak izinin altındaki EN YÜKSEK yüzeyin 0,5 üstü
        if xc - R_ <= 2492.0: return P + 0.5                                        # çalışma diski düz üstü 1168 (kenar son 15 mm konik)
        if xc - R_ <= FT.BANT_X[1]: return FT.BANT_UST_HAT + 0.5                    # giriş bandı + fırın bandı 1166
        if xc - R_ <= FT.OLU_X[1]: return KS.BANT + 2.0                             # ölü plaka 1165,5
        return KS.BANT + 0.5                                                        # K bandı 1164
    for xc, zc, R_ in _kon:
        y_ = _alt(xc, R_)
        cyl = cq.Solid.makeCylinder(R_, 28.0, cq.Vector(xc, y_, zc), cq.Vector(0, 1, 0))
        for a_, sa in _stat:
            if _bbk(cyl, sa):
                v_ = _hacim(cyl, sa)
                if v_ > 5.0 or v_ < 0: _YOL.append((int(round(xc)), round(zc, 1), round(v_, 1), "Ø%.0f %s" % (2 * R_ + 1, a_)))   # istisna (-1) da bulgu
    _n280 = len([k_ for k_ in _kon if k_[2] < 145]); _n300 = len(_kon) - _n280
    print("TP10 URUN YOLU (O280 %d konum + O300 zarf %d konum · 28 yuksek · 10 mm adim · diskte kayma + yarik + on oda + firin + K citi → 4300): %s"
          % (_n280, _n300, "TEMIZ" if not _YOL else "%d BULGU" % len(_YOL)))
    for x_ in _YOL[:40]: print("   x %d  z %.1f  %.1f mm3  %s" % x_)
    print("K UYARLAMASI: " + " · ".join(K_UYARLAMA))
    TP10_OZET = ("gerçek katı kesişimi %s (%d fırın/uyarlama parçası × %d komşu parça + yeni çerçeve) · ürün yolu %s (Ø280 %d konum + Ø300 %d konum, diskteki kaymadan K kesme merkezine)"
                 % ("TEMİZ" if not _cak else "%d BULGU" % len(_cak), len(_F), len(_DG), "TEMİZ" if not _YOL else "%d BULGU" % len(_YOL), _n280, _n300))
    assert not _cak and not _YOL, "TP10 surumu v2: cakisma / urun yolu bulgusu var"
    print("TP10 v2 YERLESIM: gövde %.0f–%.0f · ön oda %.0f–%.0f · giriş duvarı %.0f–%.0f · ISITILAN %.0f–%.0f = %.0f (aynı anda %d ürün, adım %.0f) · çıkış duvarı %.0f–%.0f · bant uçtan uca %.0f–%.0f (üst %.0f) · rulolar %.0f / %.0f · gövde y %.0f–%.0f · K çiti %.0f → %.0f"
          % (FT.X_F0, FT.X_F1, FT.X_F0, FT.X_DUV0, FT.X_DUV0, FT.X_TUN0, FT.X_TUN0, FT.X_TUN1, FT.ODA, FT.N_URUN, FT.ADIM, FT.X_TUN1, FT.X_F1, FT.BANT_X[0], FT.BANT_X[1], FT.BANT_UST_HAT, FT.RULO_X[0], FT.RULO_X[1], FT.YG0, FT.YG1, FT.CC_A[0], FT.CC_B[0]))

    # ---- çıktılar ----
''')
# ---- çıktılar: yalnız TP10 v2 dosyaları ----
degis('b1 = glb_yaz(os.path.join(OUT, "hat_v47.glb")', 'b1 = glb_yaz(os.path.join(OUT, "hat_tp10_v2.glb")')
degis('print("hat_v47.glb · %d dugum', 'print("hat_tp10_v2.glb · %d dugum')
degis('usdz_yaz([os.path.join(OUT, "hat_v47.usdz")], "hat_v47", _usd + E_USDZ, dokular)', 'usdz_yaz([os.path.join(OUT, "hat_tp10_v2.usdz")], "hat_tp10_v2", _usd + E_USDZ, dokular)')
degis('print("hat_v47.usdz · %.0f KB', 'print("hat_tp10_v2.usdz · %.0f KB')
degis('    for mk in ("A", "B", "C", "D", "K", "E", "-"):', '    for mk in ("D",):                                                              # TP10 SÜRÜMÜ: yalnız F (modul_* ana dosyalarına dokunmaz)')
degis('        dosya = "modul_%s" % hrf', '        dosya = "modul_%s_tp10_v2" % hrf')
degis('    with io.open(os.path.join(OUT, "durum.json"), "w", encoding="utf-8") as f:', '    with io.open(os.path.join(OUT, "durum_tp10_v2.json"), "w", encoding="utf-8") as f:')
degis('pafta="HAT_ATOSA_TABLALI v12 · v47 (on yuzden tasan parcalar iceri, animasyon v46 duzeltmesi) ·',
      'pafta="TP10 SURUMU v2 (ayri) · FIRIN_TP10 v3 · ana makine v47 + F = TP10 kesitli firin 1500 (bant govde disina cikmaz, isitilan 1316, 4 urun) · giris bandi on odada · K bandinda giris citi · K parcalari degismez ·')
degis('print("durum.json yazildi', 'print("durum_tp10_v2.json yazildi')
degis('dosya=MODUL_DOSYA, birim=[', 'dosya=MODUL_DOSYA, tp10_denetim=TP10_OZET, birim=[')
assert "hat_v47.glb" not in s and '"durum.json"' not in s, "ana dosya adi kaldi"
io.open(os.path.join(U, "hat_montaj_tp10_v2.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_tp10_v2.py yazildi")
