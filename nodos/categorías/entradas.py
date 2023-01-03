from PyQt5.QtGui import QBrush, QColor

from np_enlistado_de_nodos import *
from nodos.nodo_base.np_nodo_base import NodoBase
from nodos.nodo_base.np_nodo_contenido import ContenidodelNodoBase
from nodos.nodo_base.np_nodo_graficador import GraficadordelNodoBase
from nodos.objetos.np_entrada import Entrada, VALIDANTE_NUMÉRICO
from nodos.objetos.np_booleana import Booleana

imagen = "C:/Users/Maste/Downloads/icons/edit.svg"


class GraficadordelosNodosdeEntrada(GraficadordelNodoBase):
	def init_assets(self):
		super().init_assets()
		self._relleno_del_título = QBrush(QColor("#FF83314A"))


class ContenidodelosNodosdeEntrada(ContenidodelNodoBase):
	def controles(self):
		super().controles()
		self.placeholder(3)

	def configuraciones(self):
		super().configuraciones()
		self.anchura = 100

	def contenido(self):
		self.objeto_0 = Entrada(
				self, índice = 0, zócalo_de_salida = 0, texto_inicial = '0', validante = VALIDANTE_NUMÉRICO
				)
		self.objeto_1 = Entrada(
				self, índice = 1, zócalo_de_salida = 1, texto_inicial = ''
				)
		self.objeto_2 = Booleana(
				self, índice = 2, zócalo_de_salida = 2, texto_inicial = 'Valor',
				indeterminado = True, valor_inicial = 1
				)

# @registrar_nodo(CATEGORIA_ENTRADAS)
class NodosdeEntrada(NodoBase):
	icono = imagen
	codigo_op = CATEGORIA_ENTRADAS
	titulo_op = "Entradas"

	ClaseGraficadeNodo = GraficadordelosNodosdeEntrada
	ClasedelContenidodeNodo = ContenidodelosNodosdeEntrada

	Entradas = []
	Salidas = [1, 4, 3]

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)