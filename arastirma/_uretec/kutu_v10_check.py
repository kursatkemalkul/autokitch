"""Measure actual solids at actuator states; no global collision exemptions."""
import json,sys
from pathlib import Path
import cadquery as cq
import kutu_cad_v10 as K
OUT=Path(__file__).resolve().parents[2]/'_local'/'kutu-v10'
OUT.mkdir(parents=True,exist_ok=True)
RESULT=OUT/('candidate.json' if 'candidate' in sys.argv else 'checks.json')
K.modul()
P={p['ad']:p for p in K.PARCALAR}
def solid(p):
    vals=p['wp'].vals()
    return vals[0] if len(vals)==1 else cq.Compound.makeCompound(vals)
S={n:solid(p) for n,p in P.items()}
R={'parts':len(P),'invalid':[], 'collisions':[], 'contact':[], 'lid_contacts':[], 'envelope':[], 'production_validated':False}
for n,s in S.items():
    if not s.isValid():R['invalid'].append(n)
new=[n for n in P if n.startswith(('kose_','parmak_','devirme_','flap_kilavuz','flap_lineer','flap_burc','flap_vida_alt')) or n=='flap_katlayici_U']
new += [n for n in P if n in ('agiz_ust_kirisi','din_rayi_ek_klemens','klemens_sirasi')
        or (n.startswith('surucu_STP-DRV-4830_') and int(n.rsplit('_',1)[1])>=7)]

if 'probe' in sys.argv:
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
    for t in (2.85,3.35,6.0,6.3,7.4):
        w=K.blank_dunya(t)
        a=K.uygula(S['devirme_parmagi'],K.grup_matrisi('PARMAK',t))
        b=K.uygula(S['B_TIRNAK_ON_ON'],w[P['B_TIRNAK_ON_ON']['grup']])
        inter=cq.Shape.cast(BRepAlgoAPI_Common(a.wrapped,b.wrapped).Shape())
        bb=inter.BoundingBox() if inter.Volume()>.001 else None
        print('PROBE',t,K.parmak_psi(t),K.PARMAK_P,K.kafa(t),inter.Volume(),(bb.xmin,bb.xmax,bb.ymin,bb.ymax,bb.zmin,bb.zmax) if bb else None,flush=True)
    import os
    os._exit(0)

if 'static' in sys.argv:
    hits=[]; seen=set(); bb={n:s.BoundingBox() for n,s in S.items()}
    for n in new:
        for m,b in S.items():
            pair=tuple(sorted((n,m)))
            if n==m or pair in seen or P[n]['grup']!=P[m]['grup']:continue
            seen.add(pair)
            if not K._bb_kesisir(bb[n],bb[m]):continue
            v=S[n].intersect(b).Volume()
            if v>.5: hits.append([n,m,round(v,2)])
    print('RIGID_INTERSECTIONS',json.dumps(hits,indent=2),flush=True)
    support=[]
    for g in K.CORNER:
        for n in ('kose_'+g+'_yatak_govdesi','kose_'+g+'_motor_kelepcesi'):
            support.append([n,S[n].distance(S['kose_takim_hareketli_cerceve'])])
    print('CARRIER_CONTACTS',json.dumps(support),flush=True)
    print('FRAME_SOLIDS',len(S['kose_takim_hareketli_cerceve'].Solids()),flush=True)
    (OUT/'rigid.json').write_text(json.dumps(hits,indent=2),encoding='utf-8')
    assert not hits,hits[:5]
    assert all(d<=.05 for _,d in support),support
    assert len(S['kose_takim_hareketli_cerceve'].Solids())==1
    import os
    os._exit(0)
times=[0,1.6,1.8,2.6,2.85,3,3.35,3.7,4.25,4.6,5,5.5,6,6.3,6.4,6.55,6.7,6.85,7.1,7.2,7.6,8,8.5,9.4,9.7,10.2,11,14.8,15.8,16.4,17.2,20.6,23]
if 'quick' in sys.argv:times=[0,3.35,3.7,4.6,6.3,7.4,7.8,9.7]
if 'dense' in sys.argv:times=sorted(set(times+[round(i*.2,4) for i in range(116)]+[K.V10_PAUSE]))
for t in times:
    W=K.blank_dunya(t)
    world={n:K.uygula(s,W[P[n]['grup']] if P[n]['grup'].startswith('B_') else K.grup_matrisi(P[n]['grup'],t)) for n,s in S.items() if P[n]['grup'] not in ('PIZZA','CATAL','K_ITICI','SABIT_REF')}
    bb={n:s.BoundingBox() for n,s in world.items()}
    for n in new:
        q=bb[n]
        if q.xmin<-.1 or q.xmax>K.W+.1 or q.ymin<123-.1 or q.ymax>K.H+.1 or q.zmin<-K.D-.1 or q.zmax>K.Z_ON+.1:
            R['envelope'].append([t,n])
    seen=set()
    for n in new:
        a=world[n]
        for m,b in world.items():
            if n==m or tuple(sorted((n,m))) in seen:continue
            seen.add(tuple(sorted((n,m))))
            if not K._bb_kesisir(bb[n],bb[m]):continue
            # Same rigid assembly deliberately includes bolted mating surfaces.
            if P[n]['grup']==P[m]['grup'] and not P[n]['grup'].startswith('B_'):continue
            v=a.intersect(b).Volume()
            if v>.5:R['collisions'].append([t,n,m,round(v,2)])
    for g,bg in [('MF','B_CTMF'),('MB','B_CTMB'),('PF','B_CTPF'),('PB','B_CTPB')]:
        if 3<=t<=3.7:
            shoe=world['kose_CNR_'+g+'_temas_pabucu']; card=next(world[n] for n,p in P.items() if p['grup']==bg)
            R['contact'].append([t,g,round(shoe.distance(card),4)])
    if 7.2<=t<=8.0:
        R['contact'].append([t,'front',round(world['parmak_temasi_UHMW'].distance(world['B_ON_IC_KILITLI']),4)])
    if 9.4<=t<=9.8:
        for n in ('B_KAPAK_ON_FLAP','B_KAPAK_YAN_ARKA','B_KAPAK_YAN_ON'):
            R['lid_contacts'].append([t,n,world['flap_katlayici_U'].distance(world[n])])
    RESULT.write_text(json.dumps(R,indent=2),encoding='utf-8')
    print('TIME',t,'clashes',len(R['collisions']),flush=True)
RESULT.write_text(json.dumps(R,indent=2),encoding='utf-8')
print(json.dumps(R,indent=2),flush=True)
assert not R['invalid'],R['invalid']
assert not R['collisions'],R['collisions'][:5]
assert not R['envelope'],R['envelope'][:5]
assert all(row[-1]<.05 for row in R['contact']),R['contact']
assert all(row[-1]<.05 for row in R['lid_contacts']),R['lid_contacts']
