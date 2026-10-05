"""Run only inside the separately registered main-assembly worktree."""
from pathlib import Path
U=Path(__file__).resolve().parent
s=(U/'hat_montaj_v83.py').read_text(encoding='utf-8-sig')
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:100],s.count(a),n)
    s=s.replace(a,b)
rep('import kutu_cad_v9 as KC','import kutu_cad_v10 as KC')
s=s.replace('kutu_cad_v9.py','kutu_cad_v10.py')
rep('E_BIRIM = [','E_BIRIM = [\n    ("E_KOSE", "4 motorlu köşe katlayıcı + ortak kaldırma: katlama 38 / geri dönüş 60 mm; kinematik prototip", ("kose_takim_", "kose_CNR_")),')
rep('("kapak_", "flap_katlayici_", "kol_")','("kapak_", "flap_", "kol_")')
rep('Devirme parmağı: iç ön paneli kutuya devirir · NEMA 23 + SureGear 10:1','Ön çift duvar: baskı kafası üzerinde 180° katlayıcı, 1:1 kayış, çift yatak, dışa park; kartona pozitif temas')
rep('7 × STP-DRV-4830','12 × STP-DRV-4830; hareket denetleyicisi/I-O seçimi AÇIK')
rep('E_MENTESE = ("KOL", "PARMAK")','E_MENTESE = ("KOL", "PARMAK") + tuple(KC.CORNER)')
rep('        return KC.DUGUM[g][1]','        if g in KC.CORNER: return KC.CORNER[g]["P"]\n        return KC.DUGUM[g][1]')
rep('sh = KC.uygula(sh, W0[g]) if g.startswith("B_") else sh','sh = KC.uygula(sh, W0[g] if g.startswith("B_") else KC.grup_matrisi(g,0))')
rep('            _sh = KC.uygula(_sh, _W0[_p["grup"]])','            _sh = KC.uygula(_sh, _W0[_p["grup"]])\n        else:\n            _sh = KC.uygula(_sh, KC.grup_matrisi(_p["grup"],0))')
rep('te = lambda t: min(19.5, max(0.0, t - T0K))','te = lambda t: min(22.5, max(0.0, t - T0K + KC.V10_DELAY))')
rep('T0K + KC.Z_CATAL[0]','T0K + KC.Z_CATAL[0] - KC.V10_DELAY')
rep('T0K + KC.Z_CATAL[2]','T0K + KC.Z_CATAL[2] - KC.V10_DELAY')
rep('if tK < KC.Z_PIZZA[1]:','if tK < KC.Z_PIZZA[1] - KC.V10_DELAY:')
rep('"KATLAYICI": lambda t: (0.0, KC.katlayici_dy(t), 0.0)', '"KATLAYICI": lambda t: (0.0, KC.katlayici_dy(t), 0.0), "CNR_LIFT": KC.corner_translation, "FRONT_Y": lambda t: (0,KC.front_dy(t),0)',2)
rep('''        elif g == "PARMAK":
            kanal(o["ad"], lambda t: KC.quat("z", KC.parmak_psi(te(t))), "rotation")
            KONTROL.append((o["ad"], lambda t, T_=o["T"]: T_, lambda t: KC.quat("z", KC.parmak_psi(te(t))), o["tonlar"]))''','''        elif g == "PARMAK" or g in KC.CORNER:
            if g == "PARMAK":
                fT=lambda t,T_=o["T"]: (T_[0],T_[1]+KC.front_dy(te(t))*MM,T_[2])
                fR=lambda t: KC.quat("z",KC.parmak_psi(te(t)))
            else:
                fT=lambda t,T_=o["T"]: tuple(T_[j]+KC.corner_translation(te(t))[j]*MM for j in range(3))
                fR=lambda t,g_=g: KC.corner_quat(g_,te(t))
            kanal(o["ad"],fT)
            kanal(o["ad"],fR,"rotation")
            KONTROL.append((o["ad"],fT,fR,o["tonlar"]))''')
rep('''        elif g == "PARMAK":
            ANIM.append((o["ad"], _TT, [KC.quat("z", KC.parmak_psi(_te(t))) for t in _TT], "rotation"))''','''        elif g == "PARMAK":
            ANIM.append((o["ad"], _TT, [KC.quat("z", KC.parmak_psi(_te(t))) for t in _TT], "rotation"))
            T0=o["T"]
            ANIM.append((o["ad"],_TT,[(T0[0],T0[1]+KC.front_dy(_te(t))*MM,T0[2]) for t in _TT]))
        elif g in KC.CORNER:
            T0=o["T"]
            ANIM.append((o["ad"],_TT,[KC.corner_quat(g,_te(t)) for t in _TT],"rotation"))
            ANIM.append((o["ad"],_TT,[tuple(T0[j]+KC.corner_translation(_te(t))[j]*MM for j in range(3)) for t in _TT]))''')
s=s.replace('hat_v83','hat_v84').replace('hat_montaj_v83.py','hat_montaj_v84.py')
s=s.replace('pafta="HAT v83', 'pafta="HAT v84: E v10 TAHRIKLI KOSE / ON DIL / KILAVUZLU KAPAK KATLAMA; KINEMATIK PROTOTIP, FIZIKSEL KARTON TESTI BEKLENIYOR. v83')
s=s.replace('"corner-tab folding actuator missing",','"E v10: four motor-driven corner fingers, driven front tucker and guided lid former; physical folding trials pending",')
s=s.replace('geometry="E v9: internal drive, aligned supports, flush side door"','geometry="E v10: positive-drive corner/front/lid tools; internal drive, aligned supports, flush side door"')
s=s.replace('regression="288 solids; changed parts0, machine201 samples0, box-machine46 samples0, pizza25 samples0; elevator8 heights0"','regression="v10 changed-tool solid scan and contact checks stored in kutu_v10_check.py; v9 elevator/frame unchanged"')
compile(s,'hat_montaj_v84.py','exec')
(U/'hat_montaj_v84.py').write_text(s,encoding='utf-8')
print('v84 main generated from latest v83, station E only')
