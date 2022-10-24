from PyQt6.QtWidgets import *
from EscGraNod import QDMGraphicsScene


class EditorDeNodos(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initui()

    def initui(self):
        self.setGeometry(200, 200, 600, 400)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Crear escena de gráficos
        self.grScene = QDMGraphicsScene()

        # Crear vista de gráficos
        self.view = QGraphicsView(self)

        self.view.setScene(self.grScene)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Planificador con nodos")
        self.show()
