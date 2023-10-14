from PyQt5.QtWidgets import QCheckBox, QLabel
from PyQt5.QtCore import Qt
from nodos.objetos.np_objeto_base import ObjetodeNodePlanner
from np_constantes import NOMBRE_DEL_PRODUCTO


class Booleana(ObjetodeNodePlanner):
	def __init__(
			self, elemento_padre = None, texto: str = NOMBRE_DEL_PRODUCTO, llave: str = None,
			valor: int = None, indeterminado = False, con_dos_puntos = False, **kwargs
			):
		self.valor = valor
		self.indeterminado = indeterminado
		super().__init__(elemento_padre, llave = llave, con_dos_puntos = con_dos_puntos, etiqueta = texto, **kwargs)

	def definir_objeto(self):
		return QCheckBox('', self.elemento_padre)

	def estilo(self):
		self.objeto.setStyleSheet('padding-left: 1px; color: #fff; background: transparent')

	def posición_y_tamaño(self):
		self.objeto.setGeometry(self.posición_x, self.posición_y, self.anchura, self.altura)

		if self.texto_de_la_etiqueta[-1] != ':':
			self.texto_sin_puntos = self.texto_de_la_etiqueta
			self.texto_con_puntos = self.texto_de_la_etiqueta + ':'
		else:
			self.texto_sin_puntos = self.texto_de_la_etiqueta.replace(":", "")
			self.texto_con_puntos = self.texto_de_la_etiqueta

		if self.con_dos_puntos:
			self.etiqueta = QLabel(self.texto_con_puntos, self.elemento_padre)
		else:
			self.etiqueta = QLabel(self.texto_sin_puntos, self.elemento_padre)

		self.etiqueta.setGeometry(self.posición_x + 15, self.posición_y, self.anchura - 15, self.altura)
		self.etiqueta.setStyleSheet('padding-left: 1px; background: transparent')
		self.etiqueta.setAlignment(Qt.AlignVCenter)
		self.etiqueta.setFont(self.fuente)

	def configuraciones_adicionales(self):
		self.objeto.setTristate(self.indeterminado)
		if self.valor is None:
			self.objeto.setCheckState(2)
		else:
			self.objeto.setCheckState(self.valor)

	def señal(self):
		self.objeto.stateChanged.connect(self.contenido)
		self.objeto.stateChanged.connect(self.elemento_padre.nodo.datos_de_entrada_cambiados)

	def escribir_dato(self):
		return self.objeto.checkState()

	def deserialización(self, dato):
		self.objeto.setCheckState(dato)

	def widget_conectado(self):
		try:
			if self.visible and self.es_entrada and self.zócalo is not None:
				if self.elemento_padre.nodo.entradas[self.zócalo].Zocaloconexiones != []:
					self.objeto.setVisible(False)
					self.visible = False
					if self.texto_de_la_etiqueta != '' and self.texto_de_la_etiqueta is not None:
						self.etiqueta.setGeometry(self.posición_x, self.posición_y, self.anchura, self.altura)
		except IndexError:
			pass

	def widget_desconectado(self):
		try:
			if not self.oculto:
				if not self.visible and self.es_entrada and self.zócalo is not None:
					if self.elemento_padre.nodo.entradas[self.zócalo].Zocaloconexiones == []:
						self.objeto.setVisible(True)
						self.visible = True
						if self.texto_de_la_etiqueta != '' and self.texto_de_la_etiqueta is not None:
							self.etiqueta.setGeometry(
									self.posición_x + 15, self.posición_y,
									self.anchura - 15, self.altura
									)
							if self.con_dos_puntos:
								self.etiqueta.setText(self.texto_con_puntos)
							else:
								self.etiqueta.setText(self.texto_sin_puntos)
		except IndexError:
			pass
