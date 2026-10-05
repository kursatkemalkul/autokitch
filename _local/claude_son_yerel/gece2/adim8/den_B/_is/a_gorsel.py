import os, sys
D = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\adim5"
sys.path.insert(0, D)
import sac_denetim_ortak as O
import a_sac_denetim_v1 as AD
import h3_a_sac_v1 as M
import _ciz5 as _ciz
G = M.kur(); GW = M.dunya_listesi(M.govde_parcalari())
_ciz.RENK.update({"kapak": (0.62, 0.78, 0.95), "profil": (0.62, 0.66, 0.72), "pu": (0.95, 0.82, 0.25), "conta": (0.2, 0.2, 0.2), "sac": (0.80, 0.82, 0.85)})
O.gorunum_ciz(_ciz, "A", GW, AD.gorunum)
print("ok")
