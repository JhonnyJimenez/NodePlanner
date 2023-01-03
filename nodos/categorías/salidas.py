from PyQt5.QtGui import QBrush, QColor

from np_enlistado_de_nodos import *
from nodos.nodo_base.np_nodo_base import NodoBase
from nodos.nodo_base.np_nodo_contenido import ContenidodelNodoBase
from nodos.nodo_base.np_nodo_graficador import GraficadordelNodoBase
from nodos.objetos.np_etiqueta import Etiqueta

imagen = "C:/Users/Maste/Downloads/icons/visibility.svg"


class GraficadordelosNodosdeSalida(GraficadordelNodoBase):
	def init_assets(self):
		super().init_assets()
		self._relleno_del_título = QBrush(QColor("#FF3C1D26"))


class ContenidodelosNodosdeSalida(ContenidodelNodoBase):
	def controles(self):
		super().controles()
		self.placeholder(1)

	def configuraciones(self):
		super().configuraciones()
		self.anchura = 100

	def contenido(self):
		self.ejemplo_0 = Etiqueta(
				self, índice = 0, zócalo_de_entrada = 0, texto_inicial = 'Sin datos.'
				)


# @registrar_nodo(CATEGORIA_SALIDAS)
class Salidas(NodoBase):
	icono = imagen
	codigo_op = CATEGORIA_SALIDAS
	titulo_op = "Salidas"

	ClaseGraficadeNodo = GraficadordelosNodosdeSalida
	ClasedelContenidodeNodo = ContenidodelosNodosdeSalida

	Entradas = [0]
	Salidas = []

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)

	# def ImplementarEvaluacion(self):
	# 	nodo_de_entrada = self.obtener_entrada(0)
	# 	if not nodo_de_entrada:
	# 		self.Nodograficas.setToolTip("No hay un nodo conectado.")
	# 		self.marcar_inválido()
	# 		self.contenido.etiqueta_1.setText("Sin datos.")
	# 		return
	#
	# 	contrazocalo = self.obtener_contrazócalo(0)
	# 	valor = nodo_de_entrada.valores[contrazocalo.indice]
	#
	# 	if valor == '' or valor is None:
	# 		self.Nodograficas.setToolTip("No hay datos en el nodo conectado.")
	# 		self.marcar_indefinido()
	# 		self.contenido.etiqueta_1.setText("Sin datos.")
	# 		return
	#
	# 	valor = self.textualizador(valor)
	#
	# 	valor = str(valor)
	#
	# 	self.contenido.etiqueta_1.setText(valor)
	# 	self.marcar_indefinido(False)
	# 	self.marcar_inválido(False)
	# 	self.Nodograficas.setToolTip("")
	#
	# 	return valor
