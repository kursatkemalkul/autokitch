import sys,pickle,numpy as np
K=pickle.load(open('_kay.pkl','rb'))
for w in sys.argv[1:]:
    for d in K:
        if d['id']==w or d['ad']==w:
            print(d['id'],d['ad'],'r',round(d['r'],1),'Ls',round(d['Ls']))
            for q in d['S']: print('   S',np.round(q['a'],1).tolist(),'->',np.round(q['b'],1).tolist(),'r',round(q['r'],1))
            for u_ in d['uclar']: print('   UC',np.round(u_[0],1).tolist(),np.round(u_[1],2).tolist(),u_[4:] )
