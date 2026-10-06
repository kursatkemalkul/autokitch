"""Apply four catalog-length mounting screws; no supplier bodies or other stations."""
from lower_support import *
import pickle,hashlib,gzip
import k79_bound_removal_writer as W

def apply(source,dest):
 folder=OUT/'actuator_catalog_fastener_candidate'
 report=json.loads((folder/'audit.json').read_text(encoding='utf-8'))
 recipe=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()))
 assert report['passed_geometry_and_stacks'] and hashlib.sha256(source.read_bytes()).hexdigest()==report['source_model_sha256']
 path=OUT/'k1/k_parca_fluid_verified.pkl';P=pickle.loads(path.read_bytes())['P']
 assert hashlib.sha256(path.read_bytes()).hexdigest()==recipe['source_parts_sha256']
 assert set(recipe['parts'])=={f'DGRF_M10_civata_{i}' for i in range(4)}
 repairs={};entries={}
 for a,r in recipe['parts'].items():
  old=P[a]
  repairs[a]={'original_triangles':old['V'][old['F']].tolist(),'vertices':r['V'],'triangles':r['F'],'proof':{'part':a,'closed_status':'Error.NoError','maximum_declared_precision_adjustment_mm':.001,'purpose':'Our ISO4762 M10x35 A2-70 bolt: actual35mm stem,8mm hex drive,18.5mm blind engagement; factory housing unchanged'}}
  v=np.asarray(r['V']);lo=v.min(0);hi=v.max(0)
  entries[a]={'dugum':old['dugum'],'kutu':[lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]],'tur':'baglanti','bom':r.get('description')}
 recipepath=folder/'source_repair_recipe.json.gz'
 recipepath.write_bytes(gzip.compress(json.dumps({'source_model_sha256':report['source_model_sha256'],'repairs':repairs,'additional_parts':{}},separators=(',',':')).encode(),mtime=0))
 W.apply(source,dest,recipepath,expected_names=set(repairs),step=79,source_nodes=sorted({P[a]['dugum'] for a in repairs}),additional_parts={})
 dest.with_name(dest.stem+'_ent.json').write_text(json.dumps(clean({'adim':79,'prototype':'Four catalog ISO4762M10x35 A2-70 screws; actual hex drive; not full release','parca':entries}),indent=2),encoding='utf-8')

if __name__=='__main__':
 apply(*map(Path,sys.argv[1:3]));sys.stdout.flush();os._exit(0)
