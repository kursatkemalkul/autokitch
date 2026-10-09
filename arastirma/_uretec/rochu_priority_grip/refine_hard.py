from probe import *
from scipy.optimize import minimize
model,head=setup();prior=json.loads((DEST/'priority-search.json').read_text());out={}
for item in ['Box','Cola']:
 p=Probe(model,head,item);out[item]=[]
 for r in [26,27,28,29]:
  base=prior[item][0];opening=5.
  def obj(x):
   a=p.measure(r,*x,full=True,opening=opening);v=a['parts']
   return max(abs(t['tip_mm']) for t in v)+100*max(0,max(t['fixed_mm'] for t in v)) +100*max(0,max(t['open_mm'] for t in v)+.05)
  sol=minimize(obj,[base['depth_mm'],base['shift_mm']],method='Powell',bounds=[(-35,-5),(-11,0)],options={'maxiter':15,'xtol':.0001,'ftol':.0001})
  a=p.measure(r,*sol.x,full=True,opening=opening);a['opening']=opening;a['loss']=float(sol.fun)
  out[item].append(a);print(item,r,'depth',round(a['depth_mm'],4),'bend',round(a['shift_mm'],4),'entry',round(max(t['open_mm'] for t in a['parts']),4),'tips',[round(t['tip_mm'],4) for t in a['parts']],flush=True)
  (DEST/'hard-refined.json').write_text(json.dumps(out,indent=2))
