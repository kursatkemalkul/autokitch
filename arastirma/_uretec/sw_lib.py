# -*- coding: utf-8 -*-
# AUTOKITCH — SolidWorks 2025 COM yardımcı kütüphanesi (7 Eyl 2026)
# Her parça GLOBAL koordinatta modellenir (X sağa, Y yukarı zemin 0, Z öne; kasa z −820..0, ön yüz z 0..40),
# montajda AddComponent5 verilen noktaya bbox MERKEZİNİ koyduğundan merkez = kendi merkezi → birim dönüşüm.
import win32com.client, os, time, pythoncom
from win32com.client import VARIANT
from PIL import Image

TPL_DIR = r"C:\ProgramData\SolidWorks\SOLIDWORKS 2025\templates\MBD"
TPL_PRT = os.path.join(TPL_DIR, "part 1001mm and larger.prtdot"); TPL_ASM = os.path.join(TPL_DIR, "assembly 1001mm and larger.asmdot")
M = 0.001
FR, TP, RT = 0, 1, 2

def mcall(o, name, *args):
    did = o._oleobj_.GetIDsOfNames(0, name); did = did[0] if isinstance(did, tuple) else did
    r = o._oleobj_.Invoke(did, 0, pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET, True, *args)
    return win32com.client.Dispatch(r) if isinstance(r, pythoncom.TypeIIDs[pythoncom.IID_IDispatch]) else r
import sw_taskpane_off
def _connect():
    sw_taskpane_off.uygula()          # SolidWorks açılmadan önce sağ paneli kapalıya çek
    """SolidWorks'e bağlan; kapanmakta olan örnekle çakışmamak için sürüm okunana kadar dene"""
    EXE = r"C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\SLDWORKS.exe"
    for k in range(8):
        try:
            app = win32com.client.Dispatch("SldWorks.Application"); app.Visible = True; _ = app.RevisionNumber; time.sleep(2); _ = app.RevisionNumber
            return app
        except Exception as e:
            print("SolidWorks baglanti denemesi %d: %s" % (k+1, e))
            if k == 1 and os.path.exists(EXE):                  # COM sunucusu yanit vermiyorsa uygulamayi dogrudan baslat
                print("  -> SLDWORKS.exe dogrudan baslatiliyor"); os.spawnv(os.P_NOWAIT, EXE, ['"%s"' % EXE]); time.sleep(35)
            else: time.sleep(8)
    raise RuntimeError("SolidWorks baglanamadi")
sw = _connect()
NUL = VARIANT(pythoncom.VT_DISPATCH, None)
def saveas(doc, path):
    try:                                            # belge zaten bu dosyaysa: normal kaydet
        if os.path.normcase(doc.GetPathName or "") == os.path.normcase(path):
            e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
            return bool(doc.Save3(1, e, w)) and e.value == 0
    except Exception: pass
    if os.path.exists(path): os.remove(path)          # var olan dosya → SolidWorks "üzerine yaz?" diyaloğu açıp takılıyor
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    ok = doc.Extension.SaveAs3(path, 0, 1, NUL, NUL, e, w); return bool(ok) and e.value == 0
def png(doc, path, view, wpx=1800, hpx=1100):
    # HATA DUZELTMESI (10 Eyl 2026): ikinci parametre gorunus KIMLIGI; sabit 1 verilince
    # "*Right"/"*Top" istense bile hep ONDEN goruntu aliniyordu.
    VID = {"*Front": 1, "*Back": 2, "*Left": 3, "*Right": 4, "*Top": 5, "*Bottom": 6,
           "*Isometric": 7, "*Dimetric": 8, "*Trimetric": 9}
    doc.ShowNamedView2(view, VID.get(view, 1)); mcall(doc, "ViewZoomtofit2")
    for k in range(4):                      # boş (bembeyaz) görüntü gelirse bekleyip yeniden al
        time.sleep(1.5); doc.SaveBMP(path, wpx, hpx); im = Image.open(path); im.save(path)
        if im.convert("L").getextrema()[0] < 250: return
        try: mcall(doc, "GraphicsRedraw2")
        except Exception: pass
def bbox_of(doc):
    bb = [1e9]*3 + [-1e9]*3
    for x in doc.GetBodies2(0, True):
        g = mcall(x, "GetBodyBox")
        for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
    return bb

class Station:
    """bir istasyonun parça klasörü + montajı"""
    def __init__(self, root, name):
        self.root, self.name = root, name; self.pdir = os.path.join(root, "parca"); os.makedirs(self.pdir, exist_ok=True)
        self.parts = []; self.instances = set(); self.t0 = time.time(); self.bb = [1e9]*3 + [-1e9]*3
    def _track(self, bb):
        for i in range(3): self.bb[i] = min(self.bb[i], bb[i]); self.bb[i+3] = max(self.bb[i+3], bb[i+3])
    def center(self): return [(self.bb[i]+self.bb[i+3])/2 for i in range(3)]
    def add_instance(self, path, center_m=None, offset_mm=None):
        """hazır alt montaj/parça örneği. center_m: hedef bbox merkezi (m) · offset_mm: kendi koordinatından kaydırma (mm).
           offset verilirse parça kendi modellendiği yere göre taşınır (merkez hesabı gerekmez)."""
        yer = ("offset", [v*M for v in offset_mm]) if offset_mm is not None else list(center_m)
        self.parts.append((path, yer)); self.instances.add(os.path.splitext(os.path.basename(path))[0].lower())
    # ---- parça üretimi ----
    def _new(self):
        sw.NewDocument(TPL_PRT, 0, 0, 0); doc = sw.ActiveDoc; sk = doc.SketchManager; sk.AddToDB = True; sk.DisplayWhenAdded = False
        pl = []; f = mcall(doc, "FirstFeature")
        while f is not None and len(pl) < 3:
            if mcall(f, "GetTypeName2") == "RefPlane": pl.append(f)
            f = mcall(f, "GetNextFeature")
        return doc, sk, doc.FeatureManager, pl
    @staticmethod
    def _ext(fm, name, n0, n1, cut):
        if n0 >= 0: dirf, fs, st, dp = False, False, n0, n1 - n0
        else:       dirf, fs, st, dp = True, True, -n1, n1 - n0
        if cut: f = fm.FeatureCut4(True, False, not dirf, 0, 0, dp*M, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, False, False, False, 3 if st else 0, st*M, fs, False)
        else:   f = fm.FeatureExtrusion3(True, False, dirf, 0, 0, dp*M, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, 3 if st else 0, st*M, fs)
        if f is None: raise RuntimeError("feature olusmadi: " + name)
        f.Name = name
    def part(self, fname, ops, _retry=2):
        """ops: liste [(plane, 'rect'|'poly', geo, n0, n1, cut)] — geo: rect (u0,u1,v0,v1) · poly [(u,v),...]"""
        try: return self._part(fname, ops)
        except RuntimeError as e:
            if _retry <= 0: raise
            print("uyari: %s → %d s bekleyip yeniden (%s)" % (fname, 5, e)); time.sleep(5)
            try: sw.CloseAllDocuments(True)
            except Exception: pass
            return self.part(fname, ops, _retry-1)
    def _part(self, fname, ops):
        doc, sk, fm, pl = self._new()
        for k, (plane, kind, geo, n0, n1, cut) in enumerate(ops):
            doc.ClearSelection2(True); pl[plane].Select2(False, 0); sk.InsertSketch(True)
            if kind == 'rect': sk.CreateCornerRectangle(geo[0]*M, geo[2]*M, 0, geo[1]*M, geo[3]*M, 0)
            elif kind == 'circ': sk.CreateCircleByRadius(geo[0]*M, geo[1]*M, 0, geo[2]*M)
            elif kind == 'circs':                      # tek eskizde çok daire (çukur tablası)
                for g in geo: sk.CreateCircleByRadius(g[0]*M, g[1]*M, 0, g[2]*M)
            else:
                for i in range(len(geo)):
                    a, b = geo[i], geo[(i+1) % len(geo)]; sk.CreateLine(a[0]*M, a[1]*M, 0, b[0]*M, b[1]*M, 0)
            sk.InsertSketch(True); self._ext(fm, "%s_%d" % (fname, k+1), n0, n1, cut); doc.ClearSelection2(True)
        bb = bbox_of(doc); path = os.path.join(self.pdir, fname + ".SLDPRT"); self._track(bb)
        if not saveas(doc, path): raise RuntimeError("kayit hatasi " + fname)
        sw.CloseDoc(doc.GetTitle); self.parts.append((path, [(bb[i]+bb[i+3])/2 for i in range(3)])); return path
    # kısa yollar (global mm)
    def box(self, fname, x0, x1, y0, y1, z0, z1, cuts=()):
        """cuts: [(x0,x1,y0,y1,z0,z1)] ön düzlemden kesmeler"""
        ops = [(FR, 'rect', (x0, x1, y0, y1), z0, z1, False)] + [(FR, 'rect', (c[0], c[1], c[2], c[3]), c[4], c[5], True) for c in cuts]
        return self.part(fname, ops)
    def prism_y(self, fname, pts_xz, y0, y1, cuts=()):
        """üstten görünüş poligonu (x,z), Y boyunca"""
        ops = [(TP, 'poly', [(x, -z) for x, z in pts_xz], y0, y1, False)] + [(FR, 'rect', (c[0], c[1], c[2], c[3]), c[4], c[5], True) for c in cuts]
        return self.part(fname, ops)
    def prism_z(self, fname, pts_xy, z0, z1):
        """önden görünüş poligonu (x,y), Z boyunca"""
        return self.part(fname, [(FR, 'poly', pts_xy, z0, z1, False)])
    def cyl_y(self, fname, cx, cz, r, y0, y1):
        """dikey silindir (16-gen poligon yaklaşımı yerine gerçek daire)"""
        doc, sk, fm, pl = self._new(); doc.ClearSelection2(True); pl[TP].Select2(False, 0); sk.InsertSketch(True)
        sk.CreateCircleByRadius(cx*M, -cz*M, 0, r*M); sk.InsertSketch(True); self._ext(fm, fname, y0, y1, False)
        bb = bbox_of(doc); path = os.path.join(self.pdir, fname + ".SLDPRT"); self._track(bb)
        if not saveas(doc, path): raise RuntimeError("kayit hatasi " + fname)
        sw.CloseDoc(doc.GetTitle); self.parts.append((path, [(bb[i]+bb[i+3])/2 for i in range(3)])); return path
    def cyl_z(self, fname, cx, cy, r, z0, z1):
        doc, sk, fm, pl = self._new(); doc.ClearSelection2(True); pl[FR].Select2(False, 0); sk.InsertSketch(True)
        sk.CreateCircleByRadius(cx*M, cy*M, 0, r*M); sk.InsertSketch(True); self._ext(fm, fname, z0, z1, False)
        bb = bbox_of(doc); path = os.path.join(self.pdir, fname + ".SLDPRT"); self._track(bb)
        if not saveas(doc, path): raise RuntimeError("kayit hatasi " + fname)
        sw.CloseDoc(doc.GetTitle); self.parts.append((path, [(bb[i]+bb[i+3])/2 for i in range(3)])); return path
    def exit_sw(self):
        """oturumu kapat (bellek şişmesine karşı her fazda temiz SolidWorks)"""
        try: sw.CloseAllDocuments(True); sw.ExitApp()
        except Exception: pass
        time.sleep(6)
    def load_dir(self):
        """parça klasöründeki mevcut SLDPRT'leri (merkezlerini okuyarak) listeye al — yeniden üretmeden montaj için"""
        self.parts = []
        for f in sorted(os.listdir(self.pdir)):
            if not f.lower().endswith(".sldprt") or f.startswith("~$"): continue
            path = os.path.join(self.pdir, f); e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
            d = sw.OpenDoc6(path, 1, 1, "", e, w); bb = bbox_of(d); sw.CloseDoc(d.GetTitle); self._track(bb)
            self.parts.append((path, [(bb[i]+bb[i+3])/2 for i in range(3)]))
    # ---- montaj ----
    def assemble(self, asm_name):
        sw.NewDocument(TPL_ASM, 0, 0, 0); asm = sw.ActiveDoc
        for path, c in self.parts:
            e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
            d = sw.OpenDoc6(path, 2 if path.lower().endswith(".sldasm") else 1, 1, "", e, w)
            if isinstance(c, tuple) and c[0] == "offset":     # kaydırma modu: parçanın kendi bbox merkezi + kaydırma
                if path.lower().endswith(".sldasm"):
                    bb = [1e9]*3 + [-1e9]*3
                    for cp in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
                        g = cp.GetBox(False, False)
                        for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
                else: bb = bbox_of(d)
                c = [(bb[i]+bb[i+3])/2 + c[1][i] for i in range(3)]
            if asm.AddComponent5(path, 0, "", False, "", c[0], c[1], c[2]) is None: raise RuntimeError("bilesen eklenemedi " + path)
            sw.CloseDoc(d.GetTitle if d is not None else os.path.basename(path))
        comps = list(asm.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
        asm.ClearSelection2(True)
        for cpt in comps: cpt.Select4(True, NUL, False)
        mcall(asm, "FixComponent"); asm.ClearSelection2(True)
        bad = [cpt.Name2 for cpt in comps if cpt.Name2.rsplit("-", 1)[0].lower() not in self.instances and max(abs(v) for v in cpt.Transform2.ArrayData[9:12]) > 1e-6]
        apath = os.path.join(self.root, asm_name + ".SLDASM"); ok = saveas(asm, apath)
        png(asm, os.path.join(self.root, asm_name + "_asm_iso.png"), "*Isometric"); png(asm, os.path.join(self.root, asm_name + "_asm_on.png"), "*Front")
        sw.CloseDoc(asm.GetTitle)
        print("%s: %d parca, montaj kayit=%s, konum hatasi=%s, sure %.0f s" % (asm_name, len(comps), ok, bad, time.time()-self.t0))
        return apath

# ================= ORTAK YAPI ELEMANLARI (mm) =================
T_DIS, T_IC, H, D, Y0 = 1.5, 1.0, 1970.0, 840.0, 120.0
ZK = -(D - 20)          # −820 kasa arkası
ZF0, ZF1 = 38.5, 40.0   # ön yüz sac düzlemi

def shell(st, p, W, foot, y0=Y0, izgara=None, plint_y=None):
    """dış kabuk 1,5 (yan×2, üst, arka, alt) + plint (bükme sac U, 20 içeride) veya 4 ayak"""
    st.box(p+"dis_yan_sol", 0, T_DIS, y0, H, ZK, 0); st.box(p+"dis_yan_sag", W-T_DIS, W, y0, H, ZK, 0)
    st.box(p+"dis_ust", T_DIS, W-T_DIS, H-T_DIS, H, ZK, 0); st.box(p+"dis_arka", T_DIS, W-T_DIS, y0, H-T_DIS, ZK, ZK+T_DIS)
    st.box(p+"dis_alt", T_DIS, W-T_DIS, y0, y0+T_DIS, ZK+T_DIS, 0)
    if foot == "feet":
        for i, (ax, az) in enumerate([(60, -40), (W-140, -40), (60, ZK+140), (W-140, ZK+140)], 1):
            st.box(p+"ayak_%d" % i, ax, ax+80, 0, Y0, az-80, az)
    else:   # plint: U profil (ön + 2 yan) 1,5 + arka plaka + 4 ayar ayağı M12
        # izgara verilirse yariklar plint sacinin KENDISINE acilir (ayri panel = sahte izgara idi)
        # plint_y verilirse plint govdeden BAGIMSIZ yukseklikte olur (TOPPING: govde 158, plint 120)
        py = plint_y or y0
        st.prism_y(p+"plint_U", [(20, ZK+20), (20, 20), (W-20, 20), (W-20, ZK+20), (W-21.5, ZK+20), (W-21.5, 18.5), (21.5, 18.5), (21.5, ZK+20)], 10, py, izgara or ())
        st.box(p+"plint_arka", 21.5, W-21.5, 10, py, ZK+20, ZK+21.5)
        # AYAR AYAKLARI ARTIK ORTAK PARCA: _ortak/AYAK_AYAR_M12, montajda 4 ornek (bkz. AYAK_YERI)

def AYAK_YERI(W):
    """ayar ayaklarinin (x, z) merkezleri — shell() plint modunda 4 adet"""
    return [(50.0, -50.0), (W-50.0, -50.0), (50.0, ZK+50.0), (W-50.0, ZK+50.0)]

def sove_L(st, p, W, y0, y1, side=30.0):
    st.prism_y(p+"sove_sol", [(0, ZF1), (0, ZF0), (side-T_DIS, ZF0), (side-T_DIS, 0), (side, 0), (side, ZF1)], y0, y1)
    st.prism_y(p+"sove_sag", [(W, ZF1), (W, ZF0), (W-side+T_DIS, ZF0), (W-side+T_DIS, 0), (W-side, 0), (W-side, ZF1)], y0, y1)

def door_C(st, p, x0, x1, y0, y1, hinge="side", kulp=False):   # Kemal kuralı: kulp/girinti YOK, yüzey düz
    """bükme sac kapak 1,5: ön plaka + 20 mm yan dönüşler; gömme kulp oyuğu; menteşe ×2 (yan) veya alt pivot + 2 gazlı amortisör (klape)"""
    cuts = []
    if kulp:
        kx1 = x1-20 if hinge == "side" else (x0+x1)/2+90; kx0 = kx1-26 if hinge == "side" else kx1-180
        ky = (y0+y1)/2 - (90 if hinge == "side" else 17); kh = 180 if hinge == "side" else 34
        cuts = [(kx0, kx1, ky, ky+kh, ZF1-13, ZF1+1)]
        st.box(p+"kulp_cukuru", kx0-1, kx1+1, ky-1, ky+kh+1, ZF1-14, ZF1-13)      # 1,0 mm oyuk tabanı
    st.prism_y(p+"kapak", [(x0, ZF1), (x0, 20), (x0+T_DIS, 20), (x0+T_DIS, ZF0), (x1-T_DIS, ZF0), (x1-T_DIS, 20), (x1, 20), (x1, ZF1)], y0, y1, cuts)
    if hinge == "side":
        for i, yy in enumerate((y0+40, y1-80), 1): st.box(p+"mentese_%d" % i, x0-6, x0+8, yy, yy+40, 20, 33)
    else:   # klape: alt pivot mili Ø8 + 2 gazlı amortisör Ø18×200 (kapalı boy)
        st.box(p+"pivot_mil", x0-10, x1+10, y0+2, y0+10, 22, 30)
        for i, xx in enumerate((x0+15, x1-33), 1): st.box(p+"gazli_amortisor_%d" % i, xx, xx+18, y0+30, y0+230, 8, 26)

def shelf(st, p, x0, x1, y, z0, z1):
    """raf sacı 1,5 (ön/arka 20 mm bükümlü) + 2 L köşebent 30×30×2"""
    st.box(p+"raf", x0, x1, y, y+T_DIS, z0, z1)
    st.box(p+"raf_buk_on", x0, x1, y-20, y, z1-T_DIS, z1); st.box(p+"raf_buk_arka", x0, x1, y-20, y, z0, z0+T_DIS)
    st.prism_z(p+"kosebent_sol", [(x0-2, y-30), (x0, y-30), (x0, y), (x0+30, y), (x0+30, y+2), (x0-2, y+2)], z0, z1)
    st.prism_z(p+"kosebent_sag", [(x1+2, y-30), (x1, y-30), (x1, y), (x1-30, y), (x1-30, y+2), (x1+2, y+2)], z0, z1)

def tray(st, p, x0, x1, y, z0, z1, h=20.0):
    """pide tepsisi: 1,5 mm alüminyum, U kesit (taban + 2 yan), yan bükümleri"""
    st.prism_z(p+"tepsi", [(x0, y+h), (x0, y), (x1, y), (x1, y+h), (x1-T_DIS, y+h), (x1-T_DIS, y+T_DIS), (x0+T_DIS, y+T_DIS), (x0+T_DIS, y+h)], z0, z1)
    st.box(p+"tepsi_on", x0, x1, y, y+h, z1-T_DIS, z1); st.box(p+"tepsi_arka", x0, x1, y, y+h, z0, z0+T_DIS)

def rails(st, p, x0, x1, y, z0, L=500.0):
    """teleskopik ray çifti 45×12,7 (Accuride 3832 tipi)"""
    st.box(p+"ray_sol", x0, x0+12.7, y, y+45, z0-L, z0); st.box(p+"ray_sag", x1-12.7, x1, y, y+45, z0-L, z0)

def pano(st, p, x0, x1, y0, y1, z0, z1):
    """elektrik panosu: montaj plakası 2 + PLC + sürücü ×2 + kontaktör ×2 + klemens rayı + güç kaynağı + kapak"""
    st.box(p+"pano_plaka", x0+10, x1-10, y0+10, y1-10, z0+20, z0+22)
    zb = z0+22; yy = y1-40
    st.box(p+"pano_plc", x0+30, x0+130, yy-110, yy, zb, zb+75)
    st.box(p+"pano_guc_kaynagi", x0+150, x0+250, yy-110, yy, zb, zb+110)
    for i in range(2): st.box(p+"pano_surucu_%d" % (i+1), x0+30+i*90, x0+100+i*90, yy-270, yy-140, zb, zb+130)
    for i in range(2): st.box(p+"pano_kontaktor_%d" % (i+1), x0+230+i*55, x0+275+i*55, yy-230, yy-150, zb, zb+80)
    st.box(p+"pano_klemens_rayi", x0+30, x1-30, y0+40, y0+47.5, zb, zb+35)
    st.box(p+"pano_kablo_kanali", x0+30, x1-30, y0+100, y0+140, zb, zb+40)

def insulated_cell(st, p, W, ycell0, ycell1, pu, ytop_single=None, pu_back=None, y0=Y0, top_pu=True, ze=0.0):
    """PU + iç kabuk 1,0: yan×2, arka, taban, tavan (soğuk/sıcak hücre)"""
    pb = pu if pu_back is None else pu_back
    xi0, xi1 = T_DIS+pu+T_IC, W-T_DIS-pu-T_IC; zi = ZK+T_DIS+pb+T_IC
    ytek = ytop_single if ytop_single else (ycell1+T_IC+pu+T_IC if top_pu else ycell1+T_IC)
    st.box(p+"pu_yan_sol", T_DIS, T_DIS+pu, y0+T_DIS, ytek, ZK+T_DIS, ze); st.box(p+"pu_yan_sag", W-T_DIS-pu, W-T_DIS, y0+T_DIS, ytek, ZK+T_DIS, ze)
    st.box(p+"pu_arka", T_DIS+pu, W-T_DIS-pu, y0+T_DIS, ytek, ZK+T_DIS, ZK+T_DIS+pb)
    st.box(p+"pu_alt", T_DIS+pu, W-T_DIS-pu, y0+T_DIS, ycell0-T_IC, zi-T_IC, ze)
    if top_pu: st.box(p+"pu_tavan", T_DIS+pu, W-T_DIS-pu, ycell1+T_IC, ytek-T_IC, zi-T_IC, ze); st.box(p+"teknik_taban", T_DIS+pu, W-T_DIS-pu, ytek-T_IC, ytek, zi-T_IC, ze)
    st.box(p+"ic_yan_sol", xi0-T_IC, xi0, ycell0-T_IC, ycell1+T_IC, zi-T_IC, ze); st.box(p+"ic_yan_sag", xi1, xi1+T_IC, ycell0-T_IC, ycell1+T_IC, zi-T_IC, ze)
    st.box(p+"ic_arka", xi0, xi1, ycell0-T_IC, ycell1+T_IC, zi-T_IC, zi); st.box(p+"ic_alt", xi0, xi1, ycell0-T_IC, ycell0, zi, ze)
    st.box(p+"ic_tavan", xi0, xi1, ycell1, ycell1+T_IC, zi, ze)
    return xi0, xi1, zi

def cooling_unit(st, p, x0, y0, z0, kind="kompresor"):
    """soğutma grubu: kompresör Ø120×200 + kondenser 300×250×60 + fan Ø200 ; evaporatör 400×200×100 + fan"""
    if kind == "kompresor":
        st.cyl_y(p+"kompresor", x0+100, z0-100, 60, y0, y0+200); st.box(p+"kondenser", x0+220, x0+520, y0, y0+250, z0-200, z0-140)
        st.cyl_z(p+"kondenser_fan", x0+370, y0+125, 100, z0-140, z0-100)
    else:
        st.box(p+"evaporator", x0, x0+400, y0, y0+100, z0-200, z0); st.cyl_z(p+"evap_fan", x0+200, y0+50, 90, z0-240, z0-200)

def glass_door(st, p, x0, x1, y0, y1):
    """cam kapak: çerçeve 1,5 bükme C + çift cam 2×4 + hava 8 = 16 (12'ye sıkıştırılmış: 4+4+4) + üst pivot + motor"""
    st.prism_y(p+"cam_cerceve_sol", [(x0, ZF1), (x0, 20), (x0+25, 20), (x0+25, ZF1)], y0, y1); st.prism_y(p+"cam_cerceve_sag", [(x1-25, ZF1), (x1-25, 20), (x1, 20), (x1, ZF1)], y0, y1)
    st.box(p+"cam_cerceve_ust", x0+25, x1-25, y1-25, y1, 20, ZF1); st.box(p+"cam_cerceve_alt", x0+25, x1-25, y0, y0+25, 20, ZF1)
    st.box(p+"cam_dis", x0+25, x1-25, y0+25, y1-25, 34, 38); st.box(p+"cam_ic", x0+25, x1-25, y0+25, y1-25, 22, 26)
    st.box(p+"kapak_motoru", x0+30, x0+90, y0-40, y0, -70, -10)
    st.box(p+"kapak_pivot_mili", x0-10, x1+10, y0-2, y0+6, 26, 34)
