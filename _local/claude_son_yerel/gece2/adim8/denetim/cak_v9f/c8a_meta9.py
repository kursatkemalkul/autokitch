# -*- coding: utf-8 -*-
"""bileşen meta (v9 sürümü: parça adları worktree parca_kutulari.json'dan) → meta.json"""
import os, sys, json, numpy as np
import c8a_ortak as M
PKJ = os.environ.get("DENETIM_PK", r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\otonom\hat3d\v3\parca_kutulari.json")
J, B, LAB = M.tum_bilesenler(True)
EX = J["scenes"][0].get("extras", {})
MEK = EX.get("mekanizmalar", []); KAT = EX.get("kategoriler", [])
PK = json.load(open(PKJ, encoding="utf-8"))["parca"]
KK = {b: [(q[0], np.array(q[2:8], float)) for q in L if any(q[2:8])] for b, L in PK.items()}


def ad_bul(dugum, lo, hi, e=0.6):
    b = dugum.split("__")[0]
    best, bv = None, 1e30
    for pa, k in KK.get(b, []):
        if (lo >= k[0::2] - e).all() and (hi <= k[1::2] + e).all():
            v = np.prod(np.maximum(k[1::2] - k[0::2], .01))
            if v < bv: bv, best = v, pa
    return best


out = []
for n, (b, l) in enumerate(zip(B, LAB)):
    out.append(dict(k=n, dugum=b.dugum, no=b.no, ad=ad_bul(b.dugum, b.lo, b.hi), kapali=bool(b.kapali), lo=np.round(b.lo, 1).tolist(),
                    hi=np.round(b.hi, 1).tolist(), ntri=len(b.P), mek=MEK[l[0]]["kod"] if 0 <= l[0] < len(MEK) else None,
                    kat=KAT[l[1]]["kod"] if 0 <= l[1] < len(KAT) else None, kpk=round(l[2], 2)))
json.dump(dict(mek=MEK, kat=[k["kod"] for k in KAT], bil=out), open("meta.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(out), sum(1 for o in out if o["ad"]), "adlı")
sys.stdout.flush(); os._exit(0)
