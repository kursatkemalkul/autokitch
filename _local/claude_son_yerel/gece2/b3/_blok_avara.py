adim('Avara üniteleri', 'Her çekmece için avara ünitesi (kol + sensör laması + mil + kasnak + reed sensörler, kaynaklı alt montaj) önden; ön flanşı ön çerçeve arkasına içeriden TIG (2 × 8 mm).',
     'avara ünitesi × 21 · TIG 2 × 8 mm')
ilk = True
for k in sorted(KOL):
    for ck in KOL[k]: yerlestir([ck + '_avara'], ['on'], t, None, sure_bekle=0.0, grup_kaynak=[ck + '_kaynak'])
    olay(t + 0.3, 'Sütun %s: avara ünitesi × %d → ön çerçeve arkası: TIG köşe (içeriden) 2 × 8 mm' % (k, len(KOL[k])))
    if ilk: yakin(merkez(KOL[k][0] + '_kaynak'), 0.3, tt=t + 0.4); ilk = False
    t = bitti() + 0.15
