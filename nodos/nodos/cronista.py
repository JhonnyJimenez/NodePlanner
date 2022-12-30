from nodos.nodo_base.np_nodo_base import *

imagen = "C:/Users/Maste/Downloads/icons/time.svg"


class Cronista_Graficador(NodoBaseGraficador):
	def init_sizes(self):
		super().init_sizes()
		self.anchoNodo = 120
		self.altoNodo = 64
		self.altoNodoparaCalculos = self.altoNodo
		self.calculo_de_altura_disponible()

	def init_assets(self):
		super().init_assets()
		self._relleno_titulo_nodo = QBrush(QColor("#FF246283"))


class Cronista_Contenido(NodoBaseContenido):
	def contenidos(self):
		self.etiqueta_1 = self.etiqueta("Segundo inicial", "Derecha")

	def lista_a_serializar(self, res):
		pass

	def lista_a_desearializar(self, data):
		pass


# @registrar_nodo(NODO_CRONISTA)
class Cronista(NodoBase):
	icono = imagen
	codigo_op = NODO_CRONISTA
	titulo_op = "Cronista"
	content_label_objname = "Cronista"

	ClaseGraficadeNodo = Cronista_Graficador
	ClasedelContenidodeNodo = Cronista_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [], salidas = [2]):
		super().__init__(escena, titulo, entradas, salidas)

	def actualizacion(self):
		pass

	def ediciones_de_espaciado(self):
		pass

	def ImplementarEvaluacion(self):
		self.valores[0] = 0
		self.evaluar_hijos()
