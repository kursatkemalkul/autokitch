"""K lower shelf manufacturing definition (world mm), reserved step 71.

Keeps all station interfaces. Bottom fixings face upward: no intrusion into B.
Six hollow 40x40x1.5 supports; 6 mm tapped caps; M5x10 flush top screws.
This definition is not a production release or a completed animation audit.
"""
import sys
sys.dont_write_bytecode = True
exec(open(__file__.replace('lower_support.py','inspect_source.py'),encoding='utf-8-sig').read().split('g=K.kur();')[0])
import cadquery as cq
import numpy as np

PX=(4060.,4340.); PZ=(-700.,-379.,-58.)
PEM6=[(x,z) for x in (4065.,4335.) for z in (-421.,-3.)]
PEM5=[(x,z) for x in (4054.,4346.) for z in (-741.,-769.,-631.,-659.)]

def cylinder(x,y,z,r,h,axis=(0,1,0)):
    return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z),cq.Vector(*axis))

def build():
    parts=[]; joins=[]; holes=[]; welds=[]
    def add(p,stage,fix=None):
        p['stage']=stage; p['fixing']=fix; parts.append(p); return p
    def plate(name,x0,x1,y0,y1,z0,z1):
        sh=K.kutu(x0,x1,y0,y1,z0,z1)
        return S._bp(name,sh,'laser 304','Laser-cut AISI 304 plate',f'{x1-x0}x{z1-z0}x{y1-y0}',malzeme='AISI 304',birim='K_GOVDE',uretim=True,mal='sac')
    # Root extends only to bend tangent. Outer dimensions stay 390 x 812 x 30.
    shelf=S.Sac('k71_istasyon_rafi','braket',t=3,R=4.5,birim='K_GOVDE',bolge='sicrama')
    # 3 mm left overhang supplies the 2t edge ligament around unchanged
    # Ø16.4 service holes. Still wholly inside the K 4000..4400 envelope.
    q=shelf.taban([(4002.,-19.5),(4395.,-19.5),(4395.,777.5),(4002.,777.5)],O=(0,889,0),ex=(1,0,0),ey=(0,0,-1))
    # Side M8 interfaces are too close to a 30 mm bent return. Use two flat
    # welded side plates, avoiding a strained hole or changing F/E interfaces.
    fl=[q.flans(i,30,yon=-1,ad=f'kenar_{i}') for i in (0,2)]
    for x,z in ((4016.5,-569.86),(4016.5,-479.86)): q.delik(x,-z,16.4,tip='servis_deligi')
    for x,z,d in [(x,z,'M6') for x,z in PEM6]+[(x,z,'M5') for x,z in PEM5]:
        nut,c,_=S.pem_somun('SP',d,(x,889,z),(0,-1,0),3,ad=f'k71_raf_PEM_{d}_{x}_{z}',birim='K_GOVDE')
        q.delik(x,-z,c['delik'],tip='pem_somun',pem_tip='SP',kenar_min=c['kenar'],min_sac=3)
        add(nut,'shelf_pem','pressed into matching shelf hole')
    for x,z,direction in ((4005.,-720.,1),(4395.,-100.,-1)):
        side=plate(f'k71_raf_yan_sac_{int(x)}',x if direction==1 else x-3,x+3 if direction==1 else x,862,889,-777.5,19.5)
        sh=side['sh'].cut(cylinder(x-direction,877.1,z,6.8,5,axis=(direction,0,0)))
        side['sh']=sh;side['wp']=cq.Workplane('XY').add(sh)
        add(side,'shelf_weld','TIG weld along underside of top shelf')
        w=S.kaynak_dikisi((x+3*direction,889,-777.5),(x+3*direction,889,19.5),(direction,0,0),(0,-1,0),1.5,ad=f'k71_raf_yan_kaynagi_{int(x)}',birim='K_GOVDE',not_='TIG 141 ER308LSi')
        add(w,'shelf_weld','TIG fillet');welds.append(w['ad'])
    for x in PX:
      for z in PZ:
        tag=f'{int(x)}_{int(-z)}'
        foot=plate('k71_alt_flans_'+tag,x-20,x+20,791,795,z-45,z+45)
        cap=plate('k71_disli_ust_kapak_'+tag,x-20,x+20,883,889,z-20,z+20)
        fs=foot['sh']; cs=cap['sh']
        for dz in (-32.,32.):
            at=(x,788,z+dz)
            stud,c=S.pem_saplama('FHP','M5',15,at,(0,1,0),ad=f'k71_alt_saplama_{tag}_{dz}',birim='K_GOVDE',sac_ad='taban_sac_3')
            add(stud,'base_pem','pressed before base sheet installation')
            holes.append({'center':list(at),'diameter':c['delik'],'sheet':'taban_sac_3','stud':stud['ad']})
            fs=fs.cut(cylinder(x,790,z+dz,2.75,6))
            washer=add(S.pul('DIN125','M5',(x,795,z+dz),(0,1,0),ad=f'k71_alt_pul_{tag}_{dz}',birim='K_GOVDE'),'base_fastener','stud')
            wh=washer['meta']['h']
            nut=add(S.somun('ISO10511','M5',(x,795+wh,z+dz),(0,1,0),ad=f'k71_alt_somun_{tag}_{dz}',birim='K_GOVDE'),'base_fastener','stud')
            protrusion=803-(795+wh+nut['meta']['m']) if 'm' in nut['meta'] else None
            joins.append({'id':f'base_{tag}_{dz}','method':'PEM FHP-M5-15 + ISO7089 + ISO10511','axis':[0,1,0],'hole_mm':5.5,'engagement_mm':5.,'protrusion_mm':protrusion,'parts':[stud['ad'],foot['ad'],washer['ad'],nut['ad']]})
        for dx in (-10.,10.):
            xx=x+dx
            cs=cs.cut(cylinder(xx,882,z,2.1,8))
            q.delik(xx,-z,5.5,tip='vida_deligi')
            screw=add(S.vida('DIN7991','M5',10,(xx,892,z),(0,-1,0),ad=f'k71_ust_havsa_{tag}_{dx}',birim='K_GOVDE'),'shelf_fastener','tapped 6 mm top cap')
            joins.append({'id':f'top_{tag}_{dx}','method':'DIN7991 M5x10 in tapped 6 mm 304 cap','axis':[0,-1,0],'engagement_mm':6.,'protrusion_mm':1.,'parts':[screw['ad'],cap['ad'],shelf.ad]})
        foot['sh']=fs;foot['wp']=cq.Workplane('XY').add(fs)
        cap['sh']=cs;cap['wp']=cq.Workplane('XY').add(cs)
        add(foot,'support_weld','welded to hollow tube on bench')
        add(cap,'support_weld','welded to hollow tube on bench')
        profile=K.Profil('k71_dik_destek_'+tag,'y',795,883,(x,z),b=40,t=1.5,Ro=3)
        add(profile.parca(),'support_weld','four tube edges welded at foot and cap')
        for y,side in ((795,1),(883,-1)):
          for edge in range(4):
            a=[(x-17,y,z-20),(x+20,y,z-17),(x+17,y,z+20),(x-20,y,z+17)][edge]
            b=[(x+17,y,z-20),(x+20,y,z+17),(x-17,y,z+20),(x-20,y,z-17)][edge]
            n=[(0,0,-1),(1,0,0),(0,0,1),(-1,0,0)][edge]
            w=S.kaynak_dikisi(a,b,n,(0,side,0),1.,ad=f'k71_kaynak_{tag}_{y}_{edge}',birim='K_GOVDE',not_='TIG 141 ER308LSi; weld fixture holds before release')
            add(w,'support_weld','TIG fillet');welds.append(w['ad'])
    # Ream the countersink only after cutting: head is flush with food-side surface.
    sh=shelf.kati()
    for x in PX:
      for z in PZ:
       for dx in (-10.,10.):
        sh=sh.cut(cq.Solid.makeCone(5,2.75,2.8,cq.Vector(x+dx,892,z),cq.Vector(0,-1,0)))
    p=shelf.parca();p['sh']=sh;p['wp']=cq.Workplane('XY').add(sh);add(p,'shelf_install','12 flush top screws')
    return parts, {'step':71,'unit':'mm','bottom_holes':holes,'connections':joins,'welds':welds,'flat':shelf.acinim(),'dfm':clean(shelf.dfm(abkant=True)),'production_released':False},shelf

if __name__=='__main__':
    p,r,s=build(); S.glb_yaz(str(OUT/'k71_lower.glb'),p,tol=.05,aci=.25)
    (OUT/'k71_lower.json').write_text(json.dumps(clean(r),ensure_ascii=False,indent=2),encoding='utf8')
    print('LOWER_PARTS',len(p),'CONNECTIONS',len(r['connections']),'DFM',r['dfm'],flush=True)
    sys.stdout.flush();os._exit(0)
