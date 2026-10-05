import os, sys
B = os.path.dirname(os.path.abspath(__file__))
os.environ["ADIM5"] = B
os.environ["AUTOKITCH_SAC_STANDART"] = os.path.abspath(os.path.join(B, "..", "..", "sac_standart"))
sys.path.insert(0, B); sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import sac_denetim_5b as DEN
kod = sys.argv[1]; hizli = "--hizli" in sys.argv
if kod == "E":
    import h3_e_sac_v1 as M; DEN.calistir_E(M, hizli=hizli)
else:
    import h3_u_sac_v1 as M; DEN.calistir_U(M, hizli=hizli)
sys.stdout.flush(); os._exit(0)
