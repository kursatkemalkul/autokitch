# -*- coding: utf-8 -*-
L = open("teknik_h26.py", encoding="utf-8").read().split("\n")
out = []
i = 0
while i < len(L):
    ln = L[i]
    if ln.startswith("KOL = ["):
        # KOL bloğunu (4 satır) yenisiyle değiştir
        while not L[i].rstrip().endswith("])]"):
            i += 1
        out.append('KOL = [("K1", 798.5, 1418.5, S5, ["lahmacun"] * 5), ("K2", 1453.5, 2073.5, S5, ["lahmacun"] * 5),')
        out.append('       ("K3", 2108.5, 2728.5, [126, 296.5, 404.5], ["pide", "pide"]),')
        out.append('       ("K5", 2763.5, 3383.5, S4, ["pide", "pide", "pide", "içecek"]),')
        out.append('       ("K6", 3418.5, 4038.5, [126, 296.5, 460, 785], ["pide", "içecek", "içecek"]),')
        out.append('       ("Ka", 4073.5, 4203.5, [126, 296.5, 404.5, 567.5, 785], ["pide 6", "pide 6", "tatlı 6", "tatlı 6"]),')
        out.append('       ("Kb", 4208.5, 4338.5, [126, 330, 785], ["sucuk\\n2 gün", "kaşar\\n2 gün"])]')
        i += 1
        continue
    if ln.startswith("ax.plot([XF1, XF1], [Y_PL, Y_DUZ]"):
        out.append(ln)
        out.append('kutu(2111.5, 2725.5, 407.5, 785, fc="#e9ecef", ec=R, lw=1.0, z=4, hatch="xx")')
        out.append('kutu(2111.5, 2725.5, 407.5, 437.5, fc="#fff3c4", ec=K, lw=0.6, z=5)')
        out.append('kutu(2120, 2470, 450, 757, fc="#c9d8e8", ec=K, lw=0.9, z=6); yaz(2295, 603, "dolap soğutma grubu\\nSecop NLE8.8CN\\n(sıcak bölme, önde ızgara)", 7, K)')
        out.append('kutu(2490, 2715, 450, 660, fc="#dfe3e8", ec=K, lw=0.9, z=6); yaz(2602, 555, "B panosu", 7, K)')
        out.append('yaz(2418, 422, "PU 30", 6, K)')
        out.append('kutu(4338.5, XK1, Y_PL, Y_DUZ, fc="#fff3c4", ec=K, lw=0.6, z=4)')
        i += 1
        continue
    if ln.startswith("kutu(3600, 3980, 1348, 1838"):
        out.append('kutu(3330, 3710, 1348, 1838, fc="#c9d8e8", ec=R, lw=1.0, z=3); yaz(3520, 1600, "kompresör\\n(sola)", 8, R)')
        out.append('kutu(3720, 3985, 1348, 1420, fc="#dfe3e8", ec=R, lw=0.8, z=3); kutu(3735, 3970, 1420, 1790, fc="#f3e3b3", ec=R, lw=1.0, z=3)')
        out.append('yaz(3852, 1605, "yağ\\ntenekesi\\n18 L", 8, R); yaz(3852, 1384, "tartı", 6.5, K)')
        out.append('ax.plot([3970, 3995, 3995, 4040, 4040], [1500, 1500, 1200, 1200, 1170], color=R, lw=1.6, ls="--", zorder=8); yaz(4010, 1250, "yağ hattı", 6.5, R, ha="left")')
        i += 1
        continue
    if ln.startswith('yaz(4218, 820, "teneke'):
        i += 1
        continue
    if ln.startswith("kutu(4410, 5220, 130, 515"):
        out.append('kutu(4440, 4640, 126, 460, fc="#fff5f5", ec=R, lw=1.2, z=3); yaz(4540, 293, "robot\\nçöpü 15 L", 7.5, R)')
        out.append('yaz(4930, 300, "(soğutma grubu buradan çıktı)", 7, G)')
        i += 1
        continue
    out.append(ln.replace("HAT v2.6 ÖNERİ", "HAT v2.7 ÖNERİ").replace(
        "kaşar / sucuk yedeği + teneke K altında · çöp yok",
        "soğutma grubu K3'ün üstünde · teneke fırın üstünde sağda · K altında dar çekmeceler · çöp E altında"))
    i += 1
open("teknik_h27.py", "w", encoding="utf-8").write("\n".join(out))
print("ok")
