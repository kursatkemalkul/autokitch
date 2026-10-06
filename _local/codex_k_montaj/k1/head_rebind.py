"""Bind all current head parts to every nondegenerate source triangle, or reject."""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k78_rebind_ownership.py'
code=source.read_text(encoding='utf-8').replace("previous_path=H/'k_parca.pkl'","previous_path=H/'k_parca_catalog_verified.pkl'").replace('if manifest.exists():previous_path=','if False:previous_path=')
for old,new in [('k_parca78_raw.pkl','k_parca_head_raw.pkl'),('k_parca78_verified.pkl','k_parca_head_verified.pkl'),('step78_ownership_rebind_audit.json','head_ownership_rebind_audit.json'),('surface_ownership_registry78.json','surface_ownership_registry_head.json')]:code=code.replace(old,new)
anchor="repairs=pickle.load((H/'topology_repair_proposal.pkl').open('rb'))['repairs']"
replacement="""import gzip
folder=H.parent/'cut_head_yoke_candidate'
proposal=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()))
assert proposal['source_parts_sha256']==hashlib.sha256(previous_path.read_bytes()).hexdigest()
metadata=json.loads((folder/'A/hat3_v10zd_ent.json').read_text(encoding='utf-8'))['parca']
rows=dict(proposal['parts'],**proposal.get('wall_repairs',{}))
templates={'sac':dict(old['kafa_plakasi_8']),'kaynak':dict(old['ara_dikme_0']),'baglanti':dict(old['kelebek_somun_0'])}
templates['mek']=dict(old['ara_dikme_0']);templates['silikon']=dict(old['k_govde_conta_0'])
repairs={a:{'vertices':np.asarray(r['V'],float),'triangles':np.asarray(r['F'],int)} for a,r in rows.items()}
for a,r in rows.items():
 meta=dict(old[a]) if a in old else dict(templates[r['tur']])
 meta.update(tur=r['tur'],m='baglanti' if r['tur']=='baglanti' else 'kaynak' if r['tur']=='kaynak' else 'mekanizma' if r['tur']=='mek' else 'conta' if r['tur']=='silikon' else 'sac',ac=str(r.get('description',r.get('purpose','native wall hole refinement'))))
 if a in metadata:meta['dugum']=metadata[a]['dugum']
 old[a]=meta
"""
assert anchor in code;code=code.replace(anchor,replacement)
code=code.replace("H/'topology_repair_proposal.pkl'","H.parent/'cut_head_yoke_candidate/geometry.json.gz'").replace("H.parent/'chain73/A/hat3_v10s.json'","H.parent/'cut_head_yoke_candidate/A/hat3_v10zd.json'").replace('REBIND78','REBIND_OIL')
# The GLB stores metre-space float32 vertices. Its compressor merges exactly
# identical vertices, removing triangles with repeated indices. Reproduce only
# that exact operation, never an area/tolerance-based surface exemption.
header="""import struct,sys
sys.path.insert(0,str(H.parents[2]/'_local/claude_son_yerel/gece2/cekmece'))
from glb import G
source_file=H.parent/'cut_head_yoke_candidate/A/hat3_v10zd.glb'
with source_file.open('rb') as stream:
 stream.seek(12);size=struct.unpack('<I',stream.read(4))[0];stream.read(4)
 source_json=json.loads(stream.read(size))
world={}
def walk(node,parent):
 matrix=parent@G.trs(source_json['nodes'][node]);world[node]=matrix
 for child in source_json['nodes'][node].get('children',[]):walk(child,matrix)
for root in source_json['scenes'][0]['nodes']:walk(root,np.eye(4))
byname={r.get('name'):i for i,r in enumerate(source_json['nodes'])}
quantization_removed={}
def stored_surface(name,triangles):
 if name not in repairs:return triangles
 matrix=world[byname[old[name]['dugum']]]
 local=((triangles/1000-matrix[:3,3])@np.linalg.inv(matrix[:3,:3]).T).astype(np.float32)
 duplicate=np.all(local[:,0]==local[:,1],axis=1)|np.all(local[:,1]==local[:,2],axis=1)|np.all(local[:,2]==local[:,0],axis=1)
 if duplicate.any():
  original=triangles[duplicate]
  quantization_removed[name]={'count':int(duplicate.sum()),'expected_triangles_sha256':hashlib.sha256(original.astype('<f8').tobytes()).hexdigest(),'reason':'Exact repeated float32 source vertex: zero-area stored triangle','maximum_vertex_rounding_mm':float(np.linalg.norm((local[duplicate].astype(float)@matrix[:3,:3].T+matrix[:3,3])*1000-original,axis=2).max())}
 return triangles[~duplicate]
"""
code=code.replace('expected=[];lookup=defaultdict(list)',header+'\nexpected=[];lookup=defaultdict(list)')
code=code.replace(' for t in q:', ' q=stored_surface(a,q)\n for t in q:')
code=code.replace("'raw_triangles':sum", "'source_float32_zero_area_triangles':quantization_removed,'raw_triangles':sum")
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
