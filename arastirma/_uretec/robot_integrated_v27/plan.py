"""Standard rectangular underfloor modules; preserve audited cable routes."""
from pathlib import Path
import json
from shapely.geometry import box, Polygon, LineString
from shapely.ops import unary_union
ROOT=Path(__file__).resolve().parents[3]
A=ROOT/'otonom/hat3d/robot-integrated-v27'
A.mkdir(parents=True,exist_ok=True)
old=json.loads((ROOT/'otonom/hat3d/robot-integrated-v25/floor_plan.json').read_text())
def polys(g):
    g=g.simplify(.000001,preserve_topology=True).buffer(0)
    return [{'outer':list(p.exterior.coords),'holes':[list(h.coords) for h in p.interiors]} for p in (g.geoms if hasattr(g,'geoms') else [g]) if p.geom_type=='Polygon' and p.area>1e-9]
def geom(rows):return unary_union([Polygon(p['outer'],p['holes']) for p in rows])
# Widths 200/300/400/500 mm, selected height 100 mm within OKA-G 40-140 range.
# Segments butt at the junction face. Open sidewalls provide real branch ports.
spec=[('ANA_ALT_500',[5.14,-.71,5.64,.81]),('ANA_UST_500',[5.14,.81,5.64,2.05]),
      ('MAKINE_300',[4.20,-.71,5.14,-.41]),('MAKINE_DIRSEK_300',[3.90,-.88,4.20,-.41]),
      ('ROBOT_QR_400',[3.07,1.65,5.14,2.05]),('ZINCIR_DIRSEK_400',[2.67,1.65,3.07,2.05]),
      ('ZINCIR_SABIT_400',[2.67,1.135,3.07,1.65]),('MOTOR_200',[4.925,.58,5.14,.78])]
rects=[box(*r) for _,r in spec];foot=unary_union(rects)
assert foot.geom_type=='Polygon'
assert sum(r.area for r in rects)-foot.area<1e-10
floor=box(.636,-.88,5.64,2.17)
ports=[];divider_ports=[];mouths=[]
for d in old['duct_specs']:
    if d['name']=='ZINCIR_GECIS':
        n=box(2.875,1.1447,3.045,1.2253)
    else:
        x,_,z=min(d['points'],key=lambda q:q[1])
        w=.080 if d['name']=='UR_CIKIS' else d['width_m']
        h=d['height_m']
        wx,wz=(w/2,h/2) if d['normal']==[0,0,1] else (h/2,w/2)
        n=box(x-wx-.0003,z-wz-.0003,x+wx+.0003,z+wz+.0003)
    mouths.append(n);ports.append(n.buffer(.020,join_style=2));divider_ports.append(n.buffer(.040,join_style=2))
lid_openings=unary_union(ports).intersection(foot)
openings=unary_union(divider_ports).intersection(foot)
necks=unary_union(mouths).intersection(foot)
wall=foot.difference(foot.buffer(-.0015))
ledges=foot.buffer(-.0015).difference(foot.buffer(-.014)).difference(lid_openings)
modules=[]
for name,r in zip([s[0] for s in spec],rects):
    # 0.2 mm butt seam, no interpenetrating duct bodies or covers.
    cut=r.buffer(-.0001,join_style=2)
    modules.append({'name':name,'bounds_xz':list(r.bounds),'bottom':polys(cut),
                    'side':polys(wall.intersection(cut)),
                    'divider':polys(cut.difference(openings)),
                    'cover':polys(cut.difference(lid_openings)),
                    'ledge':polys(ledges.intersection(cut))})
clear=[]
for name,c in old['cables'].items():
    ds=[]
    for a,b in zip(c['points'],c['points'][1:]):
        if max(a[1],b[1])<-.001:
            line=LineString([(a[0],a[2]),(b[0],b[2])])
            ds.append(line.distance(foot.boundary)-c['radius_m'])
            assert foot.buffer(-c['radius_m']-.002).covers(line),(name,a,b)
    clear.append({'cable':name,'side_clearance_m':min(ds) if ds else None})
sources=[{'system':'OBO OKA-G screed-flush, blind channel','widths_mm':[200,300,400,500],
          'height_selected_mm':100,'height_catalog_range_mm':[40,140],
          'source':'https://www.obo.global/es/productos/canal-a-ras-de-pavimento-ciego-altura-40-140-mm-2400-500-40-140-3-7424006.html'},
         {'system':'OBO OKA-G left/right junction construction set','examples':['7423950','7423970','7423952','7423972'],
          'source':'https://www.obo.global/products/construction-set-for-90-angle-to-right-height-40-150-mm-600-7423978.html'}]
out={'version':27,'step':96,'units':'m; Y up','floor_bounds':[[.636,-.88],[5.64,2.17]],
     'inner_size_m':[4.724,3.05],'floor':polys(floor.difference(foot)),
     'trench':polys(foot),'modules':modules,'flush_collars':polys(lid_openings.difference(necks)),
     'openings':polys(openings),'lid_passages':polys(necks),'cable_clearances':clear,
     'duct_body_bottom_y_m':-.100,'cover_top_y_m':0,'cover_t_m':.003,
     'divider_top_y_m':-.0375,'sheet_t_m':.0015,'sources':sources,
     'representation':'Dimensioned simplified catalogue layout; not an imported OEM STEP or manufacturing drawing.',
     'removal':'All v26 doors, desk, chair, sink, plumbing and partition; old shaped trench and extended floor. Controller cable exit widened to 80x70mm.',
     'open':['Final manufacturer part/configuration and cover floor-load approval','Final electrical circuit/protection and building installation','Pre-existing complete robot collision and physical grip verification']}
(A/'floor_plan.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps({'modules':len(modules),'connected':True,'cable_routes':len(clear),'floor_inner_m2':4.724*3.05}))
