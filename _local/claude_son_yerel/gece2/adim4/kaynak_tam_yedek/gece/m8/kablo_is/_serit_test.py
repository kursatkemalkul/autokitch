import sys,os,pickle,numpy as np
sys.path.insert(0,'.');sys.path.insert(0,'../..')
import glbkit,serit
G=glbkit.Glb('../../../hat3_v8x.glb')
K=pickle.load(open('_kay.pkl','rb'))
for want in ('ELK_ANA_HAT__kablo_veri#121','ELK_TOPPING__kablo#75','ELK_ANA_HAT__kablo_veri#120','ELK_K__kablo#2'):
    d=[x for x in K if x['id']==want][0]
    p=G.prims[d['pid']]
    Tc=p['X'][p['T'][d['tri_idx']]]
    S=serit.segmentler(Tc)
    print(want,d['ad'],len(S), 'toplamL',round(sum(np.linalg.norm(s['b']-s['a']) for s in S)))
    for s in S[:60]: print('  ',np.round(s['a']).astype(int),np.round(s['b']).astype(int),round(s['r'],1),s['n'])
