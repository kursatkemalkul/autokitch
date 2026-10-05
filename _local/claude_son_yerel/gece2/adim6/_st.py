s=open('g6_montaj.py',encoding='utf-8').read()
h='''def sac_tamam(t):
    olay(t, '%s üretim sacı gövdesi tamam — şimdi diğer parçalar' % IST)
    kam(t, None); t += 2.2
    ADIM[-1]['t1'] = round(t, 3)
    return t


def seq_A():'''
s=s.replace("def seq_A():",h,1)
s=s.replace("    # 7 açıcı\n    t7 = t","    t = sac_tamam(t)\n    t7 = t",1)
s=s.replace("    rest = R(r'^M__')\n    raylar","    t = sac_tamam(t)\n    rest = R(r'^M__')\n    raylar",1)
s=s.replace("    no = 7\n    rest = R(r'^M__')\n    t, no = diger(t, no, [a for a in rest if sinif(a) in ('mek', 'elektrik'","    t = sac_tamam(t)\n    no = 7\n    rest = R(r'^M__')\n    t, no = diger(t, no, [a for a in rest if sinif(a) in ('mek', 'elektrik'",1)
s=s.replace("    no = 7\n    t, no = diger(t, no, R(r'^M__'), \"Ana pano","    t = sac_tamam(t)\n    no = 7\n    t, no = diger(t, no, R(r'^M__'), \"Ana pano",1)
print(s.count('sac_tamam(t)'))
open('g6_montaj.py','w',encoding='utf-8').write(s)
