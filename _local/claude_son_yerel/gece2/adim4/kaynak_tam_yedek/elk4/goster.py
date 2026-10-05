import pickle,sys,numpy as np
D=pickle.load(open(r"@@KOK_W@@\elk4\kay0.pkl","rb"))
for _,lo,hi in D['KAN']: print("KANAL",_,np.round(lo).astype(int),np.round(hi).astype(int))
for i,d in enumerate(D['KAY']):
    if d['ist']!=sys.argv[1]: continue
    print("#%d %s r%.1f L%.0f acik%.0f ntri%d"%(i,d['prim'],d['r'],d['L'],d['Lacik'],len(d['tri'])))
    for q in d['S']: print("    ",np.round(q['a'],1).tolist(),"->",np.round(q['b'],1).tolist(),"r%.1f ic%.2f"%(q['r'],q['ic'].mean()))
