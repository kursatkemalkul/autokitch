import io
f = 't3_montaj_v4.py'
L = io.open(f, encoding='utf-8').read().split('\n')
i = [k for k, l in enumerate(L) if l.startswith('SADE = [')][0]
j = [k for k, l in enumerate(L) if l.startswith('def sade(x):')][0]
yeni = r"""SADE = [(r'servis sacı için 4 × PEM SP-M5', 'servis sacı için 4 kaynak burcu (punta)'), (r'6 × PEM SP-M5 \(servis\)', '6 kaynak burcu (servis sacı)'), (r'2 × PEM SP-M5', '2 kaynak burcu'),
        (r'5 × PEM SP-M5', '5 kaynak burcu'), (r'PEM SP-M(\d)(-\d)?', r'preslenmiş somun M\1'), (r'PEM FHP-M5(-\d+)?', 'preslenmiş saplama M5'), (r"PEM'(ler|lere|in)", r'somun\1'),
        (r'\bPEM\b', 'preslenmiş somun'), (r'ISO 4762 ', 'cıvata '), (r'ISO 7092 M8 pul \(Ø15\)', 'küçük pul M8 (Ø15)'), (r'ISO 7092 ', 'küçük pul '), (r'DIN 7991 ', 'havşa vida '),
        (r'\bTIG\b', 'kaynak'), (r'TEK ÜRÜN', 'hazır ürün'), (r'\bJ1\b', 'fiş paneli'), (r'Secop ', ''), (r'astar', 'iç sac'), (r'Astar', 'İç sac')]"""
L = L[:i] + yeni.split('\n') + L[j:]
io.open(f, 'w', encoding='utf-8').write('\n'.join(L))
print('ok')
