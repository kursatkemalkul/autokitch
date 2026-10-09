from experiment import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
model,head=setup();selected=json.loads((DEST/'selected.json').read_text());r=selected['radius_mm'];size=selected['size_mm']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none'})
names={'Dough':'HAMUR','Cola':'KOLA','Dessert':'KÜÇÜK TATLI KUTUSU','Box':'PİDE KUTUSU'}
u=np.array([2**-.5,2**-.5,0]);normal=np.array([-2**-.5,2**-.5,0]);order=['Dough','Cola','Dessert','Box']
def xy(v,mode):return (np.stack([v@u,v[:,:,2]-.073],axis=-1) if v.ndim==3 and mode=='side' else np.stack([v@u,v[:,2]-.073],axis=-1) if mode=='side' else v[...,:2])*1000
def cut(v,f,mode):return trimesh.intersections.mesh_plane(trimesh.Trimesh(v,f,process=False),normal if mode=='side' else [0,0,1],[0,0,0] if mode=='side' else [0,0,.097])
fmt=lambda a:f'{a:.1f}'.replace('.',',')
legend=[Line2D([0],[0],color='#85909a',lw=1.8,ls='--',label='Açık / düz parmak'),Line2D([0],[0],color='#006b95',lw=2,label='Denemedeki parmak'),Line2D([0],[0],color='#ce3041',lw=3,label='Ürün içine giren bölge'),Line2D([0],[0],color='#f4d58a',lw=8,label='Ürün kesiti')]
metrics={}
for mode in ['side','shoulder']:
 fig,axs=plt.subplots(1,4,figsize=(20,10.3 if mode=='side' else 8.2));fig.patch.set_facecolor('#f6f8fa')
 fig.subplots_adjust(left=.04,right=.98,top=.76,bottom=.28 if mode=='side' else .28,wspace=.19)
 fig.text(.04,.95,'KÜÇÜK TATLI KUTUSU / DÖRT ÜRÜN AYNI MONTAJDA',fontsize=23,weight='bold',color='#16303f')
 fig.text(.04,.902,f'Tatlı önerisi: {size} × {size} × 60 mm  |  Karşılıklı bağlantı eksenleri: {2*r:.0f} mm  |  Diğer üç ürün değişmedi',fontsize=14)
 fig.text(.04,.855,'YAN KAVRAMA KESİTLERİ' if mode=='side' else 'OMUZ HİZASINDAKİ KESİT / SARI KESİK: ALTTAKİ ÜRÜN İZDÜŞÜMÜ',fontsize=15,weight='bold')
 for ax,item in zip(axs,order):
  pr=Probe(model,head,item,size if item=='Dessert' else None);a=selected['rows'][item]
  product=(pr.vertices-pr.base-pr.R[:,2]*a['depth_mm']/1000)@pr.R
  eq=ConvexHull(product).equations
  ll=cut(product,pr.s['faces'],mode)
  if len(ll):
   for loop in trimesh.load_path(ll).discrete:
    poly=xy(loop,mode);ax.fill(poly[:,0],poly[:,1],color='#f4d58a',alpha=.75,zorder=1)
   ax.add_collection(LineCollection(xy(ll,mode),colors='#856b27',linewidths=1.4))
  elif mode=='shoulder':
   foot=product[:,:2]*1000;h=ConvexHull(foot);poly=foot[h.vertices];poly=np.vstack([poly,poly[0]])
   ax.plot(poly[:,0],poly[:,1],color='#b58a30',lw=1.4,ls='--')
   ax.text(0,0,'Ürün bu kesitin\naltında kalıyor',ha='center',va='center',fontsize=10,color='#80601c')
  for n in head.graph.nodes_geometry:
   if not n.startswith('OEM_DAC_'):continue
   w,g=head.graph[n];w=w.copy();w[:2,3]*=r/50;t=head.geometry[g]
   if mode=='side' and abs(w[:3,3]@normal)>.0001:continue
   for shift,color,ls in [(0,'#85909a','dashed'),(a['shift_mm'],'#006b95','solid')]:
    v=deform(t.vertices,shift)@w[:3,:3].T+w[:3,3];segments=cut(v,t.faces,mode)
    ax.add_collection(LineCollection(xy(segments,mode),colors=color,linewidths=1.4 if shift==0 else 2,linestyles=ls,zorder=3))
    if shift!=0:
     inside=(segments.mean(1)@eq[:,:3].T+eq[:,3]).max(1)<-.00005
     ax.add_collection(LineCollection(xy(segments[inside],mode),colors='#ce3041',linewidths=3,zorder=4))
   if mode=='side':
    x=w[:3,3]@u*1000;ax.plot([x,x],[-14,-6],color='#68717a',lw=3)
  d=np.ptp(pr.vertices,axis=0)*1000
  ax.set_title(names[item]+'\n'+f'{fmt(d[0])} × {fmt(d[2])} × {fmt(d[1])} mm',weight='bold',fontsize=13,pad=14)
  ax.set_xlim(-65,65);ax.set_aspect('equal');ax.grid(alpha=.16);ax.set_xticks([-60,-30,0,30,60]);ax.axvline(0,color='#bbc5cd',ls='-.',lw=.7);ax.set_xlabel('mm')
  if mode=='side':
   ax.set_ylim(100,-30);ax.set_yticks([0,25,50,75,100]);ax.plot([-r,r],[-14,-14],color='#b07e3e',lw=4)
   ax.annotate('',xy=(r,-23),xytext=(-r,-23),arrowprops={'arrowstyle':'<->','lw':1});ax.text(0,-25,f'{2*r:.0f} mm',ha='center',va='bottom',fontsize=10)
  else:ax.set_ylim(-65,65);ax.set_yticks([-60,-30,0,30,60]);ax.axhline(0,color='#bbc5cd',ls='-.',lw=.7)
  fixed=max(x['fixed_mm'] for x in a['parts']);tip=[x['tip_mm'] for x in a['parts']];opening=max(x['open_mm'] for x in a['parts'])
  gap=max(0,-min(tip));over=max(0,max(tip));text=f'Omuz girişi: {fmt(max(0,fixed))} mm\nUç boşluğu: en çok {fmt(gap)} mm\nUç iç içe geçmesi: en çok {fmt(over)} mm'
  if mode=='side':ax.text(.5,-.19,text,transform=ax.transAxes,ha='center',va='top',fontsize=11,linespacing=1.5,color='#a82e3b' if max(fixed,gap,over)>.7 else '#006b95')
  metrics[item]={'dimensions_xzy_mm':d[[0,2,1]].tolist(),'fixed_intrusion_mm':max(0,fixed),'max_tip_gap_mm':gap,'max_tip_overlap_mm':over,'open_max_overlap_mm':max(0,opening),'shift_mm':a['shift_mm'],'entry_depth_delta_mm':a['depth_mm']}
 fig.legend(handles=legend,loc='lower left',bbox_to_anchor=(.04,.105),frameon=False,ncol=4,fontsize=11)
 fig.text(.04,.072,'Karşılaştırma denemesi; dört üründe başarılı kavrama sağlanmadı. Tatlı küçültüldü; OEM parmaklar ölçeklenmedi.',fontsize=12,color='#943442')
 fig.text(.04,.046,'Yan çizim karşılıklı parmak çiftinin çapraz kesiti; kutunun yatay giriş yönü aşağı çevrildi. Uzun ürünlerin alt devamı kadraj dışında.',fontsize=10,color='#485c68')
 fig.text(.04,.022,'Kırmızı kesitler geometrik girişleri gösterir. Ölçümler yaklaşık dış yüzey hesabıdır; esneme, tutma kuvveti ve fiziksel çarpışma onayı değildir.',fontsize=10,color='#485c68')
 fig.savefig(DEST/(mode+'.png'),dpi=180,facecolor=fig.get_facecolor());fig.savefig(DEST/(mode+'.svg'),facecolor=fig.get_facecolor());plt.close(fig)
(DEST/'drawing-measures.json').write_text(json.dumps({'mount_axes_mm':2*r,'dessert_footprint_mm':size,'items':metrics,'note':'Same mount and same unscaled OEM for all four; item-specific insertion and illustrative tip command. No successful all-product grasp.'},indent=2))
print(json.dumps(metrics,indent=2))
