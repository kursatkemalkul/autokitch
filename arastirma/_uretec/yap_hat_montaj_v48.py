# -*- coding: utf-8 -*-
"""hat_montaj_v47 → hat_montaj_v48 · ANA MAKİNE (26 Eyl 2026 gece, Kemal "v2 kabul" + 5 iş):
  F  · özel fırın kutuları (D_FIRIN_GOVDE · D_HAZNE · D_BANT) → TP10 kesitli, gövdesi 1500'e uzatılmış fırın (firin_tp10_cad_v3: cep yok, üst raf) ·
       taban dolabı 1060 → 956 · pizza kutusu yedeği 553 → 505 (dolap) + 55 (fırın üstü raf) = 560 = 2 gün (kural 5.5) · davlumbaz arka yarı (z −425…−830) ·
       giriş bandı ön odada · çıkış ölü plakası · K bandında giriş çiti · arka sac
  HAVA · kompresör K tabanından FIRIN ÜSTÜNE (raf 1481, ön yarı, x 3600–3980) — TOPPING'in istisnası (kural 4, 26 Eyl gece) · ana hat fırın üstünden
       TOPPING sağ dış sacındaki rakora (y 2000 / z −415) → teknik cep → kuru bölme → şartlandırıcı · K'ye dal (K besleme hattının tepesine)
  C  · TOPPING v1 mekanizması topping_cad_v24 (tekne 2500'de biter: motor sola, avara sağa, kelepçeler solda) → fırında cep gerekmez ·
       TOPPING v2 topping_uno_cad_v6 (kaset yuvaları · kavramalar · yalıtım tek blok · ön fitil) · aktarma bandı çıkar · çıkış yarığı çerçevesi v2
  K  · parça değişmez (kompresör K'den çıktı: HAVA birimi D modülüne)
  Çıktı: hat_v48.glb/usdz · modul_* (değişmeyenler git'ten geri alınır) · durum.json
"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v47.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


degis('"""v47 (26 Eyl 2026):', '"""v48 (26 Eyl 2026 gece): F = TP10 kesitli fırın, gövde 1500 (firin_tp10_cad_v3; v2 Kemal kabul) · kompresör fırın üstünde ·\n'
      '  kutu yedeği 505 + 55 · TOPPING v24 (tekne 2500\'de biter) + v2 v6 (kaset yuvaları, kavrama, yalıtım bloğu, fitil) · K değişmez.\n'
      'v47 (26 Eyl 2026):')
# ---- TOPPING sürümleri ----
degis('import topping_hesap_v6 as TH, topping_cad_v23 as TC', 'import topping_hesap_v6 as TH, topping_cad_v24 as TC                                      # v48: tekne 2500\'de biter')
degis('"topping_uno_cad_v5.py + topping_cad_v23.py", "hat/topping_v2.html")', '"topping_uno_cad_v6.py + topping_cad_v24.py", "hat/topping_v2.html")')
degis('''_sp = _ilu.spec_from_file_location("TU5", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v5.py"))''',
      '''_sp = _ilu.spec_from_file_location("TU6", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v6.py"))   # v48: kaset yuvaları + yalıtım bloğu + fitil''')
# ---- HAVA: kompresör fırın üstüne (D modülü) ----
degis('''birim("HAVA_KOMPRESOR", "Kompresör JUN-AIR OF302-15B (yağsız, 15 L, 25 kg) · K tabanı ARKADA (130–640) + Ø10 ana hat · K arkası → F arkası → TOPPING", "K", "GERCEK_HAVA",
      (X_BC + 1800.0, X_BC + 3900.0), (123.0, 1100.0), (-DZ, 0.0), "sac", "topping_uno_cad_v5.py", "hat/topping_v2.html")''',
      '''birim("HAVA_KOMPRESOR", "Kompresör JUN-AIR OF302-15B (yağsız, 15 L, 25 kg) · FIRIN ÜSTÜNDE (raf 1481, davlumbaz bölmesinin ön yarısı, kutu yedeğinin yanı — TOPPING'in tek istisnası) · Ø10 ana hat fırın üstünden TOPPING sağ dış sac rakoruna (y 2000 / z −415) → teknik cep → kuru bölme → şartlandırıcı · K'ye dal", "D", "GERCEK_HAVA",
      (3600.0, 3980.0), (1481.0, 1991.0), (-420.0, -40.0), "sac", "topping_uno_cad_v6.py", "hat/topping_v2.html")''')
degis('''KOMP_KAY = (-70.0, -390.0, -385.0)            # v44: kompresör K tabanının önünden (y 520–1030, z −40…−420) arkasına (130–640, −425…−805)
ANA_V44 = [(3530, 646, -765), (3530, 1040, -765), (3530, 1040, -790), (1830, 1040, -790), (1830, 1100, -790), (1675, 1100, -790), (1675, 1250, -740)]''',
      '''KOMP_KAY = (-510.0, 941.0, 0.0)               # v48: kompresör (TU x 3410–3790 · y 520–1030 · z −40…−420) → fırın üstü raf: dünya x 3600–3980 · y 1481–1991 · z aynı
ANA_V44 = [(3090, 1977, -380), (3090, 2000, -380), (3090, 2000, -415), (1640, 2000, -415), (1640, 2000, -740), (1640, 1335, -740), (1650, 1335, -740)]   # v48: fırın üstü → TOPPING rakoru (dünya 2500, y 2000, z −415) → teknik cep → kuru bölme → şartlandırıcı sol yüzü
ANA_K48 = [(3090, 2000, -415), (3090, 2000, -795), (3460, 2000, -795), (3460, 1700, -795)]   # v48: K'ye dal — K besleme hattının tepesine (dünya x 4160, y 1700, z −795)''')
degis('''            _ana = TU.boru(ANA_V44, 5.0)                                        # v44 · yeni güzergâh
            _ana = _ana.val() if hasattr(_ana, "val") else _ana
            ton.setdefault(("hava_ana", "SABIT"), Mesh()).ekle(TC_AG(cq.Workplane(obj=_ana.translate(cq.Vector(X_BC, 0.0, 0.0))), False))''',
      '''            for _rota in (ANA_V44, ANA_K48):                                    # v48: fırın üstünden TOPPING'e + K'ye dal
                _ana = TU.boru(_rota, 5.0)
                _ana = _ana.val() if hasattr(_ana, "val") else _ana
                ton.setdefault(("hava_ana", "SABIT"), Mesh()).ekle(TC_AG(cq.Workplane(obj=_ana.translate(cq.Vector(X_BC, 0.0, 0.0))), False))''')
# ---- FT (TOPPING malzemeleri yazıldıktan SONRA) ----
degis('''for _k, (_r, _m, _ru, _say) in TU.M.items():
    MALZEME.setdefault(_k, dict(renk=_r, met=_m, ruf=_ru, saydam=_say))
''', '''for _k, (_r, _m, _ru, _say) in TU.M.items():
    MALZEME.setdefault(_k, dict(renk=_r, met=_m, ruf=_ru, saydam=_say))
import firin_tp10_cad_v3 as FT                                                          # v48: TP10 kesitli 1500 fırın + uyarlama parçaları (cep yok)
AKTARMA_TP10 = ("bant_burun_silindiri", "bant_tahrik_silindiri", "bant", "bant_tasiyici_saci", "bant_yan_saci_0", "bant_yan_saci_1", "bant_motoru", "bant_ayagi")
YARIK_V2 = FT.kut(*FT.YARIK_V2[0]).cut(FT.kut(*FT.YARIK_V2[1])).val()                          # TOPPING çıkış yarığı çerçevesi v2 (dünya)
''')
# ---- F · taban dolabı 956 · içerik · davlumbaz arka yarı · kutu yedeği üstte · fırın birimleri ----
degis('birim("D_TABAN_KABIN", "F taban dolabı 123–1060 · önde bulaşık',
      'birim("D_TABAN_KABIN", "F taban dolabı 123–956 (fırın gövdesi bant 1166 için 956\'ya iner — istasyon tabanı 1060 kuralının F istisnası, Kemal 26 Eyl) · önde bulaşık')
degis('"D", "KUTU", (X_D, X_D + W_D), (Y_ALT, H_B), (-DZ, 0.0), "kabin", "v44 alt kısım v3")',
      '"D", "KUTU", (X_D, X_D + W_D), (Y_ALT, FT.YG0), (-DZ, 0.0), "kabin", "v44 alt kısım v3 · v48 üstü 956")')
degis('(510.0, 656.0), (130.0, 1045.0), (-210.0, -20.0), False, "B\'nin K4 nişinden taşındı',
      '(510.0, 656.0), (130.0, 950.0), (-210.0, -20.0), False, "v48: üstü 950 · B\'nin K4 nişinden taşındı')
degis('("D_PIZZA_YEDEK", "Pizza kutusu yedeği · 553 kutu düz (804 × 404 × 885 + taban 15) · şarjör 567 + 553 = 1120 = 4 gün · önde", (666.0, 1470.0), (130.0, 1030.0),',
      '("D_PIZZA_YEDEK", "Pizza kutusu yedeği · dolapta 505 kutu düz (804 × 404 × 808 + taban 15) + fırın üstünde 55 = 560 · şarjör 567 + 560 = 1127 = 4 gün (kural 5.5) · önde", (666.0, 1470.0), (130.0, 953.0),')
_d0 = s.index('birim("D_FIRIN_GOVDE",'); _d1 = s.index('birim("D_DAVLUMBAZ",')
s = s[:_d0] + s[_d1:]
degis('''birim("D_DAVLUMBAZ", "Egzoz davlumbazı · fan · yağ + karbon filtre · fırın kartı + SSR + kontaktör", "D", "KUTU", (X_D, X_D + W_D), (F_G1 + 10.0, H_MAK), (-DZ, 0.0), "kutu", "pafta v7")''',
      '''birim("D_DAVLUMBAZ", "Egzoz davlumbazı (bizim) · fan · yağ + karbon filtre · fırın üstü bölmenin ARKA yarısı (ön yarıda kutu yedeği + kompresör) · komşu modüllere asılı", "D", "KUTU", (X_D, X_D + W_D), (FT.YG1 + 10.0, H_MAK), (-DZ, -425.0), "kutu", "v48")
birim("D_PIZZA_YEDEK_UST", "Pizza kutusu yedeği · fırın üstü rafta 55 kutu düz (804 × 404 × 88) · dolaptaki 505 ile 560 = 2 gün", "D", "KUTU", (X_D + 20.0, X_D + 824.0), (1481.0, 1569.0), (-424.0, -20.0), "kutu", "v48 · kural 5.5")
FT.kur(ayak=False, plaka=False, uyarla=True)
for _k, _a in FT.BIRIMLER:
    _bb = [FT.dunya(_p).BoundingBox() for _p in FT.PARCALAR if _p["birim"] == _k]
    birim(_k, _a, "D", "GERCEK_FIRIN", (min(q.xmin for q in _bb), max(q.xmax for q in _bb)), (min(q.ymin for q in _bb), max(q.ymax for q in _bb)),
          (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", "firin_tp10_cad_v3.py", "hat/oven.html")''')
# ---- TOPPING: aktarma bandı çıkar · çıkış yarığı çerçevesi v2 ----
degis('''            ps = [p for p in TC.PARCALAR if v1_kalir(p["ad"]) and p["ad"] not in KAPAK]
            ton = {}''', '''            ps = [p for p in TC.PARCALAR if v1_kalir(p["ad"]) and p["ad"] not in KAPAK and p["ad"] not in AKTARMA_TP10]   # v48: aktarma bandı yok
            ton = {}''')
degis('''                sh = p["wp"].val().translate(cq.Vector(b["x"][0] + _d[0], b["y"][0] + _d[1], _d[2]))
''', '''                sh = p["wp"].val().translate(cq.Vector(b["x"][0] + _d[0], b["y"][0] + _d[1], _d[2]))
                if p["ad"] == "cikis_yarigi_contasi": sh = YARIK_V2                       # v48: çerçeve −417…−13, alt çıta 1145–1155
''')
# ---- yeni birim türü: GERCEK_FIRIN ----
degis('''        elif b["durum"] == "GERCEK":
            V, ps = kaset_parcalari(b["kaynak"][:-3]); AG = AG or V''', '''        elif b["durum"] == "GERCEK_FIRIN":                                                   # v48
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
    assert abs(_bk["D_TABAN_KABIN"]["y"][1] - FT.YG0) < 0.01, "v48: F taban dolabi ustu %.1f" % _bk["D_TABAN_KABIN"]["y"][1]''')
degis('''        if p["ad"].startswith("_bom") or p["ad"] in KAPAK:
            continue
        bb = p["wp"].val().BoundingBox()''', '''        if p["ad"].startswith("_bom") or p["ad"] in KAPAK or p["ad"] in AKTARMA_TP10:
            continue
        bb = p["wp"].val().BoundingBox()''')
degis('''b["durum"] not in ("GERCEK_KUTU", "GERCEK_KESME")]   # v45''', '''b["durum"] not in ("GERCEK_KUTU", "GERCEK_KESME", "GERCEK_FIRIN")]   # v48: fırın parçaları gerçek katıyla taranır · v45''')
degis('''    _ZON = ("D_FIRIN_GOVDE", "HAVA_KOMPRESOR")''', '''    _ZON = ("HAVA_KOMPRESOR",)                                                # v48: fırın kutusu yok''')
# ---- animasyon: yolculuk_v48 ----
_y47 = io.open(os.path.join(U, "yolculuk_v47.py"), encoding="utf-8").read()
_y48 = io.open(os.path.join(U, "yolculuk_v48.py"), encoding="utf-8").read()
assert s.count(_y47) == 1, "hat_montaj_v47 icindeki yolculuk yolculuk_v47.py ile birebir degil"
s = s.replace(_y47, _y48)
degis('    print("ANA MONTAJ ANIMASYONU (v47):', '    print("ANA MONTAJ ANIMASYONU (v48):')
degis('''    assert not _kotu, "TOPPING donen dugumu ekseninden kayiyor: %s" % _kotu[:3]
''', '''    assert not _kotu, "TOPPING donen dugumu ekseninden kayiyor: %s" % _kotu[:3]
    _kotu = [r for r in SAPMA if r[2].startswith("F_DONER__") and r[0] > 3.0]
    assert not _kotu, "firin / giris bandi rulosu ekseninden kayiyor: %s" % _kotu[:3]
''')
# ---- FIRIN DENETİMİ (gerçek katı kesişimi + ürün yolu) · çıktılardan ÖNCE ----
degis('''    # ---- çıktılar ----
''', '''    # ================= v48 · FIRIN DENETİMİ: gerçek katı kesişimi (mm³) + ürün yolu taraması =================
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
    for _rota in (ANA_V44, ANA_K48):
        _an = TU.boru(_rota, 5.0); _an = _an.val() if hasattr(_an, "val") else _an
        _DG.append(("HAVA:ana_hat", _an.translate(cq.Vector(X_BC, 0.0, 0.0))))
    for q in TU.P:                                                                       # kompresör fırın üstünde (rafın üstü)
        if q["ad"].startswith("kompresor_"): _DG.append(("HAVA:" + q["ad"], q["sh"].translate(cq.Vector(X_BC + KOMP_KAY[0], KOMP_KAY[1], KOMP_KAY[2]))))
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
    _CER = [x_ for x_ in _DG if x_[0] == "TOPPING:cikis_yarigi_contasi"][0]              # yeni çerçeve ↔ TOPPING (tabla aktarmada dahil)
    for c_, sc in _DG:
        if c_ == _CER[0] or not c_.startswith("TOPPING"): continue
        if _bbk(_CER[1], sc):
            v_ = _hacim(_CER[1], sc)
            if v_ > 1.0 or v_ < 0: _cak.append((round(v_, 1), _CER[0] + "(v2)", c_))
    _KOMP = [x_ for x_ in _DG if x_[0].startswith("HAVA:kompresor")]                     # kompresör ↔ raf üstündeki komşular (kutu yedeği kutusu, davlumbaz)
    for a_, sa in _KOMP:
        for c_, sc in _DG:
            if c_.startswith("HAVA:") or c_.startswith("D:D_DAVLUMBAZ") is False and not c_.startswith("D:"): continue
            if _bbk(sa, sc):
                v_ = _hacim(sa, sc)
                if v_ > 1.0 or v_ < 0: _cak.append((round(v_, 1), a_, c_))
    print("FIRIN CAKISMA (gercek kati kesisimi > 1 mm3 · TOPPING + tabla aktarmada + K + hava + kompresor + F kutulari + kendi arasinda + yeni cerceve): %s"
          % ("TEMIZ" if not _cak else "%d BULGU" % len(_cak)))
    for x_ in sorted(_cak, reverse=True)[:40]: print("   %10.1f mm3  %s  <->  %s" % x_)
    _YOL = []
    _stat = [(a_, sa) for a_, sa in _F] + [(c_, sc) for c_, sc in _DG if c_.startswith(("K:", "TOPPING"))]
    _kon = [(X_BC + TH.X_AKTARMA, ZT + (FT.Z_URUN_FIRIN - ZT) * k_ / 8.0, 139.5) for k_ in range(9)]
    _kon += [(float(x_), FT.urun_z(float(x_)), R_) for R_ in (139.5, 149.5) for x_ in range(2340, 4301, 10)]
    def _alt(xc, R_):                                                               # rijit ürün diski: ayak izinin altındaki EN YÜKSEK yüzeyin 0,5 üstü
        if xc - R_ <= 2492.0: return P + 0.5
        if xc - R_ <= FT.BANT_X[1]: return FT.BANT_UST_HAT + 0.5
        if xc - R_ <= FT.OLU_X[1]: return KS.BANT + 2.0
        return KS.BANT + 0.5
    for xc, zc, R_ in _kon:
        y_ = _alt(xc, R_)
        cyl = cq.Solid.makeCylinder(R_, 28.0, cq.Vector(xc, y_, zc), cq.Vector(0, 1, 0))
        for a_, sa in _stat:
            if _bbk(cyl, sa):
                v_ = _hacim(cyl, sa)
                if v_ > 5.0 or v_ < 0: _YOL.append((int(round(xc)), round(zc, 1), round(v_, 1), "Ø%.0f %s" % (2 * R_ + 1, a_)))
    _n280 = len([k_ for k_ in _kon if k_[2] < 145]); _n300 = len(_kon) - _n280
    print("FIRIN URUN YOLU (O280 %d konum + O300 zarf %d konum · 28 yuksek · 10 mm adim · diskte kayma + yarik + on oda + firin + K citi → 4300): %s"
          % (_n280, _n300, "TEMIZ" if not _YOL else "%d BULGU" % len(_YOL)))
    for x_ in _YOL[:40]: print("   x %d  z %.1f  %.1f mm3  %s" % x_)
    # TOPPING teknesi modülün içinde mi (v24)
    _tx = max(p["wp"].val().BoundingBox().xmax for p in TC.PARCALAR if not p["ad"].startswith("_bom") and v1_kalir(p["ad"]) and p["ad"] not in AKTARMA_TP10 and grup_modul(p["ad"]) not in ("TABLA", "ARABA"))
    print("TOPPING SABIT PARCALARIN SAG UCU: x %.1f (dunya %.1f) · duvar 2500 → %s" % (_tx, _tx + X_BC, "ICERIDE" if _tx + X_BC <= 2500.0 else "TASIYOR"))
    assert _tx + X_BC <= 2500.0, "TOPPING sabit parcasi 2500'u geciyor"
    FIRIN_OZET = ("gerçek katı kesişimi %s (%d fırın/uyarlama parçası × %d komşu parça + yeni çerçeve + kompresör) · ürün yolu %s (Ø280 %d + Ø300 %d konum) · TOPPING sabit parçaları 2500'ün içinde (%.0f)"
                  % ("TEMİZ" if not _cak else "%d BULGU" % len(_cak), len(_F), len(_DG), "TEMİZ" if not _YOL else "%d BULGU" % len(_YOL), _n280, _n300, _tx + X_BC))
    assert not _cak and not _YOL, "v48: cakisma / urun yolu bulgusu var"
    print("FIRIN YERLESIM: gövde %.0f–%.0f · ön oda %.0f–%.0f · giriş duvarı %.0f–%.0f · ISITILAN %.0f–%.0f = %.0f (aynı anda %d ürün, adım %.0f) · çıkış duvarı %.0f–%.0f · bant uçtan uca %.0f–%.0f (üst %.0f) · rulolar %.0f / %.0f · gövde y %.0f–%.0f · K çiti %.0f → %.0f"
          % (FT.X_F0, FT.X_F1, FT.X_F0, FT.X_DUV0, FT.X_DUV0, FT.X_TUN0, FT.X_TUN0, FT.X_TUN1, FT.ODA, FT.N_URUN, FT.ADIM, FT.X_TUN1, FT.X_F1, FT.BANT_X[0], FT.BANT_X[1], FT.BANT_UST_HAT, FT.RULO_X[0], FT.RULO_X[1], FT.YG0, FT.YG1, FT.CC_A[0], FT.CC_B[0]))

    # ---- çıktılar ----
''')
# ---- çıktılar ----
degis('b1 = glb_yaz(os.path.join(OUT, "hat_v47.glb")', 'b1 = glb_yaz(os.path.join(OUT, "hat_v48.glb")')
degis('print("hat_v47.glb · %d dugum', 'print("hat_v48.glb · %d dugum')
degis('usdz_yaz([os.path.join(OUT, "hat_v47.usdz")], "hat_v47", _usd + E_USDZ, dokular)', 'usdz_yaz([os.path.join(OUT, "hat_v48.usdz")], "hat_v48", _usd + E_USDZ, dokular)')
degis('print("hat_v47.usdz · %.0f KB', 'print("hat_v48.usdz · %.0f KB')
degis('pafta="HAT_ATOSA_TABLALI v12 · v47 (on yuzden tasan parcalar iceri, animasyon v46 duzeltmesi) · K = kesme_cad_v1 (gercek) · 1 tam animasyon · alt kisim v3 · B = store_cad_v5 · kompresor K tabani arkasinda · TOPPING v2 UNO\'lu (topping_uno_cad_v5) · E = kutu_cad_v3 · alt taban 123 · taban hizasi · surec 1168"',
      'pafta="HAT v48 (26 Eyl gece) · F = TP10 kesitli 1500 firin (firin_tp10_cad_v3: bant govde disina cikmaz, isitilan 1316, 4 urun) · kompresor firin ustunde · kutu yedegi 505 + 55 · TOPPING v24 (tekne 2500\'de biter) + v2 v6 (kaset yuvalari, kavrama, yalitim blogu, fitil) · K = kesme_cad_v1 · 1 tam animasyon · B = store_cad_v5 · E = kutu_cad_v3 · alt taban 123 · surec 1168", firin_denetim=FIRIN_OZET')
assert "hat_v47.glb" not in s and "D_FIRIN_GOVDE" not in s, "eski ad kaldi"
degis('''    assert not [b for b in B if "KUTU YEDE" in b["ad"].upper() or "KUTU_YEDEK" in b["kod"]], "yedek karton kutu hala var"''',
      '''    assert not [b for b in B if "KARTON KULE" in b["ad"].upper() or b["kod"].endswith("KUTU_YEDEK")], "yedek karton kutu hala var"   # v48: 'kutu yedeği' metni artık kompresör/davlumbaz adında geçiyor (fırın üstü raf) — eski karton kulesi yok''')
io.open(os.path.join(U, "hat_montaj_v48.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v48.py yazildi")
