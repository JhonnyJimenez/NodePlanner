from lib.nodeeditor.Zocalos import Zocalo
from nodos.nodo_base.np_zocalos_graficador import NodoBaseGraficadordeZocalos


class ZócalosdelNodoBase(Zocalo):
	ClaseGraficadeZocalos = NodoBaseGraficadordeZocalos

	def __init__(
			self, nodo, indice, posicion, tipo_zocalo = 1, multiconexión = True, cantidad_en_el_lado_actual = 1,
			es_entrada = False, rombito = True
			):
		super().__init__(
				nodo, indice, posicion, tipo_zocalo, multiconexión, cantidad_en_el_lado_actual, es_entrada
				)
		self.rombito = rombito

	def definir_posicion_del_zocalo(self):
		self.GraficosZocalos.setPos(
				*self.nodo.obtener_posicion_zocalo(
						self.indice, self.posicion, self.cantidad_en_el_lado_actual, self.es_entrada
						)
				)

	def posicion_zocalo(self):
		res = self.nodo.obtener_posicion_zocalo(
				self.indice, self.posicion, self.cantidad_en_el_lado_actual, self.es_entrada
				)
		return res
