import io
P = "h2_topping_v1.py"
s = io.open(P, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:60], s.count(a))
    s = s.replace(a, b)
rep("""        a = p["ad"]
        k = _ote(a, KURU_YENI)
        if k is not None:
            TC.append(dict(p, sh=tasi(p["sh"], *k), tur="kuru")); _say(say, "kuru_yeni_yer"); continue
        if a.startswith(TC_YENI):
            _say(say, "yeni_yerine_dusen"); continue
""", """        a = p["ad"]
        if a.startswith(TC_YENI) and not a.endswith("_hatti_ic"):                              # yeniden çizilenler (kasetin içindeki hat uçları kasetle gider)
            _say(say, "yeni_yerine_dusen"); continue
        k = _ote(a, KURU_YENI)
        if k is not None:
            TC.append(dict(p, sh=tasi(p["sh"], *k), tur="kuru")); _say(say, "kuru_yeni_yer"); continue
""")
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
