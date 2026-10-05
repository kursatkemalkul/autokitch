s=open('plan_kod.py',encoding='utf-8').read()
def rep(a,b):
    global s
    assert a in s, a[:70]; s=s.replace(a,b)
rep("""for a in sorted(x for x in P if x.startswith('b_kanal_') and x != 'b_kanal_988'): yerlestir([a], ['on', 'ust'], t, 'Sütun dikey kablo kanalı → iç arka sac')
""","")
rep("[('on', (40.0, 0.0, 0.0)), ('on', (60.0, 0.0, 0.0)), 'on']","[('on', (4.0, 0.0, 0.0)), ('on', (40.0, 0.0, 0.0)), 'on']")
rep("t = yerlestir(['kablo_klips'], ['on', 'ust'], t, 'Kablo klipsi')\n","""for a in sorted(x for x in P if x.startswith('b_kanal_') and x != 'b_kanal_988'): yerlestir([a], ['on', 'ust'], t, 'Sütun dikey kablo kanalı → iç arka sac (motor rakorlarının yanına)')
t = bitti()
t = yerlestir(['kablo_klips'], ['on', 'ust'], t, 'Kablo klipsi')
""")
rep("adim('B kablo kanalları', 'Arka kablo kanalı parçaları bölme kovanlarından geçirilerek birleştirilir (kanal boyunca uzar); sütun dikey kanalları iç arka saca.', 'B kanal × 5')",
    "adim('B arka kablo kanalı', 'Arka kablo kanalı parçaları bölme kovanlarından geçirilerek birleştirilir (kanal boyunca uzar). Sütun dikey kanalları motorlardan sonra.', 'B arka kanal')")
open('plan_kod.py','w',encoding='utf-8').write(s)
m=open('b3_montaj.py',encoding='utf-8').read(); i=m.index('# ================================================================== PLAN')
open('b3_montaj.py','w',encoding='utf-8').write(m[:i]+s); print('ok')
