import sys, re, collections
sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import h3_e_sac_v1 as E, h3_u_sac_v1 as U
g = E.kur(log=lambda *a: None)
L = E.govde_parcalari(g)
c = collections.Counter()
for p in L:
    k = (g.mal(p), p.get("tur"), g.kapakla_doner(p["ad"]), re.sub(r"_?\d.*$", "", p["ad"])[:22])
    c[k] += 1
for k, v in sorted(c.items(), key=lambda x: str(x)): print("E", k, v)
print("E arayuz", len(g.ARAYUZ), collections.Counter(re.sub(r"_?\d.*$","",p["ad"]) for p in g.ARAYUZ))
G = U.kur(log=lambda *a: None)
for k, gg in G.items():
    L = U.govde_parcalari(gg); c = collections.Counter((gg.mal(p), p.get("tur"), gg.kapakla_doner(p["ad"])) for p in L)
    print("U", k, gg.birim, dict(c), "arayuz", len(gg.ARAYUZ), collections.Counter(re.sub(r"_?\d.*$","",p["ad"]) for p in gg.ARAYUZ))
sys.stdout.flush()
import os; os._exit(0)
