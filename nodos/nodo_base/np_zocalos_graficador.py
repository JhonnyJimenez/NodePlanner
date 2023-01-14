from PyQt5.QtWidgets import QStyleOptionGraphicsItem
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt, QRectF, QPointF

from lib.nodeeditor.GraficosdeZocalos import GraficosdeZocalos

COLORES_DE_ZOCALOS = [
		QColor("#FFcca6d6"),  # 0. Zócalo todoterreno
		QColor("#FF598c5c"),  # 1. Zócalo númerico
		QColor("#FFa1a1a1"),  # 2. Zócalo temporal
		QColor("#FFcca6d6"),  # 3. Zócalo booleano
		QColor("#FF70b2ff"),  # 4. Zócalo de texto
		QColor("#FF633863"),  # 5. Zócalo para listas desplegables
		QColor("#FF6363c7"),  # 6. Zócalo vectorial
		QColor("#FFc7c729"),  # 7. Zócalo de color
		QColor("#FFed9e5c"),  # 8. Zócalo de objeto
		QColor("#FF00d6a3"),  # 9. Zócalo de geometría (Únicamente para zócalos de entrada en un nodo Salida)
		QColor("#FFf5f5f5"),  # 10. Zócalo de colecciones
		QColor("#FF9e4fa3"),  # 11. Zócalo de texturas
		QColor("#FFeb7582"),  # 12. Zócalo de material
		]

# ZOCALOS_ROMBOS = [1, 2, 3, 6, 7]


class NodoBaseGraficadordeZocalos(GraficosdeZocalos):
	def __init__(self, zocalo):
		super().__init__(zocalo)

	def init_ui(self):
		self.figura = self.zocalo.forma
		self.radio = 6.0
		self.tamaño_rombo = self.radio
		self.tamaño_rombo_interno = self.tamaño_rombo * 0.30
		self.grosor_contorno = 1.0

		if self.figura in ('Diamante', 'Rombo'):
			self.tamaño = self.tamaño_rombo
		else:
			self.tamaño = self.radio

	def obtener_color_para_el_zocalo(self, key):
		if type(key) == int:
			if len(COLORES_DE_ZOCALOS) - 1 < key:
				return Qt.transparent
			return COLORES_DE_ZOCALOS[key]
		elif type(key) == str:
			return QColor(key)
		return Qt.transparent

	def boundingRect(self):
		return QRectF(
				-self.tamaño - self.grosor_contorno,
				-self.tamaño - self.grosor_contorno,
				2 * (self.tamaño + self.grosor_contorno),
				2 * (self.tamaño + self.grosor_contorno),
				)

	def rombo(self):
		rombo = (
				QPointF(0.0, -self.tamaño_rombo), QPointF(self.tamaño_rombo, 0.0),
				QPointF(0.0, self.tamaño_rombo), QPointF(-self.tamaño_rombo, 0.0)
				)
		return rombo

	def paint(self, painter, estilo: QStyleOptionGraphicsItem, widget=None):
		painter.setBrush(self._brush)
		painter.setPen(self._lápiz if not self.isHighlighted else self._lápiz_highlight)

		if self.figura in ('Rombo', 'Diamante'):
			painter.drawPolygon(self.rombo())

			if self.figura == 'Diamante':
				rombo_pequeño = (
									QPointF(0.0, -self.tamaño_rombo_interno), QPointF(self.tamaño_rombo_interno, 0.0),
									QPointF(0.0, self.tamaño_rombo_interno), QPointF(-self.tamaño_rombo_interno, 0.0)
									)
				self._brush_nuevo = QBrush(self._color_contorno)
				painter.setBrush(self._brush_nuevo)
				painter.drawPolygon(rombo_pequeño)

		else:
			painter.drawEllipse(QRectF(-self.radio, -self.radio, 2 * self.radio, 2 * self.radio))
