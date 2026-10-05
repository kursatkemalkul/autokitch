"""Read-only physical scaling + audit of actual V2 run outputs.

Run with numpy. No Isaac dependency. Outputs are experiment documentation only.
"""
from pathlib import Path
import json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'arastirma/3_TOPPING/sucuk_v2';OUT.mkdir(parents=True,exist_ok=True)
assumptions={'food_density_kg_m3':1000,'nominal_side_mm':8,'side_range_mm':[6,10],
    'target_g':70,'stock_g':2800,'dough_thickness_mm':8,
    'note':'Recipe, temperature, surface adhesion and friction need measurement.'}
# All lengths read from the current scene configuration where possible.
cfg=json.loads((ROOT/'otonom/hat3d/sim_makine.json').read_text(encoding='utf-8'))
slot=next(s for s in cfg['yuvalar'] if s['cad']=='sucuk_cad_v7')
assert slot['doz_g']==70
cube_mass=.008**3*1000*1000
usable_r=.125
calc={'input_status':'VARSAYIM except recorded design dimensions/dose/stock',
    'assumptions':assumptions,'nominal_cube_mass_g':cube_mass,
    'nominal_cubes_per_dose':70/cube_mass,'dose_tolerance_example_66_to_74_percent':4/70*100,
    'nominal_projected_coverage_percent':70/cube_mass*.008**2/(math.pi*usable_r**2)*100,
    'ring_cv_iid_reference_percent_5_rings':math.sqrt(4/(70/cube_mass))*100,
    'contact_examples':[{'stiffness_N_m':k,'force_for_1mm_compression_N':k*.001,
        'damping_N_s_m':1.6*math.sqrt(k*cube_mass*.001)} for k in (1000,5000,20000)],
    'table_friction_requirement':[{'rpm':rpm,'mu_min_at_125mm':(rpm*2*math.pi/60)**2*usable_r/9.81,
        'edge_speed_mm_s':rpm*2*math.pi/60*usable_r*1000} for rpm in (15,20,30,35)],
    'free_fall_35mm':{'time_ms':math.sqrt(2*.035/9.81)*1000,'impact_m_s':math.sqrt(2*9.81*.035)},
    'screw_tip_force_upper_bound_N':[{'torque_Nm':t,'tangential_N':t/.034} for t in (1,3,5)],
    'limits':['Tangential force is NOT actual force on each cube or a crushing prediction.',
        'Compliant contacts allow overlap, not fracture or material deformation validation.',
        '70 g does not cover the entire dough surface: it is sparse toppings, not a paste.',
        'Random equal-mass sampling CV is a reference, not a mathematical lower bound.',
        'Friction bound assumes no adhesion and steady rotation; acceleration adds demand.']}
runs=[]
for path in sorted((OUT/'runs').glob('*.json')):
    r=json.loads(path.read_text());data=np.load(path.with_suffix('.npz'))
    xyz=data['xyz'];ts=data['time'];q=data['quat'];m=data['mass_kg']*1000;n=len(m)
    names=data['paths'].tolist();assert xyz.shape==(len(ts),n+6,3)
    assert len(names)==len(set(names)) and np.all(np.diff(ts)>0)
    assert np.isfinite(xyz).all() and np.isfinite(q).all()
    assert np.max(abs(np.linalg.norm(q,axis=2)-1))<1e-4
    ip=names.index('/World/PIDE');pp=xyz[-1,ip];pts=xyz[-1,:n]-pp
    rad=np.linalg.norm(pts[:,:2],axis=1)
    on=(rad<.140)&(pts[:,2]>0)&(pts[:,2]<.040)
    assert abs(m[on].sum()-r['last']['on_pide_g'])<1e-4
    rings=np.histogram(rad[on],np.sqrt(np.linspace(0,usable_r**2,6)),weights=m[on])[0]
    angle=np.arctan2(pts[:,1],pts[:,0]);sectors=np.histogram(angle[on],np.linspace(-np.pi,np.pi,9),weights=m[on])[0]
    cv=lambda a:float(np.std(a)/np.mean(a)*100) if np.sum(a)>0 else None
    sector_scan=[]
    for shift in np.linspace(0,np.pi/4,45,endpoint=False):
        ang=(angle[on]+shift+np.pi)%(2*np.pi)-np.pi
        h=np.histogram(ang,np.linspace(-np.pi,np.pi,9),weights=m[on])[0]
        if np.sum(h)>0:sector_scan.append(cv(h))
    stop=r.get('stopped_at') or ts[-1];mask=(ts>.5)&(ts<stop-.2)
    speeds={};turns={}
    for name,axis in [('HELEZON_KUP_SUCUK',2),('TABLA',3),('PIDE',3)]:
        j=next(i for i,p in enumerate(names) if p.endswith('/'+name))
        theta=np.unwrap(2*np.arctan2(q[:,j,axis],q[:,j,0]))
        rpm=np.gradient(theta,ts)*60/(2*np.pi)
        speeds[name]=float(np.median(rpm[mask])) if mask.any() else None
        turns[name]=float((theta[-1]-theta[0])/(2*np.pi))
    run={'tag':path.stem,'variant':r['variant'],'initial_g':r['initial_stock_g'],
        'on_pide_g':float(m[on].sum()),'dose_error_percent':float((m[on].sum()-70)/70*100),
        'preleak_g':r['pre_dose_leak_g'],'emitted_g':r['last']['emitted_g'],
        'outside_including_preleak_g':r['last']['outside_or_below_g'],
        'ring_mass_g':rings.tolist(),'ring_cv_percent':cv(rings),
        'sector_mass_g':sectors.tolist(),'sector_cv_percent':cv(sectors),
        'sector_cv_over_boundary_rotations':{'min':min(sector_scan),'mean':float(np.mean(sector_scan)),
                                            'max':max(sector_scan)} if sector_scan else None,
        'measured_rpm':speeds,'turns_including_tail':turns,'stop_time_s':r['stopped_at'],
        'virtual_feedback':r['feedback_is_virtual'],'material_assumptions':r['material_assumptions'],
        'motion_record_checks':'PASS'}
    runs.append(run)
    print(json.dumps(run),flush=True)
(OUT/'engineering_scales.json').write_text(json.dumps(calc,indent=2),encoding='utf-8')
(OUT/'run_comparison.json').write_text(json.dumps(runs,indent=2),encoding='utf-8')
print('SCALES',json.dumps(calc),flush=True)
