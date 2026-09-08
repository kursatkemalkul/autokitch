# -*- coding: utf-8 -*-
# AUTOKITCH — PRESS · TOPPING · OVEN · PACK dış gövdeleri + HAT montajı, doğrudan SolidWorks 2025 (COM) (7 Eyl 2026)
# Kaynak: hat_dis_kapak_gorunus_v2 (kapak_gorunus2.py) zonları, cm → mm. Yalnız dış görünüş.
# Koordinat: X sağa, Y yukarı (zemin 0), Z öne. Ön yüz z=+20 (paneller), gövde z 0..−820. Açıklıklar gövdeye 100 mm oyuk.
import win32com.client, os, time, pythoncom
from win32com.client import VARIANT
from PIL import Image

OUT_ROOT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
TPL_DIR  = r"C:\ProgramData\SolidWorks\SOLIDWORKS 2025\templates\MBD"
TPL_PRT  = os.path.join(TPL_DIR, "part 1001mm and larger.prtdot")
TPL_ASM  = os.path.join(TPL_DIR, "assembly 1001mm and larger.asmdot")
M = 0.001
D, H, H_FOOT, H_BODY, T_FRONT, OPN_DEPTH = 840.0, 1970.0, 120.0, 1850.0, 20.0, 100.0

# ---- istasyon tanımları: (klasör, dosya, genişlik cm, ayak tipi, [ (ad, x0,x1,z0,z1, tip) cm ]) ----
# tip: pan=sabit panel · ele=eleman servis kapağı · gls=cam kapak · opn=robot/tepsi açıklığı (oyuk) · panl=ince panel
STATIONS = [
 ("2_PRESS", "PRESS_dis_v1", 70, "feet", [
    ("panel_ust",          3, 67, 134, 195, "pan"),
    ("kapak_pano_ust",     3, 33, 134, 178, "ele"),
    ("panel_orta",         3, 67,  45, 134, "pan"),
    ("aciklik_tepsi",     10, 60,  72, 108, "opn"),
    ("panel_alt",          3, 67,  12,  45, "pan")]),
 ("3_TOPPING", "TOPPING_dis_v1", 70, "plint", [
    ("aciklik_kat1",       3, 67, 156, 195, "opn"),
    ("aciklik_kat2",       3, 67, 115, 156, "opn"),
    ("aciklik_kat3",       3, 67,  74, 115, "opn"),
    ("klape_alt_1",        3, 67,  46,  74, "ele"),
    ("klape_alt_2",        3, 67,  19,  46, "ele"),
    ("panel_alt",          3, 67,  12,  19, "panl")]),
 ("4_OVEN", "OVEN_dis_v1", 70, "plint", [
    ("kapak_fan_filtre",   3, 67, 168, 195, "ele"),
    ("firin_kapak_2_cam",  3, 67, 140, 168, "gls"),
    ("firin_kapak_1_cam",  3, 67, 112, 140, "gls"),
    ("kapak_yag_kabi",     3, 18,  82, 112, "ele"),
    ("aciklik_sprey",     18, 67,  82, 112, "opn"),
    ("aciklik_kesme",      3, 67,  32,  82, "opn"),
    ("kapak_pano",         3, 67,  12,  32, "ele")]),
 ("5_PACK", "PACK_dis_v1", 70, "plint", [
    ("kapi_sarjor",        3, 67, 104, 195, "ele"),
    ("aciklik_kutulama",   3, 67,  60, 104, "opn"),
    ("kapak_pano_mek",     3, 67,  12,  60, "ele")]),
]
HAT_ORDER = [("1_STORE", "STORE_dis_v1", 140)] + [(d, f, w) for d, f, w, _, _ in STATIONS]

def mcall(o, name, *args):
    did = o._oleobj_.GetIDsOfNames(0, name)
    if isinstance(did, tuple): did = did[0]
    r = o._oleobj_.Invoke(did, 0, pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET, True, *args)
    return win32com.client.Dispatch(r) if isinstance(r, pythoncom.TypeIIDs[pythoncom.IID_IDispatch]) else r

sw = win32com.client.Dispatch("SldWorks.Application"); sw.Visible = True
NUL = VARIANT(pythoncom.VT_DISPATCH, None)

def save(doc, path, png):
    err = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); warn = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    ok = doc.Extension.SaveAs3(path, 0, 1, NUL, NUL, err, warn)
    doc.ShowNamedView2("*Isometric", 7); mcall(doc, "ViewZoomtofit2")
    doc.SaveBMP(png, 1600, 1200); Image.open(png).save(png)      # BMP → gerçek PNG
    return ok, err.value

def bbox(doc):
    bb = [1e9]*3 + [-1e9]*3
    for b in doc.GetBodies2(0, True):
        x = mcall(b, "GetBodyBox")
        for i in range(3): bb[i] = min(bb[i], x[i]); bb[i+3] = max(bb[i+3], x[i+3])
    return [v/M for v in bb]

class Part:
    def __init__(self):
        sw.NewDocument(TPL_PRT, 0, 0, 0); self.doc = sw.ActiveDoc
        self.sk = self.doc.SketchManager; self.fm = self.doc.FeatureManager
        self.sk.AddToDB = True; self.sk.DisplayWhenAdded = False
        self.planes = []; f = mcall(self.doc, "FirstFeature")
        while f is not None and len(self.planes) < 3:
            if mcall(f, "GetTypeName2") == "RefPlane": self.planes.append(f)
            f = mcall(f, "GetNextFeature")
    def rect(self, name, plane, u0, u1, v0, v1, depth, flip, cut=False, start=0.0):
        self.doc.ClearSelection2(True); self.planes[plane].Select2(False, 0); self.sk.InsertSketch(True)
        self.sk.CreateCornerRectangle(u0*M, v0*M, 0, u1*M, v1*M, 0); self.sk.InsertSketch(True)
        if cut:
            f = self.fm.FeatureCut4(True, False, not flip, 0, 0, depth*M, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, False, False, False, 3 if start else 0, start*M, False, False)
        else:
            f = self.fm.FeatureExtrusion3(True, False, flip, 0, 0, depth*M, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, 0, 0, False)
        if f is None: raise RuntimeError("feature olusmadi: " + name)
        f.Name = name; self.doc.ClearSelection2(True); return f

def build_station(folder, fname, wcm, foot, elems):
    W = wcm*10.0; p = Part(); FR, TP = 0, 1
    p.rect("govde_kasa", FR, 0, W, H_FOOT, H_FOOT+H_BODY, D-T_FRONT, True)
    if foot == "feet":
        for i, (ax, ay) in enumerate([(50, 60), (W-130, 60), (50, D-140), (W-130, D-140)], 1):
            z0 = T_FRONT-ay; p.rect("ayak_%d" % i, TP, ax, ax+80, -z0, -(z0-80), H_FOOT, False)
    else:   # kapalı plint: 20 mm içeri çekik, tam derinlik
        p.rect("plint", FR, 20, W-20, 0, H_FOOT, D-T_FRONT-20, True)
    # ön yüz söveleri (30 mm kenar) — paneller 3 cm'den başlıyor
    p.rect("sove_sol", FR, 0, 30, H_FOOT, H_FOOT+H_BODY, T_FRONT, False)
    p.rect("sove_sag", FR, W-30, W, H_FOOT, H_FOOT+H_BODY, T_FRONT, False)
    for nm, x0, x1, z0, z1, tip in elems:
        x0, x1, z0, z1 = x0*10.0+3, x1*10.0-3, z0*10.0+3, z1*10.0-3     # 6 mm fuga
        if tip == "opn":
            p.rect(nm, FR, x0, x1, z0, z1, OPN_DEPTH, True, cut=True)     # gövdeye 100 mm oyuk
        else:
            t = 12.0 if tip == "gls" else T_FRONT
            p.rect(nm, FR, x0, x1, z0, z1, t, False)
            if tip == "ele":                                              # servis kapağı: sağ kenarda dikey gömme tutamak
                kh = min(180.0, (z1-z0)*0.5); kz = (z0+z1)/2 - kh/2
                p.rect(nm+"_kulp", FR, x1-40, x1-14, kz, kz+kh, 13.0, False, cut=True, start=T_FRONT-13)
    out = os.path.join(OUT_ROOT, folder); os.makedirs(out, exist_ok=True)
    path = os.path.join(out, fname + ".SLDPRT"); png = os.path.join(out, fname + "_sw_iso.png")
    ok, err = save(p.doc, path, png); bb = bbox(p.doc)
    print("%-16s kayit=%s err=%d govde=%d gabari %.0fx%.0fx%.0f mm" % (fname, ok, err, len(p.doc.GetBodies2(0, True)), bb[3]-bb[0], bb[4]-bb[1], bb[5]-bb[2]))
    sw.CloseDoc(p.doc.GetTitle)
    return path

t0 = time.time()
import sys
sw.CloseAllDocuments(True)
paths = {"STORE_dis_v1": os.path.join(OUT_ROOT, "1_STORE", "STORE_dis_v1.SLDPRT")}
for folder, fname, wcm, foot, elems in STATIONS:
    paths[fname] = os.path.join(OUT_ROOT, folder, fname + ".SLDPRT")
    if "--asm" not in sys.argv: build_station(folder, fname, wcm, foot, elems)

# ---- HAT montajı: istasyonlar yan yana, ön yüzler aynı düzlemde ----
sw.NewDocument(TPL_ASM, 0, 0, 0); asm = sw.ActiveDoc
x = 0.0
for folder, fname, wcm in HAT_ORDER:
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    sw.OpenDoc6(paths[fname], 1, 1, "", e, w)              # bileşen belleğe yüklensin (sessiz)
    # AddComponent5 verilen noktaya parçanın BBOX MERKEZİNİ koyar (deneyle görüldü) → merkez kaydırması ekle
    comp = asm.AddComponent5(paths[fname], 0, "", False, "", (x + wcm*5.0)*M, (H/2)*M, ((T_FRONT - (D - T_FRONT))/2)*M)
    if comp is None: raise RuntimeError("bilesen eklenemedi: " + fname)
    x += wcm*10.0
    sw.CloseDoc(os.path.basename(paths[fname]))
asm.ClearSelection2(True)
out = os.path.join(OUT_ROOT, "FULL_MAKINE"); os.makedirs(out, exist_ok=True)
apath = os.path.join(out, "HAT_dis_v1.SLDASM"); apng = os.path.join(out, "HAT_dis_v1_sw_iso.png")
ok, err = save(asm, apath, apng)
asm.ShowNamedView2("*Front", 1); mcall(asm, "ViewZoomtofit2")
apng2 = os.path.join(out, "HAT_dis_v1_sw_on.png"); asm.SaveBMP(apng2, 1800, 900); Image.open(apng2).save(apng2)
root = asm.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True)
for c in root.GetChildren:
    d = c.Transform2.ArrayData; print("  %-18s x=%5.0f y=%3.0f z=%3.0f" % (c.Name2, d[9]/M, d[10]/M, d[11]/M))
print("HAT montaji kayit=%s err=%d bilesen=%d toplam genislik=%.0f mm" % (ok, err, asm.GetComponentCount(True), x))
print("sure %.0f s" % (time.time()-t0))
