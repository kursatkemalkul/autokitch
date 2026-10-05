# -*- coding: utf-8 -*-
"""PAKET 2 · p1.glb -> p2.glb (ham JSON):
 - ROBOT_* dugumleri (kol, yer rayi, zincir olugu, enerji zinciri, robot kablolari, zemin ustu kablo koprusu) silinir; robot kolunun
   siparis animasyon kanallari + orneklecileri silinir; dugum / mesh / sahne / kanal indisleri yeniden.
 - montaj agaci: Robot istasyonu kalkar; robot kontrol kutusu -> 'QR/Robot kutusu (rezerv)'; 'Cevre/Dukkan hatti' Zemin'den sonra.
 - silinmis (dejenere) ucgenler atilir; mek / kat / kpk araliklari yeniden kurulur (indis birimi).
python p2_dugum.py p1.glb p2.glb"""
import json, struct, sys, numpy as np
gi, go = sys.argv[1:3]
raw = open(gi, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]
J = json.loads(raw[20:20 + jl]); bo = 20 + jl; bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = bytearray(raw[bo + 8:bo + 8 + bl])
LOG = []
def log(*a): s = " ".join(str(x) for x in a); LOG.append(s); print(s)
TD = {5125: np.uint32, 5123: np.uint16, 5121: np.uint8}

# ---------------------------------------------------------------- 1 · dugum silme
N = J["nodes"]
SIL = [i for i, n in enumerate(N) if n.get("name", "").startswith("ROBOT_")]
log("silinecek dugumler:", [N[i]["name"] for i in SIL])
assert all(not N[i].get("children") for i in SIL)
sil_mesh = set(N[i]["mesh"] for i in SIL if "mesh" in N[i])
for i, n in enumerate(N):
    if i not in SIL and n.get("mesh") in sil_mesh: raise RuntimeError("paylasilan mesh")
nmap = {}; yeniN = []
for i, n in enumerate(N):
    if i in SIL: continue
    nmap[i] = len(yeniN); yeniN.append(n)
mmap = {}; yeniM = []
for i, m in enumerate(J["meshes"]):
    if i in sil_mesh: continue
    mmap[i] = len(yeniM); yeniM.append(m)
for n in yeniN:
    if "mesh" in n: n["mesh"] = mmap[n["mesh"]]
    if "children" in n: n["children"] = [nmap[c] for c in n["children"] if c in nmap]
for sc in J["scenes"]: sc["nodes"] = [nmap[c] for c in sc["nodes"] if c in nmap]
nk = 0
for an in J.get("animations", []):
    ch = [c for c in an["channels"] if c["target"]["node"] not in SIL]; nk += len(an["channels"]) - len(ch)
    kul = sorted(set(c["sampler"] for c in ch)); smap = {s: k for k, s in enumerate(kul)}
    an["samplers"] = [an["samplers"][s] for s in kul]
    for c in ch: c["sampler"] = smap[c["sampler"]]; c["target"]["node"] = nmap[c["target"]["node"]]
    an["channels"] = ch
J["nodes"] = yeniN; J["meshes"] = yeniM
for k in ("skins", "cameras"): assert not J.get(k), k
log("dugum %d silindi, animasyon kanali %d silindi" % (len(SIL), nk))

# ---------------------------------------------------------------- 2 · montaj agaci sirasi
E = J["scenes"][0]["extras"]; ESKI = [m["kod"] for m in E["mekanizmalar"]]
YENI_SIRA = []
for m in E["mekanizmalar"]:
    k = m["kod"]
    if k.startswith("Robot/") or k == "Çevre/Dükkân hattı": continue
    if k == "QR/Elektrik": YENI_SIRA.append({"kod": "QR/Robot kutusu (rezerv)", "istasyon": "QR", "ad": "Robot kutusu (rezerv)"})
    YENI_SIRA.append(m)
    if k == "Çevre/Zemin": YENI_SIRA.append({"kod": "Çevre/Dükkân hattı", "istasyon": "Çevre", "ad": "Dükkân hattı"})
YK = [m["kod"] for m in YENI_SIRA]
LMAP = {}
for i, k in enumerate(ESKI):
    if k == "Robot/Kontrol kutusu": LMAP[i] = YK.index("QR/Robot kutusu (rezerv)")
    elif k in YK: LMAP[i] = YK.index(k)
    else: LMAP[i] = None
E["mekanizmalar"] = YENI_SIRA
E["gruplama"] = E.get("gruplama", "") + " · v2 3 Eki 2026: robot kalktı (kontrol kutusu QR'da rezerv), Çevre/Dükkân hattı (makine dışı ana hat)"
log("unite", len(ESKI), "->", len(YK))

# ---------------------------------------------------------------- 3 · dejenere ucgenleri at + etiketleri yeniden kur
def oku(ai):
    a = J["accessors"][ai]; v = J["bufferViews"][a["bufferView"]]; dt = TD[a["componentType"]]
    off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    return np.frombuffer(bytes(BIN[off:off + a["count"] * np.dtype(dt).itemsize]), dt).copy()
def yaz(arr):
    global BIN
    while len(BIN) % 4: BIN += b"\0"
    off = len(BIN); BIN += arr.tobytes()
    J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": 34963})
    J["accessors"].append({"bufferView": len(J["bufferViews"]) - 1, "componentType": 5125, "count": int(len(arr)), "type": "SCALAR"})
    return len(J["accessors"]) - 1
def acil(L, n, bos=-1):
    a = np.full(n, bos, np.int64)
    for i in range(0, len(L) - 2, 3): a[L[i + 1] // 3:(L[i + 1] + L[i + 2]) // 3] = L[i]
    return a
def kos(a):
    out = []; i = 0; n = len(a)
    br = np.r_[0, np.where(np.diff(a) != 0)[0] + 1, n]
    for s, e in zip(br[:-1], br[1:]):
        if e > s: out += [int(a[s]), int(s) * 3, int(e - s) * 3]
    return out
tot0 = tot1 = 0; robot_kalan = 0
for me in J["meshes"]:
    for pr in me["primitives"]:
        if pr.get("mode", 4) != 4: continue
        I = oku(pr["indices"]).astype(np.int64).reshape(-1, 3); n = len(I); tot0 += n
        ex = pr.get("extras", {})
        dej = (I[:, 0] == I[:, 1]) & (I[:, 1] == I[:, 2])
        keep = ~dej
        mek = acil(ex["mek"], n) if ex.get("mek") else None
        if mek is not None:
            yeni = np.array([LMAP[x] if x >= 0 and LMAP[x] is not None else -9 for x in mek])
            robot_kalan += int(((yeni == -9) & keep).sum())
        kat = acil(ex["kat"], n) if ex.get("kat") else None
        kpk = np.zeros(n, bool)
        L = ex.get("kpk") or []
        for i in range(0, len(L) - 1, 2): kpk[L[i] // 3:(L[i] + L[i + 1]) // 3] = True
        if not keep.all():
            pr["indices"] = yaz(I[keep].reshape(-1).astype(np.uint32))
        I2 = I[keep]; tot1 += len(I2)
        if mek is not None: ex["mek"] = kos(yeni[keep])
        if kat is not None: ex["kat"] = kos(kat[keep])
        if ex.get("kpk") is not None or kpk.any():
            k2 = kpk[keep]; idx = np.where(k2)[0]; runs = []
            if len(idx):
                b = np.where(np.diff(idx) > 1)[0]; st = np.r_[idx[0], idx[b + 1]]; en = np.r_[idx[b], idx[-1]]
                for a_, e_ in zip(st, en): runs += [int(a_) * 3, int(e_ - a_ + 1) * 3]
            if runs: ex["kpk"] = runs
            else: ex.pop("kpk", None)
        if ex: pr["extras"] = ex
log("ucgen %d -> %d (dejenere %d atildi) · silinmis uniteye bagli gorunur ucgen: %d" % (tot0, tot1, tot0 - tot1, robot_kalan))
assert robot_kalan == 0
# bos primitive / mesh kalmasin (onceki adimlarda butun ucgenleri silinmis olanlar)
bosm = []
for mi, me in enumerate(J["meshes"]):
    once = len(me["primitives"])
    me["primitives"] = [pr for pr in me["primitives"] if J["accessors"][pr["indices"]]["count"] > 0]
    if len(me["primitives"]) < once: log("bos primitive atildi:", me.get("name", mi), once - len(me["primitives"]))
    if not me["primitives"]: bosm.append(mi)
if bosm:
    mm = {}; yM = []
    for i, m in enumerate(J["meshes"]):
        if i in bosm: continue
        mm[i] = len(yM); yM.append(m)
    for n in J["nodes"]:
        if "mesh" in n:
            if n["mesh"] in bosm: log("bos mesh -> dugumden kalkti:", n.get("name")); n.pop("mesh")
            else: n["mesh"] = mm[n["mesh"]]
    J["meshes"] = yM

while len(BIN) % 4: BIN += b"\0"
J["buffers"][0]["byteLength"] = len(BIN)
jb = json.dumps(J, separators=(",", ":"), ensure_ascii=False).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
open(go.replace(".glb", "_log.txt"), "w", encoding="utf-8").write("\n".join(LOG)); log("yazildi", go)
