"""Continuous neutral-line bend preparation for screened K sheets.

Produces workshop geometry only, not an installed/fixed K assembly.
"""
import sys
sys.dont_write_bytecode=True
exec(open(__file__.replace('bending_data.py','inspect_source.py'),encoding='utf-8-sig').read().split('g=K.kur();')[0])
import numpy as np
from current_cad import factory_from_source
factory=factory_from_source(K,OUT)
screen=json.loads((OUT/'sheet_surface_screen.json').read_text(encoding='utf8'))
eligible={r['sheet']:r for r in screen['sheets'] if r['status']=='SAMPLED_VERTICES_MATCH'}
dfm={r['name']:r for r in json.loads((OUT/'source_cad_full_dfm.json').read_text(encoding='utf8'))['sheets']}
def mesh(shape):
    vs,fs=shape.tessellate(.05,.25)
    return {'vertices':[[v.x,v.y,v.z] for v in vs],'triangles':[list(f) for f in fs]}
def child_transform(B,t,f):
    if f==0:return B.Ld
    th=B.th*f; R=B.BA/th-B.K*t
    A=B.p0+np.array([0.,0.,(t+R) if B.yon>0 else -R])
    rot=S._rot(B.k,th)
    return S._M(np.column_stack([rot@B.o3,B.e3,rot@np.array([0.,0.,1.])]),A+rot@(B.p0-A))
data=[];checks=[]
for sheet in factory.SAC:
    if sheet.ad not in eligible:continue
    pk,sk=sheet._yerel_katilar(); pan,ser=sheet._bolgeler()
    record={'name':sheet.ad,'source_component':eligible[sheet.ad]['source_component'],
            'source_equality':'sampled vertices only','t':sheet.t,'root':sheet.paneller[0].M.tolist(),
            'panels':[dict(number=P.no,mesh=mesh(pk[P.no])) for P in sheet.paneller if pk[P.no] is not None],
            'bends':[],'flat':sheet.acinim(),'installation_complete':False}
    for B in sheet.bukumler:
        blocks=[]
        for a,b,w0,w1 in S._dikd_ayir(ser[B.no],B.BA):
            # Constant topology: 32 longitudinal sectors, four corners/section.
            V=[];F=[]
            for i in range(33):
                s=a+(b-a)*i/32
                V.extend([[s,w0,0.],[s,w1,0.],[s,w1,sheet.t],[s,w0,sheet.t]])
            for i in range(32):
                for k in range(4):
                    u=4*i+k;v=4*i+(k+1)%4;x=v+4;y=u+4
                    F.extend([[u,v,x],[u,x,y]])
            F.extend([[0,2,1],[0,3,2],[128,129,130],[128,130,131]])
            blocks.append({'vertices':V,'triangles':F})
        record['bends'].append({'number':B.no+1,'parent':B.ebeveyn.no,'child':B.cocuk.no,
           'angle':B.th,'direction':B.yon,'BA':B.BA,'K':B.K,'p0':B.p0.tolist(),
           'axis':B.k.tolist(),'out':B.o3.tolist(),'edge':B.e3.tolist(),
           'flat_child':B.Ld.tolist(),'folded_child':B.Lb.tolist(),'strips':blocks})
        checks.append({'sheet':sheet.ad,'bend':B.no+1,'flat_transform_error_mm':float(np.max(np.abs(child_transform(B,sheet.t,0)-B.Ld))),
                       'folded_transform_error_mm':float(np.max(np.abs(child_transform(B,sheet.t,1)-B.Lb)))})
    ab=next((r for r in dfm[sheet.ad]['dfm'] if r.get('kural')=='abkant'),{})
    record['order']=ab.get('sira') or [B.no+1 for B in sheet.bukumler]
    # Transform consistency proves final CAD panel poses, not source mesh equality.
    data.append(record)
report={'source_step':61,'units':'mm','kind':'workshop_preparation_only','sheets':data,
        'excluded_sheets':[r['sheet'] for r in screen['sheets'] if r['sheet'] not in eligible],
        'publish_allowed':False,'installed_assembly_ready':False}
(OUT/'bending_data.json').write_text(json.dumps(report,ensure_ascii=False,separators=(',',':')),encoding='utf8')
check={'checks':checks,'endpoint_transform_passed':all(max(r['flat_transform_error_mm'],r['folded_transform_error_mm'])<=.01 for r in checks),
       'continuous_collision_checked':False,'source_full_equality_checked':False,'publish_allowed':False}
(OUT/'bending_check.json').write_text(json.dumps(check,ensure_ascii=False,indent=2),encoding='utf8')
print('SHEETS',len(data),'BENDS',len(checks),'endpoint transforms',check['endpoint_transform_passed'],flush=True)
sys.stdout.flush();os._exit(0)
