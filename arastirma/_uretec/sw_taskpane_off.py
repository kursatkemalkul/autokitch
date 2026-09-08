# -*- coding: utf-8 -*-
# SolidWorks sağdaki Task Pane'i (SOLIDWORKS Resources / Design Library / haber akışı) kapalı tutar.
# Ayar SolidWorks KAPALIYKEN yazılmalı; açıkken yazılan değerin üzerine çıkışta eski hâli yazılır.
import winreg
BASE = r"SOFTWARE\SolidWorks\SOLIDWORKS 2025"
AYAR = [(r"\User Interface\General-Bar-59465", "paneWndVisible", 0),      # panel gizli
        (r"\User Interface\General-Bar-59465", "taskpaneDismissed", 1),   # kullanıcı kapattı say
        (r"\User Interface\General-Bar-59465", "paneWndIsExpanded", 0),   # açılmış hâlde başlama
        (r"\General", "Show Welcome Screen", 1),                           # ana sayfa (home) ikonu KALSIN
        (r"\General", "Show Latest News feeds In task pane", 0),          # haber akışı (paneli çağırır)
        (r"\General", "Taskpane Animation", 0)]

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

if __name__ == "__main__":
    uygula(); print("Task Pane kapatildi (SolidWorks bir sonraki acilista panelsiz gelir).")
