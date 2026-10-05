import pickle,numpy as np,trimesh,sys
sys.stdout.reconfigure(encoding='utf-8')
P=pickle.load(open('parca.pkl','rb'))
def tm(a): return trimesh.Trimesh(P[a]['V']*1000,P[a]['F'],process=False)
def kirp(a,lo,hi):
    V=P[a]['V']*1000;F=P[a]['F'];T=V[F];m=np.all(T.max(1)>=lo,1)&np.all(T.min(1)<=hi,1)
    T=T[m]; 
    if not len(T): return None
    Q=T.reshape(-1,3); return np.round(Q.min(0),2),np.round(Q.max(0),2), [np.unique(np.round(Q[:,i],2))[:30] for i in range(3)]
print('çerçeve @ avara flanşı', kirp('cevre_on_cerceve',[1454,492,20],[1470,513,25]))
print('çerçeve @ x1460 y480-520', kirp('cevre_on_cerceve',[1458,470,20],[1462,520,25]))
print('arka duvar @ motor braketi', kirp('cevre_sac',[1480,424,-800],[1525,469,-789]))
print('arka pu @ motor', kirp('cevre_pu',[1480,424,-800],[1525,469,-789]))
print('arka duvar @ sensör plakası', kirp('cevre_sac',[1453,463,-800],[1470,488,-789]))
print('kanal @ sensör plakası', kirp('cevre_kanal',[1450,460,-800],[1475,495,-750]))
print('kanal @ lama arka', kirp('cevre_kanal',[1460,480,-800],[1472,500,-740]))
print('kablo_sensor bbox', kirp('kablo_sensor',[0,0,-900],[3000,900,100])[:2])
print('dikme near', kirp('cevre_dikme',[1440,400,-800],[1530,520,50])[:2])
print('sogutma', kirp('cevre_sogutma',[1440,400,-800],[2100,520,50])[:2])
