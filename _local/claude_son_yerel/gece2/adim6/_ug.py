s=open('g6_montaj.py',encoding='utf-8').read()
k="    t6 = t\n    for b, ad in (('f', 'U_F (F üstü, ana pano bölmesi)')"
assert k in s
s=s.replace(k,"    t6 = t\n    GHOST_T.append(round(t, 2))\n    GHOST.extend([[2.5, 4.4, 0.106, 0.788, -0.83, 0.039], [4.0, 4.4, 0.788, 1.862, -0.83, 0.079], [4.4, 5.23, 0.0, 1.862, -0.83, 0.079]])\n    olay(t, 'U_F ve U_KE sahada F üst kabini, K ve E üstüne kurulur (B, K, E silik)')\n    for b, ad in (('f', 'U_F (F üstü, ana pano bölmesi)')",1)
open('g6_montaj.py','w',encoding='utf-8').write(s)
