# -*- coding: utf-8 -*-
"""hat_montaj_v74 → hat_montaj_v75 (29 Eyl 2026) — Kemal: "dönen tabla çapraz duruyor, toppingden sonra banta yaklaşırken".
Son istasyondan sonra kaset, o istasyonun yerinde (dönüş süpürmesi denetlenmiş konum) bir sonraki tam tura (360° katı) döner → burun +x, yükleme bandına düz gelir.
Hızlar değişmedi (tabla dönüş motoru tork sorunu Kemal'e soruldu). Çıktılar hat_v75."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v74.py"), encoding="utf-8").read()
NL = chr(10)
def degis(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:100]); s = s.replace(a, b)
degis('pafta="HAT v74 (29 Eyl) ·', 'pafta="HAT v75 (29 Eyl) · KASET AKTARMAYA DUZ GELIR (son istasyonda tam tura hizalanir) · v74:')
degis('print("ALCAK HAT SOZLESMESI (v74 ·', 'print("ALCAK HAT SOZLESMESI (v75 ·')
for a_ in ("hat_v74.glb", "hat_v74.usdz", '"hat_v74"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v74", "v75"))
degis('    t = X.git(t, t + gecis(X.son, TH2.X_AKTARMA), TH2.X_AKTARMA)',
      '    _kalan = (-TH.son) % 360.0                                                              # v75: kaset burnu +x (360° katı) — son istasyonun yerinde hizalanır' + NL +
      '    if 0.5 < _kalan < 359.5:' + NL +
      '        _dt = _kalan / (6.0 * TH2.RPM_NOKTA) + TH2.RAMPA_SN' + NL +
      '        TH.git(t, t + _dt, TH.son + _kalan, "ss"); t += _dt' + NL +
      '    else:' + NL +
      '        TH.git(t, t + 0.01, round(TH.son / 360.0) * 360.0, "l"); t += 0.01' + NL +
      '    t = X.git(t, t + gecis(X.son, TH2.X_AKTARMA), TH2.X_AKTARMA)')
s = s.replace('"""', '"""hat_montaj_v75 (29 Eyl 2026): kaset aktarmaya düz gelir — yap_hat_montaj_v75.py.\n', 1)
compile(s, "hat_montaj_v75.py", "exec")
io.open(os.path.join(U, "hat_montaj_v75.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v75.py yazildi")
