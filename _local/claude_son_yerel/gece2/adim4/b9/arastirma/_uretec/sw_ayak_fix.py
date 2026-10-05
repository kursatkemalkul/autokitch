import os, sys
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
sw.CloseAllDocuments(True)
for folder, name, W in (("1_STORE", "STORE", 1400.0), ("2_PRESS", "PRESS", 700.0)):
    st = Station(os.path.join(ARA, folder), name); p = name + "_"
    for i, (ax, az) in enumerate([(60, ZK+140), (W-140, ZK+140)], 3): st.box(p+"ayak_%d" % i, ax, ax+80, 0, Y0, az-80, az)
    print(name, "arka ayaklar yenilendi")
Station(ARA, "x").exit_sw()
