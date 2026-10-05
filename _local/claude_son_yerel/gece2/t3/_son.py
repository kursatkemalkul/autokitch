# ---- zaman ölçeği (izlenebilir hız): bütün zamanlar × OLC
OLC = 1.75
def _o(x): return round(x * OLC, 3)
for a in HAR: HAR[a] = [[_o(h[0]), _o(h[1])] + h[2:] for h in HAR[a]]
for a in GOR: GOR[a] = _o(GOR[a])
for a in MF:
    if 'seg' in MF[a]: MF[a]['seg'] = [[_o(x[0]), _o(x[1]), x[2], x[3]] for x in MF[a]['seg']]
    if 'buyu' in MF[a]: MF[a]['buyu'] = [_o(MF[a]['buyu'][0]), _o(MF[a]['buyu'][1])]
for a in VU: VU[a] = [[_o(v[0]), _o(v[1])] for v in VU[a]]
for x in ADIM: x['t0'] = _o(x['t0'])
OLAY = [[_o(o[0]), o[1]] for o in OLAY]
KAM = [[_o(k[0]), k[1], k[2]] for k in KAM]
for x in ACN: x['t0'] = _o(x['t0']); x['t1'] = _o(x['t1'])
for a in ROT: ROT[a] = [[_o(r[0]), _o(r[1])] + r[2:] for r in ROT[a]]
TOPLAM = _o(TOPLAM)
eksik = [a for a in P if a not in GOR]
print('süre %.1f s · adım %d · öğe %d · zamanlanmamış %d %s' % (TOPLAM, len(ADIM), len(P), len(eksik), eksik[:20]))
print('PLAN SORUNU', len(PLAN_SORUN)); [print('  ', s) for s in PLAN_SORUN[:60]]
pickle.dump(dict(P=P, HAR=HAR, GOR=GOR, MF=MF, FRAMES=FRAMES, VU=VU, ISTISNA=ISTISNA, ROT=ROT, ADIM=ADIM, OLAY=OLAY, KAM=KAM, ACN=ACN, TOPLAM=TOPLAM, PLAN_SORUN=PLAN_SORUN,
                 SAC_AD=list(SAC), CEVRE=CEVRE, KAPAK=KAPGRUP, HARIC_PLAN=sorted(HARIC_PLAN), HARIC_NEDEN=HARIC_NEDEN), open('plan_a3.pkl', 'wb'))
print('%.0f s' % (time.time() - T0))
