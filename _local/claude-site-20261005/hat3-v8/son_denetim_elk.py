import sys, os
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import h3_elektrik_v1 as EL, h3_elk_ortak as EO, h3_duzeltme_v1 as DZM
EL.yukle()
bul = []
for p in EL.PARCALAR:
    for ad, v in EO.cakisma(EL.dunya(p)):
        bul.append((round(v, 1), p["ad"], ad))
DZM.kur()
for p in DZM.PARCALAR:
    for ad, v in EO.cakisma(DZM.dunya(p)):
        bul.append((round(v, 1), "DUZ:" + p["ad"], ad))
for x in sorted(bul, reverse=True)[:40]: print("  ÇAKIŞMA %8.1f mm³  %-42s ↔ %s" % x)
print("SON DENETİM (elektrik + düzeltme ↔ delikleri açılmış makine, istisnasız): %d çakışma" % len(bul))
sys.stdout.flush(); os._exit(0)
