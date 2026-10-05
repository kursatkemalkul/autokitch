# -*- coding: utf-8 -*-
"""TC v31 hızlı denetim: yeni kaset parçaları ↔ C istasyonunun bütün parçaları (dünya) · temas mesafeleri · havada kaba bakış"""
import sys, time, importlib.util as ilu, os
import cadquery as cq
t0 = time.time()
import topping_cad_v31 as TC
TC.PARCALAR[:] = []; TC.modul()
sp = ilu.spec_from_file_location("TU19", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v19.py")); TU = ilu.module_from_spec(sp); sp.loader.exec_module(TU)
W_ = TC.dunya_parcalari(TU)
print("dunya %d parca · %.0f s" % (len(W_), time.time() - t0), flush=True)
YENI = ("TC:evap_kaseti_", "TC:sogutma_emis", "TC:sogutma_sivi", "TC:yogusma_tavasi", "TC:sicak_gaz", "TC:kuru_bolme_tabani", "TU:arka_")
B = {a: s.BoundingBox() for a, s in W_}
yeni = [(a, s) for a, s in W_ if a.startswith(YENI)]
bul = []
for a, s in yeni:
    for c, sc in W_:
        if c == a: continue
        if c.startswith(YENI) and c < a: continue
        if not TC._bbk(B[a], B[c]): continue
        v = TC._hacim(s, sc)
        if v > 1.0 or v < 0: bul.append((round(v, 1), a, c))
print("CAKISMA (yeni parca ile): %d" % len(bul))
for x in sorted(bul, reverse=True)[:40]: print("   ", x)
from OCP.BRepExtrema import BRepExtrema_DistShapeShape as DSS
S = dict(W_)
def mes(a, b):
    d = DSS(S[a].wrapped, S[b].wrapped); return d.Value() if d.IsDone() else 99.0
for a, b in (("TC:evap_kaseti_isi_kesici_cerceve", "TU:soguk_arka_dis_sac"), ("TC:evap_kaseti_isi_kesici_cerceve", "TU:arka_duvar_kaset_yuzu"), ("TC:evap_kaseti_askisi_0", "TU:soguk_arka_dis_sac"),
             ("TC:evap_kaseti_askisi_1", "TU:soguk_arka_dis_sac"), ("TC:evap_kaseti_askisi_0", "TC:evap_kaseti_dis_sac"), ("TC:sogutma_emis_hatti", "TC:sogutma_grubu_KLF66"),
             ("TC:sogutma_emis_hatti", "TC:evap_kaseti_hat_gecis_blogu"), ("TC:sogutma_sivi_hatti_ic", "TC:evap_kaseti_kollektor_TXV_zarfi"), ("TC:evap_kaseti_tahliye_hortumu", "TC:evap_kaseti_damlama_tavasi"),
             ("TC:yogusma_tavasi_sicak_gazli", "TC:dis_taban"), ("TC:sicak_gaz_dongusu", "TC:sogutma_grubu_KLF66"), ("TC:evap_kaseti_fani_0", "TC:evap_kaseti_fan_plakasi"),
             ("TC:evap_kaseti_lamel_paketi", "TC:evap_kaseti_damlama_tavasi"), ("TC:evap_kaseti_lamel_paketi", "TC:evap_kaseti_ara_saci"), ("TC:evap_kaseti_kollektor_TXV_zarfi", "TC:evap_kaseti_kollektor_ayirma_saci")):
    print("   temas %-45s ↔ %-40s %.3f" % (a, b, mes(a, b)))
print("SURE %.0f s" % (time.time() - t0))
sys.stdout.flush(); os._exit(0)
