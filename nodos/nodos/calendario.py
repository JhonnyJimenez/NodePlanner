from mpmath import mpf

from np_enlistado_de_nodos import *
from nodos.categorías.cronista import ContenidodelNodoCronista, NodoCronista

from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_entrada import Entrada
from nodos.objetos.np_utilitarios import Fecha, conversor_númerico_mpmath, UnidadDeMedida

class ContenidodelNodoCalendario(ContenidodelNodoCronista):
	def contenido(self):
		self.contenido_de_salidas = [
				Etiqueta(self, 'Fecha', 'Fecha', alineado = 3, zócalo = 0)
				]
		self.contenido_de_entradas = [
				Entrada(self, 'Calendario gregoriano', 'Nombre', etiqueta = 'Nombre', tipo = 2, proporción = '3/8', zócalo = 0),
				Etiqueta(self, '', 'Inicio', es_entrada = True, etiqueta = 'Inicio', con_dos_puntos = False, proporción = '4/4', zócalo = 1),
				Etiqueta(self, '', 'Unidades', es_entrada = True, etiqueta = 'Unidades', con_dos_puntos = False, proporción = '4/4', zócalo = 2),
				Etiqueta(self, '', 'Excepciones', es_entrada = True, etiqueta = 'Excepciones', con_dos_puntos = False, proporción = '4/4', zócalo = 3),
				Etiqueta(self, '', 'Formato', es_entrada = True, etiqueta = 'Formato', con_dos_puntos = False, proporción = '4/4', zócalo = 4),
				]


@registrar_nodo(NODO_CALENDARIO)
class NodoCalendario(NodoCronista):
	codigo_op = NODO_CALENDARIO
	titulo_op = "Calendario"

	ClasedelContenidodeNodo = ContenidodelNodoCalendario

	Entradas = [4, 2, 1, 4, 4]
	Salidas = [2]

	FormaDeEntradas = []
	FormaDeSalidas = []

	Entradas_multiconexión = ['', '', True, True]

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)

	def ajustes_preevaluación(self):
		if type(self.valores['Inicio']) is str:
			try:
				self.valores['Inicio'] = conversor_númerico_mpmath(self.valores['Inicio'])
			except TypeError:
				self.valores['Inicio'] = mpf(0)
		elif type(self.valores['Inicio']) not in (mpf, float, int):
			self.valores['Inicio'] = mpf(0)
		else:
			pass

		self.ordenado = {0: UnidadDeMedida(numero = 0, nombre = 'Segundos', es_absoluta = True)}
		if self.entradas[2].Zocaloconexiones != []:
			for elemento in self.valores['Unidades']:
				self.ordenado[elemento.llave] = elemento

		if self.entradas[3].Zocaloconexiones == []:
			self.valores['Excepciones'] = []
		else:
			pass

		if self.entradas[4].Zocaloconexiones == [] or self.valores['Formato'] == '':
			self.valores['Formato'] = '%0'
		else:
			pass

	def métodos_de_evaluación(self):
		self.valores['Fecha'] = Fecha(
			inicio = self.valores['Inicio'],
			unidades = self.ordenado,
			formato = self.valores['Formato']
			)
