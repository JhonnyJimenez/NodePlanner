from PyQt5.QtGui import QBrush, QColor

from np_enlistado_de_nodos import *
from nodos.nodo_base.np_nodo_base import NodoBase
from nodos.nodo_base.np_nodo_contenido import ContenidodelNodoBase
from nodos.nodo_base.np_nodo_graficador import GraficadordelNodoBase

from nodos.objetos.np_etiqueta import Etiqueta


class GraficadordelNodoAstronómico(GraficadordelNodoBase):
	def init_assets(self):
		super().init_assets()
		self._relleno_del_título = QBrush(QColor("#FF1D2546"))


class ContenidodelNodoAstronómico(ContenidodelNodoBase):
	def configuraciones(self):
		super().configuraciones()
		self.anchura = 140

	def contenido(self):
		self.contenido_de_salidas = [
				Etiqueta(self)
				]
		self.contenido_de_entradas = [
				Etiqueta(self)
				]


@registrar_nodo(CATEGORÍA_ASTRONOMÍA)
class NodoAstronómico(NodoBase):
	icono = "iconos/categoría universo.svg"
	codigo_op = CATEGORÍA_ASTRONOMÍA
	titulo_op = "Astrónomos"

	ClaseGraficadeNodo = GraficadordelNodoAstronómico
	ClasedelContenidodeNodo = ContenidodelNodoAstronómico

	Entradas = []
	Salidas = []

	FormadeEntradas = []
	FormadeSalidas = []

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)
