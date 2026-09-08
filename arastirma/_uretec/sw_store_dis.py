# -*- coding: utf-8 -*-
# AUTOKITCH — 1 · STORE soğuk depo, DIŞ GÖVDE — doğrudan SolidWorks 2025 içinde (COM API) (7 Eyl 2026)
# Yalnız dış görünüş, gerçek ölçüler, iç detay yok. Her eleman ayrı Boss-Extrude, feature ağacında adıyla.
# Koordinat: X sağa (genişlik), Y yukarı (yükseklik, zemin=0), Z öne (ön yüz z=0, gövde -Z'ye doğru).
import win32com.client, os, time, pythoncom
from win32com.client import VARIANT

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\1_STORE"
TPL = r"C:\ProgramData\SolidWorks\SOLIDWORKS 2025\templates\MBD\part 1001mm and larger.prtdot"
# ---------------- ölçüler (mm) ----------------
W, D, H = 1400.0, 840.0, 1970.0
H_FOOT, H_BODY, T_FRONT, GAP = 120.0, 1850.0, 20.0, 6.0
L0, L1, R0, R1, SIDE = 66.0, 690.0, 714.0, 1338.0, 66.0
FRONT = [
    ('panel_sogutma',      SIDE, W-SIDE, 1670, 1950, 'panel'),
    ('panel_bant_ust',     SIDE, W-SIDE, 1610, 1664, 'panel'),
    ('cekmece_icecek_1',   L0, L1, 1484, 1608, 'cekmece'),
    ('cekmece_icecek_2',   L0, L1, 1354, 1478, 'cekmece'),
    ('cekmece_icecek_3',   L0, L1, 1224, 1348, 'cekmece'),
    ('cekmece_icecek_4',   L0, L1, 1094, 1218, 'cekmece'),
    ('cekmece_1L',         L0, L1,  772, 1088, 'cekmece'),
    ('cekmece_taze_1',     R0, R1, 1509, 1608, 'cekmece'),
    ('cekmece_taze_2',     R0, R1, 1404, 1503, 'cekmece'),
    ('cekmece_taze_3',     R0, R1, 1299, 1398, 'cekmece'),
    ('cekmece_taze_4',     R0, R1, 1194, 1293, 'cekmece'),
    ('cekmece_taze_5',     R0, R1, 1089, 1188, 'cekmece'),
    ('cekmece_taze_6',     R0, R1,  984, 1083, 'cekmece'),
    ('cekmece_taze_7',     R0, R1,  879,  978, 'cekmece'),
    ('cekmece_taze_8',     R0, R1,  774,  873, 'cekmece'),
    ('panel_ayirici_PU80', SIDE, W-SIDE,  690,  766, 'panel'),
    ('klape_kaset_kati',   L0, L1,  403,  687, 'klape'),
    ('panel_bos_bant',     R0, R1,  403,  687, 'panel'),
    ('cekmece_donmus_1',   L0, L1,  297,  391, 'cekmece'),
    ('cekmece_donmus_2',   L0, L1,  197,  291, 'cekmece'),
    ('cekmece_donmus_3',   R0, R1,  297,  391, 'cekmece'),
    ('cekmece_donmus_4',   R0, R1,  197,  291, 'cekmece'),
    ('panel_bant_alt',     SIDE, W-SIDE,  120,  191, 'panel'),
]
RAILS = [('sove_sol', 0, SIDE), ('sove_orta', L1, R0), ('sove_sag', W-SIDE, W)]
FEET  = [(60, 60), (W-140, 60), (60, D-140), (W-140, D-140)]   # (x, y_derinlik önden)

M = 0.001  # mm → m (API metre kullanır)

def mcall(o, name, *args):
    """geç bağlamada argümansız metotları güvenli çağır (METHOD|PROPERTYGET)"""
    did = o._oleobj_.GetIDsOfNames(0, name)
    if isinstance(did, tuple): did = did[0]
    r = o._oleobj_.Invoke(did, 0, pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET, True, *args)
    return win32com.client.Dispatch(r) if isinstance(r, pythoncom.TypeIIDs[pythoncom.IID_IDispatch]) else r

sw = win32com.client.Dispatch("SldWorks.Application"); sw.Visible = True
sw.CloseAllDocuments(True)                       # önceki (kaydedilmemiş) denemeleri kapat
doc = sw.NewDocument(TPL, 0, 0, 0)
if doc is None: raise SystemExit("sablon acilamadi: " + TPL)
doc = sw.ActiveDoc
ext = doc.Extension; sk = doc.SketchManager; fm = doc.FeatureManager; sel = doc.SelectionManager
sk.AddToDB = True; sk.DisplayWhenAdded = False
FE = []   # (feature, ad)

# referans düzlemleri feature ağacından al (dil bağımsız: ilk 3 RefPlane = Front, Top, Right)
PLANES = []
_f = mcall(doc, "FirstFeature")
while _f is not None and len(PLANES) < 3:
    if mcall(_f, "GetTypeName2") == "RefPlane": PLANES.append(_f)
    _f = mcall(_f, "GetNextFeature")
print("duzlemler:", [f.Name for f in PLANES])
def _sel_plane(idx):
    doc.ClearSelection2(True)
    ok = PLANES[idx].Select2(False, 0)
    if not ok: raise RuntimeError("duzlem secilemedi: %d" % idx)

def extrude_rect(name, plane, u0, u1, v0, v1, depth, flip, merge=True, cut=False, start=0.0):
    """plane eskizinde (u,v) dikdörtgen → depth kadar ekstrüzyon. flip=True: düzlemin ters yönüne."""
    _sel_plane(plane); sk.InsertSketch(True)
    sk.CreateCornerRectangle(u0*M, v0*M, 0, u1*M, v1*M, 0)
    sk.InsertSketch(True)                         # eskizi kapat
    if cut:
        t0 = 3 if start else 0
        f = fm.FeatureCut4(True, False, not flip, 0, 0, depth*M, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, False, False, False, t0, start*M, False, False)
    else:
        f = fm.FeatureExtrusion3(True, False, flip, 0, 0, depth*M, 0, False, False, False, False, 0, 0, False, False, False, False, merge, True, True, 0, 0, False)
    if f is None: raise RuntimeError("feature olusmadi: " + name)
    f.Name = name; FE.append(f); doc.ClearSelection2(True)
    return f

# Düzlemler: Front Plane = XY (normal +Z); Top Plane = XZ; Right = YZ.
# Front eskizde u=X, v=Y. Ekstrüzyon "flip=False" → +Z (öne), "flip=True" → −Z (arkaya).
# Ön yüz z=0; gövde z ∈ [−(D−T_FRONT), −T_FRONT] olsun → gövde arkaya, önler öne.
FRONT_PLANE = 0; TOP_PLANE = 1

t0 = time.time()
# 1) gövde kasa: Front Plane'de W×H_BODY dikdörtgen, z=−T_FRONT'tan −D'ye. Eskiz z=0'da olduğu için önce
#    T_FRONT boşluğu bırakmak yerine gövdeyi z=0..−(D) çiziyoruz; önler z=0..+T_FRONT öne taşacak. Böylece
#    toplam derinlik yine D: gövde 820 (z 0..−820) + ön 20 (z 0..+20). Ön yüz düzlemi z=+20.
extrude_rect("govde_kasa", FRONT_PLANE, 0, W, H_FOOT, H_FOOT+H_BODY, D - T_FRONT, True, merge=False)

# 2) ayaklar 80×80×120: Top Plane eskiz (u=X, v=Z). Top Plane normali +Y; flip=False → +Y (yukarı).
#    Ayak derinlik konumu önden y_ölçüsü: ön yüz z=+20 olduğuna göre z = 20 − y.
for i, (ax, ay) in enumerate(FEET, 1):
    z0 = T_FRONT - ay; z1 = z0 - 80
    # Top Plane'de v ekseni: SolidWorks Top Plane eskiz v = −Z (eskiz +Y yönü model −Z'ye bakar)
    extrude_rect("ayak_%d" % i, TOP_PLANE, ax, ax+80, -z0, -z1, H_FOOT, False, merge=False)

# 3) söveler: z 0..+20 öne
for nm, x0, x1 in RAILS:
    extrude_rect(nm, FRONT_PLANE, x0, x1, H_FOOT, H_FOOT+H_BODY, T_FRONT, False, merge=False)

# 4) çekmece önleri / klape / paneller: z 0..+20 öne, fuga GAP
for nm, x0, x1, z0, z1, tip in FRONT:
    g = GAP/2
    extrude_rect(nm, FRONT_PLANE, x0+g, x1-g, z0+g, z1-g, T_FRONT, False, merge=False)
    if tip in ('cekmece', 'klape'):
        w = (x1-x0) - GAP
        kw = min(300.0, w*0.45) if tip == 'cekmece' else 180.0
        kx = x0 + g + (w-kw)/2; kz = z1 - g - 60
        # gömme kulp: ön yüz z=+20'den 13 mm derin, 34 mm yüksek oyuk → kesme z=7'den +Z'ye 13 mm (offset başlangıç)
        extrude_rect(nm + "_kulp", FRONT_PLANE, kx, kx+kw, kz, kz+34, 13.0, False, cut=True, start=T_FRONT-13)

# görünüm + kaydet
mcall(doc, "ViewZoomtofit2"); doc.ShowNamedView2("*Isometric", 7); mcall(doc, "ViewZoomtofit2")
os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "STORE_dis_v1.SLDPRT")
err = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); warn = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
NUL = VARIANT(pythoncom.VT_DISPATCH, None)
ok = ext.SaveAs3(path, 0, 1, NUL, NUL, err, warn)
png = os.path.join(OUT, "STORE_dis_v1_sw_iso.png")
doc.SaveBMP(png, 1600, 1200)
# doğrulama
bodies = doc.GetBodies2(0, True)
bb = [1e9,1e9,1e9,-1e9,-1e9,-1e9]
for b in bodies:
    x = mcall(b, "GetBodyBox")
    for i in range(3):
        bb[i] = min(bb[i], x[i]); bb[i+3] = max(bb[i+3], x[i+3])
print("kaydedildi:", ok, path, "err", err.value, "warn", warn.value)
print("feature sayisi:", len(FE), "| govde sayisi:", len(bodies))
print("gabari (mm): %.0f x %.0f x %.0f" % ((bb[3]-bb[0])/M, (bb[4]-bb[1])/M, (bb[5]-bb[2])/M))
print("z araligi (mm): %.0f .. %.0f | y: %.0f .. %.0f" % (bb[2]/M, bb[5]/M, bb[1]/M, bb[4]/M))
print("sure %.0f s" % (time.time()-t0))
