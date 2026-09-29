"""Focused dimensional/solid checks plus truthful folding audit."""
import json
from pathlib import Path
import sys
import time
import cadquery as cq
import kutu_cad_v9 as K

OUT = Path(__file__).resolve().parents[2] / '_local' / 'kutu-v9'
OUT.mkdir(parents=True, exist_ok=True)
K.modul()
P = {p['ad']: p for p in K.PARCALAR}
def shape(p):
    vs = p['wp'].vals()
    return vs[0] if len(vs) == 1 else cq.Compound.makeCompound(vs)
def bounds(s):
    b=s.BoundingBox(); return [b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]
R={'parts':len(P), 'boxes':{}, 'changed_collisions':[], 'invalid':[], 'folding_open':[
    '804x404 is an assumed die line, not the selected suppliers drawing.',
    'Corner tab folders are absent; animated tab folding is prescribed, not physically driven.',
    'Crease forces, double-sheet separation, thickness tolerances and springback require samples.',
]}
changed=('asansor_motoru','asansor_motor_plakasi','asansor_kasnak_40','asansor_kasnak_20','asansor_kayisi','asansor_kayis_koruyucu','asansor_alt_yatak','asansor_vidasi_alt_ucu','sarjor_yan_kapisi','kilavuz_sag_tasiyici','asansor_ray_plakasi_flansi')
for a in changed:
    s=shape(P[a]); R['boxes'][a]=bounds(s)
    if not s.isValid(): R['invalid'].append(a)
    for b,q in P.items():
        if b==a or q['grup'].startswith('B_') or q['grup'] in ('SABIT_REF','PIZZA','CATAL','K_ITICI'): continue
        sh=shape(q)
        if not K._bb_kesisir(s.BoundingBox(),sh.BoundingBox()):continue
        # Existing shaft/pulley interference is an idealized bore, not a body clash.
        if (a.startswith('asansor_kasnak') and b in ('asansor_motoru','asansor_vidasi_alt_ucu','asansor_kayisi')) or (b.startswith('asansor_kasnak') and a in ('asansor_motoru','asansor_vidasi_alt_ucu','asansor_kayisi')):continue
        v=s.intersect(sh).Volume()
        if v>.5: R['changed_collisions'].append([a,b,round(v,3)])
R['motor_inside']=R['boxes']['asansor_motoru'][2]>=126
R['feet']=K.AYAK_XZ
R['side_door_outer_x']=R['boxes']['sarjor_yan_kapisi'][1]
R['elevator_new_part_collisions']=[]
for dy in (0,100,200,300,400,500,600,671.3):
    for p in P.values():
        if p['grup']!='ASANSOR':continue
        a=shape(p).translate((0,dy,0))
        for n in changed:
            if n in ('asansor_alt_yatak','asansor_vidasi_alt_ucu'):continue
            b=shape(P[n])
            if K._bb_kesisir(a.BoundingBox(),b.BoundingBox()):
                v=a.intersect(b).Volume()
                if v>.5:R['elevator_new_part_collisions'].append([dy,p['ad'],n,round(v,2)])
(OUT/'checks.json').write_text(json.dumps(R,indent=2,ensure_ascii=False),encoding='utf-8')
print('CHANGED PART CHECK', json.dumps(R,ensure_ascii=False), flush=True)
K.olcum()
# Refilling is a SIDE translation of 804 x 404 mm bundles, not a 450 mm door sweep.
door_parts={'sarjor_yan_kapisi','kilavuz_sag_uhmw','kilavuz_sag_tasiyici','sarjor_yan_kapisi_basac'}
R['refill']={'blank':[K.X_BL1-K.X_BL0,K.ZS1-K.ZS0], 'minimum_right_space':K.X_BL1-K.X_BL0,
             'suggested_service_space':900, 'opening':[758,412], 'bundle':50, 'bundle_mass_assumed_kg':8,
             'collisions':[],'note':'Door+guide removed/open; machine stopped; platform at bottom. Full-stack top-up is not assumed.'}
for ya in (240.5,500,898):
    # Right-hand portion and final placement of the entire 50-sheet bundle.
    envelope=K.kut(8,1634,ya,ya+80,K.ZS0,K.ZS1).val()
    for n,p in P.items():
        if n in door_parts or n=='karton_yigini' or p['grup'].startswith('B_'):continue
        s=shape(p)
        if not K._bb_kesisir(envelope.BoundingBox(),s.BoundingBox()):continue
        v=envelope.intersect(s).Volume()
        if v>.5:R['refill']['collisions'].append([ya,n,round(v,2)])
# Travel must retain the whole carriage on the rail, not merely avoid the upper bearing.
bb=lambda a:shape(P[a]).BoundingBox()
R['elevator_limits']={'nut_stroke':bb('asansor_ust_yatak').ymin-bb('asansor_somunu').ymax,
                      'rail_stroke':bb('asansor_rayi_0').ymax-max(bb(n).ymax for n in P if n.startswith('asansor_arabasi_0'))}
travel=min(R['elevator_limits'].values())
R['elevator_limits']['platform_top_limit']=K.Y_PLAT+travel
R['elevator_limits']['unfeedable_sheets_minimum']=int(__import__('math').ceil((K.Y_YIGIN_UST-K.Y_PLAT-travel)/K.T))
R['elevator_limits']['usable_sheets_upper_bound']=K.SARJOR_ADET-R['elevator_limits']['unfeedable_sheets_minimum']
# Inspect cardboard against ITSELF as well: older tests only compare box to machine.
panels=[p for p in P.values() if p['grup'].startswith('B_')]
R['cardboard_self_collisions']=[]
for t in (1.7,3,3.5,4,4.5,5,5.5,6,7,8,10,12,12.9):
    matrices=K.blank_dunya(t)
    shapes=[(p['ad'],K.uygula(shape(p),matrices[p['grup']])) for p in panels]
    for i,(an,a) in enumerate(shapes):
        for bn,b in shapes[i+1:]:
            if K._bb_kesisir(a.BoundingBox(),b.BoundingBox()):
                vol=a.intersect(b).Volume()
                if vol>1:R['cardboard_self_collisions'].append([t,an,bn,round(vol,2)])
print('AUDIT',json.dumps({k:R[k] for k in ('refill','elevator_limits','cardboard_self_collisions')},ensure_ascii=False),flush=True)
R['refill']['validated']=False
R['refill']['limitation']='The old hinge blocks do not define separate fixed/moving leaves. Static-block hits are not an open-door clearance certification.'
R['ready_for_manufacture']=False
R['audit_status']='FAIL: pre-existing missing corner actuators, unapproved die line, cardboard interference, incomplete refill hinge model and elevator end travel.'
if 'full' in sys.argv:
    R['machine_collisions']=list(map(str,K.cakisma().items()))
    R['box_collisions']=list(map(str,K.kutu_cakisma(anlar=K.KUTU_ANLARI+K.GECIS_ANLARI).items()))
    R['pizza_collisions']=list(map(str,K.pizza_cakisma().items()))
(OUT/'checks.json').write_text(json.dumps(R,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(R,indent=2,ensure_ascii=False),flush=True)
assert not R['invalid'] and not R['changed_collisions'] and R['motor_inside']
assert not R['elevator_new_part_collisions']
# Audit findings intentionally stay visible as failures above. They are NOT
# converted to a manufacturing pass by the mechanical regression test below.
if 'full' in sys.argv:
    assert not R['machine_collisions'] and not R['box_collisions'] and not R['pizza_collisions']
