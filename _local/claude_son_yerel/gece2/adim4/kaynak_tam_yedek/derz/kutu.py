import json, numpy as np, sys
def kutular(d):
    Z = np.load(d + "/m8_onbellek.npz"); J = json.load(open(d + "/m8_parca.json"))
    X = np.stack([Z["A"], Z["B"], Z["C"]], 1); mek = Z["mek"]; out = {}
    lo = X.min(1); hi = X.max(1)
    for i, m in enumerate(J["MEK"]):
        k = mek == i
        if not k.any(): continue
        a = lo[k].min(0) / 1000; b = hi[k].max(0) / 1000
        out[m["kod"]] = [round(float(v), 4) for v in (a[0], b[0], a[1], b[1], a[2], b[2])]
    return out
W = r"C:/Users/Kemal/Desktop/Kemal/WEBSİTE/AUTOKITCH_COORDINATION/worktrees/claude-hat3-v8/otonom/hat3d/v3/mekanizma_v3_8.json"
M = json.load(open(W, encoding="utf-8"))["kutu"]
k0 = kutular("."); k1 = kutular("sonra")
fark = [k for k in M if k in k0 and any(abs(a - b) > 0.0006 for a, b in zip(M[k], k0[k]))]
print("taban yeniden hesap ile json farki:", len(fark), fark[:8])
for k in M:
    if k in k0 and k0[k] != k1[k]: print("DEGISEN", k, M[k], "->", k1[k])
