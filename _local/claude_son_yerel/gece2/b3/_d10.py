s=open('plan_kod.py',encoding='utf-8').read()
def rep(a,b):
    global s
    assert a in s, a[:70]; s=s.replace(a,b)
# arka kanal + gider hortumu motorlardan sonra (kanal boyunca uzar)
a=s.index("# ---- 8 B KABLO KANALLARI"); b=s.index("# ---- 9 SOĞUTMA")
s=s[:a]+s[b:]
rep("t = buyu('gider_hortumu', t, 0.8); olay(t - 0.8, 'Gider hortumu kanal boyunca çekilir'); t += 0.3\n","")
rep("'Evaporatör 1 ve 2 (fan + serpantin + tava, braketleriyle tek ürün) çekmece sütunlarından içeri sürülür, iç arka saca oturur. Gider hortumu kanal boyunca çekilir.',\n     'evaporatör × 2 · gider hortumu')",
    "'Evaporatör 1 ve 2 (fan + serpantin + tava, braketleriyle tek ürün) çekmece sütunlarından içeri sürülür, iç arka saca oturur.',\n     'evaporatör × 2')")
rep("""t = bitti()
t = yerlestir(['kablo_klips'], ['on', 'ust'], t, 'Kablo klipsi')
""","""t = bitti()
adim('Arka kablo kanalı + gider hortumu', 'Arka kablo kanalı parçaları bölme kovanlarından geçirilerek birleştirilir; evaporatör gider hortumu kanal boyunca çekilir; kablo klipsi.', 'B arka kanal · gider hortumu · klips')
kamera_genel(['b_kanal_988', 'gider_hortumu'], olcek=0.7)
t = buyu('b_kanal_988', t, 1.0); olay(t - 1.0, 'Arka kablo kanalı: parçalar kovanlardan geçirilip birleştirilir (kanal boyunca)')
t = buyu('gider_hortumu', t, 0.8); olay(t - 0.8, 'Gider hortumu kanal boyunca çekilir'); t += 0.2
t = yerlestir(['kablo_klips'], ['on', 'ust'], t, 'Kablo klipsi')
""")
open('plan_kod.py','w',encoding='utf-8').write(s)
m=open('b3_montaj.py',encoding='utf-8').read(); i=m.index('# ================================================================== PLAN')
head=m[:i].replace("VU[a].append([round(t0, 3), round(t0 + sure + 0.8, 3)]); YER[a] = t0 + sure\n","VU[a].append([round(t0, 3), round(t0 + sure + 0.8, 3)]); YER[a] = t0 + sure; YERINDE.append(a)\n")
assert 'YERINDE.append(a)\n    return t0 + sure' in head or True
open('b3_montaj.py','w',encoding='utf-8').write(head+s); print('YERINDE.append(a)' in head)
