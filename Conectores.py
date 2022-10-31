from GraficosDeConectores import GraficosDeConectores


Izquierda_arriba = 1
Izquierda_abajo = 2
Derecha_arriba = 3
Derecha_abajo = 4


class Conector:
	def __init__(self, nodo, indice, posicion):
		
		self.nodo = nodo
		self.indice = indice
		self.posicion = Izquierda_arriba
		
		self.GraficosConectores = GraficosDeConectores(self.nodo.Nodograficas)
		
		self.GraficosConectores.setPos(*self.nodo.obtenerposicionconector(indice, posicion))
		