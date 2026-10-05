# -*- coding: utf-8 -*-
"""DÜKKÂN YAMASI v1 · yayındaki robotlu makine modeli (hat3_robot_v18, Codex) üzerinde (5 Eki 2026 · Claude · Kemal kararları)
python dukkan_v1.py girdi_ham.glb cikti_ham.glb        (meshopt açılmış ham GLB → ham GLB; sonra meshopt_kucult + gzip)

Kemal (5 Eki): "solda arka arkaya iki kapı: biri dükkâna giriş, sonraki robotun alanına giriş — robot kapısını solda iç kısma koy"
               "ana hat şalteri sağdaki duvarın üstünde; elektrik duvarın içinden aşağı, sonra zemine gömülü gider (robota, QR'a, makineye)".
1. Robot alanı kapısı (CELL62: dikmeler, ayaklar, kapı kanadı, menteşeler, AZM40 kilit + vidaları) sağ uçtan (x 5600) sol uca:
   y ekseninde 180° döndürülür (menteşe dışta, kilit içte — sağdaki ile aynı düzen) ve x 680–720 düzlemine (A'nın sol yüzünün 16 mm solu) taşınır.
   Robot alanının sol sınırı: kapı z 660–1740 + sabit dolgu paneli z 59–660 (A'nın önü ↔ kapı dikmesi).
2. Sağ uç (x 5600) SABİT koruma paneli: aynı dikme / ayak / çerçeve / tel panel (kapı donanımı yok).
3. Eski ayaklı ana hat şalteri (ELK_ANA_HAT ayırıcı + kutu) ve ayaklığı / yükselen kablo-kanal parçaları (x 5330–5700 · z 560–1100) kaldırılır;
   zemin ÜSTÜ kablo rampası (ELK_ZEMIN_KANALI, y 0–123) ve onun içindeki zemin seviyesi ana hat kablo parçaları kaldırılır.
4. Yeni: sağ duvarın iç yüzünde (x 6000) duvar tipi ana şalter kutusu (200 × 300 × 150, kol yerden 1500) + sarı plaka + kırmızı döner kol;
   besleme duvar içinden iner (görünmez), duvar dibinden mevcut gömülü zemin oluğunun (ELK_ZEMIN, x 4040–4845, y −120…0) ön ucuna
   GÖMÜLÜ yeni oluk x 4845–6336 · z 1000–1075 (üstü zeminle aynı düzlemde paslanmaz kapak), içinde güç (kırmızı) + bilgi (mavi) kablosu.
Animasyon kanalları ve düğüm sırası korunur (yalnız sona düğüm eklenir; kaldırılan düğümlerin mesh'i boşaltılır)."""
import sys, json, struct, hashlib
import numpy as np

gi, go = sys.argv[1:3]
raw = open(gi, 'rb').read()
jl = struct.unpack('<I', raw[12:16])[0]; J = json.loads(raw[20:20 + jl])
bl = struct.unpack('<I', raw[20 + jl:24 + jl])[0]; BIN = bytearray(raw[28 + jl:28 + jl + bl])
ACC, BV = J['accessors'], J['bufferViews']
NI = {n.get('name'): i for i, n in enumerate(J['nodes'])}
LOG = []

CT = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
NC = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}
def oku(ai):
    a = ACC[ai]; v = BV[a['bufferView']]; dt = np.dtype(CT[a['componentType']]); n = NC[a['type']]
    st = v.get('byteStride', dt.itemsize * n); o = v.get('byteOffset', 0) + a.get('byteOffset', 0)
    if st == dt.itemsize * n: return np.frombuffer(bytes(BIN[o:o + a['count'] * st]), dt).reshape(a['count'], n).copy()
    return np.stack([np.frombuffer(bytes(BIN[o + i * st:o + i * st + dt.itemsize * n]), dt) for i in range(a['count'])])
def ekle_buf(arr, hedef=None):
    arr = np.ascontiguousarray(arr)
    while len(BIN) % 4: BIN.append(0)
    o = len(BIN); BIN.extend(arr.tobytes()); BV.append(dict(buffer=0, byteOffset=o, byteLength=arr.nbytes, **({'target': hedef} if hedef else {})))
    return len(BV) - 1
def ekle_acc(arr, tip):
    arr = np.asarray(arr)
    if tip == 'POS':
        v = ekle_buf(arr.astype(np.float32), 34962); ACC.append(dict(bufferView=v, componentType=5126, count=len(arr), type='VEC3', min=arr.min(0).tolist(), max=arr.max(0).tolist()))
    elif tip == 'NOR':
        v = ekle_buf(arr.astype(np.float32), 34962); ACC.append(dict(bufferView=v, componentType=5126, count=len(arr), type='VEC3'))
    else:
        v = ekle_buf(arr.astype(np.uint32).reshape(-1), 34963); ACC.append(dict(bufferView=v, componentType=5125, count=int(arr.size), type='SCALAR'))
    return len(ACC) - 1
def mat_of(nm): return J['meshes'][J['nodes'][NI[nm]]['mesh']]['primitives'][0].get('material')
def kutu_mesh(kutular, mat):
    """[(lo, hi) mm] → tek mesh (düz normaller, her kutu 24 köşe)"""
    P, N, I = [], [], []
    for lo, hi in kutular:
        lo = np.array(lo, float) / 1000; hi = np.array(hi, float) / 1000
        for ax in range(3):
            for sg in (0, 1):
                u, w = [k for k in range(3) if k != ax]
                c = []
                for a, b in ((0, 0), (1, 0), (1, 1), (0, 1)):
                    p = np.zeros(3); p[ax] = hi[ax] if sg else lo[ax]; p[u] = (lo, hi)[a][u]; p[w] = (lo, hi)[b][w]; c.append(p)
                nrm = np.zeros(3); nrm[ax] = 1 if sg else -1
                b0 = len(P); P += c; N += [nrm] * 4
                t = [(0, 1, 2), (0, 2, 3)]
                if np.dot(np.cross(c[1] - c[0], c[2] - c[0]), nrm) < 0: t = [(0, 2, 1), (0, 3, 2)]
                I += [(b0 + x, b0 + y, b0 + z) for x, y, z in t]
    pr = dict(attributes=dict(POSITION=ekle_acc(np.array(P), 'POS'), NORMAL=ekle_acc(np.array(N), 'NOR')), indices=ekle_acc(np.array(I), 'IDX'), mode=4)
    if mat is not None: pr['material'] = mat
    J['meshes'].append(dict(primitives=[pr])); return len(J['meshes']) - 1
SAHNE = J['scenes'][J.get('scene', 0)]['nodes']
def dugum(ad, mesh, ex=None, matrix=None):
    n = dict(name=ad, mesh=mesh)
    if ex: n['extras'] = ex
    if matrix is not None: n['matrix'] = matrix
    J['nodes'].append(n); SAHNE.append(len(J['nodes']) - 1); NI[ad] = len(J['nodes']) - 1
def ucgen_sil(nm, f):
    """düğümün üçgenlerinden f(merkez mm, kutu lo, hi) True olanları kaldırır (yeni indeks dizisi)"""
    me = J['meshes'][J['nodes'][NI[nm]]['mesh']]; say = 0
    for pr in me['primitives']:
        X = oku(pr['attributes']['POSITION']).astype(float) * 1000; I = oku(pr['indices']).reshape(-1, 3).astype(np.int64)
        Q = X[I]; sil = f(Q.mean(1), Q.min(1), Q.max(1))
        if sil.any(): pr['indices'] = ekle_acc(I[~sil], 'IDX'); say += int(sil.sum())
    return say

# ---------------------------------------------------------------- 1 + 2: robot alanı kapısı sola, sağ uç sabit panel
CELL = [n for n in NI if n and n.startswith('CELL62_')]
assert len(CELL) >= 30, len(CELL)
SABIT = ['CELL62_post_660', 'CELL62_post_1700', 'CELL62_foot_660', 'CELL62_foot_1700', 'CELL62_gate_bar_40', 'CELL62_gate_bar_2000',
         'CELL62_gate_side_703', 'CELL62_gate_side_1667', 'CELL62_gate_screen']
for nm in SABIT:
    n = J['nodes'][NI[nm]]
    dugum('SABIT62_' + nm[7:], n['mesh'], dict(connection='sabit koruma paneli · çerçeve TIG, ayaklar zemine dübel', scope='claude_dukkan_v1'))
M = [-1, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0, 6.32, 0, 2.4, 1]          # x' = 6,32 − x · z' = 2,4 − z (m) · sütun düzeni
for nm in CELL:
    n = J['nodes'][NI[nm]]; assert not any(k in n for k in ('matrix', 'translation', 'rotation', 'scale')), nm
    n['matrix'] = M; n.setdefault('extras', {})['konum'] = 'robot alanı sol girişi (dükkân giriş kapısının arkası)'
LOG.append('robot kapısı: %d parça x 5600 → x 680–720 (y 180°) · sağ uca %d parçalı sabit panel' % (len(CELL), len(SABIT)))
# sol dolgu paneli z 59–660 (A'nın önü ↔ kapı dikmesi)
mp, ms = mat_of('CELL62_post_660'), mat_of('CELL62_gate_screen')
dugum('SABIT62_sol_dolgu_dikme', kutu_mesh([((680, 6, 59), (720, 2050, 99))], mp), dict(connection='TIG · ayak zemine dübel', scope='claude_dukkan_v1'))
dugum('SABIT62_sol_dolgu_cerceve', kutu_mesh([((690, 40, 99), (720, 70, 660)), ((690, 2000, 99), (720, 2030, 660))], mp), dict(connection='TIG', scope='claude_dukkan_v1'))
dugum('SABIT62_sol_dolgu_panel', kutu_mesh([((705, 70, 99), (708, 2000, 660))], ms), dict(connection='tel panel, çerçeveye cıvatalı', scope='claude_dukkan_v1'))
dugum('SABIT62_sol_dolgu_ayak', kutu_mesh([((650, 0, 29), (750, 6, 129))], mp), dict(connection='zemine 2 dübel', scope='claude_dukkan_v1'))

mk, ms_, mc = mat_of('ELK_ANA_HAT__ayirici_kirmizi'), mat_of('ELK_ANA_HAT__ayirici_sari'), mat_of('ELK_ANA_HAT__cihaz_koyu')
# ---------------------------------------------------------------- 3: eski ayaklı şalter + ayaklık + zemin üstü rampa
for nm in ('ELK_ANA_HAT__ayirici_kirmizi', 'ELK_ANA_HAT__ayirici_sari', 'ELK_ANA_HAT__cihaz_koyu', 'ELK_ZEMIN_KANALI__paslanmaz'):
    J['nodes'][NI[nm]].pop('mesh', None)
LOG.append('kaldırıldı: eski ayırıcı + kutu + zemin üstü rampa (ELK_ZEMIN_KANALI)')
AYAK = lambda C, lo, hi: (C[:, 0] > 5330) & (C[:, 0] < 5700) & (C[:, 2] > 560) & (C[:, 2] < 1100)
RAMPA = lambda C, lo, hi: (hi[:, 1] < 130) & (lo[:, 0] > 4030) & (C[:, 2] > -720) & (lo[:, 1] > -1)
for nm in ('ELK_ANA_HAT__paslanmaz', 'ELK_ANA_HAT__kablo', 'ELK_ANA_HAT__kablo_veri', 'ELK_ANA_HAT__rakor', 'ELK_ANA_HAT__kanal'):
    n = ucgen_sil(nm, lambda C, lo, hi: AYAK(C, lo, hi) | RAMPA(C, lo, hi))
    LOG.append('  %s: %d üçgen (ayaklık + zemin üstü)' % (nm, n))

n = ucgen_sil('ELK_IC__kanal', lambda C, lo, hi: (C[:, 0] > 5150) & (C[:, 0] < 5300) & (C[:, 2] > 600) & (C[:, 2] < 1100))
LOG.append('  ELK_IC__kanal: %d üçgen (E önünden eski şaltere uzanan kanal)' % n)
# ---------------------------------------------------------------- 4: duvar tipi şalter + gömülü oluk
WX = 6000.0                                                       # sağ duvar iç yüzü (Kemal: makinenin sağına biraz pay)
dugum('DUVAR_SALTER__kutu', kutu_mesh([((WX - 150, 1350, 1350), (WX, 1650, 1550))], mc), dict(bom='Ana hat yük ayırıcı 3P 63 A, kilitlenebilir (EN 60947-3) · duvar tipi muhafaza IP65, 4 dübel', scope='claude_dukkan_v1'))
dugum('DUVAR_SALTER__plaka', kutu_mesh([((WX - 154, 1455, 1405), (WX - 150, 1545, 1495))], ms_), dict(bom='Sarı ön plaka (acil kesme)', scope='claude_dukkan_v1'))
dugum('DUVAR_SALTER__kol', kutu_mesh([((WX - 172, 1490, 1420), (WX - 154, 1510, 1480)), ((WX - 166, 1480, 1440), (WX - 154, 1520, 1460))], mk), dict(bom='Kırmızı döner kol, asma kilitlenebilir (kol yerden 1500)', scope='claude_dukkan_v1'))
mo = mat_of('ELK_ZEMIN__oluk') if 'ELK_ZEMIN__oluk' in NI else mc
mkp = mat_of('ELK_ZEMIN__kapak') if 'ELK_ZEMIN__kapak' in NI else mo
X0 = 4843.0
dugum('ZEMIN_OLUK_SALTER__oluk', kutu_mesh([((X0, -120, 1000), (WX, -117, 1075)), ((X0, -117, 1000), (WX, -2, 1003)), ((X0, -117, 1072), (WX, -2, 1075)),
                                             ((WX - 75, -117, 1000), (WX, -2, 1075))], mo), dict(bom='Gömülü kablo oluğu AISI 304 1,5 (şap içinde) · duvar dibinden mevcut zemin oluğunun ön ucuna', scope='claude_dukkan_v1'))
dugum('ZEMIN_OLUK_SALTER__kapak', kutu_mesh([((X0, -2, 1000), (WX, 0, 1075))], mkp), dict(bom='Oluk kapağı AISI 304 2 mm, zeminle aynı düzlem, sökülebilir', scope='claude_dukkan_v1'))
mg = mat_of('ELK_ZEMIN__kablo_guc') if 'ELK_ZEMIN__kablo_guc' in NI else mk
mv_ = mat_of('ELK_ZEMIN__kablo_veri') if 'ELK_ZEMIN__kablo_veri' in NI else mc
dugum('ZEMIN_OLUK_SALTER__kablo_guc', kutu_mesh([((X0, -80, 1020), (WX - 75, -60, 1040))], mg), dict(bom='Ana besleme 5 × 10 mm² (duvar içinden iner)', scope='claude_dukkan_v1'))
dugum('ZEMIN_OLUK_SALTER__kablo_veri', kutu_mesh([((X0, -80, 1046), (WX - 75, -70, 1056))], mv_), dict(bom='Şalter yardımcı kontak / bilgi kablosu', scope='claude_dukkan_v1'))
LOG.append('eklendi: duvar tipi ana şalter (x %.0f, kol yerden 1500) + gömülü oluk x %.0f–%.0f + kapak + 2 kablo' % (WX, X0, WX))

# ---------------------------------------------------------------- 8 bitlik indeksler → 32 bit (meshopt kodlayıcısı UINT8 indeks kabul etmiyor; değerler aynı)
n8 = 0
for me in J['meshes']:
    for pr in me['primitives']:
        if 'indices' in pr and ACC[pr['indices']]['componentType'] == 5121:
            pr['indices'] = ekle_acc(oku(pr['indices']).reshape(-1).astype(np.uint32), 'IDX'); n8 += 1
LOG.append('UINT8 indeks → UINT32: %d primitive' % n8)
# ---------------------------------------------------------------- yaz
J['buffers'] = [dict(byteLength=len(BIN) + (-len(BIN)) % 4)]
while len(BIN) % 4: BIN.append(0)
jb = json.dumps(J, separators=(',', ':'), ensure_ascii=False).encode(); jb += b' ' * ((-len(jb)) % 4)
with open(go, 'wb') as f:
    f.write(struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack('<II', len(jb), 0x4E4F534A) + jb + struct.pack('<II', len(BIN), 0x004E4942) + bytes(BIN))
for l in LOG: print(l)
print('düğüm', len(J['nodes']), '· mesh', len(J['meshes']))
