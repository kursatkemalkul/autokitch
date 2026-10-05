import sys,pickle,numpy as np
sys.path.insert(0,'.')
import ortam as O
K=pickle.load(open('_kay.pkl','rb'))
for w in ('ELK_QR_KABLO__kablo#19','ELK_QR_KABLO__kablo#25','ELK_QR_KABLO__kablo#31'):
    d=[x for x in K if x['id']==w][0]
    p=O.G.prims[d['pid']]; T=p['X'][p['T'][d['tri_idx']]]
    lo,hi=T.reshape(-1,3).min(0),T.reshape(-1,3).max(0)
    print(w,d['ad'],lo.round(1),hi.round(1))
    # kanal#2 icindeki kablo ucgenleri / kanal ucgenleri cakisma: kablo kosesi kanal kati icinde mi -> kanal ucgenine en yakin
    V=np.unique(T.reshape(-1,3),axis=0)
    hit={}
    for v in V[::3]:
        h=O.en_yakin(v,0.3,haric=lambda o:(o[:,0]==d['pid'])&(o[:,1]==d['comp']))
        if h: a=O.ad(*O.OWN[h[1]]); hit[a]=hit.get(a,0)+1
    print('  yuzeyi 0.3mm icinde:',hit)
