# -*- coding: utf-8 -*-
"""python ciz2.py model.glb out.jpg x0 x1 y0 y1 z0 z1 cam(ax,ay,az) [vurgu_re] [soluk 0..1] [kpkgizle 0/1] [olcek]
GLB malzeme renkleri · kutu ile gerçek kırpma (vtkBox) · vurgu_re dışındakiler 'soluk' saydamlıkta (1 = normal)."""
import sys, re, numpy as np
sys.path.insert(0, r"@@KOK_W@@\gece")
from m8kit import Glb
import vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
a = sys.argv
g = Glb(a[1]); out = a[2]; K = [float(v) for v in a[3:9]]; cam = np.array([float(v) for v in a[9].split(",")])
vur = a[10] if len(a) > 10 and a[10] != "-" else None
sol = float(a[11]) if len(a) > 11 else 1.0
kpkg = len(a) > 12 and a[12] == "1"
olc = float(a[13]) if len(a) > 13 else 0.42
lo = np.array(K[0::2]); hi = np.array(K[1::2])
ren = vtk.vtkRenderer(); ren.SetBackground(1, 1, 1)
box = vtk.vtkBox(); box.SetBounds(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
J = g.J
for p in g.prims:
    if p.get("gizli") or re.search(r"^(INSAN|ZEMIN)", p["name"]): continue
    T = p["T"]; vis = (T[:, 0] != T[:, 1]) & (T[:, 1] != T[:, 2])
    if kpkg: vis &= ~g.kpk_maske(p)
    P = p["X"][T[vis]]
    if not len(P): continue
    m = np.all(P.max(1) >= lo, 1) & np.all(P.min(1) <= hi, 1); P = P[m]
    if not len(P): continue
    # kutu sınırını kesen büyük üçgenleri böl (kırpma köşe değerleriyle yapılır)
    for _ in range(8):
        L = np.max(np.linalg.norm(P - P[:, [1, 2, 0]], axis=2), axis=1)
        ic = np.all(P.min(1) >= lo, 1) & np.all(P.max(1) <= hi, 1)
        b = (L > 40.0) & ~ic
        if not b.any() or len(P) > 3_000_000: break
        Q = P[b]; a, bb, c = Q[:, 0], Q[:, 1], Q[:, 2]; ab = (a + bb) / 2; bc = (bb + c) / 2; ca = (c + a) / 2
        P = np.concatenate([P[~b], np.stack([a, ab, ca], 1), np.stack([ab, bb, bc], 1), np.stack([ca, bc, c], 1), np.stack([ab, bc, ca], 1)])
        m = np.all(P.max(1) >= lo, 1) & np.all(P.min(1) <= hi, 1); P = P[m]
    V = P.reshape(-1, 3); n = len(P)
    pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(V.astype(np.float64), deep=True))
    cells = np.hstack([np.full((n, 1), 3), np.arange(3 * n).reshape(-1, 3)]).astype(np.int64).ravel()
    ca = vtk.vtkCellArray(); ca.SetCells(n, numpy_to_vtkIdTypeArray(cells, deep=True))
    pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(ca)
    cl = vtk.vtkCleanPolyData(); cl.SetInputData(pd); cl.SetTolerance(1e-6)
    cp = vtk.vtkClipPolyData(); cp.SetInputConnection(cl.GetOutputPort()); cp.SetClipFunction(box); cp.InsideOutOn(); cp.Update()
    mi = p["pr"].get("material"); mat = J["materials"][mi] if mi is not None else {}
    col = mat.get("pbrMetallicRoughness", {}).get("baseColorFactor", [0.7, 0.7, 0.7, 1])
    mp = vtk.vtkPolyDataMapper(); mp.SetInputConnection(cp.GetOutputPort()); mp.ScalarVisibilityOff()
    ac = vtk.vtkActor(); ac.SetMapper(mp); ac.GetProperty().SetColor(*col[:3])
    op = col[3] if len(col) > 3 else 1.0
    if vur and not re.search(vur, p["name"]): op = min(op, sol)
    ac.GetProperty().SetOpacity(op)
    ren.AddActor(ac)
    if op > 0.5:
        fe = vtk.vtkFeatureEdges(); fe.SetInputConnection(cp.GetOutputPort()); fe.BoundaryEdgesOff(); fe.FeatureEdgesOn(); fe.SetFeatureAngle(35); fe.ManifoldEdgesOff(); fe.NonManifoldEdgesOff()
        m2 = vtk.vtkPolyDataMapper(); m2.SetInputConnection(fe.GetOutputPort()); m2.ScalarVisibilityOff()
        a2 = vtk.vtkActor(); a2.SetMapper(m2); a2.GetProperty().SetColor(0.1, 0.1, 0.1); a2.GetProperty().SetLineWidth(1); ren.AddActor(a2)
c = (lo + hi) / 2; dmax = np.linalg.norm(hi - lo)
cm = ren.GetActiveCamera(); cm.SetFocalPoint(*c); cm.SetPosition(*(c + cam / np.linalg.norm(cam) * dmax * 2.0))
cm.SetViewUp(0, 1, 0) if abs(cam[1]) / np.linalg.norm(cam) < 0.95 else cm.SetViewUp(0, 0, -1)
cm.ParallelProjectionOn(); cm.SetParallelScale(dmax * olc)
ren.ResetCameraClippingRange()
ren.TwoSidedLightingOn()
rw = vtk.vtkRenderWindow(); rw.SetOffScreenRendering(1); rw.AddRenderer(ren); rw.SetSize(1600, 1100); rw.Render()
w2i = vtk.vtkWindowToImageFilter(); w2i.SetInput(rw); w2i.Update()
wr = vtk.vtkJPEGWriter(); wr.SetFileName(out); wr.SetInputConnection(w2i.GetOutputPort()); wr.SetQuality(90); wr.Write()
print("yazildi", out)
