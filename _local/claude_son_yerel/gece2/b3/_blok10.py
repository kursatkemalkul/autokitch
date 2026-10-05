# ---- 10 İÇ KANALLAR + KABLOLAR + TAHRİK (ön çerçeveden önce)
adim('İç kanallar + kablolar', 'İç kablo kanalı parçaları sütun sütun önden; enerji zinciri kanalı + zemin contası, kablo klipsi. Güç (kırmızı) ve evaporatör (mavi) kabloları kanal boyunca çekilir.',
     'iç kanal parçası × %d · zincir kanalı · klips · güç / bilgi kabloları' % len([a for a in P if a.startswith('ic_kanal_')]))
kamera_genel([a for a in P if a.startswith('ic_kanal_')], yon=(0.35, 0.4, 0.9), olcek=0.6)
for a in sorted(x for x in P if x.startswith('ic_kanal_')): yerlestir([a], ['on', 'ust'], t, None, sure_bekle=0.0)
t = bitti()
t = yerlestir(['zincir_kanal'], ['on', 'alt'], t, 'Enerji zinciri kanalı + zemin contası')
t = yerlestir(['kablo_klips'], ['on'], t, 'Kablo klipsi')
t = buyu('guc_kablo', t, 0.8)
if 'evap_kablo' in P: t = buyu('evap_kablo', t - 0.4, 0.8)
olay(t - 0.8, 'Güç (kırmızı) ve evaporatör (mavi) kabloları kanal boyunca çekilir'); t += 0.3
KOL = {}
for ck in CEKD: KOL.setdefault(ck.split('_')[1], []).append(ck)
adim('Tahrik üniteleri', 'Her çekmece için tahrik ünitesi (step motor + braket + GT3 kasnak, tezgâhta kurulu) önden arka duvara; 2 × DIN 7991 M5 × 6 → arka iç sacdaki PEM SP-M5. Ön çerçeve takılmadan (motor gövdesi çerçeve ağzından geçmez).',
     'tahrik ünitesi × 21 · DIN 7991 M5 × 6 × 42 → PEM SP-M5')
kamera_genel([ck + '_tahrik' for ck in CEKD], yon=(0.35, 0.45, 0.85), olcek=0.6)
ilk = True
for k in sorted(KOL):
    for ck in KOL[k]: yerlestir([ck + '_tahrik'], ['on'], t, None, sure_bekle=0.0)
    t = bitti()
    for ck in KOL[k]: tak(ck + '_tahrik_vida', t, 0.5, 25.0)
    olay(t, 'Sütun %s: tahrik ünitesi × %d · motor braketi 2 × DIN 7991 M5 × 6 → arka iç sac PEM SP-M5' % (k, len(KOL[k])))
    if ilk: yakin(merkez(KOL[k][0] + '_tahrik_vida'), 0.35, tt=t - 0.6); ilk = False
    t = bitti() + 0.15
