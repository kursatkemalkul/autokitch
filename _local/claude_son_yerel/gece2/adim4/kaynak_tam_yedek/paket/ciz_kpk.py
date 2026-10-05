# -*- coding: utf-8 -*-
"""npz onbellekten bolge goruntusu (ucgen agirlik merkezi kutu icinde). python ciz.py dizin out.jpg x0 x1 y0 y1 z0 z1 ax,ay,az [vurgu_mek,..] [orto]"""
import sys, json, numpy as np, vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
d=sys.argv[1]; out=sys.argv[2]; K=[float(v) for v in sys.argv[3:9]]; cam=np.array([float(v) for v in sys.argv[9].split(',')])
vur=set(int(v) for v in sys.argv[10].split(',')) if len(sys.argv)>10 and sys.argv[10]!='-' else set()
orto=len(sys.argv)>11
D=np.load(d+'/m8_onbellek.npz'); PJ=json.load(open(d+'/m8_parca.json',encoding='utf-8'))['parca']
A,B,C,P,mek=D['A'],D['B'],D['C'],D['P'],D['mek']
lo=np.array(K[0::2]); hi=np.array(K[1::2]); c=(A+B+C)/3
m=np.all(c>=lo,1)&np.all(c<=hi,1)
RENK=[("kablo_veri",(0.20,0.45,0.85)),("kablo",(0.15,0.15,0.15)),("hava",(0.25,0.65,0.95)),("hortum",(0.3,0.6,0.3)),("pu",(0.95,0.9,0.55)),("kanal",(0.55,0.55,0.6)),("rakor",(0.2,0.2,0.2)),("conta",(0.1,0.1,0.1)),("bakir",(0.8,0.5,0.25)),("celik",(0.5,0.52,0.55)),("paslanmaz",(0.78,0.8,0.82)),("sac",(0.72,0.74,0.77)),("aluminyum",(0.82,0.84,0.86)),("koyu",(0.25,0.25,0.25)),("siyah",(0.1,0.1,0.1)),("pom",(0.95,0.95,0.92)),("motor",(0.35,0.35,0.4)),("silikon",(0.9,0.3,0.3))]
ren=vtk.vtkRenderer(); ren.SetBackground(1,1,1)
idx=np.where(m)[0]; parts=np.unique(P[idx])
for pi in parts:
    s=idx[P[idx]==pi]; Q=np.stack([A[s],B[s],C[s]],1); n=len(Q)
    pts=vtk.vtkPoints(); pts.SetData(numpy_to_vtk(Q.reshape(-1,3).astype(np.float64),deep=True))
    cells=np.hstack([np.full((n,1),3),np.arange(3*n).reshape(-1,3)]).astype(np.int64).ravel()
    ca=vtk.vtkCellArray(); ca.SetCells(n,numpy_to_vtkIdTypeArray(cells,deep=True))
    pd=vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(ca)
    mp=vtk.vtkPolyDataMapper(); mp.SetInputData(pd); a=vtk.vtkActor(); a.SetMapper(mp)
    ad=PJ[pi]['ad']; mal=ad.split('__')[1] if '__' in ad else ad; col=(0.7,0.7,0.7)
    for k,v in RENK:
        if k in mal.lower(): col=v; break
    if PJ[pi]['mek'] in vur: col=(1.0,0.45,0.05)
    a.GetProperty().SetColor(*col)
    fe=vtk.vtkFeatureEdges(); fe.SetInputData(pd); fe.BoundaryEdgesOn(); fe.FeatureEdgesOn(); fe.SetFeatureAngle(35); fe.ManifoldEdgesOff(); fe.NonManifoldEdgesOff()
    m2=vtk.vtkPolyDataMapper(); m2.SetInputConnection(fe.GetOutputPort()); m2.ScalarVisibilityOff()
    a2=vtk.vtkActor(); a2.SetMapper(m2); a2.GetProperty().SetColor(0,0,0)
    ren.AddActor(a); ren.AddActor(a2)
cc=(lo+hi)/2; dm=np.linalg.norm(hi-lo)
cm=ren.GetActiveCamera(); cm.SetFocalPoint(*cc); cm.SetPosition(*(cc+cam/np.linalg.norm(cam)*dm*1.6)); cm.SetViewUp(0,1,0); cm.SetViewAngle(30)
if orto: cm.ParallelProjectionOn(); cm.SetParallelScale(max(hi[1]-lo[1],(hi[0]-lo[0])*0.7)/2*1.05)
ren.ResetCameraClippingRange()
rw=vtk.vtkRenderWindow(); rw.SetOffScreenRendering(1); rw.AddRenderer(ren); rw.SetSize(1400,1000); rw.Render()
w=vtk.vtkWindowToImageFilter(); w.SetInput(rw); w.Update(); wr=vtk.vtkJPEGWriter(); wr.SetFileName(out); wr.SetInputConnection(w.GetOutputPort()); wr.SetQuality(90); wr.Write(); print('yazildi',out)
