import pickle,numpy as np,sys
D=pickle.load(open("kay0.pkl","rb"))
for i,d in enumerate(D['KAY']):
    if d['ist']!=sys.argv[1]: continue
    if len(sys.argv)>2 and d['Lacik']<float(sys.argv[2]): continue
    s=" | ".join("%s>%s"%(np.round(q['a']).astype(int).tolist(),np.round(q['b']).astype(int).tolist()) for q in d['S'])
    print("#%d %s r%.1f L%.0f a%.0f :: %s"%(i,d['prim'],d['r'],d['L'],d['Lacik'],s))
