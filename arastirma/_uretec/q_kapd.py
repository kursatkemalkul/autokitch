# -*- coding: utf-8 -*-
# KAP_DETAY + SOKET_MOTOR_DETAY gorselleri ve parca sayimi
import os, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ALT = os.path.join(ARA, "3_TOPPING", "alt_montaj"); R = os.path.join(ARA, "3_TOPPING")
sw.CloseAllDocuments(True)
def leafs(c, o):
    ch = list(c.GetChildren)
    if ch:
        for k in ch: leafs(k, o)
    else: o.append(c)
def ac(yol):
    e=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
    d = sw.OpenDoc6(yol, 2, 0, "", e, w); mcall(d,"EditRebuild3")
    f = mcall(d,"FirstFeature"); dl=[]
    while f is not None:
        if mcall(f,"GetTypeName2")=="RefPlane": dl.append(f)
        f = mcall(f,"GetNextFeature")
    d.ClearSelection2(True)
    for x in dl: x.Select2(True,0)
    try: mcall(d,"BlankRefGeom")
    except Exception: pass
    d.ClearSelection2(True); return d
# --- KAP_DETAY
d = ac(os.path.join(ALT,"KAP_DETAY","KAP_DETAY.SLDASM")); o=[]
leafs(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True), o)
adlar = sorted(set(c.Name2.rsplit('-',1)[0] for c in o))
print("=== KAP_DETAY: %d ornek / %d farkli parca ===" % (len(o), len(adlar)))
for a in adlar: print("  ", a)
png(d, os.path.join(R,"KAP_DETAY_iso.png"), "*Isometric")
d.ClearSelection2(True); n=0
for c in o:
    if any(k in c.Name2 for k in ("govde_profil","ust_kapak","kizak_sag","burun_PC")): c.Select4(True,NUL,False); n+=1
if n: mcall(d,"HideComponent")
d.ClearSelection2(True)
png(d, os.path.join(R,"KAP_DETAY_ici_iso.png"), "*Isometric")
sw.CloseDoc(d.GetTitle)
# --- SOKET_MOTOR_DETAY
d = ac(os.path.join(ALT,"SOKET_MOTOR_DETAY","SOKET_MOTOR_DETAY.SLDASM")); o=[]
leafs(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True), o)
adlar = sorted(set(c.Name2.rsplit('-',1)[0] for c in o))
print("=== SOKET_MOTOR_DETAY: %d ornek / %d farkli parca ===" % (len(o), len(adlar)))
for a in adlar: print("  ", a)
png(d, os.path.join(R,"SOKET_MOTOR_DETAY_iso.png"), "*Isometric")
png(d, os.path.join(R,"SOKET_MOTOR_DETAY_yan.png"), "*Right")
sw.CloseDoc(d.GetTitle)
try: sw.ExitApp()
except Exception: pass
