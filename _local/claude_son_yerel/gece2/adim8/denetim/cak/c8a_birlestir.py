import json, glob
C, I, T, Y, H = [], [], 0, [], []
for f in sorted(glob.glob("parca_*.json")):
    d = json.load(open(f)); C += d["cak"]; I += d["inc"]; T += d["temas"]; Y += d["yavas"]; H += d["hata"]
json.dump(dict(cak=C, inc=I, temas=T, yavas=Y, hata=H), open("birlesik.json", "w"))
print("cakisma", len(C), "incele", len(I), "temas", T, "yavas", len(Y), "hata", len(H))
