# -*- coding: utf-8 -*-
"""CİHAZ ENVANTERİ DENETİMİ — dökümdeki her elektrikli cihaz (motor · sensör · fan · valf adası · pompa · kompresör …) bir elektrik
parçasına (kablo / kanal / rakor / dağıtıcı · ELK_) ya da kendi mevcut kablo ucuna (motor_kablosu_, M12 soket, M8 kablo) ≤ 0,6 mm değiyor mu.
Kullanım: python cihaz_envanter.py <_dunya_tam klasörü>"""
import sys, os, io, json, re
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
import cadquery as cq
from OCP.TopoDS import TopoDS_Iterator

DD = sys.argv[1]
idx = json.load(io.open(os.path.join(DD, "dunya.json"), encoding="utf-8"))
sh = cq.Shape.importBrep(os.path.join(DD, "dunya.brep"))
it = TopoDS_Iterator(sh.wrapped); ch = []
while it.More():
    ch.append(cq.Shape.cast(it.Value())); it.Next()
L = [("%s|%s" % (i[0], i[1]), i[0], s) for i, s in zip(idx, ch)]
CIHAZ = re.compile(r"(motoru|_motor$|motor_govde|sensoru|_sensor$|sensoru_(alt|ust)|_fani_\d|^fan_(sol|sag)_\d|valf_adasi|pompasi|^sogutma_grubu_kompresor$|KLF66$|PM1704|SMT-8M_\d|PulsaJet_AAB|yuk_hucresi|reed_(acik|kapali)|isik_perdesi_(ust|alt)$|emniyet_sensoru(_alt)?$|kuru_surucu_\d|EC5000_354)", re.I)
HARIC_BIRIM = ("CEK_", "E_", "QR_", "F_TP10", "HAVA_KOMPRESOR", "INSAN", "TEZGAH", "D_BULASIK", "K_BULASIK", "ROBOT", "URUN", "BULASIK")
HARIC_AD = re.compile(r"braket|bayrag|hedefi|miknatis|lami|tutucu|somun|kizak|kablo|soket|kapak|zarf", re.I)
TASIYICI = re.compile(r"^ELK_|motor_kablosu|_m12_soket|M8_kablo|M8_soketi|EC5000_kablo|kuru_din_rayi|tahrik_rulosu_EC5000_kablo", re.I)
cihazlar = [(a, b, s) for a, b, s in L if CIHAZ.search(a.split("|", 1)[1]) and not b.startswith(HARIC_BIRIM) and not HARIC_AD.search(a.split("|", 1)[1])]
tas = [(a, s, s.BoundingBox()) for a, b, s in L if TASIYICI.search(b) or TASIYICI.search(a.split("|", 1)[1])]
def _yakin(s1, s2, t):
    b1, b2 = s1.BoundingBox(), s2.BoundingBox()
    if b2.xmin > b1.xmax + t or b1.xmin > b2.xmax + t or b2.ymin > b1.ymax + t or b1.ymin > b2.ymax + t or b2.zmin > b1.zmax + t or b1.zmin > b2.zmax + t:
        return False
    d = BRepExtrema_DistShapeShape(s1.wrapped, s2.wrapped)
    return d.IsDone() and d.Value() <= t
kablosuz = []
for a, b, s in cihazlar:
    grup = [s] + [s2 for a2, b2, s2 in L if b2 == b and a2 != a and _yakin(s, s2, 0.6)]      # cihaz + ona değen kendi parçaları (fiş, mil ucu, kapak)
    ok = any(_yakin(g, ts, 0.6) for g in grup for ta, ts, tb in tas)
    if not ok: bb = s.BoundingBox(); kablosuz.append((a, [round(v) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)]))
BILINEN = {"donus_motoru": "araba üstünde · enerji zincirinden", "tabla_home_sensoru": "araba üstünde · enerji zincirinden",
           "acici_motoru_on": "açıcı hazır alınır · yalnız görsel (Kemal 1 Eki)", "acici_motoru_arka": "açıcı hazır alınır · yalnız görsel (Kemal 1 Eki)",
           "valf_adasi_SS5Y3-20-04": "pano içinde · DIN ray/valf kablosu pano iç tesisatı", "yb_kasnak_motor": "cihaz değil: motor kasnağı (kayışla motora bağlı)",
           **{_a36: "A açıcı paketi · tedarikçinin kendi emniyet devresi (Kemal 1 Eki: açıcı çevresindeki elektrik kalkar)" for _a36 in ("onyuz_emniyet_sensoru", "onyuz_emniyet_sensoru_alt", "onyuz_isik_perdesi_ust", "onyuz_isik_perdesi_alt")}}
bil = [(a, b) for a, b in kablosuz if a.split("|", 1)[1] in BILINEN]
gercek = [(a, b) for a, b in kablosuz if a.split("|", 1)[1] not in BILINEN]
print("CİHAZ ENVANTERİ: %d cihaz · KABLOSUZ %d (bilinen istisna %d)" % (len(cihazlar), len(gercek), len(bil)))
for a, b in gercek: print("   KABLOSUZ:", a, b)
for a, b in bil: print("   istisna:", a, "·", BILINEN[a.split("|", 1)[1]])
sys.stdout.flush(); os._exit(0)
