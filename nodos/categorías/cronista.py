from PyQt5.QtGui import QBrush, QColor

from np_enlistado_de_nodos import *
from nodos.nodo_base.np_nodo_base import NodoBase
from nodos.nodo_base.np_nodo_contenido import ContenidodelNodoBase
from nodos.nodo_base.np_nodo_graficador import GraficadordelNodoBase
from nodos.objetos.np_etiqueta import Etiqueta

imagen = "C:/Users/Maste/Downloads/icons/time.svg"


class GraficadordelNodoCronista(GraficadordelNodoBase):
	def init_assets(self):
		super().init_assets()
		self._relleno_del_título = QBrush(QColor("#FF246283"))


class ContenidodelNodoCronista(ContenidodelNodoBase):
	def controles(self):
		super().controles()
		self.placeholder(1)

	def configuraciones(self):
		super().configuraciones()
		self.anchura = 100

	def contenido(self):
		self.objeto_0 = Etiqueta(
				self, índice = 0, zócalo_de_salida = 0, texto_inicial = 'Segundo inicial', alineado = 'Derecha'
				)


@registrar_nodo(NODO_CRONISTA)
class NodoCronista(NodoBase):
	icono = imagen
	codigo_op = NODO_CRONISTA
	titulo_op = "Nodo cronista"

	ClaseGraficadeNodo = GraficadordelNodoCronista
	ClasedelContenidodeNodo = ContenidodelNodoCronista

	Entradas = []
	Salidas = [2]

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)

	def métodos_de_evaluación(self):
		self.valores_de_salida[0] = 0
