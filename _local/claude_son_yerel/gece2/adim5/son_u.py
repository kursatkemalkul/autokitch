"""U son düzeltme denetimi: omega 0,3 → 0,02 (havada) · zarf (istasyon M8 / U_F↔U_KE bağlantı elemanları HARİÇ — tasarım gereği komşuya geçer) ·
taş yünü görünürlüğü (yüz normali boyunca 3 mm içinde katı var mı) · GLB + CSV yeniden · doğru çakışma sonucu önceki tam koşudan (run_U_5) korunur + omega için OCC yeniden"""
import os, sys, json, re, time
B = os.path.dirname(os.path.abspath(__file__))
os.environ["ADIM5"] = B; os.environ["AUTOKITCH_SAC_STANDART"] = os.path.abspath(os.path.join(B, "..", "..", "sac_standart"))
sys.path.insert(0, B); sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import numpy as np
import sac_denetim_5b as DEN, h3_sac_v1 as S, h3_govde_ortak_v1 as GO, h3_u_sac_v1 as M
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_IN, TopAbs_ON
DEN.LOGF = open(os.path.join(B, "U_son_log.txt"), "w", encoding="utf-8"); log = DEN.log
D = json.load(open(os.path.join(B, "U_denetim.json"), encoding="utf-8"))
GG = M.kur(log); PAR = []; RR = {}
for k, g in GG.items():
    DEN.acinim_bulanik(g)
    R = GO.denetle(g, acinim_klasoru=os.path.join(B, "acinim_U"), abkant=True, supurme=False, log=lambda *a: None); RR[k] = R
    PAR += M.govde_parcalari(g)
    D["birimler"][g.birim].update(ozet=R["ozet"], sac_ozet=R["sac_ozet"], govde_govde_occ=R["cakisma"])
    log("%s: %s" % (g.birim, json.dumps(R["ozet"], ensure_ascii=False)))
gw = [(p["ad"], DEN.sekil(p), p.get("meta", {})) for p in PAR]
D["birimler_arasi_occ"] = GO.cakisma(gw, gw, esik=0.5, ayni=True, izin=GO.ic_ice_izni); log("U OCC çakışma: %s" % D["birimler_arasi_occ"])
# omega ↔ ortam (yalnız omega değişti): bileşik GLB'den tavan bölgesi — OCC ile tavan + iç parçalar
S.glb_yaz(os.path.join(B, "U_sac_v1.glb"), PAR)
rows = []
for k, g in GG.items():
    tmp = os.path.join(B, "_U_%s.csv" % k); DEN.parca_csv(g, RR[k], tmp, None)
    L_ = open(tmp, encoding="utf-8-sig").read().splitlines()
    if not rows: rows.append("birim;" + L_[0])
    rows += ["%s;%s" % (g.birim, l) for l in L_[1:]]; os.remove(tmp)
open(os.path.join(B, "U_parca.csv"), "w", encoding="utf-8-sig").write("\n".join(rows) + "\n")
D["havada"] = DEN.havada(PAR); log("HAVADA U: %s" % D["havada"])
ARAYUZ_GECEN = re.compile(r"^govde_(f_m8_firin|ke_m8_e|f_ke_m8)_")
REF = {"U_F_GOVDE": [2500.0, 4000.0, 1862.0, 2200.0, -830.0, 59.0], "U_KE_GOVDE": [4000.0, 5230.0, 1862.0, 2200.0, -830.0, 59.0], "F_UST_KABIN": [2500.0, 4000.0, 788.0, 1862.0, -830.0, 59.0]}
for k, g in GG.items():
    P = [p for p in PAR if p["birim"] == g.birim and not ARAYUZ_GECEN.search(p["ad"])]; z = DEN.zarf(P); ref = REF[g.birim]
    f = [round(a - b, 2) for a, b in zip(z, ref)]
    D["zarf"][g.birim] = dict(zarf=z, ref=ref, fark=f, gecti=all(abs(x) <= 0.5 for x in f), not_="istasyon ↔ U M8 vidaları ve U_F ↔ U_KE cıvataları tasarım gereği komşuya geçer (hariç)")
    log("ZARF %s: %s fark %s → %s" % (g.birim, z, f, "GEÇTİ" if D["zarf"][g.birim]["gecti"] else "KALDI"))
yal = [p for p in PAR if p.get("tur") == "yalitim"]; ds = [(p["ad"], DEN.sekil(p)) for p in PAR if p.get("tur") != "yalitim"]
out = []
for p in yal:
    b = DEN.sekil(p).BoundingBox(); lo = np.array([b.xmin, b.ymin, b.zmin]); hi = np.array([b.xmax, b.ymax, b.zmax]); top = acik = 0; orn = []
    for ax in range(3):
        o = [i for i in range(3) if i != ax]
        g0 = np.arange(lo[o[0]] + 1.0, hi[o[0]] - 0.5, 40.0 if hi[o[0]] - lo[o[0]] > 40 else 4.0)
        g1 = np.arange(lo[o[1]] + 1.0, hi[o[1]] - 0.5, 40.0 if hi[o[1]] - lo[o[1]] > 40 else 4.0)
        for sg, v in ((-1, lo[ax]), (1, hi[ax])):
            for a in g0:
                for c in g1:
                    q0 = np.zeros(3); q0[ax] = v - sg * 0.25; q0[o[0]] = a; q0[o[1]] = c
                    if BRepClass3d_SolidClassifier(DEN.sekil(p).wrapped, gp_Pnt(*map(float, q0)), 1e-6).State() != TopAbs_IN: continue   # orada yün yok (kesik)
                    top += 1; ok = False
                    for dd in (0.25, 0.75, 1.5, 2.25, 3.0):
                        q = np.zeros(3); q[ax] = v + sg * dd; q[o[0]] = a; q[o[1]] = c
                        for ad, s in ds:
                            bb = s.BoundingBox()
                            if not (bb.xmin - 0.1 <= q[0] <= bb.xmax + 0.1 and bb.ymin - 0.1 <= q[1] <= bb.ymax + 0.1 and bb.zmin - 0.1 <= q[2] <= bb.zmax + 0.1): continue
                            if BRepClass3d_SolidClassifier(s.wrapped, gp_Pnt(*map(float, q)), 1e-6).State() in (TopAbs_IN, TopAbs_ON): ok = True; break
                        if ok: break
                    if not ok:
                        acik += 1
                        if len(orn) < 6: orn.append(np.round(q, 1).tolist())
    out.append((p["ad"], top, acik, orn))
D["yalitim_gorunur"] = out; D["yalitim_yontem"] = "taş yünü bloğunun 6 dış yüzünde 40 mm ızgara · yüz normali boyunca 0,25–3 mm içinde başka gövde katısı (kılıf / taban levhası / profil / kovan) var mı"
log("YALITIM (ad, nokta, açık, örnek): %s" % out)
json.dump(D, open(os.path.join(B, "U_denetim.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
log("U SON BİTTİ")
DEN.LOGF.close(); sys.stdout.flush(); os._exit(0)
