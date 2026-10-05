import io
f = 't3_montaj_v4.py'
L = io.open(f, encoding='utf-8').read().split('\n')
def bul(on):
    k = [i for i, l in enumerate(L) if l.startswith(on)]
    assert len(k) == 1, (on, k); return k[0]
# X: kamera + x_ekseni satırlarını kuru bölmeden çıkar, X ekseni adımına geri koy; motor perdelerden ÖNCE (yukarıdan, serbest)
i = bul("kamera_genel(['x_ekseni', 'x_motor']"); del L[i]
i = bul("t = koy('x_ekseni', AD((-1700, 0, 0), lift=(5, 10))"); xe = L.pop(i)
i = bul("t = koy('x_motor'"); xm = L.pop(i)
j = bul("for a in ('ayirma_perdesi_cep_sol', 'teknik_on_perde', 'teknik_sag_perde'):")
L.insert(j, xm)
j = bul("for a in sorted(a for a in P if a.startswith('x_sensor_braket')):")
L[j + 2:j + 2] = ["kamera_genel(['x_ekseni'], yon=(0.3, 0.45, 0.9), olcek=0.75)",
          "t = koy('x_ekseni', AD((-1700, 0, 0), ON9, lift=(5, 10)), 'X ekseni (raylar + araba + bantlı tabla) → A tarafındaki tabla geçiş ağzından kayar, sağ uçta motora bağlanır')"]
# soğutma hatları (bakır + yoğuşma) evaporatörlerden SONRA
i = bul("# ---- 12 SOĞUTMA"); j = bul("# ---- 13 HAVA")
blok = L[i:j]; del L[i:j]
k = bul("t = sira_tak(EAV, t, 30.0, 0.45, 0.2)")
L[k + 1:k + 1] = blok
s = '\n'.join(L)
s = s.replace("HARIC_PLAN.add(('on_cerceve_430', 'dis_tavan'))",
              "HARIC_PLAN.add(('x_ekseni', 'x_motor')); HARIC_NEDEN[('x_ekseni', 'x_motor')] = 'ray tabanı ucu motor braketinin yuvasına geçer (bağlantı)'\n"
              "HARIC_PLAN.add(('kanal_gecis_kapagi', 'kondenser_kanali')); HARIC_NEDEN[('kanal_gecis_kapagi', 'kondenser_kanali')] = 'kapak yarığı boruya 0,5 mm boşlukla sürülür'\n"
              "HARIC_PLAN.add(('on_cerceve_430', 'dis_tavan'))")
s = s.replace("t = koy('x_motor', AD(UST6, lift=(5, 10)), 'X ekseni motoru + braketi → yukarıdan sağ uca, ray tabanına bağlanır')",
              "t = koy('x_motor', AD(UST6, lift=(5, 10)), 'X ekseni motoru + braketi → yukarıdan sağ arka köşeye (X ekseni sonra A tarafından gelip bağlanır)')")
s = s.replace("X ekseni parçalı girer: raylar + araba + tabla A tarafındaki tabla ağzından kayar, motoru yukarıdan sağ uca iner.", "X ekseninin motoru yukarıdan sağ arka köşeye iner (ünite parçalı gelir).")
s = s.replace("'X ekseni kuru bölme adımında parçalı girmişti (raylar + araba + tabla A tarafından, motor yukarıdan). Sensör braketleri alttan.", "'X ekseni parçalı: motoru kuru bölme adımında konmuştu; raylar + araba + bantlı tabla A tarafındaki tabla ağzından kayar ve motora bağlanır. Sensör braketleri alttan.")
io.open(f, 'w', encoding='utf-8').write(s)
print('ok')
