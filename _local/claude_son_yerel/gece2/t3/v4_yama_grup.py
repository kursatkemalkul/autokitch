import io
f = 't3_parca_v4.py'
s = io.open(f, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


# X ekseni parçalı: motor + braketi (sağ uç, z ≤ −397) ayrı gelir (arkadan, teknik bölmenin sağındaki köşeden)
rep("grup('x_ekseni', sec(lambda o: kod(o) == 'TOPPING/Tabla' and id(o) not in ATANAN), 'mekanizma', 'mek', 'X ekseni ünitesi (ray tabanı + 2 lineer ray + araba + bantlı tabla + motor + kayış · TEK ÜRÜN, hazır)')",
    "grup('x_motor', sec(lambda o: kod(o) == 'TOPPING/Tabla' and id(o) not in ATANAN and o['lo'][0] > 2330 and o['hi'][2] < -385), 'motor', 'mek', 'X ekseni motoru + braketi + kasnak (ünitenin ayrı gelen parçası)')\n"
    "grup('x_ekseni', sec(lambda o: kod(o) == 'TOPPING/Tabla' and id(o) not in ATANAN), 'mekanizma', 'mek', 'X ekseni (ray tabanı + 2 lineer ray + araba + bantlı tabla + kayış · hazır)')")
# kondenser kanalı: taban üstündeki alt braket (dış tabanda, 2 FHP) ayrı ve önce
rep("grup('kondenser_kanali', [o for o in S17 if (o['lo'][0] > 2010",
    "grup('kondenser_braketi', [o for o in S17 if o['dug'] == 'TOPPING_MODUL__sac' and o['lo'][1] < 895 and 2090 < o['lo'][0] < 2110], 'mekanizma', 'mek', 'Kondenser kanalı alt braketi (dış tabanın FHP-M5 saplamalarına)')\n"
    "grup('kondenser_kanali', [o for o in S17 if id(o) not in ATANAN and (o['lo'][0] > 2010")
# kaset: çıkış ağzı (kovan içi, sabit) + mandal (raf içine gömülü kilit) gövdeye ait · kaset rayından sürülür
rep("    grup('kaset_' + ad + '_cikis', [o for o in K_ if id(o) not in ATANAN and o['hi'][1] < 1150], 'mekanizma', 'mek', '%s kaseti çıkış ağzı (raf kovanından)' % ad.capitalize())",
    "    grup('kaset_' + ad + '_mandal', [o for o in K_ if id(o) not in ATANAN and o['hi'][1] < 1161 and o['hi'][0] < (1980 if ad == 'kasar' else 2312)], 'koyu', 'mek', '%s kaseti kilit mandalı (POM yuva + yaylı dil · rafa gömülü)' % ad.capitalize())\n"
    "    grup('kaset_' + ad + '_conta', [o for o in K_ if id(o) not in ATANAN and o['dug'] == 'TOPPING_MODUL__conta' and o['hi'][1] < 1153], 'yapistirici', 'mek', '%s kovanı raf contası' % ad.capitalize())\n"
    "    grup('kaset_' + ad + '_cikis', [o for o in K_ if id(o) not in ATANAN and o['hi'][1] < 1150], 'mekanizma', 'mek', '%s çıkış ağzı (kovanın içinde sabit · alttan takılır)' % ad.capitalize())")
# UNO sos / harç: çıkış borusu + yayıcı (y < 1182, kelepçe altı) ayrı, alttan kovandan · gövde önden, kelepçe ile bağlanır
rep("    alt = [o for o in U if id(o) not in ATANAN and o['hi'][1] < 1152.5] if ad == 'harc' else []",
    "    alt = [o for o in U if id(o) not in ATANAN and o['hi'][1] < 1182.5 and o['dug'] != 'TOPPING_MODUL__conta'] if ad in ('harc', 'sos') else []\n"
    "    if ad in ('harc', 'sos'): grup('uno_%s_conta' % ad, [o for o in U if id(o) not in ATANAN and o['dug'] == 'TOPPING_MODUL__conta' and o['hi'][1] < 1153], 'yapistirici', 'mek', 'UNO %s kovanı raf contası' % ad)")
rep("    if alt: grup('uno_%s_cikis' % ad, alt, 'mekanizma', 'mek', 'UNO %s · çıkış ağzı + yayıcı (raf kovanından aşağı)' % ad)",
    "    if alt: grup('uno_%s_cikis' % ad, alt, 'mekanizma', 'mek', 'UNO %s çıkış borusu + yayıcı (alttan kovana · üstte kelepçe)' % ad)")
io.open(f, 'w', encoding='utf-8').write(s)
print('ok')
