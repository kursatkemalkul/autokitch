import sys,numpy as np
sys.path.insert(0,'../gece'); sys.path.insert(0,'..')
import glbkit
G=glbkit.Glb('../hat3_v8zi.glb')
for ad in ('ELK_QR_KABLO__kablo','ELK_QR_KABLO__kablo_veri'):
    p=G.bul(ad); tl,kut=G.komp(p)
    for i,(a,b,n) in kut.items():
        if a[1]<120 and b[1]>500:
            m=(tl==i)&G.gorunur(p); V=p['X'][np.unique(p['T'][m])]
            # cluster vertices by rounding -> path corners: print vertices with y<200 extents
            print(ad,i,np.round(a,1),np.round(b,1),n)
            lowv=V[V[:,1]<150]; print('  low y<150 bbox',np.round(lowv.min(0),1),np.round(lowv.max(0),1))
            for zz in (700,720,760,800,900,1000,1040):
                s=V[np.abs(V[:,2]-zz)<15]
                if len(s): print('   z~',zz,np.round(s.min(0),1),np.round(s.max(0),1))
