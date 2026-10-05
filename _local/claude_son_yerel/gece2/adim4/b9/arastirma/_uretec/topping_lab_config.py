"""Pure, testable experiment specification; no USD or UI dependencies."""
from pathlib import Path
import json, math
from functools import lru_cache
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'arastirma/3_TOPPING/topping_lab_v1'
MY='/World/MAKINE/TOPPING'
PRODUCTS={
    'kasar':dict(slot='KASAR_KABI',x=1.2575,nozzle_y=.150,target_g=55.,rpm=32.,table_rpm=25.,
        mu=.35,stiffness=2000.,nominal_particle_kg=.000176,stock_g=8800.,law='kasar_v2/radius_law_v1.json'),
    'sucuk':dict(slot='KUP_SUCUK',x=1.4725,nozzle_y=.1525,target_g=70.,rpm=8.,table_rpm=20.,
        mu=.25,stiffness=5000.,nominal_particle_kg=.000512,stock_g=2800.,law='sucuk_v2/radius_law_v2.json')}
RECIPES={'kasar':['kasar'],'sucuk':['sucuk'],'karisik':['kasar','sucuk']}

def settings(recipe='karisik',mode='hazne',kasar=10.,sucuk=10.,variant='candidate',seed=7,**kw):
    assert recipe in RECIPES and mode in ('hazne','stok') and variant in ('candidate','baseline')
    for v in (kasar,sucuk):
        if not math.isfinite(v) or not 0<=v<=100:raise ValueError('Doluluk 0..100 olmali')
    doses={p:float(kw.get(p+'_g',PRODUCTS[p]['target_g'])) for p in PRODUCTS}
    if any(not math.isfinite(v) or not 0<v<=250 for v in doses.values()):raise ValueError('Doz 0..250 g olmali')
    dry=bool(kw.get('dry_run',False))
    return dict(recipe=recipe,mode=mode,fill_percent=dict(kasar=0. if dry else float(kasar),sucuk=0. if dry else float(sucuk)),
        variant=variant,seed=int(seed),doses_g=doses,dry_run=dry)

def charge(product,cfg):
    if cfg['fill_percent'][product]==0 and not (OUT/f'{product}_packing.json').exists():
        return dict(points=np.empty((0,3)),dimensions=np.empty((0,3)),mass_kg=np.empty(0),
            report=dict(requested_g=0.,actual_g=0.,count=0,nominal_hopper_percent=0.,two_day_stock_percent=0.,
                max_initial_z_m=None,fill_line_z_m=.592,bulk_density_g_ml_assumption=None))
    meta=json.loads((OUT/f'{product}_packing.json').read_text())
    pack=np.load(OUT/f'{product}_packing.npz')
    target=(meta['packed_max_g'] if cfg['mode']=='hazne' else PRODUCTS[product]['stock_g'])*cfg['fill_percent'][product]/100
    mass=pack['mass_kg'];n=0 if target==0 else int(np.searchsorted(np.cumsum(mass)*1000,target)+1)
    if cfg['mode']=='hazne' and cfg['fill_percent'][product]==100:n=len(mass)
    if n>len(mass):raise ValueError(f'{product}: istenen stok CAD icinde cakismasiz sigmiyor')
    return dict(points=pack['points'][:n].copy(),dimensions=pack['dimensions'][:n].copy(),mass_kg=mass[:n].copy(),
        report=dict(requested_g=target,actual_g=float(mass[:n].sum()*1000),count=n,
        nominal_hopper_percent=100*float(mass[:n].sum()*1000)/meta['nominal_full_g'],
        physical_initial_fill_percent=100*float(mass[:n].sum()*1000)/meta['packed_max_g'],
        two_day_stock_percent=100*float(mass[:n].sum()*1000)/PRODUCTS[product]['stock_g'],
        max_initial_z_m=float((pack['points'][:n,2]+pack['dimensions'][:n,2]/2).max()) if n else None,
        fill_line_z_m=meta['fill_line_world_z_m'],bulk_density_g_ml_assumption=meta['bulk_density_g_ml_assumption']))

@lru_cache(maxsize=2)
def radius_law(product):
    return json.loads((ROOT/'arastirma/3_TOPPING'/PRODUCTS[product]['law']).read_text())

def radius_x(product,progress):
    p=PRODUCTS[product]
    law=radius_law(product)
    r=float(np.interp(np.clip(progress,0,1),law['progress_knots'],law['radius_knots_mm']))*.001
    offset=abs(.170-p['nozzle_y'])
    return p['x']-math.sqrt(max(0.,r*r-offset*offset))
