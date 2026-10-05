"""Six K supports: explicit bench clamps and weld-before-loading sequence.

Workshop fixture geometry is illustrative. Fixture and torch paths still need
solid collision checks; this is not the whole K animation/release.
"""
from lower_support import *
import math
source,_,_=build();by={p['ad']:p for p in source};parts=[];events=[];initial={};warnings=[]
def meshpart(name,shape,kind):
    p=S._bp(name,shape,'workshop fixture','Workshop tool; not installed in K','',mal='celik');p['scene_kind']=kind;parts.append(p);return p
def box(name,lo,hi,kind='fixture'):return meshpart(name,K.kutu(lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]),kind)
def event(op,nodes,text,**kw):
    e={'number':len(events)+1,'operation':op,'nodes':nodes,'text':text,**kw};events.append(e);return e['number']
box('stok_tezhagi_tabla',(4500,997,-780),(5300,1000,30),'stock_fixture')
for x,z in ((4520,-760),(5280,-760),(4520,10),(5280,10)):
    box(f'stok_tezhagi_ayak_{x}_{z}',(x-15,0,z-15),(x+15,997,z+15),'stock_fixture')
for x in PX:
  for z in PZ:
    tag=f'{int(x)}_{int(-z)}'
    # Individual fixture pedestals leave both flange ends accessible to clamps.
    box(f'fikstur_tabla_{tag}',(x-20,787,z-45),(x+20,791,z+45))
    box(f'fikstur_dikme_{tag}',(x-10,4,z-10),(x+10,787,z+10))
    box(f'fikstur_agir_taban_{tag}',(x-70,0,z-70),(x+70,4,z+70))
    group_names=[f'k71_alt_flans_{tag}',f'k71_dik_destek_{tag}',f'k71_disli_ust_kapak_{tag}']
    for i,name in enumerate(group_names):
        p=by[name];parts.append(p);b=p['sh'].BoundingBox();initial[name]=[600+90*i,1000-b.ymin,0]
    units={}
    for label,dz in (('arka',-33.),('on',33.)):
        zz=z+dz;prefix=f'fikstur_mengene_{tag}_{label}'
        frame=K.kutu(x+26,x+36,783,817,zz-5,zz+5).fuse(K.kutu(x-10,x+36,783,787,zz-5,zz+5)).fuse(K.kutu(x-10,x+36,805,817,zz-5,zz+5))
        frame=frame.cut(cylinder(x+8,804,zz,3.4,14))
        meshpart(prefix+'_govde',frame,'clamp_frame')
        screw=S.vida('ISO4762','M8',30,(x+8,828,zz),(0,-1,0),ad=prefix+'_mil');screw['scene_kind']='clamp_spindle';parts.append(screw)
        meshpart(prefix+'_pabuc',cylinder(x+8,795,zz,5,3),'clamp_jaw')
        units[label]=[prefix+'_govde',prefix+'_mil',prefix+'_pabuc']
        for name in units[label]:initial[name]=[120,0,0]
        for name in units[label][1:]:initial[name][1]=8
    foot,tube,cap=group_names
    arrive_foot=event('arrive',[foot],f'{tag}: delikli alt flans fikstür tablasına gelir.',start_mm=initial[foot],end_mm=[0,0,0],temporary_supported=True,load_allowed=False)
    close={}
    for label in ('arka','on'):
        names=units[label]
        event('clamp_arrive',names,f'{tag}: {label} mengene açık çeneyle yana girer.',start_mm=[120,0,0],end_mm=[0,0,0],jaw_extra_mm=8)
        close[label]=event('clamp_close',names[1:],f'{tag}: {label} mengene alt flansı fikstüre sıkar.',start_mm=[0,8,0],end_mm=[0,0,0],fixes=[foot],pitch_mm=1.25,rotating_node=names[1],pivot_mm=[x+8,828,z+(-33 if label=='arka' else 33)])
    events[arrive_foot-1]['fixed_at_step']=close['arka']
    arrive_tube=event('arrive',[tube],f'{tag}: boş profil sabit alt flansa iner.',start_mm=initial[tube],end_mm=[0,0,0],loads=[foot],temporary_supported=True,load_allowed=False)
    def weld(y,edge):
        a=[(x-17,y,z-20),(x+20,y,z-17),(x+17,y,z+20),(x-20,y,z+17)][edge]
        b=[(x+17,y,z-20),(x+20,y,z+17),(x-17,y,z+20),(x-20,y,z-17)][edge]
        n=[(0,0,-1),(1,0,0),(0,0,1),(-1,0,0)][edge];direction=np.array(n,dtype=float)+np.array([0,1 if y==795 else -1,0]);direction/=np.linalg.norm(direction)
        name=f'k71_kaynak_{tag}_{y}_{edge}';p=by[name];parts.append(p);initial[name]=None
        return event('weld',[name],f'{tag}: {"alt flans–profil" if y==795 else "profil–üst kapak"} TIG dikişi {edge+1}/4.',p0_mm=list(a),p1_mm=list(b),torch_outward=direction.tolist(),fixes=[tube if y==795 else cap],onto=foot if y==795 else tube,forming_material=True)
    # Alternate clamps: the opposite clamp remains engaged during obstructed
    # front/back welds. No moment exists with both clamps open.
    for label,edge in (('on',2),('arka',0)):
        names=units[label];event('clamp_open',names[1:],f'{tag}: karşı mengene sıkılı kalır; {label} çene açılır.',start_mm=[0,0,0],end_mm=[0,8,0],removes_fixture=label)
        event('clamp_retract',names,f'{tag}: {label} mengene torç yolu için yana çekilir.',start_mm=[0,0,0],end_mm=[120,0,0],jaw_extra_mm=8)
        number=weld(795,edge)
        if label=='on':events[arrive_tube-1]['fixed_at_step']=number
        event('clamp_arrive',names,f'{tag}: {label} mengene açık çeneyle geri gelir.',start_mm=[120,0,0],end_mm=[0,0,0],jaw_extra_mm=8)
        event('clamp_close',names[1:],f'{tag}: {label} mengene yeniden sıkar.',start_mm=[0,8,0],end_mm=[0,0,0],fixes=[foot],adds_fixture=label,pitch_mm=1.25)
    weld(795,1);weld(795,3)
    arrive_cap=event('arrive',[cap],f'{tag}: delinip M5 diş çekilmiş 6 mm kapak sabit profile iner.',start_mm=initial[cap],end_mm=[0,0,0],loads=[tube],temporary_supported=True,load_allowed=False)
    for edge in range(4):
        number=weld(883,edge)
        if edge==0:events[arrive_cap-1]['fixed_at_step']=number
    for e in events:
        if e.get('temporary_supported') and e['nodes'][0] in group_names:
            e['warning']=f'Geçici olarak dayalı — {e["fixed_at_step"]}. adımda sabitlenecek; önce üstüne yük konmaz.'
S.glb_yaz(str(OUT/'support_workshop.glb'),parts,tol=.05,aci=.25)
report={'kind':'support workshop sequence; not full K','units':'mm','product_parts':66,'events':events,'initial_offsets_mm':initial,'fixture_nodes':[p['ad'] for p in parts if p.get('scene_kind')],
        'manufacturing_before_workshop_not_animated':True,'fixture_tool_geometry':'illustrative; not purchase-approved','fixture_and_torch_paths_checked':False,'full_assembly_release':False}
(OUT/'support_workshop.json').write_text(json.dumps(clean(report),ensure_ascii=False,indent=2),encoding='utf8')
print('SUPPORT_WORKSHOP',len(parts),'PARTS',len(events),'EVENTS',flush=True);sys.stdout.flush();os._exit(0)
