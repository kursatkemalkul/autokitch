import pickle, numpy as np, sys
sys.stdout.reconfigure(encoding='utf-8')
B = pickle.load(open('t_bil.pkl','rb')); L=B['L']
# triangles (bbox) of all comps in dry compartment, excluding evaporator casings themselves (we stop at their bottom) and govde sheets except kuru taban? include all
TB=[]
for o in L:
    if np.all(o['hi']>np.array([1440,1109.2,-827])) and np.all(o['lo']<np.array([2230,1390,-631])):
        P=o['V'][o['F']]; lo=P.min(1); hi=P.max(1)
        m=np.all(hi>np.array([1440,1109.2,-827]),1)&np.all(lo<np.array([2230,1390,-631]),1)
        TB.append((lo[m],hi[m]))
lo=np.vstack([a for a,b in TB]); hi=np.vstack([b for a,b in TB])
print(len(lo),'tri')
def bos(x0,x1,z0,z1,y0,y1):
    m=(hi[:,0]>x0)&(lo[:,0]<x1)&(hi[:,2]>z0)&(lo[:,2]<z1)&(hi[:,1]>y0)&(lo[:,1]<y1)
    return not m.any()
for nm,(xa,xb,yt) in {'L':(1446,1670,1282),'R':(1758,2223,1383)}.items():
    res=[]
    for x in np.arange(xa,xb-24+0.1,2):
        for z in np.arange(-826,-640-24+0.1,2):
            if bos(x,x+24,z,z+24,1109.3,yt-0.3): res.append((x,z))
    print(nm,len(res))
    if res:
        R=np.array(res); 
        # cluster print extremes
        for xx in sorted(set(R[:,0]))[::6]:
            zz=R[R[:,0]==xx][:,1]; print('  x',xx,'z',zz.min(),'..',zz.max(),len(zz))
