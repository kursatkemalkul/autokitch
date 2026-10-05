# -*- coding: utf-8 -*-
"""m7 doğrulama çizimi: bölgedeki üçgenlerin izdüşümü (ön görünüş x-y, plan x-z). python m7_ciz.py model.glb cikti.png gorunus kutu [dugum_suzgec]
gorunus: on (x-y) | plan (x-z) | yan (z-y) · kutu: x0,x1,y0,y1,z0,z1 (yalnız tamamen kutudaki üçgenler)"""
import sys, numpy as np
sys.path.insert(0, ".")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from glbkit import Glb

gi, out, gor, kut = sys.argv[1], sys.argv[2], sys.argv[3], list(map(float, sys.argv[4].split(",")))
suz = sys.argv[5].split(",") if len(sys.argv) > 5 else None
G = Glb(gi)
ax_ = {"on": (0, 1), "plan": (0, 2), "yan": (2, 1)}[gor]
fig, ax = plt.subplots(figsize=(16, 11), dpi=110)
RENK = {"pu": "#f3e3a0", "sac": "#9aa3ad", "paslanmaz": "#c9d1d9", "cam": "#a8d8ff", "hortum": "#ffffff", "pom": "#e8e8e8", "motor": "#555",
        "kablo": "#222", "celik": "#8a96a3", "silikon": "#d77", "conta": "#d55", "aluminyum": "#aab", "kanal": "#666"}
for p in G.prims:
    nm = p["name"]
    if suz and not any(s in nm for s in suz): continue
    if len(p["T"]) == 0: continue
    C = p["X"][p["T"][G.gorunur(p)]]
    if not len(C): continue
    m = ((C[:, :, 0] >= kut[0]) & (C[:, :, 0] <= kut[1]) & (C[:, :, 1] >= kut[2]) & (C[:, :, 1] <= kut[3]) & (C[:, :, 2] >= kut[4]) & (C[:, :, 2] <= kut[5])).all(1)
    if not m.any(): continue
    Q = C[m][:, :, list(ax_)]
    renk = "#bbb"
    for k, v in RENK.items():
        if k in nm.lower(): renk = v
    if nm.startswith("A_"): renk = "#7fb07f"
    ax.add_collection(PolyCollection(Q, facecolors=renk, edgecolors="#00000022", linewidths=0.15, alpha=0.35))
ax.set_xlim(kut[ax_[0] * 2], kut[ax_[0] * 2 + 1]); ax.set_ylim(kut[ax_[1] * 2], kut[ax_[1] * 2 + 1])
ax.set_aspect("equal"); ax.grid(True, lw=0.3)
ax.set_xticks(np.arange(np.ceil(kut[ax_[0] * 2] / 50) * 50, kut[ax_[0] * 2 + 1], 50)); ax.tick_params(labelsize=6)
plt.xticks(rotation=90)
ax.set_title("%s · %s · %s" % (gi.split("/")[-1], gor, kut))
plt.tight_layout(); plt.savefig(out); print("ok", out)
