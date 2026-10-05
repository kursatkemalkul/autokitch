# -*- coding: utf-8 -*-
import io, os
H3 = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\b3\arastirma\_uretec\h3"
P = os.path.join(H3, "h3_elk_ist_v1.py")
s = io.open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:90], s.count(a))
    s = s.replace(a, b)


# 1 · TOPPING araba zarfı: ölçülen parçalardan (araba plakası / kızak ayakları / kaset bandı + sarkan dönüş motoru), x 930 → aktarma 2500
rep('''TOPPING_ZARF = kut(780.0, 2620.0, 940.0, 1040.0, -515.0, 12.0)                               # araba + tabla + kaset (x boyunca)''',
    '''TOPPING_ZARF = kut(930.0, 2500.0, 912.0, 1045.0, -320.0, -20.0)                              # araba plakası + kızak ayakları + kaset (x 936 → aktarma)
TOPPING_ZARF_MOTOR = kut(1055.0, 2500.0, 898.0, 942.0, -200.0, -140.0)                       # tekneye sarkan dönüş motoru''')
rep('''    ER.ekli_ekle("YASAK_TOPPING_araba_zarfi", TOPPING_ZARF)''',
    '''    ER.ekli_ekle("YASAK_TOPPING_araba_zarfi", TOPPING_ZARF); ER.ekli_ekle("YASAK_TOPPING_donus_motoru_zarfi", TOPPING_ZARF_MOTOR)''')

# 2 · K süpürmeleri: kaba kutu yerine gerçek yörünge (kesme_cad_v11.grup_trs, 0,1 s örnek, yön değişim noktaları arası parça kutuları)
rep('''def _supurmeler():
    import json, io, os
    idx = json.load(io.open(os.path.join(EO.DD, "dunya.json"), encoding="utf-8"))
    G = {"%s|%s" % (i[0], i[1]): i[3] for i in idx}
    out = []
    for ad, s, b in EO.dokum():
        d = KS_SUPURME.get(G.get(ad))
        if d is None or not ad.startswith("K_"): continue
        out.append(("SUPURME_" + ad, kut(b[0] + d[0], b[1] + d[1], b[2] + d[2], b[3] + d[3], b[4] + d[4], b[5] + d[5])))
    return out''',
    '''def _yorunge(g):
    """grup öteleme yörüngesi → yön değiştirdiği noktalar (tekrarsız)"""
    import kesme_cad_v11 as K11
    P = []
    for i in range(0, 262):
        p = tuple(round(v, 1) for v in K11.grup_trs(g, i * 0.1))
        if not P or math.dist(p, P[-1]) > 0.05: P.append(p)
    anah = [P[0]]
    for i in range(1, len(P) - 1):
        a, b, c = anah[-1], P[i], P[i + 1]
        d1 = [b[k] - a[k] for k in range(3)]; d2 = [c[k] - b[k] for k in range(3)]
        cr = (d1[1] * d2[2] - d1[2] * d2[1], d1[2] * d2[0] - d1[0] * d2[2], d1[0] * d2[1] - d1[1] * d2[0])
        if math.sqrt(sum(v * v for v in cr)) > 1e-3 or sum(d1[k] * d2[k] for k in range(3)) < 0: anah.append(b)
    anah.append(P[-1])
    return anah


def _supurmeler():
    import json, io, os
    idx = json.load(io.open(os.path.join(EO.DD, "dunya.json"), encoding="utf-8"))
    G = {"%s|%s" % (i[0], i[1]): i[3] for i in idx}
    Y = {g: _yorunge(g) for g in KS_SUPURME}
    out = []
    for ad, s, b in EO.dokum():
        g = G.get(ad)
        if g not in Y or not ad.startswith("K_"): continue
        A = Y[g]
        for j, (p, q) in enumerate(zip(A[:-1], A[1:])):
            out.append(("SUPURME_%s_%d" % (ad, j), kut(b[0] + min(p[0], q[0]), b[1] + max(p[0], q[0]), b[2] + min(p[1], q[1]), b[3] + max(p[1], q[1]),
                                                       b[4] + min(p[2], q[2]), b[5] + max(p[2], q[2]))))
    return out''')

# 3 · yol bulma: gerçek denetimi geçemeyen voksel yolu daha geniş payla yeniden
rep('''        p, neden = EV.bul(a, b, r, bolge=bolge, haric=haric, h=h)
        if p is None: return None, neden
        ok, engel = ER.temiz(boru(p, r), haric)
        return (p, None) if ok else (None, "voksel yolu gerçek denetimde: " + str(engel))''',
    '''        neden = None
        for pay in (1.0, 3.0, 5.0):
            p, neden = EV.bul(a, b, r, bolge=bolge, haric=haric, h=h, pay=pay)
            if p is None: return None, neden
            ok, engel = ER.temiz(boru(p, r), haric)
            if ok: return p, None
            neden = "voksel yolu gerçek denetimde: " + str(engel)
        return None, neden''')
rep('''        pts = [tuple(S)]
        cur = tuple(S)
        if itme:
            c2 = list(S); c2[itme[0]] += itme[1]; cur = tuple(c2); pts.append(cur)''',
    '''        if itme:                                                              # kablo cihaz yüzünden 0,3 mm açıkta başlar (eğri yüz / döküm gürültüsü)
            S = list(S); S[itme[0]] += 0.3 * (1.0 if itme[1] > 0 else -1.0); S = tuple(S)
        pts = [tuple(S)]
        cur = tuple(S)
        if itme:
            c2 = list(S); c2[itme[0]] += itme[1]; cur = tuple(c2); pts.append(cur)''')
rep('''        for v, har in durak:
            p, neden = yol_bul(cur, v, r, haric=har, bolge=bolge, h=h)''',
    '''        for v, har in durak:
            if math.dist(cur, v) < 1e-6: continue
            p, neden = yol_bul(cur, v, r, haric=har, bolge=bolge, h=h)''')

# 4 · KLF6.6: rakordan sonra dik 30 mm (rakor gövdesinden uzaklaş) sonra pano
rep('''          via=[((1700.0, 1125.0, -805.0), ("TOPPING_MODUL|kuru_bolme_tabani",))], on=PANO_ON(1700.0, -800.0), bolge=BOLGE_KURU,''',
    '''          via=[((1700.0, 1140.0, -805.0), ("TOPPING_MODUL|kuru_bolme_tabani",))], on=PANO_ON(1700.0, -800.0), bolge=BOLGE_KURU,''')

# 5 · x eksen sensörleri: tekne ön şeridinde (y 902, üç şerit z −10 / −16 / −22) sola, arabanın dinlendiği yerin solunda (x 880) yukarı → A dağıtıcı kutusu
rep('''    BOLGE_TEKNE = (1040.0, 2468.5, 893.5, 1109.0, -828.5, 0.0)
    for j, (nm, S) in enumerate((("x_limit_sag", (2375.0, 926.0, -22.0)), ("x_home", (1086.0, 926.0, -22.0)), ("x_limit_sol", (1056.0, 926.0, -22.0)))):
        cihaz("TOPPING_sensor_%s" % nm, S, KD1(950.0 + 12.0 * j), 2.0, "C", itme=(1, 3.0), on=(2462.0, 950.0 + 12.0 * j, -808.0), bolge=BOLGE_TEKNE, h=5.0)
''', '')
rep('''    # A: emniyet sensörleri + ışık perdesi → A|TOPPING duvarında M12 dağıtıcı kutusu → tek kablo G7 rakoru → pano
    parca("A_sensor_dagitici_kutusu", kut(1408.0, 1436.0, 1545.0, 1607.0, -695.0, -665.0), "cihaz_koyu", "A",
          ("M12 pasif dağıtıcı kutusu 4 port (Murrelektronik Exact12 tipi) · A|TOPPING duvarına 2 vida", 1, "62 × 30 × 28", "VARSAYIM: föyden teyit"))''',
    '''    # A: emniyet sensörleri + ışık perdesi + TOPPING x eksen sensörleri → A|TOPPING duvarında M12 dağıtıcı kutusu (8 port) → tek kablo G7 rakoru → pano
    parca("A_sensor_dagitici_kutusu", kut(1408.0, 1436.0, 1545.0, 1655.0, -695.0, -665.0), "cihaz_koyu", "A",
          ("M12 pasif dağıtıcı kutusu 8 port (Murrelektronik Exact12 tipi) · A|TOPPING duvarına 2 vida", 1, "110 × 30 × 28", "VARSAYIM: föyden teyit"))''')
rep('''              bom=("Sensör kablosu M12 4/5 kutuplu PUR (A emniyet / ışık perdesi → dağıtıcı)", 4, "", "") if i == 0 else None)
''', '''              bom=("Sensör kablosu M12 4/5 kutuplu PUR (A emniyet / ışık perdesi → dağıtıcı)", 4, "", "") if i == 0 else None)
    BOLGE_A2 = (840.0, 1436.0, 893.5, 1860.5, -720.0, 60.0)
    for i, (nm, xs, zl) in enumerate((("x_limit_sag", 2375.0, -10.0), ("x_limit_sol", 1056.0, -16.0), ("x_home", 1086.0, -22.0))):
        xk = 1412.0 + 7.0 * i
        cihaz("TOPPING_sensor_%s" % nm, (xs, 920.0, -19.0), (xk, 1630.0, -664.8), 2.0, "C", itme=(2, 2.7),
              via=[(xs, 902.0, -16.0), (xs, 902.0, zl), (880.0, 902.0, zl), (880.0, 960.0, zl)], on=(xk, 1630.0, -640.0), bolge=BOLGE_A2, h=4.0)
''')

# 6 · PM1704: soketi üstte (M12) → üstten çık
rep('''    cihaz("K_yag_basinc_PM1704", (4225.0, 1698.7, -520.0), KT(9), 2.0, "K", itme=(1, -5.0), on=KT_ON(9), bolge=BOLGE_K)''',
    '''    cihaz("K_yag_basinc_PM1704", (4225.0, 1809.7, -520.0), KT(9), 2.0, "K", itme=(1, 5.0), on=KT_ON(9), bolge=BOLGE_K)''')
io.open(P, "w", encoding="utf-8").write(s)
print("tamam")
