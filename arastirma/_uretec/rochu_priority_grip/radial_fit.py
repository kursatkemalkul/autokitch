from radial_probe import *
model,head=setup(); ps={k:Probe(model,head,k) for k in ['Box','Cola']}
def loss(x):
 scores=[]
 for i,p in enumerate(ps.values()):
  a=p.measure(x[:2],x[2+i*2],x[3+i*2]);v=a['parts']
  scores.append(max(abs(t['tip_mm']) for t in v)+20*max(0,max(t['fixed_mm'] for t in v)+.5)+15*max(0,max(t['open_mm'] for t in v)+.5)+15*max(0,max(t['whole_closed_mm'] for t in v)+.1))
 return max(scores)+.1*sum(scores)
sol=differential_evolution(loss,[(17,25),(39,46),(0,8),(-5,5),(0,8),(-5,5)],seed=194,popsize=5,maxiter=45,polish=True,tol=.003)
result={'x':sol.x.tolist(),'loss':float(sol.fun),'products':{k:p.measure(sol.x[:2],sol.x[2+i*2],sol.x[3+i*2],True) for i,(k,p) in enumerate(ps.items())}}
(DEST/'radial-search.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
