# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 42 · HAVADA KALAN GRUPLARI OTURT (gece 2 · adım 9 · 4 Eki 2026 · Claude · YEREL)
python 42_havada_oturt.py girdi.glb cikti.glb      (zincir: hat3_v9i.glb → hat3_v9j.glb)
Kaynak: gece2/adim8/denetim/RAPOR.md kalem 2 + d2b_bosluk (12 grup, hepsi v8zq'dan beri var). Boşluğu 0 mm ölçülen 2 grup (DOLAP sigorta +
klemens, ELK_IC kanal 215–226: üçgen-kutu grafiği bağı kuramamış, gerçekte değiyor) dokunulmaz. Kalan 9 grup (kanal 230–233 hariç, aşağıda) en yakın taşıyıcı yüzeye
ÖTELENİR: grup köşelerinden komşu yüzeye en kısa vektör (trimesh, grup dışındaki bütün üçgenler, grup kutusu ± 15 mm) · öteleme = vektör ×
(boşluk − 0,05) / boşluk → 0,05 mm temas payı (havada eşiği 0,6). Kablo kanalı (ELK_IC__kanal) grupları yalnız
taşıyıcı yapıya (sac / paslanmaz / çelik / kabuk / çerçeve / plastik / koyu gövde düğümleri; kablo ve rakor değil) oturtulur. RevPi DIO / AIO genişleme
modülleri yanındaki RevPi modülüne (PiBridge yan bağlantısı — modüller yan yana değerek dizilir) yaklaştırılır. Grup bileşen numaraları v9h/v9i'deki govde_denetim_dogru.bilesenler sırası (adım 41 bu düğümlere dokunmaz)."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import trimesh

gi, go = sys.argv[1:3]
t0 = time.time()
LOG = SE.log
GRUP = [("ELK_IC__kanal", list(range(234, 246)), None),
        ("ELK_IC__kanal", list(range(844, 856)), None),
        ("ELK_IC__kanal", list(range(265, 276)), None),
        ("ELK_DOLAP__kablo_sinyal", list(range(315, 323)), None),
        ("ELK_K__kablo_sinyal", list(range(37, 44)), None),
        # ELK_IC kanal 230–233 (x 2577–2786 · y 845–875): en yakın yapı TP10 gövde sacı (−z 11,45) — ötelenince F_UST_KABIN__plastik
        # f_ust_rakor_cee_firin'e 3 mm giriyor (tam denetim v9j) → DOKUNULMADI, açık (kanal askısı / konsolu gerekli)
        ("ELK_IC__kanal", list(range(246, 250)), None),
        ("ELK_IC__kanal", list(range(250, 254)), None),
        ("ELK_ANA_PANO_UF__cihaz_koyu", [15, 16], None),
        ("ELK_ANA_PANO_UF__cihaz_koyu", [24, 25], None)]
YAPI = ("__sac", "__paslanmaz", "__celik", "__kabuk", "__cerceve", "__plastik", "__koyu")
GRUP = [(d, n, YAPI if d == "ELK_IC__kanal" else f) for d, n, f in GRUP]
PAY = 0.05

g = Glb(gi)
# önce bütün vektörleri hesapla (öteleme diğer grupların komşuluğunu bozmasın diye kutular ilk durumdan)
HAZ = []
for d, nos, filt in GRUP:
    g.bilesen(d, 0)
    bb = [g._bc[d][n] for n in nos]
    P = np.concatenate([np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]]) for b in bb])
    lo = P.reshape(-1, 3).min(0) - 15.0; hi = P.reshape(-1, 3).max(0) + 15.0
    oz = set(r.tobytes() for r in P.round(4))
    soup = []
    for p in g.prims:
        if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
        if filt and (not any(k in p["name"] for k in filt) or "kablo" in p["name"] or "rakor" in p["name"]): continue
        Q = p["X"][p["T"]]; a = Q.min(1); b_ = Q.max(1)
        m = np.all(b_ >= lo, 1) & np.all(a <= hi, 1)
        if not m.any(): continue
        Q = Q[m]
        if p["name"] == d:
            keep = np.array([q.round(4).tobytes() not in oz for q in Q]); Q = Q[keep]
        ar = np.linalg.norm(np.cross(Q[:, 1] - Q[:, 0], Q[:, 2] - Q[:, 0]), axis=1); Q = Q[ar > 1e-9]
        if len(Q): soup.append((p["name"], Q))
    if not soup:
        LOG("UYARI %s %s: komşu yok (filtre %s)" % (d, nos[:2], filt)); continue
    T = np.concatenate([q for _, q in soup]); adi = np.repeat(np.arange(len(soup)), [len(q) for _, q in soup])
    tm = trimesh.Trimesh(T.reshape(-1, 3), np.arange(len(T) * 3).reshape(-1, 3), process=False)
    V = np.unique(P.reshape(-1, 3), axis=0)
    cp, dist, tid = trimesh.proximity.closest_point(tm, V)
    i = int(np.argmin(dist)); dmin = float(dist[i]); v = cp[i] - V[i]
    if dmin <= 0.6:
        LOG("  %s[%d..%d]: boşluk %.2f ≤ 0,6 → dokunulmadı" % (d, nos[0], nos[-1], dmin)); continue
    tas = v * (dmin - PAY) / dmin
    HAZ.append((d, [(b["lo"].copy(), b["hi"].copy()) for b in bb], tas, dmin, soup[int(adi[int(tid[i])])][0]))
    LOG("  %s[%d..%d] (%d bileşen): boşluk %.2f mm → %s · öteleme %s" % (d, nos[0], nos[-1], len(nos), dmin, soup[int(adi[int(tid[i])])][0], np.round(tas, 2)))

KAYIT = []
for d, kutular, tas, dmin, komsu in HAZ:
    for lo, hi in kutular:
        g._bc.clear(); b = g.bilesen(d, lo=lo, hi=hi, tol=0.3); g.tasi_b(b, tas)
    KAYIT.append(dict(dugum=d, adet=len(kutular), bosluk=round(dmin, 2), komsu=komsu, oteleme=[round(float(x), 3) for x in tas]))
g._bc.clear()
tmp = go + ".e1.glb"; g.kaydet(tmp); del g
SE.sikistir(tmp, go); os.remove(tmp)
import json
json.dump(dict(adim=42, gruplar=KAYIT), open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
LOG("ADIM 42 bitti · %s · %d grup · %.0f sn" % (go, len(KAYIT), time.time() - t0))
sys.stdout.flush(); os._exit(0)
