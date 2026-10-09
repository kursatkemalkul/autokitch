from probe import *
from scipy.optimize import minimize
model,head=setup();p=Probe(model,head,'Box');out=[]
for r in [26,27,28,29,30]:
 def objective(x):
  a=p.measure(r,*x,full=True,opening=5);v=a['parts']
  return max(abs(t['tip_mm']) for t in v)+200*max(0,max(t['open_mm'] for t in v)+.02)
 sol=minimize(objective,[-25.65,-3.84],method='Nelder-Mead',options={'maxiter':180,'xatol':.00005,'fatol':.0001,'initial_simplex':np.array([[-25.65,-3.84],[-25.85,-3.84],[-25.65,-4.1]])},bounds=[(-29,-23),(-7,0)])
 a=p.measure(r,*sol.x,full=True,opening=5);a['opening']=5;a['loss']=float(sol.fun);out.append(a)
 print(r,'depth',a['depth_mm'],'bend',a['shift_mm'],'entry',max(t['open_mm'] for t in a['parts']),'tips',[t['tip_mm'] for t in a['parts']],flush=True)
 (DEST/'box-precise.json').write_text(json.dumps(out,indent=2))
