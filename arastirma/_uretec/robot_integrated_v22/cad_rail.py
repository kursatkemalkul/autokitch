"""Manufacturer STEP -> meshes. Archive untouched original; identify axial extension.

3000 mm is the public configurator limit; 3684 mm is an application concept,
requiring supplier confirmation. End housings, carriage and cross section stay
at their original dimensions. Only the continuous longitudinal region extends.
"""
from pathlib import Path
import json,hashlib,os
import cadquery as cq
ROOT=Path(__file__).resolve().parents[3]
source=ROOT/'_local/codex_robot_v22/igus_ZLW_20200_3000.stp'
out=ROOT/'otonom/hat3d/robot-integrated-v22'
solids=cq.importers.importStep(str(source)).solids().vals()
assert len(solids)==3
parts=[]
for i,s in enumerate(solids):
 verts,tris=s.tessellate(.35,.2)
 v=[]
 for p in verts:
  x,y,z=p.toTuple()
  if i==0:
   # Local Isaac frame of carriage: world z=.96, parent world z=.86.
   v.extend([(y-1620)/1000,-x/1000-.1,z/1000-.045])
  else:
   # Preserve end features. Stretch only the straight continuous middle.
   if y>=3040:y+=684
   elif y>200:y+=(y-200)/2840*684
   v.extend([1.056+y/1000,.05+z/1000,.96+x/1000])
 parts.append({'name':['CARRO','CABECERAS_CORREA','PERFIL'][i],'moving':i==0,'vertices':v,'indices':[x for t in tris for x in t]})
data={'parts':parts,'manufacturer':'igus','model':'ZLW-20200S-I0BW0-D0A4B-0A0A0-3000','source':'https://www.igus-cad.com/','source_step_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'downloaded_stroke_mm':3000,'concept_stroke_mm':3684,'supplier_confirmation_required':True,'units':'m; static meshes Y-up; moving mesh local Isaac Z-up','rail_axis_world_z_m':.96,'carriage_top_y_m':.114,'robot_mount_y_m':.13,'overall_axis_x_m':[.978,5.058]}
out.mkdir(parents=True,exist_ok=True)
(out/'rail_cad.json').write_text(json.dumps(data,separators=(',',':')),encoding='utf8')
print(json.dumps({k:v for k,v in data.items() if k!='parts'}),flush=True)
# OCP on this installed runtime sometimes faults during interpreter shutdown.
os._exit(0)
