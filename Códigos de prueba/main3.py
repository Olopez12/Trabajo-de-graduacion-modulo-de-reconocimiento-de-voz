from vedo import Mesh, Plotter
import numpy as np
import vtk

J0 = Mesh("PrimerSoporte.stl").c("gold")
J1_original = Mesh("PrimerSoporte.stl").c("gold")
J2 = Mesh("Brazo.stl").c("forestgreen")

J0.pos(0, 0, 0)
J0.rotate_z(-90)

plot = Plotter(title="UR5 con slider para J1", axes=1)

def actualizar_j1(angulo, slider_widget):
    plot.clear() 

    J1 = J1_original.clone().c("gold")
    J1.pos(-126, 0, 0)
    J1.rotate_x(180)
    J1.rotate_z(angulo)

    matrix_vtk = vtk.vtkMatrix4x4()
    J1.actor.GetMatrix(matrix_vtk)

    M1 = np.eye(4)
    for i in range(4):
        for j in range(4):
            M1[i, j] = matrix_vtk.GetElement(i, j)

    offset_local = np.array([-127, 370, 0, 1])
    offset_world = M1 @ offset_local
    J2_clone = J2.clone().pos(offset_world[:3])
    plot.show(J0, J1, J2_clone, resetcam=False)

plot.add_slider(
    actualizar_j1,
    -180, 180,
    value=0,
    title="Rotación Z de J1",
    pos=([0.1, 0.05], [0.9, 0.05])
)


actualizar_j1(0, None)  
