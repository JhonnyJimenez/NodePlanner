from np_nodo_base import *

imagen = "C:/Users/Maste/Downloads/icons/star.svg"


class Universo_Graficador(NodoBase_Graficador):
	def initSizes(self):
		super().initSizes()
		self.anchoNodo = 120
		self.altoNodo = 114
		self.altoNodoparaCalculos = self.altoNodo
		self.calculo_de_altura_disponible()

	def initAssets(self):
		super().initAssets()
		self._relleno_titulo_nodo = QBrush(QColor("#FF1D2546"))


class Universo_Contenido(NodoBase_Contenido):
	def contenidos(self):
		self.objeto_1 = self.entrada_de_línea(1, "", "Nombre")
		self.etiqueta_1 = self.etiqueta("", "Centro")
		self.etiqueta_1.setGeometry(
				0, self.objeto_1.posicion_y,
				self.ancho_disponible, self.altura_por_defecto
				)
		self.posicion_libre[-1] -= (self.altura_por_defecto + self.espaciado_entre_objetos_del_nodo)
		self.etiqueta_1.hide()
		self.objeto_2 = self.entrada_de_línea(2, '0', 'Segundo inicial', VALIDANTE_NUMÉRICO)

	def lista_a_serializar(self, res):
		res['Objeto_1'] = self.objeto_1.text()
		res['Objeto_2'] = self.objeto_2.text()

	def lista_a_desearializar(self, data):
		self.objeto_1.setText(data['Objeto_1'])
		self.objeto_2.setText(data['Objeto_2'])


@registrar_nodo(NODO_UNIVERSO)
class Universo(NodoBase):
	icono = imagen
	codigo_op = NODO_UNIVERSO
	titulo_op = "Universo"
	content_label_objname = "Universo"

	ClaseGraficadeNodo = Universo_Graficador
	ClasedelContenidodeNodo = Universo_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [4, 2], salidas = [4, 2]):
		super().__init__(escena, titulo, entradas, salidas)

	def initConfiguraciones(self):
		super().initConfiguraciones()
		self.pos_det_entradas = Izquierda_arriba

	def universo_real(self):
		self.entradas[0].quitar_todas_las_conexiones(True)
		self.entradas[0].GraficosZocalos.setVisible(False)
		self.contenido.objeto_1.hide()
		self.contenido.etiqueta_1.setText(self.contenido.objeto_1.text())
		self.contenido.etiqueta_1.show()

	def actualizacion(self):
		self.contenido.objeto_1.textChanged.connect(self.DatosdeEntradaCambiados)
		self.contenido.objeto_2.textChanged.connect(self.DatosdeEntradaCambiados)

	def ediciones_de_espaciado(self):
		pass

	def DatosdeEntradaCambiados(self, zocalo = None):
		self.marcarIndefinido()

		if self.contenido.objeto_1.text() == "Universo real":
			self.universo_real()

		self.evaluar()

	def ImplementarEvaluacion(self):
		entrada_1 = self.obtenerContrazocalo(0)
		entrada_2 = self.obtenerContrazocalo(1)

		if entrada_1 is not None:
			self.contenido.objeto_1.setVisible(False)
			self.contenido.objeto_1.etiqueta.setGeometry(0, self.contenido.objeto_1.posicion_y, self.contenido.ancho_disponible, self.contenido.objeto_1.altura)
			self.contenido.objeto_1.etiqueta.setText(self.contenido.objeto_1.etiqueta.text().replace(":", ""))
			self.valores_entrantes[0] = entrada_1.nodo.valores[entrada_1.indice]
		else:
			self.contenido.objeto_1.setVisible(True)
			self.contenido.objeto_1.etiqueta.setGeometry(0, self.contenido.objeto_1.posicion_y, self.contenido.ancho_etiqueta, self.contenido.objeto_1.altura)
			if self.contenido.objeto_1.etiqueta.text()[-1] != ':':
				self.contenido.objeto_1.etiqueta.setText(self.contenido.objeto_1.etiqueta.text() + ":")
			self.valores_entrantes[0] = self.contenido.objeto_1.text()

		if entrada_2 is not None:
			self.contenido.objeto_2.setVisible(False)
			self.contenido.objeto_2.etiqueta.setGeometry(0, self.contenido.objeto_2.posicion_y, self.contenido.ancho_disponible, self.contenido.objeto_2.altura)
			self.contenido.objeto_2.etiqueta.setText(self.contenido.objeto_2.etiqueta.text().replace(":", ""))
			self.valores_entrantes[1] = entrada_2.nodo.valores[entrada_2.indice]
		else:
			self.contenido.objeto_2.setVisible(True)
			self.contenido.objeto_2.etiqueta.setGeometry(0, self.contenido.objeto_2.posicion_y, self.contenido.ancho_etiqueta, self.contenido.objeto_2.altura)
			if self.contenido.objeto_2.etiqueta.text()[-1] != ':':
				self.contenido.objeto_2.etiqueta.setText(self.contenido.objeto_2.etiqueta.text() + ":")
			self.valores_entrantes[1] = self.contenido.objeto_2.text()

			self.valores = self.valores_entrantes

		self.marcarIndefinido(False)
		self.marcarInvalido(False)
		self.Nodograficas.setToolTip("")
		self.evaluarHijos()
