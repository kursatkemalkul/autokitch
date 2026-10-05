import io
f = 't3_montaj_v4.py'
s = io.open(f, encoding='utf-8').read()
L = s.split('\n')
def bul(on):
    k = [i for i, l in enumerate(L) if l.startswith(on)]
    assert len(k) == 1, (on, k); return k[0]
# --- X ekseni + motor: kuru bölme adımının başına (dış yan sol ve kovan çıkışları henüz yok) · motor X ekseninden sonra yukarıdan
i = bul("t = koy('x_motor'"); xm = L.pop(i)
i = bul("kamera_genel(['x_ekseni']"); L.pop(i)
i = bul("t = koy('x_ekseni', AD((-1700"); xe = L.pop(i)
j = bul("t = koy('sogutma_cebi'")
L[j:j] = ["kamera_genel(['x_ekseni', 'x_motor'], yon=(0.35, 0.5, 0.85), olcek=0.6)",
          "t = koy('x_ekseni', AD((-1700, 0, 0), lift=(5, 10)), 'X ekseni (raylar + araba + bantlı tabla) → A tarafındaki tabla geçiş ağzından kayarak (ünite parçalı gelir)')",
          "t = koy('x_motor', AD(UST6, lift=(5, 10)), 'X ekseni motoru + braketi → yukarıdan sağ uca, ray tabanına bağlanır')"]
# --- kanal kapağı: yukarıdan, borunun sağında iner, sola sürülür
i = bul("t = koy('kanal_gecis_kapagi'")
L[i] = "t = koy('kanal_gecis_kapagi', [YOL((0, 300, 0), (150, 0, 0)), YOL((0, 300, 0), (160, 0, 0)), YOL((0, 300, 0), (180, 0, 0))], 'Kanal geçiş kapağı → borunun sağında iner, yarığıyla sola sürülür')"
# --- evaporatörler (ayaklarıyla): hava / valf / elektrik iç parçalarından SONRA (13. adımın sonuna)
i = bul("for nm, ay in (('evaporator_L'"); ev = L[i:i + 2]; del L[i:i + 2]
i = bul("EAV = sorted("); ev2 = L[i:i + 3]; del L[i:i + 3]
i = bul("t = koy('j1_panel'")
L[i + 1:i + 1] = ["kamera_genel(['evaporator_L', 'evaporator_R'], yon=(0.35, 0.45, -0.85), olcek=0.8)"] + ev + ev2
# --- yan / tavan / arka iç sac: PU levha + iç sac birlikte (levha iç sacın arkasına yapıştırılmış sandviç) · pullar iç sacla
i = bul("for pu in ('pu_levha_sol', 'pu_levha_sag', 'pu_levha_tavan'):")
j = bul("yakin(merkez(PER('arka_sol')[0])")
L[i:j] = '''PUL = lambda pre: sorted(a for a in P if a.startswith('astar_percin_' + pre) and a.endswith('_pul'))
PER = lambda pre: sorted(a for a in P if a.startswith('astar_percin_' + pre) and not a.endswith('_pul'))
for tr_ in ('sol', 'sag', 'tavan'):
    kamera_genel(['pu_levha_' + tr_], yon=(0.25, 0.4, 0.9), olcek=0.7)
    buyu('yapistirici_' + tr_, t, 0.6); olay(t, 'Yapıştırıcı (YEŞİL) → dış sacın iç yüzüne'); t += 0.8
    ek = PUL('tavan_') if tr_ == 'tavan' else []
    t = koy(['astar_' + tr_, 'pu_levha_' + tr_] + ek, AD(ON9, lift=(2, 5, -2, -4)), '%s iç sacı + arkasına yapıştırılmış PU levha (bükümlü kenarlar komşu levhaların yivine%s) → önden' % ({'sol': 'Sol', 'sag': 'Sağ', 'tavan': 'Tavan'}[tr_], ', POM pullar üstte' if ek else ''))
kamera_genel(['astar_arka'], yon=(0.25, 0.3, 0.9), olcek=0.7)
t = koy(['astar_arka'] + PUL('arka_'), AD(ON9), 'Arka iç sac (arka yüzünde POM pullar) → en son önden, kenar flanşlarının önüne')'''.split('\n')
s = '\n'.join(L)
# perçinler raftan sonra (raf yukarıdan inerken baş takılmasın)
a = '''yakin(merkez(PER('arka_sol')[0]), 0.35, yon=(0.6, 0.3, 0.75), tt=t)
t = sira_tak(PER('arka_') + PER('tavan_'), t, 25.0, 0.35, 0.05)'''
assert s.count(a) == 1
b_ = s[s.index(a):]; b_ = b_[:b_.index('\n', b_.index("olay(t - 1.0, 'Kör perçin")) + 1]
s = s.replace(b_, '')
a2 = "for a in sorted(a for a in P if a.endswith('_conta') and a.startswith(('kaset_', 'uno_'))):"
assert s.count(a2) == 1
s = s.replace(a2, b_ + a2)
# harç UNO: tavana 41 mm → kaldırma 37–40
s = s.replace("t = koy('uno_%s_on' % ad, AD(ON9, lift=(2, 5, 10, 20)),", "t = koy('uno_%s_on' % ad, AD(ON9, lift=(37, 38, 40, 45, 60), yan=()),")
# beyanlı temaslar
a3 = "KAY = lambda pre:"
s = s.replace(a3, '''for ad_ in ('kasar', 'sucuk'):
    for o_ in ('kaset_%s_mandal' % ad_, 'kaset_%s_conta' % ad_):
        HARIC_PLAN.add(('kaset_' + ad_, o_)); HARIC_NEDEN[('kaset_' + ad_, o_)] = 'yaylı kilit mandalı / kovan contası: kaset dili geçerken esner (sıfır boşluk teması)'
HARIC_PLAN.add(('on_cerceve_430', 'dis_tavan')); HARIC_NEDEN[('on_cerceve_430', 'dis_tavan')] = 'çerçeve üst kenarı dış tavanın altına sıfır boşlukla kayar (yüzey teması)'
''' + a3, 1)
io.open(f, 'w', encoding='utf-8').write(s)
print('ok')
