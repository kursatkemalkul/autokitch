"""Preflight current K precedence without running placement or model export."""
from pathlib import Path
import sys,json,os
HERE=Path(__file__).resolve().parent
text=(HERE/'k_montaj.py').read_text(encoding='utf-8').split('ordered=[];cycle_breaks=[]')[0]
ns={'__file__':str(HERE/'k_montaj.py'),'__name__':'order_preflight'};exec(compile(text,str(HERE/'k_montaj.py'),'exec'),ns)
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
items=ns['items'];ids={a:i for i,a in enumerate(items)};edges=ns['edges']
g=csr_matrix(([1]*len(edges),([ids[a] for a,b in edges],[ids[b] for a,b in edges])),shape=(len(items),len(items)))
n,labels=connected_components(g,directed=True,connection='strong')
cycles=[[a for a in items if labels[ids[a]]==i] for i in range(n) if sum(labels==i)>1]
(HERE/'precedence_preflight_audit.json').write_text(json.dumps({'parts':len(items),'edges':len(edges),'cycles':cycles,'passed':not cycles,'production_release':False},indent=2),encoding='utf-8')
print('PREFLIGHT_CYCLES',cycles,flush=True);os._exit(0 if not cycles else 2)
