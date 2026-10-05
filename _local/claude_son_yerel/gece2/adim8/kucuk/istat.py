# -*- coding: utf-8 -*-
"""GLB ağ istatistiği: python istat.py gir.glb"""
import json, struct, sys, collections
raw = open(sys.argv[1], "rb").read()
jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]
print("dosya", len(raw), "json", jl, "bin", bl)
print("extensionsUsed", J.get("extensionsUsed"), "required", J.get("extensionsRequired"))
acc = J["accessors"]; bvs = J["bufferViews"]
by = collections.Counter(); cnt = collections.Counter(); ntri = 0; nprim = 0; nvert = 0
comp = collections.Counter(); strided = 0
kul_bv = set(); kul_acc = set()
ext_prim = collections.Counter()
for m in J["meshes"]:
    for p in m["primitives"]:
        nprim += 1
        if p.get("mode", 4) != 4: cnt["mode!=4"] += 1
        for k in (p.get("extras") or {}): ext_prim[k] += 1
        for k, a in p["attributes"].items():
            A = acc[a]; kul_acc.add(a)
            bv = bvs[A["bufferView"]]; kul_bv.add(A["bufferView"])
            by[k] += bv["byteLength"]; comp[(k, A["componentType"], A["type"], A.get("normalized", False))] += 1
            if "byteStride" in bv: strided += 1
            if k == "POSITION": nvert += A["count"]
        if "indices" in p:
            A = acc[p["indices"]]; kul_acc.add(p["indices"]); kul_bv.add(A["bufferView"])
            by["indices"] += bvs[A["bufferView"]]["byteLength"]; ntri += A["count"] // 3
            comp[("indices", A["componentType"])] += 1
        else:
            cnt["indeksiz"] += 1
anim = 0
for a in J.get("animations", []):
    for s in a["samplers"]:
        for x in (s["input"], s["output"]):
            kul_acc.add(x); kul_bv.add(acc[x]["bufferView"]); anim += bvs[acc[x]["bufferView"]]["byteLength"]
by["animasyon"] = anim
print("mesh", len(J["meshes"]), "prim", nprim, "node", len(J.get("nodes", [])), "acc", len(acc), "bv", len(bvs), "materials", len(J.get("materials", [])), "images", len(J.get("images", [])))
print("ucgen", ntri, "kose", nvert, "strided bv", strided, cnt)
for k, v in by.most_common(): print("  %-12s %8.1f MB" % (k, v / 1e6))
print("toplam kullanılan bv", sum(bvs[i]["byteLength"] for i in kul_bv) / 1e6, "MB · yetim bv", len(bvs) - len(kul_bv), "yetim acc", len(acc) - len(kul_acc))
for k, v in comp.most_common(): print("  ", k, v)
print("prim extras anahtarları", dict(ext_prim))
ext_mesh = collections.Counter(k for m in J["meshes"] for k in (m.get("extras") or {}))
ext_node = collections.Counter(k for n in J.get("nodes", []) for k in (n.get("extras") or {}))
print("mesh extras", dict(ext_mesh), "node extras", dict(ext_node), "scene extras", [list((s.get("extras") or {}).keys()) for s in J.get("scenes", [])])
