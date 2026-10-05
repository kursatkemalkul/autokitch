# -*- coding: utf-8 -*-
"""MADDE 8 · adim 4 · deliksiz kablo gecisleri: kanal saclarinda kablo agzi (parmak yuvasi / buson yeri). python m8_fix_4_delik.py giris.glb cikis.glb"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m8kit import Glb, delik_ucgenler
g = Glb(sys.argv[1]); LOG = []
def log(*a): LOG.append(" ".join(str(x) for x in a)); print(*a)
QR4 = g.bul_nokta("ELK_QR_KABLO__kanal", (4995, 300, 1040))
ANA = g.bul_nokta("ELK_ANA_HAT__paslanmaz", (3000, 1290, -700))
log("QR alt dikey kanal", QR4["lo"].round(1), QR4["hi"].round(1), "ana besleme", ANA["lo"].round(1), ANA["hi"].round(1))
# QR alt dikey kanal yan saci: ROBOT guc 3G2,5 + ROBOT Cat6A girisi (x 4983) -> tek 29 x 15 kablo agzi (kenar korumali)
log("QR4", g.donustur(QR4, lambda P: delik_ucgenler(P, 0, [4983.0, 4984.5], 286.0, 315.0, 1038.0, 1053.0)))
# TOPPING valf adasi kablosu ana besleme kolunun uc kapagina (x 2421) giriyordu -> uc kapakta O14 agiz (rakor yeri)
log("ANA", g.donustur(ANA, lambda P: delik_ucgenler(P, 0, [2421.0, 2422.5], 1289.0, 1301.0, -814.0, -802.0)))
g.kaydet(sys.argv[2]); log("kaydedildi", sys.argv[2])
open(os.path.splitext(sys.argv[2])[0] + "_log.txt", "w", encoding="utf-8").write("\n".join(LOG))
