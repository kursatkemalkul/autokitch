"""Reserved local step73: replace only K roof and its short M8 PEMs."""
from roof_mounts import *
import subprocess,hashlib
Y=H/'yama_v9'
for path in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(path))
from m8kit import Glb
import sac_ent as SE
import manifold3d as mf

def apply(source,dest):
    parts,r,_=build_roof();g=Glb(str(source));g.bilesen('K_GOVDE__kabuk',0)
    roofs=[b for b in g._bc['K_GOVDE__kabuk'] if abs(b['hi'][1]-1862)<.05 and b['hi'][0]-b['lo'][0]>399 and b['hi'][2]-b['lo'][2]>880]
    assert len(roofs)==1,len(roofs)
    roof=roofs[0]
    origin=np.array([4200.,1860.5,-700.])
    original=SE.mf_ucgen(np.concatenate([p['X'][p['T'][idx]] for p,idx in roof['parca']])-origin)
    assert original is not None,'Original roof must be closed before local patch'
    changed=original;top=round(float(roof['hi'][1]-origin[1]),4);bottom=top-1.5
    zones=None
    for x in (4100.,4300.):
        # Preserve every source roof feature, including electrical and stud
        # interfaces. Replace only the two obsolete stepped PEM seats.
        xx=x-origin[0]
        fill=mf.Manifold.cylinder(1.5,6.,6.,circular_segments=96).rotate((-90,0,0)).translate((xx,bottom,0.))
        hole=mf.Manifold.cylinder(8.,4.5,4.5,circular_segments=96).rotate((-90,0,0)).translate((xx,bottom-3,0.))
        changed=(changed+fill)-hole
        zone=mf.Manifold.cube((14.,8.,14.)).translate((xx-7,bottom-3,-7.))
        zones=zone if zones is None else zones+zone
    delta=((original-changed)+(changed-original))-zones
    assert delta.volume()<.05,('Roof changed outside two M8 seats',delta.volume())
    g.sil_b(roof);g.ucgen_ekle('K_GOVDE__kabuk',SE.mf_P(changed)+origin,kat=0,mek=24)
    r['source_roof_preserved_except_two_M8_seats']=True;r['roof_delta_outside_seats_mm3']=delta.volume()
    g.bilesen('K_GOVDE__baglanti',0)
    pems=[b for b in g._bc['K_GOVDE__baglanti'] if abs(b['hi'][1]-1861.88)<.05 and abs((b['lo'][2]+b['hi'][2])/2+700)<.05]
    assert len(pems)==2,len(pems)
    for b in pems:g.sil_b(b)
    for p in parts[1:]:
        g.ucgen_ekle('K_GOVDE__sac',SE.ucgen(p['sh']),kat=0,mek=24)
    temp=dest.with_suffix('.raw.glb');g.kaydet(str(temp));del g
    env=dict(os.environ,YAMA_IS_KOK=str(Y/'kaynak'))
    subprocess.run([sys.executable,str(Y/'50_sikilastir.py'),str(temp),str(dest)],env=env,check=True);temp.unlink()
    r.update(input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),output_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),new_parts=[p['ad'] for p in parts],full_assembly_release=False)
    dest.with_suffix('.json').write_text(json.dumps(clean(r),ensure_ascii=False,indent=2),encoding='utf8');print('STEP73',r['output_sha256'],flush=True)

if __name__=='__main__':
    source,dest=map(Path,sys.argv[1:3]);apply(source,dest);sys.stdout.flush();os._exit(0)
