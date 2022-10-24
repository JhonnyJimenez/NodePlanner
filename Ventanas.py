from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from EscGraNod import QDMGraphicsScene
from VisGraNod import QDMGraphicsView


class EditorDeNodos(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initui()

    def initui(self):
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Crear escena de gráficos
        self.grScene = QDMGraphicsScene()

        # Crear vista de gráficos
        self.view = QDMGraphicsView(self.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Planificador con nodos")
        self.show()

        self.adddebugcontent()

    def adddebugcontent(self):
        lverde = QBrush(Qt.green)
        figcontorno = QPen(Qt.black)
        figcontorno.setWidth(2)

        rect = self.grScene.addRect(-100, -100, 80, 100, figcontorno, lverde)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.grScene.addText("¡Este es mi impresionante texto!", QFont("Please write me a song"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("¡Hola, mundo!")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)

        line = self.grScene.addLine(-200, -200, 400, -100, figcontorno)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)