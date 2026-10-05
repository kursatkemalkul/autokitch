# Blender: TOPPING X ekseni GLB'si (cadquery, mm, y yukarı) → döndür + ölçekle, kamera TC yerel mm ile
# blender -b -P bl_tc_gor.py -- <glb> <cikti.png> <kamera x,y,z> <hedef x,y,z> <fov> [WxH]
import bpy, math, sys, mathutils
argv = sys.argv[sys.argv.index("--") + 1:]
GLB, CIKTI = argv[0], argv[1]
KAM = [float(v) for v in argv[2].split(",")]; HED = [float(v) for v in argv[3].split(",")]; FOV = float(argv[4])
RX, RY = (int(v) for v in (argv[5].split("x") if len(argv) > 5 else ("1400", "820")))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
kok = bpy.data.objects.new("KOK", None); bpy.context.scene.collection.objects.link(kok)
for o in list(bpy.data.objects):
    if o is kok: continue
    if o.parent is None:
        o.parent = kok
kok.rotation_euler = (math.radians(90.0), 0.0, 0.0); kok.scale = (0.001, 0.001, 0.001)
for m in bpy.data.materials:
    c = (0.75, 0.76, 0.78, 1.0)
    if m.use_nodes:
        for n in m.node_tree.nodes:
            if n.type == "BSDF_PRINCIPLED":
                v = n.inputs["Base Color"].default_value; c = (v[0], v[1], v[2], 1.0); break
    m.diffuse_color = c
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading; sh.light = "STUDIO"; sh.color_type = "MATERIAL"; sh.show_cavity = True; sh.show_object_outline = True
sh.object_outline_color = (0, 0, 0); sh.show_backface_culling = False
sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("d"); sc.world = w; w.color = (0.93, 0.94, 0.95)
cam_d = bpy.data.cameras.new("k"); cam = bpy.data.objects.new("k", cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam_d.type = "PERSP"; cam_d.lens_unit = "FOV"; cam_d.angle = math.radians(FOV); cam_d.clip_start = 0.005
sc.render.resolution_x, sc.render.resolution_y = RX, RY
def B(x, y, z): return (x / 1000.0, -z / 1000.0, y / 1000.0)
cam.location = B(*KAM)
d = mathutils.Vector(B(*HED)) - mathutils.Vector(cam.location); cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
sc.render.filepath = CIKTI
bpy.ops.render.render(write_still=True)
print("RENDER", CIKTI, flush=True)
