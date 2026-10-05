# -*- coding: utf-8 -*-
# SolidWorks sagdaki Task Pane'i (SOLIDWORKS Resources / User Forum / Design Library) kapali tutar.
# Ayar SolidWorks KAPALIYKEN yazilmali; acikken yazilan degerin uzerine cikista eski hali yazilir.
#
# NOT (9 Eyl 2026): yalniz paneWndVisible / taskpaneDismissed YETMIYOR. SolidWorks panel duzenini
# HKCU\...\DockingPaneLayouts\DockingPaneLayout altinda ikili blob olarak saklayip acilista geri
# yukluyor ve bayraklari eziyor. Bu yuzden o anahtar da siliniyor (once .reg olarak yedeklenir).
import winreg, os, subprocess, datetime

BASE = r"SOFTWARE\SolidWorks\SOLIDWORKS 2025"
YEDEK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_yedek_registry")
AYAR = [(r"\User Interface\General-Bar-59465", "paneWndVisible", 0),      # panel gizli
        (r"\User Interface\General-Bar-59465", "taskpaneDismissed", 1),   # kullanici kapatti say
        (r"\User Interface\General-Bar-59465", "paneWndIsExpanded", 0),   # acilmis halde baslama
        (r"\User Interface\General-Bar-59465", "autoHiding", 1),
        (r"\General", "Show Latest News feeds In task pane", 0),          # haber akisi paneli cagirir
        (r"\General", "Taskpane Animation", 0)]


def _sil_dockingpanelayouts():
    """panel duzeni blob'unu yedekleyip sil — SolidWorks varsayilanla (panelsiz) acilir"""
    yol = BASE + r"\DockingPaneLayouts"
    try:
        winreg.OpenKey(winreg.HKEY_CURRENT_USER, yol).Close()
    except FileNotFoundError:
        print("  %-40s zaten yok" % "DockingPaneLayouts"); return
    os.makedirs(YEDEK, exist_ok=True)
    dosya = os.path.join(YEDEK, "DockingPaneLayouts_%s.reg" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    anahtar = "HKCU\\" + yol
    subprocess.run(["reg", "export", anahtar, dosya, "/y"], capture_output=True)
    r = subprocess.run(["reg", "delete", anahtar, "/f"], capture_output=True, text=True)
    if r.returncode == 0:
        print("  %-40s silindi (yedek: %s)" % ("DockingPaneLayouts", os.path.basename(dosya)))
    else:
        print("  %-40s SILINEMEDI: %s" % ("DockingPaneLayouts", (r.stderr or "").strip()))


def uygula():
    for sub, ad, deger in AYAR:
        try:
            k = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, BASE + sub, 0, winreg.KEY_SET_VALUE | winreg.KEY_READ)
            try: eski = winreg.QueryValueEx(k, ad)[0]
            except FileNotFoundError: eski = None
            winreg.SetValueEx(k, ad, 0, winreg.REG_DWORD, deger); winreg.CloseKey(k)
            print("  %-40s %s -> %d" % (ad, eski, deger))
        except Exception as e:
            print("  %-40s HATA %s" % (ad, e))
    _sil_dockingpanelayouts()


if __name__ == "__main__":
    uygula(); print("Task Pane kapatildi (SolidWorks bir sonraki acilista panelsiz gelir).")
