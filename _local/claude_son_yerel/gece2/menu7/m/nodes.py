import json, struct, re
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
raw = open(S + r"\gece2\b4\52a\hat3_v9t.glb", "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]
J = json.loads(raw[20:20 + jl])
print("nodes", len(J["nodes"]), "meshes", len(J["meshes"]), "anims", len(J.get("animations", [])), "scene nodes", len(J["scenes"][0]["nodes"]))
for i, nd in enumerate(J["nodes"]):
    n = nd.get("name", "")
    if re.search(r"SOS|HARC|KIYMA|KUSBASI|TOPPING_DONER|PISTON|TOPPING_MODUL__hortum|TOPPING_MODUL__hava", n):
        print(i, n, {k: v for k, v in nd.items() if k not in ("name",)}, len(J["meshes"][nd["mesh"]]["primitives"]) if "mesh" in nd else "")
for a in J.get("animations", [])[:50]:
    tg = [(J["nodes"][c["target"]["node"]]["name"], c["target"]["path"]) for c in a["channels"]]
    if any(re.search("SOS|HARC|KIYMA|KUSBASI", t[0]) for t in tg): print("ANIM", a.get("name"), tg[:6])
print([a.get("name") for a in J.get("animations", [])][:40])
print(json.dumps(J["scenes"][0]["extras"].get("kategoriler"), ensure_ascii=False)[:300])
print([k for k in J.keys()], J.get("extras"))
