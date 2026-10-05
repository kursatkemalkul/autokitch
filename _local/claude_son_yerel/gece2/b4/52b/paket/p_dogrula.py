# -*- coding: utf-8 -*-
"""etiket denetimi: her primitive'de mek + kat araliklari indis sayisini TAM kapsar (birim indis, 3'un kati), etiket aralikta; kpk aralikta; ROBOT dugumu yok."""
import json, struct, sys
raw = open(sys.argv[1], 'rb').read(); jl = struct.unpack('<I', raw[12:16])[0]; J = json.loads(raw[20:20 + jl])
nm = len(J['scenes'][0]['extras']['mekanizmalar']); nk = len(J['scenes'][0]['extras']['kategoriler'])
hata = 0; tot = 0; etsiz = 0; say = [0] * nm
for m in J['meshes']:
    for p in m['primitives']:
        n = J['accessors'][p['indices']]['count']; tot += n; ex = p.get('extras', {})
        for key, lim in (('mek', nm), ('kat', nk)):
            L = ex.get(key)
            if not L: etsiz += n; continue
            pos = 0
            for i in range(0, len(L), 3):
                if L[i + 1] != pos or L[i + 2] <= 0 or L[i + 2] % 3 or not (0 <= L[i] < lim): hata += 1
                if key == 'mek' and 0 <= L[i] < lim: say[L[i]] += L[i + 2] // 3
                pos += L[i + 2]
            if pos != n: hata += 1
        K = ex.get('kpk') or []
        for i in range(0, len(K), 2):
            if K[i] % 3 or K[i + 1] % 3 or K[i] + K[i + 1] > n: hata += 1
rob = [n['name'] for n in J['nodes'] if n.get('name', '').startswith('ROBOT_')]
print('indis toplami', tot, '(ucgen', tot // 3, ') · etiket hatasi', hata, '· etiketsiz indis', etsiz, '· ROBOT dugumu', rob)
for i, mm in enumerate(J['scenes'][0]['extras']['mekanizmalar']): print('  %2d %-32s %8d' % (i, mm['kod'], say[i]))
print('animasyon kanal hedefleri gecerli:', all(c['target']['node'] < len(J['nodes']) for a in J['animations'] for c in a['channels']))
