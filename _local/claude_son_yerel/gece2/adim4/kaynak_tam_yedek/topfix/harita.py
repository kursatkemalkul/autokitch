import json,sys,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
d=json.load(open(sys.argv[1]+'/m8_parca.json',encoding='utf-8')); M=d['MEK']
fig,ax=plt.subplots(figsize=(22,16))
col={7:'gray',9:'red',10:'red',11:'orange',12:'orange',13:'purple',14:'purple',15:'black',16:'blue',17:'cyan'}
for p in d['parca']:
    lo,hi=p['lo'],p['hi']
    if not(hi[2]<-629 and lo[2]>-829 and hi[0]>1437 and lo[0]<2499 and hi[1]>1100 and lo[1]<2199): continue
    if hi[0]-lo[0]>900 and hi[1]-lo[1]>900: continue
    c=col.get(p['mek'],'green')
    ax.add_patch(Rectangle((lo[0],lo[1]),hi[0]-lo[0],hi[1]-lo[1],fill=False,ec=c,lw=0.8))
    if (hi[0]-lo[0])*(hi[1]-lo[1])>800: ax.text(lo[0]+1,lo[1]+1,'%s z%.0f..%.0f'%(p['ad'].split('__')[-1][:8],lo[2],hi[2]),fontsize=5,color=c)
ax.set_xlim(1430,2505); ax.set_ylim(1090,2205); ax.set_aspect('equal'); ax.grid(True,lw=0.3); ax.set_xticks(range(1440,2501,20),minor=True)
plt.savefig(sys.argv[2],dpi=110,bbox_inches='tight')
