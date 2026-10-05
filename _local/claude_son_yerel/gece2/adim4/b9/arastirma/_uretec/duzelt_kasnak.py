# -*- coding: utf-8 -*-
# MOTOR_TAHRIK_GRUBU: kasnak ekseni Z idi (yuzu one bakiyordu) -> X olmali.
# Kayis (KAYIS_GT3_6x3x650) z -690..-40 boyunca, genisligi X, kalinligi Y.
# Boyle bir kayisi ancak ekseni X olan bir kasnak dondurebilir.
import os
from sw_lib import *
ORTAK = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_ortak"
sw.CloseAllDocuments(True)
ad = "MOTOR_TAHRIK_GRUBU"; st = Station(os.path.join(ORTAK, ad), ad); p = "MTG_"
for f in os.listdir(st.pdir):
    if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
st.part(p+"kasnak_D30_kayis", [(RT, 'circ', (0.0, 0.0, 15.0), -6.0, 6.0, False)])   # EKSEN X
st.box(p+"reduktor_govde_37x37x40", 8, 48, -18.5, 18.5, -18, 18)
st.box(p+"motor_24V_37x37x80", 48, 128, -18.5, 18.5, -18, 18)
st.box(p+"enkoder_kapagi", 128, 143, -15, 15, -15, 15)
st.box(p+"M12_soket", 143, 158, -8, 8, -8, 8)
st.box(p+"montaj_braketi_3mm", 0, 60, -25, -18.5, -18, 18)
st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])
st.exit_sw()
