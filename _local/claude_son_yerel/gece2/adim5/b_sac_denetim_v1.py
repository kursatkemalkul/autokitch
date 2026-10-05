# -*- coding: utf-8 -*-
"""B üretim sacı (h3_b_sac_v1) bağımsız denetim + çıktılar → bu klasör (B_sac_v1.glb, B_parca.csv, B_rapor.json, acinim_B/, B_*.jpg)"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_denetim_ortak as O
import h3_b_sac_v1 as M

HARIC = r"^B_KASA__(sac|pu|on_cerceve|koyu)$"


def ankraj(ad, b):
    return b.ymin <= 123.05


def pu_mu(ad):
    return ad.startswith("pu_") or re.search(r"(^|_)pu(_\d+)?$", ad) is not None


def gorunum(ad, gizle=False):
    if gizle: return ad.startswith(("dis_sol_yan", "dis_tavan", "on_cerceve")) or pu_mu(ad)
    if pu_mu(ad): return None
    for on, d in (("dis_sol_yan", (-700, 0, 0)), ("dis_sag_yan", (700, 0, 0)), ("dis_tavan", (0, 700, 0)), ("dis_taban", (0, -500, 0)), ("dis_arka", (0, 0, -900)),
                  ("on_cerceve", (0, 0, 900)), ("isi_kalkani_isinim", (0, 450, 0)), ("isi_kalkani", (0, 300, 0)), ("ic_tavan", (0, 250, 0))):
        if ad.startswith(on): return d
    return (0, 0, 0)


if __name__ == "__main__":
    O.calistir(M, "B", HARIC, ankraj, pu_grubu=pu_mu, gorunum=gorunum)
    sys.stdout.flush(); os._exit(0)
