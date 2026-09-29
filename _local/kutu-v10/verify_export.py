import json,struct,zipfile,bisect
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'otonom'/'hat3d'
p=OUT/'hat_v84.glb'
b=p.read_bytes()
magic,version,total=struct.unpack_from('<4sII',b)
assert magic==b'glTF' and version==2 and total==len(b)
jlen,jtype=struct.unpack_from('<II',b,12)
d=json.loads(b[20:20+jlen]); assert jtype==0x4e4f534a
binary=20+jlen+8
def values(aid):
    a=d['accessors'][aid];v=d['bufferViews'][a['bufferView']]
    assert a['componentType']==5126
    n={'SCALAR':1,'VEC3':3,'VEC4':4}[a['type']]
    start=binary+v.get('byteOffset',0)+a.get('byteOffset',0)
    stride=v.get('byteStride',4*n)
    return [struct.unpack_from('<'+'f'*n,b,start+i*stride) for i in range(a['count'])]
names={n['name']:i for i,n in enumerate(d['nodes']) if 'name' in n}
required=['E_KOSE__CNR_'+g for g in ('MF','MB','PF','PB')]+['E_PARMAK__PARMAK']
for n in required: assert n in names,n
assert len(d['animations'])>=6
for anim in d['animations']:
    channels={(c['target']['node'],c['target']['path']) for c in anim['channels']}
    for n in required:
        for path in ('rotation','translation'): assert (names[n],path) in channels,(anim['name'],n,path)
    assert any('CNR_LIFT' in d['nodes'][i].get('name','') for i,path in channels if path=='translation')
    assert any('KATLAYICI' in d['nodes'][i].get('name','') for i,path in channels if path=='translation')
    lifts=[c for c in anim['channels'] if c['target']['path']=='translation' and 'CNR_LIFT' in d['nodes'][c['target']['node']].get('name','')]
    ymax=max(v[1] for c in lifts for v in values(anim['samplers'][c['sampler']]['output']))
    assert abs(ymax-.060)<5e-5,(anim['name'],'common lift not latest two-stage 38/60mm (0.05 mm sampled tolerance)',ymax)
print('GLB',len(b),'bytes;',len(d['animations']),'animations; corner/front/lid actuator channels PASS')
main_data=d
b=(OUT/'modul_E.glb').read_bytes()
jlen,jtype=struct.unpack_from('<II',b,12)
d=json.loads(b[20:20+jlen]);binary=20+jlen+8
checked=0
for anim in d['animations']:
    for c in anim['channels']:
        n=d['nodes'][c['target']['node']].get('name','')
        if 'CNR_LIFT' not in n or c['target']['path']!='translation':continue
        sample=anim['samplers'][c['sampler']]
        times=[v[0] for v in values(sample['input'])];vs=values(sample['output'])
        for t,expected in ((9.2,.060),(9.8,.038),(10.6,0)):
            i=max(0,min(len(times)-2,bisect.bisect_right(times,t)-1))
            f=(t-times[i])/(times[i+1]-times[i])
            y=vs[i][1]*(1-f)+vs[i+1][1]*f
            assert abs(y-expected)<5e-5,(n,t,y)
        checked+=1
assert checked>0
print('MODULE latest timed 60 -> 38 -> 0 reset PASS',checked)
with zipfile.ZipFile(OUT/'hat_v84.usdz') as z:
    assert z.testzip() is None
print('USDZ ZIP PASS')
status=json.loads((OUT/'durum.json').read_text(encoding='utf-8'))
# The build began before the metadata-only source amendment, so sync this
# generated label with the versioned builder; no geometry is altered here.
prefix='HAT v84: E v10 TAHRIKLI KOSE / ON DIL / KILAVUZLU KAPAK KATLAMA; KINEMATIK PROTOTIP, FIZIKSEL KARTON TESTI BEKLENIYOR. v83'
if status['hat']['pafta'].startswith('HAT v83'):
    status['hat']['pafta']=status['hat']['pafta'].replace('HAT v83',prefix,1)
description='4 motorlu köşe katlayıcı + ortak kaldırma: katlama 38 / geri dönüş 60 mm; kinematik prototip'
for u in status['birim']:
    if u['kod']=='E_KOSE': u['ad']=description
(OUT/'durum.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
parts=json.loads((OUT/'parca_kutulari.json').read_text(encoding='utf-8'))
head=[p for p in parts['parca']['E_PISTON'] if p[0]=='piston_kafasi']
assert len(head)==1 and abs(head[0][2]-4747)<.001 and abs(head[0][3]-5008)<.001,head
print('LATEST HEAD relief x4747..5008 PASS')
parts['birim']['E_KOSE']['ad']=description
(OUT/'parca_kutulari.json').write_text(json.dumps(parts,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
assert status['hat']['pafta'].startswith('HAT v84')
assert status['kutu_denetim']['ready_for_manufacture'] is False
print('VERSION / PROTOTYPE LABEL PASS')
