# -*- coding: utf-8 -*-
"""Hızlı içinde/dışında: kapalı yüzey (VTK vtkSelectEnclosedPoints, C++ döngü) · OCC katısından ya da üçgen ağından."""
import numpy as np, vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy


def yuzey_ag(X, T):
    pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(np.ascontiguousarray(X, dtype=np.float64), deep=1))
    cells = vtk.vtkCellArray(); ids = np.hstack([np.full((len(T), 1), 3), T]).astype(np.int64).ravel()
    cells.SetCells(len(T), numpy_to_vtkIdTypeArray(ids, deep=1))
    pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(cells)
    cl = vtk.vtkCleanPolyData(); cl.SetInputData(pd); cl.SetTolerance(0.0); cl.SetAbsoluteTolerance(1e-4); cl.ToleranceIsAbsoluteOn(); cl.Update()
    return cl.GetOutput()


def yuzey_kati(s, tol=0.05):
    V, T = s.tessellate(tol, 0.2)
    X = np.array([[v.x, v.y, v.z] for v in V]); T = np.array(T, np.int64)
    return yuzey_ag(X, T)


def ic_maske(yuzey, P):
    if not len(P): return np.zeros(0, bool)
    pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(np.ascontiguousarray(P, dtype=np.float64), deep=1))
    pd = vtk.vtkPolyData(); pd.SetPoints(pts)
    se = vtk.vtkSelectEnclosedPoints(); se.SetInputData(pd); se.SetSurfaceData(yuzey); se.SetTolerance(1e-7); se.CheckSurfaceOff(); se.Update()
    return vtk_to_numpy(se.GetOutput().GetPointData().GetArray("SelectedPoints")).astype(bool)
