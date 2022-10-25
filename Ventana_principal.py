from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Escena import Escena
from Nodo import Nodo
from Vista_grafica_vp import QDMGraphicsView


class EditorDeNodos(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)

        # Administrador de espacio en pantalla
        self.AdminDeEspEnPan = QVBoxLayout()
        self.AdminDeEspEnPan.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.AdminDeEspEnPan)

        # Crear escena de gráficos
        self.scene = Escena()
        # self.Esc_grafica = self.scene.Esc_grafica

        Nodos = Nodo(self.scene, "Nodo de personaje")

        # Crear vista de gráficos
        self.Vista_grafica = QDMGraphicsView(self.scene.Esc_grafica, self)
        self.AdminDeEspEnPan.addWidget(self.Vista_grafica)

        self.setWindowTitle("NodePlanner - Versión alpha")
        self.show()

        # self.AddDebugContent()

    def AddDebugContent(self):
        lverde = QBrush(Qt.green)
        figcontorno = QPen(Qt.black)
        figcontorno.setWidth(2)

        rect = self.Esc_grafica.addRect(-100, -100, 80, 100, figcontorno, lverde)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.Esc_grafica.addText("¡Este es mi impresionante texto!", QFont("Please write me a song"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("¡Hola, mundo!")
        proxy1 = self.Esc_grafica.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.Esc_grafica.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)

        line = self.Esc_grafica.addLine(-200, -200, 400, -100, figcontorno)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)