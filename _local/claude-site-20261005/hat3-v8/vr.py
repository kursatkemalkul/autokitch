# python eg/vr.py glb out.png "fx,fy,fz" "ex,ey,ez" [haric_regex] [dahil_regex] [vurgu_regex] [clip lo] [clip hi]
import sys, re, numpy as np, vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
sys.path.insert(0,"."); import govde_denetim_dogru as GD
glb,out=sys.argv[1],sys.argv[2]
F=[float(v) for v in sys.argv[3].split(",")]; E=[float(v) for v in sys.argv[4].split(",")]
g=lambda i: sys.argv[i] if len(sys.argv)>i and sys.argv[i] else None
hr=re.compile(g(5)) if g(5) else None; dr=re.compile(g(6)) if g(6) else None; vr=re.compile(g(7)) if g(7) else None
clo=np.array([float(v) for v in g(8).split(",")]) if g(8) else None; chi=np.array([float(v) for v in g(9).split(",")]) if g(9) else None
D=GD.glb_oku(glb)
ren=vtk.vtkRenderer(); ren.SetBackground(0.08,0.09,0.1)
pal={"on_seffaf":(0.6,0.78,0.95),"kabuk":(0.78,0.8,0.83),"sac":(0.72,0.74,0.78),"celik":(0.85,0.55,0.2),"plastik":(0.3,0.6,0.3),"sensor":(0.2,0.4,0.95),"motor":(0.35,0.35,0.4),"kablo":(0.9,0.2,0.2),"kanal":(0.9,0.8,0.1),"aluminyum":(0.65,0.65,0.7),"uhmw":(0.97,0.97,0.97),"paslanmaz":(0.55,0.6,0.65)}
for nd,P in D.items():
    if not len(P): continue
    if hr and hr.search(nd): continue
    if dr and not dr.search(nd): continue
    if clo is not None:
        m=((P.max(1)>clo)&(P.min(1)<chi)).all(1); P=P[m]
        if not len(P): continue
    pts=vtk.vtkPoints(); pts.SetData(numpy_to_vtk(P.reshape(-1,3).astype(float),deep=1))
    n=len(P); cells=np.hstack([np.full((n,1),3),np.arange(3*n).reshape(-1,3)]).astype(np.int64).ravel()
    ca=vtk.vtkCellArray(); ca.SetCells(n,numpy_to_vtkIdTypeArray(cells,deep=1))
    pd=vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(ca)
    mp=vtk.vtkPolyDataMapper(); mp.SetInputData(pd)
    a=vtk.vtkActor(); a.SetMapper(mp)
    c=(0.5,0.5,0.5)
    for k,v in pal.items():
        if k in nd.lower(): c=v
    if not nd.startswith("E_"): c=tuple(0.55*x+0.35 for x in c)
    if vr and vr.search(nd): c=(1.0,0.1,0.6)
    a.GetProperty().SetColor(*c)
    a.GetProperty().EdgeVisibilityOn(); a.GetProperty().SetEdgeColor(0.1,0.1,0.1); a.GetProperty().SetLineWidth(0.5)
    if "on_seffaf" in nd: a.GetProperty().SetOpacity(0.35)
    ren.AddActor(a)
cam=ren.GetActiveCamera(); cam.SetFocalPoint(*F); cam.SetPosition(*E); cam.SetViewUp(0,1,0); cam.SetViewAngle(35)
ren.ResetCameraClippingRange()
rw=vtk.vtkRenderWindow(); rw.SetOffScreenRendering(1); rw.AddRenderer(ren); rw.SetSize(1100,1000); rw.Render()
w=vtk.vtkWindowToImageFilter(); w.SetInput(rw); w.Update()
pw=vtk.vtkPNGWriter(); pw.SetFileName(out); pw.SetInputConnection(w.GetOutputPort()); pw.Write(); print(out)
import os; sys.stdout.flush(); os._exit(0)
