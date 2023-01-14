from mpmath import mpf
from PyQt5.QtGui import QBrush, QColor

from np_enlistado_de_nodos import *
from nodos.nodo_base.np_nodo_base import NodoBase
from nodos.nodo_base.np_nodo_contenido import ContenidodelNodoBase
from nodos.nodo_base.np_nodo_graficador import GraficadordelNodoBase

from nodos.objetos.np_etiqueta import Etiqueta


class GraficadordelNodoCronista(GraficadordelNodoBase):
	def init_assets(self):
		super().init_assets()
		self._relleno_del_título = QBrush(QColor("#FF246283"))


class ContenidodelNodoCronista(ContenidodelNodoBase):
	def configuraciones(self):
		super().configuraciones()
		self.anchura = 130

	def contenido(self):
		self.contenido_de_salidas = [
				Etiqueta(self, 'Segundo inicial', 'Segundo inicial', 3, zócalo = 0)
				]
		self.contenido_de_entradas = [

				]


@registrar_nodo(CATEGORÍA_CRONISTAS)
class NodoCronista(NodoBase):
	icono = "iconos/categoría cronista.svg"
	codigo_op = CATEGORÍA_CRONISTAS
	titulo_op = "Cronistas"

	ClaseGraficadeNodo = GraficadordelNodoCronista
	ClasedelContenidodeNodo = ContenidodelNodoCronista

	Entradas = []
	Salidas = [2]

	FormaDeEntradas = []
	FormaDeSalidas = ['Círculo']

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)

	def métodos_de_evaluación(self):
		self.valores['Segundo inicial'] = mpf('0')
