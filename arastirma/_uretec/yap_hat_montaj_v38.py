# -*- coding: utf-8 -*-
"""hat_montaj_v37 -> v38 : E KUTU KATLAMA MODÜLÜ ANA MONTAJA (kutu_cad_v2) + ORTAK ANİMASYON · STEP ÇIKTISI KALDIRILDI

Kemal (25 Eyl 2026): "detaylar neden genel montajda gözükmüyor, illa kutuyu açacağım; o istasyonun detayları ana montajda da olsun."
  · E'nin 7 ölçü kutusu (E_KABIN, E_SARJOR, E_AGZ, E_TEPSI, E_KALIP, E_VAKUM, E_KART) yerine kutu_cad_v2'nin 217 parçası
    11 işlevsel birim olarak (durum GERCEK_KUTU) girer. E genişliği 830 → hat 5430 (PAFTA v8 henüz yok — Kemal onayı).
  · Animasyon: E'nin 20 sn'lik döngüsü (itici, piston, köprü, flap, kol, parmak, menteşeli karton, pizza) montaja girer.
    Dönen parçalar (kol, parmak, karton panelleri) için GLB'de menteşe düğümü + döndürme kanalı (v37 yazıcısı yalnız ötelemeydi).
    Ortak döngü 40 sn: çekmeceler 34,8 sn'de bir tur + bekleme, kutu modülü iki tur.
  · Kemal (25 Eyl): "SolidWorks için bir şey yapmayacağız" → HAT_vNN_YERLESIM.step yazımı kaldırıldı.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v37.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, "YOK/COK (%d): %s" % (s.count(a), a[:90])
    s = s.replace(a, b)


degis('"""v37 (24 Eyl 2026):', '''"""v38 (25 Eyl 2026): E KUTU KATLAMA = kutu_cad_v2 (11 birim, 830 genişlik, hat 5430) + montajda ortak animasyon (40 sn) · STEP çıktısı yok.
v37 (24 Eyl 2026):''')
degis("ÇIKTI: otonom/hat3d/hat_v37.glb + .usdz  ·  otonom/hat3d/durum.json (sayfa oradan okur)  ·  FULL_MAKINE/HAT_v37_YERLESIM.step (SolidWorks)",
      "ÇIKTI: otonom/hat3d/hat_v37.glb + .usdz  ·  otonom/hat3d/durum.json (sayfa oradan okur)  ·  (v38: SolidWorks STEP'i YAZILMAZ — Kemal 25 Eyl)")

# ---- yerlesim: E 830 ----
degis('''X_K, W_K, X_E, W_E = _g7["X_K"], _g7["W_K"], _g7["X_E"], _g7["W_E"]''',
      '''X_K, W_K, X_E, W_E = _g7["X_K"], _g7["W_K"], _g7["X_E"], _g7["W_E"]
# v38 · E = kutu_cad_v2: standart 32 × 32 × 4,2 kutunun açılımı 804 × 404 → 700'e sığmıyor, modül 830.
# PAFTA v7'de E hâlâ 700; pafta v8 Kemal'in onayını bekliyor. Model burada ÖNDEN gidiyor (bilerek).
W_E = 830.0''')
degis('''HAT_W = _g7["HAT"]                                                                       # 5300''',
      '''HAT_W = X_E + W_E                                                                        # v38: 5430 (pafta v7: 5300)''')

# ---- E birimleri: 7 ölçü kutusu yerine kutu_cad_v2 ----
a = s.index('birim("E_KABIN", ')
b = s.index('\n', s.index('birim("E_KART", ')) + 1
s = s[:a] + '''# --- E · KUTU KATLAMA MODÜLÜ (v38: GERÇEK üretim modeli kutu_cad_v2 — işlevsel birimlere ayrılır) ---
import kutu_cad_v2 as KC
KC.modul()
E_BIRIM = [
    ("E_GOVDE", "KUTU modülü gövdesi: 304 kabuk (saydam) · ayaklar · taban · ağız kirişi · şarjör yan kapısı", ("ayak_", "taban_sac", "plint_on", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "sarjor_yan_kapisi", "on_alt_sac", "on_ust_kapak", "agiz_ust_kirisi", "kose_dikme_")),
    ("E_SARJOR", "Şarjör + asansör: 567 kutu (1,6 mm) · Tr16×4 · 2 HGR15 · NEMA 23 · 2:1 GT3", ("kilavuz_", "sarjor_kapi_esigi", "karton_yigini", "asansor_")),
    ("E_BESLEYICI", "Besleyici itici: en üstteki blankı 411 mm öne sürer · 2 HGR15 · GT3 · NEMA 23", ("besleyici_", "itici_")),
    ("E_KALIP", "Zımba kalıbı + 4 çubuklu tepsi (robot çatalı aralardan) · arka ray · ön tarak · ön ray", ("kalip_", "tepsi_")),
    ("E_KOPRU", "Pizza köprüsü: katlamada 30 mm aşağıda · SFU1605 + NEMA 23 + 2 LM12UU", ("kopru_",)),
    ("E_PISTON", "Piston: 296 × 296 kafa · SFU1610 (üstten BK12) · 2 HGR15 · NEMA 23 · taban / kilit / kapak", ("piston_",)),
    ("E_PARMAK", "Devirme parmağı: iç ön paneli kutuya devirir · NEMA 23 + SureGear 10:1", ("devirme_parmagi", "parmak_")),
    ("E_KAPAK", "Kapak masası + U flap katlayıcı (SFU1605) + kapak kolu (NEMA 23 + SureGear 10:1)", ("kapak_", "flap_katlayici_", "kol_")),
    ("E_ELEKTRIK", "Pano: S7-1200 1214C + SM1221 + SM1222 · 7 × STP-DRV-4830 · Mean Well 24/48 V · sensörler", ("pano_", "din_rayi", "plc_", "guc_", "surucu_", "klemens_", "kablo_kanali", "sensor_")),
    ("E_KUTU", "Pizza kutusu 32 × 32 × 4,2 E-dalga: düz açılım 804 × 404 → katlanır (menteşeli paneller)", ("B_",)),
    ("E_PIZZA", "Pizza Ø300 (K plakasından kutuya kayar)", ("pizza_",)),
]
E_HARIC = ("robot_catal_", "robot_flansi", "REF_K_")          # robotun çatalı (R'nin aleti) ve K referansı montaja girmez
E_PARCA = {k: [] for k, _a, _o in E_BIRIM}
for _p in KC.PARCALAR:
    if _p["ad"].startswith(E_HARIC):
        continue
    for _k, _a, _o in E_BIRIM:
        if _p["ad"].startswith(_o):
            E_PARCA[_k].append(_p); break
    else:
        raise AssertionError("kutu_cad_v2 parcasi birimsiz kaldi: " + _p["ad"])
_W0 = KC.blank_dunya(0.0)
for _k, _a, _o in E_BIRIM:
    _bb = []
    for _p in E_PARCA[_k]:
        if "_kulp" in _p["ad"]:
            continue                                            # kapı tutamakları zarfın 18–22 mm dışına çıkar (tutamak)
        _sh = _p["wp"].val()
        if _p["grup"].startswith("B_"):
            _sh = KC.uygula(_sh, _W0[_p["grup"]])
        _bb.append(_sh.BoundingBox())
    _x = (X_E + min(q.xmin for q in _bb), X_E + max(q.xmax for q in _bb)); _y = (min(q.ymin for q in _bb), max(q.ymax for q in _bb))
    _z = (min(q.zmin for q in _bb), max(q.zmax for q in _bb))
    birim(_k, _a, "E", "GERCEK_KUTU", _x, _y, _z, "sac", "kutu_cad_v2.py", "hat/pack.html")
''' + s[b:]

# ---- GLB yazıcısı: menteşe düğümü (hiyerarşi) + döndürme/ölçek kanalı ----
degis('''ANIM = []                                                                                # v37: (dugum adi, zamanlar, oteleme) listesi''',
      '''ANIM = []                                                                                # v37: (dugum adi, zamanlar, oteleme) · v38: + yol (translation/rotation/scale)
OZEL = []                                                                                # v38: menteşeli düğümler: dict(ad, ebeveyn, T (m), tonlar {malzeme: Mesh (yerel)})''')
degis('''def glb_yaz(yol, parcalar, dokular):''', '''def glb_yaz(yol, parcalar, dokular, ozel=None):''')
degis('''    kullanilan = sorted(set(mal for _a, _m, mal in parcalar)); blob, views, accs, meshes, nodes = [], [], [], [], []; off = [0]''',
      '''    ozel = OZEL if ozel is None else ozel
    kullanilan = sorted(set(mal for _a, _m, mal in parcalar) | set(k for o in ozel for k in o["tonlar"])); blob, views, accs, meshes, nodes = [], [], [], [], []; off = [0]''')
degis('''    anim_sm, anim_ch = [], []                                                            # v37: cekmece calisma animasyonu
    if ANIM:
        ad2node = {n["name"]: i for i, n in enumerate(nodes)}
        for ad_, T, V in ANIM:
            if ad_ not in ad2node:
                continue
            vi = gomu(struct.pack("<%df" % len(T), *T))
            accs.append({"bufferView": vi, "componentType": 5126, "count": len(T), "type": "SCALAR", "min": [min(T)], "max": [max(T)]})
            vo = gomu(struct.pack("<%df" % (3 * len(V)), *[c for v_ in V for c in v_]))
            accs.append({"bufferView": vo, "componentType": 5126, "count": len(V), "type": "VEC3"})
            anim_sm.append({"input": len(accs) - 2, "output": len(accs) - 1, "interpolation": "LINEAR"})
            anim_ch.append({"sampler": len(anim_sm) - 1, "target": {"node": ad2node[ad_], "path": "translation"}})''',
      '''    # v38 · menteşeli düğümler: her biri kendi menteşe noktasında (T), çocukları ebeveyne göre; birden çok malzeme = birden çok primitive
    kok_dugum = list(range(len(nodes)))
    oz_idx = {}
    for o in ozel:
        prims = []
        for k_, m in sorted(o["tonlar"].items()):
            vp = gomu(struct.pack("<%df" % (3 * len(m.P)), *[c for p in m.P for c in p]), 34962)
            vn = gomu(struct.pack("<%df" % (3 * len(m.N)), *[c for nn in m.N for c in nn]), 34962)
            vi = gomu(struct.pack("<%dI" % len(m.I), *m.I), 34963)
            mn = [min(p[k] for p in m.P) for k in range(3)]; mx = [max(p[k] for p in m.P) for k in range(3)]
            accs.append({"bufferView": vp, "componentType": 5126, "count": len(m.P), "type": "VEC3", "min": mn, "max": mx})
            accs.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"})
            accs.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
            prims.append({"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}, "indices": len(accs) - 1, "material": kullanilan.index(k_)})
        n_ = {"name": o["ad"], "translation": list(o["T"])}
        if prims:
            meshes.append({"name": o["ad"], "primitives": prims}); n_["mesh"] = len(meshes) - 1
        oz_idx[o["ad"]] = len(nodes); nodes.append(n_)
    for o in ozel:
        if o["ebeveyn"]:
            nodes[oz_idx[o["ebeveyn"]]].setdefault("children", []).append(oz_idx[o["ad"]])
        else:
            kok_dugum.append(oz_idx[o["ad"]])
    anim_sm, anim_ch = [], []                                                            # v37: cekmece · v38: + kutu modulu
    if ANIM:
        ad2node = {n["name"]: i for i, n in enumerate(nodes)}
        for kayit in ANIM:
            ad_, T, V = kayit[0], kayit[1], kayit[2]
            yol_ = kayit[3] if len(kayit) > 3 else "translation"
            if ad_ not in ad2node:
                continue
            n_el = 4 if yol_ == "rotation" else 3
            vi = gomu(struct.pack("<%df" % len(T), *T))
            accs.append({"bufferView": vi, "componentType": 5126, "count": len(T), "type": "SCALAR", "min": [min(T)], "max": [max(T)]})
            vo = gomu(struct.pack("<%df" % (n_el * len(V)), *[c for v_ in V for c in v_]))
            accs.append({"bufferView": vo, "componentType": 5126, "count": len(V), "type": "VEC4" if n_el == 4 else "VEC3"})
            anim_sm.append({"input": len(accs) - 2, "output": len(accs) - 1, "interpolation": "LINEAR"})
            anim_ch.append({"sampler": len(anim_sm) - 1, "target": {"node": ad2node[ad_], "path": yol_}})''')
degis('''"scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes, "meshes": meshes,''',
      '''"scene": 0, "scenes": [{"nodes": kok_dugum}], "nodes": nodes, "meshes": meshes,''')
degis('''        g["animations"] = [{"name": "cekmece_calisma", "samplers": anim_sm, "channels": anim_ch}]''',
      '''        g["animations"] = [{"name": "hat_calisma", "samplers": anim_sm, "channels": anim_ch}]''')

# ---- STEP yok (Kemal 25 Eyl) ----
degis('''    t0 = time.time(); parcalar, asm, sayac, AG = [], cq.Assembly(name="HAT_v1"), {}, None''',
      '''    class _StepYok:                                                                      # v38: SolidWorks montajı YAZILMAZ (Kemal 25 Eyl)
        def add(self, *a, **k): pass
    t0 = time.time(); parcalar, asm, sayac, AG = [], _StepYok(), {}, None''')
degis('''    os.makedirs(STEP, exist_ok=True); asm.save(os.path.join(STEP, "HAT_v37_YERLESIM.step"))
    print("HAT_v37_YERLESIM.step · SolidWorks'te montaj olarak acilir · %s" % STEP)
''', '')

# ---- ana döngü: GERCEK_KUTU dalı ----
degis('''        elif b["durum"] == "GERCEK_STORE":''', '''        elif b["durum"] == "GERCEK_KUTU":
            ps = E_PARCA[b["kod"]]
            ton = {}
            for p in ps:
                g = p["grup"]
                kaba = p["ad"].startswith(("surucu_", "guc_")) or p["ad"].endswith(("_motoru", "_reduktoru"))
                if g in E_MENTESE or g.startswith("B_"):
                    continue                                                   # menteşeli düğümler aşağıda (e_mentese_dugumleri)
                sh = p["wp"].val().translate(cq.Vector(X_E, 0.0, 0.0))
                gg = "SABIT" if g in ("SABIT", "ASANSOR") else g
                ton.setdefault((p["mal"], gg), Mesh()).ekle(TC_AG(cq.Workplane(obj=sh), kaba))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            e_mentese_dugumleri(b, ps)
            b["parca"] = len(ps)
        elif b["durum"] == "GERCEK_STORE":''')

# ---- menteşeli düğüm kurucusu (glb_yaz'dan hemen önce) ----
degis('''def glb_yaz(yol, parcalar, dokular, ozel=None):''', '''E_MENTESE = ("KOL", "PARMAK")          # dönen makine grupları (kutu panelleri B_* ayrıca)
E_USDZ = []                             # v38: menteşeli düğümlerin t=0 dünya ağları (USDZ durağan kopya)


def e_mentese_dugumleri(b, ps):
    """kutu_cad_v2'nin dönen gruplarını montaj GLB'sine MENTEŞE DÜĞÜMÜ olarak ekler.
    Ağ düğümün menteşesine göre yerel (m); T = menteşe (ebeveyne göre). Kinematik KC'den (tek kaynak)."""
    def pivot(g):
        if g == "KOL": return (KC.KOL_P[0], KC.KOL_P[1], 0.0)
        if g == "PARMAK": return (KC.PARMAK_P[0], KC.PARMAK_P[1], 0.0)
        return KC.DUGUM[g][1]
    gruplar = []
    for p in ps:
        g = p["grup"]
        if (g in E_MENTESE or g.startswith("B_")) and g not in gruplar:
            gruplar.append(g)
    if b["kod"] == "E_KUTU":                                           # karton ağacının tüm düğümleri (boş ara düğüm kalmasın)
        gruplar = list(KC.DUGUM.keys())
    W0 = KC.blank_dunya(0.0)
    for g in gruplar:
        P = pivot(g)
        par = KC.DUGUM[g][0] if g.startswith("B_") else None
        Pp = pivot(par) if par else (-X_E, 0.0, 0.0)                    # kök düğüm dünyada: menteşe + hattaki E ofseti
        tonlar = {}
        for p in ps:
            if p["grup"] != g:
                continue
            m = TC_AG(p["wp"])                                              # E-yerel ağ (m)
            yerel = Mesh(); yerel.P = [(q[0] - P[0] * MM, q[1] - P[1] * MM, q[2] - P[2] * MM) for q in m.P]; yerel.N = list(m.N); yerel.I = list(m.I)
            tonlar.setdefault(mal_ad(b, p["mal"]), Mesh()).ekle(yerel)
            sh = p["wp"].val()
            sh = KC.uygula(sh, W0[g]) if g.startswith("B_") else sh
            E_USDZ.append(("%s__%s__%s_usdz" % (b["kod"], p["mal"], p["ad"]), TC_AG(cq.Workplane(obj=sh.translate(cq.Vector(X_E, 0.0, 0.0)))), mal_ad(b, p["mal"])))
        ad = "%s__%s" % (b["kod"], g)
        ebeveyn = ("E_KUTU__" + par) if par else None
        OZEL.append(dict(ad=ad, ebeveyn=ebeveyn, T=((P[0] - Pp[0]) * MM, (P[1] - Pp[1]) * MM, (P[2] - Pp[2]) * MM), tonlar=tonlar))


def glb_yaz(yol, parcalar, dokular, ozel=None):''')

# ---- birim listesi ve kontroller ----
degis('''    assert tuple(_bk["E_KABIN"]["y"]) == (0.0, H_MAK), "E kesilmemeli"''',
      '''    assert abs(_bk["E_GOVDE"]["y"][0]) < 0.01 and abs(_bk["E_GOVDE"]["y"][1] - H_MAK) < 0.01, "E kesilmemeli (tek parca 0-2030)"
    print("E KUTU MODULU (kutu_cad_v2): %d birim · %d parca · %d mentese dugumu · genislik %.0f · hat %.0f"
          % (len([b for b in B if b["durum"] == "GERCEK_KUTU"]), sum(len(v) for v in E_PARCA.values()), len(OZEL), W_E, HAT_W))''')
degis('''    _ZON = ("D_FIRIN_GOVDE", "E_AGZ")                      # zarf/bolge birimleri: icindekilerle kesismesi dogal''',
      '''    _ZON = ("D_FIRIN_GOVDE",)                              # zarf/bolge birimleri: icindekilerle kesismesi dogal''')
degis('''    _yeni = [b for b in B if b["modul"] in ("D", "K", "E") and not b["kod"].endswith("_KABIN")]''',
      '''    _yeni = [b for b in B if b["modul"] in ("D", "K", "E") and not b["kod"].endswith("_KABIN") and b["durum"] != "GERCEK_KUTU"]   # v38: E kendi taramasini yapiyor (kutu_cad_v2: makine 201 an + kutu 46 an + pizza 25 an = 0)''')

# ---- ortak animasyon: 40 sn (cekmeceler 1 tur + bekleme, kutu modulu 2 tur) ----
degis('''        T = [0.0, t0_, t0_ + _ac, t0_ + _ac + _bek, t0_ + 2 * _ac + _bek, _T_top]''',
      '''        T = [0.0, t0_, t0_ + _ac, t0_ + _ac + _bek, t0_ + 2 * _ac + _bek, T_HAT]''')
degis('''    print("ANIMASYON: %d cekmece sirayla · acilma %.1f sn · dongu %.1f sn · %d hareketli dugum" % (len(_sira), _ac, _T_top, len(ANIM)))''',
      '''    print("ANIMASYON: %d cekmece sirayla · acilma %.1f sn · cekmece turu %.1f sn · %d hareketli dugum" % (len(_sira), _ac, _T_top, len(ANIM)))
    # ---- v38 · KUTU MODULU: kutu_cad_v2 kinematigi (tek kaynak) 40 sn'ye iki tur ornekleniyor ----
    _n = int(round(T_HAT * 15.0)) + 1
    _TT = [min(T_HAT, i_ / 15.0) for i_ in range(_n)]
    def _te(t):
        return t % KC.DONGU
    _mm = lambda v: (v[0] * MM, v[1] * MM, v[2] * MM)
    _trs = {"ITICI": lambda t: (0.0, 0.0, KC.itici_dz(t)), "PISTON": lambda t: (0.0, KC.kafa(t) - KC.H_UST, 0.0),
            "KOPRU": lambda t: (0.0, KC.kopru_dy(t), 0.0), "KATLAYICI": lambda t: (0.0, KC.katlayici_dy(t), 0.0), "PIZZA": KC.pizza_trs}
    _say0 = len(ANIM)
    for a_, _m, _x in parcalar:
        if a_.startswith("E_") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] in _trs:
            f_ = _trs[a_.rsplit("__", 1)[1]]
            ANIM.append((a_, _TT, [_mm(f_(_te(t))) for t in _TT]))
            if a_.endswith("__PIZZA"):
                ANIM.append((a_, _TT, [(max(1e-4, KC.gorunur(_te(t))),) * 3 for t in _TT], "scale"))
    _oz = {o["ad"]: o for o in OZEL}
    for o in OZEL:
        g = o["ad"].split("__", 1)[1]
        if g == "KOL":
            ANIM.append((o["ad"], _TT, [KC.quat("z", KC.kol_beta(_te(t))) for t in _TT], "rotation"))
        elif g == "PARMAK":
            ANIM.append((o["ad"], _TT, [KC.quat("z", KC.parmak_psi(_te(t))) for t in _TT], "rotation"))
        elif g == "B_ROOT":
            T0 = o["T"]
            ANIM.append((o["ad"], _TT, [(T0[0] + KC.blank_acilar(_te(t))[0][0] * MM, T0[1] + KC.blank_acilar(_te(t))[0][1] * MM, T0[2] + KC.blank_acilar(_te(t))[0][2] * MM) for t in _TT]))
            ANIM.append((o["ad"], _TT, [(max(1e-4, KC.gorunur(_te(t))),) * 3 for t in _TT], "scale"))
        elif g.startswith("B_"):
            ANIM.append((o["ad"], _TT, [KC.quat(KC.DUGUM[g][2], KC.blank_acilar(_te(t))[1][g]) for t in _TT], "rotation"))
    print("ANIMASYON (v38): ortak dongu %.0f sn · cekmeceler 1 tur · kutu modulu %d tur · E kanali %d · toplam kanal %d"
          % (T_HAT, int(T_HAT // KC.DONGU), len(ANIM) - _say0, len(ANIM)))''')
degis('''ANIM = []                                                                                # v37: (dugum adi, zamanlar, oteleme) · v38: + yol (translation/rotation/scale)''',
      '''ANIM = []                                                                                # v37: (dugum adi, zamanlar, oteleme) · v38: + yol (translation/rotation/scale)
T_HAT = 40.0                                                                             # v38: ortak animasyon dongusu (cekmece turu 34,8 · kutu modulu 2 × 20)''')

# ---- USDZ: menteşeli düğümlerin durağan kopyası ----
degis('''    b2, prim, sorun, _u = usdz_yaz([os.path.join(OUT, "hat_v37.usdz")], "hat_v37", parcalar, dokular)''',
      '''    b2, prim, sorun, _u = usdz_yaz([os.path.join(OUT, "hat_v37.usdz")], "hat_v37", parcalar + E_USDZ, dokular)''')
degis('''        d1 = glb_yaz(os.path.join(OUT, dosya + ".glb"), alt, dokular)
        d2, _p, _s, _u2 = usdz_yaz([os.path.join(OUT, dosya + ".usdz")], dosya, alt, dokular)''',
      '''        oz_ = [o for o in OZEL if mk == "E"]
        d1 = glb_yaz(os.path.join(OUT, dosya + ".glb"), alt, dokular, ozel=oz_)
        d2, _p, _s, _u2 = usdz_yaz([os.path.join(OUT, dosya + ".usdz")], dosya, alt + ([x for x in E_USDZ] if mk == "E" else []), dokular)''')

degis('''pafta="HAT_ATOSA_TABLALI_v7 · v37 · B = store_cad_v2 · taban hizasi · surec 1168"''',
      '''pafta="HAT_ATOSA_TABLALI_v7 (+ E 830: pafta v8 bekliyor) · v38 · E = kutu_cad_v2 · B = store_cad_v2 · taban hizasi · surec 1168"''')

s = s.replace("hat_v37", "hat_v38").replace("HAT_v37", "HAT_v38")
io.open(os.path.join(U, "hat_montaj_v38.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v38.py yazildi")
