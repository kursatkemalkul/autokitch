# -*- coding: utf-8 -*-
"""B ÇEKMECE + DEPO FİTİLLERİ (Kemal 2 Eki: "B dolabı fitilini yap").
SORUN: eski fitil (geçmeli manyetik profil, taban 21) yolu açıklık kenarının 4 mm dışındaydı → tabanın 6,5 mm'si açıklığın içine
taşıyor, çerçeveye yalnız ~%70 (depo %63) değiyordu.
ÇÖZÜM (gerçekte olduğu gibi: fitil açıklığın tamamen DIŞINDA, çerçeve yüzüne basar):
  · Komşu açıklıklar arası çerçeve köprüsü 33 (kolon içi, kapak derzi 3 → kapak açıklıktan 15 taşar) / 35 (kolonlar arası, 16 taşar).
    21'lik taban hem çerçevenin üstünde hem kapağın altında kalamaz (21 > 15). → DAR PROFİL: taban 14 (ezik gövde 15 aynı, geçme dili +
    kanal 6,4 × 8,4 AYNI → kapak kanalı ölçüsü değişmez). Taban açıklık kenarından 0,5 dışarıda başlar (0,5 … 14,5) → kapak kenarına 0,5 kalır.
  · Yol her kenarda ayrı: c = min(7,5 ; kapak taşması − 0,5 − 7). Depo ALT kenarı: kapak açıklıktan yalnız 7 taşar (altında servis paneli,
    derz 3) → kanal kapakta kalmak zorunda → orta yol c = −0,5 (taban 457–471, çerçevede 6,5 / 14).
  · Kapak (dış ölçü DEĞİŞMEZ): dış sac 1,5 kabuk + arkada kanal dış kenarına kadar dönüş · PU · iç sac 1,0 (kanalın içi) — kanal yeni yolda.
Dokunulan düğümler: CEK_*__on_seffaf__CEKMECE (kapak + fitil, tamamen yeniden) · B_DEPO__conta__CEKMECE (fitil) · B_DEPO__pu__CEKMECE (kapak PU) ·
B_DEPO__sac__CEKMECE (yalnız son 56 üçgen = kapak dış + iç sacı; ilk 108 üçgen — kap / ayırıcı — aynen).
Kullanım: python b_fitil_duzelt.py giris.glb cikis.glb"""
import json, struct, sys
import numpy as np
import cadquery as cq
import glb_oku
import b_govde_yeni as BG

# ---------------------------------------------------------------- profil (u: yoldan DIŞARI, z mutlak) · taban 14
FW = 14.0
FITIL = [(-7.0, 24.0), (7.0, 24.0), (7.0, 29.0), (5.5, 29.0), (5.5, 37.0), (4.0, 37.0), (4.0, 39.0), (2.0, 39.0), (2.0, 43.8), (3.15, 45.0),
         (2.0, 46.0), (2.0, 47.3), (-2.0, 47.3), (-2.0, 46.0), (-3.15, 45.0), (-2.0, 43.8), (-2.0, 39.0), (-4.0, 39.0), (-4.0, 37.0),
         (-5.5, 37.0), (-5.5, 29.0), (-7.0, 29.0)]
KAN = 3.2                       # kanal yarı genişliği (6,4) · z 39 … 47,4
ZK0, ZK1, ZKD, ZPU0, ZPU1, ZK_ = 39.0, 79.0, 40.5, 40.5, 77.5, 47.4
PAY = 0.5                       # taban ↔ açıklık kenarı ve taban ↔ kapak kenarı payı
C_MAX = PAY + FW / 2.0          # 7,5


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))


def genis(R, d):
    return (R[0] - d, R[1] + d, R[2] - d, R[3] + d)


def yol(ack, kap):
    """her kenar için yol ofseti (açıklıktan dışarı) — c = min(7,5 ; taşma − 0,5 − 7)"""
    ax0, ax1, ay0, ay1 = ack; a, b, c, d = kap
    ov = (ax0 - a, b - ax1, ay0 - c, d - ay1)
    cs = [min(C_MAX, o - PAY - FW / 2.0) for o in ov]
    return (ax0 - cs[0], ax1 + cs[1], ay0 - cs[2], ay1 + cs[3]), cs, ov


def fitil_ag(P):
    """dikdörtgen yol P boyunca profilin keskin (gönye) köşeli süpürmesi → üçgenler (n, 3, 3) mm"""
    L = []
    for u, z in FITIL:
        x0, x1, y0, y1 = genis(P, u)
        L.append(np.array([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)]))
    tr = []
    n = len(L)
    for i in range(n):
        A, B = L[i], L[(i + 1) % n]
        for j in range(4):
            k = (j + 1) % 4
            tr += [(A[j], A[k], B[k]), (A[j], B[k], B[j])]
    tr = np.array(tr)
    v = np.einsum("ij,ij->i", tr[:, 0], np.cross(tr[:, 1], tr[:, 2])).sum() / 6.0
    if v < 0: tr = tr[:, [0, 2, 1]]
    return tr


def kapak_kati(kap, P):
    a, b, c, d = kap
    ko, ki = genis(P, KAN), genis(P, -KAN)                       # kanal dış / iç dikdörtgeni
    ds = kutu(a, b, c, d, ZK0, ZK1).cut(kutu(a + 1.5, b - 1.5, c + 1.5, d - 1.5, ZKD, ZPU1)).cut(kutu(*ko, ZK0 - 1.0, ZKD))
    ic = kutu(*ki, ZK0, ZK0 + 1.0)
    pu = kutu(a + 1.5, b - 1.5, c + 1.5, d - 1.5, ZPU0, ZPU1).cut(kutu(*ko, ZPU0 - 1.0, ZK_)).fuse(kutu(*ki, ZK0 + 1.0, ZK_)).clean()
    for s in (ds, ic, pu): assert len(s.Solids()) == 1, "kapak katısı tek parça değil"
    return ds, pu, ic


def tri_kati(solidler):
    out = []
    for s in solidler:
        for f in s.Faces():
            v, t = f.tessellate(0.1, 0.2)
            if len(t):
                V = np.array([[q.x, q.y, q.z] for q in v]); out.append(V[np.array(t)])
    return np.concatenate(out)


# ---------------------------------------------------------------- birimler
def birimler(D):
    U = {}
    for n in D:
        if n.startswith("CEK_") and n.endswith("__on_seffaf__CEKMECE"):
            u = n.split("__")[0]; X, T = D[n]; P = X[T]
            K = P[P[:, :, 2].min(1) >= 38.99].reshape(-1, 3)
            kap = (K[:, 0].min(), K[:, 0].max(), K[:, 1].min(), K[:, 1].max())
            m = [(x0, x1, y0, y1) for _k, x0, x1, y0, y1 in BG.ACIKLIK if kap[0] < (x0 + x1) / 2 < kap[1] and kap[2] < (y0 + y1) / 2 < kap[3]]
            assert len(m) == 1, u
            U[u] = dict(kap=tuple(round(float(q), 3) for q in kap), ack=m[0], strok=700.0)
    X, T = D["B_DEPO__sac__CEKMECE"]; K = X[T[-56:]].reshape(-1, 3)
    assert K[:, 2].min() > 38.9
    U["B_DEPO"] = dict(kap=tuple(round(float(q), 3) for q in (K[:, 0].min(), K[:, 0].max(), K[:, 1].min(), K[:, 1].max())), ack=BG.DEPO_ACIK, strok=450.0)
    for u, r in U.items():
        r["P"], r["c"], r["ov"] = yol(r["ack"], r["kap"])
        r["fit"] = fitil_ag(r["P"])
        r["ds"], r["pu"], r["ic"] = kapak_kati(r["kap"], r["P"])
    return U


# ---------------------------------------------------------------- GLB yazımı
def glb_yaz(gi, go, U):
    raw = open(gi, "rb").read()
    jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
    bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = bytearray(raw[bo + 8:bo + 8 + bl])
    TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}

    def oku(i, n):
        a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]; dt = TD[a["componentType"]]
        o = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        r = np.frombuffer(bytes(BIN[o:o + a["count"] * n * np.dtype(dt).itemsize]), dt)
        return r.reshape(-1, n) if n > 1 else r

    def ekle(arr, tip, hedef):
        while len(BIN) % 4: BIN.extend(b"\0")
        off = len(BIN); BIN.extend(arr.tobytes())
        J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": hedef})
        a = {"bufferView": len(J["bufferViews"]) - 1, "componentType": 5126 if arr.dtype == np.float32 else 5125, "count": int(len(arr)), "type": tip}
        if tip == "VEC3": a["min"] = arr.min(axis=0).tolist(); a["max"] = arr.max(axis=0).tolist()
        J["accessors"].append(a); return len(J["accessors"]) - 1

    def koy(dugum, tri_mm, bas=None):
        """tri_mm (n,3,3) mm · bas: korunacak ilk üçgenler (n,3,3) mm (sıra korunur)"""
        nd = [n for n in J["nodes"] if n.get("name") == dugum][0]
        for k in ("rotation", "scale", "matrix"): assert k not in nd, dugum
        t = np.array(nd.get("translation", [0, 0, 0])) * 1000.0
        assert np.allclose(t, 0), dugum
        pr = J["meshes"][nd["mesh"]]["primitives"]; assert len(pr) == 1; pr = pr[0]
        tr = tri_mm if bas is None else np.concatenate([bas, tri_mm])
        Xf = tr.reshape(-1, 3); n = np.cross(tr[:, 1] - tr[:, 0], tr[:, 2] - tr[:, 0])
        n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
        pr["attributes"] = {"POSITION": ekle((Xf / 1000.0).astype(np.float32), "VEC3", 34962),
                            "NORMAL": ekle(np.repeat(n, 3, axis=0).astype(np.float32), "VEC3", 34962)}
        pr["indices"] = ekle(np.arange(len(Xf), dtype=np.uint32), "SCALAR", 34963)
        return pr, len(Xf)

    def tri_oku(dugum):
        nd = [n for n in J["nodes"] if n.get("name") == dugum][0]; pr = J["meshes"][nd["mesh"]]["primitives"][0]
        X = oku(pr["attributes"]["POSITION"], 3).astype(float) * 1000.0; I = oku(pr["indices"], 1).astype(np.int64)
        return X[I.reshape(-1, 3)], pr

    for u, r in U.items():
        kap_tri = tri_kati([r["ds"], r["pu"], r["ic"]])
        if u != "B_DEPO":
            pr, ni = koy(u + "__on_seffaf__CEKMECE", np.concatenate([kap_tri, r["fit"]]))
            ex = pr.setdefault("extras", {})
            ex["kat"] = [ex.get("kat", [0])[0], 0, ni]; ex["mek"] = [ex["mek"][0], 0, ni]; ex["kpk"] = [0, ni]
        else:
            pr, ni = koy("B_DEPO__conta__CEKMECE", r["fit"]); ex = pr["extras"]
            ex["kat"] = [ex["kat"][0], 0, ni]; ex["mek"] = [ex["mek"][0], 0, ni]; ex["kpk"] = [0, ni]
            pr, ni = koy("B_DEPO__pu__CEKMECE", tri_kati([r["pu"]])); ex = pr["extras"]
            ex["kat"] = [ex["kat"][0], 0, ni]; ex["mek"] = [ex["mek"][0], 0, ni]; ex["kpk"] = [0, ni]
            eski, pr0 = tri_oku("B_DEPO__sac__CEKMECE")
            ex0 = pr0["extras"]; assert ex0["kpk"] == [324, 168] and ex0["kat"][3:] == [0, 192, 300], ex0
            pr, ni = koy("B_DEPO__sac__CEKMECE", tri_kati([r["ds"], r["ic"]]), bas=eski[:108]); ex = pr["extras"]
            ex["kat"] = [ex["kat"][0], 0, 192, 0, 192, ni - 192]; ex["mek"] = [ex["mek"][0], 0, ni]; ex["kpk"] = [324, ni - 324]
    J["buffers"][0]["byteLength"] = len(BIN)
    jb = json.dumps(J, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
    while len(BIN) % 4: BIN.extend(b"\0")
    open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb
                         + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
    print("yazıldı", go)


if __name__ == "__main__":
    gi, go = sys.argv[1:3]
    J, D = glb_oku.yukle(gi)
    U = birimler(D)
    print("%-16s %-27s %-27s %-27s" % ("birim", "kapak taşma s/s/a/ü", "yol ofseti s/s/a/ü", "fitil dış x / y"))
    for u, r in U.items():
        o = genis(r["P"], 7.0)
        print("%-16s %6.1f %6.1f %6.1f %6.1f  %6.2f %6.2f %6.2f %6.2f  %7.1f–%7.1f / %5.1f–%5.1f" % ((u,) + tuple(r["ov"]) + tuple(r["c"]) + o))
    glb_yaz(gi, go, U)
