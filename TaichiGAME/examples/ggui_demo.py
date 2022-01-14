import taichi as ti

ti.init(arch=ti.cpu)

window = ti.ui.Window('Window Title', (640, 360))
while window.running:
    window.show()
