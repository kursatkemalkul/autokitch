# A gövdesi küçük BOŞLUK taraması: gövde parçaları + komşu kaide/kapak kutuları arasında 0,2–15 mm aralık (iki eksende örtüşüp üçüncüde açık)
import io, sys, json
src = open("a_govde_yeni.py", encoding="utf-8").read().split("gi, go = sys.argv[1:3]")[0]
G = {}; exec(src, G)
P = {**G["SAC"], **G["CERCEVE"], **G["KAIDE_P"], **G["KAIDE_S"]}
B = {k: v.BoundingBox() for k, v in P.items()}
bul = []
ad = list(B)
for i in range(len(ad)):
    for j in range(i + 1, len(ad)):
        a, b = B[ad[i]], B[ad[j]]
        r = [(a.xmin, a.xmax, b.xmin, b.xmax), (a.ymin, a.ymax, b.ymin, b.ymax), (a.zmin, a.zmax, b.zmin, b.zmax)]
        ort = [min(p[1], p[3]) - max(p[0], p[2]) for p in r]
        for e in range(3):
            diger = [ort[k] for k in range(3) if k != e]
            if min(diger) > 1.0 and -15.0 < ort[e] < -0.2:
                bul.append((ad[i], ad[j], "xyz"[e], round(-ort[e], 2)))
for b in bul: print("BOŞLUK %-28s ↔ %-28s %s ekseninde %.2f mm" % b)
print("toplam", len(bul))
