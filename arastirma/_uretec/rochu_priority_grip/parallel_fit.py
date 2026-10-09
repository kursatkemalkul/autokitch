from parallel_probe import *
model,head=setup();out={}
for item in ['Box','Cola']:
 p=Probe(model,head,item);out[item]=[]
 for r in [40,42,44,46]:
  def obj(x):
   a=p.measure(r,*x);v=a['parts']
   return max(abs(t['tip_mm']) for t in v)+20*max(0,max(t['fixed_mm'] for t in v)) +20*max(0,max(t['open_mm'] for t in v)+.3)+10*max(0,max(t['whole_closed_mm'] for t in v)-.2)
  sol=differential_evolution(obj,[(-32,10),(-11,5)],seed=93,popsize=8,maxiter=70,polish=True,tol=.005)
  a=p.measure(r,*sol.x,full=True);a['opening']=-11;a['loss']=float(sol.fun);out[item].append(a)
  print(item,r,'depth',round(a['depth_mm'],3),'bend',round(a['shift_mm'],3),'body',round(max(t['fixed_mm'] for t in a['parts']),3),'entry',round(max(t['open_mm'] for t in a['parts']),3),'whole',round(max(t['whole_closed_mm'] for t in a['parts']),3),'tips',[round(t['tip_mm'],3) for t in a['parts']],flush=True)
  (DEST/'parallel-search.json').write_text(json.dumps(out,indent=2))
