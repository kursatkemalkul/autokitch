import sys, os, pickle, time, re, numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
sys.path.insert(0, S)
import govde_denetim_dogru as GD
D = pickle.load(open(os.path.join(S, "gece2/adim5/_is/bolge_tri.pkl"), "rb"))
pat = re.compile(sys.argv[1])
for nd, P in sorted(D.items()):
    if not pat.search(nd): continue
    B = GD.bilesenler(nd, P)
    print("==", nd, len(B), "bileşen")
    for b in sorted(B, key=lambda b: (round(b.lo[1]), round(b.lo[0]))):
        print("   %s lo %s hi %s %s" % (b.no, np.round(b.lo, 1).tolist(), np.round(b.hi, 1).tolist(), "" if b.kapali else "ACIK"))
