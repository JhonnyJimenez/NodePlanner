from Escena_grafica_vp import QDMGraphicsScene

class Escena ():
    def __init__(self):
        self.Nodos = []
        self.Bordes = []

        self.Escena_Ancho = 64000
        self.Escena_Alto = 64000

        self.initUI()

    def initUI(self):
        self.Esc_grafica = QDMGraphicsScene(self)
        self.Esc_grafica.ConfigEscenaGrafica(self.Escena_Ancho, self.Escena_Alto)

    def AgregarNodo(self, Nodo):
        self.Nodos.append(Nodo)

    def AgregarBorde(self, Borde):
        self.Bordes.append(Borde)

    def EliminarNodo(self, Nodo):
        self.Nodos.remove(Nodo)

    def EliminarBorde(self, Borde):
        self.Bordes.remove(Borde)
