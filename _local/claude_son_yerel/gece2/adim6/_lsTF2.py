import sys, glbio, re
sys.stdout.reconfigure(encoding='utf-8')
ist = sys.argv[1]
J, P = glbio.oku(r'../adim5/%s_sac_v1.glb' % ist)
for a, p in sorted(P.items(), key=lambda kv: (kv[1]['extras'].get('tur') or '', kv[0])):
    if re.search(r'servis_arka_.*_(pem|vida)$|delik_kaynagi_\d+$', a) and not a.endswith(('_0', '1700_903_pem', '1700_903_vida')): continue
    lo = p['V'].min(0); hi = p['V'].max(0)
    print('%-9s %-48s %6d x %.4f–%.4f y %.4f–%.4f z %.4f–%.4f %s' % (p['extras'].get('tur'), a, len(p['F']), lo[0], hi[0], lo[1], hi[1], lo[2], hi[2],
          {k: v for k, v in p['extras'].items() if k not in ('tur',)}))
