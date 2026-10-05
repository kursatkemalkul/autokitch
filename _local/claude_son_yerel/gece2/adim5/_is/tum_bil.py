# bölgedeki bütün bileşenler → pickle (ad, no, lo, hi, kapali, P) — denetimler için tek önbellek
import sys, os, pickle, time, numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
sys.path.insert(0, S)
import govde_denetim_dogru as GD
D = pickle.load(open(os.path.join(S, "gece2/adim5/_is/bolge_tri.pkl"), "rb"))
t = time.time(); out = []
for nd, P in sorted(D.items()):
    if nd.startswith("URUN"): continue
    for b in GD.bilesenler(nd, P):
        out.append(dict(ad=nd, no=b.no, lo=b.lo, hi=b.hi, kapali=b.kapali, P=b.P))
print(len(out), "bileşen", time.time() - t)
pickle.dump(out, open(os.path.join(S, "gece2/adim5/_is/bil_hepsi.pkl"), "wb"))
