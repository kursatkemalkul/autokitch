import json
from pathlib import Path
def write_ent(dest,parts,step):
    out={}
    for i,p in enumerate(parts):
        name=p['ad'];b=p['sh'].BoundingBox()
        if step==71: node='K_GOVDE__sac' if p['mal']=='sac' or p.get('tur') in ('sac','profil','kaynak') else 'K_GOVDE__celik'
        elif step==72: node=('K_BANT' if ('bant' in name or 'M6' in name) else 'K_ITICI')+('__sac' if p.get('tur') in ('sac','profil','kaynak') else '__celik')
        else: node='K_GOVDE__kabuk' if i==0 else 'K_GOVDE__sac'
        out[name]={'dugum':node,'kutu':[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax],'tur':p.get('tur','sac' if p.get('mal')=='sac' else 'arayuz'),'bom':p.get('bom',[])}
    Path(dest).with_name(Path(dest).stem+'_ent.json').write_text(json.dumps({'adim':step,'parca':out},ensure_ascii=False,indent=2),encoding='utf-8')
