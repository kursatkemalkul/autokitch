"""Rebase the prepared K change onto the latest READY main, never on unfinished work."""
from pathlib import Path
import re,sys
def build(source):
    s=source
    def rep(a,b,n=1):
        nonlocal s
        assert s.count(a)==n,(a,s.count(a),n)
        s=s.replace(a,b)
    def block(a,b,replacement):
        nonlocal s
        i=s.index(a);j=s.index(b,i);s=s[:i]+replacement+s[j:]
    rep('W_E = 830.0','W_K = 400.0\nX_E = X_K + W_K\nW_E = 830.0')
    rep('HAT_W - X_S','QR.X0 + QR.W - X_S')
    s=s.replace('kesme_cad_v6','kesme_cad_v7')
    rep('MODÜL K · KESME + SPREY (+ taban: bulaşık)','MODÜL K · KESME + SPREY · 400 mm prototip')
    rep('İtici: igus ZLW-1040 eksen + NEMA 23 · SMC MGPM20-60 kaldırma · kol + POM yüz (E\'ye 110 mm girer)','K400: iki düz kısa eksen; X 250 / Z 350, arkaya taşmaz. Katalog zarfları; kuvvet ve gıda testi bekleniyor.')
    block('# ---- v57 · BULAŞIK MAKİNESİ K ALTINDA', '# --- E · KUTU KATLAMA (TEK PARCA', '# K400: Kemal onayıyla bulaşık ana montajdan kaldırıldı.\nBM.PARCALAR.clear()\nBM_KOD = {}\n\n')
    s='\n'.join(line for line in s.split('\n') if not line.lstrip().startswith(('("bulasik x:', '("bulasik y:', '("bulasik z:')))
    rep('QR.X0 + QR.W, HAT_W, 5430.0','QR.X0 + QR.W, 5430.0')
    rep('S modulu sag ucu: QR.X0 + QR.W = HAT_W = 5430','S modulu sabit; QR sag ucu 5430, daralan hat sag ucu 5230')
    # Explicit, stronger replacement for checks whose subject was removed.
    block('    # ---- v57 · BULAŞIK MAKİNESİ K ALTINDA','    # ---- v54 · HAVA ANA HATTI', '''    _KSP = [("K:" + p["ad"], _tek(p["wp"]).translate(cq.Vector(X_K, 0, 0))) for p in KS.PARCALAR if p["grup"] not in K_HARIC_GRUP]
    assert not BM.PARCALAR and not any(b["durum"] == "GERCEK_BULASIK" for b in B)
    assert W_K == KS.W == 400 and X_E == X_K + W_K and HAT_W == 5230
    print("K400 + BULASIK YOK + HAT 5230: PASS")
''')
    block('    _kx, _ky, _kz = BM.kapi_acik_zarf()', '    print("hat_v', '')
    rep('("KESICI", "ITICI_ARABA", "ITICI_KOL")','("KESICI", "ITICI_ARABA", "ITICI_CAPRAZ", "ITICI_KOL", "ITICI_YUZ")',2)
    rep('te = lambda t: min(22.5, max(0.0, t - T0K + KC.V10_DELAY))','te = lambda t: KS.e_time(t - T0K)')
    rep('if tK < KC.Z_PIZZA[1] - KC.V10_DELAY:', 'if tK < 13.2:')
    rep('def iki_lahmacun(A, Z, TE_H=10.4):','def iki_lahmacun(A, Z, TE_H=13.3):')
    rep('return t % KC.DONGU','return KS.e_time(t % (KS.DONGU + 3.0) - 3.0)')
    rep('KS.grup_trs(g_, _te(t))','KS.grup_trs(g_, max(0.0, t % (KS.DONGU + 3.0) - 3.0))')
    # Subsequent QR moves shift by the exact E clock delay after K return.
    for x in (16.8,17.5,18.6,19.9,20.6,21.3,20.5,24.5,25.5):
        s=s.replace('T0K + '+str(x),'T0K + '+str(round(x+3.4,1)))
    rep('T0K + KC.Z_CATAL[2] - KC.V10_DELAY','T0K + KC.Z_CATAL[2] + 0.4')
    rep('T0K + KC.Z_CATAL[0] - KC.V10_DELAY','T0K + KC.Z_CATAL[0] + 0.4')
    # Cosmetic labels in model metadata only, no information-page rewrites.
    rep('Bant ürünü 200 mm taşır; itici ürünün üstünden geri gelip arkasına iner ve ürünü kutuya sürer.','K bandı 220 mm ön besler; kısa düz itici yandan arkaya gelir ve 240 mm kutuya iter.')
    rep('İtici ürünü katlanmış kutuya sürer (1,6 s);','İtici ürünü katlanmış kutuya sürer (2,5 s);')
    s=re.sub(r'hat_v(?:85|86)(?!\d)','hat_v87',s)
    s=s.replace('pafta="HAT v86:', 'pafta="HAT v87: K400 KISA ITICI + BULASIK YOK + HAT5230; VANTUZLU E11 KORUNDU. KINEMATIK PROTOTIP. v86:')
    compile(s,'hat_montaj_v87.py','exec')
    return s
if __name__=='__main__':
    src,dst=map(Path,sys.argv[1:])
    dst.write_text(build(src.read_text(encoding='utf-8-sig')),encoding='utf-8')
