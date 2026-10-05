import sys, numpy as np
sys.path.insert(0,'.')
from glbkit import Glb
G=Glb(sys.argv[1]); nm=sys.argv[2]; ci=int(sys.argv[3]); box=list(map(float,sys.argv[4].split(',')))
p=G.bul(nm); tl,kut=G.komp(p)
m=(tl==ci)&G.gorunur(p); V=p['X'][np.unique(p['T'][m].reshape(-1))]
k=(V[:,0]>=box[0])&(V[:,0]<=box[1])&(V[:,1]>=box[2])&(V[:,1]<=box[3])&(V[:,2]>=box[4])&(V[:,2]<=box[5])
W=V[k]; print(len(V), len(W))
if len(W):
  # coarse path: cluster by rounding 20mm
  Q=np.unique(np.round(W/20)*20,axis=0); print(Q[:80])
