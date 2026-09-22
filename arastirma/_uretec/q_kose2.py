# -*- coding: utf-8 -*-
# kat1 robot agzinin SOL ALT kosesine yakin cekim
import os, time, pythoncom
from sw_lib import *
R = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING"
sw.CloseAllDocuments(True)
e=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
d = sw.OpenDoc6(os.path.join(R,"TOPPING.SLDASM"), 2, 0, "", e, w); mcall(d,"EditRebuild3")
f = mcall(d,"FirstFeature"); dl=[]
while f is not None:
    if mcall(f,"GetTypeName2")=="RefPlane": dl.append(f)
    f = mcall(f,"GetNextFeature")
d.ClearSelection2(True)
for x in dl: x.Select2(True,0)
try: mcall(d,"BlankRefGeom")
except Exception: pass
d.ClearSelection2(True)
def kare(ad, view, kutu):
    d.ShowNamedView2(view, 7 if view=="*Isometric" else 1)
    try: mcall(d, "ViewZoomTo2", *kutu)
    except Exception as ex: print("zoom hata", ex); mcall(d,"ViewZoomtofit2")
    time.sleep(1.5); yol = os.path.join(R, ad); d.SaveBMP(yol, 1600, 1100)
    from PIL import Image; Image.open(yol).save(yol); print("  ", ad)
# sol alt kose (kat1 agzi y 1572..1689) — izometrik yakin
kare("AGIZ_kose_sol_iso.png", "*Isometric", (-0.03, 1.53, -0.06, 0.20, 1.72, 0.06))
kare("AGIZ_on.png", "*Front", (-0.02, 1.52, -0.10, 0.72, 1.75, 0.06))
sw.Visible = True
