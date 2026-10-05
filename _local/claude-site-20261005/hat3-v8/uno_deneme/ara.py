# -*- coding: utf-8 -*-
import itertools
L,R=1495,2441; G=62
ALT={'cur':{'kiyma':(190,95),'kusbasi':(190,95),'kasar':(308,164),'sucuk':(169,94)},
     'man':{'kiyma':(190,95),'kusbasi':(190,95),'kasar':(288,144),'sucuk':(150,75)}}
UST={'kucuk':220,'buyuk':380}
EVAP=(1657,2235)
def ara(env,ust,evap,order_fixed=True,G=G):
    W=ALT[env]; res=[]
    orders=[('kiyma','kusbasi','kasar','sucuk')] if order_fixed else list(itertools.permutations(W))
    n=len(ust)
    for o in orders:
        S=(R-L)-sum(W[u][0] for u in o)-n*G
        for slots in itertools.combinations(range(5),n):
            if S<0: res.append((S,o,slots,None,None)); continue
            # distribute slack in 1mm over 5 slots (pad before each unit + after last)
            st=max(1,S//10)
            for pads in itertools.product(list(range(0,S+1,st))+[S],repeat=4):
                if sum(pads)>S: continue
                x=L; gx=[]; ux={}
                for i in range(5):
                    if i<4: x+=pads[i]
                    if i in slots: gx.append(x+G/2); x+=G
                    if i<4: ux[o[i]]=(x,x+W[o[i]][0]); x+=W[o[i]][0]
                for perm in set(itertools.permutations(ust)):
                    ok=True; hz=[]
                    for g,u in zip(gx,perm):
                        a,b=g-UST[u]/2,g+UST[u]/2
                        if a<L or b>R: ok=False
                        if evap and EVAP[0]<g<EVAP[1]: ok=False
                        hz.append((a,b))
                    for i in range(len(hz)-1):
                        if hz[i][1]+10>hz[i+1][0]: ok=False
                    if ok: res.append((S,o,slots,(pads,gx,ux),perm))
    return res
for env in ['cur','man']:
  for ust in [('kucuk','buyuk'),('kucuk','kucuk','buyuk')]:
    for evap in [False,True]:
      for of in [True,False]:
        r=ara(env,ust,evap,of)
        ok=[x for x in r if x[3]]
        S=r[0][0] if r else None
        print(env,len(ust),'evap' if evap else '-', 'sira_sabit' if of else 'sira_serbest','S=',S,'cozum',len(ok))
        for x in ok[:3]: print('   ',x[1],x[2],[round(g) for g in x[3][1]],x[4],{k:tuple(round(v) for v in vv) for k,vv in x[3][2].items()})
