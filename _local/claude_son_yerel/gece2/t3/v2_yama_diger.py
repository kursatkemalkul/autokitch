import io, sys
f = sys.argv[1]
s = io.open(f, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)


# ---------------- kuru bölme tabanı: kanal deliği + kapak + evaporatör ayakları
rep('''    for x, z, d in KUR_TABAN_DELIK: wdelik(P, (x, Y_SO - T, z), d, tip="rakor_deligi", parca="kablo / tahliye rakoru geçişi (v8zq)")
    G.PANEL["kuru_taban"] = P
''', '''    for x, z, d in KUR_TABAN_DELIK: wdelik(P, (x, Y_SO - T, z), d, tip="rakor_deligi", parca="kablo / tahliye rakoru geçişi (v8zq)")
    G.PANEL["kuru_taban"] = P
    kanal_ve_ayak(P)
''')
rep('''# =====================================================================================================================================
# 4 · KAIDE_C''', '''def kanal_ve_ayak(P):
    """v2 D4 · kondenser kanalı geçiş deliği + kapak · v2 D3 · evaporatör ayakları (kuru bölme tabanına PEM SP-M5)"""
    x0, x1, z0, z1 = KANAL_DELIK
    wrect(P, x0, x1, Y_SO - T, Y_SO, z0, z1, r=3.0, tip="kanal_gecisi", parca="kondenser kanalı (dirsekli boru) dikey iniş deliği 135 × 33")
    s = _sac("kanal_gecis_kapagi", "dis")
    a0, a1, b0, b1 = KANAL_KAPAK
    Q = s.taban([(a0, -b1), (a1, -b1), (a1, -(z1 - 0.5)), (2240.5, -(z1 - 0.5)), (2240.5, -(z0 + 0.5)), (a1, -(z0 + 0.5)), (a1, -b0), (a0, -b0)],
                O=(0, Y_SO, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="kapak")          # sağdan açık yarık: kanal borusunun dikey kolu çevresinde sola sürülür
    for x, z in KANAL_KAPAK_M5:
        b_ = S.vidali_birlesim(Q, P, (x, Y_SO + T, z), "pem_somun", dis="M5", vida_std="ISO7380", ad="kanal_kapagi_%d" % int(x), birim=BIRIM)
        for q in b_["parcalar"]: _eleman(q)
    G.PANEL["kanal_kapak"] = Q
    for i, (xa, yt) in enumerate(EVAP_AYAK):
        s = _sac("evaporator_ayagi_%d" % i, "braket", t=2.5)
        g = s.R + s.t
        A = s.taban([(xa, Y_SO + g), (xa + 30.0, Y_SO + g), (xa + 30.0, yt), (xa, yt)], O=(0, 0, ZAI), ex=(1, 0, 0), ey=(0, 1, 0), ad="dik")
        ay = A.flans(0, 30.0, yon=+1, ad="taban_ayak")
        b_ = S.vidali_birlesim(ay, P, (xa + 15.0, Y_SO + 2.5, ZAI + 17.0), "pem_somun", dis="M5", vida_std="ISO7380", ad="evaporator_ayak_%d" % i, birim=BIRIM)
        for q in b_["parcalar"]: _eleman(q)
    G.NOT.append("v2 D3 · evaporatör ayağı 4 × (2,5 mm L, eski sekme düzleminde, kaset gövdesine üreticide kaynaklı) → kuru bölme tabanına ISO 7380 M5 → PEM SP-M5 · "
                 "v2 D4 · kondenser kanalı deliği 135 × 33 + geçiş kapağı (2 × ISO 7380 M5 → tabanda PEM SP-M5)")


# =====================================================================================================================================
# 4 · KAIDE_C''')
# ---------------- T1 · TOPPING → B pulu ISO 7092
rep('''        pu = S.pul("DIN9021", "M8", (x, yk, z), (0, 1.0, 0), ad="arayuz_kb_%d_%d_pul" % (int(x), int(-z)), birim=BIRIM)
        vd = S.vida("ISO4762", "M8", 25, (x, yk + 2.0, z), (0, -1.0, 0), ad="arayuz_kb_%d_%d" % (int(x), int(-z)), birim=BIRIM)''',
    '''        pu = S._bp("arayuz_kb_%d_%d_pul" % (int(x), int(-z)), S._tasi(S._halka(7.5, 4.2, 1.6), S._cerceve((x, yk, z), (0, 1.0, 0))), "ISO 7092",
                   "Küçük seri pul M8 (Ø16 servis deliğinden geçer)", "8,4 / 15 × 1,6", "A2", birim=BIRIM, meta=dict(dis="M8", d1=8.4, d2=15.0, h=1.6))
        vd = S.vida("ISO4762", "M8", 25, (x, yk + 1.6, z), (0, -1.0, 0), ad="arayuz_kb_%d_%d" % (int(x), int(-z)), birim=BIRIM)''')
# ---------------- govde_parcalari: dimple / havşa (DIMPLE) uygula
rep('''    havsa = [e["sh"] for e in G.ELEMAN if e["ad"].startswith("servis_arka_") and e["ad"].endswith("_vida")]   # çökertme havşa: servis sacı + dönüşü baş konisi kadar
    for p in L:
        sh = p.get("sh") if p.get("sh") is not None else p["wp"].val()
        if p.get("tur") == "sac" and havsa:
            bb = sh.BoundingBox(); kes = [h for h in havsa if _ic(h.BoundingBox(), bb) and sh.intersect(h).Volume() > 1e-3]
            if kes:
                sh = sh.cut(*kes).clean()
                if sh.ShapeType() != "Solid" and len(sh.Solids()) == 1: sh = sh.Solids()[0]''',
    '''    DM = {}
    for sad, isl, k in DIMPLE: DM.setdefault(sad, []).append((isl, k))
    for p in L:
        sh = p.get("sh") if p.get("sh") is not None else p["wp"].val()
        if p.get("tur") == "sac" and p["ad"] in DM:                       # v2: çökertme (dimple) / havşa — lazer + delik + büküm SONRASI pres
            kes = [k for i_, k in DM[p["ad"]] if i_ == "kes"]; ek = [k for i_, k in DM[p["ad"]] if i_ == "ekle"]
            if kes: sh = sh.cut(*kes)
            if ek: sh = sh.fuse(*ek)
            sh = sh.clean()
            if sh.ShapeType() != "Solid" and len(sh.Solids()) == 1: sh = sh.Solids()[0]''')
# ---------------- kur(): derz silikonu (PU'dan önce) · DIMPLE sıfırla
rep('''    G.PANEL, G.PROF = {}, {}
    _FHP.clear()''', '''    G.PANEL, G.PROF = {}, {}
    _FHP.clear(); DIMPLE.clear()''')
rep('''    gida_dolgulari()
    pu_bloklari()''', '''    gida_dolgulari()
    derz_silikonu()
    pu_bloklari()''')
# ---------------- PU: soğuk duvar → 4 kesilmiş levha + 0,5 mm yapıştırıcı
rep('''    G.PU = out
    return out''', '''    G.PU = levhalar(out)
    return G.PU


PU_KES = [("arka", [((-1e4, -1e4, -1e4), (1e4, 1e4, -571.0))]),
          ("sol", [((-1e4, -1e4, -571.0), (1495.0, 1e4, 1e4)), ((1495.0, -1e4, -571.0), (1968.0, 2140.5, 1e4))]),
          ("sag", [((2441.0, -1e4, -571.0), (1e4, 1e4, 1e4)), ((1968.0, -1e4, -571.0), (2441.0, 2140.5, 1e4))]),
          ("tavan", [((1495.0, 2140.5, -571.0), (2441.0, 1e4, 1e4))])]
YAP = {"sol": (0, XI0, XI0 + 0.5), "sag": (0, XI1 - 0.5, XI1), "tavan": (1, YTI - 0.5, YTI), "arka": (2, Z_SA + T, Z_SA + T + 0.5)}
TRAD = {"arka": "arka", "sol": "sol", "sag": "sağ", "tavan": "tavan"}


def levhalar(out):
    """v2 D2 · yerinde köpük YOK: soğuk oda duvar yalıtımı ölçüsünde kesilmiş 4 PU levha (yüzey yüzey) + dış saca 0,5 mm yapıştırıcı · flanş / perçin / pul
    yuvaları levhada açık (köpük bloğu sacların, perçinlerin ve pulların çıkarılmış hâlidir)"""
    sd = [p for p in out if p["ad"].startswith("pu_soguk_duvar")]
    kalan = [p for p in out if not p["ad"].startswith("pu_soguk_duvar")]
    blok = sd[0]["sh"]
    for p in sd[1:]: blok = blok.fuse(p["sh"])
    yeni = []
    for ad, kutular in PU_KES:
        bx = kutu(*[v for ab in zip(*kutular[0]) for v in ab])
        for lo, hi in kutular[1:]: bx = bx.fuse(kutu(*[v for ab in zip(lo, hi) for v in ab]))
        L = blok.intersect(bx).clean()
        e, a0, a1 = YAP[ad]
        lo = [-1e4] * 3; hi = [1e4] * 3; lo[e] = a0; hi[e] = a1
        sl = kutu(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
        Y = L.intersect(sl).clean(); L = L.cut(sl).clean()
        for k, so in enumerate(L.Solids()):
            if so.Volume() < 20.0: continue
            nm = "pu_levha_%s" % ad + ("" if k == 0 else "_%d" % k)
            yeni.append(dict(ad=nm, wp=cq.Workplane("XY").add(so), sh=so, mal="pu", birim=BIRIM, grup="SABIT", kaynak=SURUM, tur="pu",
                             bom=("PU levha %s 40 kg/m³ (λ 0,022) · ölçüsünde kesilmiş, flanş / perçin yuvaları açık" % TRAD[ad], 1, "%.1f dm³" % (so.Volume() / 1e6),
                                  "CNC kesim + yuva frezesi", "ÜRETİM"), meta=dict(tur="pu", hacim_dm3=round(so.Volume() / 1e6, 3))))
        for k, so in enumerate(Y.Solids()):
            if so.Volume() < 1.0: continue
            p = S._bp("yapistirici_%s" % ad + ("" if k == 0 else "_%d" % k), so, "PU levha yapıştırıcısı (tek bileşenli PU, gıda dışı bölge)",
                      "Yapıştırıcı katmanı %s · PU levha → dış sac 0,5 mm" % TRAD[ad], "%.1f cm³" % (so.Volume() / 1e3), "PU yapıştırıcı", birim=BIRIM, mal="conta")
            p["tur"] = "silikon"; G.ELEMAN.append(p)
    return kalan + yeni''')
io.open(f, 'w', encoding='utf-8').write(s)
print('ok')
