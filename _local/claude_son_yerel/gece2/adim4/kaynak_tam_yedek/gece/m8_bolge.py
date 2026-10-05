# python m8_bolge.py x0 x1 y0 y1 z0 z1 [desen]  -> v8x meta (ad) ile bolgedeki bilesenler
import sys, json, re
M = json.load(open(r"@@KOK_W@@\gece\m8\cak8a\meta.json", encoding="utf-8"))["bil"]
k = [float(v) for v in sys.argv[1:7]]; des = sys.argv[7] if len(sys.argv) > 7 else ""
for b in M:
    if all(b["lo"][i] <= k[2 * i + 1] and b["hi"][i] >= k[2 * i] for i in range(3)) and re.search(des, b["dugum"] + " " + str(b["ad"])):
        print("%-34s %4d %-48s %s %s kat=%s" % (b["dugum"], b["no"], b["ad"], b["lo"], b["hi"], b["kat"]))
