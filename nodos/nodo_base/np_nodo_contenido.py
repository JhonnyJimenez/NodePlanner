from PyQt5.QtGui import QFont
from lib.nodeeditor.ContenidodelNodo import ContenidoDelNodo
from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_entrada import Entrada, VALIDANTE_NUMÉRICO
from nodos.objetos.np_booleana import Booleana
from nodos.objetos.np_desplegable import Desplegable


class ContenidodelNodoBase(ContenidoDelNodo):
	def init_ui(self):
		self.configuraciones()
		self.controles()
		self.contenido()

	def configuraciones(self):
		self.anchura = 160
		self.altura = 20
		self.espaciado = 4

		self.nombre_de_la_fuente = "Rounded Mgen+ 1c"
		self.fuente = QFont(self.nombre_de_la_fuente, 8)

	def controles(self):
		self.lista_de_alturas = [0]             # Para la ubicación automática de cada objeto y para determinar
												# la altura del nodo automáticamente.
		self.lista_de_anchuras = []             # Para determinar la anchura del nodo automáticamente.
		self.posicionador_de_entradas = []      # Para ubicar las entradas según el objeto que las use.
		self.posicionador_de_salidas = []       # Para ubicar las salidas según el objeto que las use.
		self.valores = {}
		self.diccionarios = {'Salidas': {}, 'Entradas': {}}

		for entradas in self.nodo.Entradas:
			self.posicionador_de_entradas.append(None)

		for salidas in self.nodo.Salidas:
			self.posicionador_de_salidas.append(None)

	def contenido(self):
		self.contenido_de_salidas = [
				Etiqueta(self, 'Salida númerica', alineado = 3, llave = 'Objeto 1', zócalo = 0),
				Etiqueta(self, 'Salida de texto', alineado = 3, llave = 'Objeto 2', zócalo = 1),
				Etiqueta(self, 'Salida booleana', alineado = 3, llave = 'Objeto 3', zócalo = 2),
				Etiqueta(self, 'Salida de desplegables', alineado = 3, llave = 'Objeto 4', zócalo = 3),
				]
		self.contenido_de_entradas = [
				Etiqueta(self, 'Tipos de objetos'),
				Entrada(self, '0', 'Objeto 1', etiqueta = 'Entrada númerica', validante = VALIDANTE_NUMÉRICO, zócalo = 0),
				Entrada(self, '', 'Objeto 2', etiqueta = 'Entrada de texto', zócalo = 1),
				Booleana(self, 'Entrada booleana', 'Objeto 3', 1, True, zócalo = 2),
				Desplegable(self, 'Objeto 4', ['Desplegable'])
				]

		# self.método_para_reordenar()

	def método_para_reordenar(self):
		self.respaldo = self.contenido_de_entradas.copy()

		# Usa while porque for elimina los elementos hasta que el largo de a lista se reduce al índice al que debería
		# avanzar.
		for elemento in self.contenido_de_entradas:
			try:
				elemento.etiqueta.deleteLater()
			except AttributeError:
				pass
			elemento.objeto.deleteLater()

		self.contenido_de_entradas = []

		for elemento in self.respaldo:
			self.contenido_de_entradas.append(elemento)

		self.contenido_de_entradas[0] = self.respaldo[1]
		self.contenido_de_entradas[1] = self.respaldo[0]
		print(self.contenido_de_entradas)

		self.lista_de_alturas = [25]
		for elemento in self.contenido_de_entradas:
			elemento.reordenando = True
			elemento.init_ui()

	def serialización(self):
		res = super().serialización()
		res['Valores'] = self.valores
		return res

	def deserialización(self, data, hashmap = {}):
		super().deserialización(data, hashmap)
		for widget in self.contenido_de_entradas:
			widget.método_de_deserialización(data['Valores'])
		return True