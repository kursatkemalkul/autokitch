import sys, os, json, io
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import h3_elk_ortak as EO
idx = json.load(io.open("h3/_dunya/dunya.json", encoding="utf-8"))
G = {"%s|%s" % (i[0], i[1]): i[3] for i in idx}
out = [(ad, G[ad], [round(v, 2) for v in b]) for ad, s, b in EO.dokum()]
json.dump(out, io.open("h3/_dunya/kutular.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(out)); sys.stdout.flush(); os._exit(0)
