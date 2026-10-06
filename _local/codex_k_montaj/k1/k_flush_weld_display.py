"""Surface process markings for ground-flush welds; not added physical stock.
Uses only existing common-player fields: mesh, material, visibility, movement.
Every marking lies on the real cap sidewall; product source meshes are untouched.
"""
import numpy as np

def export_markers(D,material_names):
 meshes=[];parts={};records=[]
 for operation in D.get('FABRICATION_JOINS',[]):
  profile=operation['profile'];cap=operation['cap']
  assert profile in D['P'] and cap in D['P']
  def offset(name,t):
   result=np.zeros(3)
   for row in D['HAR'][name]:
    u=min(1.,max(0.,(t-row[0])/(row[1]-row[0]))) if row[1]>row[0] else float(t>=row[1])
    result+=np.asarray(row[2:5])*(1.-u*u*(3.-2.*u))
   return result
  boundaries={operation['t0'],operation['t1'],D['TOPLAM']}
  for name in (profile,cap):
   boundaries.update(t for row in D['HAR'][name] for t in row[:2] if t>=operation['t0'])
  times=sorted(boundaries);times+=list((np.asarray(times[:-1])+np.asarray(times[1:]))/2.)
  assert all(np.linalg.norm(offset(profile,t)-offset(cap,t))<1e-8 for t in times)
  assert not D['ROT'].get(profile) and not D['ROT'].get(cap)
  assert operation['t1']>operation['t0']
  perimeter=sum(s['length_mm'] for s in operation['root_segments_mm']);travelled=0.
  for i,segment in enumerate(operation['root_segments_mm']):
   a=np.asarray(segment['start_mm'],float);b=np.asarray(segment['end_mm'],float)
   # Coplanar display strip on the cap's actual outer face. It represents
   # the TIG operation after grinding, not a protruding bead or fastener.
   V=np.array([a,b,b+[0.,.4,0.],a+[0.,.4,0.]])/1000.
   F=np.array([[0,1,2],[0,2,3]],dtype=np.int32)
   c=np.round((V.min(0)+V.max(0))/2,6)
   name='process_flush_TIG_'+cap+'_'+str(i)
   g=operation['t0']+(operation['t1']-operation['t0'])*travelled/perimeter
   travelled+=segment['length_mm']
   meshes.append(dict(ad=name,V=V-c,F=F,mat=material_names.index('kaynak'),translation=c))
   parts[name]=dict(c=c.tolist(),m='kaynak',bb=[V.min(0).tolist(),V.max(0).tolist()],g=g,h=[list(x) for x in D['HAR'][cap]],ad='Dikme tapası çevresel TIG: taşlanmış kaynak yüzeyi işareti',process_marking=True,physical_part=False,reference_cap=cap)
   if D['ROT'].get(profile):parts[name]['r']=[list(x) for x in D['ROT'][profile]]
   records.append(dict(name=name,reference_cap=cap,operation_start=operation['t0'],operation_end=operation['t1'],source_root_segment=i,physical_part=False))
 return meshes,parts,records
