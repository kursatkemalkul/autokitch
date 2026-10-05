# -*- coding: utf-8 -*-
"""Üçgen ağ → OCC katı (dikiş + düzlem birleştirme)"""
import numpy as np
import cadquery as cq
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid
from OCP.gp import gp_Pnt
from OCP.TopoDS import TopoDS
from OCP.TopAbs import TopAbs_SHELL
from OCP.TopExp import TopExp_Explorer
from OCP.ShapeUpgrade import ShapeUpgrade_UnifySameDomain
from OCP.ShapeFix import ShapeFix_Solid


def kati(X, T, tol=1e-3, birlestir=True):
    sw = BRepBuilderAPI_Sewing(tol)
    for t in T:
        p = X[t]
        if np.linalg.norm(np.cross(p[1] - p[0], p[2] - p[0])) < 1e-9: continue
        mp = BRepBuilderAPI_MakePolygon(gp_Pnt(*p[0]), gp_Pnt(*p[1]), gp_Pnt(*p[2]), True)
        f = BRepBuilderAPI_MakeFace(mp.Wire(), True)
        if f.IsDone(): sw.Add(f.Face())
    sw.Perform()
    sh = sw.SewedShape()
    ex = TopExp_Explorer(sh, TopAbs_SHELL); sol = []
    while ex.More():
        ms = BRepBuilderAPI_MakeSolid(TopoDS.Shell_s(ex.Current()))
        fx = ShapeFix_Solid(ms.Solid()); fx.Perform()
        s = fx.Solid()
        if birlestir:
            u = ShapeUpgrade_UnifySameDomain(s, True, True, False); u.Build(); s = u.Shape()
        sol.append(cq.Shape.cast(s))
        ex.Next()
    return sol
