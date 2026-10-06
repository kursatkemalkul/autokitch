"""One flush trench tree, separate cable lanes, continuous rounded hollow risers."""
from pathlib import Path
import json
from shapely.geometry import LineString,box
from shapely.ops import unary_union
from routing import rounded,ramp
ROOT=Path(__file__).resolve().parents[3]
A=ROOT/'otonom/hat3d/robot-integrated-v23'

def power_start(x,z,floor_z):
    return [[x-.14,1.0,z],[x-.14,.90,z],[x,.90,z],[x,-.060,z],[x,-.060,floor_z]]
raw={
 'MAKINE_BESLEME':power_start(6.31,-.36,-.64)+[[4.047,-.060,-.64],[4.047,-.060,-.797],[4.047,.123,-.797]],
 'QR_GUC':power_start(6.29,-.32,-.62)+[[5.36,-.060,-.62],[5.36,-.060,1.776],[4.096,-.060,1.776],[4.096,-.060,2.11],[4.096,1.69,2.11],[4.096,1.69,1.965]],
 'ROBOT_BESLEME':power_start(6.27,-.28,-.60)+[[5.38,-.060,-.60],[5.38,-.060,1.800],[4.64,-.060,1.800],[4.64,-.060,1.890],[4.64,.100,1.890]],
 'SURUCU_BESLEME':power_start(6.25,-.24,-.58)+[[5.40,-.060,-.58],[5.40,-.060,1.824],[3.965,-.060,1.824],[3.965,-.060,1.930],[3.965,.040,1.930]],
 'SERVO_MOTOR_KABLO':[[4.04,.040,1.93],[4.04,-.072,1.93],[4.04,-.072,1.844],[5.44,-.072,1.844],[5.44,-.072,.680],[5.025,-.072,.680],[5.025,.0815,.680],[5.025,.0815,.745]],
}
raw['SURUCU_BESLEME']=[[x, -.072 if y==-.060 else y,z] for x,y,z in raw['SURUCU_BESLEME']]
raw['SERVO_MOTOR_KABLO']=[[x, -.046 if y==-.072 else y,z] for x,y,z in raw['SERVO_MOTOR_KABLO']]
cables={k:{**rounded(p,.040),'radius_m':.005 if k in ('MAKINE_BESLEME','ROBOT_BESLEME') else .004,'kind':'power','raw':p} for k,p in raw.items()}
sr=ramp(dy=.084);p=[[4.71,.100,1.82],[4.71,-.026,1.82],[2.72,-.026,1.82],[2.72,-.026,1.185],sr['points'][0]]
c=rounded(p,.060);offset=len(c['points'])-1;c['points']+=sr['points'][1:];c['arcs']+=[{**x,'first':x['first']+offset,'last':x['last']+offset} for x in sr['arcs']]
cables['UR_HIGH_FLEX_12M_SABIT']={**c,'radius_m':.0073,'kind':'robot','raw':p,'end_connection':'energy chain fixed end'}
# Ethernet is kept in the upper separated compartment, on its own lane.
for idx,(name,target,x,z) in enumerate([('MAKINE_ETHERNET',[4.06,.123,-.797],0,0),('QR_ETHERNET',[4.12,1.69,1.965],5.30,1.708),('UR_ETHERNET',[4.60,.100,1.89],5.32,1.730)]):
    wx=6.240-idx*.008;wz=idx*.022;fy=-.0125;fz=-.52+idx*.022
    start=[[wx-.14,1.0,wz],[wx-.14,.82,wz],[wx,.82,wz],[wx,fy,wz],[wx,fy,fz]]
    if name=='MAKINE_ETHERNET':path=start+[[4.06,fy,fz],[4.06,fy,-.797],target]
    elif name=='QR_ETHERNET':path=start+[[x,fy,fz],[x,fy,z],[4.12,fy,z],[4.12,fy,2.11],[4.12,1.69,2.11],target]
    else:path=start+[[x,fy,fz],[x,fy,z],[4.60,fy,z],[4.60,fy,1.89],target]
    cables[name]={**rounded(path,.025),'radius_m':.003,'kind':'data','raw':path}
moving={**rounded([[0,-.325,.263],[-.180,-.325,.263],[-.180,-.325,.060],[-.180,-.100,.060],[-.105,-.100,.060]],.060),'radius_m':.0073,'kind':'robot'}

# The trench is the union of the actual cable corridor envelopes, not overlapping boxes.
trench_segments=[]
for c in cables.values():
    pts=c['points']
    for a,b in zip(pts,pts[1:]):
        if max(a[1],b[1])<.002:
            trench_segments.append(LineString([(a[0],a[2]),(b[0],b[2])]).buffer(.034,cap_style=3,join_style=1,quad_segs=16))
# Supply paths, branching tee and chain transition remain connected to the shared corridor.
trench_segments += [box(6.215,-.70,6.336,.105),box(2.80,1.14,3.06,1.23)]
foot=unary_union(trench_segments).buffer(0)
floor=box(-.864,-.86,6.336,2.17)
foot=foot.intersection(floor)
assert foot.geom_type=='Polygon',f'Disconnected trench: {foot.geom_type}'

def polygons(geom):
    if geom.is_empty:return []
    return [{'outer':list(p.exterior.coords),'holes':[list(h.coords) for h in p.interiors]} for p in (geom.geoms if hasattr(geom,'geoms') else [geom]) if p.geom_type=='Polygon' and p.area>1e-10]

spec=[]
def duct(name,pts,width=.050,height=.050,normal=(1,0,0),r=.040):
    spec.append({'name':name,**rounded(pts,r),'width_m':width,'height_m':height,'wall_m':.0015,'normal':normal,'connection':'continuous hollow trunk; butt welded radius elbow; removable cover; gland at equipment'})
duct('MAKINE_DIK',[[4.047,0,-.797],[4.047,.123,-.797]],.050,.050,(1,0,0))
duct('QR_DIK',[[4.108,0,2.11],[4.108,1.69,2.11],[4.108,1.69,1.965]],.070,.070,(1,0,0))
for n,x,z,y,w,h in [('UR_GIRIS',4.62,1.89,.100,.080,.065),('UR_CIKIS',4.71,1.82,.100,.060,.070),('SURUCU_GIRIS',3.965,1.93,.040,.050,.050),('SURUCU_CIKIS',4.04,1.93,.040,.050,.050)]:duct(n,[[x,0,z],[x,y,z]],w,h,(0,0,1))
duct('MOTOR_DIK',[[5.025,0,.680],[5.025,.0815,.680],[5.025,.0815,.745]],.045,.045,(1,0,0))
spec.append({'name':'ZINCIR_GECIS',**sr,'width_m':.034,'height_m':.070,'wall_m':.0015,'normal':[0,0,1],'connection':'rounded fixed transition, end supported on chain guide'})
# Wall power/data trunk is embedded; short enclosed bends under the cabinet only.
duct('DUVAR_GUC',[[6.14,1.0,-.30],[6.14,.90,-.30],[6.28,.90,-.30],[6.28,0,-.30]],.080,.190,(0,0,1))
duct('DUVAR_VERI',[[6.092,1.0,.022],[6.092,.82,.022],[6.232,.82,.022],[6.232,0,.022]],.028,.105,(0,0,1),.025)
opening_shapes=[];neck_shapes=[]
for d in spec:
    if d['name']=='ZINCIR_GECIS':
        neck_shapes.append(box(2.90,1.15,3.025,1.22));opening_shapes.append(box(sr['points'][0][0]-.02,1.14,3.06,1.23));continue
    low=min(d['points'],key=lambda p:p[1]);x,_,z=low
    opening_shapes.append(box(x-.052,z-.055,x+.052,z+.055))
    # Vertical section projects directly to X/Z. Flat escutcheon fills the oversized service hole.
    wx=d['width_m']/2 if d['normal']==(0,0,1) or d['normal']==[0,0,1] else d['height_m']/2
    wz=d['height_m']/2 if d['normal']==(0,0,1) or d['normal']==[0,0,1] else d['width_m']/2
    neck_shapes.append(box(x-wx-.0003,z-wz-.0003,x+wx+.0003,z+wz+.0003))
opening_shapes.extend([box(6.218,-.41,6.336,-.19),box(6.216,-.035,6.28,.105)])
openings=unary_union(opening_shapes);necks=unary_union(neck_shapes);collars=openings.intersection(foot).difference(necks)
# Cut to manageable lid/wall modules with butt joints; one union for seam supports.
cells=[box(-.9+i*.8,-.9+j*.7,-.9+(i+1)*.8-.0006,-.9+(j+1)*.7-.0006) for i in range(10) for j in range(5)]
wall=foot.difference(foot.buffer(-.0015));wall=wall.difference(openings)
lids=[];walls=[]
for cell in cells:lids+=polygons(foot.intersection(cell).difference(openings));walls+=polygons(wall.intersection(cell))
support=[]
for i in range(1,10):support.append(box(-.9+i*.8-.008,-.90,-.9+i*.8+.008,2.2))
for j in range(1,5):support.append(box(-.9,-.9+j*.7-.008,6.4,-.9+j*.7+.008))
support.append(foot.difference(foot.buffer(-.012)))
supports=unary_union(support).intersection(foot).difference(openings)
out={'version':23,'units':'metres; Y up','cables':cables,'moving_cable':moving,'duct_specs':spec,'paths':{k:c['raw'] for k,c in cables.items()},'floor':polygons(floor.difference(foot)),'trench':polygons(foot),'walls':walls,'divider':polygons(foot.difference(openings)),'lids':lids,'lid_supports':polygons(supports),'openings':polygons(openings.intersection(foot)),'flush_escutcheons':polygons(collars),'lid_passages':polygons(necks.intersection(foot)),'width_m':'variable shared lanes, minimum 68 mm','depth_m':.080,'lid_thickness_m':.006,'lid_top_y_m':0,'horizontal_divider_y_m':-.040,'power_centre_y_m':-.060,'signal_centre_y_m':-.022,'single_connected_trench':True,'former_floor_openings_filled':True,'floor_bounds':[[-.864,-.86],[6.336,2.17]],'wall_box':{'wall_inner_x_m':6.216,'wall_outer_x_m':6.336,'cabinet_bounds':[[5.946,1.000,-.450],[6.196,1.700,.150]],'power_data_separation':True},'installation':'recessed frame/flush lids; cable voltage/section/protection selectivity and slab/pedestrian load approval pending'}
(A/'floor_plan.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps({'connected_trenches':1,'lid_top_y_m':0,'area_m2':foot.area,'cable_routes':len(cables),'hollow_risers':len(spec)}))
