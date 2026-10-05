import io
p = 'plan_v4.py'; s = io.open(p, encoding='utf-8').read()
# teknik bölme adımını bölmelerden SONRAYA taşı
a = s.index("KONS_Z = [a for a in P if a.startswith('b_zincir_') and not a.startswith('b_zincir_taban_')]\nTEZGAH_BAG.update(KONS_Z)\nadim('Teknik bölme")
b = s.index("# ---- 6 SOL DUVAR + İÇ ARKA")
blok = s[a:b]
s = s[:a] + s[b:]
blok = blok.replace("""t = yerlestir(['sogutma_grubu'], ['ust', 'on'], t, 'Soğutma grubu (tek ürün) → teknik bölmenin altı, taban rayları zemine', kamera_yakin=True)
t = baglantilari_tamamla(t, 'Soğutma grubu taban rayı uçları: ISO 4762 M4 + pul → şasedeki kapalı uçlu perçin somun / tabanın altında pul + somun (mavi)') + 0.1
t = yerlestir(['elektrik_kutusu'], ['on', ('on', (0.0, 12.0, 0.0)), 'ust'], t, 'B elektrik montaj plakası → dış arka sacın saplamalarına', kamera_yakin=True)""",
"""t = yerlestir(['elektrik_kutusu'], ['on', ('on', (0.0, 12.0, 0.0)), 'ust'], t, 'B elektrik montaj plakası → dış arka sacın saplamalarına', kamera_yakin=True)
t = baglantilari_tamamla(t) + 0.1
t = yerlestir(['sogutma_grubu'], ['on', 'ust', ('on', (0.0, 10.0, 0.0))], t, 'Soğutma grubu (tek ürün) → teknik bölmenin altı, taban rayları zemine', kamera_yakin=True)
t = baglantilari_tamamla(t, 'Soğutma grubu taban rayı uçları: ISO 4762 M4 + pul → şasedeki kapalı uçlu perçin somun / tabanın altında pul + somun (mavi)') + 0.1""")
blok = blok.replace("Teknik bölme boşken: soğutma grubu (kompresör + kondenser + fan, tek ürün) iner, taban raylarının uçları 4 × ISO 4762 M4 + pul ile. Enerji zinciri", "Bölmelerden sonra, sağ yan kapanmadan: B elektrik montaj plakası önden dış arka sacın 6 PEM saplamasına (M5 pul + somun); soğutma grubu (kompresör + kondenser + fan, tek ürün) önden iner, taban raylarının uçları 4 × ISO 4762 M4 + pul ile. Enerji zinciri")
blok = blok.replace(" B elektrik montaj plakası önden dış arka sacın 6 PEM saplamasına, M5 pul + somun.\"", "\"")
k = s.index("adim('Sağ yan sac',")
s = s[:k] + blok + s[k:]
# kanallar: yalnız soldan / önden; artık saplama yok
s = s.replace("""'İç kablo kanalı parçaları sütun sütun önden saplamalarına geçer (taban plakası Ø4,5 delikli); kanal içinden M4 pul + somun. Dar kanalda (güç kablosu) kanal kelepçesi. Zincir kanalı tezgâhta 2 L konsoluna kör perçinlenir, tabandaki saplamalara oturur. Güç ve evaporatör kabloları kanal boyunca çekilir.'""",
              """'İç kablo kanalı parçaları sütun sütun önden yerine; taban plakasından saca DIN 7337 Ø4 (dar yerde Ø3,2) kör perçin, kanalın içinden (mavi; perçin ucu saç arkasındaki PU levhanın cebine açılır). Güç ve evaporatör kabloları kanal boyunca çekilir.'""")
s = s.replace("""     'iç kanal parçası × %d · kelepçe × 2 · zincir kanalı + 2 L konsol · B kablo kanalı · kablolar' % len([a for a in P if a.startswith('ic_kanal_')]))""",
              """     'iç kanal parçası × %d · kör perçin · kablolar' % len([a for a in P if a.startswith('ic_kanal_')]))""")
# GDOKUN: konsol / kelepçe (b_ sac) da dokunulan parça sayılır
s = s.replace("""GDOKUN = {}
for k, L in GRUP.items():
    R = grup_kalan(L)
    if not R: continue
    lo = np.min([LO[a] for a in R], 0) - 0.4; hi = np.max([HI[a] for a in R], 0) + 0.4
    m = np.all(BOX[:, :3] <= hi, 1) & np.all(BOX[:, 3:] >= lo, 1)
    GDOKUN[k] = [YAPI[i] for i in np.where(m)[0]]""",
"""GDOKUN = {}
BSAC = [a for a in BAG if P[a]['etur'] == 'sac']
YAPI2 = YAPI + BSAC; BOX2 = np.array([np.r_[LO[a], HI[a]] for a in YAPI2])
for k, L in GRUP.items():
    R = grup_kalan(L)
    if not R: continue
    lo = np.min([LO[a] for a in R], 0) - 0.4; hi = np.max([HI[a] for a in R], 0) + 0.4
    m = np.all(BOX2[:, :3] <= hi, 1) & np.all(BOX2[:, 3:] >= lo, 1)
    GDOKUN[k] = [YAPI2[i] for i in np.where(m)[0] if YAPI2[i] not in L]""")
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
