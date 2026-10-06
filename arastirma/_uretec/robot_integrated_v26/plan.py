"""Compact shop around the unchanged v25 robot, machine and 12 QR bays."""
from pathlib import Path
import json, math
from shapely.geometry import Polygon, box, Point
from shapely.ops import unary_union

ROOT=Path(__file__).resolve().parents[3]
A=ROOT/'otonom/hat3d/robot-integrated-v26'
OLD=ROOT/'otonom/hat3d/robot-integrated-v25'
scan=json.loads((OLD/'layout_scan.json').read_text())
floor=json.loads((OLD/'floor_plan.json').read_text())
def poly(p):return Polygon(p['outer'],p['holes'])
def polygons(g):
    if g.is_empty:return []
    return [{'outer':list(p.exterior.coords),'holes':[list(h.coords) for h in p.interiors]} for p in (g.geoms if hasattr(g,'geoms') else [g]) if p.geom_type=='Polygon' and p.area>1e-10]

left=.636; right=scan['right_wall_inner_x_m']; back=-.880
partition=math.ceil((max(s['max'][2] for s in scan['stage_bounds'].values())+.060)*1000)/1000
pocket=.800; desk_depth=.620; front=partition+pocket+desk_depth
door=[left+.050,left+.950]
desk=[left+1.100,3.097]
sink=[3.097,3.597]
trench=unary_union([poly(p) for p in floor['trench']])
water_holes=unary_union([Point(x,3.470).buffer(r+.0004,quad_segs=16) for x,r in [(3.290,.008),(3.325,.008),(3.455,.016)]])
new_floor=box(left-.050,back-.050,right+.280,front+.060).difference(trench).difference(water_holes)
robot_min_x=min(s['min'][0] for s in scan['stage_bounds'].values())
robot_max_z=max(s['max'][2] for s in scan['stage_bounds'].values())
plan={
 'version':26,'units':'metres; X along machine, Y up, +Z customer/front',
 'inner_bounds':[[left,0,back],[right,2.400,front]],
 'inner_dimensions_m':[right-left,front-back],
 'inner_area_m2':round((right-left)*(front-back),3),
 'floor_bounds':[[left-.050,-.010,back-.050],[right+.280,0,front+.060]],
 'floor':polygons(new_floor),'water_holes':polygons(water_holes),
 'partition':{'z_m':partition,'x_m':[left,3.597],'height_m':2.050,'outline_only':True,'physical_guard_certified':False},
 'doors':[
  {'name':'DUKKAN_GIRIS','x_m':door,'z_m':front,'clear_width_m':.900,'clear_height_m':2.080,'opening_side':'outside +Z','swing_radius_m':.894},
  {'name':'ROBOT_ALANI_GIRIS','x_m':door,'z_m':partition,'clear_width_m':.900,'clear_height_m':2.080,'opening_side':'staff +Z','swing_radius_m':.894,'interlock_required':True}],
 'desk':{'bounds':[[desk[0],.740,partition+pocket],[desk[1],.770,front]],'seated_pocket_m':pocket,
         'knee_clear_bounds':[[2.040,0,partition+pocket],[2.840,.715,front-.005]],'generic_furniture_envelope':True},
 'chair':{'centre':[2.440,.460,partition+.430],'seat_m':[.460,.030,.430],'behind_seat_clearance_m':.170,'behind_chair_passage':False},
 'sink':{'bounds':[[sink[0],0,partition+pocket],[sink[1],.900,front]],'bowl_inner_mm':[300,300,150],
         'bowl_centre_xz':[3.347,partition+pocket+.230],'sheet_thickness_m':.001,'drain_diameter_m':.032,
         'cold_hot_from_building':True,'no_immersion_or_electric_heater':True,'manufacturer_cad':False,
         'drain_and_water_floor_ports_xz':[[3.290,3.470],[3.325,3.470],[3.455,3.470]]},
 'preserved':['machine v10l','v25 inward box path','all14 GLB clips','8 order controls','12 QR bays','QR reader/keypad','rail','9 floor electrical routes','right wall X5.360'],
 'clearance':{'conservative_partition_to_recorded_body_m':partition-robot_max_z,'left_wall_to_recorded_body_m':robot_min_x-left,
              'machine_left_air_m':.736-left,'machine_back_air_m':-.830-back,'machine_right_air_m':right-5.230,
              'desk_to_partition_m':pocket,'entrance_to_robot_door_m':front-partition,
              'customer_zone_x_m':[3.597,right],'door_sweep_to_desk_x_gap_m':desk[0]-door[1]},
 'references':{'seated_knee_foot_clearance':'https://www.osha.gov/etools/computer-workstations/checklists/purchasing-guide'},
 'open':['planning dimensions, not a building survey','robot guarding/interlock and electrical safety not certified','door/egress/accessibility approval pending','hot/cold supply, drainage fall and floor penetrations require installation design','full pre-existing robot/station collision certification remains open']}
assert plan['clearance']['conservative_partition_to_recorded_body_m']>=.060
assert plan['clearance']['door_sweep_to_desk_x_gap_m']>=.100-1e-8
assert front-partition>2*.894-.5  # neither door opens into the other closed door
assert trench.difference(box(*[left-.05,back-.05,right+.28,front+.06])).area<1e-8
(A/'shop_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'inner_m':plan['inner_dimensions_m'],'area_m2':plan['inner_area_m2'],'partition_clearance_mm':1000*plan['clearance']['conservative_partition_to_recorded_body_m'],'seated_pocket_mm':800,'door_clear_mm':900}))
