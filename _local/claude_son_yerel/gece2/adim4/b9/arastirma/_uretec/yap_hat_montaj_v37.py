# -*- coding: utf-8 -*-
"""hat_montaj_v36 -> v37 : B ÇEKMECE MODÜLÜ v2 (store_cad_v2) + ÇALIŞMA ANİMASYONU

Kemal (24 Eyl 2026): "fitil, çekmecelerin içi, nasıl çalıştığı (otomatik, tam açılacaktı), motor nerede —
SolidWorks'te tasarlamıştık, hepsini ekle, adapte et; üretilebilir, standart ürünler."
  · store_cad_v2: gerçek fitil profili (kanallı), yan bantta kayış (T4), Transmotec motor, Accuride ray,
    Littelfuse açık/kapalı reed, K1 üstünde Siemens PLC + Mean Well + Electromen + 21 röle, kablo kanalları,
    Secop yoğuşturucu ünite, ebm-papst fanlar, roll-bond evaporatör.
  · GLB'ye glTF ANİMASYONU: seçilen çekmeceler sırayla açılır (3,3 sn), bekler, kapanır — store sayfasında otomatik oynar.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v36.py"), encoding="utf-8").read()

s = s.replace('"""v36 (24 Eyl 2026):', '''"""v37 (24 Eyl 2026): B = store_cad_v2 (fitil, yan kayış, standart ürünler) + GLB'de çekmece çalışma animasyonu.
v36 (24 Eyl 2026):''', 1)

R = [
 ("import store_cad_v1 as SC", "import store_cad_v2 as SC"),
 ('''_SC_AD = {"B_KASA": "ÇEKMECE modülü gövdesi: sandviç kabuk + PU + 3 kolon bölmesi + ön çerçeve + plint",
          "B_KART": "K1 üstü kuru teknik bölme: B kartı + %d çekmece sürücüsü + 24 V güç kaynağı" % len(SC.CEK),
          "B_SOGUTMA": "Soğutma: ⅓ HP grup (K4 altı, ızgaralı kapak) + 3 evaporatör + fan",''',
  '''_SC_AD = {"B_KASA": "ÇEKMECE modülü gövdesi: sandviç kabuk + PU + 3 kolon bölmesi + ön çerçeve + plint",
          "B_ELEKTRIK": "K1 üstü pano: Siemens S7-1200 + Mean Well NDR-240-24 + Electromen EM-324C + %d seçici röle" % len(SC.CEK),
          "B_KABLO": "Kablo kanalları 40 × 25: her kolonda dikey + üstte yatay (bölmelerden geçer)",
          "B_SOGUTMA": "Soğutma: Secop CU KLF4.0CND R290 (K4 altı, ızgaralı kapak) + 3 roll-bond evaporatör + ebm-papst fan",'''),
 ('''        _ad = "%s · %s çekmecesi %s · %d %s · contalı · 24 V motorlu · strok %.0f" % (''',
  '''        _ad = "%s · %s çekmecesi %s · %d %s · fitilli · Transmotec motor + GT3 kayış · strok %.0f" % ('''),
 ('''    print("B CEKMECE MODULU (store_cad_v1): %d birim · %d parca · %d cekmece" % (len(_bs), sum(b.get("parca", 0) for b in _bs), len(SC.CEK)))''',
  '''    print("B CEKMECE MODULU (store_cad_v2): %d birim · %d parca · %d cekmece" % (len(_bs), sum(b.get("parca", 0) for b in _bs), len(SC.CEK)))'''),
 ('pafta="HAT_ATOSA_TABLALI_v7 · v36 · B = store_cad_v1 · taban hizasi · surec 1168"', 'pafta="HAT_ATOSA_TABLALI_v7 · v37 · B = store_cad_v2 · taban hizasi · surec 1168"'),
]
for a, b in R:
    assert s.count(a) == 1, "YOK: " + a[:70]
    s = s.replace(a, b, 1)

# ------------------------------------------------------------------ glTF animasyon destegi (glb_yaz)
a = '''    images, textures, doku_idx = [], [], {}'''
b = '''    anim_sm, anim_ch = [], []                                                            # v37: cekmece calisma animasyonu
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
            anim_ch.append({"sampler": len(anim_sm) - 1, "target": {"node": ad2node[ad_], "path": "translation"}})
    images, textures, doku_idx = [], [], {}'''
assert s.count(a) == 1
s = s.replace(a, b, 1)
a = '''    js = json.dumps(g, separators=(",", ":")).encode("utf-8")'''
b = '''    if anim_ch:
        g["animations"] = [{"name": "cekmece_calisma", "samplers": anim_sm, "channels": anim_ch}]
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")'''
assert s.count(a) == 1
s = s.replace(a, b, 1)
a = '''def glb_yaz(yol, parcalar, dokular):'''
b = '''ANIM = []                                                                                # v37: (dugum adi, zamanlar, oteleme) listesi


def glb_yaz(yol, parcalar, dokular):'''
assert s.count(a) == 1
s = s.replace(a, b, 1)

# ------------------------------------------------------------------ animasyon senaryosu (ciktilardan once kurulur)
a = '''    # ---- çıktılar ----'''
b = '''    # ---- v37 · CEKMECE CALISMA ANIMASYONU: sirayla ac (strok) · bekle · kapa ----
    _sira = ["CEK_K1_hamur_3", "CEK_K2_lahm_4", "CEK_K3_icecek_1", "CEK_K3_lahm_2"]
    _ac = SC.STROK / (127.0 / 60.0 * 3.141592653589793 * SC.KAS_PD)               # 3,3 sn (motor hizi)
    _bek, _ara = 1.5, 0.6
    _adim = _ac + _bek + _ac + _ara
    _T_top = _adim * len(_sira)
    _dz = SC.STROK * MM
    for i_, kod_ in enumerate(_sira):
        t0_ = i_ * _adim
        T = [0.0, t0_, t0_ + _ac, t0_ + _ac + _bek, t0_ + 2 * _ac + _bek, _T_top]
        V = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, _dz), (0.0, 0.0, _dz), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)]
        if t0_ == 0.0:
            T, V = T[1:], V[1:]
        for a_, _m, _x in parcalar:
            if a_.startswith(kod_ + "__") and a_.endswith("__CEKMECE"):
                ANIM.append((a_, T, V))
    print("ANIMASYON: %d cekmece sirayla · acilma %.1f sn · dongu %.1f sn · %d hareketli dugum" % (len(_sira), _ac, _T_top, len(ANIM)))
    assert ANIM, "animasyon icin hareketli dugum bulunamadi"

    # ---- çıktılar ----'''
assert s.count(a) == 1
s = s.replace(a, b, 1)

s = s.replace("hat_v36", "hat_v37").replace("HAT_v36", "HAT_v37")
io.open(os.path.join(U, "hat_montaj_v37.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v37.py yazildi")
