# -*- coding: utf-8 -*-
"""TOPPING PU GÖRÜNÜRLÜK DENETİMİ (görüntü): yalnız TOPPING düğümleri, ışıksız düz renk · PU üçgenleri KIRMIZI, diğerleri gri ·
6 dik görünüş (ön kapaklar gizli · ön kapaklar opak · arka · üst · alt · sol · sağ) → kırmızı piksel sayısı 0 olmalı.
Kullanım: python topping_pu_gorunur.py hat3_v8o.glb hat3_v8n.glb cikti_klasoru"""
import os, sys, json
import numpy as np, vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "tg"))
from glbx import yukle, aralik_maske

g1, g0, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
J1, D1 = yukle(g1); J0, D0 = yukle(g0)
DZ = json.load(open(os.path.join(HERE, "tg", "cikti", "yeni_dizin.json"), encoding="utf-8"))
say, pu_tri = {}, {}
for nd, ad, bb, ntri in DZ["rapor"]["yeni"]:
    b = say.get(nd, len(D0[nd]["T"])); say[nd] = b + ntri
    if "PU" in ad or ad.endswith("_pu"): pu_tri.setdefault(nd, []).append((b, b + ntri))


def sahne(gizle_kpk):
    ren = vtk.vtkRenderer(); ren.SetBackground(0, 0, 0)
    for nd, d in D1.items():
        if not (nd.startswith("TOPPING") or nd.startswith("ELK_TOPPING")): continue
        X, T = d["X"], d["T"]; m = d["ok"].copy()
        if gizle_kpk and d["ex"].get("kpk"): m &= ~aralik_maske(d["ex"]["kpk"], len(T))
        pu = np.zeros(len(T), bool)
        if nd in ("TOPPING_MODUL__pu", "TOPPING_MODUL__yalitim_gorunur"): pu[:] = True
        for a, b in pu_tri.get(nd, []): pu[a:b] = True
        for flag, col in ((False, (0.5, 0.5, 0.5)), (True, (1.0, 0.0, 0.0))):
            TT = T[m & (pu == flag)]
            if not len(TT): continue
            pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(np.ascontiguousarray(X, dtype=np.float64), deep=1))
            cells = vtk.vtkCellArray(); ids = np.hstack([np.full((len(TT), 1), 3), TT]).astype(np.int64).ravel()
            cells.SetCells(len(TT), numpy_to_vtkIdTypeArray(ids, deep=1))
            pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(cells)
            mp = vtk.vtkPolyDataMapper(); mp.SetInputData(pd); ac = vtk.vtkActor(); ac.SetMapper(mp)
            p = ac.GetProperty(); p.SetColor(*col); p.SetLighting(False); p.SetAmbient(1.0); p.SetDiffuse(0.0)
            ren.AddActor(ac)
    return ren


GOR = [("on_kapak_gizli", True, (1968, 1500, 4000), (0, 1, 0)), ("on_kapak_opak", False, (1968, 1500, 4000), (0, 1, 0)),
       ("arka", False, (1968, 1500, -4000), (0, 1, 0)), ("ust", True, (1968, 5000, -400), (0, 0, -1)), ("alt", True, (1968, -3000, -400), (0, 0, -1)),
       ("sol", True, (-1000, 1500, -400), (0, 1, 0)), ("sag", True, (5000, 1500, -400), (0, 1, 0))]
sonuc = {}
for ad, gz, kam, yuk in GOR:
    ren = sahne(gz); cam = ren.GetActiveCamera()
    cam.SetFocalPoint(1968, 1500, -400); cam.SetPosition(*kam); cam.SetViewUp(*yuk); cam.ParallelProjectionOn(); cam.SetParallelScale(760)
    ren.ResetCameraClippingRange()
    rw = vtk.vtkRenderWindow(); rw.SetOffScreenRendering(1); rw.AddRenderer(ren); rw.SetSize(1400, 1400); rw.Render()
    wi = vtk.vtkWindowToImageFilter(); wi.SetInput(rw); wi.Update()
    img = vtk_to_numpy(wi.GetOutput().GetPointData().GetScalars()).reshape(1400, 1400, -1)
    kir = int(((img[..., 0] > 200) & (img[..., 1] < 60) & (img[..., 2] < 60)).sum())
    pw = vtk.vtkPNGWriter(); pw.SetFileName(os.path.join(OUT, "pu_%s.png" % ad)); pw.SetInputConnection(wi.GetOutputPort()); pw.Write()
    sonuc[ad] = kir; print("  %-16s kırmızı (PU) piksel: %d" % (ad, kir))
print("PU GÖRÜNÜRLÜK: %s" % ("TEMİZ" if not any(sonuc.values()) else "BULGU"))
json.dump(sonuc, open(os.path.join(OUT, "pu_gorunur.json"), "w"), indent=1)
os._exit(0)
