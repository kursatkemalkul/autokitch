# -*- coding: utf-8 -*-
"""F üretim sacı (h3_f_sac_v1) bağımsız denetim + çıktılar → bu klasör (TOPPING_sac_v1.glb, TOPPING_parca.csv, TOPPING_rapor.json, acinim_TOPPING/, TOPPING_*.jpg)
A/B ile aynı denetim (sac_denetim_ortak.calistir) · v8zq'da yerine geçilen bileşenler düğüm + bileşen no ile çıkarılır (TOPPING_MODUL düğümleri karışık)"""
import os, sys, re, pickle as _pk
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_denetim_ortak as O
import h3_f_sac_v1 as M


def degisen(b):
    d = M.DEGISEN.get(b["ad"])
    return d == "hepsi" or (d is not None and b["no"] in d)


class _P:
    @staticmethod
    def load(f): return [b for b in _pk.load(f) if not degisen(b)]


O.pickle = _P
HARIC = r"^$^"


def ankraj(ad, b):
    return ad.startswith(("onyuz_kapak_F_sol_dis_tava", "onyuz_kapak_F_sag_dis_tava", "davlumbaz_atis_kanali_L", "baca_dis_kilif_L", "baca_alt_kapama"))


def pu_mu(ad):
    return ad.startswith("yalitim_")


def gorunum(ad, gizle=False):
    if gizle: return ad.startswith(("onyuz_kapak", "baca_dis_kilif")) or pu_mu(ad)
    if pu_mu(ad): return None
    for on, d in (("onyuz_kapak_F_sol_dis", (0, 0, 500)), ("onyuz_kapak_F_sag_dis", (0, 0, 500)), ("onyuz_kapak", (0, 0, 250)), ("baca_ust", (0, 400, 0)),
                  ("baca_dis", (0, 0, -300)), ("baca_ic", (0, 200, 0)), ("davlumbaz", (0, -150, 0))):
        if ad.startswith(on): return d
    return (0, 0, 0)


if __name__ == "__main__":
    O.calistir(M, "F", HARIC, ankraj, pu_grubu=pu_mu, gorunum=gorunum)
    sys.stdout.flush(); os._exit(0)
