# -*- coding: utf-8 -*-
"""python ciz.py model.glb out.jpg x0 x1 y0 y1 z0 z1 cam(ax,ay,az) [dahil_re|-] [haric_re|-] [vurgu_re|-] [orto 0/1] [kpkgizle 0/1]
Ucgen agirlik merkezi kutu icinde olanlar cizilir (buyuk zemin ucgenleri tasmaz)."""
import sys, os, re, numpy as np
from _env import *
from m8kit import Glb
import vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
a=sys.argv
g = Glb(a[1]) if not a[1].endswith(".pkl") else None
out=a[2]; K=[float(v) for v in a[3:9]]; cam=np.array([float(v) for v in a[9].split(",")])
dah=a[10] if len(a)>10 and a[10]!="-" else None
har=a[11] if len(a)>11 and a[11]!="-" else r"^(INSAN|ZEMIN)"
vur=a[12] if len(a)>12 and a[12]!="-" else None
orto=len(a)>13 and a[13]=="1"
kpkg=len(a)>14 and a[14]=="1"
RENK = [("kablo_veri", (0.20, 0.45, 0.85)), ("kablo", (0.15, 0.15, 0.15)), ("hava", (0.25, 0.65, 0.95)), ("hortum", (0.3, 0.6, 0.3)),
        ("pu", (0.95, 0.9, 0.55)), ("kanal", (0.55, 0.55, 0.6)), ("rakor", (0.25, 0.25, 0.25)), ("conta", (0.1, 0.1, 0.1)), ("bakir", (0.8, 0.5, 0.25)),
        ("seffaf",(0.6,0.75,0.85)),("celik", (0.5, 0.52, 0.55)), ("paslanmaz", (0.8, 0.82, 0.84)), ("sac", (0.74, 0.76, 0.79)), ("aluminyum", (0.86, 0.87, 0.89)),
        ("koyu", (0.25, 0.25, 0.25)), ("siyah", (0.1, 0.1, 0.1)), ("pom", (0.95, 0.95, 0.92)), ("cam", (0.75, 0.88, 0.95)),("motor",(0.35,0.35,0.4)),("robot_kutu",(0.95,0.6,0.2)),("plastik",(0.35,0.35,0.38)),("ups",(0.3,0.3,0.32))]
ren = vtk.vtkRenderer(); ren.SetBackground(1, 1, 1)
lo = np.array(K[0::2]); hi = np.array(K[1::2])
for p in g.prims:
    if p.get("gizli") or re.search(har, p["name"]): continue
    if dah and not re.search(dah,p["name"]): continue
    T = p["T"]; vis = (T[:, 0] != T[:, 1]) & (T[:, 1] != T[:, 2])
    if kpkg: vis &= ~g.kpk_maske(p)
    P = p["X"][T[vis]]
    for ek in (p.get("ekX") or []): P = np.concatenate([P, ek.reshape(-1, 3, 3)])
    if not len(P): continue
    c=P.mean(1); m = np.all(c >= lo, 1) & np.all(c <= hi, 1)
    P = P[m]
    if not len(P): continue
    V = P.reshape(-1, 3); n = len(P)
    pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(V.astype(np.float64), deep=True))
    cells = np.hstack([np.full((n, 1), 3), np.arange(3 * n).reshape(-1, 3)]).astype(np.int64).ravel()
    ca = vtk.vtkCellArray(); ca.SetCells(n, numpy_to_vtkIdTypeArray(cells, deep=True))
    pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(ca)
    cl=vtk.vtkCleanPolyData(); cl.SetInputData(pd); cl.SetTolerance(1e-6); cl.Update()
    mp = vtk.vtkPolyDataMapper(); mp.SetInputConnection(cl.GetOutputPort())
    ac = vtk.vtkActor(); ac.SetMapper(mp)
    mal = p["name"].split("__")[1] if "__" in p["name"] else p["name"]
    col = (0.7, 0.7, 0.7)
    for k, v in RENK:
        if k in mal.lower(): col = v; break
    if vur and re.search(vur, p["name"]): col = (1.0, 0.45, 0.05)
    ac.GetProperty().SetColor(*col)
    if "seffaf" in mal: ac.GetProperty().SetOpacity(0.35)
    fe = vtk.vtkFeatureEdges(); fe.SetInputConnection(cl.GetOutputPort()); fe.BoundaryEdgesOn(); fe.FeatureEdgesOn(); fe.SetFeatureAngle(35); fe.ManifoldEdgesOff(); fe.NonManifoldEdgesOff()
    m2 = vtk.vtkPolyDataMapper(); m2.SetInputConnection(fe.GetOutputPort()); m2.ScalarVisibilityOff()
    a2 = vtk.vtkActor(); a2.SetMapper(m2); a2.GetProperty().SetColor(0, 0, 0); a2.GetProperty().SetLineWidth(1)
    ren.AddActor(ac); ren.AddActor(a2)
c = (lo + hi) / 2; dmax = np.linalg.norm(hi - lo)
cm = ren.GetActiveCamera(); cm.SetFocalPoint(*c); cm.SetPosition(*(c + cam / np.linalg.norm(cam) * dmax * 1.6))
cm.SetViewUp(0, 1, 0) if abs(cam[1])/np.linalg.norm(cam)<0.95 else cm.SetViewUp(0,0,-1)
cm.SetViewAngle(30)
if orto:
    cm.ParallelProjectionOn(); cm.SetParallelScale(dmax*0.4)
ren.ResetCameraClippingRange()
rw = vtk.vtkRenderWindow(); rw.SetOffScreenRendering(1); rw.AddRenderer(ren); rw.SetSize(1400, 1000); rw.Render()
w2i = vtk.vtkWindowToImageFilter(); w2i.SetInput(rw); w2i.Update()
wr = vtk.vtkJPEGWriter(); wr.SetFileName(out); wr.SetInputConnection(w2i.GetOutputPort()); wr.SetQuality(90); wr.Write()
print("yazildi", out)
