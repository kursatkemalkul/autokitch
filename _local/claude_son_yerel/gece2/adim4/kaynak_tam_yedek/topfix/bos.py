import numpy as np, json
D=np.load('zb/m8_onbellek.npz'); A,B,C,P,mek=D['A'],D['B'],D['C'],D['P'],D['mek']
PJ=json.load(open('zb/m8_parca.json',encoding='utf-8'))['parca']
lo=np.minimum(np.minimum(A,B),C); hi=np.maximum(np.maximum(A,B),C)
# haric: tasinacak birimler + sogutma(evap) + TOPPING hava + KLF kablo
har=np.isin(mek,[9,10,11,12,13,14,16,17])
klf=np.array([PJ[p]['ad']=='ELK_TOPPING__kablo' and PJ[p]['lo'][0]>1660 and PJ[p]['hi'][0]<1710 and PJ[p]['hi'][1]>1800 for p in P])
s=(~har)&(~klf)&(hi[:,2]>-828.4)&(lo[:,2]<-630)&(hi[:,0]>1437.6)&(lo[:,0]<2498.4)&(hi[:,1]>1109)&(lo[:,1]<2198)
# buyuk kabuklari at (dis sac/tavan/taban)
ext=(hi-lo)
pe={}
for p in np.unique(P[s]):
    q=PJ[p]; e=np.array(q['hi'])-np.array(q['lo'])
    pe[p]=e
big=np.array([ (pe[p][0]>900 or pe[p][1]>900) for p in P[s]])
idx=np.where(s)[0][~big]
print('ucgen',len(idx))
h=5.0; X0,Y0,Z0=1437.5,1109.0,-828.5
nx,ny,nz=int((2498.5-X0)/h)+1,int((2198.5-Y0)/h)+1,int((-630-Z0)/h)+1
O=np.zeros((nx,ny,nz),bool)
for i in idx:
    a=np.floor((lo[i]-[X0,Y0,Z0])/h).astype(int); b=np.ceil((hi[i]-[X0,Y0,Z0])/h).astype(int)
    a=np.maximum(a,0); b=np.minimum(b,[nx,ny,nz])
    O[a[0]:b[0],a[1]:b[1],a[2]:b[2]]=True
np.save('occ.npy',O)
for z0,z1 in [(-826,-640),(-770,-640),(-800,-640)]:
    k0,k1=int((z0-Z0)/h),int((z1-Z0)/h)
    M=O[:,:,k0:k1].any(2)
    # en buyuk serbest dikdortgen, x1<=1686 (sol) ve x0>=1758 (sag)
    for side,(xa,xb) in (('sol',(1437.5,1686)),('sag',(1758,2214))):
        ia,ib=int((xa-X0)/h),int((xb-X0)/h)
        best=(0,)
        sub=M[ia:ib]
        W,H=sub.shape
        for y0 in range(H):
            for y1 in range(y0+20,H):
                col=sub[:,y0:y1].any(1)
                # en uzun serbest x araligi
                run=0;br=0;be=0
                for xi in range(W):
                    run = 0 if col[xi] else run+1
                    if run>br: br=run; be=xi
                ar=br*(y1-y0)
                if ar>best[0]: best=(ar,X0+(ia+be-br+1)*h,X0+(ia+be+1)*h,Y0+y0*h,Y0+y1*h)
        print(z0,z1,side,'alan %.0f cm2'%(best[0]*h*h/100),'x %.0f-%.0f y %.0f-%.0f'%best[1:])
