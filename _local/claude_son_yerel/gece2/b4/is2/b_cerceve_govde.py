# B dolabı ÖN ÇERÇEVE SACI (430, çekmece açıklıklı · sabit, gövde) yanlışlıkla "ön kapak" malzemesindeydi (on_seffaf) → kapaklarla saydamlaşıyor / gizleniyordu.
# Gövde malzemesine alınır (opak 430 sac), kapak etiketi kalkar. Kullanım: python b_cerceve_govde.py giris.glb cikis.glb
import json, struct, sys
gi, go = sys.argv[1:3]
raw = open(gi, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]
for n in J["nodes"]:
    if n.get("name") == "B_KASA__on_seffaf":
        n["name"] = "B_KASA__on_cerceve"
        for p in J["meshes"][n["mesh"]]["primitives"]:
            m = J["materials"][p["material"]]; m["name"] = "MB_B_KASA__on_cerceve"
            m["pbrMetallicRoughness"] = {"baseColorFactor": [0.74, 0.77, 0.80, 1.0], "metallicFactor": 0.85, "roughnessFactor": 0.32}
            m.pop("alphaMode", None); m["doubleSided"] = True
            p.setdefault("extras", {})["kpk"] = []
        print("B ön çerçeve sacı → gövde (opak, kapak değil)")
jb = json.dumps(J, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb + struct.pack("<II", len(BIN), 0x004E4942) + BIN)
