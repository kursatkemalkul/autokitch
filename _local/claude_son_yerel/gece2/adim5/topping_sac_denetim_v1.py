# -*- coding: utf-8 -*-
"""TOPPING üretim sacı (h3_topping_sac_v1) bağımsız denetim + çıktılar → bu klasör (TOPPING_sac_v1.glb, TOPPING_parca.csv, TOPPING_rapor.json, acinim_TOPPING/, TOPPING_*.jpg)
A/B ile aynı denetim (sac_denetim_ortak.calistir) · v8zq'da yerine geçilen bileşenler düğüm + bileşen no ile çıkarılır (TOPPING_MODUL düğümleri karışık)"""
import os, sys, re, pickle as _pk
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_denetim_ortak as O
import h3_topping_sac_v1 as M


def degisen(b):
    d = M.DEGISEN.get(b["ad"])
    return d == "hepsi" or (d is not None and b["no"] in d)


class _P:
    @staticmethod
    def load(f): return [b for b in _pk.load(f) if not degisen(b)]


O.pickle = _P
HARIC = r"^$^"


def ankraj(ad, b):
    return b.ymin <= 788.05


def pu_mu(ad):
    return ad.startswith("pu_")


def gorunum(ad, gizle=False):
    if gizle: return ad.startswith(("dis_yan_sol", "dis_tavan", "on_cerceve", "dis_arka")) or pu_mu(ad)
    if pu_mu(ad): return None
    for on, d in (("dis_yan_sol", (-600, 0, 0)), ("dis_yan_sag", (600, 0, 0)), ("dis_tavan", (0, 600, 0)), ("dis_arka", (0, 0, -700)), ("dis_taban", (0, -250, 0)),
                  ("on_cerceve", (0, 0, 600)), ("kaide", (0, -550, 0)), ("astar_tavan", (0, 300, 0)), ("soguk_arka", (0, 0, -350)), ("teknik_on", (0, 0, 250))):
        if ad.startswith(on): return d
    return (0, 0, 0)


if __name__ == "__main__":
    O.calistir(M, "TOPPING", HARIC, ankraj, pu_grubu=pu_mu, gorunum=gorunum)
    sys.stdout.flush(); os._exit(0)
