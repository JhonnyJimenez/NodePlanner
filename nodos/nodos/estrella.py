from np_enlistado_de_nodos import *
from nodos.categorías.astronomia import ContenidodelNodoAstronómico, NodoAstronómico

from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_entrada import Entrada, VALIDANTE_NUMÉRICO
from nodos.objetos.np_booleana import Booleana
from nodos.objetos.np_desplegable import Desplegable

TIPOS = ['Enana amarilla']


class ContenidodelNodoEstrella(ContenidodelNodoAstronómico):
	def contenido(self):
		self.contenido_de_salidas = [
				Etiqueta(self, 'Nombre', 'Nombre', 3, zócalo = 0),
				Etiqueta(self, 'Inicio', 'Inicio', 3, zócalo = 1)
				]
		self.contenido_de_entradas = [
				Etiqueta(self, 'Pertenece a:', es_entrada = True),
				Etiqueta(self, 'Galaxia', es_entrada = True, zócalo = 0),
				Desplegable(self, 'Tipo', TIPOS),
				Entrada(self, '', 'Nombre', zócalo = 1),
				Entrada(
						self, '0', 'Inicio', validante = VALIDANTE_NUMÉRICO, etiqueta = 'Inicio', proporción = '3/7',
						zócalo = 2,
						),
				Etiqueta(self, 'Zona habitable:', es_entrada = True),
				Etiqueta(self, 'Desconocido', etiqueta = 'Desde', es_entrada = True),
				Etiqueta(self, 'Desconocido', etiqueta = 'Hasta', es_entrada = True)
				]


@registrar_nodo(NODO_ESTRELLA)
class NodoEstrella(NodoAstronómico):
	codigo_op = NODO_ESTRELLA
	titulo_op = "Estrella"

	ClasedelContenidodeNodo = ContenidodelNodoEstrella

	Entradas = [4, 4, 2]
	Salidas = [4, 2]

	# 'Círculo', 'Rombo', 'Diamante'
	FormadeEntradas = ['Círculo', 'Círculo', 'Círculo']
	FormadeSalidas = ['Círculo', 'Círculo']

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)

	def métodos_de_evaluación(self):
		pass
