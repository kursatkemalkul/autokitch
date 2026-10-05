# -*- coding: utf-8 -*-
"""hat_montaj_v72 → hat_montaj_v73 (29 Eyl 2026) — Kemal: "en alttaki ayakları sil, havada dursun, etekleri de sil".
B / K / E ayakları (ayak_*) ve ön süpürgelikler (onyuz_plint*) modelden çıkar; makine alt şaselerin üstünde havada durur. Başka değişiklik yok. Çıktılar hat_v73."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v72.py"), encoding="utf-8").read()
NL = chr(10)
def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120])
    s = s.replace(a, b)
degis('pafta="HAT v72 (29 Eyl) ·', 'pafta="HAT v73 (29 Eyl) · AYAKLAR + ETEKLER YOK (Kemal: havada dursun) · v72:')
degis('print("ALCAK HAT SOZLESMESI (v72 ·', 'print("ALCAK HAT SOZLESMESI (v73 ·')
for a_ in ("hat_v72.glb", "hat_v72.usdz", '"hat_v72"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v72", "v73"))
degis('print("v72 · BAGIMSIZ ISTASYONLAR:',
      '_SIL73 = lambda p_: p_["ad"].startswith(("ayak_", "onyuz_plint"))                        # v73: ayaklar + ön süpürgelikler (etekler) kalkar' + NL +
      '_n73 = sum(1 for L_ in [SC.PARCALAR, KS.PARCALAR, KC.PARCALAR] for p_ in L_ if _SIL73(p_))' + NL +
      'for L_ in [SC.PARCALAR, KS.PARCALAR, KC.PARCALAR] + list(K_PARCA.values()) + list(E_PARCA.values()):' + NL +
      '    L_[:] = [p_ for p_ in L_ if not _SIL73(p_)]' + NL +
      'print("v73 · AYAK + ETEK SILINDI: %d parca (B/K/E ayaklari + on supurgelikler) · makine alt saselerin ustunde havada" % _n73)' + NL +
      'print("v72 · BAGIMSIZ ISTASYONLAR:')
s = s.replace('"""', '"""hat_montaj_v73 (29 Eyl 2026): ayaklar + etekler yok — yap_hat_montaj_v73.py.\n', 1)
compile(s, "hat_montaj_v73.py", "exec")
io.open(os.path.join(U, "hat_montaj_v73.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v73.py yazildi")
