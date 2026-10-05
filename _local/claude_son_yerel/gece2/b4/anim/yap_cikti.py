import io
s = io.open('../../b3/b3_cikti.py', encoding='utf-8').read()
R = [
("sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE)", "sys.path.insert(0, os.path.join(HERE, '..', '..', 'cekmece')); sys.path.insert(0, os.path.join(HERE, '..', '..', 'b3')); sys.path.insert(0, HERE)"),
("D = pickle.load(open('plan_b3.pkl', 'rb'))", "D = pickle.load(open('plan_b4.pkl', 'rb'))"),
("""for ck in D['CEKD']:
    har(ck + '_kayis', ck + '_kasnak',""", """# yapıştırıcı filmi / punta noktaları / kaynak dikişleri birleşme anında yerinde belirir; yol denetiminde engel sayılmaz (levha ya da sac yüzünde)
DEKOR = [a for a in P if a.startswith(('yap_', 'punta_'))]
for d in DEKOR:
    for b in P:
        if b != d: HARIC[tuple(sorted((d, b)))] = 'yapıştırıcı filmi / punta noktası (yüzeyde, birleşme anında belirir)'
# kör perçin (sıkılmış hâliyle modelde: uç şişkin) ve PEM saplama (baskıyla oturur) kendi deliğinden geçer: son konumda değdiği sac / kanal / levha ile çifti beyanlı
LOa_ = {a: P[a]['V'].min(0) for a in P}; HIa_ = {a: P[a]['V'].max(0) for a in P}
for a in P:
    et = P[a].get('etur')
    if not (a.startswith('b_') and (et in ('percin', 'saplama', 'percin_somun') or a.endswith('_burc'))): continue
    for b in P:
        if b == a or P[b]['tur'] == 'kablo' or b.startswith(('b_', 'kaynak_', 'punta_', 'yap_')) and not (b.startswith('b_') and (P[b].get('etur') in ('percin', 'pul', 'saplama', 'sac') or not P[b].get('etur'))): continue
        if np.all(HIa_[b] >= LOa_[a] - 0.3) and np.all(LOa_[b] <= HIa_[a] + 0.3):
            HARIC[tuple(sorted((a, b)))] = 'kör perçin / PEM saplama / aralık burcu kendi deliğinde: gövde düz girer, perçin ucu sıkılınca şişer (model sıkılmış hâli) · saplama baskıyla oturur'
for ck in D['CEKD']:
    har(ck + '_kayis', ck + '_kasnak',"""),
("            if P[b].get('sac') == a: continue", "            if P[b].get('sac') == a or b.startswith(('yap_', 'punta_')): continue"),
("MATAD = ['sac', 'kapak', 'profil', 'kaynak',", "MATAD = ['punta', 'yapistirici', 'sac', 'kapak', 'profil', 'kaynak',"),
("""vida_kayit('sase_civata', 'ISO 4762 M8', (0, -1, 0), 'dış taban Ø9 + pul', 'M8 kapalı uçlu perçin somun (şase üst duvarı)', -120.0, -yb.min(), 10, 'perçin somun gövdesi: y %.1f … 120 (iç diş)' % yb.min())""",
 """vida_kayit('sase_civata', 'ISO 4762 M8 × 16', (0, -1, 0), 'dış taban Ø15,5 + pul', 'M8 kapalı uçlu perçin somun (şase üst duvarı, iç diş dibi y 107,5)', -124.5, -107.5, 10, 'kapalı uç: cıvata ucu diş dibinin %.1f mm üstünde' % (uc('sase_civata', (0, -1, 0)) * -1 - 107.5))"""),
("HAVADA = sorted(a for a, (tl, l) in TEM.items() if not l and not a.endswith('_ara'))", "HAVADA = sorted(a for a, (tl, l) in TEM.items() if not l and not a.endswith('_ara') and not P[a].get('ev') and not P[a].get('tezgah') and not P[a].get('fikstur'))   # üretimde preslenen / kaynaklanan, tezgâhta bağlanan, kaynak fikstüründe duran elemanlar\nfrom havada_grup import havada_grup\nHAVADA = havada_grup(HAVADA, P, Pm, HAR, GOR)"),
("DEN = dict(adim=len(D['ADIM']),", "DEN = dict(model_acigi=sum(1 for k, v in HARIC.items() if v.startswith('MODEL AÇIĞI')), adim=len(D['ADIM']),"),
("OUTJ = dict(surum='b_montaj_v3', ist='B', tarih='4 Eki 2026', kaynak='hat3_v9l.glb (zincir 00–44) · B gövdesi h3_b_sac_v1 (açınım) + ana model · üretim: b3_montaj.py',",
 "OUTJ = dict(surum='b_montaj_v4', ist='B', tarih='4 Eki 2026', kaynak='hat3_v9s.glb (zincir 00–51, adım 37 v2 ile · sayfa ?v=9t) · B gövdesi h3_b_sac_v1 (açınım) + ana model · üretim: b4_montaj.py', sehpa=False,"),
]
for a, b in R:
    assert a in s, a[:50]; s = s.replace(a, b)
io.open('b4_cikti.py', 'w', encoding='utf-8', newline='').write(s)
print('ok')
