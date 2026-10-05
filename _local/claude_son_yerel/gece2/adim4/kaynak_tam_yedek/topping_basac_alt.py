# -*- coding: utf-8 -*-
"""TOPPING KANATLARI — ALT BAS-AÇ (Kemal 2 Eki: "bas-açı da yap").
Taban hat3_v8o.glb → hat3_v8o_basac.glb. Montaj / elektrik ÇALIŞTIRILMAZ: GLB düğüm geometrisi yerinde (topping_govde_yeni yöntemi).

ÜRÜN: üstteki ile AYNI — Southco E4 sınıfı touch latch (push-to-close / push-to-open, gizli) · gövde 30 × 30 × 13 + karşılık (striker)
  plakası 30 × 30 × 3 kanat iç tavasında. Kanat kapanırken bastırılır → kilitlenir; tekrar bastırınca itip açar (kulp yok).
YER: her kanadın ALT serbest köşesi · K1 x 1927–1957 · K2 x 1977–2007 (üsttekilerle aynı x, derz 1965,75 | 1968,75 yanında) ·
  y 900–930 (gövde tabanı 893,5'in 6,5 üstü; kaide C ön profili 788–892 kapalı kutu → mandal oraya sığmaz, kaideye DOKUNULMAZ) ·
  z 26–39 (ön düzlem 39'un arkası, mekanizma bandı açıklığında: hareketli tabla / X arabası en önde z −5, arada 31 mm).
KARŞILIK BRAKETİ (bu işin tek yeni sac parçası): 304 2,0 L-büküm (iç R 2), x 1919–2015 · dik kol z 24–26 / y 893,5–940
  (iki mandal gövdesi önüne vidalı) · yatık kol y 893,5–895,5 / z 6–26 dış taban sacının ÜSTÜNE oturur · 2 × PEM FHS-M4-12 (taban sacına
  alttan preslenmiş, başı sac içinde gömme → kaide üst plakasına bir şey çıkmaz) + 2 × M4 somun (DIN 934). Önden görünmez (kanat kapalıyken).
KANAT: iç tava (1,0) karşılık plakası yerinde 30 × 30 kesilir (üstteki gibi: plaka z 39–42, kanadın boş alt tavasına 2 mm girer).
Kullanım: python topping_basac_alt.py giris.glb cikis.glb [cikti_klasoru]"""
import os, sys, json, struct, time
import numpy as np
import cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tg")); sys.path.insert(0, HERE)
import tgeo as G
from glbx import yukle
from dikis import kati

TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}
BASAC = G.BASAC                                   # üsttekilerle aynı x: K1 1927–1957 · K2 1977–2007
Y_ALT = (900.0, 930.0)
ZG0 = 26.0                                        # mandal gövdesi z 26–39 (üstteki gibi)
BR_X = (1919.0, 2015.0); BR_T = 2.0; BR_RI = 2.0
BR_YUST = 940.0; BR_ZARKA = 6.0; BR_ZDIK = (24.0, 26.0)
STUD = [(1935.0, 14.0), (1999.0, 14.0)]           # PEM FHS-M4-12 (x, z)
Y_TABAN = G.YBI                                   # 893,5 dış taban sacı üstü


def bul(d, bb, e=0.3):
    """parça sınırı = düğümün 'mek' aralıkları (her eklenen parça kendi aralığında) · bbox'ı bb olan aralığın canlı üçgenleri"""
    X, T, ok, m = d["X"], d["T"], d["ok"], d["ex"]["mek"]; out = []
    for k in range(0, len(m), 3):
        a, b = m[k + 1] // 3, (m[k + 1] + m[k + 2]) // 3
        ti = a + np.where(ok[a:b])[0]
        if not len(ti): continue
        Q = X[T[ti]].reshape(-1, 3); mn, mx = Q.min(0), Q.max(0)
        if (np.abs(mn - np.array(bb[0::2])) < e).all() and (np.abs(mx - np.array(bb[1::2])) < e).all(): out.append(ti)
    return out


def etiket_degeri(lst, tri):
    i = tri * 3
    for k in range(0, len(lst), 3):
        if lst[k + 1] <= i < lst[k + 1] + lst[k + 2]: return lst[k]
    return lst[-3] if lst else 0


def ag(s):
    P, I = [], []
    for f in s.Faces():
        v, t = f.tessellate(0.1, 0.2)
        o = sum(len(p) for p in P)
        P.append(np.array([[q.x, q.y, q.z] for q in v], float))
        I.append(np.array(t, np.int64) + o if len(t) else np.zeros((0, 3), np.int64))
    X = np.vstack(P); T = np.vstack(I)
    Xf = X[T.reshape(-1)]; n = np.cross(Xf[1::3] - Xf[0::3], Xf[2::3] - Xf[0::3])
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    return Xf, np.repeat(n, 3, axis=0)


def hex_somun(x, y0, z, af=7.0, h=3.2, delik=2.0):
    """M4 DIN 934 (SW 7 · m 3,2) · y0'dan +y yönünde · ortası saplama çapında (değer, çakışma değil)"""
    r = af / np.sqrt(3.0)
    pts = [cq.Vector(x + r * np.cos(np.pi / 3 * i), y0, z + r * np.sin(np.pi / 3 * i)) for i in range(6)]
    w = cq.Wire.makePolygon(pts, close=True)
    s = cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), cq.Vector(0, h, 0))
    return G.tekle(s.cut(G.silindir(delik, (x, y0 - 1, z), (x, y0 + h + 1, z))))


def braket():
    x0, x1 = BR_X; y0 = Y_TABAN; t = BR_T; za, zd0, zd1 = BR_ZARKA, BR_ZDIK[0], BR_ZDIK[1]
    dik = G.kutu(x0, x1, y0, BR_YUST, zd0, zd1)
    yat = G.kutu(x0, x1, y0, y0 + t, za, zd1)
    s = G.tekle(dik.fuse(yat))
    # büküm: dış köşe (y 893,5 · z 26) R 4 · iç köşe (y 895,5 · z 24) R 2 · kenarlar x yönünde
    s = cq.Workplane().add(s).edges(cq.selectors.BoxSelector((x0 - 1, y0 - 0.1, zd1 - 0.1), (x1 + 1, y0 + 0.1, zd1 + 0.1))).fillet(BR_RI + t).val()
    s = cq.Workplane().add(s).edges(cq.selectors.BoxSelector((x0 - 1, y0 + t - 0.1, zd0 - 0.1), (x1 + 1, y0 + t + 0.1, zd0 + 0.1))).fillet(BR_RI).val()
    del_ = [G.silindir(2.25, (x, y0 - 1, z), (x, y0 + t + 1, z)) for x, z in STUD]               # Ø4,5 saplama delikleri
    return G.tekle(s.cut(*del_))


def parcalar():
    S = {}                                                                                       # sabit (paslanmaz düğümü)
    K = {}                                                                                       # kanatla dönen (on_seffaf düğümü)
    for kn, (x0, x1) in BASAC.items():
        S["onyuz_basac_alt_govde_%s" % kn] = G.kutu(x0, x1, Y_ALT[0], Y_ALT[1], ZG0, G.ZF)
        K["onyuz_basac_alt_karsilik_%s" % kn] = G.kutu(x0, x1, Y_ALT[0], Y_ALT[1], G.ZF, 42.0)
    S["onyuz_basac_alt_karsilik_braketi"] = braket()
    for i, (x, z) in enumerate(STUD):
        S["onyuz_basac_alt_braket_saplama_%d" % i] = G.silindir(2.0, (x, Y_TABAN, z), (x, Y_TABAN + 10.5, z))   # FHS-M4-12 (1,5'i sac içinde)
        S["onyuz_basac_alt_braket_somun_%d" % i] = hex_somun(x, Y_TABAN + BR_T, z)
    return S, K


def yap(gi, go, cikti):
    t0 = time.time()
    J, D = yukle(gi)
    S, K = parcalar()
    for k, s in list(S.items()) + list(K.items()):
        assert s.isValid(), k
    # ---- kanat iç tavaları: eski ağ → katı, karşılık plakası yerinde kesilir
    nd_k = "TOPPING_MODUL__on_seffaf"; nd_s = "TOPPING_MODUL__paslanmaz"
    ICT = {"K1": (G.K1X[0] + 1.5, G.K1X[1] - 1.5, G.KY0 + 1.5, G.KY1 - 1.5, G.ZK0, G.ZK0 + 1.0),
           "K2": (G.K2X[0] + 1.5, G.K2X[1] - 1.5, G.KY0 + 1.5, G.KY1 - 1.5, G.ZK0, G.ZK0 + 1.0)}
    SIL = {nd_k: [], nd_s: []}; YENI = []                                                       # (ad, katı, düğüm, ref üçgen)
    for kn, bb in ICT.items():
        b = bul(D[nd_k], bb); assert len(b) == 1, (kn, len(b))
        ti = b[0]; SIL[nd_k].append(("onyuz_%s_ic_tava" % kn, ti))
        ss = kati(D[nd_k]["X"], D[nd_k]["T"][ti]); assert all(x.isValid() for x in ss), kn          # iç tava = fitil halkasının içi + dışı (2 katı)
        kb = K["onyuz_basac_alt_karsilik_%s" % kn]; v0 = sum(x.Volume() for x in ss)
        yeni = [G.tekle(x.cut(kb)) if G._kesisir_bb(G._bb(x), G._bb(kb)) else x for x in ss]
        assert all(x.isValid() for x in yeni) and abs(v0 - sum(x.Volume() for x in yeni) - 900.0) < 1.0, (kn, v0)
        for i, x in enumerate(yeni): YENI.append(("onyuz_%s_ic_tava_%d" % (kn, i), x, nd_k, int(ti[0])))
        YENI.append(("onyuz_basac_alt_karsilik_%s" % kn, K["onyuz_basac_alt_karsilik_%s" % kn], nd_k, int(ti[0])))
    b = bul(D[nd_s], (BASAC["K1"][0], BASAC["K1"][1], G.BASAC_Y[0], G.BASAC_Y[1], 26.0, G.ZF)); assert len(b) == 1
    ref_s = int(b[0][0])                                                                        # üst bas-aç gövdesi (K1) → kat / mek değeri
    for k, s in S.items(): YENI.append((k, s, nd_s, ref_s))
    print("parça hazır · %.0f s" % (time.time() - t0))
    # ---- GLB yazımı (topping_govde_yeni ile aynı yöntem)
    raw = open(gi, "rb").read()
    jl = struct.unpack("<I", raw[12:16])[0]; JJ = json.loads(raw[20:20 + jl]); bo = 20 + jl
    bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = bytearray(raw[bo + 8:bo + 8 + bl])

    def oku(i):
        a = JJ["accessors"][i]; v = JJ["bufferViews"][a["bufferView"]]; n = {"SCALAR": 1, "VEC3": 3}[a["type"]]; dt = TD[a["componentType"]]
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        r = np.frombuffer(bytes(BIN[off:off + a["count"] * n * np.dtype(dt).itemsize]), dt).copy()
        return r.reshape(-1, n) if n > 1 else r

    def ekle_buf(arr, tip, hedef):
        while len(BIN) % 4: BIN.extend(b"\0")
        off = len(BIN); BIN.extend(arr.tobytes())
        JJ["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": hedef})
        a = {"bufferView": len(JJ["bufferViews"]) - 1, "componentType": 5126 if arr.dtype == np.float32 else 5125, "count": int(len(arr)), "type": tip}
        if tip == "VEC3": a["min"] = arr.min(axis=0).tolist(); a["max"] = arr.max(axis=0).tolist()
        JJ["accessors"].append(a); return len(JJ["accessors"]) - 1

    rapor = dict(silinen=[], yeni=[])
    for nd in (nd_k, nd_s):
        node = [n for n in JJ["nodes"] if n.get("name") == nd][0]
        tr = np.array(node.get("translation", [0, 0, 0]), float)
        assert not any(k in node for k in ("rotation", "scale", "matrix")), nd
        pr = JJ["meshes"][node["mesh"]]["primitives"][0]
        X = oku(pr["attributes"]["POSITION"]); N = oku(pr["attributes"]["NORMAL"]).astype(np.float32)
        T = oku(pr["indices"]).astype(np.uint32).reshape(-1, 3).copy()
        assert len(T) == len(D[nd]["T"])
        ex = pr.setdefault("extras", {})
        for ad, ti in SIL[nd]:
            T[ti, 1] = T[ti, 0]; T[ti, 2] = T[ti, 0]; rapor["silinen"].append([nd, ad, int(len(ti))])
        Xa, Na, Ia = [X.astype(np.float32)], [N], [T.reshape(-1)]
        say = len(X); ek = {"kat": [], "mek": []}; ek_kpk = []
        for ad, s, n2, ref in [y for y in YENI if y[2] == nd]:
            Xf, Nf = ag(s)
            Xa.append((Xf / 1000.0 - tr).astype(np.float32)); Na.append(Nf.astype(np.float32))
            n_ = len(Xf); bas = sum(len(i) for i in Ia); Ia.append(np.arange(say, say + n_, dtype=np.uint32))
            for k in ("kat", "mek"): ek[k].append([etiket_degeri(ex.get(k, []), ref), bas, n_])
            if nd == nd_k: ek_kpk.append([bas, n_])
            say += n_
            rapor["yeni"].append([nd, ad, [round(v, 1) for v in G._bb(s)], n_ // 3])
        pr["attributes"] = {"POSITION": ekle_buf(np.vstack(Xa), "VEC3", 34962), "NORMAL": ekle_buf(np.vstack(Na), "VEC3", 34962)}
        pr["indices"] = ekle_buf(np.concatenate(Ia), "SCALAR", 34963)
        for k in ("kat", "mek"):
            if ex.get(k) is not None:
                for e in ek[k]: ex[k] = list(ex[k]) + e
        if ek_kpk: ex["kpk"] = list(ex.get("kpk", [])) + [v for e in ek_kpk for v in e]
        print("  %-28s sil %d üçgen · +%d parça" % (nd, sum(len(t) for _, t in SIL[nd]), len([y for y in YENI if y[2] == nd])))
    JJ["buffers"][0]["byteLength"] = len(BIN)
    jb = json.dumps(JJ, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
    while len(BIN) % 4: BIN.extend(b"\0")
    open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb
                         + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
    os.makedirs(cikti, exist_ok=True)
    cq.Compound.makeCompound([y[1] for y in YENI]).exportBrep(os.path.join(cikti, "basac_alt_katilar.brep"))
    json.dump(dict(yeni=[[y[0], y[2]] for y in YENI], rapor=rapor), open(os.path.join(cikti, "basac_alt_dizin.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    for r in rapor["yeni"]: print("   +", r)
    print("yazıldı %s · %.0f s" % (go, time.time() - t0))


if __name__ == "__main__":
    yap(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "ba", "cikti"))
    sys.stdout.flush(); os._exit(0)
