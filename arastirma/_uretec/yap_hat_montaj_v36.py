# -*- coding: utf-8 -*-
"""hat_montaj_v35 -> v36 : B ÇEKMECE MODÜLÜ GERÇEK ÜRETİM MODELİ (store_cad_v1)

Kemal (24 Eyl 2026): "şu çekmeceleri detaylandırsana teknik resimdeki gibi"
  · v35'te B = 21 şeffaf kutu (v19 kolon yerleriyle bile tutmuyordu: 20/720/1420 · pafta 62,5/717,5/1372,5).
  · Artık store_cad_v1: sandviç gövde, 3 bölme, ön çerçeve, 21 contalı motorlu çekmece (ray + kayış + motor +
    avara + reed), ince tepsiler + toplar, içecek 2 kat, K4 (soğutma grubu + depo + temizlik nişi), K1 üstü kart bölmesi.
  · Her çekmece AYRI BİRİM (sayfada üstüne gelince adı çıkar); kasa, kart, soğutma, depo, temizlik ayrı birimler.
  · Eski B_SOGUTMA (K1 altı, v19) kaldırıldı: soğutma grubu paftadaki gibi K4 altında.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v35.py"), encoding="utf-8").read()

s = s.replace('"""v35 (24 Eyl 2026):', '''"""v36 (24 Eyl 2026): B ÇEKMECE MODÜLÜ GERÇEK (store_cad_v1): 21 contalı motorlu çekmece + K4 + kart bölmesi, her çekmece ayrı birim.
v35 (24 Eyl 2026):''', 1)

# ------------------------------------------------------------------ B blogu
a = s.index("# --- B · ÇEKMECELER (STORE, TOPPING'in altında) ---")
b = s.index("\n", s.index('birim("B_KABIN"')) + 1
YENI_B = r'''# --- B · ÇEKMECE MODÜLÜ (v36: GERÇEK üretim modeli store_cad_v1 — her çekmece ayrı birim) ---
import store_cad_v1 as SC
SC_OZET = {k: (t, n) for k, t, n, _u, _a in SC.modul()}
_SC_AD = {"B_KASA": "ÇEKMECE modülü gövdesi: sandviç kabuk + PU + 3 kolon bölmesi + ön çerçeve + plint",
          "B_KART": "K1 üstü kuru teknik bölme: B kartı + %d çekmece sürücüsü + 24 V güç kaynağı" % len(SC.CEK),
          "B_SOGUTMA": "Soğutma: ⅓ HP grup (K4 altı, ızgaralı kapak) + 3 evaporatör + fan",
          "B_DEPO": "K4 kaşar + sucuk deposu · kapaklı · +3 °C (içerik VARSAYIM)",
          "B_TEMIZLIK": "K4 temizlik malzemesi nişi · kapaklı"}
_TIP_AD = {"hamur": "taze pide", "lahm": "lahmacun", "icecek": "içecek + tatlı · 2 katlı"}
for _kod in dict.fromkeys(p["birim"] for p in SC.PARCALAR):
    _ps = [p for p in SC.PARCALAR if p["birim"] == _kod]
    _bb = [p["wp"].val().BoundingBox() for p in _ps]
    _x = (min(q.xmin for q in _bb), max(q.xmax for q in _bb)); _y = (min(q.ymin for q in _bb), max(q.ymax for q in _bb))
    _z = (min(q.zmin for q in _bb), max(q.zmax for q in _bb))
    if _kod in SC_OZET:
        _t, _n = SC_OZET[_kod]; _kol = _kod.split("_")[1]
        _ad = "%s · %s çekmecesi %s · %d %s · contalı · 24 V motorlu · strok %.0f" % (
            _kol, _TIP_AD[_t], _kod.rsplit("_", 1)[1], _n, "kutu" if _t == "icecek" else "top", SC.STROK)
    else:
        _ad = _SC_AD.get(_kod, _kod)
    birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "store_cad_v1.py", "")
'''
s = s[:a] + YENI_B + s[b:]

# ------------------------------------------------------------------ yapim dongusu: GERCEK_STORE dali
imza = '        elif b["durum"] == "GERCEK":\n'
assert s.count(imza) == 1
DAL = '''        elif b["durum"] == "GERCEK_STORE":
            ps = [p for p in SC.PARCALAR if p["birim"] == b["kod"]]
            ton = {}
            for p in ps:
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(p["wp"]))
                asm.add(p["wp"].val(), name="%s__%s" % (b["kod"], p["ad"]), color=cq.Color(*RENK.get(p["mal"], RENK["kutu"])))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(ps)
'''
s = s.replace(imza, DAL + imza, 1)

# ------------------------------------------------------------------ denetim: B ozeti
imza2 = "    # ---- v35 · SUREC KOTU + TABAN HIZASI + CAKISMA ----\n"
assert s.count(imza2) == 1
s = s.replace(imza2, '''    # ---- v36 · B CEKMECE MODULU ----
    _bs = [b for b in B if b["durum"] == "GERCEK_STORE"]
    print("B CEKMECE MODULU (store_cad_v1): %d birim · %d parca · %d cekmece" % (len(_bs), sum(b.get("parca", 0) for b in _bs), len(SC.CEK)))
    assert all(b["y"][1] <= H_B + 0.01 for b in _bs), "B tavani 1060'i asiyor"
''' + imza2, 1)

s = s.replace('pafta="HAT_ATOSA_TABLALI_v7 · v35 taban hizasi · surec 1168"', 'pafta="HAT_ATOSA_TABLALI_v7 · v36 · B = store_cad_v1 · taban hizasi · surec 1168"')
_e = 'for k_ in ("B_KABIN", "D_TABAN_KABIN", "K_TABAN_KABIN"):'
assert s.count(_e) == 1
s = s.replace(_e, 'for k_ in ("B_KASA", "D_TABAN_KABIN", "K_TABAN_KABIN"):', 1)       # v36: B kabini artik gercek kasa
s = s.replace("hat_v35", "hat_v36").replace("HAT_v35", "HAT_v36")
io.open(os.path.join(U, "hat_montaj_v36.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v36.py yazildi")
