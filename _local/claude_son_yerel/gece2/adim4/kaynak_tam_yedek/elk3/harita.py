import numpy as np
h=5.0
for xf in (2500,4000,4400):
    L=np.load("dep_%d_L.npy"%xf); R=np.load("dep_%d_R.npy"%xf)
    print("=== face",xf," rows y(top->down) every 40mm, cols z -830..80 every 20mm; char: min(L,R) free depth: '#'<40 '+'<80 '-'<130 '.'>=130 ; L/R separately below")
    for nmz,M in (("MIN",np.minimum(L,R)),("L",L),("R",R)):
        print("--",nmz)
        for y in range(2160,0,-40):
            iy=int(y/h); row=""
            for z in range(-825,80,20):
                iz=int((z+830)/h)
                d=M[iy-2:iy+3, max(iz-2,0):iz+2].min()
                row+="#" if d<40 else "+" if d<80 else "-" if d<130 else "."
            print("%5d %s"%(y,row))
