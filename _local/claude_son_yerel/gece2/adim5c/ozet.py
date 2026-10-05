import sys, json, math, numpy as np
sys.path.insert(0, '.')
from dilim import dilim
def ozet(ad, no, eksen=None, konum=None, yaz=True):
    r = dilim(ad, no, eksen, konum)
    dk = r["dik"]; ax = "xyz".index(r["eksen"])
    lo, hi = r["lo"], r["hi"]
    i0, i1 = "xyz".index(dk[0]), "xyz".index(dk[1])
    PA = (hi[i0] - lo[i0]) * (hi[i1] - lo[i1])
    out = []
    for d in r["dis"] + r["delik"]:
        b = d["bb"]; w, h = b[2] - b[0], b[3] - b[1]
        if d["alan"] > 0.9 * PA: continue
        if abs(d["alan"] - w * h) < 0.02 * w * h + 0.5: t = ("R", round((b[0] + b[2]) / 2, 2), round((b[1] + b[3]) / 2, 2), round(w, 2), round(h, 2))
        elif abs(w - h) < 0.3 and abs(d["alan"] - math.pi * w * h / 4) < 0.05 * w * h: t = ("C", round((b[0] + b[2]) / 2, 2), round((b[1] + b[3]) / 2, 2), round((w + h) / 2, 2))
        else: t = ("P", b, d["n"], d["alan"])
        out.append(t)
    out.sort(key=lambda t: (t[0], t[1] if t[0] != "P" else t[1][0]))
    if yaz:
        print("== %s[%d] %s=%.2f (%s,%s) bb %s..%s · %d kesik" % (ad, no, r["eksen"], r["konum"], dk[0], dk[1], lo, hi, len(out)))
        for t in out: print("   ", t)
    return r, out
if __name__ == "__main__":
    for a in sys.argv[1:]:
        k = a.split(":"); ozet(k[0], int(k[1]), k[2] if len(k) > 2 and k[2] else None, float(k[3]) if len(k) > 3 else None)
