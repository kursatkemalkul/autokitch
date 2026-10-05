"""Fit an outward-to-inward radius schedule using measured outlet footprints.

This is a reduced-order optimization, not an independent physics validation.
The resulting control law must be run again in PhysX. No output food is moved.
"""
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import nnls
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'arastirma/3_TOPPING/sucuk_v2'
tag=sys.argv[1] if len(sys.argv)>1 else 'full_candidate_01'
d=np.load(OUT/'runs'/(tag+'.npz'));n=len(d['mass_kg']);x=d['xyz'][:,:n]
samples=[];weights=[]
for i in range(n):
    jj=np.flatnonzero((x[:-1,i,2]>=.145)&(x[1:,i,2]<.145))
    if not len(jj):continue
    j=int(jj[0]);a=x[j,i];b=x[j+1,i];f=(a[2]-.145)/(a[2]-b[2])
    p=a+f*(b-a)
    if abs(p[0]-1.4725)<.04 and abs(p[1]-.1525)<.04:
        samples.append([(p[0]-1.4725)*1000,(p[1]-.1525)*1000]);weights.append(d['mass_kg'][i])
s=np.array(samples);w=np.array(weights);w/=w.sum();assert len(s)>80
radius=np.arange(112.,19.,-4.)
edges=np.sqrt(np.linspace(0,125**2,13))
A=[]
for r in radius:
    dx=np.sqrt(r*r-17.5**2)
    rr=np.sqrt((dx+s[:,0])**2+(-17.5+s[:,1])**2)
    h=np.histogram(rr,edges,weights=w)[0]
    A.append(np.r_[h,w[rr>125].sum()])
A=np.array(A).T
# Uniform AREAL mass, with explicit outside-usable-disk penalty and smoothing.
penalty=np.ones(13);penalty[-1]=3.
D=np.diff(np.eye(len(radius)),2,axis=0)
mat=np.vstack([A*penalty[:,None],.06*D,np.ones((1,len(radius)))*5])
target=np.r_[np.ones(12)/12,0,np.zeros(len(D)),5]
q,_=nnls(mat,target);q/=q.sum()
pred=A@q
keep=q>.001;r=radius[keep];q=q[keep];q/=q.sum()
mid=np.cumsum(q)-q/2
frac=np.r_[0,mid,1];radii=np.r_[r[0],r,r[-1]]
law={'source_run':tag,'method':'NNLS using measured XY at z=145 mm; requires new PhysX run',
     'footprint_count':len(s),'footprint_mean_mm':s.mean(0).tolist(),
     'radii_mm':r.tolist(),'mass_fractions':q.tolist(),
     'progress_knots':frac.tolist(),'radius_knots_mm':radii.tolist(),
     'predicted_12_ring_fractions':pred[:-1].tolist(),
     'predicted_outside_usable_fraction':float(pred[-1]),
     'predicted_ring_cv_percent':float(np.std(pred[:-1])/np.mean(pred[:-1])*100),
     'assumptions':['Landing scatter approximated by actual outlet-plane XY samples.',
         'Rolling, post-impact slide, changing feed bias and table lag NOT included in surrogate.',
         'No food adhesion assumed. This is NOT a perfect-distribution claim.']}
(OUT/'radius_law_v1.json').write_text(json.dumps(law,indent=2),encoding='utf-8')
print(json.dumps(law),flush=True)
