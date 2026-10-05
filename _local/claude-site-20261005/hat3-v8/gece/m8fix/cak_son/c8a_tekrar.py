# hata veren çiftleri tek süreçte yeniden çalıştır -> parca_99.json
import os, sys, json, glob
import c8a_ortak as M
J, B, _ = M.tum_bilesenler(False)
H = []
for f in sorted(glob.glob("parca_[0-2]*.json")): H += json.load(open(f))["hata"]
out = dict(cak=[], inc=[], temas=0, yavas=[], hata=[])
for i, j, _ in H:
    i, j = int(i), int(j)
    try: r = M.G.cift(B[i], B[j])
    except Exception as e: out["hata"].append([i, j, str(e)]); continue
    if r is None: continue
    if r[0] == "CAKISMA": out["cak"].append(dict(i=i, j=j, d=r[1], hacim=r[2], bilgi=r[3]))
    elif r[0] == "INCELE": out["inc"].append(dict(i=i, j=j, d=r[1], hacim=r[2], bilgi=r[3]))
    else: out["temas"] += 1
for f in sorted(glob.glob("parca_[0-2]*.json")):
    d = json.load(open(f)); d["hata"] = []; json.dump(d, open(f, "w"), default=float)
json.dump(out, open("parca_99.json", "w"), default=float)
print(len(H), "tekrar ·", len(out["cak"]), "çakışma ·", len(out["hata"]), "hata"); sys.stdout.flush(); os._exit(0)
