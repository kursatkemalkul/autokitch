"""Transparent cheese engineering estimates and physical-run comparisons."""
from pathlib import Path
import json,math
import numpy as np
from kasar_akis_model_v2 import roberts
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'arastirma/3_TOPPING/kasar_v2'
OUT.mkdir(parents=True,exist_ok=True)

def capacity(p,starts=1,friction_deg=30):
    v,e,_,_=roberts(40,16,p,fi_s=friction_deg,agiz=starts)
    return v*e

q=capacity(30.17)
calc=dict(target_g=55,stock_2day_g=8800,body_mm=[280,325,360],
    main_capacity_ml_rev_estimate=q,
    end_capacity_old_ml_rev_estimate=capacity(36,2),end_capacity_candidate_ml_rev_estimate=capacity(60,2),
    nominal_g_rev_estimate=q*.6*.50,nominal_rpm_for_55g_10s=55/(q*.6*.50)*6,
    radial_gap_mm=2,old_end_channel_mm=15,new_end_channel_mm=27,
    particle_assumption_mm={'width':[3,4,5],'length':[6,10,14],'thickness':[3,4,5]},
    capacity_sensitivity=[dict(rho_bulk=rho,fill=fill,wall_friction_deg=friction,
        g_rev=capacity(30.17,friction_deg=friction)*rho*fill)
        for rho in [.40,.48,.55] for fill in [.35,.6,.8] for friction in [20,30,40]],
    assumptions=['Roberts granular flow approximation is not calibrated for adhesive cheese',
        'Bulk density and solid density are separate quantities; no direct interchange',
        'Friction, compliance, shred distribution, no adhesion, rigid pieces are uncalibrated',
        'Ring uniformity counts landed mass; no invented melting or smearing credit'],
    source_urls={
        'variable_pitch':'https://www.kwsmfg.com/engineering-guides/screw-conveyor/types-of-screw-feeders/',
        'temperature_matting':'https://pubmed.ncbi.nlm.nih.gov/23706488/',
        'shred_shapes':'https://www.urschel.com/cutting-applications/cheese-shreds/',
        'food_contact_POM_candidate':'https://www.ensingerplastics.com/en/shapes/acetal-tecaform-ah-natural'},
    open_risks=['2 mm radial tip gap can pinch 3-5 mm shreds; not a crushing test',
        'Removal of pegs may reduce clump breaking; compare with real cheese',
        'Closed shroud shorter than 2 inlet control pitches; idle flooding must be tested',
        'Full 8.8 kg contact load and 48-hour matting are not certified by partial-stock run',
        'Inherited v13 tray collider is a solid disc, not verified thin formed tray/pin pockets'])

def signed_rpm(quats,times,axis):
    # q_current * conjugate(q_previous), scalar-first; exact small relative angle.
    a=quats[1:];b=quats[:-1].copy();b[:,1:]*=-1
    v=a[:,:1]*b[:,1:]+b[:,:1]*a[:,1:]+np.cross(a[:,1:],b[:,1:])
    w=a[:,0]*b[:,0]-np.sum(a[:,1:]*b[:,1:],axis=1)
    return np.degrees(2*np.arctan2(v[:,axis],w))/np.diff(times)/6

results=[]
for file in sorted((OUT/'runs').glob('*.json')):
    r=json.loads(file.read_text());npz=file.with_suffix('.npz')
    if not npz.exists() or 'measurements' not in r:continue
    d=np.load(npz);names=d['paths'].tolist();n=r['count'];t=d['time'];mass=d['mass_kg']*1000
    xyz=d['xyz'][-1,:n];pp=d['xyz'][-1,names.index('/World/PIDE')];rr=np.linalg.norm(xyz[:,:2]-pp[:2],axis=1)
    on=(rr<.14)&(xyz[:,2]>pp[2])&(xyz[:,2]<pp[2]+.020)
    rings=np.histogram(rr[on],np.sqrt(np.linspace(0,.125**2,6)),weights=mass[on])[0]
    ang=np.arctan2(xyz[:,1]-pp[1],xyz[:,0]-pp[0])
    cvs=[]
    for shift in np.linspace(0,2*np.pi/8,45,endpoint=False):
        sectors=np.histogram((ang[on]+shift)%(2*np.pi),np.linspace(0,2*np.pi,9),weights=mass[on])[0]
        cvs.append(float(sectors.std()/sectors.mean()*100) if sectors.sum() else None)
    rpm=signed_rpm(d['quat'][:,names.index('/World/MAKINE/TOPPING/HELEZON_KASAR_KABI')],t,1)
    table_rpm=signed_rpm(d['quat'][:,names.index('/World/MAKINE/TOPPING/TABLA')],t,2)
    runmask=t[1:]<(r.get('stopped_at') or 1e9)
    results.append(dict(tag=file.stem,variant=r['variant'],stock_g=r['initial_stock_g'],on_pide_g=float(mass[on].sum()),
        emitted_g=r['last']['emitted_g'],preleak_g=r['pre_dose_leak_g'],
        all_outside_g=r['last']['outside_or_below_g'],
        on_usable_125mm_g=float(mass[on&(rr<.125)].sum()),
        on_edge_margin_g=float(mass[on&(rr>=.125)].sum()),
        stock_mass_consistent=bool(abs(float(mass.sum())-r['initial_stock_g'])<1e-5),
        rings_g=rings.tolist(),ring_cv_percent=float(rings.std()/rings.mean()*100) if rings.sum() else None,
        sector_cv_mean_percent=float(np.mean(cvs)) if all(x is not None for x in cvs) else None,
        actual_screw_rpm_median=float(np.median(rpm[runmask])) if runmask.any() else None,
        actual_table_rpm_median=float(np.median(table_rpm[runmask])) if runmask.any() else None,
        command_rpm=r['rpm'],table_rpm=r['table_rpm'],stop_at_s=r['stopped_at'],
        finite=bool(np.isfinite(d['xyz']).all() and np.isfinite(d['quat']).all()),
        max_quaternion_norm_error=float(np.max(abs(np.linalg.norm(d['quat'],axis=-1)-1)))))
(OUT/'engineering_calculations.json').write_text(json.dumps(calc,indent=2),encoding='utf-8')
(OUT/'run_comparison.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps({'design':{k:calc[k] for k in ['target_g','nominal_g_rev_estimate','nominal_rpm_for_55g_10s','end_capacity_old_ml_rev_estimate','end_capacity_candidate_ml_rev_estimate']},'runs':results},indent=2))
