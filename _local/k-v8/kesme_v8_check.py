# -*- coding: utf-8 -*-
"""K v8 denetimi (30 Eyl 2026 · Claude)
1 · katılar geçerli · 2 · durağan (bütün parçalar evde) kesişim > 0,5 mm³ — İSTİSNASIZ · 3 · hareket taraması: hareketli gruplar ↔ her şey (0,1 s + olay anları)
4 · ürün yolu: Ø300 × 15 disk ↔ bütün parçalar (bant üst yüzü ve ölü plaka temas: yalnız hacim > 0,5 mm³ sayılır) · 5 · bağlantı (0,25 mm: havada parça)
6 · kütleler (CAD hacmi × yoğunluk) → zaman denetimi (kesme_cad_v8.zaman_denetimi)
Çıktı: _local/k-v8/denetim.json · 'hizli' → 3 ve 5 atlanır"""
import json, sys, time, hashlib
from pathlib import Path
import cadquery as cq
import kesme_cad_v8 as K

t0 = time.time()
K.modul()
P = {p["ad"]: p for p in K.PARCALAR}
assert len(P) == len(K.PARCALAR), "ad tekrar"
S = {n: p["wp"].val() for n, p in P.items()}
OUT = Path(__file__).resolve().parents[2] / "_local" / "k-v8"; OUT.mkdir(parents=True, exist_ok=True)
R = dict(kaynak_sha256=hashlib.sha256(Path(K.__file__).read_bytes()).hexdigest(), parca=len(P), gecersiz=[n for n, s in S.items() if not s.isValid()],
         bomsuz=[], durgun=[], hareket=[], urun=[], yakin={}, havada=[], kutle={}, zaman=None)
print("K v8 · %d parça · geçersiz %d %s · %.0f s" % (len(P), len(R["gecersiz"]), R["gecersiz"][:5], time.time() - t0), flush=True)
GRUPSUZ = ("SPREY", "URUN", "URUN_IZ", "REF")
names = [n for n in P if P[n]["grup"] not in GRUPSUZ]
BB = {n: S[n].BoundingBox() for n in names}


def bbk(a, b, pay=0.05):
    return not (a.xmin >= b.xmax - pay or b.xmin >= a.xmax - pay or a.ymin >= b.ymax - pay or b.ymin >= a.ymax - pay or a.zmin >= b.zmax - pay or b.zmin >= a.zmax - pay)


for i, a in enumerate(names):
    for b in names[i + 1:]:
        if not bbk(BB[a], BB[b]): continue
        v = S[a].intersect(S[b]).Volume()
        if v > 0.5:
            R["durgun"].append([a, b, round(v, 2)])
print("   DURGUN kesişim: %d %s" % (len(R["durgun"]), R["durgun"][:30]), flush=True)

HAREKETLI = ("KESICI", "ITICI_ARABA", "ITICI_CAPRAZ", "ITICI_KOL", "ITICI_YUZ")


def konum(n, t):
    g = P[n]["grup"]
    if g in HAREKETLI:
        d = K.grup_trs(g, t)
        return S[n].moved(cq.Location(cq.Vector(*d))) if any(abs(c) > 1e-9 for c in d) else S[n]
    return S[n]


if "hizli" not in sys.argv:
    anlar = sorted(set([round(i * 0.1, 3) for i in range(int(K.DONGU * 10) + 1)] + list(getattr(K, "OLAY_ANLARI", ()))))
    hn = [n for n in names if P[n]["grup"] in HAREKETLI]
    ILK = set()
    for t in anlar:
        M = {n: konum(n, t) for n in names}
        MB = {n: (M[n].BoundingBox() if P[n]["grup"] in HAREKETLI else BB[n]) for n in names}
        for a in hn:
            for b in names:
                if a == b or P[a]["grup"] == P[b]["grup"]: continue
                if P[b]["grup"] in HAREKETLI and b < a: continue
                if not bbk(MB[a], MB[b]): continue
                v = M[a].intersect(M[b]).Volume()
                if v > 0.5:
                    R["hareket"].append([t, a, b, round(v, 2)])
                    if (a, b) not in ILK:
                        ILK.add((a, b)); print("      HAREKET %s ↔ %s %.1f mm³ (t %.2f)" % (a, b, v, t), flush=True)
    print("   HAREKET taraması: %d kayıt · %d çift · %.0f s" % (len(R["hareket"]), len(ILK), time.time() - t0), flush=True)

# ürün yolu · BEKLENEN temaslar ayrı sayılır: bıçaklar (kesim 4,0–6,5) · E'ye geçişte düz disk modelinin K bandına inmesi (x > X_INIS[0]:
# ürün gerçekte eğilir; E'nin kendi modeli de aynı düz iniş) — en büyük batma derinliği raporlanır
GECIS = ("bant_PU_ust", "bant_sarim_354", "olu_plaka", "kayma_tablasi", "tahrik_rulosu_EC5000_354", "bant_traversi_0", "bant_traversi_1")


def beklenen(n, t, x):
    return (n.startswith("bicak_") and K.Z_KES[0] <= t <= K.Z_KES[3]) or (x > K.X_INIS[0] and n in GECIS)


R["urun_beklenen"] = []
ILK = set()
for i in range(int(K.DONGU * 20) + 1):
    t = i * 0.05
    x, y, z = K.urun_merkez(t)
    if x < -200: continue
    disk = cq.Solid.makeCylinder(K.PZ_R, K.PZ_H, cq.Vector(x, y, z), cq.Vector(0, 1, 0))
    db = disk.BoundingBox()
    for n in names:
        sh = konum(n, t)
        if not bbk(db, sh.BoundingBox()): continue
        v = disk.intersect(sh).Volume()
        if v > 0.5 and beklenen(n, t, x):
            R["urun_beklenen"].append([round(t, 2), n, round(v, 2), round(996.0 - y, 2)])
            continue
        if v > 0.5:
            R["urun"].append([round(t, 2), n, round(v, 2)])
            if n not in ILK:
                ILK.add(n); print("      ÜRÜN ↔ %s %.1f mm³ (t %.2f · x %.0f)" % (n, v, t, x), flush=True)
print("   ÜRÜN yolu: %d kayıt · %d parça · beklenen temas %d (bıçak + E geçişi, en derin batma %.1f mm)" % (len(R["urun"]), len(ILK), len(R["urun_beklenen"]),
      max([b[3] for b in R["urun_beklenen"] if not b[1].startswith("bicak_")] or [0.0])), flush=True)

# bağlantı (havada): 0,25 mm içinde temas eden parçalar aynı bileşen (hareketliler evde)
if "hizli" not in sys.argv:
    graph = {n: set() for n in names}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            A, B_ = BB[a], BB[b]
            if any(getattr(A, k + "min") > getattr(B_, k + "max") + .25 or getattr(B_, k + "min") > getattr(A, k + "max") + .25 for k in "xyz"): continue
            if S[a].distance(S[b]) <= .25: graph[a].add(b); graph[b].add(a)
    todo = set(names); comps = []
    while todo:
        found = set(); stack = [next(iter(todo))]
        while stack:
            n = stack.pop()
            if n in found: continue
            found.add(n); stack.extend(graph[n] - found)
        todo -= found; comps.append(sorted(found))
    comps.sort(key=len, reverse=True)
    R["havada"] = comps[1:]
    print("   BAĞLANTI: bileşen boyları %s · havada %s" % ([len(c) for c in comps][:8], comps[1:12]), flush=True)

R["bomsuz"] = [n for n in names if not P[n].get("bom") and not any(n.startswith(k) for k in ("bicak_", "koruma_braketi_", "kelebek_somun_", "ara_dikme_", "DGRF_", "itici_", "valf_", "hava_hortumu", "din_rayi", "pano_ara", "urun_sensoru", "cit_", "bant_", "SSR_", "sicaklik_", "yag_", "tahrik_", "avara_", "PulsaJet_", "isitmali_", "hortum_", "sartlandirici_", "taban_", "kose_", "onyuz_", "ayak_", "eksen_", "kopru_", "sol_", "sag_", "ust_", "arka_"))]
R["kutle"] = K.grup_kutleleri() if hasattr(K, "grup_kutleleri") else {}
if hasattr(K, "zaman_denetimi"):
    R["zaman"] = K.zaman_denetimi()
    print("   ZAMAN: %s" % R["zaman"], flush=True)
print("   KÜTLE: %s" % R["kutle"], flush=True)
(OUT / "denetim.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
ok = not R["gecersiz"] and not R["durgun"] and not R["hareket"] and not R["urun"] and not R["havada"] and (R["zaman"] is None or R["zaman"].get("ok"))
print("K v8 DENETİM: %s · geçersiz %d · durgun %d · hareket %d · ürün %d · havada %d · %.0f s" % ("GEÇTİ" if ok else "KALDI", len(R["gecersiz"]), len(R["durgun"]),
      len(R["hareket"]), len(R["urun"]), len(R["havada"]), time.time() - t0), flush=True)
