# -*- coding: utf-8 -*-
"""M7-A · TOPPING birimlerini yeni x'lere taşı (UNO ×4 + kaşar / sucuk kaseti) · sos'a harç tipi dik çıkış (dirsek + düz hortum).
python m7a_birim_tasi.py giris.glb cikis.glb
 - parça adları pk.json (v7 parca_kutulari) kutularıyla bulunur (m7_etiket) · birim = ad öneki
 - animasyonlu düğümler (döner valf rotoru, kaset helezon/karıştırıcı, pistonlar) düğüm translation + animasyon kanalı ile ötelenir
 - silinen: sos eğri hortumu, sos üst raf contası (eğri hortum için), kaşar/sucuk yan kilit mandalları (m7c yenisini kurar)
 - kopya: harç çıkış dirseği 316L + TC kelepçe + D32 düz hortum + üst raf contası → sos yeni yerine (X_R)
Üretece taşınacak yer: topping_uno_cad / h3 TOPPING montaj yerleşim tablosu (birim x'leri m7_olcu.DX)."""
import sys, re, numpy as np
sys.path.insert(0, ".")
from m7kit import Glb
from m7_etiket import etiketle
from m7_olcu import DX, X_L, X_R

gi, go = sys.argv[1], sys.argv[2]
G = Glb(gi)
R = etiketle(G, ("TOPPING_MODUL",))
rap = []


def birim(ad, lo, hi):
    if ad.startswith("kablo"): return None
    if "mandal" in ad: return "SIL"
    if ad in ("sos_urun_hortumu_D32", "ust_raf_gecis_contasi_sos"): return "SIL"
    if re.match(r"^(raf_gecis_contasi_|ust_raf_gecis_contasi_)?(kiyma|kusbasi|sos|harc)(_|$)", ad):
        return re.match(r"^(?:raf_gecis_contasi_|ust_raf_gecis_contasi_)?(kiyma|kusbasi|sos|harc)", ad).group(1)
    if ad.startswith("soguk_"): return None
    if "kasar" in ad: return "kasar"
    if "sucuk" in ad: return "sucuk"
    if ad == "?":
        if lo[0] >= 2020 and hi[0] <= 2105 and lo[1] >= 1040 and hi[1] <= 1150: return "kasar"
        if lo[0] >= 2270 and hi[0] <= 2355 and lo[1] >= 1040 and hi[1] <= 1150: return "sucuk"
    return None


# ---------------------------------------------------------------- 1 · sos'a harç tipi çıkış kopyası (taşımadan önce)
KOPYA = ("harc_cikis_dirsegi_316L", "harc_cikis_dirsegi_tc_kelepcesi", "harc_urun_hortumu_D32", "ust_raf_gecis_contasi_harc")
dk = X_R - 2190.0
SOS_MEK = None
for i, (tl, kut, ad) in R.items():
    for c, nm in ad.items():
        if nm == "sos_hazne_bizim" and SOS_MEK is None:
            p = G.prims[i]; SOS_MEK = G.etiket_of(p, int(np.where((tl == c) & G.gorunur(p))[0][0]), "mek")
for i, (tl, kut, ad) in R.items():
    p = G.prims[i]
    for c, nm in ad.items():
        if nm not in KOPYA: continue
        m = (tl == c) & G.gorunur(p); ti = np.where(m)[0]
        Xf = p["X"][p["T"][m]].reshape(-1, 3) + np.array([dk, 0, 0])
        G.ekle_etiket(p, Xf, np.arange(len(Xf)).reshape(-1, 3), kat=G.etiket_of(p, ti[0]), mek=SOS_MEK)
        rap.append("KOPYA %-40s %s → x+%.0f (sos)" % (nm, p["name"], dk))

# ---------------------------------------------------------------- 2 · taşı / sil
say = {}
for i, (tl, kut, ad) in R.items():
    p = G.prims[i]
    if "__PISTON_" in p["name"]: continue
    vis = G.gorunur(p)
    for c, nm in ad.items():
        lo, hi, n = kut[c]
        u = birim(nm, lo, hi)
        if u is None: continue
        m = (tl == c) & vis
        if u == "SIL":
            G.sil(p, m); rap.append("SIL   %-40s %s %d üçgen" % (nm, p["name"], m.sum())); continue
        d = DX[u]
        G.tasi(p, m, lambda V, d=d: V + np.array([d, 0, 0]))
        say.setdefault(u, []).append(nm)

# ---------------------------------------------------------------- 3 · animasyonlu düğümler
DUGUM = {"TOPPING_DONER__VALF_KIYMA": "kiyma", "TOPPING_DONER__VALF_KUSBASI": "kusbasi", "TOPPING_DONER__VALF_SOS": "sos",
         "TOPPING_DONER__VALF_HARC": "harc", "TOPPING_DONER__HELEZON_KASAR": "kasar", "TOPPING_DONER__KARISTIRICI_KASAR": "kasar",
         "TOPPING_DONER__HELEZON_SUCUK": "sucuk", "TOPPING_DONER__KARISTIRICI_SUCUK": "sucuk"}
for u in ("KIYMA", "KUSBASI", "SOS", "HARC"):
    for mt in ("paslanmaz", "pom"): DUGUM["TOPPING_MODUL__%s__PISTON_%s" % (mt, u)] = u.lower()
# paylaşılan çıktı erişimcisi aynı ötelemeyle ise bir kez kaydırılır
acc_d = {}
for ad_, u in DUGUM.items():
    J = G.J; ni = [k for k, nd in enumerate(J["nodes"]) if nd.get("name") == ad_][0]
    for an in J.get("animations", []):
        for ch in an["channels"]:
            if ch["target"]["node"] == ni and ch["target"]["path"] == "translation":
                a = an["samplers"][ch["sampler"]]["output"]
                if a in acc_d and acc_d[a] != DX[u]: raise RuntimeError("paylaşılan erişimci farklı öteleme: %s" % ad_)
                acc_d[a] = DX[u]
G._otelenen_acc = {}
yapilan = set()
for ad_, u in DUGUM.items():
    d = np.array([DX[u], 0, 0])
    J = G.J; ni = [k for k, nd in enumerate(J["nodes"]) if nd.get("name") == ad_][0]; nd = J["nodes"][ni]
    nd["translation"] = (np.array(nd.get("translation", [0, 0, 0]), float) + d / 1000.0).tolist()
    for p in G.prims:
        if p["nd"] is nd: p["t"] = np.array(nd["translation"], float); p["X"] = p["X"] + d
    for an in J.get("animations", []):
        for ch in an["channels"]:
            if ch["target"]["node"] != ni or ch["target"]["path"] != "translation": continue
            a = an["samplers"][ch["sampler"]]["output"]
            if a in yapilan: continue
            yapilan.add(a)
            A = J["accessors"][a]; v = J["bufferViews"][A["bufferView"]]
            off = v.get("byteOffset", 0) + A.get("byteOffset", 0); n = A["count"]
            arr = np.frombuffer(bytes(G.BIN[off:off + n * 12]), np.float32).reshape(-1, 3).copy() + (d / 1000.0).astype(np.float32)
            G.BIN[off:off + n * 12] = arr.tobytes()
            if "min" in A: A["min"] = arr.min(0).tolist(); A["max"] = arr.max(0).tolist()
    rap.append("DUGUM %-40s x%+.1f" % (ad_, DX[u]))

for u, l in say.items(): rap.append("TASI  %-8s %+7.1f  %3d bileşen: %s" % (u, DX[u], len(l), ", ".join(sorted(set(l)))))
G.kaydet(go)
open(go.replace(".glb", "_rapor.txt"), "w", encoding="utf-8").write("\n".join(rap))
print("\n".join(rap)); print("yazildi", go)
