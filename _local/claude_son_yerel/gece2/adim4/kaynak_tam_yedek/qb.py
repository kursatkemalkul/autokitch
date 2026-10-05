import sys, json, io, re
K = json.load(io.open("h3/_dunya/kutular.json", encoding="utf-8"))
a = sys.argv[1:]
if len(a) >= 6:
    q = list(map(float, a[:6])); pat = a[6] if len(a) > 6 else "."
    for ad, g, b in K:
        if all(q[2*i] < b[2*i+1] and b[2*i] < q[2*i+1] for i in range(3)) and re.search(pat, ad):
            print("%-58s %-8s x %7.1f %7.1f  y %7.1f %7.1f  z %7.1f %7.1f" % (ad, g, *b))
else:
    for ad, g, b in K:
        if re.search(a[0], ad): print("%-58s %-8s x %7.1f %7.1f  y %7.1f %7.1f  z %7.1f %7.1f" % (ad, g, *b))
