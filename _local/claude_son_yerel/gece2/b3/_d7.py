m=open('b3_montaj.py',encoding='utf-8').read()
i=m.index('# ================================================================== PLAN'); head=m[:i]; plan=m[i:]
old="""for kb_ in ('g_kosebent_sol_ust_1', 'g_kosebent_sol_ust_2', 'g_kosebent_sol_ust_3'):"""
assert old in plan
add="""N_PU = 'MODEL AÇIĞI: PU (köpük modelinden kesilmiş levha) sac flanşının / köşebendin altına sarıyor — levha olarak takılamaz, levha bölümü yeniden kesilmeli'
for pu, L in (('g_pu_arka_yuksek', ('g_dis_arka_1', 'g_dis_arka_ek_lamasi', 'g_dis_arka_2')), ('g_pu_arka_alcak', ('g_dis_arka_2',)),
              ('g_pu_sol', ('g_kosebent_sol_alt_1', 'g_kosebent_sol_alt_2', 'g_kosebent_sol_alt_3', 'g_dis_arka_1', 'g_dis_sol_yan'))):
    for x in L: HARIC_PLAN.add((pu, x)); HARIC_NEDEN[(pu, x)] = N_PU
"""
plan=plan.replace(old, add+old)
plan=plan.replace("t = yerlestir(['g_ic_sol_duvar'], ['ust', 'on'], t,","t = yerlestir(['g_ic_sol_duvar'], [('on', (60.0, 0.0, 0.0)), 'ust', 'on'], t,")
open('b3_montaj.py','w',encoding='utf-8').write(head+plan); open('plan_kod.py','w',encoding='utf-8').write(plan)
print('ok')
