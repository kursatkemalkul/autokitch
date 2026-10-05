# -*- coding: utf-8 -*-
"""Bir üreteci ÖNBELLEKLE çalıştırır: python ob_calistir.py <betik.py> [argümanlar] · önbellek modülü betikten önce yüklenir."""
import os, runpy, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadquery  # noqa
import onbellek as OB
betik = sys.argv[1]
sys.argv = sys.argv[1:]
_orj_exit = os._exit


def _cikis(k=0):
    OB.ozet()
    _orj_exit(k)


os._exit = _cikis
try:
    runpy.run_path(betik, run_name="__main__")
finally:
    OB.ozet()
