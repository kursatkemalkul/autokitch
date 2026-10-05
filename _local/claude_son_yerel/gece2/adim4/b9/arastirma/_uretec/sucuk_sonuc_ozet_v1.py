"""Read-only validation of saved cube experiment records."""
import json
from pathlib import Path
import numpy as np

root=Path(__file__).resolve().parents[2]/'arastirma/3_TOPPING'
for folder in sorted(root.glob('sucuk_fizik_deney_v*')):
    for path in sorted(folder.glob('*.json')):
        r=json.loads(path.read_text())
        npz=path.with_suffix('.npz')
        if not npz.exists():continue
        d=np.load(npz)
        if 'quat' not in d:continue
        ts=d['time']; xyz=d['xyz']; q=d['quat']; paths=d['paths'].tolist()
        assert len(ts)==len(xyz)==len(q)==len(r['measurements'])
        assert len(paths)==r['count']+6 and len(paths)==len(set(paths))
        assert np.all(np.diff(ts)>0) and np.isfinite(xyz).all() and np.isfinite(q).all()
        assert np.max(abs(np.linalg.norm(q,axis=2)-1))<1e-4
        stop=r.get('stopped_at') or ts[-1]
        mask=(ts>.5)&(ts<stop-.2)
        speed={}
        for name,axis in [('HELEZON_KUP_SUCUK',2),('TABLA',3),('PIDE',3)]:
            j=next(i for i,p in enumerate(paths) if p.endswith('/'+name))
            theta=np.unwrap(2*np.arctan2(q[:,j,axis],q[:,j,0]))
            rpm=np.gradient(theta,ts)*60/(2*np.pi)
            speed[name]=round(float(np.median(rpm[mask])),2) if mask.any() else None
        j=paths.index('/World/PIDE'); pp=xyz[-1,j]; cubes=xyz[-1,:r['count']]
        rad=np.linalg.norm(cubes[:,:2]-pp[:2],axis=1)
        # Same geometric footprint/height rule as the experiment's live counter.
        # This is not a physical load-cell measurement or contact-force integration.
        on=(rad<.140)&(cubes[:,2]>pp[2])&(cubes[:,2]<pp[2]+.040)
        mass=int(on.sum())*.512
        assert abs(mass-r['last']['on_pide_g'])<1e-4
        rings=np.histogram(rad[on],np.sqrt(np.linspace(0,.125**2,6)))[0]
        cv=float(np.std(rings)/np.mean(rings)*100) if sum(rings)>0 else None
        print(json.dumps(dict(run=folder.name+'/'+path.stem,stock_g=r['initial_stock_g'],
            preleak_g=r['pre_dose_leak_g'],on_pide_g=round(mass,3),
            target_error_g=round(mass-r['target_g'],3),ring_counts=rings.tolist(),ring_cv=cv,
            measured_rpm=speed,frames=len(ts),paths=len(paths),finite_and_quat_checks='PASS')))
