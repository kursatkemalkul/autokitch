import sys, os, pickle, numpy as np, re
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
B = pickle.load(open(os.path.join(S, "gece2/adim5/_is/bil_hepsi.pkl"), "rb"))
lo = np.array(list(map(float, sys.argv[1].split(",")))); hi = np.array(list(map(float, sys.argv[2].split(","))))
h = re.compile(sys.argv[3]) if len(sys.argv) > 3 else None
for b in B:
    if h and h.search(b["ad"]): continue
    if (b["hi"] > lo).all() and (b["lo"] < hi).all():
        print("%-36s %4d %s %s %s" % (b["ad"], b["no"], np.round(b["lo"], 1).tolist(), np.round(b["hi"], 1).tolist(), "" if b["kapali"] else "ACIK"))
