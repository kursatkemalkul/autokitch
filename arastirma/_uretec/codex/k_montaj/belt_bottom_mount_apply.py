"""Apply actual bottom-access mounts after geometry/access checks, no release."""
from lower_support import *
import pickle,hashlib,gzip
import k79_bound_removal_writer as W

def apply(source,dest):
 folder=OUT/'belt_bottom_mount_candidate';data=json.loads((folder/'audit.json').read_text(encoding='utf-8'));access=json.loads((folder/'access_audit.json').read_text(encoding='utf-8'))
 recipe=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()));P=pickle.load((OUT/'k1/k_parca_belt_verified.pkl').open('rb'))['P']
 assert data['passed_geometry_only'] and access['passed_access_and_insertion_only']
 assert access['candidate_geometry_sha256']==hashlib.sha256((folder/'geometry.json.gz').read_bytes()).hexdigest()
 assert data['source_parts_sha256']==recipe['source_parts_sha256']==access['source_parts_sha256']==hashlib.sha256((OUT/'k1/k_parca_belt_verified.pkl').read_bytes()).hexdigest()
 expected_source=json.loads((OUT/'belt_support_candidate/source_geometry_audit.json').read_text(encoding='utf-8'))['output_sha256']
 assert hashlib.sha256(source.read_bytes()).hexdigest()==expected_source
 templates={'plate':'k72_bant_ayak_flansi_4065.0_-421.0','weld':'k79_bant_tapa_cevre_kaynagi_4065_-421','screw':'k72_vida_M6_4065.0_-421.0','washer':'k72_alt_pul_M6_4065.0_-421.0_0'}
 repairs={}
 for a in (templates['plate'],templates['weld']):
  p=P[a];repairs[a]={'original_triangles':p['V'][p['F']].tolist(),'vertices':p['V'].tolist(),'triangles':p['F'].tolist(),
   'proof':{'part':a,'closed_status':'Error.NoError','maximum_declared_precision_adjustment_mm':0.,'purpose':'unchanged render template, exact same source triangles'}}
 removals={a:{'original_triangles':P[a]['V'][P[a]['F']].tolist(),'reason':'Top-insert M6 support clamp and shelf PEM superseded by bottom-access screw and welded6mm threaded insert'} for a in recipe['superseded_parts']}
 extra={};entries={}
 for a,r in recipe['parts'].items():
  typ='plate' if r['tur']=='sac' else 'weld' if r['tur']=='kaynak' else 'washer' if 'pul' in a else 'screw'
  template=templates[typ]
  if a in P:
   repairs[a]={'original_triangles':recipe['original_repaired_triangles'][a],'vertices':r['V'],'triangles':r['F'],
    'proof':{'part':a,'closed_status':'Error.NoError','maximum_declared_precision_adjustment_mm':0.,'purpose':'Restore own32x32x3 laser flange and original6.6mm M6 hole, remove overlapping/nonmanifold source surfaces'}}
  else:extra[a]={'source_template':template,'vertices':r['V'],'triangles':r['F']}
  v=np.asarray(r['V'],float);lo=v.min(0);hi=v.max(0)
  entries[a]={'dugum':P[template]['dugum'],'kutu':[lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]],'tur':r['tur'],'bom':r['description']}
 payload=folder/'source_repair_recipe.json.gz'
 payload.write_bytes(gzip.compress(json.dumps({'source_model_sha256':expected_source,'repairs':repairs,'removed_parts':removals,'additional_parts':extra},separators=(',',':')).encode(),mtime=0))
 nodes=sorted(set(P[a]['dugum'] for a in list(repairs)+list(removals)))
 W.apply(source,dest,payload,expected_names=set(repairs),step=79,source_nodes=nodes,additional_parts=extra,removed_parts=removals)
 dest.with_name(dest.stem+'_ent.json').write_text(json.dumps(clean({'adim':79,'prototype':'bottom-access belt supports','removed_parts':recipe['superseded_parts'],'parca':entries}),indent=2),encoding='utf-8')
if __name__=='__main__':
 apply(*map(Path,sys.argv[1:3]));sys.stdout.flush();os._exit(0)
