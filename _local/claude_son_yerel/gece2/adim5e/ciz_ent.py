# -*- coding: utf-8 -*-
"""ent_*.jpg: VTK ekran dışı çizim · python ciz_ent.py model.glb cikti_klasoru"""
import sys, os, json, struct, numpy as np, vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
gl, cik = sys.argv[1:3]
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
raw = open(gl, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]
def acc(i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]; n = {"SCALAR": 1, "VEC3": 3}[a["type"]]; dt = TD[a["componentType"]]
    o = v.get("byteOffset", 0) + a.get("byteOffset", 0); r = np.frombuffer(BIN[o:o + a["count"] * n * np.dtype(dt).itemsize], dt)
    return r.reshape(-1, n) if n > 1 else r
GRUP = []   # (P (n,3,3) mm, renk, kpk maske)
for nd in J["nodes"]:
    if "mesh" not in nd: continue
    ad = nd.get("name", "")
    t = np.array(nd.get("translation", [0, 0, 0]))
    for pr in J["meshes"][nd["mesh"]]["primitives"]:
        if "POSITION" not in pr.get("attributes", {}): continue
        X = (acc(pr["attributes"]["POSITION"]).astype(float) + t) * 1000.0; T = acc(pr["indices"]).reshape(-1, 3).astype(np.int64)
        ok = (T[:, 0] != T[:, 1]) & (T[:, 1] != T[:, 2])
        m = np.zeros(len(T), bool); k = pr.get("extras", {}).get("kpk") or []
        for i in range(0, len(k) - 1, 2): m[k[i] // 3:(k[i] + k[i + 1]) // 3] = True
        mat = J["materials"][pr["material"]]; c = mat.get("pbrMetallicRoughness", {}).get("baseColorFactor", [0.7, 0.7, 0.7, 1])
        GRUP.append((ad, X[T[ok]], np.array(c[:3]), m[ok], c[3] if len(c) > 3 else 1.0))


def ciz(yol, sec, kam, odak, yukari=(0, 1, 0), boy=(1600, 1000), kapaksiz=False):
    ren = vtk.vtkRenderer(); ren.SetBackground(1, 1, 1)
    for ad, P, c, kp, al in GRUP:
        if re.search(r"__pu$|__yalitim|ZEMIN|INSAN|DUKKAN", ad) or al < 0.05: continue
        m = sec(P)
        if kapaksiz: m &= ~kp
        if not m.any(): continue
        Q = P[m].reshape(-1, 3); n = len(Q) // 3
        pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(Q.astype(np.float32), deep=True))
        cel = np.c_[np.full(n, 3), np.arange(3 * n).reshape(-1, 3)].astype(np.int64).ravel()
        ca = vtk.vtkCellArray(); ca.SetCells(n, numpy_to_vtkIdTypeArray(cel, deep=True))
        pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(ca)
        mp = vtk.vtkPolyDataMapper(); mp.SetInputData(pd)
        a = vtk.vtkActor(); a.SetMapper(mp); a.GetProperty().SetColor(*np.clip(c, 0.05, 1)); a.GetProperty().SetOpacity(min(1.0, max(al, 0.35)))
        a.GetProperty().SetInterpolationToFlat(); ren.AddActor(a)
    cam = ren.GetActiveCamera(); cam.SetPosition(*kam); cam.SetFocalPoint(*odak); cam.SetViewUp(*yukari); ren.ResetCameraClippingRange()
    cam.SetViewAngle(30)
    rw = vtk.vtkRenderWindow(); rw.SetOffScreenRendering(1); rw.AddRenderer(ren); rw.SetSize(*boy); rw.Render()
    w = vtk.vtkWindowToImageFilter(); w.SetInput(rw); w.Update()
    wr = vtk.vtkJPEGWriter(); wr.SetFileName(yol); wr.SetInputConnection(w.GetOutputPort()); wr.SetQuality(88); wr.Write()
    print("yazıldı", yol, flush=True)


import re
os.makedirs(cik, exist_ok=True)
hep = lambda P: np.ones(len(P), bool)
ciz(os.path.join(cik, "ent_makine_genel.jpg"), hep, (2600, 2600, 6200), (2900, 1000, -380))
IST = {"A": (736, 1436), "B": (736, 4400), "TOPPING": (1436, 2500), "F": (2500, 4000), "E": (4400, 5230), "U": (2500, 5230)}
for k, (x0, x1) in IST.items():
    yb = {"B": (0, 790), "U": (1862, 2210), "F": (788, 2210)}.get(k, (0, 2210))
    def sec(P, x0=x0, x1=x1, yb=yb):
        c = P.mean(1); return (c[:, 0] > x0 - 1) & (c[:, 0] < x1 + 1) & (c[:, 1] > yb[0] - 1) & (c[:, 1] < yb[1] + 1)
    cx = (x0 + x1) / 2; cy = (yb[0] + min(yb[1], 2200)) / 2; L = max(x1 - x0, yb[1] - yb[0], 900)
    ciz(os.path.join(cik, "ent_%s_kapaksiz.jpg" % k), sec, (cx + 0.55 * L, cy + 0.45 * L, 1.55 * L), (cx, cy, -380), kapaksiz=True)
os._exit(0)
