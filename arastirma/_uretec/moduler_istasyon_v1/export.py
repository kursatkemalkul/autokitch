import json,csv,math,os,sys,time
from pathlib import Path
import cadquery as cq
from load_source import OUT,ROOT

def bounds(s):
    b=s.BoundingBox();return [b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]
def overlaps(a,b,t=.06):return all(min(a[2*i+1],b[2*i+1])-max(a[2*i],b[2*i])>t for i in range(3))
def write(M,parts,checks,changes):
    site=ROOT/'otonom/hat/moduler-v1';site.mkdir(parents=True,exist_ok=True)
    collisions=[];invalid=[];contacts={};records=[]
    for p in parts:
        p['bounds']=bounds(p['shape'])
        if p['new'] and (not p['shape'].isValid() or len(p['shape'].Solids())!=1):invalid.append(p['name'])
    additions=[p for p in parts if p['new'] and p['kind'] not in ('shipping','connection')]
    for p in additions:
        near=[]
        for q in parts:
            if p is q or q['kind'] in ('shipping','connection'):continue
            if q['new'] and q['name']<p['name']:continue
            if not overlaps(p['bounds'],q['bounds']):continue
            vol=abs(p['shape'].intersect(q['shape']).Volume())
            if vol>.5:collisions.append(dict(a=p['name'],b=q['name'],mm3=round(vol,2)))
        print('CHECK',p['name'],len(collisions),flush=True)
    for p in additions:
        b=p['bounds'];near=[]
        for q in parts:
            if q is p or q['kind'] in ('shipping','connection'):continue
            if not all(min(b[2*i+1],q['bounds'][2*i+1])+0.1>=max(b[2*i],q['bounds'][2*i]) for i in range(3)):continue
            if p['shape'].distance(q['shape'])<.06:near.append(q['name'])
            if len(near)>=3:break
        contacts[p['name']]=near
    density={'304':7.93e-6,'celik':7.93e-6,'sac':7.93e-6,'paslanmaz':7.93e-6,'fircali':7.93e-6,'PU':4e-8,'pu':4e-8,'aluminyum':2.7e-6,'pom':1.41e-6,'EPDM':1.2e-6,'GFRP':1.8e-6,'wood':6e-7}
    masses={};mass_parts=[];catalog_seen=set()
    for p in parts:
        if p['kind']=='shipping':continue
        m=masses.setdefault(p['module'],{'known_material_kg':0,'unknown_material_volume_mm3':0})
        if p['note']=='D_BULASIK':
            if 'dishwasher' not in catalog_seen:m['known_material_kg']+=70;catalog_seen.add('dishwasher')
            continue
        vol=abs(p['shape'].Volume())
        if p['material'] in density:
            kg=vol*density[p['material']];m['known_material_kg']+=kg
            if kg>2:mass_parts.append(dict(module=p['module'],name=p['name'],material=p['material'],kg=round(kg,2)))
        else:m['unknown_material_volume_mm3']+=vol
    report=dict(checks=checks,collisions=collisions,invalid_new_solids=invalid,contacts=contacts,changes=changes,masses=masses,mass_parts=sorted(mass_parts,key=lambda p:-p['kg']),notes=[
        'Preliminary engineering model, not approved lifting equipment.',
        'No robot, QR or counter checks. Process dimensions and drawer stock unchanged.',
        'Existing continuous A/C rail is transported as a removable bridge subassembly T.',
        'B remains one 4000 x 909 mm cabinet: door width, turning route and transport equipment must be measured.',
        'Transport empty: remove food, GN pans, loose tools and stocks; latch drawers and remove upper modules.',
        'B transport: continuous load-spreading bed or supports no more than 1000 mm apart; NOT two widely spaced lifting forks.',
        'Mass is incomplete CAD + dishwasher catalog 70 kg; unknown catalog internals and contents are not included.',
        'Weld design, M12 feet capacity, fastener grades, actual masses and GFRP creep require final supplier verification.'])
    (OUT/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('CHECK RESULT',len(collisions),'collisions',len(invalid),'invalid',flush=True)
    if '--check-only' in sys.argv:return
    # Never label failed geometry checks as ready; diagnostic previews are marked.
    from kaset_3d_v3 import Mesh,MALZEME,glb_yaz
    from kiyma_cad_v6 import ag
    for name,d in M.MALZEME.items():MALZEME[name]=dict(d)
    for k,rgba in [('304',(.74,.77,.8,1)),('PU',(.93,.88,.72,1)),('GFRP',(.20,.35,.34,1)),('EPDM',(.06,.06,.06,1)),('wood',(.55,.35,.17,1))]:
        MALZEME[k]=dict(renk=rgba,met=.85 if k=='304' else 0,ruf=.35 if k=='304' else .85)
    grouped={};meta=[]
    for i,p in enumerate(parts):
        if p['shape'].Volume()<.001:continue
        key=(p['module'],p['kind'],p['material'],'new' if p['new'] else 'base')
        if key not in grouped:grouped[key]=Mesh()
        grouped[key].ekle(ag(p['shape'],.35,.4))
        meta.append({k:v for k,v in p.items() if k!='shape'})
        if i%200==0:print('MESH',i,'/',len(parts),flush=True)
    # Register unique group materials so viewer can hide complete components.
    meshes=[]
    for key,g in grouped.items():
        name='__'.join(key);mat=dict(MALZEME.get(key[2],MALZEME['304']));mat.pop('doku',None)
        MALZEME[name]=mat;meshes.append((name,g,name))
    # Only used materials; old text textures are not required for this revision.
    used={m for _,_,m in meshes}
    for key in list(MALZEME):
        if key not in used:del MALZEME[key]
    glb_yaz(str(site/'moduler_v1.glb'),meshes,{})
    (site/'parts.json').write_text(json.dumps(meta,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    (site/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    with (OUT/'BOM_EK.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f);writer.writerow(['modul','parca','malzeme','sinif','x_mm','y_mm','z_mm','hacim_mm3','not'])
        for p in parts:
            if not p['new']:continue
            b=p['bounds'];writer.writerow([p['module'],p['name'],p['material'],p['kind'],*[round(b[i+1]-b[i],2) for i in (0,2,4)],round(p['shape'].Volume(),2),p['note']])
    asm=cq.Assembly(name='MODULER_ISTASYON_EK_V1')
    for i,p in enumerate(parts):
        if p['new'] and p['kind']!='shipping':asm.add(p['shape'],name='%s_%d'%(p['module'],i))
    asm.save(str(OUT/'MODULER_EK_PARCA_v1.step'))
    print('MODEL WRITTEN',site/'moduler_v1.glb',flush=True)
