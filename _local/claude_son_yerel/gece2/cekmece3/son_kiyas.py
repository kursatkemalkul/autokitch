# animasyon son karesi ↔ ana model (hat3_v9l) — her öğenin kutusu modeldeki bileşen(ler)in kutusuyla ±0,01 mm
import sys,pickle,json,numpy as np
sys.path.insert(0,'../cekmece'); sys.stdout.reconfigure(encoding='utf-8')
from glb import G,bilesen
g=G('hat3_v9l.glb')
M=[]
for n in [x.get('name','') for x in g.J['nodes']]:
    if not (n.startswith('CEK_K2_lahm_3__') or n in ('B_KASA__paslanmaz','B_KASA__conta','ELK_DOLAP__kablo_sinyal')): continue
    for X,T,_,_,_ in g.tris(g.byname[n]):
        Pm=X[T]; ar=np.linalg.norm(np.cross(Pm[:,1]-Pm[:,0],Pm[:,2]-Pm[:,0]),axis=1); T=T[ar>1e-9]; cl=bilesen(X,T); Pm=X[T]
        for c in np.unique(cl):
            Q=Pm[cl==c].reshape(-1,3); M.append((n,Q.min(0),Q.max(0)))
D=pickle.load(open('plan_v3.pkl','rb')); P=D['P']
GRUP={'mil':['avara_mili','e_segman'],'kol_tabla_cene':['kol','tabla','kulak','cene_ust'],'kutu':['kutu_taban','kutu_yan_sol','kutu_yan_sag','kutu_arka','kutu_on'],'kapak':['kapak_dis','kapak_ic','kapak_pu'],'avara':['avara_kolu','sensor_lamasi'],
      'cene':['cene_alt']}
tek=[a for a in P if P[a]['tur'] not in ('cevre','kaynak') and not any(a in v for v in GRUP.values())]
SON={}; enb=0; sorun=[]
def kut(adlar):
    V=np.vstack([P[a]['V'] for a in adlar]); return V.min(0),V.max(0)
for ad,adlar in [(a,[a]) for a in tek]+list(GRUP.items()):
    lo,hi=kut(adlar)
    ic=[m for m in M if np.all(m[1]>=lo-0.02) and np.all(m[2]<=hi+0.02)]
    if not ic: sorun.append((ad,'modelde karşılık yok')); continue
    l2=np.min([m[1] for m in ic],0); h2=np.max([m[2] for m in ic],0)
    f=float(max(np.abs(l2-lo).max(),np.abs(h2-hi).max())); SON[ad]=round(f,4); enb=max(enb,f)
    if f>0.01: sorun.append((ad,round(f,4)))
print('öğe',len(SON),'en büyük fark %.4f mm'%enb); print('SORUN',sorun)
json.dump(dict(oge=len(SON),enb=round(enb,4),sorun=sorun,fark=SON),open('son_kiyas_v3.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
