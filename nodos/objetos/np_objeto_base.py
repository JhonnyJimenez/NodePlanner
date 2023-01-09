from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from nodos.objetos.np_utilitarios import tratado_de_datos

DEBUG = True
ADVERTENCIA_1 = 'Esa posición ya fue escrita.'
ADVERTENCIA_2 = 'La %s %s no existe.'

class ObjetodeNodePlanner:
	def __init__(
			self, elemento_padre = None, llave: str = None, fuente: QFont = None,
			posición_y_tamaño: list = [None, None, None, None], espaciado: int = None,
			etiqueta: str = None, proporción: str = '2/4', zócalo: int = None,
			es_entrada: bool = True, reordenando: bool = False
			):

		self.elemento_padre = elemento_padre
		self.fuente = fuente
		self.medidas = posición_y_tamaño
		self.espaciado = espaciado
		self.texto_de_la_etiqueta = etiqueta
		self.proporción = proporción
		self.zócalo = zócalo
		self.es_entrada = es_entrada
		self.es_salida = not self.es_entrada
		self.reordenando = reordenando
		self.llave = llave
		self.oculto = False
		self.visible = True
		self.deserializando = False

		self.init_ui()

	def init_ui(self):
		self.indexador()
		self.objeto = self.definir_objeto()
		self.estilo()
		self.definir_fuente()
		self.definir_valores_de_geometría()
		self.posición_y_tamaño()
		self.enlistador()

		self.configuraciones_adicionales()
		self.señal()

		self.posicionador_del_zócalo()
		self.contenido()

	def indexador(self):
		if self.zócalo is not None and self.llave is not None:
			if self.es_entrada:
				self.elemento_padre.diccionarios['Entradas'][self.zócalo] = self.llave
			else:
				self.elemento_padre.diccionarios['Salidas'][self.zócalo] = self.llave

	def definir_objeto(self):
		# Aquí declaras el widget principal con sus parámetros: una etiqueta, un line edit...
		return None

	def estilo(self):
		# Aquí declaras el stylesheet para quitarle el fondo a las etiquetas, o a los botones booleanos...
		pass

	def definir_fuente(self):
		if self.fuente is None:
			self.fuente = self.elemento_padre.fuente

		try:
			self.objeto.setFont(self.fuente)
		except AttributeError:
			if DEBUG:
				print(self.objeto.__class__.__name__, "no usa fuente.")

	def definir_valores_de_geometría(self):
		# Posición en x
		if self.medidas[0] is None:
			self.posición_x = 0
		else:
			self.posición_x = self.medidas[0]

		# Posición en y
		if self.medidas[1] is None:
			self.posición_y = self.elemento_padre.lista_de_alturas[-1]
		else:
			self.posición_y = self.medidas[1]

		# Anchura
		if self.medidas[2] is None:
			try:
				self.anchura = max(self.elemento_padre.lista_de_anchuras)
			except ValueError:
				self.anchura = self.elemento_padre.anchura
		else:
			self.anchura = self.medidas[2]

		# Altura
		if self.medidas[3] is None:
			self.altura = self.elemento_padre.altura
		else:
			self.altura = self.medidas[3]

		# Espaciado
		if self.espaciado is None:
			self.espaciado = self.elemento_padre.espaciado

	def posición_y_tamaño(self):
		if self.texto_de_la_etiqueta in ('', None):
			self.objeto.setGeometry(self.posición_x, self.posición_y, self.anchura, self.altura)
		else:
			dato = self.proporción.find('/')

			fracción = float(self.proporción[0:dato])
			partes = float(self.proporción[dato + 1:])

			self.anchura_de_la_etiqueta = int((self.anchura / partes) * fracción)
			anchura_del_objeto = int((self.anchura / partes) * (partes - fracción))

			if self.texto_de_la_etiqueta[-1] != ':':
				self.texto_sin_puntos = self.texto_de_la_etiqueta
				self.texto_con_puntos = self.texto_de_la_etiqueta + ':'
			else:
				self.texto_sin_puntos = self.texto_de_la_etiqueta.replace(":", "")
				self.texto_con_puntos = self.texto_de_la_etiqueta

			self.etiqueta = QLabel(self.texto_con_puntos, self.elemento_padre)
			self.etiqueta.setGeometry(self.posición_x, self.posición_y, self.anchura_de_la_etiqueta, self.altura)
			self.etiqueta.setStyleSheet('padding-left: 1px; background: transparent')
			self.etiqueta.setAlignment(Qt.AlignVCenter)
			self.etiqueta.setFont(self.fuente)

			self.objeto.setGeometry(
					self.anchura_de_la_etiqueta,
					self.posición_y,
					anchura_del_objeto,
					self.altura
					)

	def enlistador(self):
		self.elemento_padre.lista_de_alturas.append(self.posición_y + self.altura + self.espaciado)
		self.elemento_padre.lista_de_anchuras.append(self.anchura)

	def posicionador_del_zócalo(self):
		if self.es_entrada:
			lista = self.elemento_padre.posicionador_de_entradas
		else:
			lista = self.elemento_padre.posicionador_de_salidas

		try:
			if self.zócalo is not None:
				if lista[self.zócalo] is None or self.reordenando:
					lista[self.zócalo] = (self.posición_y + (self.altura / 2))
					self.reordenando = False
				else:
					if DEBUG:
						print(ADVERTENCIA_1)
		except IndexError:
			if DEBUG:
				print(ADVERTENCIA_2 % ('entrada' if self.es_entrada else 'salida', self.zócalo))

	def configuraciones_adicionales(self):
		pass

	def señal(self):
		pass

	def contenido(self):
		if self.llave is not None and self.es_entrada:
			self.elemento_padre.valores[self.llave] = self.escribir_dato()

	def escribir_dato(self):
		return None

	def obtener_dato(self):
		return self.elemento_padre.valores.get(self.llave)

	def ocultar_zócalo(self):
		if self.zócalo is not None:
			if self.es_entrada:
				self.elemento_padre.nodo.entradas[self.zócalo].quitar_todas_las_conexiones(True)
				self.elemento_padre.nodo.entradas[self.zócalo].GraficosZocalos.setVisible(False)
			else:
				self.elemento_padre.nodo.salidas[self.zócalo].quitar_todas_las_conexiones(True)
				self.elemento_padre.nodo.salidas[self.zócalo].GraficosZocalos.setVisible(False)

	def mostrar_zócalo(self):
		if self.zócalo is not None:
			if self.es_entrada:
				self.elemento_padre.nodo.entradas[self.zócalo].GraficosZocalos.setVisible(True)
			else:
				self.elemento_padre.nodo.salidas[self.zócalo].GraficosZocalos.setVisible(True)

	def ocultar(self):
		self.ocultar_zócalo()
		self.objeto.setVisible(False)
		self.oculto = True
		if self.texto_de_la_etiqueta != '' and self.texto_de_la_etiqueta is not None:
			self.etiqueta.setVisible(False)

	def mostrar(self):
		self.mostrar_zócalo()
		self.objeto.setVisible(True)
		self.oculto = False
		if self.texto_de_la_etiqueta != '' and self.texto_de_la_etiqueta is not None:
			self.etiqueta.setVisible(True)

	def widget_conectado(self):
		try:
			if self.visible and self.es_entrada and self.zócalo is not None:
				if self.elemento_padre.nodo.entradas[self.zócalo].Zocaloconexiones != []:
					self.objeto.setVisible(False)
					self.visible = False
					if self.texto_de_la_etiqueta != '' and self.texto_de_la_etiqueta is not None:
						self.etiqueta.setGeometry(self.posición_x, self.posición_y, self.anchura, self.altura)
						self.etiqueta.setText(self.texto_sin_puntos)
		except IndexError:
			pass

	def widget_desconectado(self):
		try:
			if not self.oculto:
				if not self.visible and self.es_entrada and self.zócalo is not None:
					if self.elemento_padre.nodo.entradas[self.zócalo].Zocaloconexiones == []:
						self.objeto.setVisible(True)
						self.visible = True
						if self.texto_de_la_etiqueta != '' and self.texto_de_la_etiqueta is not None:
							self.etiqueta.setGeometry(
									self.posición_x, self.posición_y,
									self.anchura_de_la_etiqueta, self.altura
									)
							self.etiqueta.setText(self.texto_sin_puntos)
		except IndexError:
			pass

	def método_de_deserialización(self, data):
		if self.llave is not None:
			try:
				self.deserialización(data[self.llave])
			except TypeError:
				self.deserialización(tratado_de_datos(data[self.llave]))

	def deserialización(self, dato):
		pass