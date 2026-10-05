import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "h3"))
import h3_elektrik_v1 as E, h3_elk_rota as ER
E.yukle()
for p in E.PARCALAR:
    if not p["ad"].startswith(("kablo_TOPPING_sensor_x_home", "kablo_K_EC5000")): ER.ekli_ekle(p["ad"], E.dunya(p))
print("x_home:", ER.kelepceler([(1086.0, 902.0, -13.0), (880.0, 902.0, -13.0)], 2.0))
import h3_elk_ortak as EO
for x in (983.0, 963.0, 1003.0, 943.0):
    p=(x, 902.0, -13.0); y=ER.kelepce_yeri_gercek(p, "x", 2.0); print(x, y)
    if y:
        ks=EO.kelepce(p,"x",2.0,y[0],y[1]); b=ks.BoundingBox(); print("  ", [round(v,1) for v in (b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax)], ER.temiz(ks))
        for a,s_ in ER._engeller((b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax),()):
            try: v=ks.intersect(s_).Volume()
            except Exception: v=-1
            if v>0.01: print("     ", a, round(v,2))
for eks in "":
    print("EC5000", eks, ER.kelepce_yeri((4374.0, 1209.0, -727.0), eks, 3.0), ER.kelepce_yeri_gercek((4374.0, 1209.0, -727.0), eks, 3.0))
sys.stdout.flush(); os._exit(0)
