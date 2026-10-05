"""Fit a cheese table law from recorded impact drift; validate in PhysX again.

The fit changes only control inputs. It does not reposition any food and does
not itself validate distribution, adhesive matting, or real-food performance.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.optimize import nnls

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'arastirma/3_TOPPING/kasar_v2'
tag='candidate_02'
path=OUT/'runs'/(tag+'.npz')
d=np.load(path);n=len(d['mass_kg']);xyz=d['xyz'];names=d['paths'].tolist()
cfg=json.loads((ROOT/'otonom/hat3d/sim_makine.json').read_text(encoding='utf-8'))
slot=next(v for v in cfg['yuvalar'] if v['cad']=='kasar_cad_v14')
outlet=np.array([slot['x']/1000,-slot['agiz_z']/1000])
pp=xyz[:,names.index('/World/PIDE')];pts=xyz[:,:n]
error=[];mass=[]
for i in range(n):
    jj=np.flatnonzero((pts[:-1,i,2]>=.140)&(pts[1:,i,2]<.140))
    if not len(jj):continue
    j=int(jj[0])+1
    if np.linalg.norm(pts[j,i,:2]-outlet)>.055:continue
    if pts[-1,i,2]<.10:continue
    nominal=float(np.linalg.norm(pp[j,:2]-outlet)*1000)
    actual=float(np.linalg.norm(pts[-1,i,:2]-pp[-1,:2])*1000)
    e=actual-nominal
    if abs(e)>60:continue
    error.append(e);mass.append(d['mass_kg'][i])
e=np.array(error);w=np.array(mass);w/=w.sum()
assert len(e)>100
radii=np.arange(118.,19.,-2.)
edges=np.sqrt(np.linspace(0,125**2,11))
A=[]
for r in radii:
    predicted=np.maximum(0,r+e)
    h=np.histogram(predicted,edges,weights=w)[0]
    A.append(np.r_[h,w[predicted>125].sum(),w[predicted>140].sum()])
A=np.array(A).T
D=np.diff(np.eye(len(radii)),2,axis=0)
trials=[]
for spill_weight in (.5,1.,2.,4.):
    penalty=np.r_[np.ones(10),0.,spill_weight]
    mat=np.vstack([A*penalty[:,None],.10*D,np.ones((1,len(radii)))*5])
    target=np.r_[np.ones(10)*.095,0,0,np.zeros(len(D)),5]
    q,_=nnls(mat,target);q/=q.sum();pred=A@q
    cv=float(np.std(pred[:10])/np.mean(pred[:10])*100)
    trials.append((cv,float(pred[-1]),spill_weight,q.copy(),pred.copy()))
feasible=[a for a in trials if a[1]<=.03]
chosen=min(feasible or trials,key=lambda a:a[0])
_,_,spill_weight,q,pred=chosen
keep=q>.001;r=radii[keep];q=q[keep];q/=q.sum()
knots=[0.];values=[float(r[0])]
cum=np.cumsum(q)
for k,b in enumerate(cum[:-1]):
    ramp=min(.002,q[k]/8,q[k+1]/8)
    knots.extend([float(b-ramp),float(b+ramp)])
    values.extend([float(r[k]),float(r[k+1])])
knots.append(1.);values.append(float(r[-1]))
assert all(b>a for a,b in zip(knots,knots[1:]))
assert all(b<=a for a,b in zip(values,values[1:]))
law=dict(source_run=tag,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    method='NNLS empirical radial drift; needs NEW physical validation',
    sample_count=len(e),radial_error_mean_mm=float(np.sum(w*e)),
    radial_error_std_mm=float(np.sqrt(np.sum(w*(e-np.sum(w*e))**2))),
    progress_knots=knots,radius_knots_mm=values,
    radii_mm=r.tolist(),mass_fractions=q.tolist(),
    predicted_ring_cv_percent=float(np.std(pred[:10])/np.mean(pred[:10])*100),
    predicted_edge_margin_fraction=float(pred[-2]),predicted_spill_fraction=float(pred[-1]),
    suggested_table_rpm=35,
    limits=['One uncalibrated material and one seed.',
        'Radial drift assumed independent of radius and table speed.',
        'Real table servo lag and impact may change the fit.',
        'Virtual mass counter is not installed physical hardware.'])
(OUT/'radius_law_v1.json').write_text(json.dumps(law,indent=2),encoding='utf-8')
print(json.dumps(law),flush=True)
