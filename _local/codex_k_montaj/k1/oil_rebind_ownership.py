"""Bind all907 expected parts to actual new source triangles, or reject."""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k78_rebind_ownership.py'
code=source.read_text(encoding='utf-8').replace("previous_path=H/'k_parca.pkl'","previous_path=H/'k_parca_bottom_verified.pkl'").replace('if manifest.exists():previous_path=','if False:previous_path=')
for old,new in [('k_parca78_raw.pkl','k_parca_oil_raw.pkl'),('k_parca78_verified.pkl','k_parca_oil_verified.pkl'),('step78_ownership_rebind_audit.json','oil_ownership_rebind_audit.json'),('surface_ownership_registry78.json','surface_ownership_registry_oil.json')]:code=code.replace(old,new)
anchor="repairs=pickle.load((H/'topology_repair_proposal.pkl').open('rb'))['repairs']"
replacement="""import gzip
folder=H.parent/'oil_shelf_mount_candidate'
proposal=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()))
assert proposal['source_parts_sha256']==hashlib.sha256(previous_path.read_bytes()).hexdigest()
metadata=json.loads((folder/'A/hat3_v10y_ent.json').read_text(encoding='utf-8'))['parca']
rows=dict(proposal['parts'],**proposal['wall_repairs'])
templates={'sac':dict(old['yag_pompa_plakasi']),'kaynak':dict(old['k79_bant_disli_plaka_kaynagi_4065_-421']),'baglanti':dict(old['k71_alt_saplama_4060_379_-32.0'])}
repairs={a:{'vertices':np.asarray(r['V'],float),'triangles':np.asarray(r['F'],int)} for a,r in rows.items()}
for a,r in rows.items():
 meta=dict(old[a]) if a in old else dict(templates[r['tur']])
 meta.update(tur=r['tur'],m='baglanti' if r['tur']=='baglanti' else 'kaynak' if r['tur']=='kaynak' else 'sac',ac=str(r.get('description',r.get('purpose','native wall hole refinement'))))
 if a in metadata:meta['dugum']=metadata[a]['dugum']
 old[a]=meta
"""
assert anchor in code;code=code.replace(anchor,replacement)
code=code.replace("H/'topology_repair_proposal.pkl'","H.parent/'oil_shelf_mount_candidate/geometry.json.gz'").replace("H.parent/'chain73/A/hat3_v10s.json'","H.parent/'oil_shelf_mount_candidate/A/hat3_v10y.json'").replace('REBIND78','REBIND_OIL')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
