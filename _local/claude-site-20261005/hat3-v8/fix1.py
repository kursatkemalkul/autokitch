import io
p='yap_mek_v1.py'; s=io.open(p,encoding='utf-8').read()
a='''    g = _grup(grup) if birim not in ("E_KOSE", "E_PISTON", "E_KALIP", "E_KOPRU", "E_PARMAK", "E_BESLEYICI") or grup in ("VAC_Y", "ITICI") else None
    if birim == "E_BESLEYICI": g = "E/Besleyici"
    return g or mekanizma_bul(birim, None, mal, grup)'''
b='''    return mekanizma_bul(birim, None, mal, grup)                              # grup yalnız TOPPING'te anlamlı (ACICI · ARABA · PISTON_SOS …)'''
assert a in s; s=s.replace(a,b)
a='''    (_r(r"^CEKMECE"), "B/Çekmeceler"), (_r(r"^KESICI"), "K/Bıçak"), (_r(r"^ITICI"), "K/İtici"),
    (_r(r"^VAC|^ITICI"), "E/Besleyici"), (_r(r"^KAPAK_|^YAY_|^ALT_PANEL|^SERVIS_KAPAGI"), None),
]'''
b=''']'''
assert a in s; s=s.replace(a,b)
a='''                    # önceki satırın önek minimumu (k' <= k)
                    idx = np.arange(len(kol))
                    pmv = np.minimum.accumulate(dp)
                    am = np.zeros(len(kol), np.int64)
                    # önek argmin
                    cur = 0
                    best = dp[0]
                    for k in range(len(kol)):
                        if dp[k] < best: best = dp[k]; cur = k
                        am[k] = cur
'''
b='''                    pmv = np.minimum.accumulate(dp)                                # önek minimumu (k' <= k)
                    am = np.maximum.accumulate(np.where(dp <= pmv, ar, 0))          # önek argmin
'''
assert a in s; s=s.replace(a,b)
a='''                INF = np.inf; dp = np.full(len(kol), 0.0); geri = np.zeros((nb, len(kol)), np.int32)'''
b='''                dp = np.full(len(kol), 0.0); geri = np.zeros((nb, len(kol)), np.int32); ar = np.arange(len(kol))'''
assert a in s; s=s.replace(a,b)
io.open(p,'w',encoding='utf-8').write(s)
