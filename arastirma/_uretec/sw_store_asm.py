# -*- coding: utf-8 -*-
# AUTOKITCH — 1 · STORE, AYRI PARÇALI SAC KASA + MONTAJ, doğrudan SolidWorks 2025 (COM) (7 Eyl 2026)
# Kurgu: bükme sac self-supporting soğuk dolap. Dış kabuk 1,5 mm 304 · iç kabuk 1,0 mm 304 · PU 60 (yan/arka/taban/tavan) · PU80 ayırıcı.
# Çekmece önü sandviç 40 (1,5 dış + 37,5 PU + 1,0 iç) · çekmece kutusu 1,0 mm U-profil 600 derin. Her eleman AYRI .SLDPRT, STORE.SLDASM'de birleşir.
# Koordinat (montaj = parça, global): X sağa 0..1400, Y yukarı zemin 0..1970, Z öne; kasa z −820..0, ön yüzler z 0..40.
import win32com.client, os, time, pythoncom, sys
from win32com.client import VARIANT
from PIL import Image

ROOT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\1_STORE"
PDIR = os.path.join(ROOT, "parca"); os.makedirs(PDIR, exist_ok=True)
TPL_DIR = r"C:\ProgramData\SolidWorks\SOLIDWORKS 2025\templates\MBD"
TPL_PRT = os.path.join(TPL_DIR, "part 1001mm and larger.prtdot"); TPL_ASM = os.path.join(TPL_DIR, "assembly 1001mm and larger.asmdot")
M = 0.001
T_DIS, T_IC, PU, PU_AYR = 1.5, 1.0, 60.0, 80.0
W, D, H = 1400.0, 840.0, 1970.0
Y0 = 120.0                      # ayak üstü / kasa altı
Y_CELL0 = Y0 + T_DIS + PU + T_IC        # hücre tabanı 182,5
Y_CELL1 = 1610.0                        # hücre tavanı (iç sac altı)
Y_TEK0 = Y_CELL1 + T_IC + (PU-2) + T_IC # teknik bölme tabanı 1670
Z_ARKA_IC = -(D - 20) + T_DIS + PU + T_IC   # −757,5  (kasa derinliği 820: z −820..0)
ZK = -(D - 20)                   # −820
X_IC0, X_IC1 = T_DIS + PU + T_IC, W - T_DIS - PU - T_IC   # 62,5 .. 1337,5
L0, L1, R0, R1, SIDE = 66.0, 690.0, 714.0, 1338.0, 66.0
F0, F1 = 0.0, 40.0               # ön yüz sandviç z aralığı
GAP = 6.0; RAY = 12.7; KUTU_D = 600.0
FRONT = [
    ('cekmece_icecek_1', L0, L1, 1484, 1608, 'cekmece'), ('cekmece_icecek_2', L0, L1, 1354, 1478, 'cekmece'),
    ('cekmece_icecek_3', L0, L1, 1224, 1348, 'cekmece'), ('cekmece_icecek_4', L0, L1, 1094, 1218, 'cekmece'),
    ('cekmece_1L',       L0, L1,  772, 1088, 'cekmece'),
    ('cekmece_taze_1', R0, R1, 1509, 1608, 'cekmece'), ('cekmece_taze_2', R0, R1, 1404, 1503, 'cekmece'),
    ('cekmece_taze_3', R0, R1, 1299, 1398, 'cekmece'), ('cekmece_taze_4', R0, R1, 1194, 1293, 'cekmece'),
    ('cekmece_taze_5', R0, R1, 1089, 1188, 'cekmece'), ('cekmece_taze_6', R0, R1,  984, 1083, 'cekmece'),
    ('cekmece_taze_7', R0, R1,  879,  978, 'cekmece'), ('cekmece_taze_8', R0, R1,  774,  873, 'cekmece'),
    ('klape_kaset_kati', L0, L1, 403, 687, 'klape'),
    ('cekmece_donmus_1', L0, L1, 297, 391, 'cekmece'), ('cekmece_donmus_2', L0, L1, 197, 291, 'cekmece'),
    ('cekmece_donmus_3', R0, R1, 297, 391, 'cekmece'), ('cekmece_donmus_4', R0, R1, 197, 291, 'cekmece'),
]

def mcall(o, name, *args):
    did = o._oleobj_.GetIDsOfNames(0, name); did = did[0] if isinstance(did, tuple) else did
    r = o._oleobj_.Invoke(did, 0, pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET, True, *args)
    return win32com.client.Dispatch(r) if isinstance(r, pythoncom.TypeIIDs[pythoncom.IID_IDispatch]) else r
sw = win32com.client.Dispatch("SldWorks.Application"); sw.Visible = True
NUL = VARIANT(pythoncom.VT_DISPATCH, None)
def saveas(doc, path):
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    ok = doc.Extension.SaveAs3(path, 0, 1, NUL, NUL, e, w); return ok and e.value == 0
def png(doc, path, view, wpx=1800, hpx=1100):
    doc.ShowNamedView2(view, 7 if view == "*Isometric" else 1); mcall(doc, "ViewZoomtofit2"); doc.SaveBMP(path, wpx, hpx); Image.open(path).save(path)

PARTS = []   # (dosya yolu, bbox merkezi m)
class P:
    def __init__(self):
        sw.NewDocument(TPL_PRT, 0, 0, 0); self.doc = sw.ActiveDoc; self.sk = self.doc.SketchManager; self.fm = self.doc.FeatureManager
        self.sk.AddToDB = True; self.sk.DisplayWhenAdded = False; self.pl = []
        f = mcall(self.doc, "FirstFeature")
        while f is not None and len(self.pl) < 3:
            if mcall(f, "GetTypeName2") == "RefPlane": self.pl.append(f)
            f = mcall(f, "GetNextFeature")
    def _ext(self, name, n0, n1, cut=False):
        """eskiz düzlemine dik aralık [n0,n1] (mm): n0>=0 → +yön, n1<=0 → −yön (offset semantiği deneyle doğrulandı)"""
        if n0 >= 0: dirf, fs, st, dp = False, False, n0, n1 - n0
        else:       dirf, fs, st, dp = True, True, -n1, n1 - n0
        if cut: f = self.fm.FeatureCut4(True, False, not dirf, 0, 0, dp*M, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, False, False, False, 3 if st else 0, st*M, fs, False)
        else:   f = self.fm.FeatureExtrusion3(True, False, dirf, 0, 0, dp*M, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, 3 if st else 0, st*M, fs)
        if f is None: raise RuntimeError("feature olusmadi: " + name)
        f.Name = name; self.doc.ClearSelection2(True); return f
    def poly(self, name, plane, pts, n0, n1, cut=False):
        self.doc.ClearSelection2(True); self.pl[plane].Select2(False, 0); self.sk.InsertSketch(True)
        for i in range(len(pts)):
            a, b = pts[i], pts[(i+1) % len(pts)]; self.sk.CreateLine(a[0]*M, a[1]*M, 0, b[0]*M, b[1]*M, 0)
        self.sk.InsertSketch(True); return self._ext(name, n0, n1, cut)
    def rect(self, name, plane, u0, u1, v0, v1, n0, n1, cut=False):
        self.doc.ClearSelection2(True); self.pl[plane].Select2(False, 0); self.sk.InsertSketch(True)
        self.sk.CreateCornerRectangle(u0*M, v0*M, 0, u1*M, v1*M, 0); self.sk.InsertSketch(True); return self._ext(name, n0, n1, cut)
    def done(self, fname):
        b = self.doc.GetBodies2(0, True); bb = [1e9]*3 + [-1e9]*3
        for x in b:
            g = mcall(x, "GetBodyBox")
            for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
        path = os.path.join(PDIR, fname + ".SLDPRT")
        if not saveas(self.doc, path): raise RuntimeError("kayit hatasi " + fname)
        sw.CloseDoc(self.doc.GetTitle); PARTS.append((path, [(bb[i]+bb[i+3])/2 for i in range(3)])); return path

FR, TP = 0, 1
def box(fname, x0, x1, y0, y1, z0, z1):
    """Front Plane eskizi (u=X, v=Y), z aralığı [z0,z1] → tek gövdeli parça dosyası"""
    p = P(); p.rect(fname, FR, x0, x1, y0, y1, z0, z1); return p.done(fname)
def prism_y(fname, pts_xz, y0, y1):
    """Top Plane eskizi (u=X, v=−Z) kapalı poligon, Y aralığı [y0,y1]"""
    p = P(); p.poly(fname, TP, [(x, -z) for x, z in pts_xz], y0, y1); return p.done(fname)

t0 = time.time()
if "--asm" not in sys.argv:
    sw.CloseAllDocuments(True)
    # ---- ayaklar 80×80×120 ----
    for i, (ax, az) in enumerate([(60, -40), (W-140, -40), (60, ZK+60), (W-140, ZK+60)], 1):
        box("STORE_ayak_%d" % i, ax, ax+80, 0, Y0, az-80, az)
    # ---- dış kabuk 1,5 ----
    box("STORE_dis_yan_sol", 0, T_DIS, Y0, H, ZK, 0)
    box("STORE_dis_yan_sag", W-T_DIS, W, Y0, H, ZK, 0)
    box("STORE_dis_ust", T_DIS, W-T_DIS, H-T_DIS, H, ZK, 0)
    box("STORE_dis_arka", T_DIS, W-T_DIS, Y0, H-T_DIS, ZK, ZK+T_DIS)
    box("STORE_dis_alt", T_DIS, W-T_DIS, Y0, Y0+T_DIS, ZK+T_DIS, 0)
    # ---- PU 60 + iç kabuk 1,0 (soğuk hücre y 182,5..1610; teknik bölme üstte tek cidar) ----
    box("STORE_pu_yan_sol", T_DIS, T_DIS+PU, Y0+T_DIS, Y_TEK0, ZK+T_DIS, 0)
    box("STORE_pu_yan_sag", W-T_DIS-PU, W-T_DIS, Y0+T_DIS, Y_TEK0, ZK+T_DIS, 0)
    box("STORE_pu_arka", T_DIS+PU, W-T_DIS-PU, Y0+T_DIS, Y_TEK0, ZK+T_DIS, ZK+T_DIS+PU)
    box("STORE_pu_alt", T_DIS+PU, W-T_DIS-PU, Y0+T_DIS, Y0+T_DIS+PU, ZK+T_DIS+PU, 0)
    box("STORE_ic_yan_sol", X_IC0-T_IC, X_IC0, Y_CELL0-T_IC, Y_CELL1+T_IC, Z_ARKA_IC-T_IC, 0)
    box("STORE_ic_yan_sag", X_IC1, X_IC1+T_IC, Y_CELL0-T_IC, Y_CELL1+T_IC, Z_ARKA_IC-T_IC, 0)
    box("STORE_ic_arka", X_IC0, X_IC1, Y_CELL0-T_IC, Y_CELL1+T_IC, Z_ARKA_IC-T_IC, Z_ARKA_IC)
    box("STORE_ic_alt", X_IC0, X_IC1, Y_CELL0-T_IC, Y_CELL0, Z_ARKA_IC, 0)
    box("STORE_ic_tavan", X_IC0, X_IC1, Y_CELL1, Y_CELL1+T_IC, Z_ARKA_IC, 0)
    box("STORE_pu_tavan", T_DIS+PU, W-T_DIS-PU, Y_CELL1+T_IC, Y_TEK0-T_IC, ZK+T_DIS+PU, 0)
    box("STORE_teknik_taban", T_DIS+PU, W-T_DIS-PU, Y_TEK0-T_IC, Y_TEK0, ZK+T_DIS+PU, 0)
    # ---- yatay ayırıcı PU80 (y 690..766) ve orta dikey bölme (x 690..714) ----
    box("STORE_ayirici_sac_alt", X_IC0, X_IC1, 690, 691, Z_ARKA_IC, 0)
    box("STORE_ayirici_pu", X_IC0, X_IC1, 691, 765, Z_ARKA_IC, 0)
    box("STORE_ayirici_sac_ust", X_IC0, X_IC1, 765, 766, Z_ARKA_IC, 0)
    box("STORE_orta_bolme_sac_sol", 690, 691, Y_CELL0, Y_CELL1, Z_ARKA_IC, 0)
    box("STORE_orta_bolme_pu", 691, 713, Y_CELL0, Y_CELL1, Z_ARKA_IC, 0)
    box("STORE_orta_bolme_sac_sag", 713, 714, Y_CELL0, Y_CELL1, Z_ARKA_IC, 0)
    # ---- ön çerçeve: bükme sac 1,5 (L / T profil, üstten görünüş, Y boyunca) ----
    zf0, zf1 = F1-T_DIS, F1
    prism_y("STORE_sove_sol", [(0, zf1), (0, zf0), (SIDE-T_DIS, zf0), (SIDE-T_DIS, F0), (SIDE, F0), (SIDE, zf1)], Y0, H)
    prism_y("STORE_sove_sag", [(W, zf1), (W, zf0), (W-SIDE+T_DIS, zf0), (W-SIDE+T_DIS, F0), (W-SIDE, F0), (W-SIDE, zf1)], Y0, H)
    xm = (L1+R0)/2
    prism_y("STORE_sove_orta", [(L1, zf1), (L1, zf0), (xm-T_DIS/2, zf0), (xm-T_DIS/2, F0), (xm+T_DIS/2, F0), (xm+T_DIS/2, zf0), (R0, zf0), (R0, zf1)], Y_CELL0, Y_CELL1)
    # ---- sabit ön paneller 1,5 (ön yüzle aynı düzlem) ----
    box("STORE_panel_sogutma", SIDE, W-SIDE, Y_TEK0, H, zf0, zf1)          # teknik bölme servis paneli
    box("STORE_panel_bant_ust", SIDE, W-SIDE, Y_CELL1, Y_TEK0, zf0, zf1)
    box("STORE_panel_ayirici_on", SIDE, W-SIDE, 690, 766, zf0, zf1)
    box("STORE_panel_bos_bant", R0, R1, 403, 687, zf0, zf1)
    box("STORE_panel_bant_alt", SIDE, W-SIDE, Y0, Y_CELL0, zf0, zf1)
    # ---- çekmece önleri (sandviç 40) + kutuları (U-profil 1,0 × 600) ----
    for nm, x0, x1, y0, y1, tip in FRONT:
        g = GAP/2; a, b, c, d = x0+g, x1-g, y0+g, y1-g
        box(nm + "_on_ic_sac", a, b, c, d, F0, F0+T_IC)
        box(nm + "_on_pu", a, b, c, d, F0+T_IC, F1-T_DIS)
        box(nm + "_on_dis_sac", a, b, c, d, F1-T_DIS, F1)
        if tip == 'cekmece':
            ka, kb = a + RAY + 1, b - RAY - 1; kc, kd = c + 8, d - 12
            p = P(); p.poly(nm + "_kutu", FR, [(ka, kd), (ka, kc), (kb, kc), (kb, kd), (kb-T_IC, kd), (kb-T_IC, kc+T_IC), (ka+T_IC, kc+T_IC), (ka+T_IC, kd)], -KUTU_D, F0)
            p.done(nm + "_kutu")
    print("parca: %d, sure %.0f s" % (len(PARTS), time.time()-t0))
else:
    for f in sorted(os.listdir(PDIR)):
        if f.lower().endswith(".sldprt"): PARTS.append((os.path.join(PDIR, f), None))

# ---- STORE.SLDASM: her parça global koordinatta modellendi → AddComponent5 bbox merkezine koyar → merkez = kendi merkezi ----
sw.NewDocument(TPL_ASM, 0, 0, 0); asm = sw.ActiveDoc
for path, c in PARTS:
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(path, 1, 1, "", e, w)
    if c is None:
        bb = [1e9]*3 + [-1e9]*3
        for x in d.GetBodies2(0, True):
            g = mcall(x, "GetBodyBox")
            for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
        c = [(bb[i]+bb[i+3])/2 for i in range(3)]
    comp = asm.AddComponent5(path, 0, "", False, "", c[0], c[1], c[2])
    if comp is None: raise RuntimeError("bilesen eklenemedi " + path)
    sw.CloseDoc(os.path.basename(path))
root = asm.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True); comps = list(root.GetChildren)
asm.ClearSelection2(True)
for cpt in comps: cpt.Select4(True, NUL, False)
mcall(asm, "FixComponent"); asm.ClearSelection2(True)
bad = [cpt.Name2 for cpt in comps if max(abs(v) for v in cpt.Transform2.ArrayData[9:12]) > 1e-6]
apath = os.path.join(ROOT, "STORE.SLDASM"); print("montaj kayit:", saveas(asm, apath), "| bilesen:", len(comps), "| konum hatasi:", bad)
png(asm, os.path.join(ROOT, "STORE_asm_iso.png"), "*Isometric")
png(asm, os.path.join(ROOT, "STORE_asm_on.png"), "*Front")
print("toplam sure %.0f s" % (time.time()-t0))
