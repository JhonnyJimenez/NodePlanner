from nodos.nodo_base.np_nodo_base import *

imagen = "C:/Users/Maste/Downloads/icons/edit.svg"


class Entradas_Graficador(NodoBaseGraficador):
	def init_sizes(self):
		super().init_sizes()
		self.anchoNodo = 120
		self.altoNodo = 139
		self.altoNodoparaCalculos = self.altoNodo
		self.calculo_de_altura_disponible()

	def init_assets(self):
		super().init_assets()
		self._relleno_titulo_nodo = QBrush(QColor("#FF83314A"))


class Entradas_Contenido(NodoBaseContenido):
	def contenidos(self):
		self.objeto_1 = self.entrada_de_línea(1, "")
		self.objeto_2 = self.entrada_de_línea(2, "0", validante = QIntValidator())
		self.objeto_3 = self.entrada_de_línea(3, "0.000", validante = QDoubleValidator())
		self.objeto_4 = self.entrada_booleana(4, 0, "Valor")

	def lista_a_serializar(self, res):
		res['Objeto_1'] = self.objeto_1.text()
		res['Objeto_2'] = self.objeto_2.text()
		res['Objeto_3'] = self.objeto_3.text()
		res['Objeto_4'] = self.objeto_4.checkState()

	def lista_a_desearializar(self, data):
		self.objeto_1.setText(data['Objeto_1'])
		self.objeto_2.setText(data['Objeto_2'])
		self.objeto_3.setText(data['Objeto_3'])
		self.objeto_4.setCheckState(data['Objeto_4'])


# @registrar_nodo(CATEGORIA_ENTRADAS)
class Entradas(NodoBase):
	icono = imagen
	codigo_op = CATEGORIA_ENTRADAS
	titulo_op = "Entrada"
	content_label_objname = "Entradas"

	ClaseGraficadeNodo = Entradas_Graficador
	ClasedelContenidodeNodo = Entradas_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [], salidas = [4, 1, 2, 3]):
		super().__init__(escena, titulo, entradas, salidas)

	def actualizacion(self):
		self.contenido.objeto_1.textChanged.connect(self.datos_de_entrada_cambiados)
		self.contenido.objeto_2.textChanged.connect(self.datos_de_entrada_cambiados)
		self.contenido.objeto_3.textChanged.connect(self.datos_de_entrada_cambiados)
		self.contenido.objeto_4.stateChanged.connect(self.datos_de_entrada_cambiados)

	def ediciones_de_espaciado(self):
		pass

	def ImplementarEvaluacion(self):
		self.Evaluacion_de_texto(self.contenido.objeto_1)
		self.Evaluacion_de_texto(self.contenido.objeto_2)
		self.Evaluacion_de_texto(self.contenido.objeto_3)
		self.EvaluacionBooleana(self.contenido.objeto_4)
		self.evaluar_hijos()
