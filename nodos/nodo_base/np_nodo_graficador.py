from PyQt5.QtGui import QImage

from lib.nodeeditor.GraficosdelNodo import *


class NodoBaseGraficador(GraficosdelNodo):

	def init_sizes(self):
		super().init_sizes()

		if self.redondez_del_nodo > self.altura_del_título / 2:
			self.redondez_del_nodo = self.altura_del_título / 2

	# 	self.sangria_de_la_orilla = 10.0  # Es el márgen desde cada orilla, arriba desde la etiqueta.
	# 	# self.alturaTituloNodo = 24.0  # Es la altura de la etiqueta donde está el título.
	# 	self.sangria_del_titulo = 10.0
	# 	# self.sangria_vertical_del_titulo = 4.0  # No sé qué hace esto :v
	# 	self.anchoNodo = 180
	# 	self.altoNodo = 164
	# 	self.altoNodoparaCalculos = self.altoNodo
	# 	self.calculo_de_altura_disponible()
	#
	# def calculo_de_altura_disponible(self):
	# 	self.altura_disponible = int(self.altoNodo - (2 * self.sangria_de_la_orilla) - self.alturaTituloNodo)
	# 	return self.altura_disponible
	#
	def init_assets(self):
		super().init_assets()
		self.íconos = QImage("../../lib/examples/example_calculator/iconos/status_icons.png")
		self._relleno_del_fondo = QBrush(QColor("#FF303030"))
	#
	# def mouseMoveEvent(self, evento):
	# 	super().mouseMoveEvent(evento)
	#
	# 	# ¡Optimízame! ¡Solo actualizo los nodos seleccionados!
	# 	for nodo in self.scene().escena.nodos:
	# 		for zocalo in nodo.entradas + nodo.salidas:
	# 			for conexion in zocalo.Zocaloconexiones:
	# 				conexion.graficador_de_conexiones.definir_color_desde_el_zocalo()
	# 		if nodo.Nodograficas.isSelected():
	# 			nodo.actualizarconexiones()
	# 	self._elemento_movido = True
	#
	# def paint(self, painter, QStyleOptionGraphicsItem, widget = None):
	# 	super().paint(painter, QStyleOptionGraphicsItem, widget)
	#
	# 	offset = 24.0
	# 	if self.nodo.esIndefinido():
	# 		offset = 0.0
	# 	if self.nodo.esInvalido():
	# 		offset = 48.0
	#
	# 	painter.drawImage(
	# 			QRectF(-10, -10, 24.0, 24.0),
	# 			self.iconos,
	# 			QRectF(offset, 0, 24.0, 24.0)
	# 			)