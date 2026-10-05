# -*- coding: utf-8 -*-
"""m8 madde 1-3: havada parca (tum model), kapak gizli, istasyon gorunumu. Temas grafi kose testinden; havada gorunen kumeler kenar ornegiyle (0,7 mm) incelenir."""
import m8_ortak as O
from m8_ortak import *
import m8_temas as T, collections, pickle, os, time
ISTL = [s for s in sorted(set(pist)) if s != "Çevre"]
SEN = [("tum", np.ones(N, bool)), ("kapak_gizli", ~pkpk)] + [("ist:" + s, pist == s) for s in ISTL]
incelenen = set()
def ana_kume(lab, gor):
    """istasyon gorunumunde en buyuk (ucgen) kume = istasyon govdesi"""
    w = collections.Counter()
    for i in np.where(gor)[0]: w[lab[i]] += PC[i]["n"]
    return w.most_common(1)[0][0]
for tur in range(6):
    E = O.E; S = set()
    for ad, g in SEN:
        der, lab, topr = grafik(g)
        ana = ana_kume(lab, g) if ad.startswith("ist:") else None
        for k in np.unique(lab[g]):
            if topr[k] or k == ana: continue
            u = np.where((lab == k) & g)[0]
            if sum(PC[i]["n"] for i in u) > 40000: continue
            S |= set(u.tolist())
    S -= incelenen
    print("tur", tur, len(S), "parca", flush=True)
    if not S: break
    t = time.time(); pts, pid = T.kenar_ornek(S, adim=0.7); print(len(pts), "ornek", flush=True)
    R = T.temas(pts, pid); pa = pid[R[:, 0]]; pb = T.TPc[R[:, 1]]
    En = np.unique(np.vstack([E, np.stack([np.minimum(pa, pb), np.maximum(pa, pb)], 1)]), axis=0)
    print("  yeni kenar", len(En) - len(E), "%.0f s" % (time.time() - t), flush=True)
    O.E = En; incelenen |= S
np.save("m8_kenar_son.npy", O.E)
E = O.E
nb = collections.defaultdict(set)
for a, b in E: nb[int(a)].add(int(b)); nb[int(b)].add(int(a))
def kume_ozet(u, gor, dis=True):
    u = list(map(int, u)); lo = LO[u].min(0); hi = HI[u].max(0)
    d, j = en_yakin(u, gor)
    r = dict(parca_sayisi=len(u), dugumler=dict(collections.Counter(PC[i]["ad"] for i in u).most_common(8)),
             mek=dict(collections.Counter(mekad(pmek[i]) for i in u).most_common(4)),
             x=[round(float(lo[0]), 1), round(float(hi[0]), 1)], y=[round(float(lo[1]), 1), round(float(hi[1]), 1)], z=[round(float(lo[2]), 1), round(float(hi[2]), 1)],
             boyut=[round(float(v), 1) for v in (hi - lo)], kpk=sorted(set(bool(pkpk[i]) for i in u)),
             en_yakin_mm=round(d, 2) if d is not None else None,
             en_yakin_parca=(PC[j]["ad"] + " · " + mekad(pmek[j]) + (" (kpk)" if pkpk[j] else "")) if j >= 0 else None,
             haric=all(haric(i) for i in u), parcalar=u)
    if dis:   # tam modelde neye degiyor (gorunmeyenler dahil)
        S = set(u); k = set()
        for i in u: k |= {j for j in nb[i] if j not in S}
        r["tam_modelde_degdigi"] = sorted(set(PC[j]["ad"] + " · " + mekad(pmek[j]) + (" (kpk)" if pkpk[j] else "") for j in k))[:8]
    return r
OUT = {}
base = grafik(np.ones(N, bool))
def havada(gor, ad):
    der, lab, topr = grafik(gor)
    ana = ana_kume(lab, gor) if ad.startswith("ist:") else None
    R = []
    for k in np.unique(lab[gor]):
        if topr[k] or k == ana: continue
        u = np.where((lab == k) & gor)[0]
        if ad != "tum":   # tam modelde zaten havada olan kumeyi tekrar etme
            bl = set(base[1][u]); 
            if len(bl) == 1 and not base[2][list(bl)[0]] and (base[1] == list(bl)[0]).sum() == len(u): continue
        R.append(kume_ozet(u, gor))
    return R, (der, lab, topr, ana)
for ad, g in SEN:
    R, info = havada(g, ad); OUT[ad] = R; print(ad, len(R), flush=True)
    if ad.startswith("ist:"):
        der, lab, topr, ana = info; u = np.where((lab == ana) & g)[0]
        OUT[ad + "|ana"] = dict(parca=len(u), ucgen=int(sum(PC[i]["n"] for i in u)), topraklı=bool(topr[ana]), y_alt=float(LO[u, 1].min()))
# kpk tersi: kpk'li olup hicbir kpk parcaya degmeyen (govdeye ait olabilir)
ters = []
for i in np.where(pkpk)[0]:
    if any(pkpk[j] for j in nb[int(i)]): continue
    t = tanim(int(i)); t["komsular"] = sorted(set(PC[j]["ad"] + " · " + mekad(pmek[j]) for j in nb[int(i)]))[:6]; ters.append(t)
OUT["kpk_ters"] = ters
# kpk'siz olup YALNIZ kpk parcalara degen (kapakla gitmesi gereken)
yalniz_kpk = []
for i in np.where(~pkpk)[0]:
    k = nb[int(i)]
    if k and all(pkpk[j] for j in k) and not haric(int(i)):
        t = tanim(int(i)); t["komsular"] = sorted(set(PC[j]["ad"] + " · " + mekad(pmek[j]) for j in k))[:6]; yalniz_kpk.append(t)
OUT["kpksiz_yalniz_kpk_degen"] = yalniz_kpk
# karisik: ayni dugumde kpk + kpk'siz parca birbirine degiyor (ayni fiziksel bilesen bolunmus olabilir)
OUT["kpk_karisik"] = [dict(kpk=tanim(int(a if pkpk[a] else b)), govde=tanim(int(b if pkpk[a] else a))) for a, b in E if PC[a]["prim"] == PC[b]["prim"] and pkpk[a] != pkpk[b]]
pickle.dump(OUT, open("m8_k123.pkl", "wb"))
print("bitti")
