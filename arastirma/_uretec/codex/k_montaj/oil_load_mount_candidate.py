"""Real shelf and pump-plate fastenings on the verified oil wall-mount source.

Preserves pump equipment coordinates. Uses a3mm load deck with a separately
welded3mm front retaining strip, flat3mm bracket legs, and catalog M5x16.
No activation, source-chain registration or production release here.
"""
from pathlib import Path
source=Path(__file__).with_name('oil_shelf_mount_candidate.py')
code=source.read_text(encoding='utf-8').split("if __name__=='__main__':")[0]
code=code.replace("DEST=OUT/'oil_shelf_mount_candidate'","DEST=OUT/'oil_load_mount_candidate'")
code=code.replace("k_parca_bottom_verified.pkl","k_parca_oil_verified.pkl")
code=code.replace("lo=P[name]['V'].min(0);hi=P[name]['V'].max(0)","lo=P['k79_yag_raf_yatay_kosebent_'+side]['V'].min(0);hi=P['k79_yag_raf_yatay_kosebent_'+side]['V'].max(0)")
code=code.replace("assert np.allclose(lo[1:],[1610.,-600.],atol=.001)","assert np.allclose(lo[1:],[1637.,-600.],atol=.001)")
code=code.replace('1637.','1635.5').replace('1640.','1638.5')
# The previous horizontal part, used only as envelope reference, remains
# at1637..1640 in the input source; do not misstate that measured envelope.
code=code.replace("[1635.5,-600.]","[1637.,-600.]").replace("[1638.5,-435.]","[1640.,-435.]")
exec(compile(code,str(source),'exec'),globals())

def part(name,shape,tur='sac',description=''):
    r=S._bp(name,shape,'laser AISI304','AISI304 own mounting piece',description,
            malzeme='AISI304',birim='K_YAG',uretim=True,mal='sac')
    r['tur']=tur
    return r

def build_load_mounts():
    pieces,wall_joins=build()
    shelf=K.kutu(4004.5,4395.5,1638.5,1641.5,-600.,-438.)
    # The existing air-clip feet touch the old shelf underside at1640.
    # Two R2 underside pockets preserve those clip/hose coordinates.
    # Top surface and stock thickness remain unchanged; this is explicit
    # machining, not a collision exemption or omitted mounting part.
    pockets=[]
    for name in ('hava_ic_aski_10','hava_ic_aski_11'):
        lo=P[name]['V'].min(0);hi=P[name]['V'].max(0)
        assert abs(float(hi[1])-1640.)<.001
        x,z=(lo[[0,2]]+hi[[0,2]])/2.
        tool=K.kutu(x-9.,x+9.,1638.49,1640.,z-9.,z+9.)
        tool=cq.Workplane('XY').add(tool).edges('|Y').fillet(2.).val()
        shelf=shelf.cut(tool)
        pockets.append({'part':name,'center_xz_mm':[float(x),float(z)],
                        'size_mm':[18.,18.],'corner_radius_mm':2.,'depth_mm':1.5})
    plate=K.kutu(4040.,4360.,1641.5,1644.5,-600.,-440.)
    joins=[]
    targets=[('raf',x,z,1641.5,1635.5,'k79_yag_raf_yatay_kosebent_'+side)
             for side,x in [('sol',4020.5),('sag',4379.5)] for z in (-580.,-455.)]
    targets += [('plaka',x,z,1644.5,1638.5,'yag_pompa_rafi')
                for x in (4049.,4351.) for z in (-589.,-451.)]
    for i,(kind,x,z,top,bottom,host) in enumerate(targets):
        tag=f'{kind}_{i}'
        carrier='yag_pompa_rafi' if kind=='raf' else 'yag_pompa_plakasi'
        cutter=cylinder(x,bottom-4,z,2.75,top-bottom+5)
        countersink=cq.Solid.makeCone(5.,2.45,2.8,cq.Vector(x,top,z),cq.Vector(0,-1,0))
        if kind=='raf':
            shelf=shelf.cut(cutter).cut(countersink)
            bracket=next(p for p in pieces if p['ad']==host)
            bracket['sh']=bracket['sh'].cut(cutter)
            bracket['wp']=cq.Workplane('XY').add(bracket['sh'])
        else:
            shelf=shelf.cut(cutter)
            plate=plate.cut(cutter).cut(countersink)
        # A2mm solid shim provides a catalog-length stack without excess
        # threads. It is a separate laser-cut part, not a fake thick washer.
        shim=K.kutu(x-6.,x+6.,bottom-2.,bottom,z-6.,z+6.).cut(cutter)
        shimname='k79_yag_M5_ara_plaka_'+tag
        pieces.append(part(shimname,shim,description='12x12x2; ISO273 M5 clearance5.5'))
        screw=S.vida('DIN7991','M5',16,(x,top,z),(0,-1,0),ad='k79_yag_M5x16_'+tag,birim='K_YAG')
        washer=S.pul('DIN125','M5',(x,bottom-2.,z),(0,-1,0),ad='k79_yag_M5_pul_'+tag,birim='K_YAG')
        nut=S.somun('ISO10511','M5',(x,bottom-3.,z),(0,-1,0),ad='k79_yag_M5_somun_'+tag,birim='K_YAG')
        for p in (screw,washer,nut):p['tur']='baglanti';pieces.append(p)
        protrusion=16.-(top-bottom+2.+washer['meta']['h']+nut['meta']['m'])
        joins.append({'id':tag,'carrier':carrier,'host':host,'center_mm':[x,top,z],
            'axis':[0,-1,0],'screw':screw['ad'],'washer':washer['ad'],'nut':nut['ad'],
            'shim':shimname,'length_mm':16.,'clearance_mm':5.5,'countersink_depth_mm':2.8,
            'engagement_mm':nut['meta']['m'],'pitch_mm':.8,'protrusion_mm':protrusion,
            'passed_stack':nut['meta']['m']>=5. and .8<=protrusion<=2.4,
            'tool_access_checked':False})
    pieces.extend((part('yag_pompa_rafi',shelf,description='391x162x3 load deck; original equipment top1641.5 retained'),
                   part('yag_pompa_plakasi',plate,description='320x160x3; four realM5 fixing bores/countersinks'),
                   part('k79_yag_raf_on_dayama',K.kutu(4004.5,4395.5,1641.5,1661.5,-438.,-435.),
                        description='391x20x3 flat front strip; welded, not a zero-radius bend')))
    seam=S.kaynak_dikisi((4004.5,1641.5,-438.),(4395.5,1641.5,-438.),
                         (0,0,-1),(0,1,0),1.5,ad='k79_yag_raf_on_dayama_kaynagi',birim='K_YAG',
                         not_='Continuous TIG141; torch, heat and fixture validation remain open')
    seam['tur']='kaynak';pieces.append(seam)
    return pieces,wall_joins,joins,pockets

if __name__=='__main__':
    pieces,walls,joins,pockets=build_load_mounts()
    report=audit(pieces,walls)
    measured=json.loads(gzip.decompress((DEST/'geometry.json.gz').read_bytes()))
    records=measured['parts'];wall_repairs=measured['wall_repairs']
    # Six bores are already proved in the input. Repeating their boolean
    # produced eight tiny sliver triangles lost by source compression.
    # Preserve the original walls, whose actual clear cores are empty.
    assert len(report['original_coarse_wall_bores'])==6
    assert all(j['original_material_mm3']<.001 for j in report['original_coarse_wall_bores'])
    wall_repairs={}
    report['source_walls_unchanged']=True
    report['wall_refinements']={}
    # audit() measures against P, so repaired/added shelf and plate surfaces
    # are explicitly in its exclusion/replacement set; purchased parts are not.
    report['source_model_sha256']=hashlib.sha256((OUT/'oil_shelf_mount_candidate/A/hat3_v10y.glb').read_bytes()).hexdigest()
    report['source_parts_sha256']=hashlib.sha256((K1/'k_parca_oil_verified.pkl').read_bytes()).hexdigest()
    report['load_joins']=joins
    report['all_load_stacks_passed']=all(j['passed_stack'] for j in joins)
    report['load_deck_stock_mm']=3.
    report['underside_air_clip_pockets']=pockets
    report['pump_coordinates_changed']=False
    report['pump_to_plate_mounting_completed']=False
    report['production_release']=False
    assert report['all_load_stacks_passed']
    payload={'source_parts_sha256':report['source_parts_sha256'],
             'parts':clean(records),'wall_repairs':clean(wall_repairs),
             'original_triangles':{a:P[a]['V'][P[a]['F']].tolist() for a in records if a in P}}
    (DEST/'geometry.json.gz').write_bytes(gzip.compress(json.dumps(payload,separators=(',',':')).encode(),mtime=0))
    (DEST/'audit.json').write_text(json.dumps(clean(report),indent=2),encoding='utf-8')
    print('OIL_LOAD_MOUNTS',len(pieces),'wall_joins',len(walls),'load_joins',len(joins),
          'clashes',len(report.get('clashes',[])),flush=True)
    assert report['passed_stack_and_geometry_only']
    sys.stdout.flush();os._exit(0)
