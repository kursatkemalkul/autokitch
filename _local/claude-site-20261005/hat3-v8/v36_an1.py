import json, io, re, sys
from collections import Counter
L = json.load(io.open(sys.argv[1], encoding="utf-8"))
c = Counter(b for b, a, m, g, bb in L)
print("BIRIMLER:", dict(c))
print("--- ETEK adaylari")
for b, a, m, g, bb in L:
    if re.search(r"plint|etek|supurge|süpürge|skirt|kick|alt_bant|altbant|toe", a, re.I):
        print(b, a, m, g, bb)
print("--- ZEMIN")
for b, a, m, g, bb in L:
    if re.search(r"zemin|doseme|döşeme|karo|floor", b + a, re.I) and not b.startswith("ELK_"):
        print(b, a, m, g, bb)
