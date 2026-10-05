import io, sys
f = sys.argv[1]
s = io.open(f, encoding='utf-8').read()
i = s.index('def astar():'); j = s.index('def kovan_z(')
new = r'''def astar():
    """v2 D2 · bükümlü kenarlı iç sac (304 1,0 · R 1) + kör perçin + POM ısı kesici pul (TIG YOK) — sıra: arka PU → yan PU → tavan PU → sol / sağ
    astar (önden; arka kenar arka levhanın yivine, üst kenar tavan levhasının yivine) → tavan astarı (önden, yanların üst kenarının altına) → arka astar
    (önden, en son) → içeriden perçinler → ön çerçeve (çerçeveden gömme perçin) → derz silikonu"""
    a = AST; t = a["t"]; R = 1.0; g = R + t
    ZB, ZON, YUST = -573.0, 37.0, 2143.0                       # yan / tavan arka flanşı dış yüzü · ön flanş dış yüzü · yan üst flanş dış yüzü
    for tr in ("sol", "sag"):
        s = _sac("astar_%s" % tr, "ic", t=t, R=R, bolge="gida")
        if tr == "sol":
            P = s.taban([(a["y0"], ZB + g), (YUST - g, ZB + g), (YUST - g, ZON - g), (a["y0"], ZON - g)], O=(1495.0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="sol")
            arka = P.flans(0, 20.0, yon=+1, son=YUST - g - 2112.0, ad="arka_flans")
            ust = P.flans(1, 20.0, yon=+1, bas=3.0, son=3.0, ad="ust_flans")
            on = P.flans(2, 20.0, yon=-1, bas=3.0, ad="on_flans")
        else:
            P = s.taban([(a["y0"], -(ZON - g)), (YUST - g, -(ZON - g)), (YUST - g, -(ZB + g)), (a["y0"], -(ZB + g))], O=(2441.0, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="sag")
            on = P.flans(0, 20.0, yon=-1, son=3.0, ad="on_flans")
            ust = P.flans(1, 20.0, yon=+1, bas=3.0, son=3.0, ad="ust_flans")
            arka = P.flans(2, 20.0, yon=+1, bas=YUST - g - 2112.0, ad="arka_flans")
        G.PANEL["astar_" + tr] = dict(yan=P, arka=arka, ust=ust, on=on, s=s)
    A_ = G.PANEL["astar_sol"]["arka"]
    for y0, y1 in ((1336.5, 1498.5), (1580.5, 1638.5)):
        wrect(A_, 1501.5, 1516.0, y0, y1, ZB - 0.5, ZB + t + 0.5, tip="centik", parca="evaporatör kanal kovanı çentiği")
    s = _sac("astar_tavan", "ic", t=t, R=R, bolge="gida")
    P = s.taban([(1496.0, ZB + g), (2440.0, ZB + g), (2440.0, ZON - g), (1496.0, ZON - g)], O=(0, a["y1"], 0), ex=(1, 0, 0), ey=(0, 0, 1), ad="tavan")
    arka = P.flans(0, 20.0, yon=+1, bas=24.0, son=24.0, ad="arka_flans")
    on = P.flans(2, 18.0, yon=-1, bas=2.0, son=2.0, ad="on_flans")
    G.PANEL["astar_tavan"] = dict(yan=P, arka=arka, on=on, s=s)
    s = _sac("astar_arka", "ic", t=t, R=R, bolge="gida")
    P = s.taban([(1496.0, a["y0"]), (2440.0, a["y0"]), (2440.0, a["y1"] - t), (1496.0, a["y1"] - t)], O=(0, 0, a["zb"]), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
    _gecisler(P, a["zb"], kanal_delik=False)
    G.PANEL["astar_arka"] = dict(yan=P, s=s)
    Ys = [1190.0, 1300.0, 1520.0, 1660.0, 1800.0, 1950.0, 2090.0]
    J = []
    for tr, xr in (("sol", 1507.0), ("sag", 2429.0)):
        for y in Ys: J.append(("arka_%s" % tr, G.PANEL["astar_arka"]["yan"], G.PANEL["astar_" + tr]["arka"], (xr, y, -570.0), (0, 0, -1.0), "kor"))
        for z in (-520.0, -380.0, -240.0, -100.0, 10.0):
            J.append(("tavan_%s" % tr, G.PANEL["astar_tavan"]["yan"], G.PANEL["astar_" + tr]["ust"], (xr, 2140.0, z), (0, 1.0, 0), "kor"))
    for x in (1560.0, 1720.0, 1880.0, 2050.0, 2220.0, 2380.0):
        J.append(("arka_tavan", G.PANEL["astar_arka"]["yan"], G.PANEL["astar_tavan"]["arka"], (x, 2130.0, -570.0), (0, 0, -1.0), "kor"))
    Yon = [1200.0, 1340.0, 1480.0, 1620.0, 1760.0, 1900.0, 2040.0]
    for tr, xo in (("sol", 1485.0), ("sag", 2451.0)):
        for y in Yon: J.append(("cerceve_%s" % tr, G.PANEL["cerceve"], G.PANEL["astar_" + tr]["on"], (xo, y, ZFC + 1.0), (0, 0, -1.0), "havsa"))
    for x in (1560.0, 1720.0, 1880.0, 2050.0, 2220.0, 2380.0):
        J.append(("cerceve_tavan", G.PANEL["cerceve"], G.PANEL["astar_tavan"]["on"], (x, 2150.0, ZFC + 1.0), (0, 0, -1.0), "havsa"))
    n = 0
    for ad, A, B, p, d, tip in J:
        _percin(A, B, np.asarray(p, float), np.asarray(d, float), tip, "astar_percin_%s_%d" % (ad, n)); n += 1
    G.NOT.append("v2 D2 · iç sac 4 bükümlü sac, %d perçin (ISO 15983 Ø3,2 içeriden · ISO 15984 havşa Ø3,2 çerçeveden) + %d POM-C ısı kesici pul Ø9 × 1 · TIG yok" % (n, n))


def _percin(A, B, p, d, tip, ad):
    """A (baş tarafı) · 1,0 POM pul · B · p: baş tarafı dış yüz noktası · d: içeri"""
    tA, tB = A.sac.t, B.sac.t
    wdelik(A, tuple(p), 3.3, tip="kor_percin", parca="ISO 15983 / 15984 Ø3,2 perçin deliği")
    wdelik(B, tuple(p + d * (tA + 1.0)), 3.3, tip="kor_percin", parca="ISO 15983 / 15984 Ø3,2 perçin deliği")
    kav = tA + 1.0 + tB
    pul = cq.Solid.makeCylinder(4.5, 1.0, V(*(p + d * tA)), V(*d)).cut(cq.Solid.makeCylinder(1.7, 3.0, V(*(p + d * (tA - 1.0))), V(*d)))
    if tip == "havsa":
        bas = cq.Solid.makeCone(3.0, 1.6, 1.4, V(*p), V(*d))
        DIMPLE.append((A.sac.ad, "kes", bas.fuse(cq.Solid.makeCylinder(3.0, 1.0, V(*(p - d * 1.0)), V(*d)))))
        pul = pul.cut(bas)
        sh = bas.fuse(cq.Solid.makeCylinder(1.57, 6.0, V(*p), V(*d))).fuse(cq.Solid.makeCylinder(2.16, 1.2, V(*(p + d * kav)), V(*d))).clean()
        pr = S._bp(ad, sh, "ISO 15984", "Havşa başlı kör perçin Ø3,2 × 6 A2/A2 (çerçeve dış yüzüyle aynı düzlem · kapak fitili oturur)", "delik Ø3,3 · havşa 90°",
                   "A2/A2", birim=BIRIM, meta=dict(cap=3.2, boy=6, delik=3.3, kavrama=kav))
    else:
        pr = S.kor_percin(3.2, 8, tuple(p), tuple(d), ad=ad, birim=BIRIM, kavrama=kav)
        pr["bom"] = ("Kör perçin Ø3,2 × 8 bombe baş A2/A2 · kapalı uçlu (gıda tarafı sızdırmaz)",) + tuple(pr["bom"][1:])
    _eleman(pr)
    pp = S._bp(ad + "_pul", pul.clean(), "POM-C (FDA) · zımba", "Isı kesici ara pul Ø9 × 1 POM-C (iç sac ↔ dış parça arası soğuk köprü kesici)",
               "Ø9 / Ø3,4 × 1", "POM-C", birim=BIRIM, mal="pom")
    pp["tur"] = "baglanti"; _eleman(pp, mal="pom")


def derz_silikonu():
    """gıda tarafı iç köşeler 3 × 3 üçgen fitil + ön derz (iç sacın ön bükümü ↔ ön çerçeve arkası) dolgu · on_cerceve'den sonra çağrılır"""
    def fitil(ad, p0, p1, u, v, a_=3.0):
        p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); u = np.asarray(u, float) * a_; v = np.asarray(v, float) * a_
        w = cq.Wire.makePolygon([V(*p0), V(*(p0 + u)), V(*(p0 + v))], close=True)
        sh = cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), [], V(*(p1 - p0)))
        p = S._bp(ad, sh, "gıda sınıfı silikon (FDA 21 CFR 177.2600)", "Derz silikonu 3 × 3 (gıda tarafı iç köşe)", "%.0f mm" % np.linalg.norm(p1 - p0),
                  "VMQ silikon", birim=BIRIM, mal="conta")
        p["tur"] = "silikon"; G.ELEMAN.append(p)
    for tr, x, u in (("sol", 1496.0, 1.0), ("sag", 2440.0, -1.0)):
        fitil("derz_arka_%s_alt" % tr, (x, 1152.0, -570.0), (x, 1533.0, -570.0), (u, 0, 0), (0, 0, 1.0))
        fitil("derz_arka_%s_ust" % tr, (x, 1576.0, -570.0), (x, 2140.0, -570.0), (u, 0, 0), (0, 0, 1.0))
        fitil("derz_tavan_%s" % tr, (x, 2140.0, -570.0), (x, 2140.0, 37.5), (u, 0, 0), (0, -1.0, 0))
    fitil("derz_arka_tavan", (1496.0, 2140.0, -570.0), (2440.0, 2140.0, -570.0), (0, -1.0, 0), (0, 0, 1.0))
    saclar = [s.kati() for s in G.SAC if s.ad.startswith(("astar", "on_cerceve"))]
    pul = [e["sh"] for e in G.ELEMAN if e["ad"].startswith("astar_percin")]
    for ad, bx in (("derz_on_sol", kutu(1493.5, 1496.0, 1152.0, 2140.0, 34.0, ZFC)), ("derz_on_sag", kutu(2440.0, 2442.5, 1152.0, 2140.0, 34.0, ZFC)),
                   ("derz_on_tavan", kutu(1496.0, 2440.0, 2140.0, 2142.5, 34.0, ZFC))):
        sh = bx.cut(*saclar).cut(*pul).clean()
        for k, so in enumerate(sh.Solids()):
            if so.Volume() < 1.0: continue
            p = S._bp("%s_%d" % (ad, k), so, "gıda sınıfı silikon (FDA 21 CFR 177.2600)", "Ön derz silikonu (iç sac ön bükümü ↔ ön çerçeve arkası)",
                      "%.1f cm³" % (so.Volume() / 1e3), "VMQ silikon", birim=BIRIM, mal="conta")
            p["tur"] = "silikon"; G.ELEMAN.append(p)


'''
s = s[:i] + new + s[j:]
io.open(f, 'w', encoding='utf-8').write(s)
print('ok')
