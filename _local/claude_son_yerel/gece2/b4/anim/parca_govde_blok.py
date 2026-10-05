# ---------------------------------------------------------------- gövde: m8kit bileşenleri + ad eşleme (v4)
def VF(P):
    u, inv = np.unique(np.round(P.reshape(-1, 3), 4), axis=0, return_inverse=True); return u, inv.reshape(-1, 3)


def sinif(a, dug, tur_ent):
    if tur_ent == 'sac': return ('kapak' if dug == 'B_KASA__on_cerceve' else 'sac'), 'sac'
    if a.startswith('pu_') or a.endswith('_pu') or '_pu_' in a or a.startswith('tk_depo_kose'): return 'pu', 'pu'
    if 'kaynagi' in a: return 'kaynak', 'kaynak'
    if 'silikon' in a: return 'yapistirici', 'silikon'
    if 'kopuk_kapagi' in a: return 'koyu', 'baglanti'
    if a.startswith('isi_kalkani_takozu'): return 'koyu', 'mek'
    return 'baglanti', 'baglanti'


def kut(k): return np.array(k[0::2], float), np.array(k[1::2], float)


GOV_DUG = sorted(set(v['dugum'] for v in ENT.values()) | {'B_KASA__pu_dolgu'})
ATANDI = {}
for dug in GOV_DUG:
    C = BR.get(dug, []); kul = set()
    E = {a: kut(ENT[a]['kutu']) for a, v in ENT.items() if v['dugum'] == dug}
    for a, v in E46.items():
        if v['dugum'] == dug: E.pop(a, None); E[a] = kut(v['kutu'])
    if dug == 'B_KASA__pu':                                  # adım 46: yeniden kesilen blokların eski adları artık yok
        for a in ('pu_sol', 'pu_arka_yuksek', 'pu_arka_alcak', 'tk_depo_arka_pu', 'tk_depo_sag_pu'):
            if a not in E46: E.pop(a, None)
    for a, (lo, hi) in E.items():                            # 1) birebir kutu
        c = [i for i, b in enumerate(C) if i not in kul and np.all(np.abs(b['lo'] - lo) < 0.35) and np.all(np.abs(b['hi'] - hi) < 0.35)]
        if len(c) == 1: kul.add(c[0]); ATANDI[(dug, a)] = c[0]
    for a, (lo, hi) in E.items():                            # 2) kutuyu kapsayan en küçük bileşen (flanşlı iç sac, kapalı uçlu perçin somun)
        if (dug, a) in ATANDI: continue
        c = [i for i, b in enumerate(C) if i not in kul and np.all(b['lo'] <= lo + 0.35) and np.all(b['hi'] >= hi - 0.35)]
        if c:
            i = min(c, key=lambda i: np.prod(C[i]['hi'] - C[i]['lo'] + 0.1)); kul.add(i); ATANDI[(dug, a)] = i
    for a, (lo, hi) in E.items():                            # 3) ent kutusunun İÇİNDEKİ bileşen (kısaltılan cıvata: adım 43 / 47)
        if (dug, a) in ATANDI: continue
        c = [i for i, b in enumerate(C) if i not in kul and np.all(b['lo'] >= lo - 0.35) and np.all(b['hi'] <= hi + 0.35)]
        if c:
            i = max(c, key=lambda i: np.prod(C[i]['hi'] - C[i]['lo'] + 0.1)); kul.add(i); ATANDI[(dug, a)] = i
    for (d_, a), i in list(ATANDI.items()):
        if d_ != dug: continue
        b = C[i]; V, F = VF(b['P'])
        if a in ENT and a not in E46: m_, tur = sinif(a, dug, ENT[a]['tur']); bom = ENT[a].get('bom')
        else: m_, tur = 'pu', 'pu'; bom = E46[a].get('bom')
        ekle('g_' + a, V, F, m_, tur, a, kaynak=dug, bom=bom)
    kalan = [i for i in range(len(C)) if i not in kul]
    for j, i in enumerate(kalan):
        b = C[i]; V, F = VF(b['P'])
        if dug == 'B_KASA__paslanmaz': ekle('g_ray_pem_arka_%02d' % j, V, F, 'baglanti', 'baglanti', 'PEM SP-M5-1 (arka iç sac)')
        elif dug == 'B_KASA__conta': ekle('g_ray_pem_arka_%02d_kopuk_kapagi' % j, V, F, 'koyu', 'baglanti', 'köpük kapağı (arka PEM)')
        elif dug.endswith('baglanti'): ekle('g_percin_somun_ek_%02d' % j, V, F, 'baglanti', 'baglanti', 'M8 kapalı uçlu perçin somun')
        elif dug == 'B_KASA__on_cerceve': ekle('g_cerceve_derz_dolgusu', V, F, 'kapak', 'sac', 'ön çerçeve derz dolgu şeridi')
        else: ekle('g_yeni_%s_%02d' % (dug.replace('__', '_'), j), V, F, 'baglanti', 'baglanti', 'eklenti'); print('  ATANMAYAN', dug, np.round(b['lo'], 1), np.round(b['hi'], 1))
print('gövde:', sum(1 for a in P if a.startswith('g_')), '· ent eşleşmeyen:', [a for a in ENT if (ENT[a]['dugum'], a) not in ATANDI and a not in ('pu_sol', 'pu_arka_yuksek', 'pu_arka_alcak', 'tk_depo_arka_pu', 'tk_depo_sag_pu')][:30])

# ---------------------------------------------------------------- yeni bağlantı elemanları (adım 47 / 49) — B_BAGLANTI__paslanmaz
META = {a: dict(v) for a, v in E47.items() if v['dugum'] == 'B_BAGLANTI__paslanmaz'}
for r in E49['percin']: META[r['ad']] = dict(kutu=r['kutu'], bom=r['bom'], n=r.get('n'), tur='percin', grup='I', dugum='B_BAGLANTI__paslanmaz', ref49=r.get('ref'))
C = BR['B_BAGLANTI__paslanmaz']; kul = set(); bul_yok = []
Cl = np.array([b['lo'] for b in C]); Ch = np.array([b['hi'] for b in C])
for a, v in META.items():
    lo, hi = kut(v['kutu'])
    d_ = np.abs(Cl - lo).max(1) + np.abs(Ch - hi).max(1)
    for i in np.argsort(d_)[:3]:
        if i in kul or d_[i] > 1.4: continue
        kul.add(i); V, F = VF(C[i]['P']); t_ = v['tur']
        ekle('b_' + a, V, F, 'sac' if t_ == 'sac' else 'baglanti', 'sac' if t_ == 'sac' else 'baglanti', a, bom=v['bom'], n=v.get('n'), etur=t_, grup=v.get('grup'))
        break
    else:
        bul_yok.append(a)
print('B_BAGLANTI: %d / %d bileşen eşlendi · eşlenmeyen meta %d %s' % (len(kul), len(C), len(bul_yok), bul_yok[:8]))
# dikme uç plakaları (adım 47, dikme düğümünde; BIL'de dikmeyle kaynaşık → dikme parçasıyla gelir)
