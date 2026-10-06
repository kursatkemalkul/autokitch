"""Apply the independently checked panel candidate through the K writer.

Prototype refinement of reserved step79. No shared chain/site activation.
Input hash, exact old triangles and candidate checks bind every replacement.
"""
from lower_support import *
import importlib.util
import manifold3d as mf

spec=importlib.util.spec_from_file_location('k_panel_writer',Path(__file__).with_name('78_k_sac_topolojisi.py'))
writer=importlib.util.module_from_spec(spec);spec.loader.exec_module(writer)

def apply(source,dest,folder=None):
    folder=folder or OUT/'panel_mount_candidate'
    audit=json.loads((folder/'audit.json').read_text(encoding='utf-8'))
    recipe=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()))
    actual=hashlib.sha256(source.read_bytes()).hexdigest()
    assert audit['passed'] and audit['source_model_sha256']==actual==recipe['source_model_sha256']
    assert audit['source_parts_sha256']==recipe['source_parts_sha256']
    repairs={};extra={};origin=np.array([4200.,1660.,-820.])
    for a,r in recipe['replacement_parts'].items():
        v=np.asarray(r['V'],float);f=np.asarray(r['F'],int)
        vv,inv=np.unique(np.asarray(v-origin,dtype=np.float32),axis=0,return_inverse=True)
        solid=mf.Manifold(mf.Mesh(vert_properties=vv,tri_verts=np.asarray(inv[f],dtype=np.uint32)))
        assert str(solid.status())=='Error.NoError' and solid.volume()>0,a
        if a in recipe['original_triangles']:
            repairs[a]={'original_triangles':recipe['original_triangles'][a],'vertices':v.tolist(),'triangles':f.tolist(),
                        'proof':{'part':a,'closed_status':str(solid.status()),'volume_mm3':solid.volume(),
                                 'maximum_declared_precision_adjustment_mm':0.,'purpose':'real bored and countersunk panel mounting',
                                 'supplier_equipment_modified':False}}
        else:
            template='din_rayi_0' if folder.name=='din_mount_candidate' else 'pano_ara_burcu_0'
            extra[a]={'source_template':template,'vertices':v.tolist(),'triangles':f.tolist()}
    expected={'pano_plakasi','arka_sac'}|{f'pano_ara_burcu_{i}' for i in range(4)}
    if folder.name=='din_mount_candidate':
        expected={'pano_plakasi','din_rayi_0','din_rayi_1'}
    assert set(repairs)==expected and set(extra)==set(audit['added_parts']) and len(extra)==12
    payload=folder/'source_repair_recipe.json.gz'
    payload.write_bytes(gzip.compress(json.dumps({'source_model_sha256':actual,'repairs':repairs},separators=(',',':')).encode(),mtime=0))
    writer.apply(source,dest,payload,expected_names=expected,step=79,
                 source_nodes=('K_ELEKTRIK__sac','K_ELEKTRIK__celik','K_GOVDE__kabuk'),additional_parts=extra)
    # Small name/box registry to distinguish every added fastener on extraction.
    entries={}
    for a,r in recipe['replacement_parts'].items():
        v=np.asarray(r['V']);lo=v.min(0);hi=v.max(0)
        node='K_GOVDE__kabuk' if a=='arka_sac' else ('K_ELEKTRIK__sac' if a=='pano_plakasi' else 'K_ELEKTRIK__celik')
        entries[a]={'dugum':node,'kutu':[float(lo[0]),float(hi[0]),float(lo[1]),float(hi[1]),float(lo[2]),float(hi[2])],
                    'tur':'sac' if a in ('pano_plakasi','arka_sac') else 'baglanti',
                    'bom':next((j['method'] for j in audit['joints'] if a in j['parts']),None)}
    dest.with_name(dest.stem+'_ent.json').write_text(json.dumps({'adim':79,'prototype':'panel refinement','parca':entries},indent=2),encoding='utf-8')

if __name__=='__main__':
    apply(*map(Path,sys.argv[1:4]));sys.stdout.flush();os._exit(0)
