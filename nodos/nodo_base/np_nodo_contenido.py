from PyQt5.QtGui import QFont
from lib.nodeeditor.ContenidodelNodo import ContenidoDelNodo
from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_entrada import Entrada, VALIDANTE_NUMÉRICO
from nodos.objetos.np_booleana import Booleana
from nodos.objetos.np_desplegable import Desplegable


class ContenidodelNodoBase(ContenidoDelNodo):
	def init_ui(self):
		self.controles()
		self.configuraciones()
		self.contenido()

	def controles(self):
		self.última_altura_usada = [0]              # Para la ubicación automática de cada objeto y para determinar
														# la altura del nodo automáticamente.
		self.lista_de_anchuras = []                 # Para determinar la anchura del nodo automáticamente.
		self.lista_de_posiciones_de_entradas = []   # Para ubicar las entradas según el objeto que las use.
		self.lista_de_posiciones_de_salidas = []    # Para ubicar las salidas según el objeto que las use.

		for entradas in self.nodo.Entradas:
			self.lista_de_posiciones_de_entradas.append(None)

		for salidas in self.nodo.Salidas:
			self.lista_de_posiciones_de_salidas.append(None)

		self.lista_de_contenidos = []

		self.placeholder(5)

	def configuraciones(self):
		self.espaciado_entre_contenidos = 5.0
		self.anchura = 220
		self.altura = 20

		self.fuente = QFont("Ubuntu", 9)

	def placeholder(self, cantidad_de_objetos: int):
		self.lista_de_información = []
		self.lista_de_deserializamiento = []

		for num in range(0, cantidad_de_objetos):
			self.lista_de_información.append(None)
			self.lista_de_deserializamiento.append(None)

	def contenido(self):
		self.ejemplo_0 = Etiqueta(
				self, índice = 0, zócalo_de_entrada = 0, texto_inicial = 'Tipos de objetos'
				)
		self.ejemplo_1 = Entrada(
				self, índice = 1, zócalo_de_entrada = 1, zócalo_de_salida = 0, texto_inicial = '0',
				etiqueta = 'Entrada númerica', validante = VALIDANTE_NUMÉRICO, proporción = '1/2'
				)
		self.ejemplo_2 = Entrada(
				self, índice = 2, zócalo_de_entrada = 2, zócalo_de_salida = 1, etiqueta = 'Entrada de texto',
				proporción = '1/2', texto_inicial = ''
				)
		self.ejemplo_3 = Booleana(
				self, índice = 3, zócalo_de_entrada = 3, zócalo_de_salida = 2, texto_inicial = 'Entrada booleana',
				indeterminado = True, valor_inicial = 1
				)
		self.ejemplo_4 = Desplegable(
				self, índice = 4, zócalo_de_salida = 3, etiqueta = 'Lista desplegable', proporción = '1/2',
				lista = ['Objeto 1', 'Objeto 2', 'Objeto 3', 'Objeto 4', 'Objeto 5']
				)

	def serialización(self):
		res = super().serialización()
		res['Valores'] = self.lista_de_información
		return res

	def deserialización(self, data, hashmap = {}):
		super().deserialización(data, hashmap)
		for objeto in self.lista_de_deserializamiento:
			if objeto is not None:
				objeto(data['Valores'][self.lista_de_deserializamiento.index(objeto)])
		return True
