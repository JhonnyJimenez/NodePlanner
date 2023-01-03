from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from np_constantes import *

DEBUG = False


class ObjetodeNodePlanner:
	def __init__(
			self, elemento_padre, índice = None, zócalo_de_entrada = None, zócalo_de_salida = None, etiqueta: str = None,
			comparte_posición = False, proporción: str = '3/4', ancho: int = None, alto = None, posición_x = 0,
			posición_y = None, texto_inicial = NOMBRE_DEL_PRODUCTO, valor_inicial = None, alineado: str | int = 2,
			fuente = None, validante = None, indeterminado = False, lista = None, separadores = None,
			especificación = False
			):

		self.elemento_padre = elemento_padre
		self.comparte_posición = comparte_posición

		if type(índice) in (int, float):
			self.índice = int(índice)
		else:
			self.índice = None

		self.zócalo_de_entrada = zócalo_de_entrada
		self.zócalo_de_salida = zócalo_de_salida
		self.texto_inicial = texto_inicial
		self.valor_inicial = valor_inicial
		self.texto_etiqueta = etiqueta
		self.validante = validante
		self.indeterminado = indeterminado
		self.lista = lista
		self.separadores = separadores
		self.especificación = especificación

		self.definir_objeto()

		self.autooculto = False
		self.es_visible = True

		self.fuente(fuente)

		self.altura_anchura_y_posición(ancho, alto, posición_x, posición_y)
		self.obtener_proporción(proporción)
		self.definir_posición_y_etiqueta()

		self.configuraciones_adicionales()
		self.señal()

		self.posición_de_zócalos()
		self.alineado(alineado)
		self.estilo()

		self.elemento_padre.última_altura_usada.append(
					int(self.posición_y + self.alto + self.elemento_padre.espaciado_entre_contenidos)
					)
		self.elemento_padre.lista_de_anchuras.append(self.ancho)

		self.elemento_padre.lista_de_contenidos.append(self)

		self.contenido_del_objeto()
		self.forma_de_deserialización()


	def definir_objeto(self):
		self.objeto = self.objeto()(*self.parámetros())

	def objeto(self):
		return None

	def parámetros(self):
		return None

	def fuente(self, fuente):
		try:
			if fuente is None:
				self.fuente = self.elemento_padre.fuente
			else:
				self.fuente = fuente
			self.objeto.setFont(self.fuente)
		except:
			if DEBUG:
				print(self.objeto.__class__.__name__, "no usa fuente.")

	def altura_anchura_y_posición(self, ancho, alto, posición_x, posición_y):
		if posición_x is None:
			self.posición_x = 0
		else:
			self.posición_x = posición_x

		if posición_y is None:
			if self.comparte_posición:
				self.posición_y = self.elemento_padre.última_altura_usada[-2]
			else:
				self.posición_y = self.elemento_padre.última_altura_usada[-1]
		else:
			self.posición_y = posición_y

		if ancho is None:
			try:
				self.ancho = max(self.elemento_padre.lista_de_anchuras)
			except ValueError:
				self.ancho = self.elemento_padre.anchura
		else:
			self.ancho = ancho

		if alto is None:
			self.alto = self.elemento_padre.altura
		else:
			self.alto = alto

	def obtener_proporción(self, proporción):
		dato = str(proporción)
		dato_encontrado = dato.find("/")

		número_1 = ''
		número_2 = ''

		for num in dato[0:dato_encontrado]:
			número_1 += num
		largo_objeto = float(número_1)

		for num in dato[dato_encontrado + 1:]:
			número_2 += num
		partes = float(número_2)

		self.proporción_1 = int((self.ancho / partes) * (partes - largo_objeto))
		self.proporción_2 = int((self.ancho / partes) * largo_objeto)

	def definir_posición_y_etiqueta(self):
		if self.texto_etiqueta == '' or self.texto_etiqueta is None:
			self.objeto.setGeometry(self.posición_x, self.posición_y, self.ancho, self.alto)
		else:
			if self.texto_etiqueta[-1] != ':':
				self.texto_sin_puntos = self.texto_etiqueta
				self.texto_etiqueta += ':'
			else:
				self.texto_sin_puntos = self.texto_etiqueta.replace(":", "")

			self.etiqueta = QLabel(self.texto_etiqueta, self.elemento_padre)
			self.etiqueta.setGeometry(self.posición_x, self.posición_y, self.proporción_1, self.alto)
			self.etiqueta.setStyleSheet('padding-left: 1px; background: transparent')
			self.etiqueta.setAlignment(Qt.AlignVCenter)
			self.etiqueta.setFont(self.fuente)
			self.objeto.setGeometry(
					self.proporción_1 + 1,
					self.posición_y,
					self.proporción_2 - 1,
					self.alto
					)

	def alineado(self, alineado):
		try:
			if alineado in (1, 'Izquierda'):
				self.objeto.setAlignment(Qt.AlignLeft)
			elif alineado in (2, 'Centro'):
				self.objeto.setAlignment(Qt.AlignCenter)
			elif alineado in (3, 'Derecha'):
				self.objeto.setAlignment(Qt.AlignRight)
		except:
			if DEBUG:
				print(self.objeto.__class__.__name__, "no usa alineado.")

	def configuraciones_adicionales(self):
		pass

	def posición_de_zócalos(self):
		self.advertencia_1 = 'Esa posición ya fue escrita.'
		self.advertencia_2 = 'La entrada %s no existe.'
		self.advertencia_3 = 'La salida %s no existe.'
		self.advertencia_4 = 'La posición fue reescrita.'

		try:
			if self.zócalo_de_entrada is not None:
				if self.elemento_padre.lista_de_posiciones_de_entradas[self.zócalo_de_entrada] is None:
					self.elemento_padre.lista_de_posiciones_de_entradas[self.zócalo_de_entrada] = (
						self.posición_y + (self.alto / 2)
					)
				else:
					if self.comparte_posición:
						self.elemento_padre.lista_de_posiciones_de_entradas[self.zócalo_de_entrada] = (
								self.posición_y + (self.alto / 2)
						)
						if DEBUG:
							print(self.advertencia_4)
					else:
						if DEBUG:
							print(self.advertencia_1)
		except IndexError:
				print(self.advertencia_2 % self.zócalo_de_entrada)

		try:
			if self.zócalo_de_salida is not None:
				if self.elemento_padre.lista_de_posiciones_de_salidas[self.zócalo_de_salida] is None:
					self.elemento_padre.lista_de_posiciones_de_salidas[self.zócalo_de_salida] = (
						self.posición_y + (self.alto / 2)
					)
				else:
					if self.comparte_posición:
						self.elemento_padre.lista_de_posiciones_de_salidas[self.zócalo_de_salida] = (
								self.posición_y + (self.alto / 2)
						)
						if DEBUG:
							print(self.advertencia_4)
					else:
						if DEBUG:
							print(self.advertencia_1)
		except IndexError:
				print(self.advertencia_3 % self.zócalo_de_salida)

	def estilo(self):
		pass

	def señal(self):
		# Aquí iría el signal de la texto_etiqueta... si es que hubiera una xD
		pass

	def contenido_del_objeto(self):
		# Aquí iría el método del objeto que emite cuando se modifica algo. Las etiquetas... bueno... xD
		pass

	def forma_de_deserialización(self):
		# Aquí iría el método con el que la deserialización pone el dato en el objeto... pero bueno... texto_etiqueta... xD
		pass

	# Estos métodos solo se pueden usar después del init en la clase del nodo. En el contenido dan error porque el
	# zócalo se crea después del contenido y obviamente no se puede ocultar o mostrar algo que aún no existe.
	def ocultar_entrada(self):
		if self.zócalo_de_entrada is not None:
			self.elemento_padre.nodo.entradas[self.zócalo_de_entrada].quitar_todas_las_conexiones(True)
			self.elemento_padre.nodo.entradas[self.zócalo_de_entrada].GraficosZocalos.setVisible(False)
		else:
			pass

	def mostrar_entrada(self):
		if self.zócalo_de_entrada is not None:
			self.elemento_padre.nodo.entradas[self.zócalo_de_entrada].GraficosZocalos.setVisible(True)
		else:
			pass

	def ocultar_salida(self):
		if self.zócalo_de_salida is not None:
			self.elemento_padre.nodo.salidas[self.zócalo_de_salida].quitar_todas_las_conexiones(True)
			self.elemento_padre.nodo.salidas[self.zócalo_de_salida].GraficosZocalos.setVisible(False)
		else:
			pass

	def mostrar_salida(self):
		if self.zócalo_de_salida is not None:
			self.elemento_padre.nodo.salidas[self.zócalo_de_salida].GraficosZocalos.setVisible(True)
		else:
			pass

	def ocultar_zócalos(self):
		self.ocultar_entrada()
		self.ocultar_salida()

	def mostrar_zócalos(self):
		self.mostrar_entrada()
		self.mostrar_salida()

	def autoocultarse(self):
		self.ocultar_zócalos()
		self.objeto.setVisible(False)
		self.autooculto = True
		if self.texto_etiqueta != '' and self.texto_etiqueta is not None:
			self.etiqueta.setVisible(False)
		else:
			pass

	def automostrarse(self):
		self.mostrar_zócalos()
		self.objeto.setVisible(True)
		self.autooculto = False
		if self.texto_etiqueta != '' and self.texto_etiqueta is not None:
			self.etiqueta.setVisible(True)
		else:
			pass

	def ocultado_por_entrada(self):
		if self.es_visible and self.zócalo_de_entrada is not None:
			if self.elemento_padre.nodo.entradas[self.zócalo_de_entrada].Zocaloconexiones != []:
				self.objeto.setVisible(False)
				self.es_visible = False
				if self.texto_etiqueta != '' and self.texto_etiqueta is not None:
					self.etiqueta.setGeometry(self.posición_x, self.posición_y, self.ancho, self.alto)
					self.etiqueta.setText(self.texto_sin_puntos)
					self.etiqueta.setVisible(True)

	def mostrado_por_entrada(self):
		if not self.autooculto:
			if not self.es_visible and self.zócalo_de_entrada is not None:
				if self.elemento_padre.nodo.entradas[self.zócalo_de_entrada].Zocaloconexiones == []:
					self.objeto.setVisible(True)
					self.es_visible = True
					if self.texto_etiqueta != '' and self.texto_etiqueta is not None:
						self.etiqueta.setGeometry(self.posición_x, self.posición_y, self.proporción_1, self.alto)
						self.etiqueta.setText(self.texto_etiqueta)
						self.etiqueta.setVisible(True)
