import glb_oku, numpy as np
J, D = glb_oku.yukle("hat3_v8l.glb")
for nd in ["ELK_ANA_HAT__kablo","ELK_ANA_HAT__kablo_veri","ELK_ANA_HAT__paslanmaz","ELK_ISTASYON__rakor","ELK_ANA_HAT__rakor","ELK_ZEMIN_KANALI__paslanmaz","URUN__top"]:
    X,T=D[nd]; P=X[np.unique(T)]
    m=(P[:,0]>736)&(P[:,0]<4400)&(P[:,1]<788.5)&(P[:,1]>0)&(P[:,2]>-830)&(P[:,2]<39)
    Q=P[m]
    if not len(Q): continue
    # histogram by x bins
    print(nd, len(Q))
    xb=np.floor(Q[:,0]/50)*50
    for x in np.unique(xb):
        R=Q[xb==x]; print("   x %5d..: y %6.1f-%6.1f z %7.1f-%7.1f n %d"%(x,R[:,1].min(),R[:,1].max(),R[:,2].min(),R[:,2].max(),len(R)))
