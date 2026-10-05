import sys, json, numpy as np
sys.path.insert(0, r"@@KOK_W@@\gece\m8")
import m8_temas as T
J = json.load(open("m8_parca.json")); P = J["parca"]
AD = ("CEK_K6_tatli_1__on_seffaf__CEKMECE", "CEK_K6_ic1_1__on_seffaf__CEKMECE", "CEK_K6_ic1_2__on_seffaf__CEKMECE", "B_SOGUTMA__sac",
      "B_SOGUTMA__celik", "B_DEPO__sac__CEKMECE", "B_DEPO__pu__CEKMECE", "K_GOVDE__on_seffaf")
sec = [i for i, p in enumerate(P) if p["ad"] in AD and p["hi"][0] > 3390 and p["lo"][0] < 4410 and p["hi"][2] > 20 and p["lo"][1] < 2200]
pts, pid = T.kenar_ornek(sec, adim=2.0)
R = T.temas(pts, pid)
der = {}
for a, b in zip(pid[R[:, 0]], T.TPc[R[:, 1]]): der.setdefault(int(a), set()).add(int(b))
yok = [i for i in sec if i not in der]
print(len(sec), "degisen parca ·", "temassiz (havada):", len(yok))
for i in yok: print("  HAVADA", i, P[i]["ad"], P[i]["lo"], P[i]["hi"])
