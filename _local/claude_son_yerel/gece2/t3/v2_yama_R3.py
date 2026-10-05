import io, sys
f = sys.argv[1]
s = io.open(f, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a))
    s = s.replace(a, b)


rep('''    a = AST; t = a["t"]; R = 1.0; g = R + t''', '''    a = AST; t = a["t"]; R = R_GIDA; g = R + t                 # gıda: iç R ≥ 3 (standart) · arka flanşı raf (y < 1155) ve üst raf (1530–1580) hizasında kesik''')
rep('''            P = s.taban([(a["y0"], ZB + g), (YUST - g, ZB + g), (YUST - g, ZON - g), (a["y0"], ZON - g)], O=(1495.0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="sol")
            arka = P.flans(0, 20.0, yon=+1, son=YUST - g - 2112.0, ad="arka_flans")
            ust = P.flans(1, 20.0, yon=+1, bas=3.0, son=3.0, ad="ust_flans")
            on = P.flans(2, 20.0, yon=-1, bas=3.0, ad="on_flans")''',
    '''            P = s.taban([(a["y0"], ZB + g), (1530.0, ZB + g), (1580.0, ZB + g), (YUST - g, ZB + g), (YUST - g, ZON - g), (a["y0"], ZON - g)], O=(1495.0, 0, 0),
                        ex=(0, 1, 0), ey=(0, 0, 1), ad="sol")
            arka = P.flans(0, 20.0, yon=+1, bas=1155.0 - a["y0"], son=4.0, ad="arka_flans_alt")
            arka2 = P.flans(2, 20.0, yon=+1, bas=4.0, son=YUST - g - 2112.0, ad="arka_flans_ust")
            ust = P.flans(3, 20.0, yon=+1, bas=4.0, son=4.0, ad="ust_flans")
            on = P.flans(4, 20.0, yon=-1, bas=4.0, ad="on_flans")''')
rep('''            P = s.taban([(a["y0"], -(ZON - g)), (YUST - g, -(ZON - g)), (YUST - g, -(ZB + g)), (a["y0"], -(ZB + g))], O=(2441.0, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="sag")
            on = P.flans(0, 20.0, yon=-1, son=3.0, ad="on_flans")
            ust = P.flans(1, 20.0, yon=+1, bas=3.0, son=3.0, ad="ust_flans")
            arka = P.flans(2, 20.0, yon=+1, bas=YUST - g - 2112.0, ad="arka_flans")
        G.PANEL["astar_" + tr] = dict(yan=P, arka=arka, ust=ust, on=on, s=s)''',
    '''            P = s.taban([(a["y0"], -(ZON - g)), (YUST - g, -(ZON - g)), (YUST - g, -(ZB + g)), (1580.0, -(ZB + g)), (1530.0, -(ZB + g)), (a["y0"], -(ZB + g))],
                        O=(2441.0, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="sag")
            on = P.flans(0, 20.0, yon=-1, son=4.0, ad="on_flans")
            ust = P.flans(1, 20.0, yon=+1, bas=4.0, son=4.0, ad="ust_flans")
            arka2 = P.flans(2, 20.0, yon=+1, bas=YUST - g - 2112.0, son=4.0, ad="arka_flans_ust")
            arka = P.flans(4, 20.0, yon=+1, bas=4.0, son=1155.0 - a["y0"], ad="arka_flans_alt")
        G.PANEL["astar_" + tr] = dict(yan=P, arka=arka, arka2=arka2, ust=ust, on=on, s=s)''')
rep('''    A_ = G.PANEL["astar_sol"]["arka"]
    for y0, y1 in ((1336.5, 1498.5), (1580.5, 1638.5)):
        wrect(A_, 1501.5, 1516.0, y0, y1, ZB - 0.5, ZB + t + 0.5, tip="centik", parca="evaporatör kanal kovanı çentiği")''',
    '''    for y0, y1, fl in ((1336.5, 1498.5, "arka"), (1584.0, 1638.5, "arka2")):
        wrect(G.PANEL["astar_sol"][fl], 1501.5, 1516.0, y0, y1, ZB - 0.5, ZB + t + 0.5, tip="centik", parca="evaporatör kanal kovanı çentiği")''')
rep('''    P = s.taban([(1496.0, ZB + g), (2440.0, ZB + g), (2440.0, ZON - g), (1496.0, ZON - g)], O=(0, a["y1"], 0), ex=(1, 0, 0), ey=(0, 0, 1), ad="tavan")''',
    '''    P = s.taban([(1497.6, ZB + g), (2438.4, ZB + g), (2438.4, ZON - g), (1497.6, ZON - g)], O=(0, a["y1"], 0), ex=(1, 0, 0), ey=(0, 0, 1), ad="tavan")''')
rep('''    arka = P.flans(0, 20.0, yon=+1, bas=24.0, son=24.0, ad="arka_flans")
    on = P.flans(2, 18.0, yon=-1, bas=2.0, son=2.0, ad="on_flans")''', '''    arka = P.flans(0, 20.0, yon=+1, bas=22.4, son=22.4, ad="arka_flans")
    on = P.flans(2, 18.0, yon=-1, bas=2.0, son=2.0, ad="on_flans")''')
rep('''    P = s.taban([(1496.0, a["y0"]), (2440.0, a["y0"]), (2440.0, a["y1"] - t), (1496.0, a["y1"] - t)], O=(0, 0, a["zb"]), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")''',
    '''    P = s.taban([(1496.8, a["y0"]), (2439.2, a["y0"]), (2439.2, a["y1"] - 2.0), (1496.8, a["y1"] - 2.0)], O=(0, 0, a["zb"]), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")''')
rep('''    Ys = [1190.0, 1300.0, 1520.0, 1660.0, 1800.0, 1950.0, 2090.0]
    J = []
    for tr, xr in (("sol", 1507.0), ("sag", 2429.0)):
        for y in Ys: J.append(("arka_%s" % tr, G.PANEL["astar_arka"]["yan"], G.PANEL["astar_" + tr]["arka"], (xr, y, -570.0), (0, 0, -1.0), "kor"))''',
    '''    Ys = [1190.0, 1300.0, 1660.0, 1800.0, 1950.0, 2090.0]
    J = []
    for tr, xr in (("sol", 1507.0), ("sag", 2429.0)):
        for y in Ys: J.append(("arka_%s" % tr, G.PANEL["astar_arka"]["yan"], G.PANEL["astar_" + tr]["arka" if y < 1530 else "arka2"], (xr, y, -570.0), (0, 0, -1.0), "kor"))''')
# derz fitilleri: büküm boşluğunu kapatan üçgen (köşe noktaları iki yüzde)
rep('''    def fitil(ad, p0, p1, u, v, a_=3.0):
        p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); u = np.asarray(u, float) * a_; v = np.asarray(v, float) * a_''',
    '''    def fitil(ad, p0, p1, u, v, a_=1.0):
        p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); u = np.asarray(u, float) * a_; v = np.asarray(v, float) * a_''')
rep('''    for tr, x, u in (("sol", 1496.0, 1.0), ("sag", 2440.0, -1.0)):
        fitil("derz_arka_%s_alt" % tr, (x, 1152.0, -570.0), (x, 1533.0, -570.0), (u, 0, 0), (0, 0, 1.0))
        fitil("derz_arka_%s_ust" % tr, (x, 1576.0, -570.0), (x, 2137.0, -570.0), (u, 0, 0), (0, 0, 1.0))
        fitil("derz_tavan_%s" % tr, (x, 2140.0, -567.0), (x, 2140.0, 37.5), (u, 0, 0), (0, -1.0, 0))
    fitil("derz_arka_tavan", (1499.0, 2140.0, -570.0), (2437.0, 2140.0, -570.0), (0, -1.0, 0), (0, 0, 1.0))''',
    '''    for tr, x, u in (("sol", 1496.0, 1.0), ("sag", 2440.0, -1.0)):
        fitil("derz_arka_%s_alt" % tr, (x + 0.8 * u, 1152.0, -570.0), (x + 0.8 * u, 1533.0, -570.0), (3.0 * u, 0, 0), (-0.8 * u, 0, 3.0))
        fitil("derz_arka_%s_ust" % tr, (x + 0.8 * u, 1576.0, -570.0), (x + 0.8 * u, 2136.0, -570.0), (3.0 * u, 0, 0), (-0.8 * u, 0, 3.0))
        fitil("derz_tavan_%s" % tr, (x + 1.6 * u, 2140.0, -566.0), (x + 1.6 * u, 2140.0, 37.5), (3.0 * u, 0, 0), (-1.6 * u, -3.0, 0))
    fitil("derz_arka_tavan", (1500.0, 2140.0, -569.0), (2436.0, 2140.0, -569.0), (0, 0, 3.0), (0, -3.0, -1.0))''')
io.open(f, 'w', encoding='utf-8').write(s)
print('ok')
