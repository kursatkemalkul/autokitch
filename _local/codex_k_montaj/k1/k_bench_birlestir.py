"""Compose verified bench preparation into the K station timeline.
Writes a separate prototype plan. Full CCD, fixture, joining and tool release
remain mandatory; geometry and the established station insertion paths stay intact.
"""
from pathlib import Path
import pickle,json,hashlib,copy
import numpy as np
H=Path(__file__).resolve().parent
source=H/'plan_k.pkl';D=pickle.load(source.open('rb'));B=pickle.load((H/'bench_plans.pkl').open('rb'))
assert not D['PLAN_SORUN']
assert B['source_parts_sha256']==hashlib.sha256((H/'k_parca.pkl').read_bytes()).hexdigest()
assert all(not b['PLAN_SORUN'] for b in B['groups'].values())
original=copy.deepcopy(D);segments=[]
for head,b in B['groups'].items():
 start=D['GOR'][head];move=min(h[0] for h in D['HAR'][head])
 seams=[a for a in D['P'] if D['P'][a]['tur']=='kaynak' and D['HAR'][a]==D['HAR'][head]]
 members=set(b['GOR'])|set(seams)
 assert all(a in D['P'] for a in members)
 old_duration=move-start
 offset=np.sum([h[2:5] for h in D['HAR'][head]],axis=0)
 # A separate factory bench, not the K installation footprint. Upright
 # native blanks need their own support/fixture audit before release.
 low=float(D['P'][head]['V'][:,1].min())
 factory=np.array([-2.,(.920-low/1000.),2.])
 safe=factory.copy();safe[1]=3.-low/1000.
 above=offset.copy();above[1]=safe[1]
 delivery=[factory,safe,above,offset]
 delivery_seconds=[max(.3,float(np.linalg.norm(q-p))) for p,q in zip(delivery[:-1],delivery[1:])]
 duration=float(b['seconds'])+(.8 if seams else 0)+.02+sum(delivery_seconds)
 assert duration>=old_duration
 segments.append(dict(head=head,start=start,move=move,duration=duration,delta=duration-old_duration,members=members,seams=seams,ofs=offset,factory=factory,delivery=delivery,delivery_seconds=delivery_seconds,bench=b))
segments.sort(key=lambda r:r['start'])
assert all(x['move']<=y['start']+.001 for x,y in zip(segments,segments[1:]))
def stamp(t):
 delta=0.
 for s in segments:
  if t>=s['move']-1e-6:delta+=s['delta'];continue
  if s['start']<=t<s['move']:
   return round(s['start']+delta+(t-s['start'])*s['duration']/(s['move']-s['start']),6)
  break
 return round(t+delta,6)
for a in D['HAR']:D['HAR'][a]=[[stamp(h[0]),stamp(h[1])]+h[2:] for h in D['HAR'][a]]
D['GOR']={a:stamp(t) for a,t in D['GOR'].items()}
for a,m in D['MF'].items():
 if 'seg' in m:m['seg']=[[stamp(x[0]),stamp(x[1])]+x[2:] for x in m['seg']]
 if 'buyu' in m:m['buyu']=[stamp(t) for t in m['buyu']]
D['VU']={a:[[stamp(x[0]),stamp(x[1])] for x in values] for a,values in D['VU'].items()}
for a,L in D['ROT'].items():D['ROT'][a]=[[stamp(x[0]),stamp(x[1])]+x[2:] for x in L]
for step in D['ADIM']:step['t0']=stamp(step['t0'])
# All events within these serial preparation intervals belong to replaced
# group preparation, not station movements or another concurrently moving part.
D['OLAY']=[[stamp(t),text] for t,text in original['OLAY'] if not any(s['start']<=t<s['move'] for s in segments)]
D['ACN']=[dict(r,t0=stamp(r['t0']),t1=stamp(r['t1'])) for r in original['ACN'] if not any(r['ad'] in s['members'] for s in segments)]
D['KAM']=[[stamp(r[0])]+r[1:] for r in original['KAM']]
report=[]
for s in segments:
 b=s['bench'];base=stamp(s['start']);depart=base+s['duration'];ofs=s['factory']
 travel=[];ts=base+b['seconds']+(.8 if s['seams'] else 0)+.02
 for prev,next_point,duration in zip(s['delivery'][:-1],s['delivery'][1:],s['delivery_seconds']):
  travel.append([round(ts,6),round(ts+duration,6)]+(prev-next_point).tolist());ts+=duration
 assert abs(ts-depart)<.001
 for a in b['GOR']:
  # Sum of remaining route deltas is the group's bench offset until departure.
  station=[[stamp(h[0]),stamp(h[1])]+h[2:] for h in original['HAR'][a] if h[0]>=s['move']-.001]
  assert station and station[0][0]>=depart-.001,(s['head'],a,station,depart)
  D['HAR'][a]=[[round(base+h[0],6),round(base+h[1],6)]+h[2:] for h in b['HAR'][a]]+travel+station
  D['GOR'][a]=round(base+b['GOR'][a],6)
  D['MF'].pop(a,None);D['FRAMES'].pop(a,None)
  if a in b['MF']:
   m=copy.deepcopy(b['MF'][a])
   if 'seg' in m:m['seg']=[[base+x[0],base+x[1]]+x[2:] for x in m['seg']]
   if 'buyu' in m:m['buyu']=[base+t for t in m['buyu']]
   D['MF'][a]=m
  if a in b['FRAMES']:D['FRAMES'][a]=b['FRAMES'][a]
  D['VU'][a]=[[base+x[0],base+x[1]] for x in b['VU'][a]]+D['VU'][a]
  D['ISTISNA'].discard(a)
  if a in b['ISTISNA']:D['ISTISNA'].add(a)
 for a in s['seams']:
  tw=base+b['seconds'];D['GOR'][a]=tw;D['MF'][a]={'buyu':[tw,tw+.6]};D['ISTISNA'].add(a)
  D['HAR'][a]=travel+[[stamp(h[0]),stamp(h[1])]+h[2:] for h in original['HAR'][a] if h[0]>=s['move']-.001]
  D['VU'][a]=[[tw,tw+1.4]]
 for r in b['ACN']:D['ACN'].append(dict(r,t0=base+r['t0'],t1=base+r['t1']))
 D['OLAY'].extend([[base+t,text] for t,text in b['OLAY']])
 D['OLAY'].append([base,'Tezgâh grubu: '+s['head'].replace('_',' ')+' — fikstür, bağlantı ve takım erişimi denetimi henüz tamamlanmadı.'])
 if s['seams']:D['OLAY'].append([base+b['seconds'],'Grup kaynakları: gerçek dikiş yerleri; torç yolu ve yük aktarımı denetimi henüz tamamlanmadı.'])
 report.append({'head':s['head'],'members':sorted(s['members']),'base_seconds':base,'departure_seconds':depart,'bench_offset_m':ofs.tolist(),'station_start_offset_m':s['ofs'].tolist(),'delivery_offsets_m':[q.tolist() for q in s['delivery']],'added_seconds':s['delta'],'bench_paths_passed':True,'fixture_verified':False,'joining_verified':False})
D['OLAY'].sort(key=lambda r:r[0]);D['ACN'].sort(key=lambda r:r['t0']);D['TOPLAM']=stamp(original['TOPLAM'])
D['prototype_bench_integration']=True;D['production_release']=False
D['station_plan_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
D['bench_plan_sha256']=hashlib.sha256((H/'bench_plans.pkl').read_bytes()).hexdigest()
assert set(D['P'])==set(original['P']) and set(D['GOR'])==set(original['GOR'])
for a in D['P']:
 assert np.array_equal(D['P'][a]['V'],original['P'][a]['V']) and np.array_equal(D['P'][a]['F'],original['P'][a]['F'])
 assert all(h[1]>=h[0] for h in D['HAR'][a])
 assert D['GOR'][a]>=0
out=H/'plan_k_full.pkl';pickle.dump(D,out.open('wb'))
rows={'source_plan_sha256':D['station_plan_sha256'],'source_model_sha256':D['source_model_sha256'],'combined_plan_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'groups':report,'geometry_unchanged':True,'group_count':len(report),'production_release':False,'full_ccd_checked':False,'parts':len(D['P']),'duration_seconds':D['TOPLAM']}
(H/'bench_integration_audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('BENCH_INTEGRATED',len(report),'parts',len(D['P']),'seconds',D['TOPLAM'],'GEOMETRY_UNCHANGED',flush=True)
