from nodos.categorías.salidas import *

@registrar_nodo(CATEGORIA_SALIDAS)
class Salida(Salidas):
	icono = imagen
	codigo_op = CATEGORIA_SALIDAS
	titulo_op = "Salida"
	content_label_objname = "Salida"

	def __init__(self, escena, titulo = titulo_op, entradas = [3], salidas = []):
		super().__init__(escena, titulo, entradas, salidas)
		self.evaluar()