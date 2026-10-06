"""One continuous recessed service trench; old openings are filled by the new floor."""
from pathlib import Path
import json
from shapely.geometry import LineString,box,mapping
from shapely.ops import unary_union

ROOT=Path(__file__).resolve().parents[3]
Y=-.040
wall=[5.30,1.48,-.80];split=[5.40,Y,-.60]
paths={
 'wall':[wall,[5.30,Y,-.80],[5.40,Y,-.80],split],
 'machine':[split,[4.047,Y,-.60],[4.047,Y,-.797],[4.047,.123,-.797]],
 'QR':[split,[5.40,Y,1.80],[4.096,Y,1.80],[4.096,Y,2.11],[4.096,1.69,2.11],[4.096,1.69,1.965]],
 'UR controller':[split,[5.40,Y,1.80],[4.64,Y,1.80],[4.64,Y,1.905],[4.64,.100,1.905]],
 'axis feed':[[4.64,Y,1.80],[3.965,Y,1.80],[3.965,Y,1.93],[3.965,.040,1.93]],
 'arm output':[[4.71,.100,1.905],[4.71,Y,1.905],[4.71,Y,1.80],[3.018,Y,1.80],[3.018,Y,1.185],[3.018,.058,1.185]],
 'axis drive':[[3.965,.040,1.93],[3.965,Y,1.93],[3.965,Y,1.80],[5.40,Y,1.80],[5.40,Y,.720],[5.025,Y,.720],[5.025,.0815,.720],[5.025,.0815,.745]],
}
segments=[]
for name,pts in paths.items():
 for a,b in zip(pts,pts[1:]):
  if a[1]==Y and b[1]==Y:
   segments.append(LineString([(a[0],a[2]),(b[0],b[2])]).buffer(.040,cap_style=3,join_style=2))
foot=unary_union(segments).buffer(0)
floor=box(-.864,-.86,6.336,2.17)
assert foot.geom_type=='Polygon' and floor.covers(foot)
surface=floor.difference(foot)
def polygons(geom):
 return [{'outer':list(p.exterior.coords),'holes':[list(h.coords) for h in p.interiors]} for p in (geom.geoms if hasattr(geom,'geoms') else [geom])]
out={'version':22,'units':'metres; Y up','paths':paths,'floor':polygons(surface),'trench':polygons(foot),'walls':polygons(foot.difference(foot.buffer(-.0015))), 'lids':polygons(unary_union([foot.intersection(box(-.9+i*.8,-.9+j*.7,-.9+(i+1)*.8-.0006,-.9+(j+1)*.7-.0006)) for i in range(10) for j in range(5)])),'width_m':.080,'depth_m':.080,'lid_thickness_m':.006,'lid_top_y_m':0,'horizontal_divider_y_m':-.040,'power_centre_y_m':-.060,'signal_centre_y_m':-.022,'single_connected_trench':True,'former_floor_openings_filled':True,'floor_bounds':[[-.864,-.86],[6.336,2.17]],'installation':'recessed load-rated frame/lids; final slab and pedestrian load approval pending'}
(ROOT/'otonom/hat3d/robot-integrated-v22/floor_plan.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps({'connected_trenches':1,'lid_top_y_m':0,'area_m2':foot.area}))
