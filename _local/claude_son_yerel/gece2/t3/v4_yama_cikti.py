import io
f = 't3_cikti_v4.py'
s = io.open(f, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a))
    s = s.replace(a, b)


rep('"""A montaj v3 · denetim (kural 17–18) + çıktı (GLB morph + JSON). Girdi: plan_a3.pkl (a3_montaj.py) · yöntem b3_cikti.py ile aynı (+ kapak dönüşü)"""',
    '"""TOPPING montaj v4 · denetim (kural 17–18) + çıktı (GLB morph + JSON). Girdi: plan_t4.pkl (t3_montaj_v4.py) · a3_cikti.py\'den uyarlandı"""')
rep("OUT = os.path.join(W, 'otonom', 'hat3d', 'v3', 'a_montaj')", "OUT = os.path.join(W, 'otonom', 'hat3d', 'v3', 'topping_montaj')")
rep("D = pickle.load(open('plan_a3.pkl', 'rb'))", "D = pickle.load(open('plan_t4.pkl', 'rb'))")
rep("""for a, b in D['HARIC_PLAN']:
    har(a, b, 'PEM kendi deliğine preslenir (sıkı geçme, model teması)')""",
    """for a, b in D['HARIC_PLAN']:
    har(a, b, D['HARIC_NEDEN'].get((a, b)) or D['HARIC_NEDEN'].get((b, a)) or 'PEM kendi deliğine preslenir (sıkı geçme, model teması)')""")
rep("    ka = P[a]['tur'] == 'kaynak' or P[b]['tur'] == 'kaynak'\n    if ka: har(a, b, 'kaynak dikişi birleştirdiği parçaya kaynar (dolgu ↔ ana metal)')",
    "    ka = P[a]['tur'] == 'kaynak' or P[b]['tur'] == 'kaynak'\n    if ka: har(a, b, 'kaynak dikişi birleştirdiği parçaya kaynar (dolgu ↔ ana metal)')\n"
    "    elif P[a]['tur'] == 'silikon' or P[b]['tur'] == 'silikon': har(a, b, 'silikon / yapıştırıcı yüzeye yapışır (dolgu teması)')")
rep("if 'acici' in HAVADA and 'acici_kolon' not in HAVADA: HAVADA.remove('acici')      # aynı ürün: kafa kolona bağlı (tek parça)\n", "")
i = s.index("for a in sorted(x for x in P if x.startswith('arayuz_ab_') and not x.endswith('_pul')):")
j = s.index("import collections\nozet = collections.OrderedDict()")
s = s[:i] + """for a in sorted(x for x in P if x.startswith('arayuz_kb_') and not x.endswith('_pul')):
    vida(a, 'cıvata M8 × 25 (+ küçük pul Ø15)', 8, 'cevre_B', 'B kirişi M8 perçin somun', ['kaide_ust_plaka_4', 'kaide_sol_boru', 'kaide_sag_boru', 'kaide_enine_boru'])
for a in sorted(x for x in P if x.startswith('arayuz_kaide_M6')):
    vida(a, 'cıvata M6 × 12', 6, 'kaide_plaka_pem_M6_' + a.split('_')[-1], 'preslenmiş somun M6 (kaide plakası)', ['teknik_on_perde', 'dis_taban', 'kaide_ust_plaka_4'])
for a in sorted(x for x in P if x.startswith('arayuz_m8_F') and not x.endswith('_pul')):
    vida(a, 'cıvata M8 × 16 (+ pul)', 8, 'pem_M8_F_' + a.split('arayuz_m8_F_')[1], 'preslenmiş somun M8 (sağ yan)', ['dis_yan_sag', 'cevre_F'])
for a in sorted(x for x in P if x.startswith('servis_arka') and x.endswith('_vida')):
    vida(a, 'havşa vida M5 × 12 (dimple)', 5, a[:-5] + '_burc', 'kaynak burcu M5 Ø14 × 9', ['dis_arka_servis'])
for a in sorted(x for x in P if x.startswith(('evaporator_ayak_', 'kanal_kapagi_')) and x.endswith('_vida')):
    vida(a, 'bombe başlı vida M5 × 6', 5, a[:-5] + '_pem', 'preslenmiş somun M5 (kuru bölme tabanı)', ['kuru_bolme_tabani'])
""" + s[j:]
rep("DEN = dict(adim=len(D['ADIM'])", "DEN = dict(haric_neden={'%s ↔ %s' % k: v for k, v in HARIC.items()} if False else None, adim=len(D['ADIM'])")
rep("n = G.glb_yaz(os.path.join(OUT, 'a_montaj.glb'), dug, MATS)", "n = G.glb_yaz(os.path.join(OUT, 'topping_montaj.glb'), dug, MATS)")
rep("OUTJ = dict(surum='a_montaj_v3', ist='A', tarih='4 Eki 2026', kaynak='hat3_v9l.glb (zincir 00–44) + zincir_A_tamamla.py (A1–A3) · A gövdesi h3_a_sac_v1 (açınım) + ana model · üretim: a3_montaj.py',",
    "OUTJ = dict(surum='topping_montaj_v4', ist='TOPPING', tarih='4 Eki 2026', kaynak='zincir 00–50 (adım 37: h3_topping_sac_v2) · TOPPING gövdesi h3_topping_sac_v2 (açınım) + ana model · üretim: t3_montaj_v4.py',")
rep("json.dump(OUTJ, open(os.path.join(OUT, 'a_montaj.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'), default=float)",
    "json.dump(OUTJ, open(os.path.join(OUT, 'topping_montaj.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'), default=float)")
rep("json.dump(DEN, open('sonuc_a3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)", "json.dump(DEN, open('sonuc_t4.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)")
io.open(f, 'w', encoding='utf-8').write(s)
print('ok')
