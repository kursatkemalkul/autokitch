# -*- coding: utf-8 -*-
# STORE: dosyasi silinmis (olu) bilesenleri montajdan cikar + kaset kati klapesinin YENI on yuzunu ekle
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); PD = os.path.join(ROOT, "parca")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
YENI = ("STORE_klape_kaset_kati_on_dis_sac_bukme_1.5", "STORE_klape_kaset_kati_on_pu_37.5", "STORE_klape_kaset_kati_on_ic_sac_1.0")
e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
sw.CloseAllDocuments(True)
d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
mcall(d, "EditRebuild3"); time.sleep(2)
comps = list(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
var = set(c.Name2.rsplit("-", 1)[0] for c in comps)
d.ClearSelection2(True); sil = []
for c in comps:
    p = c.GetPathName
    if p and not os.path.exists(p):
        d.Extension.SelectByID2(c.Name2 + "@STORE", "COMPONENT", 0.0, 0.0, 0.0, True, 0, NUL_, 0); sil.append(os.path.basename(p))
if sil: d.Extension.DeleteSelection2(0)
d.ClearSelection2(True)
print("cikarilan olu bilesen: %d" % len(sil))
for s in sil: print("   -", s)
acik = []; n = 0
for ad in YENI:
    if ad in var: print("   zaten var:", ad); continue
    yol = os.path.join(PD, ad + ".SLDPRT")
    dd = sw.OpenDoc6(yol, 1, 1, "", e, w); acik.append(dd.GetTitle); bb = bbox_of(dd)
    c = [(bb[i]+bb[i+3])/2 for i in range(3)]
    if d.AddComponent5(yol, 0, "", False, "", c[0], c[1], c[2]) is not None: n += 1; print("   + eklendi:", ad)
for t_ in acik:
    try: sw.CloseDoc(t_)
    except Exception: pass
comps = list(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
d.ClearSelection2(True)
for c in comps:
    if c.Name2.rsplit("-", 1)[0] in YENI: c.Select4(True, NUL, False)
mcall(d, "FixComponent"); d.ClearSelection2(True)
mcall(d, "EditRebuild3"); time.sleep(2)
for i in range(1, 9):
    p2 = d.Parameter("D1@LimitDistance%d" % i)
    if p2 is not None: p2.SystemValue = 0.0
mcall(d, "EditRebuild3"); time.sleep(1)
e2 = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w2 = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
print("bilesen: %d | kayit: %s" % (d.GetComponentCount(False), bool(d.Save3(1, e2, w2))))
sw.CloseAllDocuments(True)
