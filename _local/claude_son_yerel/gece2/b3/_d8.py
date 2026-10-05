p=open('b3_parca.py',encoding='utf-8').read()
old="    ekle(ck + '_tahrik', *birles([(o['V'], o['F']) for o in tah]), 'motor', 'mek', 'tahrik ünitesi: step motor + motor braketi + GT3 kasnak + 4 × M3 × 6 (tezgâhta takılı)')"
assert old in p
new='''    brk = [o for o in tah if np.all(np.abs((o['hi'] - o['lo']) - [43.0, 44.0, 38.5]) < 0.3)]
    mv = [o for o in tah if np.all(np.abs((o['hi'] - o['lo']) - [6.0, 6.0, 6.0]) < 0.3)]
    ks = [o for o in tah if abs((o['hi'] - o['lo'])[0] - 11.0) < 0.3 and abs((o['hi'] - o['lo'])[1] - 33.51) < 0.3]
    ss = [o for o in tah if np.all(np.abs((o['hi'] - o['lo']) - [2.9, 2.9, 4.0]) < 0.3)]
    rest = [o for o in tah if not any(o is x for x in brk + mv + ks + ss)]
    assert len(brk) == 1 and len(mv) == 4 and len(ks) == 1 and len(ss) == 1, (ck, len(brk), len(mv), len(ks), len(ss))
    ekle(ck + '_braket', brk[0]['V'], brk[0]['F'], 'sac', 'sac', 'motor braketi 3 mm (1 büküm · göbek deliği · 2 × M5 / 4 × M3 havşa)')
    ekle(ck + '_tahrik', *birles([(o['V'], o['F']) for o in rest]), 'motor', 'mek', 'step motor Transmotec PD3665 (redüktör + mil + enkoder + M12, katalog)')
    ekle(ck + '_motor_vida', *birles([(o['V'], o['F']) for o in mv]), 'baglanti', 'baglanti', '4 × DIN 7991 M3 × 6 A2 (braket → motor yüzü M3)', eks=(1.0, 0.0, 0.0))
    ekle(ck + '_kasnak', ks[0]['V'], ks[0]['F'], 'alu', 'mek', 'GT3 motor kasnağı 30 diş (katalog)', eks=(1.0, 0.0, 0.0))
    ekle(ck + '_setskur', ss[0]['V'], ss[0]['F'], 'baglanti', 'baglanti', 'DIN 913 M3 × 4 setskur', eks=(0.0, 0.0, -1.0))'''
p=p.replace(old,new)
open('b3_parca.py','w',encoding='utf-8').write(p)
s=open('plan_kod.py',encoding='utf-8').read()
def rep(a,b):
    global s
    assert a in s, a[:70]; s=s.replace(a,b)
rep("""    for ck in KOL[k]: yerlestir([ck + '_tahrik'], ['on'], t, None, sure_bekle=0.0)
    t = bitti()
    for ck in KOL[k]: tak(ck + '_tahrik_vida', t, 0.5, 25.0)
    olay(t, 'Sütun %s: tahrik ünitesi × %d · motor braketi 2 × DIN 7991 M5 × 6 → arka iç sac PEM SP-M5' % (k, len(KOL[k])))
    if ilk: yakin(merkez(KOL[k][0] + '_tahrik_vida'), 0.35, tt=t - 0.6); ilk = False
    t = bitti() + 0.15""",
"""    for ck in KOL[k]: yerlestir([ck + '_braket'], ['on'], t, None, sure_bekle=0.0)
    t = bitti()
    for ck in KOL[k]: tak(ck + '_tahrik_vida', t, 0.5, 25.0)
    olay(t, 'Sütun %s: motor braketi × %d → arka iç sac: 2 × DIN 7991 M5 × 6 → PEM SP-M5' % (k, len(KOL[k])))
    if ilk: yakin(merkez(KOL[k][0] + '_tahrik_vida'), 0.35, tt=t - 0.2)
    t = bitti() + 0.1
    for ck in KOL[k]: yerlestir([ck + '_tahrik'], [('on', (40.0, 0.0, 0.0)), ('on', (60.0, 0.0, 0.0)), 'on'], t, None, sure_bekle=0.0)
    t = bitti()
    for ck in KOL[k]: tak(ck + '_motor_vida', t, 0.5, 12.0)
    olay(t, 'Sütun %s: step motor redüktör göbeğiyle braket deliğine (eksen boyunca) · 4 × DIN 7991 M3 × 6 → motor yüzündeki M3 dişler' % k)
    if ilk: yakin(merkez(KOL[k][0] + '_motor_vida'), 0.3, tt=t - 0.2)
    t = bitti() + 0.1
    for ck in KOL[k]: tak(ck + '_kasnak', t, 0.5, 20.0)
    t = bitti()
    for ck in KOL[k]: tak(ck + '_setskur', t, 0.4, 15.0)
    olay(t - 0.5, 'Sütun %s: GT3 motor kasnağı mile (eksen boyunca) · DIN 913 M3 × 4 setskur radyal deliğe' % k)
    if ilk: yakin(merkez(KOL[k][0] + '_kasnak'), 0.3, tt=t - 0.5); ilk = False
    t = bitti() + 0.15""")
rep("adim('Tahrik üniteleri', 'Her çekmece için tahrik ünitesi (step motor + braket + GT3 kasnak, tezgâhta kurulu) önden arka duvara; 2 × DIN 7991 M5 × 6 → arka iç sacdaki PEM SP-M5. Ön çerçeve takılmadan (motor gövdesi çerçeve ağzından geçmez).',\n     'tahrik ünitesi × 21 · DIN 7991 M5 × 6 × 42 → PEM SP-M5')",
    "adim('Tahrik üniteleri', 'Her çekmece için (ön çerçeveden önce): motor braketi önden arka duvara, 2 × DIN 7991 M5 × 6 → arka iç sacdaki PEM SP-M5; step motor (katalog) göbeğiyle braket deliğine, 4 × DIN 7991 M3 × 6; GT3 kasnak mile + DIN 913 M3 × 4 setskur.',\n     'motor braketi × 21 + M5 × 6 × 42 · step motor × 21 + M3 × 6 × 84 · kasnak × 21 + setskur × 21')")
# çene üst: +x'ten
rep("        basla(ck + '_cene_ust', np.array([0, 0, 760.0]), t + 0.5)","        basla(ck + '_cene_ust', np.array([30.0, 0, 700.0]), t + 0.5)")
rep("üst çene (önden, kayışın üstüne)","üst çene (yandan, kayışın üstüne)")
rep("alt gövde (alttan) + üst çene (önden) +","alt gövde (alttan) + üst çene (yandan) +")
# ışınım sacı U'dan sonra · istasyon kutusu teknik kapamadan sonra
rep("'g_pu_tavan_firin', 'g_isi_kalkani_isinim_08', 'g_pu_isi_kalkani_kose_sol_0', 'g_pu_isi_kalkani_kose_sag_0', 'g_isi_kalkani_u', 'g_pu_b5_ust']",
    "'g_pu_tavan_firin', 'g_pu_isi_kalkani_kose_sol_0', 'g_pu_isi_kalkani_kose_sag_0', 'g_isi_kalkani_u', 'g_isi_kalkani_isinim_08', 'g_pu_b5_ust']")
# HARIC ekleri
rep("for kb_ in ('g_kosebent_sol_ust_1', 'g_kosebent_sol_ust_2', 'g_kosebent_sol_ust_3'):","""for k in range(1, 6):
    for yan in ('a', 'b'):
        HARIC_PLAN.add(('g_bolme_%d_pu' % k, 'kapak_bolme_%d_sac_%s' % (k, yan))); HARIC_NEDEN[('g_bolme_%d_pu' % k, 'kapak_bolme_%d_sac_%s' % (k, yan))] = 'köpük kapağı PU levhadaki cebine oturur (son 1 mm, model teması)'
for a_, L_ in (('percin_sase', ('sase_boy_arka', 'sase_boy_on')), ('percin_ust', ('moduler_cerceve_arka', 'moduler_cerceve_on', 'tasiyici_ust'))):
    for x in L_: HARIC_PLAN.add((a_, x)); HARIC_NEDEN[(a_, x)] = 'perçin somun deliğe düz gövdeyle girer, sıkılınca alt kısmı şişer (model sıkılmış hâli gösterir)'
for kb_ in ('g_kosebent_sol_ust_1', 'g_kosebent_sol_ust_2', 'g_kosebent_sol_ust_3'):""")
open('plan_kod.py','w',encoding='utf-8').write(s)
m=open('b3_montaj.py',encoding='utf-8').read(); i=m.index('# ================================================================== PLAN')
open('b3_montaj.py','w',encoding='utf-8').write(m[:i]+s)
print('ok')
