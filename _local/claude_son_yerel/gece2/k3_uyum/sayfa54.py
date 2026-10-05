import json, struct, sys, os, numpy as np
gi, V3 = sys.argv[1:3]
exec(open(r"../menu7/sayfa_json.py", encoding="utf-8").read().split("YM = os.path.join")[0].split("gi, ent, V3 = sys.argv[1:4]")[1])
YM = os.path.join(V3, "mekanizma_v3_8.json"); M = json.load(open(YM, encoding="utf-8"))
k = "TOPPING/Kuşbaşı"; print("kutu", M["kutu"][k], "->", KUTU[k])
fark = [(a, round(max(abs(x - y) for x, y in zip(M["kutu"][a], KUTU[a])), 3)) for a in M["kutu"] if a in KUTU and a != k and max(abs(x - y) for x, y in zip(M["kutu"][a], KUTU[a])) > 0.002]
print("diğer ünitelerde fark:", fark or "YOK")
M["kutu"][k] = KUTU[k]
M["surum"] += " · v9v (4 Eki 2026, adım 54): kuşbaşı hunisi tam dik kenar (x 1880)"
json.dump(M, open(YM, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
YP = os.path.join(V3, "parca_kutulari.json"); P = json.load(open(YP, encoding="utf-8"))
n = 0
for row in P["parca"]["TOPPING_MODUL"]:
    if row[0] == "kusbasi_hazne_bizim": print(row[2:8], end=" -> "); row[2:8] = [1753.0, 1880.0, 1284.0, 1499.0, -560.0, -120.0]; print(row[2:8]); n += 1
assert n == 1
json.dump(P, open(YP, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
