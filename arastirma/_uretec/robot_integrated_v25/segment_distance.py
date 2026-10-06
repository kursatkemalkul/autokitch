import numpy as np

def dist(a,b,c,d):
    u=b-a;v=d-c;w=a-c
    def endpoint(p,q,r):
        e=r-q;t=np.clip(np.einsum('ij,ij->i',p-q,e)/np.einsum('ij,ij->i',e,e),0,1)
        return np.linalg.norm(p-(q+e*t[:,None]),axis=1)
    r=np.minimum.reduce([endpoint(a,c,d),endpoint(b,c,d),endpoint(c,a,b),endpoint(d,a,b)])
    aa=np.einsum('ij,ij->i',u,u);bb=np.einsum('ij,ij->i',u,v);cc=np.einsum('ij,ij->i',v,v);dd=np.einsum('ij,ij->i',u,w);ee=np.einsum('ij,ij->i',v,w);den=aa*cc-bb*bb
    live=den>1e-20;s=np.zeros(len(den));t=s.copy();s[live]=(bb[live]*ee[live]-cc[live]*dd[live])/den[live];t[live]=(aa[live]*ee[live]-bb[live]*dd[live])/den[live]
    inside=live&(s>=0)&(s<=1)&(t>=0)&(t<=1);r[inside]=np.minimum(r[inside],np.linalg.norm(w[inside]+u[inside]*s[inside,None]-v[inside]*t[inside,None],axis=1));return r
