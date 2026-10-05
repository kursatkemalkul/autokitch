"""Reserved local K step72. K-owned geometry only; chain not edited here."""
from mechanism_mounts import *
import subprocess,hashlib
Y=H/'yama_v9'
for path in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(path))
from m8kit import Glb
import sac_ent as SE

def apply(source,dest):
    parts,r=build_mounts();g=Glb(str(source));removed=[]
    for row in r['replace']:
        node=row['node'];g.bilesen(node,0);x,z=row['center_xz']
        candidates=[b for b in g._bc[node] if abs(b['lo'][1]-row['lo_y'])<.05 and abs(b['hi'][1]-row['hi_y'])<.05 and abs((b['lo'][0]+b['hi'][0])/2-x)<.05 and abs((b['lo'][2]+b['hi'][2])/2-z)<.05]
        assert len(candidates)==1,(row,len(candidates))
        b=candidates[0];removed.append({'node':node,'lo':b['lo'].tolist(),'hi':b['hi'].tolist()});g.sil_b(b)
    labels={}
    for name in ('K_BANT__sac','K_BANT__celik','K_ITICI__sac','K_ITICI__celik'):
        p=next(p for p in g.dprims(name) if not p.get('gizli'));labels[name]=g._etiketler(p,0)
    for part in parts:
        belt=('bant' in part['ad'] or ('M6' in part['ad']))
        node=('K_BANT' if belt else 'K_ITICI')+('__sac' if part.get('tur') in ('sac','profil','kaynak') else '__celik')
        kat,mek,kpk=labels[node];g.ucgen_ekle(node,SE.ucgen(part['sh']),kat=kat,mek=mek,kpk=False)
    temp=dest.with_suffix('.raw.glb');g.kaydet(str(temp));del g
    env=dict(os.environ,YAMA_IS_KOK=str(Y/'kaynak'))
    subprocess.run([sys.executable,str(Y/'50_sikilastir.py'),str(temp),str(dest)],env=env,check=True);temp.unlink()
    r.update(input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),output_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),removed=removed,parts=[p['ad'] for p in parts],whole_assembly_release=False)
    dest.with_suffix('.json').write_text(json.dumps(clean(r),ensure_ascii=False,indent=2),encoding='utf8')
    from chain_entry import write_ent
    write_ent(dest,parts,72)
    print('STEP72',len(parts),r['output_sha256'],flush=True)

if __name__=='__main__':
    source,dest=map(Path,sys.argv[1:3]);apply(source,dest);sys.stdout.flush();os._exit(0)
