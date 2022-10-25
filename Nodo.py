from Nodo_graficas import QDMGraphicsNode

class Nodo():
    def __init__(self, scene, title="Nodo desconocido"):
        self.scene = scene
        self.title = title

        self.Nodograficas = QDMGraphicsNode(self, self.title)

        self.scene.AgregarNodo(self)
        self.scene.Esc_grafica.addItem(self.Nodograficas)

        self.inputs = []
        self.outputs = []
