from probe import *
model,head=setup();results={}
for item in ['Cola','Box']:
 p=Probe(model,head,item)
 results[item]=[]
 for r in [28,30,32,34,36]:
  def obj(x):
   a=p.measure(r,x[0],x[1],opening=x[2]);v=a['parts']
   # Hard-product contact and clear entry: shoulder interference costs more.
   return max(abs(t['tip_mm']) for t in v)+10*max(0,max(t['fixed_mm'] for t in v)) + 5*max(0,max(t['open_mm'] for t in v)+.2)
  sol=differential_evolution(obj,[(-40,10),(-11,0),(0,5)],seed=37,popsize=8,maxiter=80,polish=True,tol=.005)
  a=p.measure(r,*sol.x[:2],full=True,opening=sol.x[2]);a['opening']=float(sol.x[2]);a['coarse_loss']=float(sol.fun)
  results[item].append(a)
  print(item,r,'depth',round(a['depth_mm'],2),'bend',round(a['shift_mm'],2),'open',round(a['opening'],2),'body',round(max(t['fixed_mm'] for t in a['parts']),3),'entry',round(max(t['open_mm'] for t in a['parts']),3),'tips',[round(t['tip_mm'],3) for t in a['parts']],flush=True)
  (DEST/'priority-search.json').write_text(json.dumps(results,indent=2))
