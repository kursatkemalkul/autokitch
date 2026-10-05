# -*- coding: utf-8 -*-
"""adım 5-entegrasyon denetimi: python ent_denetim.py yeni.glb taban.glb ent.json cikti_klasoru [istasyon_zarfi x0 x1 y0 y1 z0 z1]
1 doğru çakışma aracı (govde_denetim_dogru · manifold3d + VTK yoğun örnekleme · iki yönlü) · DEĞİŞEN/YENİ bütün bileşenler ↔ bütün model
2 sınıflama: bileşen → parça adı (ent.json kutuları) · izinli = PEM gömme başı / PEM gövdesi sacda, kaynak dikişi, vida ↔ kendi somunu/PEM'i (diş)
3 havada: yeni gövde bileşenleri temas grafiği (≤ 0,6 mm) → zemine bağlı mı (zemin = y ≤ 1 olan her şey + bağlı oldukları)
4 dış zarf · etiket (kat / mek / kpk) doğrulaması"""
import os, sys, json, re, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "is"))
import govde_denetim_dogru as G

gy, gt, ej, cik = sys.argv[1:5]
zarf = [float(x) for x in sys.argv[5:11]] if len(sys.argv) >= 11 else None
os.makedirs(cik, exist_ok=True)
L = open(os.path.join(cik, "rapor.txt"), "w", encoding="utf-8")


def yaz(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); L.write(s + "\n"); L.flush()


E = json.load(open(ej, encoding="utf-8"))
PAR = E["parca"]
t0 = time.time()
D = G.glb_oku(gy)
TUM = {}
for nd in D:
    for b in G.bilesenler(nd, D[nd]): TUM[b.ad] = b
DT = G.glb_oku(gt)
eski = set()
for nd in DT:
    for b in G.bilesenler(nd, DT[nd]): eski.add((b.dugum, b.ozet))
ALLB = list(TUM.values())
LO_ = np.array([b.lo for b in ALLB]); HI_ = np.array([b.hi for b in ALLB])
degisen = [i for i, b in enumerate(ALLB) if (b.dugum, b.ozet) not in eski and len(b.P) > 0]
yaz("model %d bileşen · DEĞİŞEN/YENİ %d (açık %d) · %.0f s" % (len(ALLB), len(degisen), sum(not ALLB[i].kapali for i in degisen), time.time() - t0))
S = dict(cakisma=[], incele=[], temas=0, acik_ag=[ALLB[i].ad for i in degisen if not ALLB[i].kapali])
oz = set(degisen); gor = set()
for k, i in enumerate(degisen):
    A_ = ALLB[i]
    m = ((LO_ <= A_.hi + G.PAY) & (HI_ >= A_.lo - G.PAY)).all(1); m[i] = False
    for j in np.where(m)[0]:
        key = (min(i, j), max(i, j))
        if key in gor: continue
        gor.add(key)
        B_ = ALLB[j]
        if not A_.kapali and not B_.kapali: continue
        if (not A_.kapali or not B_.kapali):
            # açık ağ ↔ kapalı: yalnız ortak kutu küçükse örnekle (büyük açık PU levhası ↔ büyük sac: kutu kesişimi 1 mm'den inceyse geç)
            ilo = np.maximum(A_.lo, B_.lo); ihi = np.minimum(A_.hi, B_.hi)
            if np.any(ihi - ilo < 0.05): continue
            if np.prod(ihi - ilo) > 2e5:
                S.setdefault("atlanan_buyuk_acik", []).append((A_.ad, B_.ad)); continue
        r = G.cift(A_, B_)
        if r is None: continue
        kayit = dict(parca=A_.ad, komsu=B_.ad, tip=r[0], derinlik=r[1], hacim=None if r[2] is None else round(r[2], 3), bilgi=r[3])
        if r[0] == "CAKISMA": S["cakisma"].append(kayit)
        elif r[0] == "INCELE": S["incele"].append(kayit)
        else: S["temas"] += 1
    if k % 200 == 0: yaz("  %d / %d · çakışma %d · %.0f s" % (k, len(degisen), len(S["cakisma"]), time.time() - t0))
json.dump(S, open(os.path.join(cik, "cakisma_ham.json"), "w", encoding="utf-8"), ensure_ascii=False, default=float)
yaz("ÇAKIŞMA %d · İNCELE %d · TEMAS %d · %.0f s" % (len(S["cakisma"]), len(S["incele"]), S["temas"], time.time() - t0))


def adlar(bad):
    b = TUM.get(bad)
    if b is None: return []
    nd = b.dugum
    out = []
    for a, p in PAR.items():
        if p["dugum"] != nd: continue
        k = p["kutu"]
        if b.lo[0] >= k[0] - 0.2 and b.hi[0] <= k[1] + 0.2 and b.lo[1] >= k[2] - 0.2 and b.hi[1] <= k[3] + 0.2 and b.lo[2] >= k[4] - 0.2 and b.hi[2] <= k[5] + 0.2:
            out.append(a)
    return out


IZIN_AD = re.compile(r"pem|fhp|saplama|kaynak|dikis|dolgu|_pul|somun|percin|tapa", re.I)


def izinli(r):
    a1, a2 = adlar(r["parca"]), adlar(r["komsu"])
    n1, n2 = r["parca"].split("[")[0], r["komsu"].split("[")[0]
    bom1 = " ".join(" ".join(map(str, PAR[a]["bom"])) for a in a1); bom2 = " ".join(" ".join(map(str, PAR[a]["bom"])) for a in a2)
    if a1 and a2 and ((all(IZIN_AD.search(a + " " + bom1) for a in a1)) or (all(IZIN_AD.search(a + " " + bom2) for a in a2))):
        return "gövde içi bağlantı (PEM gömme başı / kaynak / somun)", a1, a2
    # karşı tarafa preslenen PEM somun / perçin somun ↔ yuvası (gövde dışı düğümde, adı ent'te yok) → yalnız PEM SP / perçin ise
    if (not a1 or not a2) and re.search(r"TOPPING_MODUL__paslanmaz|B_MODULER__paslanmaz|B_TASIYICI__celik|K_GOVDE__kabuk", n1 + n2) and any(re.search(r"PEM SP|erçin somun|_pem$", a + " " + bom1 + bom2) for a in (a1 + a2) or [""]):
        return "karşı eleman (PEM / perçin somun) ↔ yuvası", a1, a2
    return None, a1, a2


ger, izn = [], []
for r in S["cakisma"]:
    neden, a1, a2 = izinli(r)
    r["adlar"] = [a1[:3], a2[:3]]
    (izn if neden else ger).append((r, neden))
yaz("\n=== SINIFLAMA · ÇAKIŞMA %d → izinli %d · GERÇEK %d · İNCELE %d" % (len(S["cakisma"]), len(izn), len(ger), len(S["incele"])))
from collections import Counter
for k, v in Counter(n for _, n in izn).items(): yaz("   izinli: %-48s %d" % (k, v))
for r, _ in sorted(ger, key=lambda x: -x[0]["derinlik"]):
    yaz("   GERÇEK %-34s ↔ %-34s %.3f mm · %s ↔ %s · nokta %s" % (r["parca"], r["komsu"], r["derinlik"], r["adlar"][0], r["adlar"][1], r["bilgi"]["nokta"]))
for r in S["incele"]: yaz("   İNCELE %s ↔ %s hacim %s" % (r["parca"], r["komsu"], r["hacim"]))

# ---------------------------------------------------------------- dış zarf
dugler = sorted(set(p["dugum"] for p in PAR.values()))
if zarf:
    GA = [a for a in PAR if not a.startswith("arayuz_")]
    lo = np.min([np.array(PAR[a]["kutu"][0::2]) for a in GA], 0); hi = np.max([np.array(PAR[a]["kutu"][1::2]) for a in GA], 0)
    f = np.abs(np.r_[lo, hi] - np.array(zarf[0::2] + zarf[1::2]))
    yaz("\n=== ZARF yeni gövde %s..%s · hedef %s · fark en çok %.2f → %s" % (np.round(lo, 1).tolist(), np.round(hi, 1).tolist(), zarf, f.max(), "GEÇTİ" if f.max() <= 0.5 else "KALDI"))

# ---------------------------------------------------------------- havada (yeni gövde bileşenleri)
yeni = [b for k, b in TUM.items() if b.dugum in dugler]
yaz("\n=== HAVADA · yeni gövde düğümleri %s · %d bileşen" % (dugler, len(yeni)))
ALL = list(TUM.values())
LO = np.array([b.lo for b in ALL]); HI = np.array([b.hi for b in ALL])
idx = {b.ad: i for i, b in enumerate(ALL)}
zem = set(i for i, b in enumerate(ALL) if b.lo[1] <= 1.0)
komsu = {}
def temas(a, b):
    try:
        ma, mb = a.mf(), b.mf()
        if ma and mb: return ma.min_gap(mb, 0.7) <= 0.6
    except Exception: pass
    # açık ağ: köşe uzaklığı kaba ölçü
    from scipy.spatial import cKDTree
    t = cKDTree(b.P.reshape(-1, 3)); d, _ = t.query(a.P.reshape(-1, 3)[:: max(1, len(a.P) // 500)]); return d.min() <= 0.6
# BFS: zeminden başlayarak yalnız yeni gövde bileşenleri + doğrudan komşuları üzerinden
hedef = set(idx[b.ad] for b in yeni)
bagli = set()
dal = [i for i in hedef if ALL[i].lo[1] <= 1.0]
# yeni bileşenlerin komşuları (yeni olmayanlar) zemine bağlı kabul edilir (bugünkü modelde havada denetimi temiz)
for i in hedef:
    m = ((LO <= ALL[i].hi + 0.6) & (HI >= ALL[i].lo - 0.6)).all(1); m[i] = False
    komsu[i] = [j for j in np.where(m)[0]]
for i in hedef:
    if any(j not in hedef for j in komsu[i] if temas(ALL[i], ALL[j])): dal.append(i)
bagli = set(dal); yigin = list(dal)
while yigin:
    i = yigin.pop()
    for j in komsu[i]:
        if j in hedef and j not in bagli and temas(ALL[i], ALL[j]): bagli.add(j); yigin.append(j)
hav = [ALL[i].ad for i in hedef if i not in bagli]
yaz("   havada %d / %d %s" % (len(hav), len(hedef), [(h, adlar(h)[:2]) for h in hav[:20]]))
json.dump(dict(gercek=[r for r, _ in ger], izinli=len(izn), incele=S["incele"], havada=[(h, adlar(h)) for h in hav], acik_ag=S["acik_ag"]),
          open(os.path.join(cik, "ozet.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
yaz("bitti %.0f s" % (time.time() - t0))
L.close(); sys.stdout.flush(); os._exit(0)
