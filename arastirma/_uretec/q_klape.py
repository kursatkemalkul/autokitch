# -*- coding: utf-8 -*-
import os, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
sw.CloseAllDocuments(True)
def bb_of(yol):
    e=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
    d=sw.OpenDoc6(yol,2 if yol.lower().endswith(".sldasm") else 1,1,"",e,w)
    o=[]
    def gez(c):
        ch=list(c.GetChildren)
        if ch:
            for k in ch: gez(k)
        else: o.append(c)
    if yol.lower().endswith(".sldasm"):
        gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
        for c in o:
            b=c.GetBox(False,False)
            if b: print("   %-38s %6.1f x %6.1f x %6.1f   @ x%7.1f y%7.1f z%7.1f" % (
                c.Name2.rsplit('-',1)[0].split('/')[-1],(b[3]-b[0])*1000,(b[4]-b[1])*1000,(b[5]-b[2])*1000,b[0]*1000,b[1]*1000,b[2]*1000))
        bb=[1e9]*3+[-1e9]*3
        for c in o:
            b=c.GetBox(False,False)
            if b:
                for i in range(3): bb[i]=min(bb[i],b[i]); bb[i+3]=max(bb[i+3],b[i+3])
    else: bb=bbox_of(d)
    print("   TOPLAM  %.1f x %.1f x %.1f  (x %.1f..%.1f  y %.1f..%.1f  z %.1f..%.1f)" % (
        (bb[3]-bb[0])*1000,(bb[4]-bb[1])*1000,(bb[5]-bb[2])*1000,bb[0]*1000,bb[3]*1000,bb[1]*1000,bb[4]*1000,bb[2]*1000,bb[5]*1000))
    sw.CloseDoc(d.GetTitle)
for g in ("KLAPE_MOTOR_GRUBU","SENSOR_REED_D12","ROBOT_UCU_CATAL","TEPSI_D320"):
    print("=== %s ===" % g); bb_of(os.path.join(ARA,"_ortak",g,g+".SLDASM"))
print("=== TEPSI_PIDE_D320 (TOPPING alt montaj) ===")
bb_of(os.path.join(ARA,"3_TOPPING","alt_montaj","TEPSI_PIDE_D320","TEPSI_PIDE_D320.SLDASM"))
try: sw.ExitApp()
except Exception: pass
