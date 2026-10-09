from inward_probe import *
model,head=setup();out={}
for item in ['Box','Cola']:
 p=Probe(model,head,item);out[item]=[]
 for r in [46,48,50,52]:
  def obj(x):
   a=p.measure(r,*x);v=a['parts']
   return max(abs(t['tip_mm']) for t in v)+20*max(0,max(t['fixed_mm'] for t in v)) +20*max(0,max(t['open_mm'] for t in v)+.2)+20*max(0,max(t['whole_closed_mm'] for t in v)-.05)
  sol=differential_evolution(obj,[(-32,5),(-11,5)],seed=72,popsize=10,maxiter=100,polish=True,tol=.004)
  a=p.measure(r,*sol.x,full=True);a['opening']=-11;a['coarse_loss']=float(sol.fun);out[item].append(a)
  print(item,r,'depth',round(a['depth_mm'],3),'bend',round(a['shift_mm'],3),'body',round(max(t['fixed_mm'] for t in a['parts']),3),'entry',round(max(t['open_mm'] for t in a['parts']),3),'whole',round(max(t['whole_closed_mm'] for t in a['parts']),3),'tips',[round(t['tip_mm'],3) for t in a['parts']],flush=True)
  (DEST/'strict-search.json').write_text(json.dumps(out,indent=2))
