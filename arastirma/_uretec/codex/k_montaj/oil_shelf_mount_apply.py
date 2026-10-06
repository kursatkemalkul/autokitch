"""Source-bound oil-shelf wall mounting prototype; does not activate main model."""
from lower_support import *
import pickle,hashlib,gzip
import k79_bound_removal_writer as W

def apply(source,dest):
    folder=OUT/'oil_shelf_mount_candidate'
    report=json.loads((folder/'audit.json').read_text());context=json.loads((folder/'wall_context_audit.json').read_text())
    payload_path=folder/'geometry.json.gz';recipe=json.loads(gzip.decompress(payload_path.read_bytes()))
    assert report['passed_stack_and_geometry_only'] and context['passed_removal_only_context']
    assert context['candidate_recipe_sha256']==hashlib.sha256(payload_path.read_bytes()).hexdigest()
    assert hashlib.sha256(source.read_bytes()).hexdigest()==report['source_model_sha256']
    P=pickle.loads((OUT/'k1/k_parca_bottom_verified.pkl').read_bytes())['P']
    assert hashlib.sha256((OUT/'k1/k_parca_bottom_verified.pkl').read_bytes()).hexdigest()==recipe['source_parts_sha256']
    templates={'plate':'yag_pompa_plakasi','weld':'k79_bant_disli_plaka_kaynagi_4065_-421',
      'stud':next(a for a in P if a.startswith('k71_alt_saplama_')),
      'washer':next(a for a in P if a.startswith('k71_alt_pul_')),
      'nut':next(a for a in P if a.startswith('k71_alt_somun_'))}
    changed={a:r for a,r in recipe['parts'].items() if a in P}
    changed.update(recipe['wall_repairs'])
    # Rendering references remain exact source surfaces. No dummy geometry.
    references={templates[t] for t in templates}
    repairs={}
    for a in sorted(set(changed)|references):
        old=P[a];r=changed.get(a,{'V':old['V'],'F':old['F']})
        repairs[a]={'original_triangles':old['V'][old['F']].tolist(),
          'vertices':clean(r['V']),'triangles':clean(r['F']),
          'proof':{'part':a,'closed_status':'Error.NoError','maximum_declared_precision_adjustment_mm':.001,
            'purpose':r.get('purpose','Replace own3mm bracket with drilled vertical leg; horizontal leg/seam added separately') if a in changed else 'Unchanged exact render template'}}
    extra={};entries={}
    for a,r in recipe['parts'].items():
        typ='plate' if r['tur']=='sac' else 'weld' if r['tur']=='kaynak' else 'stud' if 'FHP_' in a else 'washer' if '_pul_' in a else 'nut'
        if a not in P:extra[a]={'source_template':templates[typ],'vertices':r['V'],'triangles':r['F']}
        v=np.asarray(r['V']);lo=v.min(0);hi=v.max(0)
        entries[a]={'dugum':P[a if a in P else templates[typ]]['dugum'],'kutu':[lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]],'tur':r['tur'],'bom':r.get('description')}
    repair_path=folder/'source_repair_recipe.json.gz'
    repair_path.write_bytes(gzip.compress(json.dumps({'source_model_sha256':report['source_model_sha256'],'repairs':repairs,'additional_parts':extra},separators=(',',':')).encode(),mtime=0))
    nodes=sorted({P[a]['dugum'] for a in repairs})
    W.apply(source,dest,repair_path,expected_names=set(repairs),step=79,source_nodes=nodes,additional_parts=extra)
    dest.with_name(dest.stem+'_ent.json').write_text(json.dumps(clean({'adim':79,'prototype':'oil shelf wall mounts; not full shelf/pump fixing','parca':entries}),indent=2),encoding='utf-8')

if __name__=='__main__':
    apply(*map(Path,sys.argv[1:3]));sys.stdout.flush();os._exit(0)
