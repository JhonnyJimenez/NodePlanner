from PyQt5.QtGui import QBrush, QColor

from np_enlistado_de_nodos import *
from nodos.nodo_base.np_nodo_base import NodoBase
from nodos.nodo_base.np_nodo_contenido import ContenidodelNodoBase
from nodos.nodo_base.np_nodo_graficador import GraficadordelNodoBase

from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_entrada import Entrada, VALIDANTE_NUMÉRICO
from nodos.objetos.np_booleana import Booleana


class GraficadordelosNodosdeEntrada(GraficadordelNodoBase):
	def init_assets(self):
		super().init_assets()
		self._relleno_del_título = QBrush(QColor("#FF83314A"))


class ContenidodelosNodosdeEntrada(ContenidodelNodoBase):
	def configuraciones(self):
		super().configuraciones()
		self.anchura = 130

	def contenido(self):
		self.contenido_de_salidas = [
				Etiqueta(self, 'Número', 'Entrada 1', 3, zócalo = 0),
				Etiqueta(self, 'Cadena', 'Entrada 2', 3, zócalo = 1),
				Etiqueta(self, 'Booleana', 'Entrada 3', 3, zócalo = 2),
				]
		self.contenido_de_entradas = [
				Entrada(self, '0', 'Entrada 1', validante = VALIDANTE_NUMÉRICO),
				Entrada(self, '', 'Entrada 2'),
				Booleana(self, 'Valor', 'Entrada 3', 1, True)
				]


@registrar_nodo(CATEGORÍA_ENTRADAS)
class NodosdeEntrada(NodoBase):
	icono = "iconos/categoría entradas.svg"
	codigo_op = CATEGORÍA_ENTRADAS
	titulo_op = "Entradas"

	ClaseGraficadeNodo = GraficadordelosNodosdeEntrada
	ClasedelContenidodeNodo = ContenidodelosNodosdeEntrada

	Entradas = []
	Salidas = [1, 4, 3]

	FormaDeEntradas = []
	FormaDeSalidas = ['Círculo', 'Círculo', 'Círculo']

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)