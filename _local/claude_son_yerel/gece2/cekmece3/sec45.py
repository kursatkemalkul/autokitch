# =====================================================================================================================
# 4. BAĞLANTI ELEMANLARI (tek tek) — geometri cek3geo (ana model adım 44 ile aynı)
# =====================================================================================================================
EL = {}          # ad → dict(eks (giriş yönü birim), yol (mm, giriş öncesi uzaklık))
def el(ad, man, ac, eks, yol=30.0):
    EL[ad] = dict(eks=np.asarray(eks, float), yol=yol); ekle_mf(ad, man, 'baglanti', 'baglanti', ac)


MOG = C.geo_motor()
for i in (1, 2):
    el('vida_braket_%d' % i, MOG['vida_braket_%d' % i], 'DIN 7991 M5 × 6 A2 havşa', (0, 0, -1), 40)
for i in range(1, 5):
    el('vida_motor_%d' % i, MOG['vida_motor_%d' % i], 'DIN 7991 M3 × 6 A2 havşa', (1, 0, 0), 12)
el('setskur', MOG['setskur'], 'DIN 913 M3 × 4 A2 setskur', (0, 0, -1), 25)
for i in (1, 2):
    el('vida_cene_%d' % i, A1G['vida_cene_%d' % i], 'ISO 7380 M3 × 12 A2 (bombe başlı, imbus 2)', (0, -1, 0), 20)
    el('somun_cene_%d' % i, A1G['somun_cene_%d' % i], 'ISO 4032 M3 A2 somun', (0, 1, 0), 18)
    ekle_mf('pem_kulak_%d' % i, A1G['pem_kulak_%d' % i], 'baglanti', 'baglanti', 'PEM CLS-M3-2 (mıknatıs kulağına preslenir)')
    el('vida_miknatis_%d' % i, A1G['vida_miknatis_%d' % i], 'ISO 7380 M3 × 8 A2', (1, 0, 0), 25)
for k_ in ('arka', 'on'):
    for i in (1, 2):
        ekle_mf('pem_reed_%s_%d' % (k_, i), RDG['pem_reed_%s_%d' % (k_, i)], 'baglanti', 'baglanti', 'PEM CLS-M3-2 (reed plakasına preslenir)')
        el('vida_reed_%s_%d' % (k_, i), RDG['vida_reed_%s_%d' % (k_, i)], 'ISO 7380 M3 × 8 A2', (-1, 0, 0), 25)
el('e_segman', C.geo_avara()['e_segman'], 'DIN 6799 RS 5 E segman (A2)', (0, -1, 0), 20)
KOG = C.geo_kose()
for k in KOSE:
    el('vida_' + k['ad'], KOG['vida_' + k['ad']], 'ISO 7380 M4 × 6 A2', (0, -1, 0), 30)
for k_ in STUD:
    lo_ = np.array([1483.5, 428.5, 22.0]) if k_ == 'sol' else np.array([2028.5, 428.5, 22.0]); hi_ = lo_ + [15.0, 49.0, 17.0]
    for a_, m_ in C.geo_stud(k_, lo_, hi_).items():
        if a_.startswith('pem'): ekle_mf(a_, m_, 'baglanti', 'baglanti', 'PEM FHS-M5-10 saplama (kapak iç paneline preslenir)')
        elif a_.startswith('pul'): el(a_, m_, 'DIN 125 M5 A2 pul', (0, 0, 1), 0)
        else: el(a_, m_, 'ISO 4032 M5 A2 somun', (0, 0, 1), 0)
ekle_mf('kapak_pu', C.geo_kapak_pu(MM['on_kapak']['V'].min(0), MM['on_kapak']['V'].max(0)), 'pu', 'mek', 'PU köpük (dış kabuk ↔ iç panel, enjeksiyon)')

# =====================================================================================================================
# 5. KAYNAK DİKİŞLERİ / PUNTA NOKTALARI (birleşme anında belirir + vurgu — kural 5)
# =====================================================================================================================
KAY = {}
def kaynak(ad, L, ac):
    ekle_mf(ad, G.birlesim(L), 'kaynak', 'kaynak', ac); KAY[ad] = ac


kaynak('kaynak_kutu_yan_sol', [G.kaynak_dikisi((1484.5 + 0.6, 423.5 + 0.6, -595.5), (1484.5 + 0.6, 423.5 + 0.6, 20.5))], 'TIG iç köşe: sol yan ↔ taban')
kaynak('kaynak_kutu_yan_sag', [G.kaynak_dikisi((2042.5 - 0.6, 423.5 + 0.6, -595.5), (2042.5 - 0.6, 423.5 + 0.6, 20.5))], 'TIG iç köşe: sağ yan ↔ taban')
kaynak('kaynak_kutu_arka', [G.kaynak_dikisi((1485.1, 424.1, -595.4), (2041.9, 424.1, -595.4)), G.kaynak_dikisi((1485.1, 424.1, -595.4), (1485.1, 480.9, -595.4)),
                            G.kaynak_dikisi((2041.9, 424.1, -595.4), (2041.9, 480.9, -595.4))], 'TIG: arka ↔ taban + iki yan')
kaynak('kaynak_kutu_on', [G.kaynak_dikisi((1485.1, 424.1, 20.4), (2041.9, 424.1, 20.4)), G.kaynak_dikisi((1485.1, 424.1, 20.4), (1485.1, 480.9, 20.4)),
                          G.kaynak_dikisi((2041.9, 424.1, 20.4), (2041.9, 480.9, 20.4))], 'TIG: ön ↔ taban + iki yan')
for yan, xf in (('sol', 1483.5), ('sag', 2043.5)):
    kaynak('punta_lama_' + yan, [G.kaynak_noktasi((xf, 424.8, z_), 1.6) for z_ in (-560.0, -380.0, -200.0, -20.0)], 'punta: lama ↔ kutu yanı (4 nokta)')
    kaynak('punta_braket_' + yan, [G.kaynak_noktasi((x_, y_, 22.0), 1.6) for x_, y_ in ((1491.0, 436.0), (1491.0, 470.0))] if yan == 'sol' else
           [G.kaynak_noktasi((x_, y_, 22.0), 1.6) for x_, y_ in ((2036.0, 436.0), (2036.0, 470.0))], 'punta: ön braket ↔ kutu önü (2 nokta)')
for k in KOSE:
    kaynak('punta_' + k['ad'], [G.kaynak_noktasi((k['xw'], 433.0, k['zc'] + dz), 1.2) for dz in (-5.0, 5.0)], 'punta: köşebent dik kolu ↔ kızak gövdesi (2 nokta)')
kaynak('kaynak_kol_kutu', [G.kaynak_dikisi((1483.5, 457.95, -596.5), (1483.5, 457.95, -567.5)), G.kaynak_dikisi((1483.5, 464.21, -596.5), (1483.5, 464.21, -567.5))],
       'TIG: kol ↔ kutu sol yanı (alt + üst kenar, 2 × 29 mm)')
kaynak('kaynak_tabla', [G.kaynak_dikisi((1480.5, 464.21, -720.5), (1480.5, 464.21, -711.5), 0.6), G.kaynak_dikisi((1483.5, 464.21, -720.5), (1483.5, 464.21, -711.5), 0.6)],
       'TIG köşe: tabla ↔ kol üst yüzü (2 × 9 mm)')
kaynak('kaynak_kulak', [G.kaynak_dikisi((C.KUL_X0, C.MY0, C.MZ0 + 1.0), (C.KUL_X0, C.MY0, C.MZ1 - 1.0), 0.6), G.kaynak_dikisi((C.KUL_X1, C.MY0, C.MZ0 + 1.0), (C.KUL_X1, C.MY0, C.MZ1 - 1.0), 0.6)],
       'TIG köşe: mıknatıs kulağı ↔ tabla (iki yan, 2 × 26 mm)')
kaynak('kaynak_cene', [G.kaynak_dikisi((1477.5, 460.45, -750.0), (1477.5, 460.45, -722.0), 0.5), G.kaynak_dikisi((1491.5, 460.45, -750.0), (1491.5, 460.45, -722.0), 0.5)],
       'TIG: ara parça ↔ alt çene (iki kenar, 2 × 28 mm)')
for k_ in ('arka', 'on'):
    z0, z1 = C.RZ[k_]
    kaynak('punta_reed_' + k_, [G.kaynak_noktasi((C.RPX0 + 1.0, C.RY1, z_), 1.0) for z_ in (z0 + 5.0, z1 - 5.0)], 'punta: reed plakası ↔ sensör laması alt yüzü (2 nokta)')
kaynak('kaynak_avara', [G.kaynak_dikisi((1467.2, 487.55 + 0.4, -29.0), (1467.2, 487.55 + 0.4, -9.0)), G.kaynak_dikisi((1469.2, 487.55 + 0.4, -29.0), (1469.2, 487.55 + 0.4, -9.0)),
                        G.kaynak_dikisi((1467.6, 486.55, -9.0), (1469.6, 486.55, -9.0))], 'TIG: avara kolu kulağı ↔ sensör laması (iki yan + uç)')
kaynak('kaynak_avara_mili', [G.silindir((1469.2, C.AY, -1.0), (1, 0, 0), 4.2, 0.9, 24) - G.silindir((1469.0, C.AY, -1.0), (1, 0, 0), 3.0, 1.4, 24)], 'saplama kaynağı: avara mili ↔ kol')
kaynak('kaynak_avara_cerceve', [G.kaynak_dikisi((1455.5, 492.2, 22.7), (1463.5, 492.2, 22.7), 0.6), G.kaynak_dikisi((1454.2, 494.5, 22.7), (1454.2, 502.5, 22.7), 0.6)],
       'TIG köşe (içeriden): avara kolu ön flanşı ↔ ön çerçeve arkası (2 × 8 mm)')
ekle('avara_mili', AVARA_MILI[0], AVARA_MILI[1], 'mekanizma', 'mek', 'avara mili Ø6 (+1 mm, E segman yuvası Ø5) — kola saplama kaynaklı')

