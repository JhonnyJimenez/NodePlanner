from mpmath import mpf

from np_enlistado_de_nodos import *
from nodos.categorías.cronista import ContenidodelNodoCronista, NodoCronista
from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_entrada import Entrada, VALIDANTE_NUMÉRICO
from nodos.objetos.np_booleana import Booleana
from nodos.objetos.np_utilitarios import UnidadDeMedida, Fecha


class ContenidodelNodoUnidadTemporal(ContenidodelNodoCronista):
	def contenido(self):
		self.contenido_de_salidas = [
				Etiqueta(self, 'Salida', 'Salida', alineado = 3, zócalo = 0),
				]
		self.contenido_de_entradas = [
				Entrada(self, '1', 'Orden', etiqueta = 'No.', proporción = '3/8', validante = VALIDANTE_NUMÉRICO, tipo_de_validante = 2, zócalo = 0),
				Entrada(self, 'Unidad', 'Nombre', etiqueta = 'Nombre', proporción = '3/8', zócalo = 1),
				Booleana(self, 'Unidad absoluta', 'Unidad absoluta', valor = 0, zócalo = 2, tooltip = 'Unidad de uso común tan pequeña que es la base para otras, o tan grande que generalmente no se usa para crear superiores'),
				Entrada(self, '0', 'No_subunidad', etiqueta = 'No. sub', proporción = '3/8', validante = VALIDANTE_NUMÉRICO, tipo_de_validante = 2, zócalo = 3),
				# Booleana(self, 'Subunidad constante', 'Subunidad constante', zócalo = 4),
				Entrada(self, '0', 'Subunidades', etiqueta = 'Subuni.', proporción = '3/8', zócalo = 4),
				# Booleana(self, '¿Usa nombres?', 'Uso de nombres', valor = 0, zócalo = 5),
				Entrada(self, '', 'Lista de nombres', etiqueta = 'Nombre', proporción = '3/8', zócalo = 5),
				]


@registrar_nodo(NODO_UNIDAD_TEMPORAL)
class NodoUnidadTemporal(NodoCronista):
	codigo_op = NODO_UNIDAD_TEMPORAL
	titulo_op = "Unidad temporal"

	ClasedelContenidodeNodo = ContenidodelNodoUnidadTemporal

	Entradas = [1, 4, 3, 1, 3, 4]
	Salidas = [2]

	FormaDeEntradas = []
	FormaDeSalidas = []

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)

	def ajustes_preevaluación(self):
		# Valores que usa el nodo para ocultar secciones de este que no están en uso.
		self.unidad_absoluta = self.contenido.contenido_de_entradas[2]
		self.ocultables = self.contenido.contenido_de_entradas[3:]

	def sistema_de_autoocultado(self, absoluto):
		if absoluto:
			for elemento in self.ocultables:
				elemento.ocultar()
			self.Nodograficas.altura_del_nodo = (
				self.Nodograficas.altura_del_título + (2 * self.Nodograficas.márgen) + self.unidad_absoluta.altura
				+ self.unidad_absoluta.posición_y
			)
		else:
			for elemento in self.ocultables:
				elemento.mostrar()
			self.Nodograficas.altura_del_nodo = (
				self.Nodograficas.altura_del_título + (2 * self.Nodograficas.márgen) + self.ocultables[-1].altura
				+ self.ocultables[-1].posición_y
			)

	def métodos_de_evaluación(self):
		absoluto = True if self.valores['Unidad absoluta'] != 0 else False
		
		self.sistema_de_autoocultado(absoluto)

		if self.valores['Subunidades'].find(',') != -1:
		# Find devuelve la posición en el string del carácter buscado. Si no lo encuentra devuelve menos -1.
			try:
				self.valores['Subunidades'] = self.valores['Subunidades'].replace(' ', '')
				self.valores['Subunidades'] = self.valores['Subunidades'].split(',')
				contador = -1
				for subunidad in self.valores['Subunidades']:
					contador += 1
					if subunidad in ('', None):
						self.valores['Subunidades'][contador] = mpf('0')
					else:
						self.valores['Subunidades'][contador] = mpf(subunidad)
			except ValueError:
				self.errores_graves += 1
				self.Nodograficas.setToolTip('El valor de las subunidades tienen que ser números.')

		# Esto evitará una lista de subunidades con valor cero, lo que acarrearía un bucle infito al calcular (porque usa bucle while con restas).
			if sum(self.valores['Subunidades']) == mpf('0'):
				contador = 0
				for subunidad in self.valores['Subunidades']:
					if subunidad == mpf('0'):
						self.valores['Subunidades'][contador] = mpf('1')
						contador += 1

		else:
			try:
				self.valores['Subunidades'] = mpf(self.valores['Subunidades'])
			except ValueError as e:
				self.errores_graves += 1
				self.Nodograficas.setToolTip('El valor de la subunidad tiene que ser un número.')

		unidad = UnidadDeMedida(
			numero = self.valores['Orden'],
			nombre = self.valores['Nombre'],
			es_absoluta = absoluto,
			no_subunidad = self.valores['No_subunidad'],
			subunidades = self.valores['Subunidades'],
			lista_de_nombres = self.valores['Lista de nombres']
			)
		
		self.valores['Salida'] = unidad
