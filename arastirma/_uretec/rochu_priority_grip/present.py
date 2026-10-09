from parallel_probe import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
model,head=setup();report=json.loads((DEST/'selected.json').read_text());checks=json.loads((DEST/'verification.json').read_text());r=report['radius_mm'];names={'Dough':'HAMUR','Cola':'KOLA','Dessert':'TATLI','Box':'PİDE KUTUSU'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none'})
datasets={};assembly=trimesh.Scene();root_specs=[]
for n in head.graph.nodes_geometry:
 if not n.startswith('OEM_DAC_'):continue
 w,g=head.graph[n];w=w.copy();w[:2,3]*=r/50;w[:3,:3]=Rotation.from_euler('z',90 if w[1,3]>0 else -90,degrees=True).as_matrix();m=head.geometry[g].copy();m.visual=trimesh.visual.ColorVisuals(m,vertex_colors=[61,80,91,255]);assembly.add_geometry(m,node_name=n,geom_name=n,transform=w);root_specs.append({'name':n,'matrix':w.tolist()})
(DEST/'fixed-fingers.glb').write_bytes(assembly.export(file_type='glb'))
for item,row in report['products'].items():
 p=Probe(model,head,item)
 if item=='Dessert':p.vertices*=np.array([.065/np.ptp(p.vertices[:,0]),1,.0655/np.ptp(p.vertices[:,2])]);p.eq=np.unique(np.round(ConvexHull(p.vertices).equations,9),axis=0)
 product=(p.vertices-p.base-p.R[:,2]*row['depth_mm']*.001)@p.R
 m=trimesh.Trimesh(product,p.s['faces'],process=False);m.visual=trimesh.visual.ColorVisuals(m,vertex_colors=([213,169,102,255] if item=='Dough' else [191,52,45,255] if item=='Cola' else [203,179,133,255]));(DEST/(item.lower()+'.glb')).write_bytes(trimesh.Scene(m).export(file_type='glb'))
 parts={a['name']:a for a in row['parts']};points=[];meshes=[]
 for spec in root_specs:
  n=spec['name'];w=np.array(spec['matrix']);_,g=head.graph[n];t=head.geometry[g];shift=parts[n]['shift_mm'];v=deform(t.vertices,shift)@w[:3,:3].T+w[:3,3];opened=deform(t.vertices,-11)@w[:3,:3].T+w[:3,3]
  if item!='Dough':point=(np.array(parts[n]['point_world_relative'])-p.base-p.R[:,2]*row['depth_mm']*.001)@p.R
  else:
   world=v@p.R.T+p.base+p.R[:,2]*row['depth_mm']*.001;pl=world@p.eq[:,:3].T+p.eq[:,3];d=-pl.max(1)*1000;mask=(t.vertices[:,2]>.032)&(np.abs(world[:,1]-p.belly)<.003);i=np.where(mask)[0][np.argmax(d[mask])];point=v[i]
  points.append(point);meshes.append((n,t.faces,v,opened))
 datasets[item]={'probe':p,'product':product,'faces':p.s['faces'],'parts':meshes,'points':np.array(points)}
 metadata={'tool_orientation':p.R.tolist(),'shifts':{n:a['shift_mm'] for n,a in parts.items()},'contact_points':np.array(points).tolist(),'dimensions_xzy_mm':(np.ptp(p.vertices,axis=0)[[0,2,1]]*1000).tolist()}
 row['view']=metadata
(DEST/'viewer-data.json').write_text(json.dumps({'roots':root_specs,'items':{k:v['view'] for k,v in report['products'].items()},'open_shift':-11,'pitch_mm':75},indent=2))
fmt=lambda x:f'{x:.1f}'.replace('.',',')
for mode in ['side','plan']:
 fig,axs=plt.subplots(1,4,figsize=(20,10));fig.patch.set_facecolor('#f5f8fa');fig.subplots_adjust(left=.035,right=.98,top=.75,bottom=.29,wspace=.2)
 fig.text(.035,.947,'DÖRT ÜRÜN / TEK SABİT MONTAJ / İKİ KARŞILIKLI PARMAK ÇİFTİ',fontsize=23,weight='bold',color='#163641')
 fig.text(.035,.90,'Bağlantı eksenleri 75 × 75 mm; çapraz mesafe 106,1 mm. Ürün değişirken kökler ve montaj açıları değişmiyor.',fontsize=13)
 fig.text(.035,.86,'TEMAS NOKTALARINDAN YAN KESİT' if mode=='side' else 'KAVRAMA EKSENİNDEN BAKIŞ / TEMAS HİZASI KESİTİ',fontsize=15,weight='bold')
 for ax,item in zip(axs,['Dough','Cola','Dessert','Box']):
  d=datasets[item];p=d['probe'];points=d['points'];positive=points[points[:,0]>0];cx=float(np.mean(positive[:,0]));cz=float(points[:,2].mean())
  normal=np.array([1,0,0]) if mode=='side' else np.array([0,0,1]);origin=np.array([cx,0,0]) if mode=='side' else np.array([0,0,cz])
  def project(v):return (np.stack([v[...,1],v[...,2]-.073],axis=-1) if mode=='side' else v[...,:2])*1000
  def section(v,f):return trimesh.intersections.mesh_plane(trimesh.Trimesh(v,f,process=False),normal,origin)
  ll=section(d['product'],d['faces'])
  if len(ll):
   for loop in trimesh.load_path(ll).discrete:
    poly=project(loop);ax.fill(poly[:,0],poly[:,1],color='#f1d18a',alpha=.75,zorder=1)
   ax.add_collection(LineCollection(project(ll),colors='#8f7024',linewidths=1.3))
  eq=ConvexHull(d['product']).equations
  for n,f,v,opened in d['parts']:
   for vv,col,ls in [(opened,'#9aa6ae','dashed'),(v,'#006b8c','solid')]:
    lines=section(vv,f);ax.add_collection(LineCollection(project(lines),colors=col,linestyles=ls,linewidths=1.3 if ls=='dashed' else 2,zorder=3))
    if ls=='solid' and item=='Dough':
     inside=(lines.mean(1)@eq[:,:3].T+eq[:,3]).max(1)<-.00005;ax.add_collection(LineCollection(project(lines[inside]),colors='#b75677',linewidths=3,zorder=4))
  dims=report['products'][item]['view']['dimensions_xzy_mm'];ax.set_title(names[item]+'\n'+' × '.join(fmt(x) for x in dims)+' mm',fontsize=13,weight='bold',pad=14)
  ax.set_aspect('equal');ax.set_xlim(-62,62);ax.grid(alpha=.15);ax.set_xticks([-60,-30,0,30,60]);ax.set_xlabel('mm')
  if mode=='side':
   ax.set_ylim(80,-20);ax.set_yticks([0,20,40,60,80]);ax.text(.5,-.16,f'Kesit düzlemi: X = {fmt(cx*1000)} mm',transform=ax.transAxes,ha='center',fontsize=10)
  else:
   ax.set_ylim(-62,62);ax.set_yticks([-60,-30,0,30,60]);ax.scatter(points[:,0]*1000,points[:,1]*1000,c='#188956' if item!='Dough' else '#b75677',s=28,zorder=6)
   ax.text(.5,-.16,'Dört temas noktası' if item!='Dough' else 'Dört yumuşak temas noktası',transform=ax.transAxes,ha='center',fontsize=11)
  if item=='Dough':desc=f'Hamurun şişkin yanları hedeflendi.\nGereken ezilme: en çok {fmt(max(t["closing_max_penetration_mm"] for t in checks[item]["parts"]))} mm'
  else:
   depth=min(t['inside_entry_mm'] for t in report['products'][item]['parts']);clear=-max(t['fixed_penetration_mm'] for t in checks[item]['parts']);desc=f'4 / 4 yan yüzey teması\nKenardan içeride: {fmt(depth)} mm\nOmuz boşluğu: en az {fmt(clear)} mm'
  ax.text(.5,-.25,desc,transform=ax.transAxes,ha='center',va='top',fontsize=11,color='#176b50' if item!='Dough' else '#98435f',linespacing=1.45)
 legend=[Line2D([0],[0],color='#9aa6ae',ls='--',lw=1.5,label='Giriş için açık uç'),Line2D([0],[0],color='#006b8c',lw=2,label='Kavrama konumu'),Line2D([0],[0],color='#b75677',lw=3,label='Hamurda gereken ezilme'),Line2D([0],[0],color='#188956',marker='o',lw=0,label='Geometrik temas')]
 fig.legend(handles=legend,loc='lower left',bbox_to_anchor=(.035,.10),ncol=4,frameon=False,fontsize=11)
 fig.text(.035,.070,'Parmaklar montajda çiftler halinde yönlendirildi. Yalnız tatlı ölçüsü küçültüldü; kola, pide kutusu, hamur ve OEM parmak boyları değişmedi.',fontsize=10.5,color='#415b68')
 fig.text(.035,.043,'Kesitler her ürünün temas konumundan alınmıştır. Kutuda gerçek robot yaklaşımı yataydır; karşılaştırmada takım ekseni aşağı çevrildi.',fontsize=10.5,color='#415b68')
 fig.text(.035,.017,'Bu sonuç geometriye aittir: ayrı esneyen uçlar varsayılmıştır. Ortak basınç, tutma kuvveti ve hamurun malzeme davranışı üreticiyle doğrulanmalıdır.',fontsize=10.5,color='#8c4545')
 fig.savefig(DEST/(mode+'.png'),dpi=180,facecolor=fig.get_facecolor());fig.savefig(DEST/(mode+'.svg'),facecolor=fig.get_facecolor());plt.close(fig)
print('Drawings and neutral OEM GLB exported.')
