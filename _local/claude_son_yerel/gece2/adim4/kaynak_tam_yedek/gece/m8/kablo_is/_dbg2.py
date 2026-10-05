import sys,pickle,numpy as np
sys.path.insert(0,'.');sys.path.insert(0,'../..')
import glbkit
G=glbkit.Glb('../../../hat3_v8x.glb')
K=pickle.load(open('_kay.pkl','rb'))
for w in sys.argv[1:]:
    d=[x for x in K if x['id']==w][0]
    p=G.prims[d['pid']]; Tc=p['X'][p['T'][d['tri_idx']]]
    V=np.unique(Tc.reshape(-1,3).round(1),axis=0)
    print(w,d['ad'],len(Tc),len(V))
    o=np.argsort(V[:,1]); 
    for v in V[o][::max(1,len(V)//25)]: print('  ',v)
