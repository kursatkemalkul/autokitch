"""Tessellate the unchanged manufacturer's Storm K-range STEP (12-way)."""
from pathlib import Path
import cadquery as cq
import json,hashlib,os
ROOT=Path(__file__).resolve().parents[3]
source=Path(__file__).parent/'vendor/K_Range 12 way.STEP'
solids=cq.importers.importStep(str(source)).solids().vals()
bb=solids[0].BoundingBox()
dimensions=[bb.xlen,bb.ylen,bb.zlen];centre=[(bb.xmin+bb.xmax)/2,(bb.ymin+bb.ymax)/2];front=bb.zmax
parts=[]
for i,s in enumerate(solids):
    vertices,triangles=s.tessellate(.15,.15)
    points=[p.toTuple() for p in vertices]
    parts.append({'name':['KEYPAD','CONNECTOR','CONTACT_1','CONTACT_2'][i], 'vertices':[c/1000 for p in points for c in p], 'indices':[c for t in triangles for c in t]})
data={'manufacturer':'Storm Interface','model':'2000 series 12-key telephone, 2K12T10','source':'https://shop.storm-interface.com/2000-series-12-key-telephone.html','cad_url':'https://shop.storm-interface.com/pub/media/productattachments/files/File-1494330773.zip','source_step_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'dimensions_mm':dimensions,'centre_xy_mm':centre,'front_z_mm':front,'parts':parts,'units':'metres; same X/Y/Z axes as supplier CAD','modified_manufacturer_geometry':False,'usb_encoder_required':'Storm 450 USB encoder'}
(ROOT/'otonom/hat3d/robot-integrated-v24/keypad_cad.json').write_text(json.dumps(data,separators=(',',':')),encoding='utf8')
print(json.dumps({k:v for k,v in data.items() if k!='parts'}),flush=True)
os._exit(0)
