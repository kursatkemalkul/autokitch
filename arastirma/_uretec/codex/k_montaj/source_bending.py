"""Invert source mesh onto native sheet panels/bend strips.

Keeps every original source triangle at the folded endpoint; no CAD mesh swap.
Unclassified vertices prevent acceptance. Workshop path/tool audits remain separate.
"""
from lower_support import *
from current_cad import factory_from_source
Y=H/'yama_v9'
for path in (Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(path))
from m8kit import Glb
factory=factory_from_source(K,OUT);model=Glb(str(OUT/'k73a.glb'))
source_bounds={r['id']:r for r in json.loads((OUT/'source_components.json').read_text(encoding='utf8'))['components']}
screen=json.loads((OUT/'sheet_surface_screen.json').read_text(encoding='utf8'))
eligible={r['sheet']:r for r in screen['sheets'] if r['status']=='SAMPLED_VERTICES_MATCH'}
limit=int(sys.argv[1]) if len(sys.argv)>1 else 999
records=[];errors=[]
for sheet in factory.SAC:
    if sheet.ad not in eligible:continue
    if len(records)>=limit:break
    ref=eligible[sheet.ad]['source_component'];name,num=ref.rsplit('[',1)
    # Step71 adds/removes components: numerical component IDs are not stable.
    # Identify current counterpart uniquely by six source bounds, then use its
    # actual triangles. Bounding boxes identify; they do not prove surface equality.
    old=source_bounds[ref];model.bilesen(name,0)
    candidates=[r for r in model._bc[name] if max(np.max(np.abs(r['lo']-old['lo'])),np.max(np.abs(r['hi']-old['hi'])))<.01]
    assert len(candidates)==1,(sheet.ad,'ambiguous current component',len(candidates))
    b=candidates[0];current_ref=f'{name}[{b["no"]}]'
    P=np.concatenate([p['X'][p['T'][indices]] for p,indices in b['parca']]);V,F=np.unique(P.reshape(-1,3),axis=0,return_inverse=True);F=F.reshape(-1,3)
    pk,sk=sheet._yerel_katilar();encoded=[];worst=0.;missing=[]
    for index,world in enumerate(V):
        point=world-[4000,0,0];record=None;reconstructed=None
        for panel in sheet.paneller:
            sh=pk.get(panel.no)
            if sh is None:continue
            local=S._p(np.linalg.inv(panel.M),point);bb=sh.BoundingBox()
            if not (bb.xmin-.001<=local[0]<=bb.xmax+.001 and bb.ymin-.001<=local[1]<=bb.ymax+.001 and -.001<=local[2]<=sheet.t+.001):continue
            if sh.distance(cq.Vertex.makeVertex(*local))>.001:continue
            record={'panel':panel.no,'point':local.tolist()};reconstructed=S._p(panel.M,local);break
        if record is None:
            for B in sheet.bukumler:
                local=S._p(np.linalg.inv(B.ebeveyn.M),point)
                A=B.p0+np.array([0.,0.,sheet.t+B.R if B.yon>0 else -B.R])
                diff=local-A;w=float(diff@B.e3);radial=diff-B.e3*w
                refvec=np.array([0.,0.,-1. if B.yon>0 else 1.]);ang=float(np.arctan2(radial@np.cross(B.k,refvec),radial@refvec));rho=float(np.linalg.norm(radial))
                if not (-.001<=ang/B.th<=1.001 and B.R-.001<=rho<=B.R+sheet.t+.001 and B.a-.001<=w<=B.b+.001):continue
                s=ang/B.th*B.BA;z=sheet.t+B.R-rho if B.yon>0 else rho-B.R
                record={'bend':B.no+1,'point':[s,w,z]}
                r0=np.array([0.,0.,-(B.R+sheet.t-z) if B.yon>0 else B.R+z])
                reconstructed=S._p(B.ebeveyn.M,A+S._rot(B.k,ang)@r0+B.e3*w);break
        if record is None:missing.append(index);encoded.append(None)
        else:encoded.append(record);worst=max(worst,float(np.linalg.norm(reconstructed-point)))
    bends=[]
    for B in sheet.bukumler:
        bends.append({'number':B.no+1,'parent':B.ebeveyn.no,'child':B.cocuk.no,'angle':B.th,'direction':B.yon,'BA':B.BA,'K':B.K,'p0':B.p0.tolist(),'axis':B.k.tolist(),'out':B.o3.tolist(),'edge':B.e3.tolist(),'flat_child':B.Ld.tolist()})
    order=next((r.get('sira') for r in sheet.dfm(abkant=True) if r.get('kural')=='abkant'),None) or [B.no+1 for B in sheet.bukumler]
    rec={'name':sheet.ad,'source_component':current_ref,'legacy_reference':ref,'root':sheet.paneller[0].M.tolist(),'source_offset':[4000,0,0],'t':sheet.t,'vertices':V.tolist(),'triangles':F.tolist(),'encoded_vertices':encoded,'bends':bends,'order':order,
         'unclassified_vertices':missing,'folded_endpoint_max_error_mm':worst,'endpoint_passed':not missing and worst<=.01}
    records.append(rec);errors.append({k:rec[k] for k in ('name','unclassified_vertices','folded_endpoint_max_error_mm','endpoint_passed')})
    print('SOURCE_BEND',sheet.ad,'vertices',len(V),'unclassified',len(missing),'endpoint',worst,flush=True)
import hashlib
r={'units':'mm','source_model':'k73a.glb','source_sha256':hashlib.sha256((OUT/'k73a.glb').read_bytes()).hexdigest(),'sheets':records,'tool_path_checked':False,'publish_allowed':False}
(OUT/'source_bending.json').write_text(json.dumps(clean(r),separators=(',',':')),encoding='utf8')
(OUT/'source_bending_audit.json').write_text(json.dumps(clean({'checks':errors,'all_screened_sheets_processed':len(records)==len(eligible),'passed':all(x['endpoint_passed'] for x in errors) and len(records)==len(eligible),'full_assembly_release':False}),indent=2),encoding='utf8')
sys.stdout.flush();os._exit(0 if all(x['endpoint_passed'] for x in errors) else 2)
