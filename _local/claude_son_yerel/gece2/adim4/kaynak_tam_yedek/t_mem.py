import os, sys, ctypes
def priv():
    import ctypes.wintypes as w
    class PMC(ctypes.Structure):
        _fields_=[("cb",w.DWORD),("PageFaultCount",w.DWORD),("PeakWorkingSetSize",ctypes.c_size_t),("WorkingSetSize",ctypes.c_size_t),("QuotaPeakPagedPoolUsage",ctypes.c_size_t),("QuotaPagedPoolUsage",ctypes.c_size_t),("QuotaPeakNonPagedPoolUsage",ctypes.c_size_t),("QuotaNonPagedPoolUsage",ctypes.c_size_t),("PagefileUsage",ctypes.c_size_t),("PeakPagefileUsage",ctypes.c_size_t),("PrivateUsage",ctypes.c_size_t)]
    m=PMC(); m.cb=ctypes.sizeof(PMC); ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(m), m.cb); return m.PrivateUsage/1e6
print("base", priv())
if sys.argv[1]=="ocp":
    from OCP.BRepTools import BRepTools; from OCP.BRep import BRep_Builder; from OCP.TopoDS import TopoDS_Shape
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape; from OCP.BRepAlgoAPI import BRepAlgoAPI_Common; from OCP.GProp import GProp_GProps; from OCP.BRepGProp import BRepGProp
else:
    import cadquery
print(sys.argv[1], priv())
