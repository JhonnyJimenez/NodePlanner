# Escena gráfica de los nodos
import math
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Configuraciones
        self.gridSize = 20
        self.gridSquares = 5

        self.colorfondo = QColor("#393939")
        self.colorclaro = QColor("#2f2f2f")
        self.coloroscuro = QColor("#292929")

        self.lapizclaro = QPen(self.colorclaro)
        self.lapizclaro.setWidth(1)
        self.lapizoscuro = QPen(self.coloroscuro)
        self.lapizoscuro.setWidth(2)

        self.scene_width, self.scene_height = 64000, 64000
        self.setSceneRect(-self.scene_width//2, -self.scene_height//2, self.scene_width, self.scene_height)

        self.setBackgroundBrush(self.colorfondo)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # La grilla, we.
        izq = int(math.floor(rect.left()))
        der = int(math.ceil(rect.right()))
        techo = int(math.floor(rect.top()))
        piso = int(math.ceil(rect.bottom()))

        marizq = izq - (izq % self.gridSize)
        martecho = techo - (techo & self.gridSize)

        # Cálculo las líneas a dibujar.
        lineasclaras, lineasoscuras = [], []
        for x in range(marizq, der, self.gridSize):
            if x % (self.gridSize * self.gridSquares) != 0:
                lineasclaras.append(QLine(x, techo, x, piso))
            else:
                lineasoscuras.append(QLine(x, techo, x, piso))
        for y in range(martecho, piso, self.gridSize):
            if y % (self.gridSize * self.gridSquares) != 0:
                lineasclaras.append(QLine(izq, y, der, y))
            else:
                lineasoscuras.append(QLine(izq, y, der, y))

        # Las líneas.
        painter.setPen(self.lapizclaro)
        painter.drawLines(*lineasclaras)

        painter.setPen(self.lapizoscuro)
        painter.drawLines(*lineasoscuras)
