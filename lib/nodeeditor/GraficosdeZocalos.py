from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QRectF

COLORES_DE_ZOCALOS =[
	QColor("#FFFF7700"),
	QColor("#FF52e220"),
	QColor("#FF0056a6"),
	QColor("#FFa86db1"),
	QColor("#FFb54747"),
	QColor("#FFdbe220"),
]

class GraficosdeZocalos(QGraphicsItem):
	def __init__(self, zocalo):
		super().__init__(zocalo.nodo.Nodograficas)
		self.zocalo = zocalo

		self.isHighlighted = False

		self.init_ui()
		self.init_assets()

	def init_ui(self):
		self.radio = 6.0
		self.grosor_contorno = 1.0
	
	@property
	def tipo_zocalo(self):
		return self.zocalo.tipo_zocalo
		
	def obtener_color_para_el_zocalo(self, key):
		if type(key) == int: return COLORES_DE_ZOCALOS[key]
		elif type(key) == str: return QColor(key)
		return Qt.transparent
	
	def cambiar_tipo_de_zocalo(self):
		self._color_de_fondo = self.obtener_color_para_el_zocalo(self.tipo_zocalo)
		self._brush = QBrush(self._color_de_fondo)
		self.update()
		
	def init_assets(self):
		self._color_de_fondo = self.obtener_color_para_el_zocalo(self.tipo_zocalo)
		self._color_contorno = QColor("#FF000000")
		self._color_highlight = QColor("#FF37A6FF")
		
		self._lápiz = QPen(self._color_contorno)
		self._lápiz.setWidthF(self.grosor_contorno)
		self._lápiz_highlight = QPen(self._color_highlight)
		self._lápiz_highlight.setWidthF(2.0)
		self._brush = QBrush(self._color_de_fondo)
		
	def paint(self, painter, estilo: QStyleOptionGraphicsItem, widget=None):
		# Dibujando el círculo
		painter.setBrush(self._brush)
		painter.setPen(self._lápiz if not self.isHighlighted else self._lápiz_highlight)
		painter.drawEllipse(QRectF(-self.radio, -self.radio, 2 * self.radio, 2 * self.radio))
		
	def boundingRect(self):
		return QRectF(
			-self.radio - self.grosor_contorno,
			-self.radio - self.grosor_contorno,
			2 * (self.radio + self.grosor_contorno),
			2 * (self.radio + self.grosor_contorno),
		)
	
	# def mousePressEvent(self, QGraphicsSceneMouseEvent):
	# 	pass
	# 	# print('El zócalo ha sido presionado')
