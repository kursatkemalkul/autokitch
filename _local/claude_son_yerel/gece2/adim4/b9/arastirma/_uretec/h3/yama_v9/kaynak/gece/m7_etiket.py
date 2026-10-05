# -*- coding: utf-8 -*-
"""m7 ortak: GLB bilesenlerini parca_kutulari (pk.json, v7 adlari) ile adlandir.
etiketle(G, onekler) -> {prim_index: (tl, kut, ad{komp:ad})}"""
import json, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
PK = json.load(open(os.path.join(HERE, "pk.json"), encoding="utf-8"))["parca"]


def etiketle(G, onekler=("TOPPING_MODUL", "ELK_TOPPING"), e=0.35):
    R = {}
    for i, p in enumerate(G.prims):
        b = p["name"].split("__")[0]
        if b not in onekler: continue
        if len(p["T"]) == 0: continue
        tl, kut = G.komp(p)
        kk = [(q[0], np.array(q[2:8], float)) for q in PK.get(b, [])]
        vol = [max(k[1] - k[0], .01) * max(k[3] - k[2], .01) * max(k[5] - k[4], .01) for _, k in kk]
        ad = {}
        for c, (lo, hi, n) in kut.items():
            best, bv = None, 1e30
            for j, (pa, k) in enumerate(kk):
                if (lo >= k[0::2] - e).all() and (hi <= k[1::2] + e).all() and vol[j] < bv: bv, best = vol[j], pa
            ad[c] = best or "?"
        R[i] = (tl, kut, ad)
    return R


def pk_yeni(rapor_dosyalari=()):
    """m7 sonrası kutu tablosu: birim parçaları DX kadar kaydırılmış + yeni parçalar (rapor YENI satırlarından)."""
    import re, copy
    from m7_olcu import DX, X_L, X_R, DELTA
    P2 = copy.deepcopy(PK)
    T = P2.get("TOPPING_MODUL", [])

    def birim(ad):
        if ad.startswith("kablo"): return None
        m = re.match(r"^(?:raf_gecis_contasi_|ust_raf_gecis_contasi_)?(kiyma|kusbasi|sos|harc)(_|$)", ad)
        if m: return m.group(1)
        if ad.startswith("soguk_"): return None
        if "kasar" in ad: return "kasar"
        if "sucuk" in ad: return "sucuk"
        return None
    ek = []
    for q in T:
        ad = q[0]
        if "mandal" in ad or ad in ("sos_urun_hortumu_D32", "ust_raf_gecis_contasi_sos"): q[2:8] = [0, 0, 0, 0, 0, 0]; continue
        if ad in ("harc_cikis_dirsegi_316L", "harc_cikis_dirsegi_tc_kelepcesi", "harc_urun_hortumu_D32", "ust_raf_gecis_contasi_harc"):
            d = X_R - 2190.0; ek.append([ad.replace("harc", "sos"), q[1], q[2] + d, q[3] + d] + q[4:8])
        u = birim(ad)
        if u: q[2] += DX[u]; q[3] += DX[u]
        if ad in ("tabla_bos_sensoru", "sensor_braketi_tabla_bos"): q[6] -= 45.0; q[7] -= 45.0
        if ad.startswith(("raf_askisi_burclari_sol", "ust_raf_askisi_burclari_sol")): q[2] -= DELTA; q[3] -= DELTA
    T += ek
    for f in rapor_dosyalari:
        if not os.path.exists(f): continue
        for ln in open(f, encoding="utf-8"):
            m = re.match(r"YENI\s+(\S+)\s+(\S+)\s+x\s+(\S+)\s+(\S+)\s+y\s+(\S+)\s+(\S+)\s+z\s+(\S+)\s+(\S+)", ln)
            if not m: continue
            nd, ad = m.group(1), m.group(2); v = [float(m.group(k)) for k in range(3, 9)]
            b = nd if "__" not in nd else nd.split("__")[0]
            if b in ("paslanmaz", "pu", "sac", "celik", "pom", "silikon"): b = "TOPPING_MODUL"
            P2.setdefault(b, []).append([ad, 0] + v)
    return P2


def etiketle_yeni(G, onekler=("TOPPING_MODUL", "ELK_TOPPING"), raporlar=(), e=0.35):
    global PK
    eski = PK
    try:
        PK = pk_yeni(raporlar)
        return etiketle(G, onekler, e)
    finally:
        PK = eski
