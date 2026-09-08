# -*- coding: utf-8 -*-
# PRESS: çatal lamaları öne taşıyordu → 4 parçayı yeniden üret, montajı klasörden yeniden kur
import os
from sw_lib import *
ROOT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
sw.CloseAllDocuments(True)
st = Station(os.path.join(ROOT, "2_PRESS"), "PRESS"); p = "PRESS_"
for f in ("uc_catal_sirt", "uc_catal_lama_1", "uc_catal_lama_2", "uc_catal_flans_ISO9409"):
    fp = os.path.join(st.pdir, p + f + ".SLDPRT")
    if os.path.exists(fp): os.remove(fp)
st.box(p+"uc_catal_sirt", 280, 420, 1174, 1254, -600, -550); st.box(p+"uc_catal_lama_1", 290, 306, 1176, 1188, -550, -50); st.box(p+"uc_catal_lama_2", 394, 410, 1176, 1188, -550, -50)
st.box(p+"uc_catal_flans_ISO9409", 320, 380, 1254, 1266, -600, -550)
st.load_dir(); st.assemble("PRESS")
