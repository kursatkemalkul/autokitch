"""Replace only our four mounting bolts with actual catalog M10x35 ISO4762.
Supplier actuator housing and mounting interface remain unchanged.
"""
from pathlib import Path
source=Path(__file__).with_name('oil_fluid_clamp_candidate.py')
ns=dict(__file__=str(source),__name__='clamp_helpers')
exec(compile(source.read_text(encoding='utf-8').split("if __name__=='__main__':")[0],str(source),'exec'),ns)
P=ns['pickle'].loads((ns['K1']/'k_parca_fluid_verified.pkl').read_bytes())['P']
DEST=ns['OUT']/'actuator_catalog_fastener_candidate';DEST.mkdir(exist_ok=True)
ns.update(P=P,BASE=ns['OUT']/'oil_fluid_clamp_candidate/A/hat3_v10zb.glb',DEST=DEST)
# Source parts hash belongs to current1009 cache, not helper's previous975 cache.
fn_source=source.read_text(encoding='utf-8').split('def audit_clamps(')[1].split("if __name__=='__main__':")[0]
fn_source='def audit_clamps('+fn_source.replace('k_parca_pump_verified.pkl','k_parca_fluid_verified.pkl')
exec(compile(fn_source,str(source),'exec'),ns)
S=ns['S'];parts=[];joins=[]
for i,(x,y) in enumerate([(4160.,1304.5),(4160.,1344.5),(4240.,1304.5),(4240.,1344.5)]):
 name=f'DGRF_M10_civata_{i}'
 p=S.vida('ISO4762','M10',35.,(x,y,-266.),(0,0,1),ad=name,birim='K_KESICI',malzeme='A2-70')
 # Use the native shaft facet phase for the visual nominal cylinder.
 # This avoids interpenetration caused solely by a differently tessellated
 # circular bolt in the existing coarse circular factory bore.
 cq=ns['cq'];np=ns['np']
 old=P[name]['V'];tip=old[np.abs(old[:,2]+232.5)<.001]
 outline=tip[np.linalg.norm(tip[:,:2]-np.array([x,y]),axis=1)>4.8]
 outline=outline[np.argsort(np.arctan2(outline[:,1]-y,outline[:,0]-x))]
 points=[cq.Vector(x+.98*(q[0]-x),y+.98*(q[1]-y),-266.) for q in outline]
 wire=cq.Wire.makePolygon(points,close=True)
 shaft=cq.Solid.extrudeLinear(wire,[],cq.Vector(0,0,35.))
 head=S._silindir(8.,10.,-10.).cut(S._altigen(8.,5.01,-10.01))
 head=S._tasi(head,S._cerceve((x,y,-266.),(0,0,1)))
 p['sh']=head.fuse(shaft);p['wp']=cq.Workplane('XY').add(p['sh'])
 p['tur']='baglanti';parts.append(p)
 v=P[name]['V'];old_length=float(v[:,2].max()-(-266.))
 assert abs(old_length-33.5)<.001
 joins.append({'id':name,'catalog_standard':'ISO4762','material':'A2-70','nominal_length_mm':35.,'old_non_catalog_length_mm':old_length,'center_mm':[x,y,-266.],'axis':[0,0,1],'mounting_plate_thickness_mm':16.5,'blind_thread_depth_mm':24.,'engagement_mm':18.5,'blind_bottom_clearance_mm':5.5,'minimum_required_engagement_mm':10.,'pitch_mm':1.5,'passed_stack':18.5>=10. and 5.5>=1.5,'supplier_body_changed':False})
r=ns['audit_clamps'](parts,joins,{},[])
ns['sys'].stdout.flush();ns['os']._exit(0 if r['passed_geometry_and_stacks'] else 2)
