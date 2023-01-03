from PyQt5.QtWidgets import QCheckBox
from nodos.objetos.np_objeto_base import *


class Booleana(ObjetodeNodePlanner):
	def objeto(self):
		return QCheckBox

	def parámetros(self):
		return self.texto_inicial, self.elemento_padre

	def definir_posición_y_etiqueta(self):
		self.objeto.setGeometry(self.posición_x, self.posición_y, self.ancho, self.alto)

		self.etiqueta = QLabel(self.texto_inicial, self.elemento_padre)
		self.etiqueta.setGeometry(self.posición_x, self.posición_y, self.ancho, self.alto)
		self.etiqueta.setVisible(False)
		self.etiqueta.setStyleSheet('padding-left: 1px; background: transparent')
		self.etiqueta.setAlignment(Qt.AlignVCenter)
		self.etiqueta.setFont(self.fuente)

	def configuraciones_adicionales(self):
		if self.valor_inicial is None:
			self.objeto.setCheckState(2)
		else:
			self.objeto.setCheckState(self.valor_inicial)
		self.objeto.setTristate(self.indeterminado)

	def estilo(self):
		self.objeto.setStyleSheet('padding-left: 1px; color: #fff; background: transparent')

	def señal(self):
		self.objeto.stateChanged.connect(self.contenido_del_objeto)
		self.objeto.stateChanged.connect(self.elemento_padre.nodo.datos_de_entrada_cambiados)

	def contenido_del_objeto(self):
		self.elemento_padre.lista_de_información[self.índice] = self.objeto.checkState()

	def forma_de_deserialización(self):
		self.elemento_padre.lista_de_deserializamiento[self.índice] = self.objeto.setCheckState

	def ocultado_por_entrada(self):
		if self.es_visible and self.zócalo_de_entrada is not None:
			if self.elemento_padre.nodo.entradas[self.zócalo_de_entrada].Zocaloconexiones != []:
				self.objeto.setVisible(False)
				self.etiqueta.setVisible(True)
				self.es_visible = False

	def mostrado_por_entrada(self):
		if not self.es_visible and self.zócalo_de_entrada is not None:
			if self.elemento_padre.nodo.entradas[self.zócalo_de_entrada].Zocaloconexiones == []:
				self.objeto.setVisible(True)
				self.etiqueta.setVisible(False)
				self.es_visible = True