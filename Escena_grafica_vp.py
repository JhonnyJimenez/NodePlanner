# Escena gráfica (Ventana_principal).
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene

        # Configuraciones
        self.GrillaSize = 20
        self.GrillaCuadros = 5

        self.ColorDeFondo = QColor("#393939")
        self.ColorClaro = QColor("#2f2f2f")
        self.ColorOscuro = QColor("#292929")

        self.LapizClaro = QPen(self.ColorClaro)
        self.LapizClaro.setWidth(1)
        self.LapizOscuro = QPen(self.ColorOscuro)
        self.LapizOscuro.setWidth(2)

        self.setBackgroundBrush(self.ColorDeFondo)

    def ConfigEscenaGrafica(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # La grilla, we.
        izq = int(math.floor(rect.left()))
        der = int(math.ceil(rect.right()))
        techo = int(math.floor(rect.top()))
        piso = int(math.ceil(rect.bottom()))

        marco_izq = izq - (izq % self.GrillaSize)
        marco_techo = techo - (techo % self.GrillaSize)

        # Cálculo las líneas a dibujar.
        LineasClaras, LineasOscuras = [], []
        for x in range(marco_izq, der, self.GrillaSize):
            if x % (self.GrillaSize * self.GrillaCuadros) != 0:
                LineasClaras.append(QLine(x, techo, x, piso))
            else:
                LineasOscuras.append(QLine(x, techo, x, piso))
        for y in range(marco_techo, piso, self.GrillaSize):
            if y % (self.GrillaSize * self.GrillaCuadros) != 0:
                LineasClaras.append(QLine(izq, y, der, y))
            else:
                LineasOscuras.append(QLine(izq, y, der, y))

        # Las líneas.
        painter.setPen(self.LapizClaro)
        painter.drawLines(*LineasClaras)

        painter.setPen(self.LapizOscuro)
        painter.drawLines(*LineasOscuras)
