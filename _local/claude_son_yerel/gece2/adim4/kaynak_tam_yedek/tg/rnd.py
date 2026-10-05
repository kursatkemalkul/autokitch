# -*- coding: utf-8 -*-
"""VTK ekran dışı görüntü. python rnd.py glb out.png --kam ex,ey,ez [--hedef] [--kutu] [--gizle kpk,seffaf] [--ad] [--haric] [--vurgu] [--seg pkl] [--olcek] [--kesit eksen,değer,yön]"""
import sys, os, argparse, hashlib, pickle
import numpy as np, vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glbx import yukle, aralik_maske
ap = argparse.ArgumentParser(); ap.add_argument("glb"); ap.add_argument("out")
ap.add_argument("--kutu", default="1300,2650,700,2300,-900,130"); ap.add_argument("--kam", required=True); ap.add_argument("--hedef", default=None)
ap.add_argument("--gizle", default=""); ap.add_argument("--ad", default=""); ap.add_argument("--haric", default=""); ap.add_argument("--olcek", type=float, default=0)
ap.add_argument("--boy", default="1600,1200"); ap.add_argument("--kenar", type=int, default=1); ap.add_argument("--vurgu", default=""); ap.add_argument("--seg", default="")
ap.add_argument("--yukari", default="0,1,0")
a = ap.parse_args()
J, D = yukle(a.glb)
SEG = pickle.load(open(a.seg, "rb")) if a.seg else {}
k = [float(v) for v in a.kutu.split(",")]
ren = vtk.vtkRenderer(); ren.SetBackground(0.09, 0.1, 0.12)
adlar = [s for s in a.ad.split(",") if s]; haric = [s for s in a.haric.split(",") if s]; vurgu = [s for s in a.vurgu.split(",") if s]


def ciz(gad, X, T):
    pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(np.ascontiguousarray(X, dtype=np.float64), deep=1))
    cells = vtk.vtkCellArray()
    ids = np.hstack([np.full((len(T), 1), 3), T]).astype(np.int64).ravel()
    cells.SetCells(len(T), numpy_to_vtkIdTypeArray(ids, deep=1))
    pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(cells)
    mp = vtk.vtkPolyDataMapper(); mp.SetInputData(pd)
    ac = vtk.vtkActor(); ac.SetMapper(mp)
    h = hashlib.md5(gad.encode()).digest()
    col = (0.5 + 0.45 * h[0] / 255, 0.5 + 0.45 * h[1] / 255, 0.5 + 0.45 * h[2] / 255)
    if "__pu" in gad or "yalitim" in gad or "PU" in gad: col = (0.93, 0.86, 0.62)
    if "kablo" in gad: col = (0.95, 0.75, 0.2)
    if "seffaf" in gad: ac.GetProperty().SetOpacity(0.3)
    if vurgu and any(s in gad for s in vurgu): col = (1.0, 0.2, 0.15)
    ac.GetProperty().SetColor(*col); ren.AddActor(ac)
    if a.kenar:
        fe = vtk.vtkFeatureEdges(); fe.SetInputData(pd); fe.BoundaryEdgesOn(); fe.FeatureEdgesOn(); fe.SetFeatureAngle(30); fe.ManifoldEdgesOff(); fe.NonManifoldEdgesOff()
        m2 = vtk.vtkPolyDataMapper(); m2.SetInputConnection(fe.GetOutputPort()); m2.ScalarVisibilityOff()
        a2 = vtk.vtkActor(); a2.SetMapper(m2); a2.GetProperty().SetColor(0, 0, 0); ren.AddActor(a2)


for ad, dd in D.items():
    if adlar and not any(s in ad for s in adlar): continue
    X, T = dd["X"], dd["T"]
    msk = dd["ok"].copy()
    if "kpk" in a.gizle and dd["ex"].get("kpk"): msk &= ~aralik_maske(dd["ex"]["kpk"], len(T))
    if "seffaf" in a.gizle and "seffaf" in ad: continue
    P = X[T]
    msk &= ((P[..., 0] > k[0]) & (P[..., 0] < k[1]) & (P[..., 1] > k[2]) & (P[..., 1] < k[3]) & (P[..., 2] > k[4]) & (P[..., 2] < k[5])).all(axis=1)
    if not msk.any(): continue
    if ad in SEG:
        L = SEG[ad]
        for p in sorted(set(L[msk])):
            gad = ad + "|" + p
            if any(s in gad for s in haric): continue
            ciz(gad, X, T[msk & (L == p)])
    else:
        if any(s in ad for s in haric): continue
        ciz(ad, X, T[msk])
cam = ren.GetActiveCamera()
hd = [float(v) for v in a.hedef.split(",")] if a.hedef else [(k[0] + k[1]) / 2, (k[2] + k[3]) / 2, (k[4] + k[5]) / 2]
e = [float(v) for v in a.kam.split(",")]
cam.SetFocalPoint(*hd); cam.SetPosition(*e); cam.SetViewUp(*[float(v) for v in a.yukari.split(",")])
if a.olcek: cam.ParallelProjectionOn(); cam.SetParallelScale(a.olcek)
ren.ResetCameraClippingRange()
w, hgt = [int(v) for v in a.boy.split(",")]
rw = vtk.vtkRenderWindow(); rw.SetOffScreenRendering(1); rw.AddRenderer(ren); rw.SetSize(w, hgt); rw.Render()
wi = vtk.vtkWindowToImageFilter(); wi.SetInput(rw); wi.Update()
pw = vtk.vtkPNGWriter(); pw.SetFileName(a.out); pw.SetInputConnection(wi.GetOutputPort()); pw.Write()
print("ok", a.out)
