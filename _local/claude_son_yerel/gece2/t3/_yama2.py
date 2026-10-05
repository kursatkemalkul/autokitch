s = open('t3_montaj.py', encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:60]
    s = s.replace(a, b)
# arka: burçlar astar arkadan sonra, arkadan
rep("""for a in sorted(a for a in P if a.startswith(('pom_gecis', 'burc_'))): koy(a, AD(ON9), '%s → arka duvara' % P[a]['ac'].split('(')[0].strip(), sure_bekle=0.05)""",
    """for a in sorted(a for a in P if a.startswith('pom_gecis')): koy(a, AD(ON9, ARKA9), '%s → arka duvara' % P[a]['ac'].split('(')[0].strip(), sure_bekle=0.05)""")
rep("""t = koy('pu_levha_arka', AD(ON9), 'PU levha arka (ölçüsünde kesilmiş) → arka dış saca yaslanır')
t = koy('astar_arka', AD(ON9), 'Astar arka 1,0 → levhanın önüne')""",
    """buyu('yapistirici_arka', t, 0.6); olay(t, 'Yapıştırıcı (YEŞİL) → arka dış sacın iç yüzüne'); t += 0.8
t = koy('pu_levha_arka', AD(ON9), 'PU levha arka (ölçüsünde kesilmiş) → yapıştırıcıya bastırılır')
t = koy('astar_arka', AD(ON9), 'Astar arka 1,0 → levhanın önüne')
for a in sorted(a for a in P if a.startswith('burc_')): koy(a, AD(ARKA9, ON9), '%s → arka duvar deliğine' % P[a]['ac'].split('(')[0].strip(), sure_bekle=0.05)
t = bitti() + 0.3""")
rep("""    t = koy(pu, yp, '%s → dış saca yaslanır' % P[pu]['ac'].split('(')[0].strip())""",
    """    yk = 'yapistirici_' + pu.split('_')[-1]; buyu(yk, t, 0.6); olay(t, 'Yapıştırıcı (YEŞİL) → dış sacın iç yüzüne'); t += 0.8
    t = koy(pu, yp, '%s → yapıştırıcıya bastırılır' % P[pu]['ac'].split('(')[0].strip())""")
rep("""olay(t, 'Raf askı burcu POM × 16 → astar + levha deliklerinden içeriden (sıkı geçme)'); t = bitti() + 0.5""",
    """olay(t, 'Raf askı burcu POM × 16 → astar + levha deliklerinden içeriden (sıkı geçme)'); t = bitti() + 0.5
buyu('derz_silikonu', t, 0.8); olay(t, 'Derz silikonu (YEŞİL) → gıda tarafı iç köşeler'); t += 1.0""")
rep("'PU levha sol + astar sol · PU levha sağ + astar sağ · PU levha tavan + astar tavan · iç köşe TIG · POM burç × 16'",
    "'yapıştırıcı · PU levha + astar (sol, sağ, tavan) · iç köşe TIG · POM burç × 16 · derz silikonu'")
open('t3_montaj.py', 'w', encoding='utf-8').write(s)
