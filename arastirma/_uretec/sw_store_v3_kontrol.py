# -*- coding: utf-8 -*-
# STORE v3 — KONTROL LISTESI DOGRULAMA (modelden okur)
import os, time, math, pythoncom, collections
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
R = os.path.join(ARA, "1_STORE_v3"); NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
sw.CloseAllDocuments(True)
e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
d = sw.OpenDoc6(os.path.join(R, "STORE_v3.SLDASM"), 2, 0, "", e, w); sw.Visible = True; sw.FrameState = 2
mcall(d, "EditRebuild3"); time.sleep(3)
kok = d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True)
ust = list(kok.GetChildren)
say = collections.Counter(c.Name2.rsplit("-",1)[0] for c in ust)
hr = [c.Name2 for c in ust if not c.IsFixed]
yap = collections.Counter()
def gez(c):
    for k in c.GetChildren:
        if not list(k.GetChildren): yap["parca"] += 1
        gez(k)
gez(kok)
print("=== ADET ===")
for k in ("CEKMECE3_icecek","CEKMECE3_1L","CEKMECE3_hamur88","CEKMECE3_donmus115","KLAPE3_KASET",
          "RAY_DIS_PROFIL","KAYIS_GT3_6mm","MOTOR_TAHRIK_GRUBU","KABLO_24V_D5","SENSOR_REED_D12",
          "KLAPE_MOTOR_GRUBU","KAP_14x68x24","L_RAF_CIFTI"):
    print("  %-22s %3d" % (k, say.get(k, 0)))
print("  cekmece toplam        %3d" % sum(say.get(k,0) for k in ("CEKMECE3_icecek","CEKMECE3_1L","CEKMECE3_hamur88","CEKMECE3_donmus115")))
print("  hareketli             %3d" % len(hr))
print("  toplam parca          %3d" % yap["parca"])
print("=== OLCU (montaj kutusu) ===")
bb = [1e9]*3 + [-1e9]*3
for c in ust:
    g = c.GetBox(False, False)
    for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
print("  dis olcu  x %.0f..%.0f  y %.0f..%.0f  z %.0f..%.0f" % (bb[0]/M,bb[3]/M,bb[1]/M,bb[4]/M,bb[2]/M,bb[5]/M))
print("=== ON YUZ KONUMLARI (y alt kenar) ===")
for c in sorted(ust, key=lambda c: (c.GetBox(False,False)[0], c.GetBox(False,False)[1])):
    n = c.Name2.rsplit("-",1)[0]
    if n.startswith(("CEKMECE3_","KLAPE3_")):
        g = c.GetBox(False, False)
        print("  %-20s x %6.1f..%-6.1f  y %6.1f..%-6.1f" % (n, g[0]/M, g[3]/M, g[1]/M, g[4]/M))
# gorseller
d.ClearSelection2(True); n = 0
f = mcall(d, "FirstFeature")
while f is not None:
    if mcall(f, "GetTypeName2") == "RefPlane": d.Extension.SelectByID2(f.Name, "PLANE", 0.0,0.0,0.0, True, 0, NUL_, 0); n += 1
    f = mcall(f, "GetNextFeature")
if n: mcall(d, "BlankRefGeom")
d.ClearSelection2(True)
png(d, os.path.join(R, "STORE_v3_on.png"), "*Front", 1100, 1450)
ad = [i for i in range(1, 26) if d.Parameter("D1@LimitDistance%d" % i) is not None]
for i in ad[:4]: d.Parameter("D1@LimitDistance%d" % i).SystemValue = 0.45
mcall(d, "EditRebuild3"); time.sleep(2)
png(d, os.path.join(R, "STORE_v3_acik_iso.png"), "*Isometric", 1600, 1000)
for i in ad[:4]: d.Parameter("D1@LimitDistance%d" % i).SystemValue = 0.0
# --- KLAPE 90 DERECE: kaset kati dumduz mu, kot farki kaldi mi ---
ac = None
for ad2 in ["D1@LimitAngle%d" % i for i in range(1, 6)] + ["D1@Angle%d" % i for i in range(1, 6)]:
    if d.Parameter(ad2) is not None: ac = ad2; break
if ac:
    d.Parameter(ac).SystemValue = math.radians(90.0)
    mcall(d, "EditRebuild3"); time.sleep(2)
    png(d, os.path.join(R, "STORE_v3_klape90_iso.png"), "*Isometric", 1600, 1000)
    png(d, os.path.join(R, "STORE_v3_klape90_yan.png"), "*Right", 1400, 1100)
    kl = [c for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren
          if c.Name2.startswith("KLAPE3_")]
    if kl:
        g = kl[0].GetBox(False, False)
        print("=== KLAPE 90 ===  aci olcusu=%s  klape kutusu y %.1f..%.1f  z %.1f..%.1f"
              % (ac, g[1]/M, g[4]/M, g[2]/M, g[5]/M))
    d.Parameter(ac).SystemValue = 0.0
    mcall(d, "EditRebuild3"); time.sleep(1)
else:
    print("=== KLAPE 90 ===  aci olcusu YOK — mate betigi calistirilmali")
e2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
print("=== KAYIT ===  mesafe olcusu=%d  kayit=%s  hata=%d uyari=%d" % (len(ad), bool(d.Save3(1,e2,w2)), e.value, w.value))
