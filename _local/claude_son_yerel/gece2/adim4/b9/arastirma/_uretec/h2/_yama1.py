import io
P = "h2_topping_v1.py"
s = io.open(P, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:60], s.count(a))
    s = s.replace(a, b)
rep("""    xb = (587.5 + 40.0 + 980.0) / 2.0 - 20.0 + 20.0 - 20.0
    xb = ((587.5 + 40.0) + 980.0) / 2.0 - 20.0                                                  # yerel 783,75 − 20 → 763,75
""", """    xb = ((587.5 + 40.0) + 980.0) / 2.0 - 20.0                                                  # 627,5 ile 980'in ortası 803,75 → lama 783,75–823,75 (yerel)
""")
rep("""            if (a[1] - RAF2[1]) * (b[1] - RAF2[0]) < 0 or min(a[1], b[1]) < RAF2[0] < max(a[1], b[1]):
""", """            if min(a[1], b[1]) < RAF2[0] and max(a[1], b[1]) > RAF2[1]:
""")
rep("""    for a, s in bul.items():
        b = s.BoundingBox()
        if not (b.ymin < 1152.0 - 0.1 and b.ymax > 1109.0 + 0.1 and b.xmin < IX[1] and b.xmax > IX[0] and b.zmax > -570.0 and b.zmin < ZF): continue
        kk = kut(b.xmin - 1.0, b.xmax + 1.0, b.ymin - 1.0, b.ymax + 1.0, b.zmin - 1.0, b.zmax + 1.0)
        if a.startswith(("raf_gecis_contasi_", "raf_kaset_contasi_")):
            raf = raf.cut(kk)
        else:
            alt_pu = alt_pu.cut(kk); alt_sac = alt_sac.cut(kk); raf = raf.cut(kk)
""", """    for a, s in bul.items():
        b = s.BoundingBox()
        if not (b.ymin < 1152.0 - 0.1 and b.ymax > 1109.0 + 0.1 and b.xmin < IX[1] and b.xmax > IX[0] and b.zmax > -570.0 and b.zmin < ZF): continue
        if a.startswith(("raf_gecis_contasi_", "raf_kaset_contasi_")):                           # konta = rafın deliği
            raf = raf.cut(kut(b.xmin, b.xmax, 1148.0, 1153.0, b.zmin, b.zmax)); continue
        dil = s.intersect(kut(b.xmin - 1.0, b.xmax + 1.0, KY[0] - 1.0, 1149.0, b.zmin - 1.0, b.zmax + 1.0))
        if dil.Volume() < 1e-3: continue
        d = dil.BoundingBox()                                                                    # yalnız alt PU + alt sacın içinden geçen kısım (+1 pay)
        kk = kut(d.xmin - 1.0, d.xmax + 1.0, KY[0] - 1.0, 1149.5, d.zmin - 1.0, d.zmax + 1.0)
        alt_pu = alt_pu.cut(kk); alt_sac = alt_sac.cut(kk)
""")
rep("""    ek("yalitim_blogu", pu, "pu",""", """    # kaset penceresi: iki POM kanalın dışında kalan boşluk PU ile dolar (v2: dönüş ALT katta, üfleme ÜST katta → aradan kısa devre olmamalı)
    kn_ = [bul[a].BoundingBox() for a in ("arka_hava_kanali_ust", "arka_hava_kanali_alt")]
    dol = kut(KAS_YUZ[0], KAS_YUZ[1], KAS_YUZ[2], KAS_YUZ[3], -628.5, -570.0)
    for b in kn_:
        dol = dol.cut(kut(b.xmin, b.xmax, b.ymin, b.ymax, -631.0, -569.0))
    ek("kaset_penceresi_dolgusu", dol, "pu", "v2 · kaset penceresinde kanalların dışı PU 57,5 · kanallar arası 20 mm bant (üst raf hizası) kapalı: üfleme (üst kat) ile dönüş (alt kat) arasında kısa devre yok")
    ek("yalitim_blogu", pu, "pu",""")
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
