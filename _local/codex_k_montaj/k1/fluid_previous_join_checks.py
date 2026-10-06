"""Re-measure surviving body/lower/pusher joints against the new source and full plan.

Four obsolete conveyor clamps are explicitly superseded, not marked passed.
Their replacements have separate geometry, insertion and access audits.
"""
from pathlib import Path
H=Path(__file__).resolve().parent
for filename,output in [('k_baglanti_kaynak.py','body'),
                        ('k_lower_connection_audit.py','lower'),
                        ('k_mount_connection_audit.py','mount')]:
    source=H/filename
    code=source.read_text(encoding='utf-8')
    code=code.replace('k_parca.pkl','k_parca_fluid_verified.pkl')
    code=code.replace('plan_k_full.pkl','plan_k_fluid_full.pkl')
    old=output+'_connection_measured_audit.json'
    assert old in code
    code=code.replace(old,'fluid_'+old)
    if output=='mount':
        anchor="source=H.parent/'k72_mounts.json';joins=json.loads(source.read_text(encoding='utf-8'))['connections']"
        assert anchor in code
        code=code.replace(anchor,anchor+"\nremoved=json.loads(__import__('gzip').decompress((H.parent/'belt_bottom_mount_candidate/geometry.json.gz').read_bytes()))['superseded_parts']\nremoved=set(removed)\nsuperseded=[j for j in joins if any(a in removed for a in j['parts'])]\nassert len(superseded)==4 and all(all(a in removed for a in j['parts']) for j in superseded)\njoins=[j for j in joins if j not in superseded]\nassert len(joins)==8")
        code=code.replace('12 conveyor/pusher mounting bolts only; no full station release','8 surviving pusher mounting bolts only; four conveyor clamps superseded and audited separately; no full station release')
    exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
