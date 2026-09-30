# -*- coding: utf-8 -*-
"""E v12 denetimi (30 Eyl 2026 · Claude)
1 · katılar geçerli
2 · GERÇEK SÜRE: her eksenin gerçek saatteki tepe hızı katalog sınırının içinde (zaman_denetimi_v12) + hareket tablosu (eski → gerçek süre)
3 · kafa iniş penceresi (eski 1,85–2,80, 5 ms adım): kafada taşınan bütün takımlar (PISTON, CNR_LIFT, FRONT_Y, PARMAK, köşe parmakları) ↔ besleme
    arabası + vakum (ITICI, VAC_Y) · en kısa mesafe ve kesişim (v11: itici_araba_plakasi_sol ↔ piston_kafasi 1,29 mm)
4 · bütün döngü (eski saat 0,25 s adım + olay anları): bütün hareketli gruplar ↔ bütün parçalar kesişim > 0,5 mm³
    v11 ISTISNA listesi (kamalı mil ↔ göbek, vida ↔ somun …) sayılmaz · karton ↔ karton (kat yeri kalınlık bindirmesi) ayrı: R["karton_ic"]
    makine ↔ karton ayrı: R["karton"] (asıl önemli olan: makine kartonu ezmesin)
Çıktı: _local/e-v12/denetim.json · 'hizli' argümanı 4'ü atlar."""
import json, sys, time, hashlib
from pathlib import Path
import kutu_cad_v12 as K

t0 = time.time()
K.modul()
P = {p["ad"]: p for p in K.PARCALAR}
S = {n: p["wp"].val() for n, p in P.items()}
OUT = Path(__file__).resolve().parents[2] / "_local" / "e-v12"; OUT.mkdir(parents=True, exist_ok=True)
R = dict(kaynak_sha256=hashlib.sha256(Path(K.__file__).read_bytes()).hexdigest(), parca=len(P), gecersiz=[n for n, s in S.items() if not s.isValid()],
         dongu_eski=K.DONGU, dongu_gercek=round(K.DONGU_GERCEK, 2), zaman_ihlal=K.zaman_denetimi_v12(), hareketler=K.zaman_ozeti_v12(),
         yakin=[], kesisim=[], tam=False)
print("E v12 · %d parça · geçersiz %d · döngü eski %.1f s → gerçek %.2f s" % (len(P), len(R["gecersiz"]), K.DONGU, K.DONGU_GERCEK), flush=True)
for h in R["hareketler"]:
    if h["phi"] > 1.0001:
        print("   %-30s eski %.2f–%.2f (%.2f s) → gerçek %.2f s · tepe %.0f → %.0f %s/s (sınır %.0f) · φ %.2f"
              % (h["eksen"], h["t0"], h["t1"], h["sure_eski"], h["sure_gercek"], h["v_tepe_eski"], h["v_tepe_eski"] / h["phi"], h["birim"], h["v_sinir"], h["phi"]), flush=True)
print("   ZAMAN İHLALİ (gerçek saatte sınırı aşan eksen): %s" % (R["zaman_ihlal"] or "YOK"), flush=True)

GRUPSUZ = ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF")


def dunya(t):
    W = K.blank_dunya(t)
    M = {n: (W[P[n]["grup"]] if P[n]["grup"].startswith("B_") else K.grup_matrisi(P[n]["grup"], t)) for n in S if P[n]["grup"] not in GRUPSUZ}
    return M


cache = {}


def sekil(n, M):
    key = (n, tuple(round(v, 6) for row in M[:3] for v in row))
    if key not in cache:
        sh = K.uygula(S[n], M); cache[key] = (sh, sh.BoundingBox())
    return cache[key]


KAFA_G = ("PISTON", "CNR_LIFT", "FRONT_Y", "PARMAK") + tuple(K.CORNER)
BES_G = ("ITICI", "VAC_Y")
kafa_p = [n for n in S if P[n]["grup"] in KAFA_G]
bes_p = [n for n in S if P[n]["grup"] in BES_G]
en_kisa = (1e9, None)
t = 1.85
while t <= 2.80 + 1e-9:
    M = dunya(t)
    for a in kafa_p:
        sa, ba = sekil(a, M[a])
        for b in bes_p:
            sb, bb = sekil(b, M[b])
            if ba.xmin > bb.xmax + 20 or bb.xmin > ba.xmax + 20 or ba.ymin > bb.ymax + 20 or bb.ymin > ba.ymax + 20 or ba.zmin > bb.zmax + 20 or bb.zmin > ba.zmax + 20:
                continue
            d = sa.distance(sb)
            if d < en_kisa[0]: en_kisa = (d, (round(t, 3), a, b))
            if d < 0.01 and sa.intersect(sb).Volume() > 0.5:
                R["kesisim"].append([round(t, 3), a, b])
    t += 0.005
R["yakin"] = dict(en_kisa_mm=round(en_kisa[0], 2), an=en_kisa[1])
print("   KAFA İNİŞİ ↔ BESLEME (eski 1,85–2,80 · 5 ms): en kısa %.2f mm %s · kesişim %d" % (en_kisa[0], en_kisa[1], len(R["kesisim"])), flush=True)

if "hizli" not in sys.argv:
    anlar = sorted(set([round(i * 0.25, 3) for i in range(int(K.DONGU * 4) + 1)] + [0.35, 0.65, 1.35, 1.65, 1.9, 2.2, 2.7, 2.858, 3.0, 3.7, 4.5, 5.3, 5.858,
                                                                                     6.3, 6.55, 6.85, 7.1, 8.0, 8.2, 8.7, 9.05, 9.5, 9.8, 10.15, 10.55, 10.8, 11.1,
                                                                                     13.6, 13.9, 14.2, 15.6, 15.9, 16.7, 18.1, 18.6, 20.3, 21.7, 22.8, 22.98]))
    hareketli = [n for n in S if P[n]["grup"] not in GRUPSUZ and P[n]["grup"] != "SABIT"]
    R["karton"] = []; R["karton_ic"] = []; ILK = set()
    for t in anlar:
        M = dunya(t)
        W = {n: sekil(n, M[n]) for n in M}
        gor = set()
        for a in hareketli:
            sa, ba = W[a]
            for b, (sb, bb) in W.items():
                if a == b or (b, a) in gor: continue
                gor.add((a, b))
                if not K._bb_kesisir(ba, bb): continue
                if P[a]["grup"] == P[b]["grup"] and not P[a]["grup"].startswith("B_"): continue
                if K._istisna(a, b): continue
                v = sa.intersect(sb).Volume()
                if v > 0.5:
                    ka = P[a]["grup"].startswith("B_") or P[a]["mal"] == "karton_yigin"
                    kb = P[b]["grup"].startswith("B_") or P[b]["mal"] == "karton_yigin"
                    liste = R["karton_ic"] if (ka and kb) else R["karton"] if (ka or kb) else R["kesisim"]
                    liste.append([t, a, b, round(v, 2)])
                    if (a, b) not in ILK:
                        ILK.add((a, b)); print("      %s %s ↔ %s %.1f mm³ (t %.2f)" % ("KARTON-İÇ" if (ka and kb) else "KARTON" if (ka or kb) else "KESİŞİM", a, b, v, t), flush=True)
        print("   an %.2f · kesişim %d · makine↔karton %d · karton içi %d · %.0f s" % (t, len(R["kesisim"]), len(R["karton"]), len(R["karton_ic"]), time.time() - t0), flush=True)
    R["tam"] = True
(OUT / "denetim.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
ok = not R["gecersiz"] and not R["zaman_ihlal"] and not R["kesisim"] and not R.get("karton") and R["yakin"]["en_kisa_mm"] >= 3.0
print("E v12 DENETİM: %s · geçersiz %d · zaman ihlali %d · kesişim %d · kafa↔besleme en kısa %.2f mm (≥ 3) · %.0f s"
      % ("GEÇTİ" if ok else "KALDI", len(R["gecersiz"]), len(R["zaman_ihlal"]), len(R["kesisim"]), R["yakin"]["en_kisa_mm"], time.time() - t0), flush=True)

if "baglanti" in sys.argv:
    # v11 yöntemi: 0,25 mm (kayar geçmeler) içinde temas eden parçalar aynı bileşen · v11: 381 parça tek bileşen + asansör kayışı (0,38 mm diş boşluğu)
    names = [n for n in P if not P[n]["grup"].startswith("B_") and P[n]["grup"] not in GRUPSUZ and P[n]["mal"] != "karton_yigin" and not n.startswith("icecek_")]
    solids = {n: K.uygula(S[n], K.grup_matrisi(P[n]["grup"], 0)) for n in names}
    boxes = {n: s.BoundingBox() for n, s in solids.items()}
    graph = {n: set() for n in names}
    for i, n in enumerate(names):
        for m in names[i + 1:]:
            a, b = boxes[n], boxes[m]
            if any(getattr(a, k + "min") > getattr(b, k + "max") + .25 or getattr(b, k + "min") > getattr(a, k + "max") + .25 for k in "xyz"): continue
            if solids[n].distance(solids[m]) <= .25: graph[n].add(m); graph[m].add(n)
    todo = set(names); comps = []
    while todo:
        found = set(); stack = [next(iter(todo))]
        while stack:
            n = stack.pop()
            if n in found: continue
            found.add(n); stack.extend(graph[n] - found)
        todo -= found; comps.append(sorted(found))
    comps.sort(key=len, reverse=True)
    (OUT / "baglanti.json").write_text(json.dumps(comps, ensure_ascii=False, indent=1), encoding="utf-8")
    print("E v12 BAĞLANTI: bileşen boyları %s · tek kalanlar %s" % ([len(c) for c in comps][:6], [c for c in comps[1:] if len(c) <= 3][:6]), flush=True)
