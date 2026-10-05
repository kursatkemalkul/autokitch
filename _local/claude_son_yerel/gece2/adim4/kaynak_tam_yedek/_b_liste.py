import glb_oku, numpy as np, json
J, D = glb_oku.yukle("hat3_v8l.glb")
for n in J["nodes"]:
    nm = n.get("name","")
    if "mesh" not in n: continue
    if nm.startswith(("B_",)) or nm.startswith("CEK_K1_lahm_1"):
        X,T = D[nm]
        P = X[np.unique(T)] if len(T) else X
        pr = J["meshes"][n["mesh"]]["primitives"]
        ex=[p.get("extras") for p in pr]
        m=J["materials"][pr[0]["material"]]
        print(nm, len(T), np.round(P.min(0),1), np.round(P.max(0),1), len(pr), json.dumps(ex)[:200], m.get("name"), m.get("alphaMode"))
print(J["scenes"][0].get("extras",{}).keys())
