from nodos.categorías.salidas import *

# @registrar_nodo(NODO_SALIDA)
class Salida(Salidas):
	icono = imagen
	codigo_op = NODO_SALIDA
	titulo_op = "Salida"
	content_label_objname = "Salida"

	def __init__(self, escena, titulo = titulo_op, entradas = [0], salidas = []):
		super().__init__(escena, titulo, entradas, salidas)