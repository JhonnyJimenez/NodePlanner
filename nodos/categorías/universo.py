from PyQt5.QtGui import QBrush, QColor

from np_enlistado_de_nodos import *
from nodos.nodo_base.np_nodo_base import NodoBase
from nodos.nodo_base.np_nodo_contenido import ContenidodelNodoBase
from nodos.nodo_base.np_nodo_graficador import GraficadordelNodoBase
from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_entrada import Entrada, VALIDANTE_NUMÉRICO


class GraficadordelNodoUniverso(GraficadordelNodoBase):
	def init_assets(self):
		super().init_assets()
		self._relleno_del_título = QBrush(QColor("#FF1D2546"))


class ContenidodelNodoUniverso(ContenidodelNodoBase):
	def configuraciones(self):
		super().configuraciones()
		self.anchura = 130

	def contenido(self):
		self.contenido_de_salidas = [
				Etiqueta(self, 'Nombre', alineado = 3, llave = 'Objeto 1', zócalo = 0),
				Etiqueta(self, 'Tiempo', alineado = 3, llave = 'Objeto 2', zócalo = 1),
				Etiqueta(self, 'Diámetro', alineado = 3, llave = 'Diámetro', zócalo = 2),
				]
		self.contenido_de_entradas = [
				Entrada(self, '', 'Objeto 1', etiqueta = 'Nombre', proporción = '3/7', zócalo = 0),
				Entrada(
						self, '0', 'Objeto 2', etiqueta = 'Inicio', proporción = '3/7', zócalo = 1,
						validante = VALIDANTE_NUMÉRICO
						)
				]


@registrar_nodo(NODO_UNIVERSO)
class NodoUniverso(NodoBase):
	icono = "iconos/categoría universo.svg"
	codigo_op = NODO_UNIVERSO
	titulo_op = "Universo"

	ClaseGraficadeNodo = GraficadordelNodoUniverso
	ClasedelContenidodeNodo = ContenidodelNodoUniverso

	Entradas = [4, 2]
	Salidas = [4, 2, 1]

	FormaDeEntradas = ['Círculo', 'Círculo']
	FormaDeSalidas = ['Círculo', 'Círculo', 'Círculo']

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)
		self.lista_de_bloqueos = ['Universo real', 'universo real', 'Universo Real', 'universo real', 'Realidad',
		                          'realidad', 'Vida real', 'vida Real', 'vida real']
		self.valor_seguro = ''
		self.bloqueo_de_nombre = False

	def universo_real(self):
		self.contenido.contenido_de_entradas[0].ocultar()
		self.contenido.contenido_de_entradas[0] = Etiqueta(self.contenido, texto = 'Universo real', es_entrada =
		True, posición_y_tamaño = [None, (self.contenido.altura + self.contenido.espaciado) * len(
				self.contenido.contenido_de_salidas), None, None], reordenando = True)
		self.contenido.contenido_de_entradas[0].mostrar()

		self.bloqueo_de_nombre = True

	def universo_ficticio(self):
		self.contenido.contenido_de_entradas[0].ocultar()
		self.contenido.contenido_de_entradas[0] = Entrada(
				self.contenido, self.valor_seguro, 'Objeto 1', etiqueta = 'Nombre', proporción = '3/7',
				posición_y_tamaño = [None, (self.contenido.altura + self.contenido.espaciado) * len(
				self.contenido.contenido_de_salidas), None, None],
				zócalo = 0, reordenando = True
				)
		self.contenido.contenido_de_entradas[0].mostrar()
		self.bloqueo_de_nombre = False

	def datos_de_entrada_cambiados(self, conexión):
		self.marcar_indefinido()
		self.evaluación()

		# ¿Por qué rayos esto funciona al revés? Ni idea. Solo sé que puedes hacer Ctrl + Z y volver al estado
		# anterior del bloqueo y que la conexión no se restaura si el valor de entrada es de los del bloqueo. Coso
		# random

		if self.bloqueo_de_nombre is False and self.valores['Objeto 1'] in self.lista_de_bloqueos:
			self.universo_real()
		elif self.bloqueo_de_nombre is True:
			self.valores['Objeto 1'] = self.valor_seguro
			self.universo_ficticio()
		else:
			self.valor_seguro = self.valores['Objeto 1']

	def datos_de_salida_cambiados(self):
		self.marcar_indefinido()
		self.evaluación(False)

	def métodos_de_evaluación(self):
		self.valores['Diámetro'] = 0