# Blender arka plan (5.1): hat_v87.glb → K (ön kapaksız) + personel tezgâhı (bulaşık + evye) + genel
# Kullanım: blender -b -P blender_v86.py -- <glb> <cikti_klasoru>
import bpy, bmesh, math, sys, os, mathutils
argv = sys.argv[sys.argv.index("--") + 1:]
GLB, CIKTI = argv[0], argv[1]
KESIT_X = 1.820            # m · soğutma grubunun ortası (Secop CU x 1633–2013)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
sc = bpy.context.scene
sc.frame_set(0)

# --- malzeme renkleri: Principled Base Color → görünüm rengi (Workbench MATERIAL) ---
for m in bpy.data.materials:
    c = (0.75, 0.76, 0.78, 1.0)
    if m.use_nodes:
        for n in m.node_tree.nodes:
            if n.type == "BSDF_PRINCIPLED":
                v = n.inputs["Base Color"].default_value
                c = (v[0], v[1], v[2], 1.0)
                break
    ad = m.name.lower()
    if "on_seffaf" in ad or "seffaf" in ad or "cam" == ad:
        c = (0.80, 0.82, 0.84, 1.0)
    m.diffuse_color = c

# --- kenar çizgisi düğümleri (KENAR_*) render'a girmez ---
for o in bpy.data.objects:
    if o.name.startswith("KENAR_"):
        o.hide_render = True; o.hide_set(True)

# --- sahne: Workbench, malzeme rengi, boşluk + dış çizgi ---
sc.render.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading
sh.light = "STUDIO"; sh.color_type = "MATERIAL"
sh.show_cavity = True; sh.cavity_type = "BOTH"; sh.cavity_ridge_factor = 1.0; sh.cavity_valley_factor = 1.0
sh.show_object_outline = True; sh.object_outline_color = (0.0, 0.0, 0.0)
sh.show_shadows = False; sh.show_specular_highlight = True
sc.render.film_transparent = False
sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("dunya"); sc.world = w; w.color = (0.93, 0.94, 0.95)
sc.render.resolution_percentage = 100

cam_d = bpy.data.cameras.new("kamera")
cam = bpy.data.objects.new("kamera", cam_d); sc.collection.objects.link(cam); sc.camera = cam


def bak(konum, hedef):
    cam.location = konum
    d = mathutils.Vector(hedef) - mathutils.Vector(konum)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def render(ad):
    sc.render.filepath = os.path.join(CIKTI, ad)
    bpy.ops.render.render(write_still=True)
    print("RENDER", ad, flush=True)



SAKLI = []
def kapak_gizle(evet):
    for o in bpy.data.objects:
        if o.type != "MESH": continue
        ms = [s_.material.name.lower() for s_ in o.material_slots if s_.material]
        if any("seffaf" in m_ for m_ in ms):
            o.hide_render = evet
def B(x, y, z): return (x / 1000.0, -z / 1000.0, y / 1000.0)
cam_d.type = "PERSP"; cam_d.lens_unit = "FOV"
# 1 · genel (kapaklar kapalı)
cam_d.angle = math.radians(38); sc.render.resolution_x, sc.render.resolution_y = 1900, 1150
bak(B(1200, 2900, 3600), B(2900, 900, 300)); render("v87_genel")
# 2 · K ön kapaksız (önden 3/4)
kapak_gizle(True)
cam_d.angle = math.radians(34); sc.render.resolution_x, sc.render.resolution_y = 1500, 1700
bak(B(3500, 2150, 1500), B(4200, 1050, -380)); render("v87_K_34")
cam_d.type = "ORTHO"; cam_d.ortho_scale = 1.95; sc.render.resolution_x, sc.render.resolution_y = 1100, 1700
bak(B(4200, 960, 3000), B(4200, 960, 0)); render("v87_K_on")
# 3 · personel tezgâhı v2 (bulaşık altta, el evyesi üstte) — bekleme tarafından
cam_d.type = "PERSP"; cam_d.angle = math.radians(40); sc.render.resolution_x, sc.render.resolution_y = 1600, 1200
bak(B(2950, 1550, 1250), B(4170, 620, 1460)); render("v87_tezgah")
kapak_gizle(False)
print("BITTI", flush=True)
