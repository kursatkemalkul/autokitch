"""Replay the bound conveyor support recipe through the existing K writer."""
from lower_support import *
import importlib.util,pickle,hashlib,gzip
import panel_mount_candidate as PM
spec=importlib.util.spec_from_file_location('k_belt_writer',Path(__file__).with_name('78_k_sac_topolojisi.py'))
writer=importlib.util.module_from_spec(spec);spec.loader.exec_module(writer)

def apply(source,dest):
 folder=OUT/'belt_support_candidate';audit=json.loads((folder/'audit.json').read_text(encoding='utf-8'))
 recipe=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()))
 assert audit['passed'] and hashlib.sha256(source.read_bytes()).hexdigest()==audit['source_model_sha256']==recipe['source_model_sha256']
 assert audit['source_parts_sha256']==recipe['source_parts_sha256']
 repairs={};extra={};origin=np.array([4200.,920.,-220.])
 template=audit['unchanged_render_template'];post=audit['changed_parts'][0]
 for a,r in recipe['replacement_parts'].items():
  v=np.asarray(r['V'],float);f=np.asarray(r['F'],int);solid=PM.solid(v,f,origin)
  assert solid.volume()>0
  if a in recipe['original_triangles']:
   repairs[a]={'original_triangles':recipe['original_triangles'][a],'vertices':v.tolist(),'triangles':f.tolist(),'proof':{'part':a,'closed_status':str(solid.status()),'volume_mm3':solid.volume(),'maximum_declared_precision_adjustment_mm':0.,'purpose':'sealed conveyor support; actual belt seat unchanged','supplier_component_modified':False}}
  else:extra[a]={'source_template':template if r['tur']=='kaynak' else post,'vertices':v.tolist(),'triangles':f.tolist()}
 expected=set(audit['changed_parts'])|{template}
 assert set(repairs)==expected and set(extra)==set(recipe['added_parts']) and len(extra)==16
 payload=folder/'source_repair_recipe.json.gz';payload.write_bytes(gzip.compress(json.dumps({'source_model_sha256':audit['source_model_sha256'],'repairs':repairs},separators=(',',':')).encode(),mtime=0))
 writer.apply(source,dest,payload,expected_names=expected,step=79,source_nodes=('K_BANT__sac',),additional_parts=extra)
 entries={}
 for a,r in recipe['replacement_parts'].items():
  v=np.asarray(r['V']);lo=v.min(0);hi=v.max(0)
  entries[a]={'dugum':'K_BANT__sac','kutu':[float(lo[0]),float(hi[0]),float(lo[1]),float(hi[1]),float(lo[2]),float(hi[2])],'tur':r['tur'],'bom':r['description']}
 dest.with_name(dest.stem+'_ent.json').write_text(json.dumps({'adim':79,'prototype':'sealed conveyor support','parca':entries},indent=2),encoding='utf-8')

if __name__=='__main__':
 apply(*map(Path,sys.argv[1:3]));sys.stdout.flush();os._exit(0)
