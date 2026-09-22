# -*- coding: utf-8 -*-
import os, time, pythoncom
from sw_lib import *
ARA=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"; R=os.path.join(ARA,"4_OVEN_v4")
e=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
sw.CloseAllDocuments(True); sw.FrameState=2
d=sw.OpenDoc6(os.path.join(R,"OVEN_v4.SLDASM"),2,1,"",e,w); mcall(d,"EditRebuild3"); time.sleep(2)
png(d, os.path.join(R,"OVEN_v4_iso.png"), "*Isometric", 1100, 1500)
png(d, os.path.join(R,"OVEN_v4_on.png"), "*Front", 900, 1500)
GIZ=("O4_panel_","FK4_","O4_sove_","O4_dis_on","O4_ust_cephe","O4_agiz_cerceve","O4_agiz_cep")
d.ClearSelection2(True); n=[0]
def gez(c):
    for k in (c.GetChildren or []): gez(k)
    if any(g in c.Name2 for g in GIZ): c.Select4(True,NUL,False); n[0]+=1
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
if n[0]: mcall(d,"HideComponent")
d.ClearSelection2(True)
png(d, os.path.join(R,"OVEN_v4_ic_on.png"), "*Front", 900, 1500)
png(d, os.path.join(R,"OVEN_v4_ic_iso.png"), "*Isometric", 1100, 1500)
print("png tamam, gizlenen", n[0]); sw.CloseDoc(d.GetTitle)
try: sw.ExitApp()
except Exception: pass
