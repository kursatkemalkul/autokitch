# -*- coding: utf-8 -*-
"""TP6 · SIPARIS ANIMASYONU: tabla duruslari / tarama araliklari yeni dusme noktalarina.
Eski animasyon v8w dusme noktalariyla uretilmisti (kiyma 1596 · kusbasi 1806 · kasar 2062 · sucuk 2311 · harc 2190 · sos 1645).
Yeni (topfix t2, v8zc+): kiyma 1596 · harc 1722 · kusbasi 1848 · kasar 2088,5 · sos 2259,5 · sucuk 2360,5.
Her urun fazi (tablanin dondugu aralik + o araliktaki duruslar) dx = yeni - eski kadar kaydirilir; ev (x 1086) ve aktarma (x 2365,4) sabit;
fazlar arasi yol anahtarlari x'e gore dogrusal ara degerle. Ayni dx(t) tabla ile giden ARABA dugumlerine ve tablanin ustundeki URUN
dugumlerine (|x - x_tabla| < 200) uygulanir. Zamanlama degismez. python tp6_anim.py giris.glb cikis.glb"""
import json, struct, sys, numpy as np
gi, go = sys.argv[1:3]
raw = open(gi, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]
J = json.loads(raw[20:20 + jl]); bo = 20 + jl; bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = bytearray(raw[bo + 8:bo + 8 + bl])
ESKI = {"kiyma": 1596.0, "kusbasi": 1806.0, "kasar": 2062.0, "sucuk": 2311.0, "harc": 2190.0, "sos": 1645.0}
YENI = {"kiyma": 1596.0, "kusbasi": 1848.0, "kasar": 2088.5, "sucuk": 2360.5, "harc": 1722.0, "sos": 2259.5}
FAZ = {"siparis_kasarli": ["kasar"], "siparis_kiymali": ["kiyma"], "siparis_kusbasili": ["kusbasi"], "siparis_sucuklu": ["kasar", "sucuk"],
       "siparis_lahmacun": ["harc", "harc", "harc", "harc"], "siparis_pizza": ["sos", "kasar", "sucuk"]}
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); LOG.append(s); print(s)


def acc_ref(i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]; n = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}[a["type"]]
    off = v.get("byteOffset", 0) + a.get("byteOffset", 0); return off, a["count"], n


def oku(i):
    off, c, n = acc_ref(i); r = np.frombuffer(bytes(BIN[off:off + c * n * 4]), np.float32).copy()
    return r.reshape(-1, n) if n > 1 else r


def yaz(i, arr):
    off, c, n = acc_ref(i); arr = np.asarray(arr, np.float32); BIN[off:off + arr.nbytes] = arr.tobytes()
    a = J["accessors"][i]
    if "min" in a: a["min"] = arr.reshape(c, -1).min(0).tolist(); a["max"] = arr.reshape(c, -1).max(0).tolist()


ND = {i: nd.get("name", "") for i, nd in enumerate(J["nodes"])}
yapildi = set()
for an in J["animations"]:
    ad = an.get("name"); fazlar = FAZ.get(ad)
    if fazlar is None: continue
    ch = {(ND[c["target"]["node"]], c["target"]["path"]): an["samplers"][c["sampler"]] for c in an["channels"]}
    st = ch[("TOPPING_DONER__TABLA", "translation")]; t = oku(st["input"]); X = oku(st["output"]); x = X[:, 0] * 1000.0
    sr = ch[("TOPPING_DONER__TABLA", "rotation")]; tr = oku(sr["input"]); q = oku(sr["output"]); ang = np.degrees(2 * np.arctan2(q[:, 1], q[:, 3]))
    dd = np.abs(np.diff(ang)) > 1e-3; iv = []; i = 0
    while i < len(dd):
        if dd[i]:
            j = i
            while j < len(dd) and dd[j]: j += 1
            iv.append((float(tr[i]), float(tr[j]))); i = j
        else: i += 1
    if len(iv) != len(fazlar): log("UYARI", ad, "donus araligi", len(iv), "faz", len(fazlar)); continue
    # her faz: donus araligindaki x araligi + bu araliga bitisik durus anahtarlari
    D = np.full(len(t), np.nan)
    for (a0, a1), urun in zip(iv, fazlar):
        dx = YENI[urun] - ESKI[urun]
        m = (t >= a0 - 1e-4) & (t <= a1 + 1e-4)
        if not m.any():
            m = np.zeros(len(t), bool); m[np.argmin(np.abs(t - (a0 + a1) / 2))] = True
        lo, hi = x[m].min() - 0.6, x[m].max() + 0.6
        k = np.where(m)[0]; s, e = k.min(), k.max()
        while s > 0 and lo <= x[s - 1] <= hi: s -= 1
        while e < len(t) - 1 and lo <= x[e + 1] <= hi: e += 1
        D[s:e + 1] = dx
        log("%-18s %-7s t %.2f-%.2f  x %.1f-%.1f -> %.1f-%.1f  (dx %+.1f)" % (ad, urun, t[s], t[e], x[s:e + 1].min(), x[s:e + 1].max(), x[s:e + 1].min() + dx, x[s:e + 1].max() + dx, dx))
    sabit = (np.abs(x - 1086.0) < 0.6) | (np.abs(x - 2365.4) < 0.6)
    D[sabit & np.isnan(D)] = 0.0
    D[0] = 0.0 if np.isnan(D[0]) else D[0]; D[-1] = 0.0 if np.isnan(D[-1]) else D[-1]
    # yol anahtarlari: komsu capalar arasinda x'e gore dogrusal
    cap = np.where(~np.isnan(D))[0]
    for i in range(len(t)):
        if not np.isnan(D[i]): continue
        a = cap[cap < i].max(); b = cap[cap > i].min()
        f = (x[i] - x[a]) / (x[b] - x[a]) if abs(x[b] - x[a]) > 1e-6 else 0.0
        D[i] = D[a] + (D[b] - D[a]) * np.clip(f, 0, 1)
    def dx_t(tt): return np.interp(tt, t, D)
    # tabla + araba (ayni zaman tabani) + tablanin ustundeki urunler
    xt = lambda tt: np.interp(tt, t, x)
    n_urun = 0
    for (nm, path), smp in ch.items():
        if path != "translation": continue
        if smp["output"] in yapildi: continue
        if nm == "TOPPING_DONER__TABLA" or nm.endswith("__ARABA"):
            tt = oku(smp["input"]); O = oku(smp["output"]); O[:, 0] += dx_t(tt) / 1000.0; yaz(smp["output"], O); yapildi.add(smp["output"])
        elif nm.startswith("URUN__"):
            tt = oku(smp["input"]); O = oku(smp["output"])
            yak = np.abs(O[:, 0] * 1000.0 - xt(tt)) < 200.0
            d = np.where(yak, dx_t(tt), 0.0)
            if np.abs(d).max() > 0.01:
                O[:, 0] += d / 1000.0; yaz(smp["output"], O); yapildi.add(smp["output"]); n_urun += 1
    X2 = oku(st["output"])[:, 0] * 1000.0
    pl = []; i = 0
    while i < len(t) - 1:
        j = i
        while j + 1 < len(t) and abs(X2[j + 1] - X2[i]) < 0.05: j += 1
        if t[j] - t[i] > 0.3: pl.append((round(float(X2[i]), 1), round(float(t[i]), 2), round(float(t[j]), 2)))
        i = j + 1
    log("   yeni duruslar", pl, "· x araligi %.1f-%.1f · urun izi %d" % (X2.min(), X2.max(), n_urun))
jb = json.dumps(J, separators=(",", ":"), ensure_ascii=False).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
open(go.replace(".glb", "_log.txt"), "w", encoding="utf-8").write("\n".join(LOG)); log("yazildi", go)
