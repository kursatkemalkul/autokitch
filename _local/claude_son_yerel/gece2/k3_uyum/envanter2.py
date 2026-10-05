# -*- coding: utf-8 -*-
"""K3 iş 1 · standart uyum envanteri: bir istasyon üretecini kurar (kur()), sac / profil / eleman / kaynak / arayüz listesini JSON'a döker.
python envanter.py <ist>   (A B E F K U T)  → env_<ist>.json"""
import os, sys, json, time, re, collections
W = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8"
H3 = os.path.join(W, "arastirma", "_uretec", "h3")
Y = os.path.join(H3, "yama_v9")
os.environ.setdefault("AUTOKITCH_SAC_STANDART", os.path.join(Y, "sac_standart"))
os.environ["ADIM5"] = os.path.join(Y, "veri")
for p in (os.path.dirname(H3), H3):
    sys.path.insert(0, p)
OUT = os.path.dirname(os.path.abspath(__file__))
ist = sys.argv[1]
MOD = dict(A="h3_a_sac_v1", B="h3_b_sac_v1", E="h3_e_sac_v1", F="h3_f_sac_v1", K="h3_k_sac_v1", U="h3_u_sac_v1", T="h3_topping_sac_v2")[ist]
t0 = time.time()
m = __import__(MOD)
r = m.kur(log=lambda *a: None)
if isinstance(r, dict): gs = list(r.items())
elif r is None or r is getattr(m, "G", None): gs = [(ist, m.G)]
else: gs = [(ist, r)]


def bom(p):
    b = p.get("bom")
    return list(b) if b else None


def lst(g, ad):
    v = getattr(g, ad, None)
    if v is None: return []
    if isinstance(v, dict): return list(v.values())
    return list(v)


out = dict(ist=ist, mod=MOD, gruplar={})
DX = dict(A=736.0, K=4000.0, E=4400.0).get(ist, 0.0)
for gad, g in gs:
    D = dict(sac=[], profil=[], eleman=[], arayuz=[], kaynak=[])
    for s in lst(g, "SAC"):
        try:
            B_ = s.kati().BoundingBox(); sbb = [round(B_.xmin + DX, 2), round(B_.xmax + DX, 2), round(B_.ymin, 2), round(B_.ymax, 2), round(B_.zmin, 2), round(B_.zmax, 2)]
        except Exception as e:
            sbb = None
        D["sac"].append(dict(bb=sbb, ad=s.ad, rol=getattr(s, "rol", None), t=s.t, R=s.R, K=s.K, bolge=getattr(s, "bolge", None), birim=s.birim,
                             bukum=[dict(R=round(B.R, 4), aci=round(B.aci, 2), K=B.K) for B in s.bukumler],
                             kose=[dict(getattr(B, "kose_son", {}) or {}) for B in s.bukumler if hasattr(B, "kose_son")] and None))
    profs = lst(g, "PROFIL") or lst(g, "PROF")
    for p in profs:
        D["profil"].append(dict(ad=p.ad, b1=getattr(p, "b1", getattr(p, "bu", getattr(p, "b", None))), b2=getattr(p, "b2", getattr(p, "bv", getattr(p, "b", None))),
                                t=p.t, Ro=getattr(p, "Ro", None), std=getattr(p, "std", None), L=round(p.a1 - p.a0, 2)))
    for k in ("ELEMAN", "ARAYUZ", "KAYNAK"):
        for p in lst(g, k):
            if not isinstance(p, dict): continue
            sh = p.get("sh") if p.get("sh") is not None else (p["wp"].val() if p.get("wp") is not None else None)
            bb = None
            if sh is not None:
                B_ = sh.BoundingBox(); bb = [round(B_.xmin + DX, 2), round(B_.xmax + DX, 2), round(B_.ymin, 2), round(B_.ymax, 2), round(B_.zmin, 2), round(B_.zmax, 2)]
            D[k.lower()].append(dict(ad=p.get("ad"), bom=bom(p), bb=bb, meta={a: b for a, b in (p.get("meta") or {}).items() if isinstance(b, (int, float, str))},
                                     birim=p.get("birim")))
    out["gruplar"][gad] = D
out["sure"] = round(time.time() - t0, 1)
json.dump(out, open(os.path.join(OUT, "env2_%s.json" % ist), "w", encoding="utf-8"), ensure_ascii=False, indent=0, default=str)
print(ist, "tamam", out["sure"], {g: {k: len(v) for k, v in D.items()} for g, D in out["gruplar"].items()})
sys.stdout.flush(); os._exit(0)
