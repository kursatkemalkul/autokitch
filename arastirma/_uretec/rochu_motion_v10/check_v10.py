"""Inspect the rendered scene, including removed covers and actual cut supports.
Native triangle crossing confirms conservative Boolean candidates separately.
"""
from motion_v10 import *
import argparse

def scene_fixtures(r):
 scene=trimesh.load(io.BytesIO(gzip.decompress((OUT/'focus.glb.gz').read_bytes())),file_type='glb')
 manifest=json.loads((OUT/'focus_manifest.json').read_text());result=[]
 for row in manifest:
  if row['group'].startswith(('UR10E','Product_')) or row['source'].startswith(('A_AGIZ','A_ONYUZ')) or row['source']=='E_GOVDE__on_seffaf':continue
  w,g=scene.graph[row['node']];t=scene.geometry[g];v=t.vertices@w[:3,:3].T+w[:3,3]
  result.append(dict(name=row['source'],world=v,faces=t.faces,bounds=np.array([v.min(0),v.max(0)]),group=row['group']))
 return result

def run(item,full=False):
 r=Review();fixtures=scene_fixtures(r);seq=json.loads((OUT/(item.lower()+'_v10_candidate.json')).read_text());frames=seq['frames'];report=[]
 selected=range(len(frames)) if full else sorted(set([0]+([next(i for i,f in enumerate(frames) if f['held']),max(i for i,f in enumerate(frames) if f['held'])] if any(f['held'] for f in frames) else [])+[i for i,f in enumerate(frames) if i==len(frames)-1 or f['label']!=frames[i+1]['label']]))
 for index in selected:
  f=frames[index];p=f['pose'];parts=r.tool_parts(p,arm=True);hits=[];proxies=0
  for s in fixtures:
   drawer=p['drawer_open_m'] if s['group']=='Drawer_'+item else 0
   opener=p.get('opener_lift_m',0) if s['group']=='Opener' else 0
   delta=np.array([0,opener,drawer]);bounds=s['bounds']+delta
   candidates=[x for x in parts if not np.any(x[1].max(0)<bounds[0]) and not np.any(x[1].min(0)>bounds[1])]
   if not candidates:continue
   bv,bf,b,bh=r.fixture(s,drawer=drawer)
   if opener:bv=bv+[0,opener,0];b=b.translate([0,opener,0])
   for name,v,faces,a,ah in candidates:
    volume=max(0,float((a^b).volume())*1e9)
    if volume<=.1:continue
    confirmed=bool(crosses(v[faces],bv[bf]));proxies+=int(bool(ah or bh))
    hits.append({'fixture':s['name'],'moving':name,'proxy_overlap_mm3':volume,'uses_proxy':bool(ah or bh),'native_surface_crossing':confirmed})
  row={'frame':index,'phase':f['label'],'hits':hits,'native_crossings':sum(x['native_surface_crossing'] for x in hits)};report.append(row)
  print(item,index,row['native_crossings'],[(x['fixture'],x['moving']) for x in hits if x['native_surface_crossing']][:6],flush=True)
  (OUT/(item.lower()+'_v10_scene_check.json')).write_text(json.dumps({'scope':'Sampled whole arm/head versus rendered static scene and moving drawer; product contact and continuous paths separate','full_frame_sampling':full,'rows':report},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('item',choices=['Dough','Cola','Dessert','Box']);p.add_argument('--full',action='store_true');args=p.parse_args();run(args.item,args.full)
