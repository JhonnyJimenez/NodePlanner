from np_enlistado_de_nodos import *
from nodos.categorías.astronomia import ContenidodelNodoAstronómico, NodoAstronómico

from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_entrada import Entrada, VALIDANTE_NUMÉRICO
from nodos.objetos.np_booleana import Booleana
from nodos.objetos.np_desplegable import Desplegable

CATEGORÍA = ['Planeta', 'Planeta gaseoso', 'Planeta enano', 'Plutoide', 'Plutino', 'Satélite', 'Supertierra']


class ContenidodelNodoCuerpoCeleste(ContenidodelNodoAstronómico):
	def contenido(self):
		self.contenido_de_salidas = [
				Etiqueta(self, 'Nombre', 'Nombre', 3, zócalo = 0),
				Etiqueta(self, 'Inicio', 'Inicio', 3, zócalo = 1)
				]
		self.contenido_de_entradas = [
				Etiqueta(self, 'un astro.', etiqueta = 'Orbita a', es_entrada = True, zócalo = 0),
				Desplegable(self, 'Tipo', CATEGORÍA),
				Entrada(self, '', 'Nombre', zócalo = 1),
				Entrada(
						self, '0', 'Inicio', validante = VALIDANTE_NUMÉRICO, etiqueta = 'Inicio', proporción = '3/7',
						zócalo = 2,
						),
				Etiqueta(self, 'Características físicas', es_entrada = True),
				Entrada(self, '0', 'Masa', etiqueta = 'Masa', proporción = '3/7', validante = VALIDANTE_NUMÉRICO,
				        zócalo = 3),
				Entrada(self, '0', 'Volumen', etiqueta = 'Volumen', proporción = '3/7', validante = VALIDANTE_NUMÉRICO,
				        zócalo = 4),
				Etiqueta(self, 'Desconocida', etiqueta = 'Densidad', es_entrada = True),
				Etiqueta(self, 'Desconocida', etiqueta = 'Superficie', es_entrada = True),
				]


@registrar_nodo(NODO_CELESTE)
class NodoCuerpoCeleste(NodoAstronómico):
	codigo_op = NODO_CELESTE
	titulo_op = "Cuerpo celeste"

	ClasedelContenidodeNodo = ContenidodelNodoCuerpoCeleste

	Entradas = [4, 4, 2, 1, 1]
	Salidas = [4, 2]

	# 'Círculo', 'Rombo', 'Diamante'
	FormadeEntradas = ['Círculo', 'Círculo', 'Círculo', 'Círculo', 'Círculo']
	FormadeSalidas = ['Círculo', 'Círculo']

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)

	def métodos_de_evaluación(self):
		pass
