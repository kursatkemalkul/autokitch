# -*- coding: utf-8 -*-
"""MADDE 8 TUR 3 · istenmeyen dar derzler (havada_pu_kapak.md §5). Kural: kalinlik SABIT, yuzeyler ust uste BINMEZ;
yalniz sacin KENARI (kalinlik eksenine dik yon) komsu parcanin kenarina/yuzune alin alina uzatilir.
Analiz: m8t3/gap.py (en yakin nokta + araya giren parca), m8t3/icinde.py (derz ortasini dolduran parca, isin paritesi).
python m8t3_derz.py hat3_v8z.glb cikis.glb"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m8kit import Glb, esle
g = Glb(sys.argv[1]); LOG = []
def log(*a): LOG.append(" ".join(str(x) for x in a)); print(*a)

# 1) F davlumbaz bacası kanalı (F_DAVLUMBAZ__sac, 1,5 mm cidar, dis 2952..3248 x -718..-522) cati sacinin ALT yuzunde (y 1860,5) bitiyordu;
#    cati deligi 2951,5..3248,5 (0,5 mm gecme payi), U_F_BACA (ic 2951,5..3248,5) y 1862'den baslar -> kanal ile baca arasinda 1,5 mm dikey yarik.
#    Kanalin 4 cidarinin ust KENARI 1860,5 -> 1862 (cati sacinin kalinligi kadar, delikten gecer, baca tabanina alin alina). Cidar kalinligi ayni.
b = g.bilesen("F_DAVLUMBAZ__sac", lo=np.array([2952.0, 1361.5, -718.0]), hi=np.array([3248.0, 1860.5, -522.0]), tol=0.3)
n = g.donustur(b, lambda P: esle(P, 1, 1860.5, 1862.0, tol=0.02))
log("1 F_DAVLUMBAZ__sac kanal ust kenari y 1860,5 -> 1862,0 (ucgen %d)" % n)

g.kaydet(sys.argv[2]); log("kaydedildi", sys.argv[2])
open(os.path.splitext(sys.argv[2])[0] + "_log.txt", "w", encoding="utf-8").write("\n".join(LOG))
