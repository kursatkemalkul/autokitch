m=open('b3_montaj.py',encoding='utf-8').read()
i=m.index('# ================================================================== PLAN'); head=m[:i]; plan=m[i:]
head=head.replace("HARIC_PLAN = set()","HARIC_PLAN = set(); HARIC_NEDEN = {}")
head=head.replace("""    P['g_' + ad] = dict(V=V, F=F, m=old['m'], tur='sac', ac=old['ac'], bom=old.get('bom'), model_lo=old['V'].min(0), model_hi=old['V'].max(0))""",
"""    kb = np.array(D0['ENT'][ad]['kutu'])
    P['g_' + ad] = dict(V=V, F=F, m=old['m'], tur='sac', ac=old['ac'], bom=old.get('bom'), model_lo=kb[[0, 2, 4]], model_hi=kb[[1, 3, 5]])""")
old="""for a in ('g_dis_taban_1', 'g_dis_taban_2'): HARIC_PLAN.add(('percin_sase', a))"""
assert old in plan
plan=plan.replace(old, old+"""
for k in range(1, 6):
    for kv in [x for x in P if x.startswith('g_bolme_%d_kovan' % k)]:
        HARIC_PLAN.add(('g_bolme_%d_pu' % k, kv)); HARIC_NEDEN[('g_bolme_%d_pu' % k, kv)] = 'kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)'
for kb_ in ('g_kosebent_sag_ust_2',):
    for pu in ('g_tk_depo_arka_pu', 'g_tk_depo_sag_pu'):
        HARIC_PLAN.add((kb_, pu)); HARIC_NEDEN[(kb_, pu)] = 'MODEL AÇIĞI: PU levha köşebendin büküm dış köşesini ve ön ucunu sarıyor (köpük modeli) — kesilmiş levha olarak takılamaz'
for kb_ in ('g_kosebent_sol_ust_1', 'g_kosebent_sol_ust_2', 'g_kosebent_sol_ust_3'):
    HARIC_PLAN.add((kb_, 'g_pu_sol')); HARIC_NEDEN[(kb_, 'g_pu_sol')] = 'MODEL AÇIĞI: PU sol levha köşebendin büküm dış köşesini sarıyor (köpük modeli) — kesilmiş levha olarak takılamaz'""")
plan=plan.replace("CEKD=CEKD, SAC_AD=list(SAC), HARIC_PLAN=sorted(HARIC_PLAN)),","CEKD=CEKD, SAC_AD=list(SAC), HARIC_PLAN=sorted(HARIC_PLAN), HARIC_NEDEN=HARIC_NEDEN),")
open('b3_montaj.py','w',encoding='utf-8').write(head+plan); open('plan_kod.py','w',encoding='utf-8').write(plan)
p=open('b3_parca.py',encoding='utf-8').read()
p=p.replace("pickle.dump(dict(P=P, CEKD=","pickle.dump(dict(P=P, ENT=ENT, CEKD=")
open('b3_parca.py','w',encoding='utf-8').write(p)
c=open('b3_cikti.py',encoding='utf-8').read()
c=c.replace("for a, b in D['HARIC_PLAN']: har(a, b, 'perçin somun başı sacın boşluk deliğinde (Ø15,5 ↔ Ø15, 0,25 mm boşluk; çokgen yaklaşımı)')",
"for a, b in D['HARIC_PLAN']: har(a, b, D['HARIC_NEDEN'].get((a, b), 'perçin somun başı sacın boşluk deliğinde (Ø15,5 ↔ Ø15, 0,25 mm boşluk; çokgen yaklaşımı)'))")
open('b3_cikti.py','w',encoding='utf-8').write(c)
print('ok')
