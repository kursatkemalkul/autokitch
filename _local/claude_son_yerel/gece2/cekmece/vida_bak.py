import pickle,numpy as np,trimesh,sys
sys.stdout.reconfigure(encoding='utf-8')
P=pickle.load(open('parca.pkl','rb'))
def prof(a, ax=0, c=(443.35,-580)):
    V=P[a]['V']*1000
    xs=np.unique(np.round(V[:,0],2))
    print(a,'x seviyeleri',xs[:40])
    for x in xs:
        m=np.abs(V[:,0]-x)<0.01
        r=np.sqrt((V[m,1]-c[0])**2+(V[m,2]-c[1])**2)
        print('   x %.2f  r %.2f–%.2f'%(x,r.min(),r.max()))
prof('vida_sol_1')
V=P['cevre_pem']['V']*1000; m=(np.abs(V[:,2]+580)<8)&(V[:,0]<1460)
xs=np.unique(np.round(V[m,0],2)); print('PEM x',xs)
for x in xs:
    mm=m&(np.abs(V[:,0]-x)<0.01); r=np.sqrt((V[mm,1]-443.35)**2+(V[mm,2]+580)**2); print('   x %.2f r %.2f–%.2f'%(x,r.min(),r.max()))
V=P['cevre_kopuk_kapagi']['V']*1000; m=(np.abs(V[:,2]+580)<8)&(V[:,0]<1460)
xs=np.unique(np.round(V[m,0],2)); print('köpük kapağı x',xs)
for x in xs:
    mm=m&(np.abs(V[:,0]-x)<0.01); r=np.sqrt((V[mm,1]-443.35)**2+(V[mm,2]+580)**2); print('   x %.2f r %.2f–%.2f'%(x,r.min(),r.max()))
# sabit ray deliği
V=P['sabit_ray_sol']['V']*1000; m=(np.abs(V[:,2]+580)<8)
print('sabit ray verts near screw', np.unique(np.round(V[m,0],2)), np.round(np.sort(np.unique(np.round(np.sqrt((V[m,1]-443.35)**2+(V[m,2]+580)**2),2)))[:10],2))
V=P['ara_ray_sol']['V']*1000; m=(np.abs(V[:,2]+580)<12)
print('ara ray verts near screw', np.unique(np.round(V[m,0],2)), np.round(np.sort(np.unique(np.round(np.sqrt((V[m,1]-443.35)**2+(V[m,2]+580)**2),2)))[:10],2))
# çevre sac bölme
V=P['cevre_sac']['V']*1000; m=(np.abs(V[:,2]+580)<20)&(V[:,0]>1400)&(V[:,0]<1460)&(np.abs(V[:,1]-443)<20)
print('sac x near', np.unique(np.round(V[m,0],2)))
V=P['cevre_pu']['V']*1000; m=(np.abs(V[:,2]+580)<20)&(V[:,0]>1400)&(V[:,0]<1460)&(np.abs(V[:,1]-443)<20)
print('pu x near', np.unique(np.round(V[m,0],2)))
