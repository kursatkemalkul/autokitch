from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[4]; OUT=ROOT/'_local/codex_k_montaj'
def audit(records):
 ws=[]
 for x in records:
  if x['node'].startswith('K_GOVDE'):
   d=sorted(b-a for a,b in zip(x['lo'],x['hi']))
   if abs(d[0]-1)<.06 and abs(d[1]-10)<.25 and abs(d[2]-10)<.25:ws.append(x)
 unresolved=[];result=[]
 for w in ws:
  lo,hi=w['lo'],w['hi']; k=min(range(3),key=lambda i:hi[i]-lo[i]); side=[i for i in range(3) if i!=k];c=[(a+b)/2 for a,b in zip(lo,hi)]
  near=[x for x in records if x['node'].startswith('K_GOVDE') and x['id']!=w['id'] and max(abs((x['hi'][i]+x['lo'][i])/2-c[i]) for i in side)<.8]
  nuts=[x for x in near if abs(x['hi'][k]-x['lo'][k]-5)<.2 and min(x['hi'][i]-x['lo'][i] for i in side)>7.5 and (abs(x['lo'][k]-hi[k])<.15 or abs(x['hi'][k]-lo[k])<.15)]
  if len(nuts)!=1:unresolved.append({'washer':w['id'],'error':'nut not unique','count':len(nuts)});continue
  n=nuts[0];sgn=1 if abs(n['lo'][k]-hi[k])<.15 else -1
  studs=[x for x in near if x['lo'][k]<lo[k]+.1 and x['hi'][k]>hi[k]-.1 and 4.5<min(x['hi'][i]-x['lo'][i] for i in side)<7.5]
  if len(studs)!=1:unresolved.append({'washer':w['id'],'error':'stud not unique','count':len(studs)});continue
  s=studs[0];protrusion=s['hi'][k]-n['hi'][k] if sgn>0 else n['lo'][k]-s['lo'][k]
  result.append({'washer':w['id'],'nut':n['id'],'stud':s['id'],'axis':k,'direction':sgn,'protrusion_mm':round(protrusion,4),'pitch_mm':.8,'threads':round(protrusion/.8,3),'passed':.8-.01<=protrusion<=2.4+.01})
 return {'source_step':61,'current_geometry_only':True,'washers':len(ws),'results':result,'unresolved':unresolved,'passed':len(result)==len(ws) and not unresolved and all(x['passed'] for x in result)}
if __name__=='__main__':
 records=json.loads((OUT/'source_components.json').read_text(encoding='utf8'))['components']; r=audit(records)
 (OUT/'current_fastener_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps({'washers':r['washers'],'paired':len(r['results']),'unresolved':len(r['unresolved']),'protrusion_failures':sum(not x['passed'] for x in r['results']),'passed':r['passed']}))
