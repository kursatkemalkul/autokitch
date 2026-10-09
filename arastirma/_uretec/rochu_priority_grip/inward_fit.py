from inward_probe import *
model,head=setup();results={}
for item in ['Cola','Box']:
 p=Probe(model,head,item);results[item]=[]
 for r in [38,40,42,44,46]:
  def obj(x):
   a=p.measure(r,*x);v=a['parts']
   return max(abs(t['tip_mm']) for t in v)+10*max(0,max(t['fixed_mm'] for t in v)) +5*max(0,max(t['open_mm'] for t in v)+.3)
  sol=differential_evolution(obj,[(-35,10),(-11,5)],seed=47,popsize=8,maxiter=80,polish=True,tol=.005)
  a=p.measure(r,*sol.x,full=True);a['opening']=-11;a['coarse_loss']=float(sol.fun);results[item].append(a)
  print(item,r,'depth',round(a['depth_mm'],3),'bend',round(a['shift_mm'],3),'body',round(max(t['fixed_mm'] for t in a['parts']),3),'entry',round(max(t['open_mm'] for t in a['parts']),3),'tips',[round(t['tip_mm'],3) for t in a['parts']],flush=True)
  (DEST/'inward-search.json').write_text(json.dumps(results,indent=2))
