from np_enlistado_de_nodos import *
from nodos.categorías.astronomia import ContenidodelNodoAstronómico, NodoAstronómico

from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_entrada import Entrada, VALIDANTE_NUMÉRICO


class ContenidodelNodoUniverso(ContenidodelNodoAstronómico):
	def contenido(self):
		self.contenido_de_salidas = [
				Etiqueta(self, 'Nombre', 'Nombre', 3, zócalo = 0),
				Etiqueta(self, 'Inicio', 'Inicio', 3, zócalo = 1),
				Etiqueta(self, 'Diámetro', 'Diámetro', 3, zócalo = 2),
				]
		self.contenido_de_entradas = [
				Entrada(self, '', 'Nombre', etiqueta = 'Nombre', proporción = '3/7', zócalo = 0),
				Entrada(
						self, '0', 'Inicio', validante = VALIDANTE_NUMÉRICO, etiqueta = 'Inicio', proporción = '3/7',
						zócalo = 1,
						)
				]


@registrar_nodo(NODO_UNIVERSO)
class NodoUniverso(NodoAstronómico):
	codigo_op = NODO_UNIVERSO
	titulo_op = "Universo"

	ClasedelContenidodeNodo = ContenidodelNodoUniverso

	Entradas = [4, 2]
	Salidas = [4, 2, 1]

	FormadeEntradas = ['Círculo', 'Círculo']
	FormadeSalidas = ['Círculo', 'Círculo', 'Círculo']

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)

	def ajustes_adicionales(self):
		self.lista_de_bloqueos = ['Universo real', 'universo real', 'Universo Real', 'universo real', 'Realidad',
		                          'realidad', 'Vida real', 'vida Real', 'vida real']
		self.valor_seguro = ''
		self.bloqueo_de_nombre = False

	def widget_bloqueado(self):
		self.contenido.contenido_de_entradas[0].ocultar()
		self.contenido.contenido_de_entradas[0] = Etiqueta(self.contenido, texto = self.valores['Nombre'], es_entrada =
		True, posición_y_tamaño = [None, (self.contenido.altura + self.contenido.espaciado) * len(
				self.contenido.contenido_de_salidas), None, None], reordenando = True)
		self.contenido.contenido_de_entradas[0].mostrar()

		self.bloqueo_de_nombre = True

	def widget_desbloqueado(self):
		self.contenido.contenido_de_entradas[0].ocultar()
		self.contenido.contenido_de_entradas[0] = Entrada(
				self.contenido, self.valor_seguro, 'Nombre', etiqueta = 'Nombre', proporción = '3/7',
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

		if self.bloqueo_de_nombre is False and self.valores['Nombre'] in self.lista_de_bloqueos:
			self.widget_bloqueado()
		elif self.bloqueo_de_nombre is True:
			self.valores['Nombre'] = self.valor_seguro
			self.widget_desbloqueado()
		else:
			self.valor_seguro = self.valores['Nombre']

	def datos_de_salida_cambiados(self):
		self.marcar_indefinido()
		self.evaluación(False)

	def métodos_de_evaluación(self):
		self.valores['Diámetro'] = 0
