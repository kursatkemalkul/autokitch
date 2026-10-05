import sys, numpy as np
sys.path.insert(0,'.')
from glbkit import Glb
G=Glb(sys.argv[1])
for nm in sys.argv[2:]:
    p=G.bul(nm); ex=p['pr'].get('extras',{}); k=ex.get('kat',[]); vis=G.gorunur(p)
    print('==',nm,'tris',len(p['T']),'kat entries',len(k)//3, 'kpk',ex.get('kpk'))
    for i in range(0,len(k),3):
        a=k[i+1]//3; n=k[i+2]//3; m=np.zeros(len(p['T']),bool); m[a:a+n]=True; m&=vis
        if not m.any(): print('  [%5d +%5d] lab %s  (bos)'%(a,n,k[i])); continue
        Q=p['X'][p['T'][m]].reshape(-1,3); lo=Q.min(0); hi=Q.max(0)
        print('  [%6d +%6d] lab %-3s vis %6d  x %7.1f %7.1f y %7.1f %7.1f z %7.1f %7.1f'%(a,n,k[i],m.sum(),lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]))
