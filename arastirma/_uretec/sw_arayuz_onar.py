# -*- coding: utf-8 -*-
# SolidWorks arayüz onarımı: (1) "Toolbar information is inconsistent" uyarısı, (2) sağdaki Task Pane paneli
# Yöntem: düzgün kapat → arayüz kaydını sıfırla (varsayılan araç çubukları) → panel kapalı yaz → aç, uyarı çıkarsa OK bas, doğrula
import win32com.client, win32gui, win32con, winreg, time, os, subprocess
from PIL import ImageGrab
BASE = r"SOFTWARE\SolidWorks\SOLIDWORKS 2025"
EXE = r"C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\SLDWORKS.exe"
HAT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\HAT.SLDASM"
OUT = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\cfa68d5f-65ff-4317-9646-b634d3fef835\scratchpad"

def duzgun_kapat():
    try:
        sw = win32com.client.GetActiveObject("SldWorks.Application"); sw.CloseAllDocuments(True); sw.ExitApp(); print("  duzgun kapatildi")
    except Exception: pass
    for _ in range(20):
        time.sleep(2)
        if "SLDWORKS.exe" not in subprocess.run(["tasklist", "/FI", "IMAGENAME eq SLDWORKS.exe"], capture_output=True, text=True).stdout: return True
    os.system("taskkill /F /IM SLDWORKS.exe >nul 2>&1"); time.sleep(5); return False

def sil_anahtar(yol):
    """kayıt anahtarını alt anahtarlarıyla sil (SolidWorks yeniden varsayılanla oluşturur)"""
    try: k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, yol, 0, winreg.KEY_ALL_ACCESS)
    except FileNotFoundError: return
    while True:
        try: sil_anahtar(yol + "\\" + winreg.EnumKey(k, 0))
        except OSError: break
    winreg.CloseKey(k); winreg.DeleteKey(winreg.HKEY_CURRENT_USER, yol); print("  silindi:", yol.split("2025")[-1])

def yaz(sub, ad, deger):
    k = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, BASE + sub, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(k, ad, 0, winreg.REG_DWORD, deger); winreg.CloseKey(k)

def uyari_kapat():
    """açılışta çıkan uyarı kutusuna OK bas (varsa)"""
    bulundu = []
    def top(h, _):
        if win32gui.GetWindowText(h) == "SOLIDWORKS" and win32gui.IsWindowVisible(h): bulundu.append(h)
        return True
    win32gui.EnumWindows(top, None)
    for h in bulundu:
        cocuk = []
        win32gui.EnumChildWindows(h, lambda hh, _: (cocuk.append((hh, win32gui.GetClassName(hh), win32gui.GetWindowText(hh))), True)[1], None)
        metin = " | ".join(t for _, _, t in cocuk if t)
        for hh, c, t in cocuk:
            if c == "Button" and t.strip("&").upper() in ("OK", "TAMAM"):
                win32gui.PostMessage(hh, win32con.BM_CLICK, 0, 0); return metin[:120]
    return None

if __name__ == "__main__":
    print("1) SolidWorks kapatiliyor"); duzgun_kapat()
    print("2) arayuz kaydi sifirlaniyor (arac cubuklari varsayilana doner)")
    sil_anahtar(BASE + r"\User Interface")
    print("3) Task Pane kapali yaziliyor")
    for ad, dg in (("paneWndVisible", 0), ("taskpaneDismissed", 1), ("paneWndIsExpanded", 0)): yaz(r"\User Interface\General-Bar-59465", ad, dg)
    yaz(r"\General", "Show Latest News feeds In task pane", 0); yaz(r"\General", "Show Welcome Screen", 1)
    print("4) SolidWorks aciliyor"); os.spawnv(os.P_NOWAIT, EXE, ['"%s"' % EXE, HAT])
    uyari = None
    for _ in range(40):
        time.sleep(3); m = uyari_kapat()
        if m: uyari = m; print("  uyari cikti ve kapatildi:", m)
        if any("SOLIDWORKS Premium" in win32gui.GetWindowText(h) for h in [w for w in [] ] ): pass
        h = []
        win32gui.EnumWindows(lambda hh, _: (h.append(hh) if "SOLIDWORKS Premium" in win32gui.GetWindowText(hh) else None, True)[1], None)
        if h and win32gui.IsWindowVisible(h[0]): break
    time.sleep(20)
    for _ in range(5):
        m = uyari_kapat()
        if m: uyari = m; print("  uyari (gec) kapatildi:", m)
        time.sleep(2)
    h = []
    win32gui.EnumWindows(lambda hh, _: (h.append(hh) if "SOLIDWORKS Premium" in win32gui.GetWindowText(hh) else None, True)[1], None)
    if h: win32gui.ShowWindow(h[0], win32con.SW_MAXIMIZE); win32gui.SetForegroundWindow(h[0]); time.sleep(4)
    panel = []
    def kontrol(hh, _):
        t = win32gui.GetWindowText(hh)
        if t in ("Task Pane", "SOLIDWORKS Resources") and win32gui.IsWindowVisible(hh): panel.append((t, win32gui.GetWindowRect(hh)))
        return True
    win32gui.EnumWindows(kontrol, None)
    print("5) SONUC — acilis uyarisi:", uyari or "YOK", "| gorunur panel:", panel or "YOK")
    im = ImageGrab.grab(); im.thumbnail((1300, 820)); im.save(os.path.join(OUT, "onarim.png")); print("  goruntu: onarim.png")
