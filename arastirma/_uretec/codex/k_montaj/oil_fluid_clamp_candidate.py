"""Hold the unchanged filter and return regulator with two offset3mm portals.

All new stock is2/3mm; four catalog M5x20 fixings pass through our drilled
feet, pump plate and shelf. No supplier body is drilled or altered.
This is a geometry prototype, not a released station or strength approval.
"""
import panel_mount_candidate as PM
from lower_support import *
import pickle,gzip,hashlib
K1=OUT/'k1';DEST=OUT/'oil_fluid_clamp_candidate';DEST.mkdir(exist_ok=True)
P=pickle.loads((K1/'k_parca_pump_verified.pkl').read_bytes())['P']
BASE=OUT/'oil_pump_clamp_candidate/A/hat3_v10za.glb'
ORIGIN=np.array([4150.,1685.,-520.])

def own(name,shape,tur='sac',description='',material='AISI304'):
    r=S._bp(name,shape,'laser stock or declared pad','Our removable pump mounting',description,
            malzeme=material,birim='K_YAG',uretim=True,mal='sac' if tur=='sac' else 'conta')
    r['tur']=tur;return r

def build_clamps():
    pieces=[];joins=[];holes=[]
    shelf=PM.solid(P['yag_pompa_rafi']['V'],P['yag_pompa_rafi']['F'],ORIGIN)
    plate=PM.solid(P['yag_pompa_plakasi']['V'],P['yag_pompa_plakasi']['F'],ORIGIN)
    old_shelf,old_plate=shelf,plate
    for i,x,center,radius,body_top,pad_half,body in [
        (0,4087.5,4080.,13.,1744.5,6.,'yag_emis_filtresi'),
        (1,4311.5,4295.,27.5,1761.5,17.,'yag_geri_basinc_regulatoru_KBP')]:
        outer=radius+8.;inner=radius+2.;top=body_top+2.
        poly=[(1647.5,-520.-outer),(top+8.,-520.-outer),(top+8.,-520.+outer),
              (1647.5,-520.+outer),(1647.5,-520.+inner),(top,-520.+inner),
              (top,-520.-inner),(1647.5,-520.-inner)]
        s=S.Sac(f'k79_yag_akis_portal_{i}','braket',t=3.,R=4.5,birim='K_YAG')
        s.taban(poly,O=(x,0,0),ex=(0,1,0),ey=(0,0,1))
        p=s.parca();p['tur']='sac';pieces.append(p)
        pieces.append(own(f'k79_yag_akis_ust_pad_{i}',K.kutu(x,x+3.,body_top,top-.1,-520.-pad_half,-520.+pad_half),
                          'mek','EPDM1.9mm hold-down pad; inlet/return hose remains outside the offset portal','EPDM food-compatible'))
        pieces.append(own(f'k79_yag_akis_pad_yapistirici_{i}',K.kutu(x,x+3.,top-.1,top,-520.-pad_half,-520.+pad_half),
                          'silikon','0.1mm retaining adhesive; supplier casing not changed','food-compatible silicone'))
        for side,z,span,leg in [
            ('on',-520.-outer-7.,(-520.-outer-16.,-520.-inner-1.),(-520.-outer,-520.-inner)),
            ('arka',-520.+outer+7.,(-520.+inner+1.,-520.+outer+16.),(-520.+inner,-520.+outer))]:
            tag=f'{i}_{side}';xx=x+1.5
            footname='k79_yag_akis_ayak_'+tag
            cutter=cylinder(xx,1626.5,z,2.75,22.)
            foot=K.kutu(x-8.,x+11.,1644.5,1647.5,*span).cut(cutter)
            foot=foot.cut(cq.Solid.makeCone(5.,2.45,2.8,cq.Vector(xx,1647.5,z),cq.Vector(0,-1,0)))
            pieces.append(own(footname,foot,description='3mm laser-cut clamp foot; M5 clearance5.5/countersink2.8'))
            shimname='k79_yag_akis_M5_ara_plaka_'+tag
            shim=K.kutu(xx-6.,xx+6.,1635.5,1638.5,z-6.,z+6.).cut(cutter)
            pieces.append(own(shimname,shim,description='12x12x3; catalog-length mounting stack'))
            bolt=S.vida('DIN7991','M5',20,(xx,1647.5,z),(0,-1,0),ad='k79_yag_akis_M5x20_'+tag,birim='K_YAG')
            washer=S.pul('DIN125','M5',(xx,1635.5,z),(0,-1,0),ad='k79_yag_akis_M5_pul_'+tag,birim='K_YAG')
            nut=S.somun('ISO10511','M5',(xx,1634.5,z),(0,-1,0),ad='k79_yag_akis_M5_somun_'+tag,birim='K_YAG')
            for item in (bolt,washer,nut):item['tur']='baglanti';pieces.append(item)
            vv,ff=PM.mesh(cutter);tool=PM.solid(vv,ff,ORIGIN)
            shelf=shelf-tool;plate=plate-tool
            seams=[]
            for face,xf,n in [('sol',x,(-1,0,0)),('sag',x+3.,(1,0,0))]:
                seam=S.kaynak_dikisi((xf,1647.5,leg[0]),(xf,1647.5,leg[1]),n,(0,1,0),1.5,
                         ad='k79_yag_akis_ayak_kaynagi_'+tag+'_'+face,birim='K_YAG',
                         not_='TIG141 ER308LSi; own portal-to-foot seam, tool/fixture gate remains open')
                seam['tur']='kaynak';pieces.append(seam);seams.append(seam['ad'])
            protrusion=20.-(3.+3.+3.+3.+washer['meta']['h']+nut['meta']['m'])
            joins.append({'id':tag,'portal':p['ad'],'foot':footname,'shim':shimname,'seams':seams,
                'screw':bolt['ad'],'washer':washer['ad'],'nut':nut['ad'],'center_mm':[xx,1647.5,z],
                'supplier_body':body,'axis':[0,-1,0],'engagement_mm':nut['meta']['m'],'pitch_mm':.8,'protrusion_mm':protrusion,
                'passed_stack':nut['meta']['m']>=5. and .8<=protrusion<=2.4,'tool_checked':False})
            holes.append({'center_mm':[xx,1641.5,z],'diameter_mm':5.5,
                          'parts':['yag_pompa_rafi','yag_pompa_plakasi']})
    repairs={}
    for name,solid,before in [('yag_pompa_rafi',shelf,old_shelf),('yag_pompa_plakasi',plate,old_plate)]:
        m=solid.to_mesh();repairs[name]={'V':np.asarray(m.vert_properties)[:,:3]+ORIGIN,
              'F':np.asarray(m.tri_verts,dtype=np.int32),'tur':'sac',
              'original_triangles':P[name]['V'][P[name]['F']],
              'added_material_mm3':float((solid-before).volume()),
              'removed_material_mm3':float((before-solid).volume()),
              'purpose':'Four actual Ø5.5 clamp holes; supplier equipment is unchanged'}
        assert repairs[name]['added_material_mm3']<1e-6
    return pieces,joins,repairs,holes

def audit_clamps(pieces,joins,repairs,holes):
    records={p['ad']:{'V':PM.mesh(p['sh'])[0],'F':PM.mesh(p['sh'])[1],
                      'tur':p['tur'],'description':p.get('bom')} for p in pieces}
    records.update(repairs)
    solids={a:PM.solid(np.asarray(r['V']),np.asarray(r['F']),ORIGIN) for a,r in records.items()}
    other={};clashes=[];crossings=[];own_clashes=[]
    for a,r in records.items():
        if a in repairs:continue # subtract-only; cannot increase previous intersections
        v=np.asarray(r['V']);lo=v.min(0);hi=v.max(0)
        for b,p in P.items():
            if b in records:continue
            bv=p['V'];blo=bv.min(0);bhi=bv.max(0)
            if np.any(np.minimum(hi,bhi)-np.maximum(lo,blo)<=.0005):continue
            try:
                if b not in other:other[b]=PM.solid(bv,p['F'],ORIGIN)
                volume=float((solids[a]^other[b]).volume())
                if volume>.02:clashes.append({'a':a,'source':b,'volume_mm3':volume})
            except AssertionError:
                triangles=bv[p['F']]
                triangles=triangles[np.all(triangles.max(1)>=lo-.01,axis=1)&np.all(triangles.min(1)<=hi+.01,axis=1)]
                n=int(PM.YD.poz_kesisim(np.asarray(v[np.asarray(r['F'])],float),np.asarray(triangles,float),.002).sum()) if len(triangles) else 0
                crossings.append({'a':a,'source':b,'crossing_pairs':n})
                if n:clashes.append(crossings[-1])
    for i,a in enumerate(records):
        for b in list(records)[i+1:]:
            volume=float((solids[a]^solids[b]).volume())
            if volume>.02:own_clashes.append({'a':a,'b':b,'volume_mm3':volume})
    report={'source_model_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),
       'source_parts_sha256':hashlib.sha256((K1/'k_parca_pump_verified.pkl').read_bytes()).hexdigest(),
       'joins':joins,'new_parts':[a for a in records if a not in P],
       'source_clashes':clashes,'own_clashes':own_clashes,'surface_checks':crossings,
       'drilled_holes':holes,'supplier_equipment_bodies_changed':False,
       'passed_geometry_and_stacks':not clashes and not own_clashes and all(j['passed_stack'] for j in joins),
       'pad_force_and_material_approval_checked':False,'manufacturing_release':False,'production_release':False}
    payload={'source_parts_sha256':report['source_parts_sha256'],'parts':clean(records),
       'original_triangles':{a:P[a]['V'][P[a]['F']].tolist() for a in records if a in P}}
    (DEST/'geometry.json.gz').write_bytes(gzip.compress(json.dumps(payload,separators=(',',':')).encode(),mtime=0))
    (DEST/'audit.json').write_text(json.dumps(clean(report),indent=2),encoding='utf-8')
    print('PUMP_CLAMPS',len(records),'passed',report['passed_geometry_and_stacks'],'clashes',clashes,own_clashes,flush=True)
    return report

if __name__=='__main__':
    r=audit_clamps(*build_clamps());sys.stdout.flush();os._exit(0 if r['passed_geometry_and_stacks'] else 2)

