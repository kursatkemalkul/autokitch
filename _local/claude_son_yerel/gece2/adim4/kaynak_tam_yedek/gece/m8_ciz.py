# -*- coding: utf-8 -*-
"""Bolge goruntusu (VTK ekran disi): python m8_ciz.py model.glb cikti.jpg x0 x1 y0 y1 z0 z1 kamera(ax,ay,az) [vurgu_desen] [gizle_desen]
kamera = bakis yonu (bolge merkezinden kameraya). Dugum adina gore renk; vurgu_desen eslesen dugumler turuncu."""
import sys, os, re, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m8kit import Glb
import vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray

g = Glb(sys.argv[1]); out = sys.argv[2]
K = [float(v) for v in sys.argv[3:9]]; cam = np.array([float(v) for v in sys.argv[9].split(",")])
vur = sys.argv[10] if len(sys.argv) > 10 and sys.argv[10] != "-" else None
giz = sys.argv[11] if len(sys.argv) > 11 else r"^(INSAN|ROBOT|ZEMIN|URUN)|__on_seffaf|__cam_kapak|KAPAK__seffaf"
RENK = [("kablo_veri", (0.20, 0.45, 0.85)), ("kablo", (0.15, 0.15, 0.15)), ("hava", (0.25, 0.65, 0.95)), ("hortum", (0.3, 0.6, 0.3)),
        ("pu", (0.95, 0.9, 0.55)), ("kanal", (0.55, 0.55, 0.6)), ("rakor", (0.2, 0.2, 0.2)), ("conta", (0.1, 0.1, 0.1)), ("bakir", (0.8, 0.5, 0.25)),
        ("celik", (0.5, 0.52, 0.55)), ("paslanmaz", (0.78, 0.8, 0.82)), ("sac", (0.72, 0.74, 0.77)), ("aluminyum", (0.82, 0.84, 0.86)),
        ("koyu", (0.25, 0.25, 0.25)), ("siyah", (0.1, 0.1, 0.1)), ("pom", (0.95, 0.95, 0.92)), ("cam", (0.75, 0.88, 0.95))]
ren = vtk.vtkRenderer(); ren.SetBackground(1, 1, 1)
lo = np.array(K[0::2]); hi = np.array(K[1::2])
for p in g.prims:
    if p.get("gizli") or re.search(giz, p["name"]): continue
    T = p["T"]; vis = (T[:, 0] != T[:, 1]) & (T[:, 1] != T[:, 2])
    P = p["X"][T[vis]]
    for ek in (p.get("ekX") or []): P = np.concatenate([P, ek.reshape(-1, 3, 3)])
    if not len(P): continue
    m = np.all(P.max(1) >= lo, 1) & np.all(P.min(1) <= hi, 1)
    P = P[m]
    if not len(P): continue
    V = P.reshape(-1, 3); n = len(P)
    pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(V.astype(np.float64), deep=True))
    cells = np.hstack([np.full((n, 1), 3), np.arange(3 * n).reshape(-1, 3)]).astype(np.int64).ravel()
    ca = vtk.vtkCellArray(); ca.SetCells(n, numpy_to_vtkIdTypeArray(cells, deep=True))
    pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(ca)
    mp = vtk.vtkPolyDataMapper(); mp.SetInputData(pd)
    a = vtk.vtkActor(); a.SetMapper(mp)
    mal = p["name"].split("__")[1] if "__" in p["name"] else p["name"]
    c = (0.7, 0.7, 0.7)
    for k, v in RENK:
        if k in mal.lower(): c = v; break
    if vur and re.search(vur, p["name"]): c = (1.0, 0.45, 0.05)
    a.GetProperty().SetColor(*c)
    fe = vtk.vtkFeatureEdges(); fe.SetInputData(pd); fe.BoundaryEdgesOn(); fe.FeatureEdgesOn(); fe.SetFeatureAngle(35); fe.ManifoldEdgesOff(); fe.NonManifoldEdgesOff()
    m2 = vtk.vtkPolyDataMapper(); m2.SetInputConnection(fe.GetOutputPort()); m2.ScalarVisibilityOff()
    a2 = vtk.vtkActor(); a2.SetMapper(m2); a2.GetProperty().SetColor(0, 0, 0); a2.GetProperty().SetLineWidth(1)
    ren.AddActor(a); ren.AddActor(a2)
c = (lo + hi) / 2; dmax = np.linalg.norm(hi - lo)
cm = ren.GetActiveCamera(); cm.SetFocalPoint(*c); cm.SetPosition(*(c + cam / np.linalg.norm(cam) * dmax * 1.6)); cm.SetViewUp(0, 1, 0)
cm.SetViewAngle(30); ren.ResetCameraClippingRange()
rw = vtk.vtkRenderWindow(); rw.SetOffScreenRendering(1); rw.AddRenderer(ren); rw.SetSize(1400, 1000); rw.Render()
w2i = vtk.vtkWindowToImageFilter(); w2i.SetInput(rw); w2i.Update()
wr = vtk.vtkJPEGWriter(); wr.SetFileName(out); wr.SetInputConnection(w2i.GetOutputPort()); wr.SetQuality(90); wr.Write()
print("yazildi", out)
