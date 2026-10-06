"""Source-bound885part rebind; explicitly supersede20 old fasteners."""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k78_rebind_ownership.py'
code=source.read_text(encoding='utf-8').replace("previous_path=H/'k_parca.pkl'","previous_path=H/'k_parca_belt_verified.pkl'").replace('if manifest.exists():previous_path=','if False:previous_path=')
code=code.replace('k_parca78_raw.pkl','k_parca_bottom_raw.pkl').replace('k_parca78_verified.pkl','k_parca_bottom_verified.pkl').replace('step78_ownership_rebind_audit.json','bottom_ownership_rebind_audit.json').replace('surface_ownership_registry78.json','surface_ownership_registry_bottom.json')
anchor="repairs=pickle.load((H/'topology_repair_proposal.pkl').open('rb'))['repairs']"
replacement='''import gzip
folder=H.parent/'belt_bottom_mount_candidate'
proposal=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()))
assert proposal['source_parts_sha256']==hashlib.sha256(previous_path.read_bytes()).hexdigest()
metadata=json.loads((folder/'A/hat3_v10x_ent.json').read_text(encoding='utf-8'))['parca']
templates={'sac':dict(old['k72_bant_ayak_flansi_4065.0_-421.0']),'kaynak':dict(old['k79_bant_tapa_cevre_kaynagi_4065_-421']),'baglanti':dict(old['k72_vida_M6_4065.0_-421.0'])}
for a in proposal['superseded_parts']:assert a in old;old.pop(a)
repairs={a:{'vertices':np.asarray(r['V'],float),'triangles':np.asarray(r['F'],int)} for a,r in proposal['parts'].items()}
for a,r in proposal['parts'].items():
 meta=dict(old[a]) if a in old else dict(templates[r['tur']]);meta.update(tur=r['tur'],m='baglanti' if r['tur']=='baglanti' else 'kaynak' if r['tur']=='kaynak' else 'sac',dugum=metadata[a]['dugum'],ac=str(r['description']))
 old[a]=meta
'''
assert anchor in code;code=code.replace(anchor,replacement).replace("H/'topology_repair_proposal.pkl'","H.parent/'belt_bottom_mount_candidate/geometry.json.gz'").replace("H.parent/'chain73/A/hat3_v10s.json'","H.parent/'belt_bottom_mount_candidate/A/hat3_v10x.json'").replace('REBIND78','REBIND_BOTTOM')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
