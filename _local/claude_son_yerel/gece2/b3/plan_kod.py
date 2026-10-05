# ================================================================== PLAN (plan_B.md v2 sırası)
for a in ('g_dis_taban_1', 'g_dis_taban_2'): HARIC_PLAN.add(('percin_sase', a))
for k in range(1, 6):
    for kv in [x for x in P if x.startswith('g_bolme_%d_kovan' % k)]:
        HARIC_PLAN.add(('g_bolme_%d_pu' % k, kv)); HARIC_NEDEN[('g_bolme_%d_pu' % k, kv)] = 'kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)'
for kb_ in ('g_kosebent_sag_ust_2',):
    for pu in ('g_tk_depo_arka_pu', 'g_tk_depo_sag_pu'):
        HARIC_PLAN.add((kb_, pu)); HARIC_NEDEN[(kb_, pu)] = 'MODEL AÇIĞI: PU levha köşebendin büküm dış köşesini ve ön ucunu sarıyor (köpük modeli) — kesilmiş levha olarak takılamaz'
N_PU = 'MODEL AÇIĞI: PU (köpük modelinden kesilmiş levha) sac flanşının / köşebendin altına sarıyor — levha olarak takılamaz, levha bölümü yeniden kesilmeli'
for pu, L in (('g_pu_arka_yuksek', ('g_dis_arka_1', 'g_dis_arka_ek_lamasi', 'g_dis_arka_2')), ('g_pu_arka_alcak', ('g_dis_arka_2',)),
              ('g_pu_sol', ('g_kosebent_sol_alt_1', 'g_kosebent_sol_alt_2', 'g_kosebent_sol_alt_3', 'g_dis_arka_1', 'g_dis_sol_yan'))):
    for x in L: HARIC_PLAN.add((pu, x)); HARIC_NEDEN[(pu, x)] = N_PU
for k in range(1, 6):
    for yan in ('a', 'b'):
        HARIC_PLAN.add(('g_bolme_%d_pu' % k, 'kapak_bolme_%d_sac_%s' % (k, yan))); HARIC_NEDEN[('g_bolme_%d_pu' % k, 'kapak_bolme_%d_sac_%s' % (k, yan))] = 'köpük kapağı PU levhadaki cebine oturur (son 1 mm, model teması)'
for a_, L_ in (('percin_sase', ('sase_boy_arka', 'sase_boy_on')), ('percin_ust', ('moduler_cerceve_arka', 'moduler_cerceve_on', 'tasiyici_ust'))):
    for x in L_: HARIC_PLAN.add((a_, x)); HARIC_NEDEN[(a_, x)] = 'perçin somun deliğe düz gövdeyle girer, sıkılınca alt kısmı şişer (model sıkılmış hâli gösterir)'
for kb_ in ('g_kosebent_sol_ust_1', 'g_kosebent_sol_ust_2', 'g_kosebent_sol_ust_3'):
    HARIC_PLAN.add((kb_, 'g_pu_sol')); HARIC_NEDEN[(kb_, 'g_pu_sol')] = 'MODEL AÇIĞI: PU sol levha köşebendin büküm dış köşesini sarıyor (köpük modeli) — kesilmiş levha olarak takılamaz'
for a in ('g_dis_tavan_1', 'g_dis_tavan_2', 'tasiyici_ust', 'tasiyici_plaka_-484', 'tasiyici_plaka_-574', 'gfrp_ust_arka', 'gfrp_ust_on'): HARIC_PLAN.add(('percin_ust', a))
KAM.append([0.0, [6.2, 3.2, 5.6], [2.57, 0.45, -0.4]])
t = 0.4
SASE = ['sase_boy_arka', 'sase_boy_on'] + sorted(a for a in P if a.startswith('sase_capraz_'))
YAN = (60.0, 0.0, 0.0)          # sütundan yana sürme (bölme sandviçi): önce sütunda +x 60, sonra −x
# ---- 1 ŞASE
adim('Şase', 'Alt şase: 2 boy profili + 7 çapraz profil (AISI 304 kutu 60 × 60, kesim boyunda) yukarıdan iner; her çapraz profil iki ucundan boy profillerine TIG çevre dikişiyle kaynaklanır. Üst duvara 10 × M8 kapalı uçlu perçin somun sıkılır.',
     'boy profili × 2 · çapraz profil × 7 · TIG çevre dikişi × 14 · M8 perçin somun × 10')
kamera_genel(SASE, olcek=0.9)
for a in ['sase_boy_arka', 'sase_boy_on']: t = yerlestir([a], ['ust'], t, 'Boy profili 60 × 60 (kesim boyu 3661) yerine', sure_bekle=0.1)
KAY_SASE = {a: [k for k in P if k.startswith('kaynak_' + a + '_')] for a in SASE if a.startswith('sase_capraz')}
ilk = True
for a in sorted(KAY_SASE):
    tt = yerlestir([a], ['ust'], t, 'Çapraz profil ↔ boy profilleri: iki uçta TIG çevre dikişi', grup_kaynak=KAY_SASE[a], sure_bekle=0.05)
    if ilk: yakin(merkez(KAY_SASE[a][0]), 0.45, tt=tt - 0.2); ilk = False
t = bitti() + 0.2
yakin(np.array([1100, 115, -110]), 0.3)
t = tak('percin_sase', t, 0.6, 40.0, 'Perçin somun M8 × 10 → şase üst duvarındaki deliklere sıkılır (çekme aleti, başı oturur)') + 0.5
# ---- 2 AYAKLAR
adim('Ayaklar', '14 ayarlı ayak (M12, katalog) şasenin altındaki kör burçlara aşağıdan vidalanır.', 'ayarlı ayak × 14 (M12)')
kamera_genel(SASE + ['ayaklar'], yon=(0.4, 0.25, 0.8), olcek=0.8)
t = yerlestir(['ayaklar'], ['alt'], t, 'Ayarlı ayaklar M12 → şase altındaki burçlara (aşağıdan vidalanır)') + 0.4
# ---- 3 DIŞ TABAN + ŞASE CIVATALARI
adim('Dış taban', 'Dış taban iki parça (AISI 304 1,5 mm, lazer — büküm yok) şasenin üstüne iner; perçin somun başları tabandaki Ø15,5 boşluk deliklerine girer. Ek yerine üstten ek laması (punta 18). 10 × M8 cıvata + pul taban deliklerinden şasedeki perçin somunlara.',
     'dış taban 1 / 2 · ek laması (punta 18) · M8 cıvata × 10 + pul × 10')
kamera_genel(['g_dis_taban_1', 'g_dis_taban_2'], olcek=0.75)
for a in ['g_dis_taban_1', 'g_dis_taban_2', 'g_dis_taban_ek_lamasi']: t = yerlestir([a], ['ust'], t, '%s → şase üst yüzüne' % P[a]['ac'])
olay(t - 0.3, 'Punta 18 nokta: dış taban ek laması ↔ taban 1 / 2'); vurgu(['g_dis_taban_ek_lamasi'], t - 0.3, t + 1.0)
yakin(np.array([1100, 125, -110]), 0.3, tt=t + 0.2)
t = tak('sase_pul', t + 0.3, 0.5, 30.0, 'DIN 9021 M8 pul × 10 → dış taban delikleri üstüne')
t = tak('sase_civata', t, 0.6, 40.0, 'ISO 4762 M8 cıvata × 10 → pul + dış taban → şase perçin somunu') + 0.3
# ---- 4 TABAN SANDVİÇİ
adim('Taban yalıtımı + iç taban', 'GFRP ısı köprüsü takozları (dikme altları) dış tabana; PU yalıtım levhası (kesilmiş: dikme, takoz ve cıvata boşlukları açık) serilir; iç taban sacları (1 / 2) üstüne.',
     'GFRP takoz × 6 · PU taban levhası · iç taban 1 / 2')
kamera_genel(['g_pu_taban_0'], olcek=0.7)
t = yerlestir(['gfrp_alt'], ['ust'], t, 'GFRP takoz × 6 → dış taban (dikme altları)')
t = yerlestir(['g_pu_taban_0'], ['ust', 'on'], t, 'PU taban levhası → dış tabanın üstüne (kesilmiş levha)')
for a in ['g_ic_taban_1', 'g_ic_taban_2']: t = yerlestir([a], ['ust', 'on'], t, '%s → PU levhanın üstüne' % P[a]['ac'])
t += 0.3
# ---- 5 DIŞ KABUK
adim('Dış kabuk (taban köşebentleri + arka)', 'Alt köşebentler (1,5 mm · 1 büküm) tabana; arka sac 1 / 2 (2 büküm) arkadan, ek laması içeriden (punta); arka köşe silikonu.',
     'köşebent alt × 8 · arka 1 / 2 + ek laması · punta · silikon')
kamera_genel(['g_dis_sol_yan', 'g_dis_sag_yan', 'g_dis_arka_1', 'g_dis_arka_2'], yon=(0.35, 0.55, -0.75), olcek=0.7)
ilk = True
for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_alt_' in x):
    yerlestir([a], ['ust', 'on'], t, '%s → taban köşesi (punta)' % P[a]['ac'], kamera_yakin=ilk); ilk = False
t = bitti()
t = yerlestir(['g_dis_arka_1', 'g_dis_arka_ek_lamasi'], ['arka', 'ust'], t, 'Dış arka 1 (+ ek laması tezgâhta puntalı) → arkadan')
t = yerlestir(['g_dis_arka_2'], ['arka', 'ust'], t, 'Dış arka 2 → arkadan, ek lamasına punta')
t = buyu('silikon_arka_kose', t, 0.6); olay(t - 0.6, 'Arka köşe silikonları sıkılır'); t += 0.3
adim('Sol yan sac', 'Sol yan sac (1 büküm) yukarıdan iner; alt köşebentlere ve arka saca punta.', 'sol yan · punta')
kamera_genel(['g_dis_sol_yan'], olcek=0.9)
t = yerlestir(['g_dis_sol_yan'], ['ust', 'sol'], t, 'Dış sol yan → taban + köşebentler (punta)') + 0.2
# ---- 6 ARKA + SOL DUVAR SANDVİÇİ
adim('Arka ve sol duvar yalıtımı + iç saclar', 'Yüzey yüzey: PU arka levhaları (alçak / yüksek, kesilmiş) dış arka sacın önüne, iç arka sac 1 / 2 önüne; sol duvarda PU levha ve iç sol duvar (15 PEM SP-M5 + köpük kapağı üretimde preslenir).',
     'PU arka × 2 · iç arka 1 / 2 · PU sol · iç sol duvar + 15 PEM')
kamera_genel(['g_pu_arka_yuksek', 'g_pu_arka_alcak', 'g_pu_sol'], olcek=0.7)
for a in ['g_pu_arka_yuksek', 'g_pu_arka_alcak']: t = yerlestir([a], ['ust', 'on'], t, '%s → dış arka sacın önüne (kesilmiş levha)' % P[a]['ac'])
for a in ['g_ic_arka_1', 'g_ic_arka_2']: t = yerlestir([a], ['ust', 'on'], t, '%s → PU levhanın önüne' % P[a]['ac'], pem=PEM_SAC.get(a, []))
t = yerlestir(['g_pu_sol'], ['ust', 'on'], t, 'PU sol levha → dış sol yanın içine')
t = yerlestir(['g_ic_sol_duvar'], [('on', (60.0, 0.0, 0.0)), 'ust', 'on'], t, 'İç sol duvar → PU sol levhanın önüne', pem=PEM_SAC.get('g_ic_sol_duvar', []), kamera_yakin=True) + 0.2
# ---- 7 BÖLMELER (soldan sağa, her biri sandviç)
adim('Bölmeler 1–5', 'Her bölme bir sandviç: sac A yukarıdan (PEM SP-M5 + köpük kapağı üretimde preslenir) → kovanlar (kablo kanalı geçişi, 1–2 büküm) sütundan yana sürülür, sac A\'ya köşe TIG → PU levha (kesilmiş) sütundan yana → sac B (PEM\'li) sütundan yana kapanır, kovanlara köşe TIG. Bölme 5\'i teknik bölme sol duvarı kapatır.',
     'sac A × 5 · kovan × 12 (köşe TIG) · PU × 5 · sac B × 4 + teknik sol duvar · PEM SP-M5 × 111 + köpük kapağı · gider silikonu')
ilk = True
for k in range(1, 6):
    kamera_genel(['g_bolme_%d_sac_a' % k, 'g_bolme_%d_pu' % k], yon=(0.6, 0.5, 0.65), olcek=0.75)
    a = 'g_bolme_%d_sac_a' % k
    t = yerlestir([a], ['ust', 'on'], t, 'Bölme %d sac A → iç taban + iç arka' % k, pem=PEM_SAC.get(a, []), kamera_yakin=ilk)
    for a in sorted(x for x in SAC if x.startswith('g_bolme_%d_kovan' % k)):
        kk = 'kaynak_%s_a' % a[2:]
        yerlestir([a], [('on', YAN), 'sag', 'ust'], t, '%s → sac A deliğine, köşe TIG' % P[a]['ac'], grup_kaynak=[kk] if kk in P else [], kamera_yakin=ilk); ilk = False
    t = bitti()
    t = yerlestir(['g_bolme_%d_pu' % k], [('on', YAN), 'sag', 'ust'], t, 'Bölme %d PU levhası (kesilmiş) → sac A\'ya, kovanlar boşluklarından geçer' % k)
    b = 'g_bolme_%d_sac_b' % k if k < 5 else 'g_teknik_sol_duvar'
    kb = [x for x in P if x.startswith('kaynak_bolme_%d_kovan' % k) and x.endswith('_b')]
    t = yerlestir([b], [('on', YAN), 'sag', 'ust'], t, '%s → PU levhanın üstüne kapanır, kovanlara köşe TIG' % P[b]['ac'], pem=PEM_SAC.get(b, []), grup_kaynak=kb)
for k in range(1, 6):
    if 'silikon_gider_%d' % k in P: buyu('silikon_gider_%d' % k, t, 0.6)
olay(t, 'Gider geçişi silikonları sıkılır'); t += 0.9
adim('Soğutma grubu + elektrik kutuları', 'Bölmeler bitince, sağ yan kapanmadan: soğutma grubu (kompresör + kondenser + fan, tek ürün) sağ alt bölmeye yukarıdan iner, braketleri köşebent aralıklarına oturur; B elektrik kutusu rafın üstünden önden dış arka saca; istasyon kutusu.',
     'soğutma grubu · B elektrik kutusu · istasyon kutusu')
kamera_genel(['sogutma_grubu', 'elektrik_kutusu'], olcek=0.9)
t = yerlestir(['sogutma_grubu'], ['ust', 'on', 'sag'], t, 'Soğutma grubu → sağ alt bölme (braketler köşebent aralıklarına)', kamera_yakin=True)
t = yerlestir(['elektrik_kutusu'], ['on', ('on', (0.0, 25.0, 0.0)), ('on', (0.0, 29.0, 0.0)), 'ust'], t, 'B elektrik kutusu → soğutma grubu rafının üstünden teknik bölme arka duvarına', kamera_yakin=True)
t = yerlestir(['istasyon_kutusu'], ['ust', 'on'], t, 'İstasyon kutusu') + 0.2
adim('Sağ yan sac', 'Sağ yan sac (1 büküm) yukarıdan iner; alt köşebentlere ve arka saca punta.', 'sağ yan · punta')
kamera_genel(['g_dis_sag_yan'], olcek=0.9)
t = yerlestir(['g_dis_sag_yan'], ['ust', 'sag'], t, 'Dış sağ yan → taban + köşebentler (punta)')
t += 0.2
# ---- 9 SOĞUTMA
adim('Evaporatörler', 'Evaporatör 1 ve 2 (fan + serpantin + tava, braketleriyle tek ürün) çekmece sütunlarından içeri sürülür, iç arka saca oturur.',
     'evaporatör × 2')
kamera_genel(['evaporator_1', 'evaporator_2'], olcek=0.7)
for a in ['evaporator_1', 'evaporator_2']: t = yerlestir([a], ['on', 'ust'], t, '%s → iç arka saca (önden)' % P[a]['ac'], kamera_yakin=(a == 'evaporator_1'))
# ---- 10 İÇ KANALLAR + KABLOLAR + TAHRİK (ön çerçeveden önce)
adim('İç kanallar + kablolar', 'İç kablo kanalı parçaları sütun sütun önden; enerji zinciri kanalı + zemin contası, kablo klipsi. Güç (kırmızı) ve evaporatör (mavi) kabloları kanal boyunca çekilir.',
     'iç kanal parçası × %d · zincir kanalı · klips · güç / bilgi kabloları' % len([a for a in P if a.startswith('ic_kanal_')]))
kamera_genel([a for a in P if a.startswith('ic_kanal_')], yon=(0.35, 0.4, 0.9), olcek=0.6)
KANAL_BUYU = []
for a in sorted(x for x in P if x.startswith('ic_kanal_')):
    n0 = len(PLAN_SORUN); yon_sec([a], ['on', 'ust'])
    if len(PLAN_SORUN) > n0: PLAN_SORUN.pop(); KANAL_BUYU.append(a); continue
    yerlestir([a], ['on', 'ust'], t, None, sure_bekle=0.0)
t = bitti()
for a in KANAL_BUYU: buyu(a, t, 0.7)
if KANAL_BUYU: olay(t, '%d kanal parçası kovan / bölme geçişinden geçirilerek birleştirilir (kanal boyunca)' % len(KANAL_BUYU)); t += 0.8
t = bitti()
t = yerlestir(['zincir_kanal'], ['on', 'alt'], t, 'Enerji zinciri kanalı + zemin contası')
t = buyu('guc_kablo', t, 0.8)
if 'evap_kablo' in P: t = buyu('evap_kablo', t - 0.4, 0.8)
olay(t - 0.8, 'Güç (kırmızı) ve evaporatör (mavi) kabloları kanal boyunca çekilir'); t += 0.3
KOL = {}
for ck in CEKD: KOL.setdefault(ck.split('_')[1], []).append(ck)
adim('Tahrik üniteleri', 'Her çekmece için (ön çerçeveden önce): motor braketi önden arka duvara, 2 × DIN 7991 M5 × 6 → arka iç sacdaki PEM SP-M5; step motor (katalog) göbeğiyle braket deliğine, 4 × DIN 7991 M3 × 6; GT3 kasnak mile + DIN 913 M3 × 4 setskur.',
     'motor braketi × 21 + M5 × 6 × 42 · step motor × 21 + M3 × 6 × 84 · kasnak × 21 + setskur × 21')
kamera_genel([ck + '_tahrik' for ck in CEKD], yon=(0.35, 0.45, 0.85), olcek=0.6)
ilk = True
for k in sorted(KOL):
    for ck in KOL[k]: yerlestir([ck + '_braket'], ['on'], t, None, sure_bekle=0.0)
    t = bitti()
    for ck in KOL[k]: tak(ck + '_tahrik_vida', t, 0.5, 25.0)
    olay(t, 'Sütun %s: motor braketi × %d → arka iç sac: 2 × DIN 7991 M5 × 6 → PEM SP-M5' % (k, len(KOL[k])))
    if ilk: yakin(merkez(KOL[k][0] + '_tahrik_vida'), 0.35, tt=t - 0.2)
    t = bitti() + 0.1
    for ck in KOL[k]: yerlestir([ck + '_tahrik'], [('on', (4.0, 0.0, 0.0)), ('on', (40.0, 0.0, 0.0)), 'on'], t, None, sure_bekle=0.0)
    t = bitti()
    for ck in KOL[k]: tak(ck + '_motor_vida', t, 0.5, 12.0)
    olay(t, 'Sütun %s: step motor redüktör göbeğiyle braket deliğine (eksen boyunca) · 4 × DIN 7991 M3 × 6 → motor yüzündeki M3 dişler' % k)
    if ilk: yakin(merkez(KOL[k][0] + '_motor_vida'), 0.3, tt=t - 0.2)
    t = bitti() + 0.1
    for ck in KOL[k]: tak(ck + '_kasnak', t, 0.5, 12.0)
    t = bitti()
    for ck in KOL[k]: tak(ck + '_setskur', t, 0.4, 15.0)
    olay(t - 0.5, 'Sütun %s: GT3 motor kasnağı mile (eksen boyunca) · DIN 913 M3 × 4 setskur radyal deliğe' % k)
    if ilk: yakin(merkez(KOL[k][0] + '_kasnak'), 0.3, tt=t - 0.5); ilk = False
    t = bitti() + 0.15
for a in sorted(x for x in P if x.startswith('b_kanal_') and x != 'b_kanal_988'): yerlestir([a], ['on', 'ust'], t, 'Sütun dikey kablo kanalı → iç arka sac (motor rakorlarının yanına)')
t = bitti()
adim('Arka kablo kanalı + gider hortumu', 'Arka kablo kanalı parçaları bölme kovanlarından geçirilerek birleştirilir; evaporatör gider hortumu kanal boyunca çekilir; kablo klipsi.', 'B arka kanal · gider hortumu · klips')
kamera_genel(['b_kanal_988', 'gider_hortumu'], olcek=0.7)
t = buyu('b_kanal_988', t, 1.0); olay(t - 1.0, 'Arka kablo kanalı: parçalar kovanlardan geçirilip birleştirilir (kanal boyunca)')
t = buyu('gider_hortumu', t, 0.8); olay(t - 0.8, 'Gider hortumu kanal boyunca çekilir'); t += 0.2
t = yerlestir(['kablo_klips'], ['on', 'ust'], t, 'Kablo klipsi')
# ---- 11 İÇ TAVAN + ISI KALKANI + TEKNİK KAPAMA (iskelet üst kirişlerinden önce)
adim('İç tavan + ısı kalkanı + teknik kapama', 'Üst köşebentler (1 büküm) yan saclara (punta); iç tavan 1 / 2 bölmelerin üstüne; PU tavan levhaları (kiriş kanalları açık, kesilmiş); fırın üstünde PU tavan, ısı kalkanı U (2 büküm) + ışınım sacı, köşe PU\'ları, 12 PTFE takoz; teknik bölmede ara arka sac ve PU levhalar.',
     'iç tavan × 2 · PU fırın tavanı · ısı kalkanı U · ışınım sacı · PU köşe × 2 · PU B5 üst · takoz × 12 · teknik PU × 4 · ara arka sac')
kamera_genel(['g_ic_tavan_1', 'g_ic_tavan_2', 'g_isi_kalkani_u'], olcek=0.7)
for a in ['g_ic_tavan_1', 'g_ic_tavan_2', 'g_pu_tavan_yuksek', 'g_pu_tavan_topping', 'g_pu_tavan_firin', 'g_pu_isi_kalkani_kose_sol_0', 'g_pu_isi_kalkani_kose_sag_0', 'g_isi_kalkani_u', 'g_isi_kalkani_isinim_08', 'g_pu_b5_ust']:
    t = yerlestir([a], ['ust', 'on'], t, '%s → yerine' % P[a]['ac'])
t = yerlestir(['takozlar'], ['ust', 'on'], t, '12 PTFE takoz → ısı kalkanı üstü')
for a in ['g_tk_ara_arka_sac', 'g_tk_ara_pu', 'depo_arka_sac', 'g_tk_depo_arka_pu', 'g_tk_depo_sag_pu', 'g_tk_depo_tavan_pu', 'depo_ic_sac']:
    t = yerlestir([a], ['ust', 'on', 'sag'], t, '%s → teknik bölme' % P[a]['ac'])
for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_ust_' in x): yerlestir([a], ['ust', 'on'], t, '%s → yan sac üst köşesi (punta)' % P[a]['ac'])
t = bitti() + 0.2
# ---- 12 MODÜLER İSKELET
adim('Modüler iskelet', '3 ara dikme ve 6 taşıyıcı dikme yukarıdan PU / iç sac boşluklarından GFRP takozlara (dış tabana) iner; arka ve ön merdiven çerçeve (kaynaklı alt montaj) iner, ara dikme başları üst kirişe TIG. Taşıyıcı üst çerçeve dikmelere iner, dikme başları TIG. Üstte GFRP şeritler ve A / K bağlantısı için 8 × M8 perçin somun.',
     'ara dikme × 3 · merdiven çerçeve × 2 (TIG) · taşıyıcı dikme × 6 + üst çerçeve (TIG) · GFRP şerit × 2 · M8 perçin somun × 8')
ISK = ['moduler_cerceve_arka', 'moduler_cerceve_on', 'tasiyici_ust'] + [a for a in P if a.startswith(('moduler_dikme', 'tasiyici_dikme'))]
kamera_genel(ISK, olcek=0.7)
MD = sorted(x for x in P if x.startswith('moduler_dikme'))
for a in MD: yerlestir([a], ['ust'], t, 'Ara dikme → GFRP takoz (dış taban)', sure_bekle=0.05)
TD = sorted(a for a in P if a.startswith('tasiyici_dikme') and HI[a][1] < 750)
for a in TD: yerlestir([a], ['ust'], t, 'Taşıyıcı dikme → dış taban', sure_bekle=0.05)
t = bitti()
t = yerlestir(['moduler_cerceve_arka'], ['ust'], t, 'Arka merdiven çerçeve → GFRP takozlar · ara dikme başı TIG', grup_kaynak=[x for x in ['kaynak_moduler_dikme_1421_arka'] if x in P])
t = yerlestir(['moduler_cerceve_on'], ['ust'], t, 'Ön merdiven çerçeve → GFRP takozlar · ara dikme başları TIG', grup_kaynak=[x for x in ['kaynak_moduler_dikme_1421_on', 'kaynak_moduler_dikme_2076_on'] if x in P])
yakin(np.array([1436, 753, -110]), 0.4, tt=t - 0.5)
t = yerlestir(['tasiyici_ust', 'tasiyici_dikme_3386_600', 'tasiyici_plaka_-484', 'tasiyici_plaka_-574'], ['ust'], t, 'Taşıyıcı üst çerçeve → dikmelere: dikme başları TIG', grup_kaynak=['kaynak_' + a for a in TD])
for a in ['gfrp_ust_arka', 'gfrp_ust_on']: t = yerlestir([a], ['ust'], t, 'GFRP üst şerit → üst kiriş')
t = tak('percin_ust', t, 0.6, 40.0, 'M8 perçin somun × 12 → üst kirişler (A kaidesi ve K iskeleti cıvataları için)') + 0.3
# ---- 13 TAVAN
adim('Tavan', '3 ek laması; dış tavan 1 / 2 GFRP şeritlerin üstüne (punta); ek yeri silikonu.',
     'ek laması × 3 · dış tavan × 2 · silikon')
kamera_genel(['g_dis_tavan_1', 'g_dis_tavan_2'], olcek=0.7)
for a in ['g_dis_tavan_ek_lamasi_1', 'g_dis_tavan_ek_lamasi_2', 'g_dis_tavan_ek_lamasi_3']: yerlestir([a], ['ust', 'on'], t, '%s (punta)' % P[a]['ac'])
t = bitti()
for a in ['g_dis_tavan_1', 'g_dis_tavan_2']: t = yerlestir([a], ['ust'], t, '%s → GFRP şeritler + köşebentler üstüne (punta)' % P[a]['ac'])
t = buyu('silikon_ek_yeri', t, 0.6); olay(t - 0.6, 'Dış kabuk ek yeri silikonu (taban / arka / tavan)'); t += 0.3
# ---- 14 ÖN ÇERÇEVE
adim('Ön çerçeve + avara üniteleri', '430 ferritik ön çerçeve iki parça (lazer, düz). Tezgâhta: her çekmecenin avara ünitesi (kol + sensör laması + mil + kasnak + reed sensörler, kaynaklı alt montaj; çerçeve ağzından geçmeyecek kadar uzun) ön flanşından çerçevenin arkasına TIG köşe 2 × 8 mm. Çerçeve 1 (K1–K2) ve 2 (K3–K6) avaralarıyla birlikte önden gelir; ek yeri arkadan ek lamasıyla.', 'ön çerçeve 1 / 2 · ek laması · avara ünitesi × 21 · TIG 2 × 8 mm × 21')
kamera_genel(['g_on_cerceve_1', 'g_on_cerceve_2'], yon=(0.3, 0.35, 0.9), olcek=0.7)
t = yerlestir(['g_on_cerceve_ek_lamasi'], ['on'], t, 'Ön çerçeve ek laması → bölme 2 önüne')
for cer, kol in (('g_on_cerceve_1', ('K1', 'K2')), ('g_on_cerceve_2', ('K3', 'K5', 'K6'))):
    av = [ck + '_avara' for ck in sorted(CEKD) if ck.split('_')[1] in kol]; ka = [ck + '_kaynak' for ck in sorted(CEKD) if ck.split('_')[1] in kol]
    t = yerlestir([cer] + av + ka, ['on'], t, '%s + %d avara ünitesi (tezgâhta arkasına TIG) → bölme ve kovan önlerine' % (P[cer]['ac'], len(av)), tezgah_kaynak=ka, kamera_yakin=(cer == 'g_on_cerceve_1'))
t = yerlestir(['g_cerceve_derz_dolgusu'], ['on'], t, 'Ön çerçeve derz dolgu şeridi → çerçeve 1 ↔ 2 arası')
t += 0.3
# ---- 16–18 RAYLAR · TAHRİK · ÇEKMECELER (sütun sütun)
adim('Sabit raylar', '42 ray ünitesi (Accuride DZ3832-0700, katalog) sütun sütun önden sürülür; her ray 3 × DIN 7991 M5 × 6 havşa vida ile bölme sacındaki PEM SP-M5\'lere (126 vida, her biri kendi ekseninde).',
     'ray × 42 · DIN 7991 M5 × 6 × 126 → PEM SP-M5')
kamera_genel([ck + '_ray_sol' for ck in CEKD], yon=(0.35, 0.4, 0.9), olcek=0.6)
ilk = True
for k in sorted(KOL):
    rs = [ck + '_ray_' + y for ck in KOL[k] for y in ('sol', 'sag')]
    for r in rs: yerlestir([r], ['on'], t, None, sure_bekle=0.0)
    t = bitti()
    for ck in KOL[k]:
        for y in ('sol', 'sag'): tak(ck + '_vida_' + y, t, 0.55, 25.0)
    olay(t, 'Sütun %s: %d ray × 3 × DIN 7991 M5 × 6 → bölme sacındaki PEM SP-M5 (havşa başı ray deliğine oturur)' % (k, len(rs)))
    if ilk: yakin(merkez(KOL[k][0] + '_vida_sol'), 0.3, tt=t); ilk = False
    vurgu(rs, t, t + 1.2); t = bitti() + 0.15
adim('Çekmeceler', 'İLK çekmecenin tam montajı (her vida, PEM, kaynak tek tek) ayrı sayfada: "Tek çekmece montajı" (bu sayfanın başındaki bağlantı). Burada 21 çekmece bitmiş alt montaj olarak sütun sütun ray ekseni boyunca 900 mm sürülür; GT3 kayış kasnaklara sarılır; çekmece açılır, kayış çenesi: alt gövde (alttan) + üst çene (yandan) + 2 × ISO 7380 M3 × 12 (üstten) + 2 × ISO 4032 M3 somun (alttan); çekmece kapanır; reed ve motor kabloları kanala çekilir.',
     'çekmece × 21 · kayış × 21 · çene: alt gövde + üst çene + 2 × M3 × 12 + 2 × M3 somun · kablolar')
kamera_genel([ck + '_cekmece' for ck in CEKD], yon=(0.35, 0.4, 0.9), olcek=0.6)
ilk = True
for k in sorted(KOL):
    cks = KOL[k]
    grp = [ck + x for ck in cks for x in ('_cekmece', '_ara')]
    t0 = t
    for a in grp: basla(a, np.array([0, 0, 900.0]), t0)
    olay(t0, 'Sütun %s: %d çekmece ray ekseni boyunca sürülür (kızak → ara eleman → dış eleman)' % (k, len(cks)))
    kamera_genel([ck + '_cekmece' for ck in cks], yon=(0.4, 0.4, 0.9), olcek=1.0, tt=t0)
    for a in grp: git(a, np.zeros(3), t0 + 0.2, 1.4)
    t = t0 + 1.7
    for ck in cks: buyu(ck + '_kayis', t, 0.7)
    olay(t, 'Sütun %s: GT3 kayış motor kasnağı ↔ avara kasnağı sarılır' % k); t += 0.85
    for ck in cks: git(ck + '_cekmece', np.array([0, 0, 700.0]), t, 0.9); git(ck + '_ara', np.array([0, 0, 350.0]), t, 0.9)
    olay(t, 'Çekmeceler açılır (çene erişimi)'); t += 1.0
    if ilk: yakin(merkez(cks[0] + '_cene_ust') + np.array([0, 0, 700.0]), 0.28, tt=t - 0.2)
    for ck in cks:
        basla(ck + '_cene_alt', np.array([0, -30.0, 700.0]), t); git(ck + '_cene_alt', np.array([0, 0, 700.0]), t, 0.45)
        basla(ck + '_cene_ust', np.array([30.0, 0, 700.0]), t + 0.5); git(ck + '_cene_ust', np.array([0, 0, 700.0]), t + 0.5, 0.45)
        basla(ck + '_cene_vida', np.array([0, 25.0, 700.0]), t + 1.0); git(ck + '_cene_vida', np.array([0, 0, 700.0]), t + 1.0, 0.45)
        basla(ck + '_cene_somun', np.array([0, -20.0, 700.0]), t + 1.5); git(ck + '_cene_somun', np.array([0, 0, 700.0]), t + 1.5, 0.45)
        vurgu([ck + '_cene_alt', ck + '_cene_ust'], t, t + 1.0); vurgu([ck + '_cene_vida', ck + '_cene_somun'], t + 1.0, t + 2.6)
    olay(t, 'Kayış çenesi: alt gövde (alttan) → üst çene (yandan, kayışın üstüne) → 2 × ISO 7380 M3 × 12 (üstten: tabla + üst çene + kayış + alt gövde) → 2 × ISO 4032 M3 somun (alttan)')
    t += 2.1
    for ck in cks:
        for x in ('_cekmece', '_cene_alt', '_cene_ust', '_cene_vida', '_cene_somun'): git(ck + x, np.zeros(3), t, 0.9)
        git(ck + '_ara', np.zeros(3), t, 0.9)
    olay(t, 'Çekmeceler kapanır'); t += 1.0
    for ck in cks:
        if ck + '_kablo' in P: buyu(ck + '_kablo', t, 0.7)
    olay(t, 'Sütun %s: reed sensör + motor kabloları kanal boyunca' % k); t += 0.85
    for ck in cks:
        for x in ('_cekmece', '_ara', '_kayis', '_cene_alt', '_cene_ust', '_cene_vida', '_cene_somun', '_kablo'):
            if ck + x in P: YER[ck + x] = t; YERINDE.append(ck + x)
    ilk = False
# ---- 19 SOĞUK DEPO + ÖN PANELLER
adim('Soğuk depo + ön paneller', 'Izgara tutucuları, depo rayları ve depo çekmecesi (ön panel + PU + conta) önden; soğutma bölmesinin ön ızgarası; depo önündeki acil stop.',
     'ızgara tutucuları · depo rayları · depo çekmecesi · ön ızgara · acil stop')
kamera_genel(['depo_cekmece', 'sogutma_on_izgara'], yon=(0.4, 0.35, 0.9), olcek=0.8)
t = yerlestir(['izgara_tutucu'], ['on'], t, 'Izgara tutucuları → ön çerçeve')
t = yerlestir(['depo_ray'], ['on'], t, 'Depo sabit rayları')
t = yerlestir(['depo_cekmece'], ['on'], t, 'Depo çekmecesi ray ekseni boyunca')
t = yerlestir(['sogutma_on_izgara'], ['on'], t, 'Soğutma bölmesi ön ızgarası → tutuculara')
t = yerlestir(['acil_stop'], ['on'], t, 'Acil stop → depo ön paneli') + 0.6
kam(t, ([6.0, 2.6, 5.4], [2.57, 0.45, -0.4]))
TOPLAM = round(bitti() + 2.0, 3)
eksik = [a for a in P if a not in GOR]
print('süre %.1f s · adım %d · öğe %d · zamanlanmamış %d %s' % (TOPLAM, len(ADIM), len(P), len(eksik), eksik[:20]))
print('PLAN SORUNU', len(PLAN_SORUN)); [print('  ', s) for s in PLAN_SORUN[:60]]
pickle.dump(dict(P=P, HAR=HAR, GOR=GOR, MF=MF, FRAMES=FRAMES, VU=VU, ISTISNA=ISTISNA, ADIM=ADIM, OLAY=OLAY, KAM=KAM, ACN=ACN, TOPLAM=TOPLAM, PLAN_SORUN=PLAN_SORUN,
                 CEKD=CEKD, SAC_AD=list(SAC), HARIC_PLAN=sorted(HARIC_PLAN), HARIC_NEDEN=HARIC_NEDEN), open('plan_b3.pkl', 'wb'))
print('%.0f s' % (time.time() - T0))
