"""Actual 2 mm arrival-path audit for six K support bench subassemblies.

Scope excludes fixtures, welding tool and installation in K; no §5 release.
"""
from lower_support import *
parts,report,_=build();by={p['ad']:p for p in parts};groups=[];clashes=[];samples=0
for x in PX:
    for z in PZ:
        tag=f'{int(x)}_{int(-z)}'
        names=[f'k71_alt_flans_{tag}',f'k71_dik_destek_{tag}',f'k71_disli_ust_kapak_{tag}']
        fixed=[];steps=[]
        for name in names:
            p=by[name];sh=p['sh'];tested=0
            for dy in range(100,-1,-2):
                moving=sh.translate((0,dy,0));a=moving.BoundingBox()
                for mate in fixed:
                    b=mate['sh'].BoundingBox()
                    if min(a.xmax,b.xmax)<max(a.xmin,b.xmin) or min(a.ymax,b.ymax)<max(a.ymin,b.ymin) or min(a.zmax,b.zmax)<max(a.zmin,b.zmin):continue
                    v=moving.intersect(mate['sh']).Volume();tested+=1
                    if v>.01:clashes.append({'moving':name,'fixed':mate['ad'],'offset_y_mm':dy,'volume_mm3':v})
                samples+=1
            fixed.append(p)
            steps.append({'part':name,'approach_mm':[0,100,0],'sample_spacing_mm':2,'samples':51,'solid_pair_tests':tested,'final_translation_mm':[0,0,0],
                          'temporary_support_required':True,'fixture_checked':False})
        groups.append({'support':tag,'steps':steps,'bottom_welds':[p['ad'] for p in parts if p['ad'].startswith(f'k71_kaynak_{tag}_795_')],
                       'top_welds':[p['ad'] for p in parts if p['ad'].startswith(f'k71_kaynak_{tag}_883_')]})
r={'scope':'six bench support arrivals only','units':'mm','groups':groups,'samples':samples,'unintended_intersections':clashes,
   'arrival_paths_passed':not clashes,'fixture_load_and_torch_verified':False,'installation_in_K_verified':False,'full_assembly_release':False}
(OUT/'support_motion_audit.json').write_text(json.dumps(clean(r),ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'sampled_poses':samples,'intersections':len(clashes),'arrival_paths_passed':not clashes,'full_assembly_release':False}),flush=True)
sys.stdout.flush();os._exit(0 if not clashes else 2)
