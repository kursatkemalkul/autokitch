# -*- coding: utf-8 -*-
"""GLB sıkıştır: kullanılmayan accessor / bufferView verisini at (düğüm düzenlemesinden kalan yetim tamponlar). python glb_sikistir.py gir.glb cik.glb"""
import json, struct, sys

gi, go = sys.argv[1:3]
raw = open(gi, "rb").read()
jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]
kul_acc = set()
for m in J.get("meshes", []):
    for p in m["primitives"]:
        kul_acc.update(p["attributes"].values())
        if "indices" in p: kul_acc.add(p["indices"])
        for t in p.get("targets", []): kul_acc.update(t.values())
for a in J.get("animations", []):
    for s in a["samplers"]: kul_acc.update([s["input"], s["output"]])
for s in J.get("skins", []):
    if "inverseBindMatrices" in s: kul_acc.add(s["inverseBindMatrices"])
kul_bv = set(J["accessors"][i]["bufferView"] for i in kul_acc if "bufferView" in J["accessors"][i])
for im in J.get("images", []):
    if "bufferView" in im: kul_bv.add(im["bufferView"])
yeni_bv, bv_map, out = [], {}, bytearray()
for i, v in enumerate(J["bufferViews"]):
    if i not in kul_bv: continue
    while len(out) % 4: out.extend(b"\0")
    o = v.get("byteOffset", 0); d = BIN[o:o + v["byteLength"]]
    nv = dict(v); nv["byteOffset"] = len(out); out.extend(d)
    bv_map[i] = len(yeni_bv); yeni_bv.append(nv)
yeni_acc, acc_map = [], {}
for i, a in enumerate(J["accessors"]):
    if i not in kul_acc: continue
    na = dict(a)
    if "bufferView" in na: na["bufferView"] = bv_map[na["bufferView"]]
    acc_map[i] = len(yeni_acc); yeni_acc.append(na)
for m in J.get("meshes", []):
    for p in m["primitives"]:
        p["attributes"] = {k: acc_map[v] for k, v in p["attributes"].items()}
        if "indices" in p: p["indices"] = acc_map[p["indices"]]
        if "targets" in p: p["targets"] = [{k: acc_map[v] for k, v in t.items()} for t in p["targets"]]
for a in J.get("animations", []):
    for s in a["samplers"]: s["input"] = acc_map[s["input"]]; s["output"] = acc_map[s["output"]]
for s in J.get("skins", []):
    if "inverseBindMatrices" in s: s["inverseBindMatrices"] = acc_map[s["inverseBindMatrices"]]
for im in J.get("images", []):
    if "bufferView" in im: im["bufferView"] = bv_map[im["bufferView"]]
J["accessors"] = yeni_acc; J["bufferViews"] = yeni_bv
while len(out) % 4: out.extend(b"\0")
J["buffers"][0]["byteLength"] = len(out)
jb = json.dumps(J, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(out)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb
                     + struct.pack("<II", len(out), 0x004E4942) + bytes(out))
print("sıkıştırıldı %s: %.1f → %.1f MB · accessor %d · bufferView %d" % (go, len(raw) / 1e6, (len(out) + len(jb)) / 1e6, len(yeni_acc), len(yeni_bv)))
