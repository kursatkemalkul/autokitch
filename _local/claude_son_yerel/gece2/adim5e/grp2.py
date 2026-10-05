import sys, re, collections, os
sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import h3_topping_sac_v1 as T, h3_f_sac_v1 as F
for M in (T, F):
    M.kur(log=print); L = M.govde_parcalari()
    print(M.SURUM, collections.Counter((M._mal(p), p.get("tur")) for p in L))
    c = collections.Counter((re.sub(r"_?-?\d.*$", "", p["ad"]), (p.get("bom") or ("",))[0][:30]) for p in M.G.ARAYUZ)
    for k, v in sorted(c.items()): print("   AR", k, v)
sys.stdout.flush(); os._exit(0)
