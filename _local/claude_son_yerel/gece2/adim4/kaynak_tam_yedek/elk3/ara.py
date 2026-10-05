import numpy as np
from scipy.ndimage import minimum_filter
h=5.0
for D in (100,120):
  for (H,W) in ((300,120),(120,300),(200,150)):
    ok=None; per={}
    for xf in (2500,4000,4400):
        M=np.minimum(np.load("dep_%d_L.npy"%xf),np.load("dep_%d_R.npy"%xf))
        # min over rect starting at (iy,iz)
        F=minimum_filter(M,size=(int(H/h),int(W/h)),origin=(-(int(H/h)//2),-(int(W/h)//2)),mode='constant',cval=0)
        g=F>=D
        g[int(1862/h):]=False   # main level only
        g[:int(800/h)]=False
        per[xf]=g
        ok=g if ok is None else ok&g
    iy,iz=np.where(ok)
    print("D",D,"HxW",H,W,"common",len(iy))
    if len(iy):
        # summarize ranges
        ys=sorted(set((iy*h).astype(int))); zs=sorted(set((iz*h-830).astype(int)))
        print("  y0 range",ys[0],ys[-1]," z0 range",zs[0],zs[-1])
        for a,b in zip(iy[::max(1,len(iy)//15)],iz[::max(1,len(iy)//15)]): print("   y0 %d z0 %d"%(a*h,b*h-830))
    for xf,g in per.items():
        iy,iz=np.where(g); print("   face",xf,"n",len(iy), "y0",(sorted(set((iy*h).astype(int)))[:3],sorted(set((iy*h).astype(int)))[-3:]) if len(iy) else "")
