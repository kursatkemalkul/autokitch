from experiment import *
from scipy.optimize import minimize_scalar
model,head=setup();a=json.loads((DEST/'selected.json').read_text())
for item in ['Dough','Cola','Dessert','Box']:
 p=Probe(model,head,item,a['size_mm'] if item=='Dessert' else None)
 def objective(x):
  m=p.measure(a['radius_mm'],*x)
  return p.score(m)+.15*sum(max(0,v['fixed_mm']) for v in m['parts'])+.01*sum(abs(v['tip_mm']) for v in m['parts'])
 rr=differential_evolution(objective,[(-30,20),(-11,0)],seed=53,popsize=8,maxiter=70,tol=.005,polish=True)
 depth,shift=rr.x
 # Correct the selected bend against all OEM vertices/triangle centres.
 f=lambda sh:p.score(p.measure(a['radius_mm'],depth,sh,True))
 refined=minimize_scalar(f,bounds=(-11,0),method='bounded',options={'xatol':.001})
 options=[p.measure(a['radius_mm'],depth,s,True) for s in [shift,refined.x,-11]]
 chosen=min(options,key=p.score);chosen['residual_mm']=p.score(chosen);a['rows'][item]=chosen
 print(item,'depth',chosen['depth_mm'],'shift',chosen['shift_mm'],'fixed',max(v['fixed_mm'] for v in chosen['parts']),'tip',[v['tip_mm'] for v in chosen['parts']],flush=True)
a['residual_mm']=max(v['residual_mm'] for v in a['rows'].values());a['refinement']='Same chosen mounting; secondary penalty avoids unnecessary fixed-body overlap; full-sample tip refinement.'
(DEST/'selected.json').write_text(json.dumps(a,indent=2))
