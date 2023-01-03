from PyQt5.QtGui import QBrush, QColor

from np_enlistado_de_nodos import *
from nodos.nodo_base.np_nodo_base import NodoBase
from nodos.nodo_base.np_nodo_contenido import ContenidodelNodoBase
from nodos.nodo_base.np_nodo_graficador import GraficadordelNodoBase
from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_entrada import Entrada, VALIDANTE_NUMÉRICO

imagen = "C:/Users/Maste/Downloads/icons/star.svg"


class GraficadordelNodoUniverso(GraficadordelNodoBase):
	def init_assets(self):
		super().init_assets()
		self._relleno_del_título = QBrush(QColor("#FF1D2546"))


class ContenidodelNodoUniverso(ContenidodelNodoBase):
	def controles(self):
		super().controles()
		self.placeholder(3)

	def configuraciones(self):
		super().configuraciones()
		self.anchura = 140

	def contenido(self):
		self.objeto_0 = Entrada(
				self, índice = 0, zócalo_de_entrada = 0, zócalo_de_salida = 0, texto_inicial = '', etiqueta = 'Nombre',
				proporción = '4/7'
				)
		self.objeto_1 = Etiqueta(
				self, índice = 1, zócalo_de_salida = 0, texto_inicial = 'Universo real', comparte_posición = True
				)
		self.objeto_2 = Entrada(
				self, índice = 2, zócalo_de_entrada = 1, zócalo_de_salida = 1, texto_inicial = '0',
				etiqueta = 'Segundo inicial',  validante = VALIDANTE_NUMÉRICO, proporción = '4/7'
				)


@registrar_nodo(NODO_UNIVERSO)
class NodoUniverso(NodoBase):
	icono = imagen
	codigo_op = NODO_UNIVERSO
	titulo_op = "Universo"

	ClaseGraficadeNodo = GraficadordelNodoUniverso
	ClasedelContenidodeNodo = ContenidodelNodoUniverso

	Entradas = [4, 2]
	Salidas = [4, 2]

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)

	def evaluación_inicial(self):
		self.lista_de_bloqueos = ['Universo real', 'universo real', 'Universo Real', 'universo real', 'Realidad',
		                          'realidad']
		self.bloqueo_de_nombre = False
		self.contenido.objeto_1.autoocultarse()
		self.contenido.objeto_0.mostrar_salida()
		self.evaluación()

	def universo_real(self):
		self.contenido.objeto_0.autoocultarse()
		self.contenido.objeto_1.automostrarse()
		self.bloqueo_de_nombre = True

	def datos_de_entrada_cambiados(self, conexión):
		self.marcar_indefinido()
		self.evaluación()
		if not self.bloqueo_de_nombre and self.valores_internos[0] in self.lista_de_bloqueos:
			self.universo_real()

	def datos_de_salida_cambiados(self):
		self.marcar_indefinido()
		self.evaluación(False)
		if not self.bloqueo_de_nombre and self.valores_internos[0] in self.lista_de_bloqueos:
			self.universo_real()
