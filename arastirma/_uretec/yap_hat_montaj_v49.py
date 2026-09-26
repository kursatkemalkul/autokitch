# -*- coding: utf-8 -*-
"""hat_montaj_v48 → hat_montaj_v49 (26 Eyl 2026 gece, Kemal: "itici tasarımını yap · yay pim hepsi katalog · her şeyi mühendislik gözüyle
tekrar kontrol et ve düzelt · fırın özel sipariş olur yeter ki gerçek ölçülerde olsun · toppinge ön kapak yok"):
 1 · AKTARMA İTİCİSİ (itici_cad_v1, modül C, GERCEK_ITICI): SMC MY1B16-250 kolsuz silindir çapraz (24,9°), pivotlu çubuk 170 × 30,
     dönüşte sabit pime rolan makarayla 90° kalkar; pideyi diskten (2337, −170) giriş bandına (2507, −249) iter (+170 x, −79 z);
     DESTEK PLAKASI y 1167 (diskin arka kenarının gerisi) pidenin arkada kalan kısmını taşır. Animasyon: ARABA öteleme + KOL dönme
     (OZEL_T düğümü, pivot-yerel). Ürün yolu: diskte kayma yerine ÇAPRAZ itme (T_AKT+0,1 … +0,7), sonra bantlar (T_F0 = T_AKT+0,7).
 2 · FIRIN v4 (firin_tp10_cad_v4): üst raf HAVALANDIRMALI (40 mm takoz + 0,8 mm ışınım kalkanı) — JUN-AIR ortam sınırı 40 °C; raf 1516,
     kompresör 1516–2026 (hat 2030), kutu yedeği 1516–1604. Hava rotası aynı.
 3 · TOPPING v2 v7 (topping_uno_cad_v7): katalog yay (Century 66644SCS) + pimler (ISO 8734), segman kanalı DIN 471, haç 7,0,
     mandal 4,5/5,0; kabin yan PU duvarları 1277'den.
 4 · İTİCİ DENETİMİ: itici (ev-kalkık / son / orta) ↔ TOPPING (tabla park + aktarma) + F + K gerçek katı kesişimi · pide geliş
     koridoru (z −320…−20, y 1168–1201) ve disk süpürmesi ↔ itici/destek · çubuk itme süpürmesi ↔ sabitler · ürün yolu çapraz.
 5 · "Yedek karton" iddiası v48'de daraltılmıştı. Çıktılar hat_v49 · modul_* · durum.json (pafta HAT v49, firin_denetim + itici_denetim)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v48.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


NL = chr(10)
# ---- başlık ----
degis('"""v48 (26 Eyl 2026 gece): F = TP10 kesitli fırın', '"""v49 (26 Eyl 2026 gece): AKTARMA İTİCİSİ (itici_cad_v1: SMC MY1B16-250 çapraz 24,9°, pivotlu çubuk sabit pimle kalkar, destek plakası y 1167) + fırın v4 (havalandırmalı raf) + TOPPING v2 v7 (katalog yay/pim, haç 7,0) · ürün yolu çapraz itme · itici denetimi (ev/son/orta, koridor, disk, itme süpürmesi)' + NL + 'v48 (26 Eyl 2026 gece): F = TP10 kesitli fırın')
# ---- modüller ----
degis('import firin_tp10_cad_v3 as FT                                                          # v48: TP10 kesitli 1500 fırın + uyarlama parçaları (cep yok)',
      'import firin_tp10_cad_v4 as FT                                                          # v49: fırın v4 (havalandırmalı raf: 40 mm takoz + ışınım kalkanı)' + NL +
      'import itici_cad_v1 as IT                                                              # v49: aktarma iticisi + destek plakası (dünya koordinatı)' + NL +
      'for _k, _v in IT.MALZEME.items():' + NL + '    MALZEME.setdefault(_k, dict(renk=_v["renk"], met=_v["met"], ruf=_v["ruf"], saydam=False))')
degis('_sp = _ilu.spec_from_file_location("TU6", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v6.py"))',
      '_sp = _ilu.spec_from_file_location("TU7", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v7.py"))   # v49: katalog yay/pim, haç 7,0')
degis('"topping_uno_cad_v6.py + topping_cad_v24.py", "hat/topping_v2.html")', '"topping_uno_cad_v7.py + topping_cad_v24.py", "hat/topping_v2.html")')
degis('''      (3600.0, 3980.0), (1481.0, 1991.0), (-420.0, -40.0), "sac", "topping_uno_cad_v6.py", "hat/topping_v2.html")''',
      '''      (3600.0, 3980.0), (1516.0, 2026.0), (-420.0, -40.0), "sac", "topping_uno_cad_v7.py", "hat/topping_v2.html")''')
degis("FIRIN ÜSTÜNDE (raf 1481, davlumbaz bölmesinin ön yarısı", "FIRIN ÜSTÜNDE (havalandırmalı raf 1516, ortam sınırı 40 °C, davlumbaz bölmesinin ön yarısı")
degis('KOMP_KAY = (-510.0, 941.0, 0.0)', 'KOMP_KAY = (-510.0, 976.0, 0.0)')
degis('(X_D + 20.0, X_D + 824.0), (1481.0, 1569.0), (-424.0, -20.0), "kutu", "v48 · kural 5.5")', '(X_D + 20.0, X_D + 824.0), (1516.0, 1604.0), (-424.0, -20.0), "kutu", "v48 · kural 5.5 · v49 raf 1516")')
degis('''          (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", "firin_tp10_cad_v3.py", "hat/oven.html")''',
      '''          (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", "firin_tp10_cad_v4.py", "hat/oven.html")
# ---- v49 · AKTARMA İTİCİSİ + DESTEK PLAKASI (modül C, dünya koordinatı; ev konumu, çubuk kalkık) ----
IT.kur(IT.S_HOME, True)
for _k, _a in IT.BIRIMLER:
    _bb = [IT.dunya(_p).BoundingBox() for _p in IT.PARCALAR if _p["birim"] == _k]
    birim(_k, _a, "C", "GERCEK_ITICI", (min(q.xmin for q in _bb), max(q.xmax for q in _bb)), (min(q.ymin for q in _bb), max(q.ymax for q in _bb)),
          (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", "itici_cad_v1.py", "hat/oven.html#itici")''')
# ---- render dalı ----
degis('''        elif b["durum"] == "GERCEK":
            V, ps = kaset_parcalari(b["kaynak"][:-3]); AG = AG or V''',
      '''        elif b["durum"] == "GERCEK_ITICI":                                                   # v49
            ps = [p for p in IT.PARCALAR if p["birim"] == b["kod"]]
            ton = {}
            for p in ps:
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(cq.Workplane(obj=IT.dunya(p))))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(ps)
        elif b["durum"] == "GERCEK":
            V, ps = kaset_parcalari(b["kaynak"][:-3]); AG = AG or V''')
# ---- yolculuk: aktarma adımı (çapraz itme) ----
degis('''    ADIM.append((T_AKT - 0.5, "AKTARMA", "Tabla sağ uca gider; ürün diskte 79 mm arkaya kaydırılır (fırın bandının eksenine — itici AÇIK konu) ve fırının ön odasındaki giriş bandına itilir; tabla açıcının altına döner."))
    X.git(T_AKT + 0.5, T_AKT + 0.5 + gecis(TH2.X_AKTARMA, TH2.X_PARK), TH2.X_PARK)
    T_F0, T_F1 = T_AKT + 0.5, T_AKT + 10.5''',
      '''    ADIM.append((T_AKT - 0.5, "AKTARMA", "Tabla sağ uca gider; İTİCİ (SMC MY1B16-250, 24,9° çapraz) çubuğunu indirir ve pideyi diskten fırının giriş bandına iter: +170 x, −79 z (fırın bandının eksenine); arkada kalan kısmı destek plakası taşır. Çubuk kalkar, araba eve döner; tabla açıcının altına döner."))
    T_IT0, T_IT1 = T_AKT + 0.1, T_AKT + 0.7                                                      # v49: çubuk iner (T_AKT…+0,1), itme (+0,1…+0,7), bekleme, dönüş (+0,9…+1,5), son 17,5 mm'de kalkar
    X.git(T_AKT + 0.9, T_AKT + 0.9 + gecis(TH2.X_AKTARMA, TH2.X_PARK), TH2.X_PARK)
    T_F0, T_F1 = T_IT1, T_AKT + 10.7''')
degis('''        if t < T_F0:
            u = (t - T_AKT) / (T_F0 - T_AKT); return (OX + TH2.X_AKTARMA, OY + 108.0, ZT + (FT.Z_URUN_FIRIN - ZT) * u)   # v48: diskte arkaya kayma''',
      '''        if t < T_F0:
            u = min(1.0, max(0.0, (t - T_IT0) / (T_IT1 - T_IT0)))                                   # v49: çapraz itme (C0 → C1)
            return (IT.C0[0] + (IT.C1[0] - IT.C0[0]) * u, OY + 108.0, IT.C0[1] + (IT.C1[1] - IT.C0[1]) * u)''')
degis('''            u = (t - T_F0) / (T_F1 - T_F0); x0 = OX + TH2.X_AKTARMA; x_ = x0 + (3940.0 - x0) * u''',
      '''            u = (t - T_F0) / (T_F1 - T_F0); x0 = IT.C1[0]; x_ = x0 + (3940.0 - x0) * u                                # v49: bantlar 2507'den alır''')
degis('''    BANT.git(T_AKT, T_F1, (3940.0 - (OX + TH2.X_AKTARMA)), "l")''', '''    BANT.git(T_IT1, T_F1, (3940.0 - IT.C1[0]), "l")''')
# itici düğümleri: ARABA öteleme + KOL (OZEL_T, pivot-yerel) dönme
degis('''    # v48 · fırın + giriş bandı ruloları KENDİ EKSENİNDE (ağ pivota göre yerel) · bant yüzey hızıyla · dünya koordinatı''',
      '''    # v49 · AKTARMA İTİCİSİ: araba s(t) (çubuk yüzü konumu, mm) ve çubuk açısı (0 = inik, 90 = kalkık)
    def it_s(t):
        if t < T_IT0: return IT.S_HOME
        if t < T_IT1: return IT.S_HOME + (IT.S_END - IT.S_HOME) * (t - T_IT0) / (T_IT1 - T_IT0)
        if t < T_AKT + 0.9: return IT.S_END
        if t < T_AKT + 1.5: return IT.S_END + (IT.S_HOME - IT.S_END) * (t - T_AKT - 0.9) / 0.6
        return IT.S_HOME
    def it_aci(t):
        if t < T_AKT: return 90.0
        if t < T_IT0: return 90.0 * (1.0 - (t - T_AKT) / (T_IT0 - T_AKT))
        s_ = it_s(t)
        if t > T_AKT + 0.9 and s_ < IT.S_TEMAS: return 90.0 * (IT.S_TEMAS - s_) / (IT.S_TEMAS - IT.S_HOME)
        return 0.0
    def it_kay(t):
        d_ = it_s(t) - IT.S_HOME; return (d_ * IT.U[0] * MM, 0.0, d_ * IT.U[1] * MM)
    for a_, m_, mal_ in parcalar:
        if a_.startswith("C_ITICI__") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] == "ARABA":
            kanal(a_, it_kay)
    IT.kur(IT.S_HOME, False)                                                                 # KOL yerel ağı: ev konumu, çubuk İNİK (dönme animasyonla)
    _piv = IT.dunya_nokta(IT.S_HOME, IT.PIVOT_Y, IT.W_AXIS)
    ton = {}
    for p in IT.PARCALAR:
        if p["grup"] != "KOL": continue
        m_ = TC_AG(cq.Workplane(obj=IT.dunya(p)))
        y_ = Mesh(); y_.P = [(q[0] - _piv[0] * MM, q[1] - _piv[1] * MM, q[2] - _piv[2] * MM) for q in m_.P]; y_.N = list(m_.N); y_.I = list(m_.I)
        ton.setdefault(mal_ad({"kod": "C_ITICI", "modul": "C"}, p["mal"]), Mesh()).ekle(y_)
    for a_, m_, mal_ in parcalar:
        if a_.startswith("C_ITICI__") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] == "KOL": HARIC.add(a_)
    _fT = lambda t: (_piv[0] + (it_s(t) - IT.S_HOME) * IT.U[0], _piv[1], _piv[2] + (it_s(t) - IT.S_HOME) * IT.U[1])
    _fR = lambda t: qax((IT.W[0], 0.0, IT.W[1]), it_aci(t))
    OZEL_T.append(dict(ad="C_ITICI_DONER__KOL", ebeveyn=None, T=tuple(c * MM for c in _fT(0.0)), tonlar=ton))
    kanal("C_ITICI_DONER__KOL", lambda t: tuple(c * MM for c in _fT(t)))
    kanal("C_ITICI_DONER__KOL", _fR, "rotation")
    KONTROL.append(("C_ITICI_DONER__KOL", lambda t: tuple(c * MM for c in _fT(t)), _fR, ton))
    IT.kur(IT.S_HOME, True)
    # v48 · fırın + giriş bandı ruloları KENDİ EKSENİNDE (ağ pivota göre yerel) · bant yüzey hızıyla · dünya koordinatı''')
# ---- ürün yolu taraması: çapraz itme + bantlar ----
degis('''    _kon = [(X_BC + TH.X_AKTARMA, ZT + (FT.Z_URUN_FIRIN - ZT) * k_ / 8.0, 139.5) for k_ in range(9)]
    _kon += [(float(x_), FT.urun_z(float(x_)), R_) for R_ in (139.5, 149.5) for x_ in range(2340, 4301, 10)]''',
      '''    _kon = [(IT.C0[0] + (IT.C1[0] - IT.C0[0]) * k_ / 17.0, IT.C0[1] + (IT.C1[1] - IT.C0[1]) * k_ / 17.0, R_) for R_ in (139.5, 149.5) for k_ in range(18)]   # v49: çapraz itme 10 mm adım
    _kon += [(float(x_), FT.urun_z(float(x_)), R_) for R_ in (139.5, 149.5) for x_ in range(2510, 4301, 10)]''')
degis('''    _stat = [(a_, sa) for a_, sa in _F] + [(c_, sc) for c_, sc in _DG if c_.startswith(("K:", "TOPPING"))]''',
      '''    _stat = [(a_, sa) for a_, sa in _F] + [(c_, sc) for c_, sc in _DG if c_.startswith(("K:", "TOPPING"))]
    IT.kur(IT.S_HOME, True)
    _stat += [("ITICI(ev):" + p["ad"], IT.dunya(p)) for p in IT.PARCALAR if p["grup"] != "KOL"]                 # v49: itici sabitleri + araba evde (çubuk hariç: ürünle birlikte gider)''')
# ---- İTİCİ DENETİMİ (fırın özetinden sonra) ----
degis('''    assert not _cak and not _YOL, "v48: cakisma / urun yolu bulgusu var"''',
      '''    assert not _cak and not _YOL, "v48: cakisma / urun yolu bulgusu var"
    # ================= v49 · İTİCİ DENETİMİ =================
    _DGI = []
    for p in TC.PARCALAR:
        if p["ad"].startswith("_bom") or p["ad"] in KAPAK or p["ad"] in AKTARMA_TP10 or not v1_kalir(p["ad"]) or grup_modul(p["ad"]) == "TABLA": continue
        _d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
        sh = p["wp"].val().translate(cq.Vector(X_BC + _d[0], H_B + _d[1], _d[2]))
        if p["ad"] == "cikis_yarigi_contasi": sh = YARIK_V2
        if sh.BoundingBox().xmax > 1900.0: _DGI.append(("TOPPING:" + p["ad"], sh))
    for p in _TABLA:
        for _ad_, _xk in (("park", TC.XC_TABLA), ("aktarma", TH.X_AKTARMA)):
            _DGI.append(("TABLA(%s):%s" % (_ad_, p["ad"]), p["wp"].val().translate(cq.Vector(X_BC + _xk - TC.XC_TABLA, H_B, 0.0))))
    for q in TU.P:
        if q["ad"].startswith(V3_CIKAN): continue
        sh = q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))
        if sh.BoundingBox().xmax > 1900.0: _DGI.append(("TOPPING2:" + q["ad"], sh))
    _DGI += [(a_, sa) for a_, sa in _F if sa.BoundingBox().xmin < 2700.0]
    _DGI += [(c_, sc) for c_, sc in _DG if c_.startswith("K:")]
    _cak_it = []
    for _kon_, _s_, _kal_ in (("EV", IT.S_HOME, True), ("SON", IT.S_END, False), ("ORTA", (IT.S_HOME + IT.S_END) / 2.0, False)):
        IT.kur(_s_, _kal_)
        for p in IT.PARCALAR:
            sa = IT.dunya(p)
            for c_, sc in _DGI:
                if _bbk(sa, sc):
                    v_ = _hacim(sa, sc)
                    if v_ > 1.0 or v_ < 0: _cak_it.append((round(v_, 1), "ITICI(%s):%s" % (_kon_, p["ad"]), c_))
    # pide geliş koridoru (park → aktarma, Ø300 × 28 + topping 5) ve disk süpürmesi ↔ itici (evde, kalkık) + destek
    IT.kur(IT.S_HOME, True)
    _kor = FT.kut(X_BC + TC.XC_TABLA - 150.0, IT.C0[0] + 150.0, P, P + 33.0, ZT - 150.0, ZT + 150.0).val()
    _disk = FT.kut(X_BC + TC.XC_TABLA - 170.0, IT.C0[0] + 170.0, P - 14.0, P, ZT - 170.0, ZT + 170.0).val()
    for p in IT.PARCALAR:
        sa = IT.dunya(p)
        for _ad_, _sw in (("PIDE KORIDORU", _kor), ("DISK SUPURMESI", _disk)):
            if _bbk(sa, _sw):
                v_ = _hacim(sa, _sw)
                if v_ > 1.0 or v_ < 0: _cak_it.append((round(v_, 1), "ITICI(ev):" + p["ad"], _ad_))
    # çubuk itme süpürmesi: inik çubuk 20 mm adımla (temas → son) ↔ TOPPING/F/K sabitleri (tabla aktarmada)
    _sup = 0
    for _s_ in [IT.S_TEMAS + 20.0 * i_ for i_ in range(int((IT.S_END - IT.S_TEMAS) // 20.0) + 1)] + [IT.S_END]:
        IT.kur(_s_, False); _sup += 1
        for p in IT.PARCALAR:
            if p["grup"] not in ("KOL", "ARABA"): continue
            sa = IT.dunya(p)
            for c_, sc in _DGI:
                if c_.startswith("TABLA(park)"): continue
                if _bbk(sa, sc):
                    v_ = _hacim(sa, sc)
                    if v_ > 1.0 or v_ < 0: _cak_it.append((round(v_, 1), "ITICI(s=%.0f):%s" % (_s_, p["ad"]), c_))
    IT.kur(IT.S_HOME, True)
    print("ITICI DENETIMI (gercek kati kesisimi > 1 mm3 · ev/son/orta ↔ TOPPING + tabla park/aktarma + F + K · pide koridoru · disk supurmesi · itme supurmesi %d konum): %s"
          % (_sup, "TEMIZ" if not _cak_it else "%d BULGU" % len(_cak_it)))
    for x_ in sorted(_cak_it, reverse=True)[:40]: print("   %10.1f mm3  %s  <->  %s" % x_)
    ITICI_OZET = ("itici ↔ TOPPING (tabla park + aktarma) + fırın + K gerçek katı kesişimi %s (ev · son · orta) · pide geliş koridoru ve disk süpürmesi temiz · inik çubuk itme süpürmesi %d konum · ürün yolu çapraz (18 + bantlar)"
                  % ("TEMİZ" if not _cak_it else "%d BULGU" % len(_cak_it), _sup))
    assert not _cak_it, "v49: itici cakismasi var"''')
# ---- çıktılar ----
s = s.replace('hat_v48.glb', 'hat_v49.glb').replace('hat_v48.usdz', 'hat_v49.usdz').replace('"hat_v48"', '"hat_v49"')
degis('pafta="HAT v48 (26 Eyl gece) · F = TP10 kesitli 1500 firin (firin_tp10_cad_v3: bant govde disina cikmaz, isitilan 1316, 4 urun) · kompresor firin ustunde · kutu yedegi 505 + 55 · TOPPING v24 (tekne 2500\'de biter) + v2 v6 (kaset yuvalari, kavrama, yalitim blogu, fitil) · K = kesme_cad_v1 · 1 tam animasyon · B = store_cad_v5 · E = kutu_cad_v3 · alt taban 123 · surec 1168", firin_denetim=FIRIN_OZET)',
      'pafta="HAT v49 (26 Eyl gece) · AKTARMA ITICISI itici_cad_v1 (SMC MY1B16-250 capraz 24,9°, pivotlu cubuk, destek plakasi) · F = TP10 kesitli 1500 firin v4 (havalandirmali raf) · kompresor firin ustunde · kutu yedegi 505 + 55 · TOPPING v24 + v2 v7 (katalog yay/pim, hac 7,0) · K = kesme_cad_v1 · 1 tam animasyon · B = store_cad_v5 · E = kutu_cad_v3 · alt taban 123 · surec 1168", firin_denetim=FIRIN_OZET, itici_denetim=ITICI_OZET)')
degis('print("ANA MONTAJ ANIMASYONU (v48):', 'print("ANA MONTAJ ANIMASYONU (v49):')
io.open(os.path.join(U, "hat_montaj_v49.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v49.py yazildi")
