import sys, os, re, collections
sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import h3_f_sac_v1 as F
F.kur(log=print); L=F.govde_parcalari()
c=collections.Counter((F._mal(p), re.sub(r"_\d.*$","",p["ad"])) for p in L)
for k,v in sorted(c.items()): print(k,v)
for p in F.G.ARAYUZ: print("AR", p["ad"], p.get("std"), p["arayuz"]["karsi"][:60])
import h3_topping_sac_v1 as T
T.kur(log=print)
for p in T.G.ARAYUZ:
    if not p["ad"].startswith("arayuz_mek"): print("TAR", p["ad"], p["arayuz"]["karsi"][:70], p["arayuz"]["gerek"][:80])
sys.stdout.flush(); os._exit(0)
