import pickle,numpy as np,trimesh,sys
sys.stdout.reconfigure(encoding='utf-8')
P=pickle.load(open('parca.pkl','rb'))
def ayir(a):
    V=P[a]['V']*1000;F=P[a]['F']
    m=trimesh.Trimesh(V,F,process=True)
    xs=[np.unique(np.round(V[:,i],2)) for i in range(3)]
    if max(len(x) for x in xs)>40: print(a,'çok koordinat',[len(x) for x in xs]); return
    cs=[(x[:-1]+x[1:])/2 for x in xs]
    G=np.stack(np.meshgrid(*cs,indexing='ij'),-1).reshape(-1,3)
    ins=m.contains(G).reshape(len(cs[0]),len(cs[1]),len(cs[2]))
    # greedy box merge
    used=np.zeros_like(ins);out=[]
    for i,j,k in zip(*np.nonzero(ins)):
        if used[i,j,k]: continue
        i2=i
        while i2+1<ins.shape[0] and ins[i2+1,j,k] and not used[i2+1,j,k]: i2+=1
        j2=j
        while j2+1<ins.shape[1] and ins[i:i2+1,j2+1,k].all() and not used[i:i2+1,j2+1,k].any(): j2+=1
        k2=k
        while k2+1<ins.shape[2] and ins[i:i2+1,j:j2+1,k2+1].all() and not used[i:i2+1,j:j2+1,k2+1].any(): k2+=1
        used[i:i2+1,j:j2+1,k:k2+1]=True
        out.append((xs[0][i],xs[0][i2+1],xs[1][j],xs[1][j2+1],xs[2][k],xs[2][k2+1]))
    print(a,'watertight',m.is_watertight,'hacim %.0f'%m.volume)
    for b in out: print('   x %.2f–%.2f (%.2f)  y %.2f–%.2f (%.2f)  z %.2f–%.2f (%.2f)'%(b[0],b[1],b[1]-b[0],b[2],b[3],b[3]-b[2],b[4],b[5],b[5]-b[4]))
for a in sys.argv[1:]: ayir(a)
