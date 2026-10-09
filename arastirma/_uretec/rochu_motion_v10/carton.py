"""Closed, uncut carton. Centre-edge grasp; no carton cuts."""
from v2 import *

def create_carton(r):
 b=r.products['Box']['bounds'];c=b.mean(0);size=b[1]-b[0];thickness=.0015
 outer=md.Manifold.cube(size.tolist(),center=True)
 inner=md.Manifold.cube((size-2*thickness).tolist(),center=True)
 closed=outer-inner
 p=deepcopy(json.loads((OUT/'review.json').read_text())['box_support']['variants']['edge']['pose'])
 R=np.array(p['tool_orientation']);contact=np.array(p['contact'])-[0,0,.016]
 W=ident(contact-R@np.array([0,0,TIP]));W[:3,:3]=R
 ports=closed
 entries=[]
 scene=trimesh.Scene()
 for name,a,color in [('Carton_with_ports',ports,[.66,.44,.23,1]),('Carton_without_ports',closed,[.66,.44,.23,1])]:
  d=a.to_mesh();v=np.asarray(d.vert_properties)[:,:3];f=np.asarray(d.tri_verts,dtype=np.int32)
  scene.add_geometry(mesh(v,f,color),node_name=name,geom_name=name)
 save_scene(scene,'carton')
 result={'outer_dimensions_mm':(size*1000).tolist(),'proposed_wall_thickness_mm':1.5,'wall_thickness_is_assumption':True,'entry_count':0,'entries':[],'insertion_depth_mm':0,'root_hash':r.definition['root_hash'],'boolean_status':str(ports.status()),'closed_volume_mm3':closed.volume()*1e9,'cut_volume_mm3':0,'carton_strength_verified':False,'secure_grasp_verified':False,'description':'Closed uncut carton. Finger bodies stay mounted; flexible ends open and close around the centre of the front edge.'}
 (OUT/'carton_definition.json').write_text(json.dumps(result,indent=2))
 print('CARTON',result['entry_count'],'notches',result['cut_volume_mm3'],'mm3 removed',flush=True)
 return result,p,contact,ports

if __name__=='__main__':create_carton(Review())
