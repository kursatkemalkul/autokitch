import re
s = open('g6_montaj.py', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:70])
    s = s.replace(a, b)


rep("""        _mm = (_m ^ _kutu(_l, _h)).to_mesh()""", """        _mm = (_m ^ _kutu(_l, _h) ^ _kutu([1.4561, 1.1106, -0.6284], [2.4799, 2.1799, 0.0379])).to_mesh()""")
rep("""    olay(t, 'Astar 1,0 — 4 düz sac (arka, sol, sağ, tavan) · TIG + R3 iç köşe')
    t = gel(R(r'^astar_arka$'), (0, 0, 0.8), t, 1.0)
    t = gel(R(r'^astar_(sol|sag)$'), (0, 0, 0.8), t, 0.9, 0.2)
    t = gel(R(r'^astar_tavan$'), (0, 0, 0.8), t, 0.9) + 0.1
    olay(t, 'Raf 3,0 (iki büküm) + köşebentler · düşme kovanları (kıyma / kuşbaşı 3,0 sac · sos / harç boru · kaşar / sucuk POM-C)')
    kam(t, R(r'^(raf|dusme_kovani|dil_kanali|soguk_esik)'), (0, 0.4, 1))
    t = gel(R(r'^raf_kosebendi_(sol|sag)$'), (0, 0, 0.6), t, 0.7, 0.15)
    t = gel(R(r'^raf$'), (0, 0, 0.8), t, 1.0)""",
"""    # Kemal 4 Eki: yalıtım yüzey yüzey ayrı kesilmiş levha olarak gelir, her levhanın üstüne iç sac (astar) kapanır
    t = yalitim_astar(t, 'pu_levha_arka', 'astar_arka', 'Yalıtım levhası ARKA (PU, ölçüsünde kesilmiş) — kanal kovanlarının üstünden önden geçer, arka dış saca yaslanır',
                      'Astar arka 1,0 — levhanın önüne; alt kenarı alt saca oturur · alt köşe TIG punta')
    olay(t, "Sol levhadan önce: A tarafındaki PEM'lere PE köpük kapağı")
    t = yerinde(R(r'_kopuk_kapagi$'), t, 0.4, 0.1) + 0.2
    t = yalitim_astar(t, 'pu_levha_sol', 'astar_sol', 'Yalıtım levhası SOL — sol dış yan sacın iç yüzüne',
                      'Astar sol 1,0 — arka astara ve alt saca dayanır · iç köşe TIG punta (R3)')
    t = yalitim_astar(t, 'pu_levha_sag', 'astar_sag', 'Yalıtım levhası SAĞ — sağ dış yan sacın iç yüzüne',
                      'Astar sağ 1,0 — arka astara ve alt saca dayanır · iç köşe TIG punta (R3)')
    t = yalitim_astar(t, 'pu_levha_tavan', 'astar_tavan', 'Yalıtım levhası TAVAN — yan levhaların arasına, dış tavana yaslanır',
                      'Astar tavan 1,0 — sol / sağ / arka astarın üst kenarına oturur · köşeler TIG punta + taşlama')
    olay(t, 'Raf 3,0 (iki büküm) + köşebentler · düşme kovanları (kıyma / kuşbaşı 3,0 sac · sos / harç boru · kaşar / sucuk POM-C)')
    kam(t, R(r'^(raf|dusme_kovani|dil_kanali|soguk_esik)'), (0, 0.4, 1))
    t = gel(R(r'^raf_kosebendi_(sol|sag)$'), (0, 0, 0.6), t, 0.7, 0.15)
    olay(t, 'Yalıtım levhası TABAN — raf çift cidarının içine, alt sacın üstüne')
    t = gel(['pu_levha_taban'], (0, 0, 0.8), t, 1.0) + 0.1
    olay(t, 'Raf 3,0 levhanın üstüne — büküm kenarları köşebentlere oturur · arka köşe dolgu kaynağı')
    t = gel(R(r'^raf$'), (0, 0, 0.8), t, 1.0)""")
i = s.index("    # 7 PU\n"); j = s.index("    # 8 arka servis sacı alt montajı")
s = s[:i] + s[j:]
rep("""    adim(6, 'Soğuk oda · astar, raflar, eşik, kovanlar, ön çerçeve', t6, t,
         "Soğuk oda iç kabuğu dış kabuğun içine kurulur: alt sac, arka dış sac, 4 düz astar sacı.""",
"""    adim(6, 'Soğuk oda · yalıtım levhaları + astar, raflar, eşik, kovanlar, ön çerçeve', t6, t,
         "Soğuk oda iç kabuğu dış kabuğun içine kurulur: alt sac, arka dış sac, sonra YÜZEY YÜZEY: ölçüsünde kesilmiş PU yalıtım levhası (sarı) yerine konur, üstüne o yüzün astar sacı kapanır (arka → sol → sağ → tavan → taban/raf); her sac komşu sacın flanşına oturur ve TIG puntayla bağlanır.""")
rep("""'alt sac · arka dış sac · 4 kanal kovanı · astar 4 sac ·""", """'alt sac · arka dış sac · 4 kanal kovanı · 5 PU levha (arka, sol, sağ, tavan, taban) · astar 4 sac ·""")
rep("""    # 8 arka servis sacı alt montajı (tezgâhta, arkada)""", """    # 7 arka servis sacı alt montajı (tezgâhta, arkada)""")
rep("""    adim(8, 'Arka servis sacı · alt montaj', t8, t,""", """    adim(7, 'Arka servis sacı · alt montaj', t8, t,""")
rep("""    t = sac_tamam(t)
    no = 9
    # 9 soğutma""", """    t = sac_tamam(t)
    no = 8
    # 8 soğutma""")
# yardımcı: levha + astar
rep("""def seq_TOPPING():""", '''def yalitim_astar(t, pu, astar, m_pu, m_astar):
    kam(t, [pu, astar], (0, 0.3, 1))
    olay(t, m_pu)
    t = gel([pu], (0, 0, 0.8), t, 1.0) + 0.15
    olay(t, m_astar)
    t = gel([astar], (0, 0, 0.8), t, 1.0) + 0.5
    return t


def seq_TOPPING():''')
# UNO: servis sacı kapanmadan önce, arkadan
i = s.index("    # 13 servis sacı kapanır\n"); j = s.index("    # 14 UNO\n"); k = s.index("    # 15 kasetler\n")
servis = s[i:j]; uno = s[j:k]
uno = uno.replace("olay(t, 'UNO · %s: hazne + piston + valf önden, raf burcuna · gıda hortumu + yayıcı' % ad)",
                  "olay(t, 'UNO · %s: servis ağzı açıkken hazne + piston + valf arkadan, raf burcuna · gıda hortumu + yayıcı' % ad)")
uno = uno.replace("kam(t, g, (0, 0.2, 1))\n        t = gel(gv, (0, 0, 0.8), t, 1.2) + 0.1", "kam(t, g, (0, 0.2, -1))\n        t = gel(gv, (0, 0, -0.8), t, 1.2) + 0.1")
uno = uno.replace('"Dört dozaj ünitesi (kıyma, kuşbaşı, sos, harç) soğuk odaya önden girer, raf burçlarına oturur;',
                  '"Arka servis sacı henüz takılı değilken dört dozaj ünitesi (kıyma, kuşbaşı, sos, harç) arkadaki servis ağzından girer, raf burçlarına oturur;')
s = s[:i] + uno.replace('# 14 UNO', '# 13 UNO (servis ağzı açıkken)') + servis.replace('# 13 servis', '# 14 servis') + s[k:]
open('g6_montaj.py', 'w', encoding='utf8').write(s)
print('ok')
