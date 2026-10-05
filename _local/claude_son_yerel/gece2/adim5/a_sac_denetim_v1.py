# -*- coding: utf-8 -*-
"""A üretim sacı (h3_a_sac_v1) bağımsız denetim + çıktılar → bu klasör (A_sac_v1.glb, A_parca.csv, A_rapor.json, acinim_A/, A_*.jpg)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_denetim_ortak as O
import h3_a_sac_v1 as M

HARIC = r"^(A_GOVDE|A_ONYUZ|KAIDE_A|A_MODULER|U_A_GOVDE)"


def ankraj(ad, b):
    return b.ymin <= 788.05 and not ad.startswith("onyuz_kapak")


def gorunum(ad, gizle=False):
    if gizle: return ad.startswith(("sol_yan_sac", "ust_sac", "onyuz_kapak"))
    for on, d in (("onyuz_kapak", (0, 0, 650)), ("sol_yan_sac", (-450, 0, 0)), ("sag_yan_sac", (450, 0, 0)), ("ust_sac", (0, 450, 0)), ("arka_sac", (0, 0, -550)),
                  ("kaide_damlama", (0, -120, 0)), ("kaide_ust_plaka", (0, -240, 0)), ("kaide_servis", (0, -120, 0)), ("kaide_", (0, -400, 0))):
        if ad.startswith(on): return d
    if "_bag_" in ad or ad.startswith("govde_bag_arka"):
        if "_sol_" in ad: return (-450, 0, 0)
        if "_sag_" in ad: return (450, 0, 0)
        if "_ust_" in ad: return (0, 450, 0)
    return (0, 0, 0)


if __name__ == "__main__":
    O.calistir(M, "A", HARIC, ankraj, gorunum=gorunum)
    sys.stdout.flush(); os._exit(0)
