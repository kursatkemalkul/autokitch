import io
P = "h2_topping_v1.py"
s = io.open(P, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
# 1) sıvı hattı: emiş yatayını kesmesin (önde z −660 yükselir, kasetin hemen altında arkaya döner)
rep('''           "sogutma_sivi_hatti": [(2013.0, 1050.0, -660.0), (2248.0, 1050.0, -660.0), (2248.0, 1050.0, -700.0), (2248.0, 1383.0, -700.0)]}''',
    '''           "sogutma_sivi_hatti": [(2013.0, 1070.0, -660.0), (2248.0, 1070.0, -660.0), (2248.0, 1360.0, -660.0), (2248.0, 1360.0, -700.0), (2248.0, 1383.0, -700.0)]}''')
# 2) kuru bölme tabanı yeniden (hat + tahliye delikleri v2 yerinde) · tabla boş sensörü sucuk iniş borusuyla birlikte +33
rep('''           "baglama_lamasi_3", "baglama_lamasi_4")''', '''           "baglama_lamasi_3", "baglama_lamasi_4", "kuru_bolme_tabani")
TC_KAYDIR = {"tabla_bos_sensoru": (DX_ALT, 0.0, 0.0), "sensor_braketi_tabla_bos": (DX_ALT, 0.0, 0.0)}   # sucuk iniş borusu +33 → sensör de sağına (v1 bağıl yeri)''')
rep('''        if a.startswith("fire_silecegi_"):''', '''        if a in TC_KAYDIR:
            TC.append(dict(p, sh=tasi(p["sh"], *TC_KAYDIR[a]), tur="kaydir")); _say(say, "kaydir"); continue
        if a.startswith("fire_silecegi_"):''')
rep('''    ek("evap_kaseti_tahliye_hortumu", boru(TAHLIYE_V2, 4.0), "silikon",''', '''    kt = kut(x0 + SAC, 2420.0, 1107.5, 1109.0, -828.5, -630.0)
    for x_, z_, r_ in ((2270.0, -700.0, 16.5), (2248.0, -660.0, 4.2), (2215.0, -815.0, 5.0)):
        kt = kt.cut(sily(x_, z_, r_, 1106.0, 1110.0))
    ek("kuru_bolme_tabani", kt, "sac", _bom("Kuru bölme tabanı 304 1,5", 1, "1211 × 198,5 · soğutma hatları + tahliye geçiş delikleri (lastik bilezikli)", "v2 · teknik bölmenin üstü"))
    ek("evap_kaseti_tahliye_hortumu", boru(TAHLIYE_V2, 4.0), "silikon",''')
# 3) sos / harç taban kontaları yeni (Ø42 hortum): v1'in Ø36 dirsek kontaları düşer
rep('''          "raf_gecis_contasi_sos_hortum", "raf_gecis_contasi_harc_hortum", "sos__agiz_90_derece", "harc__agiz_90_derece")''',
    '''          "raf_gecis_contasi_sos", "raf_gecis_contasi_harc", "sos__agiz_90_derece", "harc__agiz_90_derece")''')
# 4) taban: v1 kurgusu (raf delikleri + kaset U-yarığı + ön büküm çentiği + alt PU üst yarığı) · sabit iniş parçaları PU / alt sacta kutu delik
rep('''    alt_sac = kut(X0, X1, KY[0], KY[0] + 1.5, -628.5, ZF)
    alt_pu = kut(IX[0] + 3.0, IX[1] - 3.0, KY[0] + 1.5, 1149.0, -567.0, 20.0)
    raf = kut(IX[0], IX[1], 1149.0, 1152.0, -570.0, ZF)
    buk = [kut(IX[0], IX[1], KY[0] + 1.5, 1149.0, 20.0, ZF), kut(IX[0], IX[1], KY[0] + 1.5, 1149.0, -570.0, -567.0)]''',
    '''    alt_sac = kut(X0, X1, KY[0], KY[0] + 1.5, -628.5, ZF)
    alt_pu = kut(IX[0] + 3.0, IX[1] - 3.0, KY[0] + 1.5, 1149.0, -567.0, 20.0)
    raf = kut(IX[0], IX[1], 1149.0, 1152.0, -570.0, ZF)
    buk = [kut(IX[0], IX[1], KY[0] + 1.5, 1149.0, 20.0, ZF), kut(IX[0], IX[1], KY[0] + 1.5, 1149.0, -570.0, -567.0)]
    for k_ in ("KIYMA", "KUSBASI"):                                                              # UNO dirsekleri Ø36 ↔ konta ↔ raf deliği Ø42
        raf = raf.cut(sily(ISTASYON[k_], TU0.ZT, 21.0, 1148.0, 1153.0))
    for k_, x_ in X_YAYICI.items():                                                              # ürün hortumu Ø42 ↔ konta ↔ raf deliği Ø48
        raf = raf.cut(sily(x_, TU0.ZT, HORTUM_R + 3.0, 1148.0, 1153.0))
        ek("raf_gecis_contasi_%s" % k_, sily(x_, TU0.ZT, HORTUM_R + 3.0, 1149.0, 1152.0).cut(sily(x_, TU0.ZT, HORTUM_R, 1148.0, 1153.0)), "conta",
           "v2 · silikon grommet Ø48 / Ø42 · %s ürün hortumu alt kat tabanından yayıcıya iner" % k_)
    for _ad, _mod, _x0, _x1 in TU0.KASET:                                                        # kaset tüpü: delik Ø60 + öne açık U-yarık (yarık dili doldurur) · v1 ile aynı
        xc = (_x0 + _x1) / 2.0 + TU0.DX_DUNYA + DX_ALT; r_ = TU0.KAS_R[_mod][0]; kz = TU0.KAS_Z
        raf = raf.cut(sily(xc, kz, r_, 1148.0, 1153.0)).cut(kut(xc - r_, xc + r_, 1148.0, 1153.0, kz, ZF + 1.0))
        buk[0] = buk[0].cut(kut(xc - r_, xc + r_, 1143.0, 1150.0, 19.0, ZF + 1.0))
        alt_pu = alt_pu.cut(kut(xc - r_, xc + r_, 1143.0, 1150.0, kz - r_ - 3.0, 21.0))''')
rep('''        if a.startswith(("raf_gecis_contasi_", "raf_kaset_contasi_")):                           # konta = rafın deliği
            raf = raf.cut(kut(b.xmin, b.xmax, 1148.0, 1153.0, b.zmin, b.zmax)); continue
''', '''        if a.startswith(("raf_gecis_contasi_", "raf_kaset_contasi_")) or "yarik_dili" in a or a.endswith("__cikis_tupu"): continue   # raf delikleri yukarıda (v1 kurgusu)
''')
# 5) kovan delikleri TAM silindir (kovan içi boş: katısıyla kesince PU çekirdeği kalıyordu)
rep('''    for a, s in bul.items():
        if a.endswith("mil_gecis_kovani") or a.startswith("kovan_"):
            delik.append(s)''', '''    for a, s in bul.items():
        if a.endswith("mil_gecis_kovani") or a.startswith("kovan_"):
            b = s.BoundingBox()
            delik.append(silz((b.xmin + b.xmax) / 2.0, (b.ymin + b.ymax) / 2.0, max(b.xlen, b.ylen) / 2.0, -631.0, -569.0))''')
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
