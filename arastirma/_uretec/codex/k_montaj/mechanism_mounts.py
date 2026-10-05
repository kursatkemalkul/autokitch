"""Real K belt/pusher foot mounting, reserved local step72. World mm.

Two identical 4mm pusher plates retain all mechanism heights. M5/M6
bolts get supplementary ISO10511 nuts underneath the short catalogue PEMs:
the thin PEM alone is not counted as full-diameter thread engagement.
"""
from lower_support import *

def build_mounts():
    parts=[];joins=[];replacements=[]
    def add(p):parts.append(p);return p
    def plate(name,center,width,t,y,holes):
        x,z=center;s=S.Sac(name,rol='braket',t=t,R=1.5*t,birim='K_ITICI')
        q=s.taban([(x-width/2,-z-width/2),(x+width/2,-z-width/2),(x+width/2,-z+width/2),(x-width/2,-z+width/2)],O=(0,y,0),ex=(1,0,0),ey=(0,0,-1))
        for xx,zz,d in holes:q.delik(xx,-zz,d,tip='vida_deligi')
        p=s.parca();p['flat']=s.acinim();p['dfm']=clean(s.dfm(abkant=False));return add(p)
    def joint(dis,x,z,seat,length,lower_washers):
        screw=add(S.vida('ISO4762',dis,length,(x,seat,z),(0,-1,0),ad=f'k72_vida_{dis}_{x}_{z}',birim='K_BAGLANTI'))
        uw=add(S.pul('DIN125',dis,(x,seat,z),(0,-1,0),ad=f'k72_ust_pul_{dis}_{x}_{z}',birim='K_BAGLANTI'))
        sp,c,_=S.pem_somun('SP',dis,(x,889,z),(0,-1,0),3)
        y=sp['sh'].BoundingBox().ymin
        names=[screw['ad'],uw['ad']]
        for i in range(lower_washers):
            w=add(S.pul('DIN125',dis,(x,y,z),(0,-1,0),ad=f'k72_alt_pul_{dis}_{x}_{z}_{i}',birim='K_BAGLANTI'));y-=w['meta']['h'];names.append(w['ad'])
        nut=add(S.somun('ISO10511',dis,(x,y,z),(0,-1,0),ad=f'k72_alt_somun_{dis}_{x}_{z}',birim='K_BAGLANTI'))
        end=y-nut['meta']['m'];protrusion=end-(seat-length);pitch=.8 if dis=='M5' else 1.
        assert pitch-.001<=protrusion<=3*pitch+.001,(dis,protrusion)
        names.append(nut['ad']);joins.append({'id':f'{dis}_{x}_{z}','axis':[0,-1,0],'center_mm':[x,seat,z],'standard':'ISO4762 + ISO7089 + ISO10511','length_mm':length,'engagement_mm':nut['meta']['m'],'nominal_diameter_mm':int(dis[1:]),'protrusion_mm':protrusion,'protrusion_threads':protrusion/pitch,'parts':names,'lower_nut_required_before_load':True})
    for x,z in PEM6:
        tag=f'{x}_{z}'
        plate('k72_bant_ayak_flansi_'+tag,(x,z),32,3,892,[(x,z,6.6)])
        leg=K.Profil('k72_bant_ayagi_'+tag,'y',895,932.5,(x,z),b=20,t=2,Ro=4)
        add(leg.parca());joint('M6',x,z,896.6,20,1)
        replacements.append({'node':'K_BANT__sac','center_xz':[x,z],'lo_y':892,'hi_y':932.5,'width_xz':20})
        for e in range(4):
            a=[(x-6,895,z-10),(x+10,895,z-6),(x+6,895,z+10),(x-10,895,z+6)][e]
            b=[(x+6,895,z-10),(x+10,895,z+6),(x-6,895,z+10),(x-10,895,z-6)][e]
            n=[(0,0,-1),(1,0,0),(0,0,1),(-1,0,0)][e]
            add(S.kaynak_dikisi(a,b,n,(0,1,0),1.5,ad=f'k72_bant_ayak_kaynagi_{tag}_{e}',birim='K_BANT',not_='TIG 141 ER308LSi'))
    for x in (4040.,4360.):
      for z in (-755.,-645.):
        xx=4054. if x==4040 else 4346.
        holes=[(xx,z+dz,5.5) for dz in (-14.,14.)]
        # 5.5 mm laser holes are smaller than 6 mm stock's permitted minimum.
        # Two identical allowed 4 mm plates avoid that manufacturing failure
        # and retain the source's 8 mm mounting height without a small shim.
        plate(f'k72_itici_taban_{x}_{z}',(x,z),58,4,892,holes)
        plate(f'k72_itici_ust_plaka_{x}_{z}',(x,z),58,4,896,holes)
        replacements.append({'node':'K_ITICI__sac','center_xz':[x,z],'lo_y':892,'hi_y':900,'width_xz':36})
        for _,zz,_ in holes:joint('M5',xx,zz,901,20,1)
        for e in range(4):
            a=[(x-8,900,z-10),(x+10,900,z-8),(x+8,900,z+10),(x-10,900,z+8)][e]
            b=[(x+8,900,z-10),(x+10,900,z+8),(x-8,900,z+10),(x-10,900,z-8)][e]
            n=[(0,0,-1),(1,0,0),(0,0,1),(-1,0,0)][e]
            add(S.kaynak_dikisi(a,b,n,(0,1,0),1.,ad=f'k72_itici_ayak_kaynagi_{x}_{z}_{e}',birim='K_ITICI',not_='TIG 141 ER308LSi'))
        # Continuous sealed perimeter joins the two plates before post load.
        for e in range(4):
            a=[(x-29,896,z-29),(x+29,896,z-29),(x+29,896,z+29),(x-29,896,z+29)][e]
            b=[(x+29,896,z-29),(x+29,896,z+29),(x-29,896,z+29),(x-29,896,z-29)][e]
            n=[(0,0,-1),(1,0,0),(0,0,1),(-1,0,0)][e]
            add(S.kaynak_dikisi(a,b,n,(0,1,0),1.,ad=f'k72_itici_ara_kaynagi_{x}_{z}_{e}',birim='K_ITICI',not_='TIG 141 ER308LSi; continuous, grind and passivate'))
    report={'step':72,'connections':joins,'replace':replacements,'manufacturing_heights_preserved':True,'mounting_release':False}
    return parts,report

if __name__=='__main__':
    parts,r=build_mounts();S.glb_yaz(str(OUT/'k72_mounts.glb'),parts)
    (OUT/'k72_mounts.json').write_text(json.dumps(clean(r),ensure_ascii=False,indent=2),encoding='utf8')
    print('MOUNT_PARTS',len(parts),'JOINTS',len(r['connections']),flush=True)
    sys.stdout.flush();os._exit(0)
