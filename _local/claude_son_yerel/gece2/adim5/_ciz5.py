# -*- coding: utf-8 -*-
"""test görselleştirici (matplotlib) — parça listesini tek PNG'ye; kesit kenarlarını 2B PNG'ye"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

RENK = {"sac": (0.78, 0.80, 0.83), "baglanti": (0.25, 0.30, 0.40), "kaynak": (0.9, 0.5, 0.1), "ayak": (0.5, 0.5, 0.55)}


def ciz(parcalar, yol, elev=25, azim=-60, tol=0.3, boyut=(10, 9), baslik="", sinir=None):
    fig = plt.figure(figsize=boyut, dpi=110); ax = fig.add_subplot(111, projection="3d")
    tum = []
    isik = np.array([0.4, 0.8, 0.45]); isik /= np.linalg.norm(isik)
    for p in parcalar:
        sh = p["sh"] if p.get("sh") is not None else p["wp"].val()
        vs, tr = sh.tessellate(tol, 0.4)
        P = np.array([[v.x, -v.z, v.y] for v in vs]); T = np.array(tr)   # sağ el: (x, −z, y) — aynalı görüntü olmasın
        if not len(T): continue
        tri = P[T]
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
        sh_ = 0.35 + 0.65 * np.abs(n @ np.array([isik[0], -isik[2], isik[1]]))
        c = np.array(RENK.get(p.get("tur", "sac"), RENK["sac"]))
        col = np.clip(c[None, :] * sh_[:, None], 0, 1)
        pc = Poly3DCollection(tri, facecolors=col, edgecolors="none", linewidths=0); ax.add_collection3d(pc)
        tum.append(P)
    A = np.vstack(tum); mn, mx = A.min(0), A.max(0)
    if sinir is not None: mn, mx = np.array(sinir[0], float), np.array(sinir[1], float)
    c = (mn + mx) / 2; r = (mx - mn).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_xlabel("x (hat boyu)"); ax.set_ylabel("−z (arka →)"); ax.set_zlabel("y (yukarı)"); ax.view_init(elev=elev, azim=azim); ax.set_title(baslik)
    fig.tight_layout(); fig.savefig(yol); plt.close(fig)


def ciz_kesit(kenarlar_list, yol, eksenler=(0, 2), baslik="", boyut=(8, 8), sinir=None):
    """kenarlar_list: [(etiket, [(tip, [noktalar])])] · eksenler: çizilecek iki dünya ekseni"""
    fig, ax = plt.subplots(figsize=boyut, dpi=120)
    renkler = plt.cm.tab20(np.linspace(0, 1, max(2, len(kenarlar_list))))
    for (et, kk), rk in zip(kenarlar_list, renkler):
        for tip, pts in kk:
            q = np.array(pts)
            ax.plot(q[:, eksenler[0]], q[:, eksenler[1]], "-", color=rk if tip == "LINE" else "red", lw=0.8 if tip == "LINE" else 1.4)
    ax.set_aspect("equal"); ax.set_title(baslik); ax.grid(True, lw=0.3)
    if sinir: ax.set_xlim(*sinir[0]); ax.set_ylim(*sinir[1])
    fig.tight_layout(); fig.savefig(yol); plt.close(fig)


def ciz_acinim(acn, yol, baslik=""):
    import math
    fig, ax = plt.subplots(figsize=(9, 7), dpi=110)
    def cz(ents, renk):
        for e in ents:
            if e["t"] == "L":
                q = np.array(e["p"]); ax.plot(q[:, 0], q[:, 1], "-", color=renk, lw=0.8)
            elif e["t"] == "A":
                c = np.array(e["c"]); a0 = math.atan2(e["p"][0][1] - c[1], e["p"][0][0] - c[0]); am = math.atan2(e["p"][1][1] - c[1], e["p"][1][0] - c[0])
                a1 = math.atan2(e["p"][2][1] - c[1], e["p"][2][0] - c[0])
                d1 = (a1 - a0) % (2 * math.pi); dm = (am - a0) % (2 * math.pi)
                if dm > d1: d1 = d1 - 2 * math.pi
                aa = a0 + np.linspace(0, d1, 20); ax.plot(c[0] + e["r"] * np.cos(aa), c[1] + e["r"] * np.sin(aa), "-", color=renk, lw=0.8)
            else:
                aa = np.linspace(0, 2 * math.pi, 40); ax.plot(e["c"][0] + e["r"] * np.cos(aa), e["c"][1] + e["r"] * np.sin(aa), "-", color=renk, lw=0.8)
    dk = acn["dis_kontur"]
    cz(dk if not (dk and isinstance(dk[0], list)) else [x for k in dk for x in k], "k")
    for k in acn["ic_konturlar"]: cz(k, "b")
    for b in acn["bukumler"]:
        q = np.array(b["cizgi"]); ax.plot(q[:, 0], q[:, 1], "--", color="r" if b["yon"] == "yukari" else "g", lw=0.7)
    ax.set_aspect("equal"); ax.set_title(baslik); ax.grid(True, lw=0.3)
    fig.tight_layout(); fig.savefig(yol); plt.close(fig)
