import sys, os, pickle, numpy as np, collections
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
B = pickle.load(open(os.path.join(S, "gece2/adim5/_is/bil_hepsi.pkl"), "rb"))
PU = [b for b in B if b["ad"] == "B_KASA__pu"]
SAC = [b for b in B if b["ad"] == "B_KASA__sac"]
def ov(a, b, e=0.05): return (np.minimum(a["hi"], b["hi"]) - np.maximum(a["lo"], b["lo"]) > e).all()
seen = collections.defaultdict(list)
for b in B:
    if b["ad"].startswith("B_KASA"): continue
    hits = [p["no"] for p in PU if ov(b, p)]
    hs = [p["no"] for p in SAC if ov(b, p)]
    if hits or hs: seen[b["ad"]].append((b["no"], np.round(b["lo"],1).tolist(), np.round(b["hi"],1).tolist(), "PU", hits, "SAC", hs))
for k, v in sorted(seen.items()):
    print("==", k, len(v))
    for x in v[:12]: print("   ", x)
