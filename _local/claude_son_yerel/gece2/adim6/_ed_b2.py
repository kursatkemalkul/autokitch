s = open('g6_montaj.py', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)


# iskelet boruları sadeleştirilmez (31 × 31 geçişlerdeki 0,5 mm boşluk korunur)
rep("""    hedef = n if n <= 600 else min(int(600 + 0.25 * (n - 600)), int(3500 + 0.05 * n))
    V, F = sadele(V, F, hedef)""", """    hedef = n if n <= 600 else min(int(600 + 0.25 * (n - 600)), int(3500 + 0.05 * n))
    if not g['dugum'].startswith(('B_MODULER', 'B_TASIYICI')): V, F = sadele(V, F, hedef)""")
# ısı kalkanı üst kirişlerden ÖNCE
blok_kiris = """    olay(t, 'Üst kirişler + üst GFRP pedler dikme başlarına — yukarıdan, TIG kaynak (K ve A bu kirişlere oturur)')
    kam(t, ['M__B_MODULER__paslanmaz__2_kiris', 'M__B_TASIYICI__celik__2_kiris'], (0, 1, 0.4))
    t = gel(['M__B_MODULER__paslanmaz__2_kiris'], (0, 0.4, 0), t, 1.2) + 0.1
    t = gel(['M__B_TASIYICI__celik__2_kiris'], (0, 0.4, 0), t, 1.2) + 0.1
    t = gel(['M__B_MODULER__gfrp__2_ust'], (0, 0.2, 0), t, 0.8) + 0.3
"""
blok_isi = """    olay(t, 'Isı kalkanı (fırın altı): U sac + ışınım sacı + 12 PTFE / cam elyaf takoz')
    kam(t, R(r'^isi_kalkani'), (0, 0.4, 1))
    t = gel(R(r'^isi_kalkani_takozu'), (0, 0.15, 0), t, 0.5, 0.04)
    t = gel(R(r'^isi_kalkani_(u|isinim)'), (0, 0, 0.9), t, 1.2, 0.2) + 0.1
"""
rep(blok_kiris + blok_isi, blok_isi.replace("12 PTFE / cam elyaf takoz'", "12 PTFE / cam elyaf takoz — üst kirişlerden önce'") + blok_kiris)
# ön çerçeve: raylardan sonra, çekmecelerden önce (raylar ve mekanizmalar çerçevenin arkasında kalır)
i = s.index("    t8 = t\n    olay(t, 'Ön çerçeve 2 parça (430) önden"); j = s.index("    t = sac_tamam(t)\n    rest = R(r'^M__')")
cer = s[i:j]; s = s[:i] + s[j:]
cer = cer.replace("    t8 = t\n", "    t0 = t\n").replace("adim(8, 'Ön çerçeve', t8, t,", "adim(no, 'Ön çerçeve', t0, t,").replace(
    "\"Kalıptan çıkan gövdeye ön çerçeve takılır;", "\"Raylar ve mekanizmalar takıldıktan sonra ön çerçeve takılır (çerçeve dudağı rayların önünü örter — önce takılırsa ray / mekanizma giremez);")
cer = cer.rstrip('\n') + "; no += 1\n"
rep("    no = 9\n    t, no = diger(t, no, [a for a in rest if not a.startswith('M__CEK_') and sinif(a) == 'mek'],", "    no = 8\n    t, no = diger(t, no, [a for a in rest if not a.startswith('M__CEK_') and sinif(a) == 'mek'],")
rep("""         '42 sabit ray · 126 × M5 × 10 havşa başlı'); no += 1
""", """         '42 sabit ray · 126 × M5 × 10 havşa başlı'); no += 1
""" + cer)
# ürün: çekmece açılır → ürün yukarıdan konur → çekmece kapanır
rep("""    t, no = diger(t, no, R(r'^M__'), '')
    olay(t, 'B tamam'); kam(t, None); t += 2.0
    for a in R(r'^arayuz_'): GIZLI.add(a)""", """    urun = [a for a in R(r'^M__') if P[a]['m'] == 'urun']
    t, no = diger(t, no, [a for a in R(r'^M__') if a not in urun], '')
    if urun:
        t0 = t; olay(t, 'Ürün yükleme (görsel): her çekmece öne açılır, ürün yukarıdan konur, çekmece kapanır')
        cek = {}
        for a in GOR:
            if a.startswith('M__CEK_') and a not in raylar and a not in GIZLI: cek.setdefault(ANA_BILGI[a]['dugum'].split('__')[0], []).append(a)
        ug = {}
        for a in urun: ug.setdefault(ANA_BILGI[a]['dugum'].split('__')[0], []).append(a)
        AC = 0.62
        for k in sorted(ug, key=lambda k: (bbox(ug[k])[0][0], -bbox(ug[k])[0][1])):
            gov = sorted(cek.get(k, []))
            kam(t, ug[k], (0, 0.6, 1))
            ofset(gov, (0, 0, -AC), t, t + 0.8)            # öne açıl (Σ: -AC + AC = 0 → AC)
            for a in sorted(ug[k]):
                bekle(a); GOR[a] = round(t + 0.85, 3)
                _h(a, t, t + 0.8, (0, 0, -AC)); _h(a, t + 0.85, t + 1.45, (0, 0.3, 0)); _h(a, t + 1.6, t + 2.4, (0, 0, AC))
            ofset(gov, (0, 0, AC), t + 1.6, t + 2.4)       # kapan
            KILITLI.update(gov + ug[k])
            t += 2.6
        adim(no, 'Ürün yükleme', t0, t + 0.3, "Devreye alma testi için ürün: çekmece raylarında öne açılır, ürün tepsiye yukarıdan konur, çekmece kapanır (kapalı dolaba ürün girmez).",
             '%d çekmeceye ürün (görsel)' % len(ug)); t += 0.3; no += 1
    olay(t, 'B tamam'); kam(t, None); t += 2.0
    for a in R(r'^arayuz_'): GIZLI.add(a)""")
open('g6_montaj.py', 'w', encoding='utf8').write(s); print('ok')
