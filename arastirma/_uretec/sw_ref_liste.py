# -*- coding: utf-8 -*-
import os
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
for rel in ("1_STORE/STORE.SLDASM", "3_TOPPING/TOPPING.SLDASM", "FULL_MAKINE/HAT.SLDASM"):
    yol = os.path.join(ARA, rel)
    dep = mcall(sw, "GetDocumentDependencies2", yol, True, True, False)
    yok = []
    if dep:
        for i in range(0, len(dep), 2):
            p = dep[i+1]
            if p and not os.path.exists(p): yok.append((dep[i], p))
    print("%-22s referans=%d  EKSIK=%d" % (os.path.basename(yol), (len(dep)//2 if dep else 0), len(yok)))
    for n, p in yok[:20]: print("    EKSIK ->", p)
