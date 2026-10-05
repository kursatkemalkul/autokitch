import sys, os, pickle, re, numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
sys.path.insert(0, S)
import govde_denetim_dogru as GD
D = pickle.load(open(os.path.join(S, "gece2/adim5/_is/bolge_tri.pkl"), "rb"))
lo = np.array(list(map(float, sys.argv[1].split(",")))); hi = np.array(list(map(float, sys.argv[2].split(","))))
haric = re.compile(sys.argv[3]) if len(sys.argv) > 3 else None
for nd, P in sorted(D.items()):
    if haric and haric.search(nd): continue
    m = ((P.max(1) >= lo) & (P.min(1) <= hi)).all(1)
    if not m.any(): continue
    B = GD.bilesenler(nd, P)
    for b in B:
        if (b.hi > lo).all() and (b.lo < hi).all():
            print("%-40s %3d lo %s hi %s %s" % (nd, b.no, np.round(b.lo, 1).tolist(), np.round(b.hi, 1).tolist(), "" if b.kapali else "ACIK"))
