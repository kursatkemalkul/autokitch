"""Reserved K step71, applied locally until the chain integration lock is taken.

Replaces only the six lower supports, lower shelf and primitive fixings.
Adds real base-sheet holes. No B/F/E/TOPPING geometry is modified.
"""
from lower_support import *
import subprocess,hashlib
Y=H/'yama_v9'
for path in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(path))
from m8kit import Glb
import sac_ent as SE

def apply(source,dest):
    g=Glb(str(source));parts,manufacturing,shelf=build();removed=[]
    def components(name):
        g.bilesen(name,no=0); return g._bc[name]
    body=components('K_GOVDE__sac')
    floor=[b for b in body if abs(b['lo'][1]-889)<.05 and abs(b['hi'][1]-892)<.05 and b['hi'][2]-b['lo'][2]>800]
    # Turned-down shelf's lower edges extend to Y862.
    if not floor:floor=[b for b in body if abs(b['lo'][1]-862)<.05 and abs(b['hi'][1]-892)<.05 and b['hi'][2]-b['lo'][2]>800]
    assert len(floor)==1,[(b['lo'].tolist(),b['hi'].tolist()) for b in floor]
    supports=[b for b in body if abs(b['lo'][1]-791)<.05 and abs(b['hi'][1]-889)<.05 and abs(b['hi'][0]-b['lo'][0]-40)<.05 and abs(b['hi'][2]-b['lo'][2]-90)<.05]
    assert len(supports)==6,len(supports)
    base=[b for b in body if abs(b['lo'][1]-788)<.05 and abs(b['hi'][1]-791)<.05 and b['hi'][2]-b['lo'][2]>880]
    assert len(base)==1
    cel=components('K_GOVDE__celik')
    primitive_heads=[b for b in cel if abs(b['lo'][1]-795)<.05 and abs(b['hi'][1]-799)<.05 and any(abs((b['lo'][0]+b['hi'][0])/2-x)<.05 for x in PX)]
    primitive_pems=[b for b in cel if abs(b['lo'][1]-886.9)<.05 and abs(b['hi'][1]-891.4)<.05 and b['hi'][0]-b['lo'][0]<9]
    assert len(primitive_heads)==12,len(primitive_heads)
    assert len(primitive_pems)==12,len(primitive_pems)
    for b in floor+supports+primitive_heads+primitive_pems:
        removed.append({'lo':b['lo'].tolist(),'hi':b['hi'].tolist()});g.sil_b(b)
    b=base[0];P=np.concatenate([p['X'][p['T'][idx]] for p,idx in b['parca']]);solid=SE.mf_ucgen(P)
    assert solid is not None,'source base sheet is not a closed manifold'
    for hole in manufacturing['bottom_holes']:
        x,y,z=hole['center'];cutter=cylinder(x,y-1,z,hole['diameter']/2,5)
        solid=solid-SE.mf_ucgen(SE.ucgen(cutter))
    g.donustur(b,lambda P:SE.mf_P(solid))
    for p in parts:
        node='K_GOVDE__sac' if p['mal']=='sac' or p.get('tur') in ('sac','profil','kaynak') else 'K_GOVDE__celik'
        g.ucgen_ekle(node,SE.ucgen(p['sh']),kat=0,mek=24)
    temp=dest.with_suffix('.raw.glb');g.kaydet(str(temp));del g
    env=dict(os.environ,YAMA_IS_KOK=str(Y/'kaynak'))
    subprocess.run([sys.executable,str(Y/'50_sikilastir.py'),str(temp),str(dest)],env=env,check=True);temp.unlink()
    report={'step':71,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'removed_primitive_components':removed,'new_parts':[p['ad'] for p in parts],'manufacturing':manufacturing,'whole_assembly_checked':False,'publish_allowed':False}
    dest.with_suffix('.json').write_text(json.dumps(clean(report),ensure_ascii=False,indent=2),encoding='utf8')
    from chain_entry import write_ent
    write_ent(dest,parts,71)
    print('STEP71',len(parts),'new parts',report['output_sha256'],flush=True)

if __name__=='__main__':
    source,dest=map(Path,sys.argv[1:3]);apply(source,dest);sys.stdout.flush();os._exit(0)
