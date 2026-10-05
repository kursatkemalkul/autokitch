import io, sys
f = sys.argv[1]; d = sys.argv[2]
s = io.open(f, encoding='utf-8').read()
a = 'DIMPLE = []          #'
assert s.count(a) == 1
s = s.replace(a, '''# Kemal 4 Eki: "uzatacaksa olmasın" → iç sac yanlarının ön kenarı ters büküm: KAZ BOYNU BIÇAK KABUL (ayrı profil yok) · DFM'de hata sayılmaz
DFM_KABUL = {"astar_sol": {"abkant": "kabul edildi — kaz boynu bıçak (Kemal 4 Eki)"}, "astar_sag": {"abkant": "kabul edildi — kaz boynu bıçak (Kemal 4 Eki)"}}
''' + a)
# açık PU: yan iç sacın arka flanşı kesik olan bölgelerde (raf altı, üst raf hizası) arka iç sac ↔ yan iç sac boşluğu → silikon dolgu şeridi
a = '''    for ad, bx in (("derz_on_sol",'''
assert s.count(a) == 1
s = s.replace(a, '''    for tr, x0, x1 in (("sol", 1494.5, 1497.5), ("sag", 2438.5, 2441.5)):
        for k, (y0, y1) in enumerate(((AST["y0"], 1160.0), (1524.0, 1586.0))):
            sh = kutu(x0, x1, y0, y1, -571.5, -568.5).cut(*saclar).cut(*pul).clean()
            for j, so in enumerate(sh.Solids()):
                if so.Volume() < 1.0: continue
                p = S._bp("derz_kose_%s_%d_%d" % (tr, k, j), so, "gıda sınıfı silikon (FDA 21 CFR 177.2600)", "Köşe dolgu silikonu (yan iç sacın arka kenarı kesik bölgede)",
                          "%.1f cm³" % (so.Volume() / 1e3), "VMQ silikon", birim=BIRIM, mal="conta")
                p["tur"] = "silikon"; G.ELEMAN.append(p)
''' + a)
io.open(f, 'w', encoding='utf-8').write(s)
o = io.open(d, encoding='utf-8').read()
a = '''        h = [m for m in d if m["durum"] == "HATA"]; u = [m for m in d if m["durum"] == "UYARI"]'''
assert o.count(a) == 1
o = o.replace(a, '''        kb = getattr(MOD, "DFM_KABUL", {}).get(s.ad, {})
        for m in d:
            if m["durum"] == "HATA" and m["kural"] in kb: m["durum"] = "KABUL"; m["detay"] = kb[m["kural"]] + " · " + m["detay"]; log("        KABUL %s %s · %s" % (s.ad, m["kural"], kb[m["kural"]]))
''' + a)
io.open(d, 'w', encoding='utf-8').write(o)
print('ok')
