# -*- coding: utf-8 -*-
# "Uzaklaşınca istasyonlar kayboluyor" — sebep testi: Level of Detail (Large Assy Target Frame Rate) açık/kapalı karşılaştırması
import win32com.client, win32gui, win32con, pythoncom, winreg, time, sys, os
from win32com.client import VARIANT
from PIL import ImageGrab
HAT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\HAT.SLDASM"
OUT = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\cfa68d5f-65ff-4317-9646-b634d3fef835\scratchpad"
PERF = r"SOFTWARE\SolidWorks\SOLIDWORKS 2025\Performance"

def ayar(ad, deger):
    k = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, PERF, 0, winreg.KEY_SET_VALUE | winreg.KEY_READ)
    try: eski = winreg.QueryValueEx(k, ad)[0]
    except FileNotFoundError: eski = None
    winreg.SetValueEx(k, ad, 0, winreg.REG_DWORD, deger); winreg.CloseKey(k); print("  %-34s %s -> %s" % (ad, eski, deger))

def kapat():
    try:
        sw = win32com.client.GetActiveObject("SldWorks.Application"); sw.CloseAllDocuments(True); sw.ExitApp()
    except Exception: pass
    os.system("taskkill /F /IM SLDWORKS.exe >nul 2>&1"); time.sleep(6)

def ac_ve_cek(dosya_adi, uzaklas=4):
    sw = win32com.client.Dispatch("SldWorks.Application"); sw.Visible = True; time.sleep(4); sw.FrameState = 2
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(HAT, 2, 1, "", e, w)
    def cagir(ad):
        did = d._oleobj_.GetIDsOfNames(0, ad); did = did[0] if isinstance(did, tuple) else did
        return d._oleobj_.Invoke(did, 0, 3, True)
    d.ShowNamedView2("*Isometric", 7); cagir("ViewZoomtofit2"); time.sleep(1)
    for _ in range(uzaklas): cagir("ViewZoomout"); time.sleep(0.4)      # kullanıcının uzaklaşması
    h = []
    win32gui.EnumWindows(lambda hh, _: (h.append(hh) if "SOLIDWORKS Premium" in win32gui.GetWindowText(hh) else None, True)[1], None)
    if h: win32gui.ShowWindow(h[0], win32con.SW_MAXIMIZE); win32gui.SetForegroundWindow(h[0])
    time.sleep(3)
    im = ImageGrab.grab(); im.thumbnail((1300, 820)); p = os.path.join(OUT, dosya_adi); im.save(p); print("  goruntu:", p)

if __name__ == "__main__":
    if sys.argv[1] == "once":                       # mevcut ayarla (LOD açık)
        kapat(); ac_ve_cek("lod_once.png")
    else:                                           # LOD kapalı + performans hattı kapalı
        kapat(); ayar("Large Assy Target Frame Rate", 0)      # Detay Seviyesi = KAPALI (kaybolmayı bitirir)
        ayar("Large Assembly Threshold", 100000)              # büyük montaj modu kendiliğinden açılmasın
        ac_ve_cek("lod_sonra.png")
