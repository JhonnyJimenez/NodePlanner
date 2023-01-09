from PyQt5.QtGui import QImage

from lib.nodeeditor.GraficosdelNodo import *

DEBUG = False


class GraficadordelNodoBase(GraficosdelNodo):

	def init_sizes(self):
		self.redondez_del_nodo = 7.0
		self.márgen = 10.0
		self.altura_del_título = 26.0
		self.sangría_del_título = int(self.márgen)
		self.sangría_vertical_del_título = 4.0

		if self.redondez_del_nodo > self.altura_del_título / 2:
			self.redondez_del_nodo = self.altura_del_título / 2

		try:
			if self.contenido.lista_de_anchuras:
				self.anchura_del_nodo = int(max(self.contenido.lista_de_anchuras) + (2 * self.márgen))
			else:
				self.anchura_del_nodo = int(2 * self.márgen)
				if DEBUG:
					self.anchura_del_nodo = 180
		except:
			self.anchura_del_nodo = 180

		try:
			self.altura_del_nodo = int(
					self.altura_del_título
					+ (2* self.márgen)
					+ self.contenido.lista_de_alturas[-1]
					- self.contenido.espaciado
					)
		except:
			self.altura_del_nodo = int(
					self.altura_del_título
					+ (2 * self.márgen)
					+ (20 * 8)
					+ (5 * 7)
					)

	def init_assets(self):
		super().init_assets()
		self._fuente_del_título = QFont(self.contenido.nombre_de_la_fuente, 10)
		self.íconos = QImage("lib/examples/example_calculator/iconos/status_icons.png")
		self._relleno_del_fondo = QBrush(QColor("#FF303030"))

	def titulo_del_nodo(self):
		super().titulo_del_nodo()
		self.título_del_objeto.setPos(self.sangría_del_título, 0)

	def actualizador_si_se_mueve_el_nodo(self):
		# ¡Optimízame! ¡Solo actualizo los nodos seleccionados!
		for nodo in self.scene().escena.nodos:
			for zocalo in nodo.entradas + nodo.salidas:
				for conexion in zocalo.Zocaloconexiones:
					conexion.graficador_de_conexiones.definir_color_desde_el_zocalo()
			if nodo.Nodograficas.isSelected():
				nodo.actualizar_conexiones()
		self._elemento_movido = True

	def paint(self, dibujante, estilo: QStyleOptionGraphicsItem, widget = None):
		super().paint(dibujante, estilo, widget)

		offset = 24.0
		if self.nodo.es_indefinido():
			offset = 0.0
		if self.nodo.es_inválido():
			offset = 48.0

		dibujante.drawImage(
				QRectF(-10, -10, 24.0, 24.0),
				self.íconos,
				QRectF(offset, 0, 24.0, 24.0)
				)