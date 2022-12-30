from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QPointF, QRectF

from lib.nodeeditor.GraficosdeZocalos import *

COLORES_DE_ZOCALOS = [
		QColor("#FFcca6d6"),  # 0. Zócalo de entrada y salida todoterreno
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

ZOCALOS_ROMBOS = [1, 2, 3, 6, 7]


class NodoBaseGraficadordeZocalos(GraficosdeZocalos):
	pass
	# def init_assets(self):
	# 	super().init_assets()
	#
	# def obtener_color_para_el_zocalo(self, key):
	# 	if type(key) == int:
	# 		if len(COLORES_DE_ZOCALOS) - 1 < key:
	# 			return Qt.transparent
	# 		return COLORES_DE_ZOCALOS[key]
	# 	elif type(key) == str:
	# 		return QColor(key)
	# 	return Qt.transparent
	#
	# def paint(self, painter: QPainter, QStyleOptionGraphicsItem, widget=None):
	# 	painter.setBrush(self._brush)
	# 	painter.setPen(self._lápiz if not self.isHighlighted else self._pen_highlight)
	#
	# 	if self.tipo_zocalo in ZOCALOS_ROMBOS:
	# 		self.nuevo_radio_1 = self.radio * 1.20
	#
	# 		rombo = (
	# 					QPointF(0.0, -self.nuevo_radio_1), QPointF(self.nuevo_radio_1, 0.0),
	# 					QPointF(0.0, self.nuevo_radio_1), QPointF(-self.nuevo_radio_1, 0.0)
	# 				)
	# 		painter.drawPolygon(rombo)
	#
	# 		self.nuevo_radio = self.radio * 0.30
	# 		rombo_pequeño = (
	# 							QPointF(0.0, -self.nuevo_radio), QPointF(self.nuevo_radio, 0.0),
	# 							QPointF(0.0, self.nuevo_radio), QPointF(-self.nuevo_radio, 0.0)
	# 							)
	#
	# 		self._brush_nuevo = QBrush(self._color_contorno)
	# 		painter.setBrush(self._brush_nuevo)
	# 		painter.drawPolygon(rombo_pequeño)
	#
	# 	else:
	# 		painter.drawEllipse(QRectF(-self.radio, -self.radio, 2 * self.radio, 2 * self.radio))
