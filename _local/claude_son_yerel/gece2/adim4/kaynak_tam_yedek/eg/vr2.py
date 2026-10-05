# python eg/vr2.py glb out.png F E katlar(virgül, boş=hepsi) [vurgu_regex] [mekler]
import sys, re, numpy as np, vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
sys.path.insert(0,"tg"); from glbx import yukle
glb,out=sys.argv[1],sys.argv[2]
F=[float(v) for v in sys.argv[3].split(",")]; E=[float(v) for v in sys.argv[4].split(",")]
KAT=set(int(v) for v in sys.argv[5].split(",")) if len(sys.argv)>5 and sys.argv[5] else None
vr=re.compile(sys.argv[6]) if len(sys.argv)>6 and sys.argv[6] else None
MEK=set(int(v) for v in sys.argv[7].split(",")) if len(sys.argv)>7 and sys.argv[7] else {40,43,50,51,52,53,54,55}
J,D=yukle(glb)
def lab(ex,k,n,dflt=-1):
    a=np.full(n,dflt); r=ex.get(k)
    if r:
        for i in range(0,len(r),3): a[r[i+1]//3:(r[i+1]+r[i+2])//3]=r[i]
    return a
ren=vtk.vtkRenderer(); ren.SetBackground(0.08,0.09,0.1)
pal={"on_seffaf":(0.6,0.78,0.95),"kabuk":(0.78,0.8,0.83),"sac":(0.72,0.74,0.78),"celik":(0.85,0.55,0.2),"plastik":(0.3,0.6,0.3),"sensor":(0.2,0.4,0.95),"motor":(0.35,0.35,0.4),"aluminyum":(0.65,0.65,0.7),"uhmw":(0.97,0.97,0.97),"paslanmaz":(0.55,0.6,0.65)}
for nd,d in D.items():
    X,T,ok,ex=d["X"],d["T"],d["ok"],d["ex"]
    if d["rot"]: continue
    n=len(T); mk=lab(ex,"mek",n); kt=lab(ex,"kat",n)
    sel=ok & np.isin(mk,list(MEK))
    if KAT is not None: sel&=np.isin(kt,list(KAT))
    if not sel.any(): continue
    P=X[T[sel]]
    pts=vtk.vtkPoints(); pts.SetData(numpy_to_vtk(P.reshape(-1,3).astype(float),deep=1))
    m=len(P); cells=np.hstack([np.full((m,1),3),np.arange(3*m).reshape(-1,3)]).astype(np.int64).ravel()
    ca=vtk.vtkCellArray(); ca.SetCells(m,numpy_to_vtkIdTypeArray(cells,deep=1))
    pd=vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(ca)
    mp=vtk.vtkPolyDataMapper(); mp.SetInputData(pd); a=vtk.vtkActor(); a.SetMapper(mp)
    c=(0.5,0.5,0.5)
    for k,v in pal.items():
        if k in nd.lower(): c=v
    if vr and vr.search(nd): c=(1.0,0.1,0.6)
    a.GetProperty().SetColor(*c); a.GetProperty().EdgeVisibilityOn(); a.GetProperty().SetEdgeColor(0.1,0.1,0.1)
    ren.AddActor(a)
cam=ren.GetActiveCamera(); cam.SetFocalPoint(*F); cam.SetPosition(*E); cam.SetViewUp(0,1,0); cam.SetViewAngle(35); ren.ResetCameraClippingRange()
rw=vtk.vtkRenderWindow(); rw.SetOffScreenRendering(1); rw.AddRenderer(ren); rw.SetSize(1100,1000); rw.Render()
w=vtk.vtkWindowToImageFilter(); w.SetInput(rw); w.Update()
pw=vtk.vtkPNGWriter(); pw.SetFileName(out); pw.SetInputConnection(w.GetOutputPort()); pw.Write(); print(out)
import os; sys.stdout.flush(); os._exit(0)
