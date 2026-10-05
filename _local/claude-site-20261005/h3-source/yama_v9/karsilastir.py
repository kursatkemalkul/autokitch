# -*- coding: utf-8 -*-
"""İki GLB'yi parça parça karşılaştırır (v9 tam derlemesi ↔ v8zq): düğüm adları/sırası/dönüşümleri, ağ başına üçgen sayısı ve indisler,
köşe koordinatları (±tol mm), normaller, primitive extras (kat / mek / kpk), malzemeler, sahne extras, animasyonlar (kanal + anahtar değerleri).
python karsilastir.py A.glb B.glb [rapor.md] [--tol 0.01]
Çıkış kodu 0 = fark yok (tolerans içinde)."""
import json, struct, sys
import numpy as np

TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8, 5122: np.int16, 5120: np.int8}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


def yukle(yol):
    raw = open(yol, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]
    J = json.loads(raw[20:20 + jl]); bo = 20 + jl; bl = struct.unpack("<I", raw[bo:bo + 4])[0]
    return J, raw[bo + 8:bo + 8 + bl], len(raw)


def acc(J, BIN, i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
    n = NC[a["type"]]; dt = TD[a["componentType"]]; off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    st = v.get("byteStride")
    if st and st != n * np.dtype(dt).itemsize:
        r = np.lib.stride_tricks.as_strided(np.frombuffer(BIN, np.uint8, offset=off), (a["count"], st), (st, 1))
        r = r[:, :n * np.dtype(dt).itemsize].copy().view(dt)
    else:
        r = np.frombuffer(BIN, dt, count=a["count"] * n, offset=off)
    return r.reshape(-1, n) if n > 1 else r


def temiz(o, at=("buffers", "bufferViews", "accessors")):
    return {k: v for k, v in o.items() if k not in at}


def main():
    arg = [x for x in sys.argv[1:] if not x.startswith("--")]
    tol = float(sys.argv[sys.argv.index("--tol") + 1]) if "--tol" in sys.argv else 0.01
    if "--tol" in sys.argv: arg = [x for x in arg if x != sys.argv[sys.argv.index("--tol") + 1]]
    pa, pb = arg[:2]; rap = arg[2] if len(arg) > 2 else None
    JA, BA, na = yukle(pa); JB, BB, nb = yukle(pb)
    L = []; fark = 0
    def yaz(s): L.append(s); print(s)
    yaz("# GLB KARŞILAŞTIRMA\n\nA = `%s` (%d bayt)  \nB = `%s` (%d bayt)  \nköşe toleransı ±%g mm\n" % (pa, na, pb, nb, tol))
    bayt = open(pa, "rb").read() == open(pb, "rb").read()
    yaz("- bayt bayt: **%s**" % ("AYNI" if bayt else "farklı (aşağıda anlamsal karşılaştırma)"))
    # 1 · yapı
    for k in ("nodes", "meshes", "materials", "animations", "scenes", "textures", "images", "samplers", "skins"):
        a, b = JA.get(k, []), JB.get(k, [])
        if len(a) != len(b): yaz("- %s sayısı FARKLI: %d ↔ %d" % (k, len(a), len(b))); fark += 1
    na_ = [n.get("name") for n in JA["nodes"]]; nb_ = [n.get("name") for n in JB["nodes"]]
    if na_ != nb_:
        sa, sb = set(na_), set(nb_)
        yaz("- düğüm adları/sırası FARKLI · yalnız A: %s · yalnız B: %s" % (sorted(sa - sb)[:30], sorted(sb - sa)[:30])); fark += 1
    else: yaz("- düğüm adları + sırası: aynı (%d düğüm)" % len(na_))
    for k in ("materials", "scenes", "asset"):
        if json.dumps(JA.get(k), sort_keys=True) != json.dumps(JB.get(k), sort_keys=True): yaz("- %s FARKLI" % k); fark += 1
    yaz("- malzemeler / sahne (extras: mekanizmalar, kategoriler…): %s" % ("aynı" if json.dumps([JA.get("materials"), JA.get("scenes")], sort_keys=True) == json.dumps([JB.get("materials"), JB.get("scenes")], sort_keys=True) else "FARKLI"))
    # 2 · düğüm dönüşümleri + ağlar
    tab = []; ytop = dict(dugum=0, ucgen=0, maxd=0.0)
    bmap = {n.get("name"): i for i, n in enumerate(JB["nodes"])}
    for ia, nA in enumerate(JA["nodes"]):
        ad = nA.get("name"); ib = bmap.get(ad)
        if ib is None: continue
        nB = JB["nodes"][ib]
        sorun = []
        for k in ("translation", "rotation", "scale", "matrix"):
            va, vb = nA.get(k), nB.get(k)
            if (va is None) != (vb is None) or (va is not None and not np.allclose(va, vb, atol=1e-9)): sorun.append(k)
        ca = [JA["nodes"][c].get("name") for c in nA.get("children", [])]; cb = [JB["nodes"][c].get("name") for c in nB.get("children", [])]
        if ca != cb: sorun.append("children")
        if json.dumps(nA.get("extras"), sort_keys=True) != json.dumps(nB.get("extras"), sort_keys=True): sorun.append("extras")
        nt = (0, 0); md = 0.0
        if ("mesh" in nA) != ("mesh" in nB): sorun.append("mesh var/yok")
        elif "mesh" in nA:
            mA, mB = JA["meshes"][nA["mesh"]], JB["meshes"][nB["mesh"]]
            if len(mA["primitives"]) != len(mB["primitives"]): sorun.append("primitive sayısı")
            ta = tb = 0
            for pA, pB in zip(mA["primitives"], mB["primitives"]):
                if json.dumps(pA.get("extras"), sort_keys=True) != json.dumps(pB.get("extras"), sort_keys=True): sorun.append("extras(kat/mek/kpk)")
                if pA.get("mode", 4) != pB.get("mode", 4): sorun.append("mode")
                if json.dumps(JA["materials"][pA["material"]] if "material" in pA else None, sort_keys=True) != json.dumps(JB["materials"][pB["material"]] if "material" in pB else None, sort_keys=True): sorun.append("malzeme")
                if sorted(pA["attributes"]) != sorted(pB["attributes"]): sorun.append("öznitelikler")
                IA = acc(JA, BA, pA["indices"]).astype(np.int64); IB = acc(JB, BB, pB["indices"]).astype(np.int64)
                ta += len(IA) // 3; tb += len(IB) // 3
                if len(IA) != len(IB) or not np.array_equal(IA, IB): sorun.append("indisler")
                for sem in pA["attributes"]:
                    if sem not in pB["attributes"]: continue
                    XA = acc(JA, BA, pA["attributes"][sem]).astype(float); XB = acc(JB, BB, pB["attributes"][sem]).astype(float)
                    if XA.shape != XB.shape: sorun.append(sem + " boyut"); continue
                    d = float(np.abs(XA - XB).max()) if XA.size else 0.0
                    if sem == "POSITION":
                        d *= 1000.0; md = max(md, d)
                        if d > tol: sorun.append("köşe %.4f mm" % d)
                    elif d > 1e-3: sorun.append("%s %.4g" % (sem, d))
            nt = (ta, tb); ytop["ucgen"] += ta
        ytop["dugum"] += 1; ytop["maxd"] = max(ytop["maxd"], md)
        if sorun: fark += 1; tab.append((ad, nt, md, sorted(set(sorun))))
    yaz("- %d düğüm karşılaştırıldı · toplam %d üçgen · en büyük köşe farkı %.5f mm" % (ytop["dugum"], ytop["ucgen"], ytop["maxd"]))
    # 3 · animasyonlar
    an_f = 0
    for k, (aA, aB) in enumerate(zip(JA.get("animations", []), JB.get("animations", []))):
        if aA.get("name") != aB.get("name") or len(aA["channels"]) != len(aB["channels"]): an_f += 1; continue
        for cA, cB in zip(aA["channels"], aB["channels"]):
            if JA["nodes"][cA["target"]["node"]].get("name") != JB["nodes"][cB["target"]["node"]].get("name") or cA["target"]["path"] != cB["target"]["path"]: an_f += 1; break
            sA, sB = aA["samplers"][cA["sampler"]], aB["samplers"][cB["sampler"]]
            if sA.get("interpolation") != sB.get("interpolation"): an_f += 1; break
            for q in ("input", "output"):
                xa, xb = acc(JA, BA, sA[q]).astype(float), acc(JB, BB, sB[q]).astype(float)
                if xa.shape != xb.shape or (xa.size and np.abs(xa - xb).max() > 1e-6): an_f += 1; break
    yaz("- animasyonlar: %d · farklı: %d" % (len(JA.get("animations", [])), an_f))
    fark += an_f
    if tab:
        yaz("\n## Farklı düğümler (%d)\n\n| düğüm | üçgen A / B | köşe farkı mm | ne farklı |\n|---|---|---|---|" % len(tab))
        for ad, nt, md, s in tab[:400]: yaz("| %s | %d / %d | %.4f | %s |" % (ad, nt[0], nt[1], md, ", ".join(s)))
    yaz("\n**SONUÇ: %s**" % ("FARK YOK (tolerans içinde)" if fark == 0 else "%d FARK" % fark))
    if rap: open(rap, "w", encoding="utf-8").write("\n".join(L) + "\n")
    sys.exit(0 if fark == 0 else 1)


if __name__ == "__main__":
    main()
