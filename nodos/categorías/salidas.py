from nodos.nodo_base.np_nodo_base import *

imagen = "C:/Users/Maste/Downloads/icons/visibility.svg"


class Salidas_Graficador(NodoBaseGraficador):
	def init_sizes(self):
		super().init_sizes()
		self.anchoNodo = 120
		self.altoNodo = 64
		self.altoNodoparaCalculos = self.altoNodo
		self.calculo_de_altura_disponible()

	def init_assets(self):
		super().init_assets()
		self._relleno_titulo_nodo = QBrush(QColor("#FF3C1D26"))


class Salidas_Contenido(NodoBaseContenido):
	def contenidos(self):
		self.etiqueta_1 = self.etiqueta("", "Centro", altura = self.altura_disponible)

	def lista_a_serializar(self, res):
		pass

	def lista_a_desearializar(self, data):
		pass


# @registrar_nodo(CATEGORIA_SALIDAS)
class Salidas(NodoBase):
	icono = imagen
	codigo_op = CATEGORIA_SALIDAS
	titulo_op = "Salida"
	content_label_objname = "Salidas"

	ClaseGraficadeNodo = Salidas_Graficador
	ClasedelContenidodeNodo = Salidas_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [0], salidas = []):
		super().__init__(escena, titulo, entradas, salidas)

	def actualizacion(self):
		pass

	def ediciones_de_espaciado(self):
		pass

	def ImplementarEvaluacion(self):
		nodo_de_entrada = self.obtener_entrada(0)
		if not nodo_de_entrada:
			self.Nodograficas.setToolTip("No hay un nodo conectado.")
			self.marcar_inválido()
			self.contenido.etiqueta_1.setText("Sin datos.")
			return

		contrazocalo = self.obtenerContrazocalo(0)
		valor = nodo_de_entrada.valores[contrazocalo.indice]

		if valor == '' or valor is None:
			self.Nodograficas.setToolTip("No hay datos en el nodo conectado.")
			self.marcar_indefinido()
			self.contenido.etiqueta_1.setText("Sin datos.")
			return

		valor = self.textualizador(valor)

		valor = str(valor)

		self.contenido.etiqueta_1.setText(valor)
		self.marcar_indefinido(False)
		self.marcar_inválido(False)
		self.Nodograficas.setToolTip("")

		return valor
