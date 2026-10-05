# -*- coding: utf-8 -*-
# Cop bolmesi ic gorunumu: cephe gizlenir, kovanin acik agzi ve huni gorunur
import os, pythoncom
from sw_lib import *
R = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\2_PRESS_v5"
sw.CloseAllDocuments(True)
e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
d = sw.OpenDoc6(os.path.join(R,"PRESS_v5.SLDASM"), 2, 1, "", e, w); mcall(d,"EditRebuild3")
out=[]
def gez(c):
    ch=list(c.GetChildren)
    if ch:
        for k in ch: gez(k)
    else: out.append(c)
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
f = mcall(d,"FirstFeature"); dl=[]
while f is not None:
    if mcall(f,"GetTypeName2")=="RefPlane": dl.append(f)
    f = mcall(f,"GetNextFeature")
d.ClearSelection2(True)
for x in dl: x.Select2(True,0)
try: mcall(d,"BlankRefGeom")
except Exception: pass
# cephe + yan duvar + PRES bolgesini gizle -> yalniz cop/atma bolmesi kalsin
GIZ = ("panel_","sove_","dis_yan_sag","dis_ust","on_cerceve","PZP400","uc_","raf_uc","pano_","plint","ayar_","pres_")
d.ClearSelection2(True); n=0
for c in out:
    if any(k in c.Name2 for k in GIZ): c.Select4(True,NUL,False); n+=1
if n: mcall(d,"HideComponent")
d.ClearSelection2(True)
png(d, os.path.join(R,"PRESS_v5_cop_ic.png"), "*Isometric")
png(d, os.path.join(R,"PRESS_v5_cop_yan.png"), "*Right")
print("gizlenen:",n)
sw.CloseDoc(d.GetTitle)
try: sw.ExitApp()
except Exception: pass
