import os, sys
from sw_lib import *
ROOT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
for folder, name in [a.split(":") for a in sys.argv[1:]]:
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, folder, name + ".SLDASM"), 2, 1, "", e, w)
    png(d, os.path.join(ROOT, folder, name + "_asm_iso.png"), "*Isometric"); png(d, os.path.join(ROOT, folder, name + "_asm_on.png"), "*Front"); sw.CloseDoc(d.GetTitle); print(name, "png ok")
