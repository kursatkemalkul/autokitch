"""Empirical radial kernel including observed post-impact drift.

Training a control law is NOT validation. Run the exported law in PhysX again.
Does not edit or reposition simulated food; only creates a new control input.
"""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import nnls

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'arastirma/3_TOPPING/sucuk_v2'
tag='full_candidate_optimized_01'
d=np.load(OUT/'runs'/(tag+'.npz'))
n=len(d['mass_kg']); xyz=d['xyz']; names=d['paths'].tolist()
pp=xyz[:,names.index('/World/PIDE')]; pts=xyz[:,:n]
error=[];mass=[];rows=[]
for i in range(n):
    jj=np.flatnonzero((pts[:-1,i,2]>=.140)&(pts[1:,i,2]<.140))
    if not len(jj):continue
    j=int(jj[0])+1
    if np.linalg.norm(pts[j,i,:2]-[1.4725,.1525])>.055:continue
    if pts[-1,i,2]<.10:continue # Floor impacts are not a landing kernel.
    nominal=float(np.linalg.norm(pp[j,:2]-[1.4725,.1525])*1000)
    actual=float(np.linalg.norm(pts[-1,i,:2]-pp[-1,:2])*1000)
    e=actual-nominal
    if abs(e)>60:continue
    error.append(e);mass.append(d['mass_kg'][i]);rows.append([nominal,actual,e])
e=np.array(error);w=np.array(mass);w/=w.sum()
assert len(e)>80
radii=np.arange(124.,19.,-2.)
edges=np.sqrt(np.linspace(0,125**2,11))
A=[]
for r in radii:
    predicted=np.maximum(0,r+e)
    h=np.histogram(predicted,edges,weights=w)[0]
    # Outside 125 mm is an edge margin, not necessarily waste (dough r=140).
    A.append(np.r_[h,w[predicted>125].sum(),w[predicted>140].sum()])
A=np.array(A).T
D=np.diff(np.eye(len(radii)),2,axis=0)
trials=[]
for spill_weight in (0.,.25,.5,1.,2.,4.):
    penalty=np.r_[np.ones(10),0.,spill_weight]
    mat=np.vstack([A*penalty[:,None],.10*D,np.ones((1,len(radii)))*5])
    target=np.r_[np.ones(10)*.09,0,0,np.zeros(len(D)),5]
    q,_=nnls(mat,target);q/=q.sum();pred=A@q
    cv=float(np.std(pred[:10])/np.mean(pred[:10])*100)
    trials.append((cv,float(pred[-1]),spill_weight,q.copy(),pred.copy()))
feasible=[a for a in trials if a[1]<=.05]
chosen=min(feasible or trials,key=lambda a:a[0])
_,_,spill_weight,q,pred=chosen
# Use piecewise constant radius stations with a narrow interpolation ramp;
# unlike mid-point interpolation, this preserves the fitted dwell masses.
keep=q>.001;r=radii[keep];q=q[keep];q/=q.sum()
knots=[0.];values=[r[0]]
cum=np.cumsum(q)
for k,b in enumerate(cum[:-1]):
    ramp=min(.002,q[k]/8,q[k+1]/8)
    knots.extend([b-ramp,b+ramp]);values.extend([r[k],r[k+1]])
knots.append(1.);values.append(r[-1])
law={'source_run':tag,'method':'NNLS empirical final radial error; requires NEW PhysX validation',
     'sample_count':len(e),'radial_error_mean_mm':float(np.sum(w*e)),
     'radial_error_std_mm':float(np.sqrt(np.sum(w*(e-np.sum(w*e))**2))),
     'progress_knots':knots,'radius_knots_mm':values,
     'radii_mm':r.tolist(),'mass_fractions':q.tolist(),
     'predicted_ring_cv_percent':float(np.std(pred[:10])/np.mean(pred[:10])*100),
     'predicted_edge_margin_fraction':float(pred[-2]),
     'predicted_spill_fraction':float(pred[-1]),
     'tradeoff_scan':[{'ring_cv_percent':a[0],'spill_fraction':a[1],'spill_weight':a[2]} for a in trials],
     'limits':['Empirical fit to one uncalibrated material / one run.',
               'Radial error assumed independent of target radius and time.',
               'No physical weighing sensor is installed.']}
(OUT/'radius_law_v2.json').write_text(json.dumps(law,indent=2),encoding='utf-8')
print(json.dumps(law),flush=True)
