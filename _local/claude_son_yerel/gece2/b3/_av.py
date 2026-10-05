import pickle, numpy as np, sys
sys.path.insert(0,r'..\cekmece'); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
D=pickle.load(open('plan_b3.pkl','rb')); P=D['P']
ck='CEK_K2_lahm_3'; a=ck+'_avara'
ST=['g_on_cerceve_1',ck+'_ray_sol',ck+'_ray_sag',ck+'_tahrik','g_bolme_1_sac_b','g_bolme_2_sac_a','g_ic_tavan_1','CEK_K2_lahm_2_tahrik','CEK_K2_lahm_4_tahrik']
TRI={k:Y._vekil(P[k]['V']/1000,P[k]['F']) for k in ST+[a]}
def bos(o1,o2):
    o1=np.asarray(o1)/1000; o2=np.asarray(o2)/1000; v=o2-o1; A0=TRI[a]+o1
    for b in ST:
        B=TRI[b]
        lam=Y.ccd(np.ascontiguousarray(A0),np.ascontiguousarray(B),v,Y.SINIR)
        m=lam<1.5
        if m.any():
            pts=lam[m][:,None]*v[None,:]; der=np.minimum(np.linalg.norm(pts-v,axis=1),np.linalg.norm(pts,axis=1))
            if der.max()>Y.OTURMA: return b
    return None
# çerçeve ağız kenarı: z 23..24'te x 1440..1520, y 470..530 bölgesindeki çerçeve köşe noktaları
V=P['g_on_cerceve_1']['V']; m=(V[:,0]>1440)&(V[:,0]<1530)&(V[:,1]>380)&(V[:,1]<540)
print(np.unique(np.round(V[m][:,[0,1]],1),axis=0))
for dy in (0,-10,-20,-30,-40,-50,-60):
    for dx in (0,10,20,30,45,60,80):
        r1=bos((dx,dy,900),(dx,dy,0)); r2=bos((dx,dy,0),(0,0,0)) if not r1 else 'x'
        if not r1 and not r2: print('OK',dx,dy)
print('bitti')
