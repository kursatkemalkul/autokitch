"""Apply the source-bound head candidate only to private prototype outputs.

All new head stock, screws and welds inherit K_KESICI/KESICI render nodes:
they must follow the native cutting head, never a fixed oil-shelf template.
This does not register or activate a shared model-chain step.
"""
from lower_support import *
import pickle, hashlib, gzip
import k79_bound_removal_writer as W

def apply(source,dest,metadata_only=False):
    folder=OUT/'cut_head_yoke_candidate'
    report=json.loads((folder/'audit.json').read_text())
    access=json.loads((folder/'access_audit.json').read_text())
    torch=json.loads((folder/'torch_access_audit.json').read_text())
    geometry=folder/'geometry.json.gz'
    payload=json.loads(gzip.decompress(geometry.read_bytes()))
    assert report['passed_geometry_and_stacks']
    assert access['passed_bottom_tool_access'] and access['passed_continuous_weld_contacts']
    assert torch['passed_all_preassembly_envelopes']
    assert access['candidate_geometry_sha256']==torch['candidate_geometry_sha256']==hashlib.sha256(geometry.read_bytes()).hexdigest()
    assert hashlib.sha256(source.read_bytes()).hexdigest()==report['source_model_sha256']
    parts=OUT/'k1/k_parca_catalog_verified.pkl'
    assert hashlib.sha256(parts.read_bytes()).hexdigest()==payload['source_parts_sha256']
    P=pickle.loads(parts.read_bytes())['P']
    templates={'sac':'kafa_plakasi_8','kaynak':'ara_dikme_0','baglanti':'kelebek_somun_0','mek':'ara_dikme_0'}
    assert all(P[a]['dugum'].startswith('K_KESICI__') and P[a]['dugum'].endswith('__KESICI') for a in templates.values())
    rows=payload['parts']
    changed={a:r for a,r in rows.items() if a in P}
    repairs={}
    for a in sorted(set(changed)|set(templates.values())):
        old=P[a];r=changed.get(a,{'V':old['V'],'F':old['F']})
        repairs[a]={'original_triangles':old['V'][old['F']].tolist(),
            'vertices':clean(r['V']),'triangles':clean(r['F']),
            'proof':{'part':a,'closed_status':'Error.NoError','maximum_declared_precision_adjustment_mm':.001,
                'purpose':r.get('purpose','Unchanged exact moving-head render template')}}
    extra={};entries={}
    for a,r in rows.items():
        template=templates[r['tur']]
        if a not in P:
            extra[a]={'source_template':template,'vertices':r['V'],'triangles':r['F']}
        v=np.asarray(r['V']);lo=v.min(0);hi=v.max(0)
        entries[a]={'dugum':P[a if a in P else template]['dugum'],
            'kutu':[lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]],'tur':r['tur'],
            'bom':r.get('description',r.get('purpose','Cutting-head connection candidate'))}
    repair=folder/'source_repair_recipe.json.gz'
    repair.write_bytes(gzip.compress(json.dumps({'source_model_sha256':report['source_model_sha256'],
        'repairs':repairs,'additional_parts':extra},separators=(',',':')).encode(),mtime=0))
    nodes=sorted({P[a]['dugum'] for a in repairs})
    assert all(n.startswith('K_KESICI__') and n.endswith('__KESICI') for n in nodes)
    if metadata_only:
        # Classification corrections do not require rebuilding a large GLB.
        # Its exact geometry recipe must already match the verified output.
        bound=json.loads(dest.with_suffix('.json').read_text())
        assert dest.exists()
        assert bound['payload_sha256']==hashlib.sha256(repair.read_bytes()).hexdigest()
        assert bound['input_sha256']==report['source_model_sha256']
        assert hashlib.sha256(dest.read_bytes()).hexdigest()==bound['output_sha256']
    else:
        W.apply(source,dest,repair,expected_names=set(repairs),step=79,source_nodes=nodes,additional_parts=extra)
    dest.with_name(dest.stem+'_ent.json').write_text(json.dumps(clean({'adim':79,
        'prototype':'PRIVATE candidate only: head stock6+2/6+4,7M8screws,3continuous TIG rings, supplied factory yoke threads represented',
        'shared_chain_registered':False,'production_release':False,'parca':entries}),indent=2),encoding='utf-8')
    print('HEAD_PRIVATE_SOURCE',str(dest),'additional_parts',len(extra),flush=True)

if __name__=='__main__':
    apply(*map(Path,sys.argv[1:3]),metadata_only='--metadata-only' in sys.argv[3:]);sys.stdout.flush();os._exit(0)
