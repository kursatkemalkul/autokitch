import os, sys, numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
K = S + r"\gece2\b4\52a"; sys.path[:0] = [K + r"\gece", K]; os.environ["YAMA_IS_KOK"] = K
from m8kit import Glb
g = Glb(K + r"\hat3_v9t.glb")
for d in ["TOPPING_GOVDE__sac", "TOPPING_GOVDE__conta", "TOPPING_GOVDE__paslanmaz", "TOPPING_GOVDE__pom", "TOPPING_GOVDE__cerceve"]:
    for p in g.dprims(d):
        P = p["X"][p["T"]]; c = P.mean(1)
        m = (P[:, :, 0].max(1) > 1532) & (P[:, :, 0].min(1) < 2131) & (P[:, :, 2].max(1) > -560) & (P[:, :, 2].min(1) < -120) & (P[:, :, 1].max(1) > 2099)
        if m.any(): print(d, "min y above hoppers", P[m][:, :, 1].min().round(2))
