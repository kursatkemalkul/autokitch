"""Local step77 prototype: bottom-open slots at two K roof/rear stud interfaces.
Allows a real downward roof insertion after the rear panel and equipment.
Keeps rear panel, studs and external dimensions; no animation exception.
"""
from lower_support import *
import subprocess,hashlib
Y=H/'yama_v9'
for path in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(path))
from m8kit import Glb
import sac_ent as SE
import manifold3d as mf

def apply(source,dest):
 g=Glb(str(source));g.bilesen('K_GOVDE__kabuk',0)
 candidates=[b for b in g._bc['K_GOVDE__kabuk'] if abs(b['hi'][1]-1862)<.05 and b['hi'][0]-b['lo'][0]>399 and b['hi'][2]-b['lo'][2]>880]
 assert len(candidates)==1,len(candidates)
 sourcepart=candidates[0];origin=np.array([4200.,1853.,-828.5])
 source_triangles=np.concatenate([p['X'][p['T'][idx]] for p,idx in sourcepart['parca']])-origin
 # The GLB compression creates sub-micron split vertices. Weld only on a
 # declared 0.001 mm grid; require a closed two-face edge topology afterwards.
 rounded=np.round(source_triangles,3)
 max_vertex_adjustment=float(np.max(np.linalg.norm(rounded-source_triangles,axis=2)))
 assert max_vertex_adjustment<0.00087,max_vertex_adjustment
 V,inv=np.unique(rounded.reshape(-1,3),axis=0,return_inverse=True);F=inv.reshape(-1,3)
 edges=np.sort(np.concatenate((F[:,[0,1]],F[:,[1,2]],F[:,[2,0]])),axis=1)
 _,counts=np.unique(edges,axis=0,return_counts=True)
 assert np.all(counts==2),'Precision welding did not restore a closed mesh'
 original=SE.mf_ucgen(rounded)
 assert original is not None,'Source body must be closed for local slot machining'
 changed=original;zones=None;slots=[]
 for x in (4040.,4360.):
  xx=x-origin[0]
  # Rear sheet ends at z=-828.5: cut only on its inner side, in roof return.
  rect=mf.Manifold.cube((5.5,13.,1.51)).translate((xx-2.75,-13.,0.))
  roundtop=mf.Manifold.cylinder(1.51,2.75,2.75,circular_segments=64).translate((xx,0.,0.))
  tool=rect+roundtop;changed=changed-tool;zones=tool if zones is None else zones+tool
  slots.append({'center_mm':[x,1853,-828.5],'width_mm':5.5,'bottom_open_y_mm':1840,'upper_radius_mm':2.75,'depth_mm':1.51,'existing_M5_stud_retained':True,'reason':'Roof lowers over horizontal rear studs; ISO7089 washer and ISO10511 nut are fitted afterwards'})
 delta=(original-changed)+(changed-original)
 assert (delta-zones).volume()<.01,'Change escaped declared roof slot machining zones'
 removed=original.volume()-changed.volume();assert .1<removed<500,removed
 g.sil_b(sourcepart);g.ucgen_ekle('K_GOVDE__kabuk',SE.mf_P(changed)+origin,kat=0,mek=24)
 raw=dest.with_suffix('.raw.glb');g.kaydet(str(raw));del g
 subprocess.run([sys.executable,str(Y/'50_sikilastir.py'),str(raw),str(dest)],env=dict(os.environ,YAMA_IS_KOK=str(Y/'kaynak')),check=True);raw.unlink()
 r={'step':77,'precision_grid_mm':0.001,'max_vertex_adjustment_mm':max_vertex_adjustment,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'slots':slots,'removed_volume_mm3':removed,'delta_outside_slots_mm3':(delta-zones).volume(),'rear_panel_modified':False,'studs_modified':False,'animation_exceptions_added':False,'production_release':False}
 dest.with_suffix('.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print('STEP77',r['output_sha256'],'removed_mm3',removed,flush=True)
if __name__=='__main__':
 apply(*map(Path,sys.argv[1:3]));sys.stdout.flush();os._exit(0)
