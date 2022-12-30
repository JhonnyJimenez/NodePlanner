from lib.nodeeditor.Zocalos import Zocalo
from nodos.nodo_base.np_zocalos_graficador import NodoBaseGraficadordeZocalos


class NodoBaseZocalos(Zocalo):
	pass
	# ClaseGraficadeZocalos = NodoBaseGraficadordeZocalos
	#
	# def __init__(
	# 		self, nodo, indice, posicion, tipo_zocalo=1, multiconexion=True, cantidad_en_el_lado_actual=1,
	# 		esEntrada=False, espaciado_extra = []
	# 		):
	# 	self.espaciado_extra = espaciado_extra
	# 	super().__init__(
	# 			nodo, indice, posicion, tipo_zocalo, multiconexion, cantidad_en_el_lado_actual, esEntrada
	# 			)
	#
	# def definir_posicion_del_zocalo(self):
	# 	self.GraficosZocalos.setPos(
	# 			*self.nodo.obtener_posicion_zocalo(
	# 					self.indice, self.posicion, self.GraficosZocalos.radio, self.cantidad_en_el_lado_actual,
	# 					self.espaciado_extra
	# 					)
	# 			)
	#
	# def posicion_zocalo(self):
	# 	res = self.nodo.obtener_posicion_zocalo(
	# 			self.indice, self.posicion, self.GraficosZocalos.radio, self.cantidad_en_el_lado_actual,
	# 			self.espaciado_extra
	# 			)
	# 	return res
