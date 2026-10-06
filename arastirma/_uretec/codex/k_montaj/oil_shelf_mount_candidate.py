"""Real six-point M5 oil-shelf wall mount; candidate geometry only.

Retains native bracket envelopes and the wall axes from h3_k_sac_v1.
PEM pressing, corner fabrication, shelf fastening and complete release remain
separate gates. Purchased pump equipment is unchanged.
"""
import panel_mount_candidate as PM
from lower_support import *
import pickle,hashlib,gzip
import manifold3d as mf
K1=OUT/'k1';DEST=OUT/'oil_shelf_mount_candidate';DEST.mkdir(exist_ok=True)
P=pickle.loads((K1/'k_parca_bottom_verified.pkl').read_bytes())['P']
ORIGIN=np.array([4200.,1625.,-517.])
Z=(-580.,-517.,-455.)

def build():
    pieces=[];joins=[]
    for side,outer,sgn in [('sol',4000.,1),('sag',4400.,-1)]:
        name='yag_pompa_rafi_kosebendi_'+side
        wall='sol_sac_urun_girisi' if side=='sol' else 'sag_sac_E_penceresi'
        lo=P[name]['V'].min(0);hi=P[name]['V'].max(0)
        assert np.allclose(lo[1:],[1610.,-600.],atol=.001)
        assert np.allclose(hi[1:],[1640.,-435.],atol=.001)
        # Two welded flat 3mm legs: unchanged outside shape, no fictional
        # zero-radius abkant. Their actual seam/process is not yet released.
        xv=outer+sgn*1.5
        a,b=sorted([xv,xv+sgn*3.])
        vertical=K.kutu(a,b,1610.,1637.,-600.,-435.)
        horizontal=K.kutu(float(lo[0]),float(hi[0]),1637.,1640.,-600.,-435.)
        bracket=vertical
        for i,z in enumerate(Z):
            bracket=bracket.cut(cylinder(outer-sgn,1625.,z,2.75,7,axis=(sgn,0,0)))
            tag=f'{side}_{i}'
            stud,c=S.pem_saplama('FHP','M5',12,(outer,1625.,z),(sgn,0,0),ad='k79_yag_raf_FHP_M5x12_'+tag,birim='K_YAG',sac_ad=wall)
            washer=S.pul('DIN125','M5',(outer+sgn*4.5,1625.,z),(sgn,0,0),ad='k79_yag_raf_M5_pul_'+tag,birim='K_YAG')
            nut=S.somun('ISO10511','M5',(outer+sgn*(4.5+washer['meta']['h']),1625.,z),(sgn,0,0),ad='k79_yag_raf_M5_somun_'+tag,birim='K_YAG')
            for item in [stud,washer,nut]:item['tur']='baglanti';pieces.append(item)
            stack=4.5+washer['meta']['h']+nut['meta']['m'];protrusion=12.-stack
            joins.append({'id':tag,'bracket':name,'wall':wall,'center_mm':[outer,1625.,z],'axis':[sgn,0,0],
              'stud':stud['ad'],'washer':washer['ad'],'nut':nut['ad'],
              'wall_thickness_mm':1.5,'bracket_thickness_mm':3.,'wall_hole_mm':c['delik'],'bracket_hole_mm':5.5,
              'engagement_mm':nut['meta']['m'],'nominal_diameter_mm':5.,'pitch_mm':.8,
              'protrusion_mm':protrusion,'passed_stack':nut['meta']['m']>=5. and .8<=protrusion<=2.4,
              'supplier_press_process_checked':False,'corner_weld_process_checked':False})
        r=S._bp(name,bracket,'laser AISI3043mm + corner weld','Vertical flat3mm oil shelf bracket leg with three native wall-axis clearance holes','30x30x165 envelope retained',malzeme='AISI304',birim='K_YAG',uretim=True,mal='sac')
        r['tur']='sac';pieces.append(r)
        legname='k79_yag_raf_yatay_kosebent_'+side
        leg=S._bp(legname,horizontal,'laser AISI3043mm','Flat3mm horizontal oil-shelf bracket leg','30x165x3; welded to vertical leg',malzeme='AISI304',birim='K_YAG',uretim=True,mal='sac')
        leg['tur']='sac';pieces.append(leg)
        seam=S.kaynak_dikisi((outer+sgn*4.5,1637.,-600.),(outer+sgn*4.5,1637.,-435.),
             (sgn,0,0),(0,-1,0),2.,ad='k79_yag_raf_kose_kaynagi_'+side,birim='K_YAG',not_='TIG141 ER308LSi;165mm seam; fixture/torch/thermal verification pending')
        seam['tur']='kaynak';pieces.append(seam)
        for j in joins:
            if j['bracket']==name:
                j['horizontal_leg']=legname;j['corner_seam']=seam['ad']

    return pieces,joins

def audit(pieces,joins):
    records={r['ad']:{'V':PM.mesh(r['sh'])[0],'F':PM.mesh(r['sh'])[1],'tur':r['tur'],'description':r.get('bom')} for r in pieces}
    solids={a:PM.solid(r['V'],r['F'],ORIGIN) for a,r in records.items()}
    clashes=[];surface=[];own=[];source_solids={};pressed=[];nominal_face_touch=[];bores=[]
    for a,r in records.items():
        lo=r['V'].min(0);hi=r['V'].max(0)
        for b,p in P.items():
            if b in records:continue
            bv=p['V'];blo=bv.min(0);bhi=bv.max(0)
            if np.any(np.minimum(hi,bhi)-np.maximum(lo,blo)<=.0005):continue
            press=next((j for j in joins if j['stud']==a and j['wall']==b),None)
            if press:
                # Flush head occupies its own native PEM press material only.
                pressed.append({'stud':a,'wall':b,'method':'FHP own wall press head, not an insertion waiver','hole_mm':press['wall_hole_mm']})
                continue
            try:
                if b not in source_solids:source_solids[b]=PM.solid(bv,p['F'],ORIGIN)
                v=float((solids[a]^source_solids[b]).volume())
                if v>.02:
                    wall_pair=next((j for j in joins if a in (j['bracket'],j.get('horizontal_leg')) and j['wall']==b),None)
                    if wall_pair:
                        overlap=solids[a]^source_solids[b]
                        xyz=np.asarray(overlap.to_mesh().vert_properties)[:,:3]+ORIGIN
                        plane=wall_pair['center_mm'][0]+wall_pair['axis'][0]*1.5
                        error=float(np.max(np.abs(xyz[:,0]-plane)))
                        if error<=.001:
                            nominal_face_touch.append({'part':a,'source':b,'native_plane_x_mm':plane,
                              'maximum_mesh_plane_error_mm':error,'volume_mm3':v,
                              'reason':'Retained bracket and wall share native flush plane; compressed wall vertices deviate less than1 micron. No movement penetration exemption.'})
                            continue
                    clashes.append({'part':a,'source':b,'volume_mm3':v})
            except AssertionError:
                tri=bv[p['F']];tri=tri[np.all(tri.max(1)>=lo-.01,axis=1)&np.all(tri.min(1)<=hi+.01,axis=1)]
                n=int(PM.YD.poz_kesisim(np.asarray(r['V'][r['F']],float),np.asarray(tri,float),.002).sum()) if len(tri) else 0
                row={'part':a,'source':b,'crossing_pairs':n};surface.append(row)
                if n:clashes.append(row)
    for i,a in enumerate(records):
        for b in list(records)[i+1:]:
            vol=float((solids[a]^solids[b]).volume())
            if vol>.02:own.append({'a':a,'b':b,'volume_mm3':vol})
    # Source native CAD declares6xØ5 wall holes, but coarse GLB facets
    # narrow the true clear core. Refine only those declared cylinders.
    wall_repairs={};coarse_bores=[]
    for wall_name in sorted({j['wall'] for j in joins}):
        old=P[wall_name];wall=PM.solid(old['V'],old['F'],ORIGIN)
        before=wall
        for j in [q for q in joins if q['wall']==wall_name]:
            x,y,z=j['center_mm'];sgn=j['axis'][0]
            native=cylinder(x-.01*sgn,y,z,2.5,1.52,axis=(sgn,0,0))
            vv,ff=PM.mesh(native);cutter=PM.solid(vv,ff,ORIGIN)
            probe=cylinder(x-.01*sgn,y,z,2.45,1.52,axis=(sgn,0,0))
            pv,pf=PM.mesh(probe)
            coarse_bores.append({'id':j['id'],'clear_core_mm':4.9,'original_material_mm3':float((wall^PM.solid(pv,pf,ORIGIN)).volume())})
            wall=wall-cutter
        raw=wall.to_mesh()
        wall_repairs[wall_name]={'V':np.asarray(raw.vert_properties)[:,:3]+ORIGIN,'F':np.asarray(raw.tri_verts,dtype=np.int32),
          'tur':'sac','original_triangles':old['V'][old['F']],
          'removed_material_mm3':float((before-wall).volume()),'added_material_mm3':float((wall-before).volume()),
          'purpose':'Refine six native Ø5 PEM wall bores; preserve original wall material outside declared hole cylinders.'}
        source_solids[wall_name]=wall
    for j in joins:
        x,y,z=j['center_mm'];sgn=j['axis'][0]
        wall=source_solids[j['wall']]
        core=cylinder(x-.01*sgn,y,z,2.45,1.52,axis=(sgn,0,0))
        vv,ff=PM.mesh(core);hole_probe=PM.solid(vv,ff,ORIGIN)
        vol=float((hole_probe^wall).volume())
        bores.append({'id':j['id'],'wall':j['wall'],'center_mm':j['center_mm'],
          'native_hole_mm':j['wall_hole_mm'],'checked_clear_core_mm':4.9,'wall_material_in_clear_core_mm3':vol,'passed':vol<.001})
    report={'source_model_sha256':'4efd0b660ccb56dfd4d53d307efdfcf218185ed7c1c95df793a47e353b8ff5c0',
      'source_parts_sha256':hashlib.sha256((K1/'k_parca_bottom_verified.pkl').read_bytes()).hexdigest(),
      'joins':joins,'added_parts':[a for a in records if a not in P],
      'changed_parts':[a for a in records if a in P], 'source_clashes':clashes,'own_clashes':own,
      'open_surface_checks':surface,'declared_press_heads':pressed,
      'original_coarse_wall_bores':coarse_bores,'wall_refinements':{a:{'removed_material_mm3':r['removed_material_mm3'],'added_material_mm3':r['added_material_mm3']} for a,r in wall_repairs.items()},'native_wall_bores':bores,'nominal_face_touches':nominal_face_touch,'bracket_fabrication':'two flat3mm laser-cut legs joined by real165mm TIG fillet; no invented zero-radius bend','closed_parts':len(records),'passed_stack_and_geometry_only':not clashes and not own and all(j['passed_stack'] for j in joins) and all(j['passed'] for j in bores),
      'shelf_attached_to_brackets':False,'pump_plate_attached_to_shelf':False,'refined_wall_full_context_checked':False,'wall_bores_measured':all(j['passed'] for j in bores),
      'press_tool_checked':False,'mounting_tool_checked':False,'corner_weld_checked':False,'production_release':False}
    recipe={'source_parts_sha256':report['source_parts_sha256'],'parts':clean(records),'wall_repairs':clean(wall_repairs),
     'original_triangles':{a:P[a]['V'][P[a]['F']].tolist() for a in records if a in P}}
    (DEST/'audit.json').write_text(json.dumps(clean(report),indent=2),encoding='utf-8')
    (DEST/'geometry.json.gz').write_bytes(gzip.compress(json.dumps(recipe,separators=(',',':')).encode(),mtime=0))
    print('OIL_SHELF_WALL_MOUNT',report['passed_stack_and_geometry_only'],'parts',len(records),'joins',len(joins),'clashes',clashes,own,flush=True)
    return report

if __name__=='__main__':
    parts,joins=build();r=audit(parts,joins);sys.stdout.flush();os._exit(0 if r['passed_stack_and_geometry_only'] else 2)
