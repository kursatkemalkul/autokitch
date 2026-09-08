import os
from sw_lib import *
ROOT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
sw.CloseAllDocuments(True)
st = Station(os.path.join(ROOT, "3_TOPPING"), "TOPPING"); st.load_dir(); print("yuklendi", len(st.parts)); st.assemble("TOPPING")
