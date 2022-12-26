import math
import numpy

from PyQt5.QtWidgets import QLineEdit, QLabel, QCheckBox, QComboBox, QCalendarWidget, QDateEdit
from PyQt5.QtGui import QColor, QPainter, QBrush, QImage, QFont, QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt, QPointF, QRectF

from lib.nodeeditor.Nodo import Nodo
from lib.nodeeditor.Utilidades import dump_exception
from lib.nodeeditor.ContenidodelNodo import ContenidoDelNodo
from lib.nodeeditor.GraficosdelNodo import GraficosdelNodo
from lib.nodeeditor.Zocalos import *

from np_enlistado_de_nodos import *

CREANDO = False
DEBUG = False
imagen = "C:/Users/Maste/Downloads/icons/help (2).svg"

# ---------------------------------------------------------------------------------------------------------------------
# Zócalos y sus gráficos.

COLORES_DE_ZOCALOS = [
		QColor("#FFcca6d6"),  # 0. Zócalo de entrada y salida todoterreno
		QColor("#FF598c5c"),  # 1. Zócalo entero
		QColor("#FFa1a1a1"),  # 2. Zócalo decimal
		QColor("#FFcca6d6"),  # 3. Zócalo booleano
		QColor("#FF70b2ff"),  # 4. Zócalo de texto
		QColor("#FF633863"),  # 5. Zócalo para listas desplegables
		QColor("#FF6363c7"),  # 6. Zócalo vectorial
		QColor("#FFc7c729"),  # 7. Zócalo de color
		QColor("#FFed9e5c"),  # 8. Zócalo de objeto
		QColor("#FF00d6a3"),  # 9. Zócalo de geometría (Únicamente para zócalos de entrada en un nodo Salida)
		QColor("#FFf5f5f5"),  # 10. Zócalo de colecciones
		QColor("#FF9e4fa3"),  # 11. Zócalo de texturas
		QColor("#FFeb7582"),  # 12. Zócalo de material
		]

ZOCALOS_ROMBOS = [1, 2, 3, 6, 7]


class NodoBase_Zocalos_Graficador(GraficosDeZocalos):
	def initAssets(self):
		super().initAssets()

	def obtenerColorparaelZocalo(self, key):
		if type(key) == int:
			if len(COLORES_DE_ZOCALOS) - 1 < key:
				return Qt.transparent
			return COLORES_DE_ZOCALOS[key]
		elif type(key) == str:
			return QColor(key)
		return Qt.transparent

	def paint(self, painter: QPainter, QStyleOptionGraphicsItem, widget=None):
		painter.setBrush(self._brush)
		painter.setPen(self._pen if not self.isHighlighted else self._pen_highlight)

		if self.tipo_zocalo in ZOCALOS_ROMBOS:
			self.nuevo_radio_1 = self.radio * 1.20

			rombo = (
						QPointF(0.0, -self.nuevo_radio_1), QPointF(self.nuevo_radio_1, 0.0),
						QPointF(0.0, self.nuevo_radio_1), QPointF(-self.nuevo_radio_1, 0.0)
					)
			painter.drawPolygon(rombo)

			self.nuevo_radio = self.radio * 0.30
			rombo_pequeño = (
								QPointF(0.0, -self.nuevo_radio), QPointF(self.nuevo_radio, 0.0),
								QPointF(0.0, self.nuevo_radio), QPointF(-self.nuevo_radio, 0.0)
								)

			self._brush_nuevo = QBrush(self._color_contorno)
			painter.setBrush(self._brush_nuevo)
			painter.drawPolygon(rombo_pequeño)

		else:
			painter.drawEllipse(QRectF(-self.radio, -self.radio, 2 * self.radio, 2 * self.radio))


class NodoBase_Zocalos(Zocalo):
	ClaseGraficadeZocalos = NodoBase_Zocalos_Graficador

	def __init__(
			self, nodo, indice, posicion, tipo_zocalo=1, multiconexion=True, cantidad_en_el_lado_actual=1,
			esEntrada=False, espaciado_extra = []
			):
		self.espaciado_extra = espaciado_extra
		super().__init__(
				nodo, indice, posicion, tipo_zocalo, multiconexion, cantidad_en_el_lado_actual, esEntrada
				)

	def definir_posicion_del_zocalo(self):
		self.GraficosZocalos.setPos(
				*self.nodo.obtener_posicion_zocalo(
						self.indice, self.posicion, self.GraficosZocalos.radio, self.cantidad_en_el_lado_actual,
						self.espaciado_extra
						)
				)

	def posicion_zocalo(self):
		res = self.nodo.obtener_posicion_zocalo(
				self.indice, self.posicion, self.GraficosZocalos.radio, self.cantidad_en_el_lado_actual,
				self.espaciado_extra
				)
		return res

# ---------------------------------------------------------------------------------------------------------------------
# Gráficador del nodo.


class NodoBase_Graficador(GraficosdelNodo):
	def initSizes(self):
		super().initSizes()

		self.redondezdelaOrilladelNodo = 10.0
		self.sangria_de_la_orilla = 10.0  # Es el márgen desde cada orilla, arriba desde la etiqueta.
		# self.alturaTituloNodo = 24.0  # Es la altura de la etiqueta donde está el título.
		self.sangria_del_titulo = 10.0
		# self.sangria_vertical_del_titulo = 4.0  # No sé qué hace esto :v
		self.anchoNodo = 180
		self.altoNodo = 164
		self.altoNodoparaCalculos = self.altoNodo
		self.calculo_de_altura_disponible()

	def calculo_de_altura_disponible(self):
		self.altura_disponible = int(self.altoNodo - (2 * self.sangria_de_la_orilla) - self.alturaTituloNodo)
		return self.altura_disponible

	def initAssets(self):
		super().initAssets()
		self.iconos = QImage("lib/examples/example_calculator/iconos/status_icons.png")
		self._relleno_fondo_nodo = QBrush(QColor("#FF303030"))

	def mouseMoveEvent(self, evento):
		super().mouseMoveEvent(evento)

		# ¡Optimízame! ¡Solo actualizo los nodos seleccionados!
		for nodo in self.scene().escena.Nodos:
			for zocalo in nodo.entradas + nodo.salidas:
				for conexion in zocalo.Zocaloconexiones:
					conexion.GraficosDeConexion.definirColordesdeelZocalo()
			if nodo.Nodograficas.isSelected():
				nodo.actualizarconexiones()
		self._elemento_movido = True

	def paint(self, painter, QStyleOptionGraphicsItem, widget = None):
		super().paint(painter, QStyleOptionGraphicsItem, widget)

		offset = 24.0
		if self.nodo.esIndefinido():
			offset = 0.0
		if self.nodo.esInvalido():
			offset = 48.0

		painter.drawImage(
				QRectF(-10, -10, 24.0, 24.0),
				self.iconos,
				QRectF(offset, 0, 24.0, 24.0)
				)

# ---------------------------------------------------------------------------------------------------------------------
# Contenido del nodo.


class NodoBase_Contenido(ContenidoDelNodo):
	def initui(self):
		self.configuraciones()
		self.posicion_libre = [0]
		self.contenidos()

		self.calculo_de_altura = (
									(self.posicion_libre[-1] - self.espaciado_entre_objetos_del_nodo)
									+ (self.sangria_de_la_orilla * 2) + self.alturaTituloNodo
									)

		if CREANDO:
			print("La altura del nodo %s debe ser:" % self.nodo.__class__.__name__, self.calculo_de_altura)

	def contenidos(self):
		self.etiqueta_1 = self.etiqueta("Tipos de entrada", 'Centro')
		self.objeto_1 = self.entrada_de_línea(1, "Cadena")
		self.objeto_2 = self.entrada_de_línea(2, '0', 'Númerica', QDoubleValidator())
		self.objeto_3 = self.entrada_booleana(3, 1, "Booleana", True)
		self.objeto_4 = self.lista_desplegable(4, 'Lista')

	def etiqueta(self, texto_inicial = None, alineado: int | str = 1, fuente = None, altura: int = None):
		if fuente is None:
			fuente = self.fuente
		if altura is None:
			altura = self.altura_por_defecto
		posicion_y = self.posicion_libre[-1]

		etiqueta = QLabel(texto_inicial, self)
		etiqueta.setStyleSheet('padding-left: 1px; background: transparent')
		etiqueta.setGeometry(0, posicion_y, self.ancho_disponible, altura)
		if alineado in (1, 'Izquierda'):
			etiqueta.setAlignment(Qt.AlignLeft)
		elif alineado in (2, 'Centro'):
			etiqueta.setAlignment(Qt.AlignCenter)
		elif alineado in (3, 'Derecha'):
			etiqueta.setAlignment(Qt.AlignRight)
		etiqueta.setFont(fuente)
		self.posicion_libre.append(posicion_y + altura + self.espaciado_entre_objetos_del_nodo)
		return etiqueta

	def entrada_de_línea(
			self, zocalo: int = None, texto_inicial: object = '', texto_etiqueta: str = None, validante: object = None,
			altura: int = None, fuente: object = None
			):
		if fuente is None:
			fuente = self.fuente
		if altura is None:
			altura = self.altura_por_defecto
		posicion_y = self.posicion_libre[-1]

		línea = QLineEdit(texto_inicial, self)

		if zocalo == 0:
			línea.zocalo = zocalo
		elif zocalo is None:
			pass
		else:
			línea.zocalo = zocalo - 1

		if texto_etiqueta == '' or texto_etiqueta is None:
			línea.setGeometry(0, posicion_y, self.ancho_disponible, altura)
		else:
			if texto_etiqueta[-1] != ':':
				texto_etiqueta += ':'
			etiqueta = QLabel(texto_etiqueta, self)
			etiqueta.setGeometry(0, posicion_y, self.ancho_etiqueta, altura)
			etiqueta.setStyleSheet('padding-left: 1px; background: transparent')
			etiqueta.setAlignment(Qt.AlignVCenter)
			etiqueta.setFont(fuente)
			línea.setGeometry(
					self.ubicación_elemento,
					posicion_y,
					self.ancho_elemento,
					altura)

		línea.setAlignment(Qt.AlignCenter)

		línea.setFont(fuente)
		línea.setValidator(validante)
		self.posicion_libre.append(posicion_y + altura + self.espaciado_entre_objetos_del_nodo)
		return línea

	def entrada_booleana(
			self, zocalo: int = None, valor_inicial: int = 0, texto_etiqueta: str = 'Valor',
			indeterminado: bool = False, altura: int = 20, fuente = None
			):
		if fuente is None:
			fuente = self.fuente
		if altura is None:
			altura = self.altura_por_defecto
		posicion_y = self.posicion_libre[-1]

		booleana = QCheckBox(texto_etiqueta, self)

		if zocalo == 0:
			booleana.zocalo = zocalo
		elif zocalo is None:
			pass
		else:
			booleana.zocalo = zocalo - 1

		booleana.setGeometry(0, posicion_y, self.ancho_disponible, altura)
		booleana.setStyleSheet('padding-left: 1px; color: #fff; background: transparent')
		booleana.setTristate(indeterminado)
		booleana.setCheckState(valor_inicial)
		booleana.setFont(fuente)
		self.posicion_libre.append(posicion_y + altura + self.espaciado_entre_objetos_del_nodo)
		return booleana

	def lista_desplegable(
			self, zocalo = None, texto_etiqueta: str = None, elementos_visibles: int = 10, listado: list = None,
			separadores: list = None, popup: bool = False, fuente = None, altura: str = 20
			):
		if fuente is None:
			fuente = self.fuente
		if altura is None:
			altura = self.altura_por_defecto
		posicion_y = self.posicion_libre[-1]

		lista = QComboBox(self)

		if zocalo == 0:
			lista.zocalo = zocalo
		elif zocalo is None:
			pass
		else:
			lista.zocalo = zocalo - 1

		if texto_etiqueta == '' or texto_etiqueta is None:
			lista.setGeometry(0, posicion_y, self.ancho_disponible, altura)
		else:
			if texto_etiqueta[-1] != ':':
				texto_etiqueta += ':'
			etiqueta = QLabel(texto_etiqueta, self)
			etiqueta.setGeometry(0, posicion_y, self.ancho_etiqueta, altura)
			etiqueta.setStyleSheet('padding-left: 1px; background: transparent')
			etiqueta.setAlignment(Qt.AlignVCenter)
			etiqueta.setFont(fuente)
			lista.setGeometry(
					self.ubicación_elemento,
					posicion_y,
					self.ancho_elemento,
					altura
					)

		lista_por_defecto = [
				"Objeto 1", "Objeto 2", "Objeto 3", "Objeto 4", "Objeto 5", "Objeto 6", "Objeto 7", "Objeto 8",
				"Objeto 9", "Objeto 10", "Objeto 11",
				]
		if listado is not None:
			if len(listado) != 0:
				lista.addItems(listado)
			else:
				lista.addItems(lista_por_defecto)
		else:
			lista.addItems(lista_por_defecto)

		cantidad_separadores = 0
		if separadores is not None:
			if len(separadores) != 0:
				for separador in separadores:
					cantidad_separadores += 1
					lista.insertSeparator(separador)

		lista.setMaxVisibleItems(elementos_visibles + cantidad_separadores)

		if not popup:
			lista.setStyleSheet('combobox-popup: 0; background: #808080')

		self.posicion_libre.append(posicion_y + altura + self.espaciado_entre_objetos_del_nodo)
		return lista

	def configuraciones(self):
		self.redondezdelaOrilladelNodo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).redondezdelaOrilladelNodo
		self.sangria_de_la_orilla = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).sangria_de_la_orilla
		self.alturaTituloNodo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).alturaTituloNodo
		self.sangria_del_titulo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).sangria_del_titulo
		self.sangria_vertical_del_titulo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).sangria_vertical_del_titulo
		self.anchoNodo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).anchoNodo
		self.altoNodo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).altoNodo

		self.altura_disponible = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).altura_disponible
		self.ancho_disponible = int(self.anchoNodo - (2 * self.sangria_de_la_orilla))
		self.espaciado_entre_objetos_del_nodo = 5
		self.altura_por_defecto = 20

		# Tamaños para elementos con etiquetas.
		self.separación = 1
		self.divisor = 3
		self.proporción = (self.ancho_disponible // self.divisor)

		self.ancho_etiqueta = self.proporción - self.separación
		self.ubicación_elemento = self.proporción + self.separación
		self.ancho_elemento = (self.proporción * (self.divisor - 1)) - self.separación

		# Fuente
		self.fuente = QFont("Ubuntu")

	def serializacion(self):
		res = super().serializacion()
		self.lista_a_serializar(res)
		return res

	def deserializacion(self, data, hashmap={}):
		res = super().deserializacion(data, hashmap)
		try:
			self.lista_a_desearializar(data)
			return True
		except Exception as e:
			dump_exception(e)
		return res

	def lista_a_serializar(self, res):
		res['Objeto_1'] = self.objeto_1.text()
		res['Objeto_2'] = self.objeto_2.text()
		res['Objeto_3'] = self.objeto_3.checkState()
		res['Objeto_4'] = self.objeto_4.currentText()

	def lista_a_desearializar(self, data):
		self.objeto_1.setText(data['Objeto_1'])
		self.objeto_2.setText(data['Objeto_2'])
		self.objeto_3.setCheckState(data['Objeto_3'])
		self.objeto_4.setCurrentText(data['Objeto_4'])


# ---------------------------------------------------------------------------------------------------------------------
# Nodo


# @registrar_nodo(NODO_BASE)
class NodoBase(Nodo):
	icono = imagen
	codigo_op = NODO_BASE
	titulo_op = "Nodo base"
	content_label = None
	content_label_objname = None

	ClaseGraficadeNodo = NodoBase_Graficador
	ClasedelContenidodeNodo = NodoBase_Contenido
	ClasedeZocalo = NodoBase_Zocalos

	def __init__(self, escena, titulo = titulo_op, entradas=[], salidas=[1, 2, 3, 4]):
		super().__init__(escena, titulo, entradas, salidas)
		self.marcarIndefinido()
		self.actualizacion()
		self.evaluar()

	def initConfiguraciones(self):
		super().initConfiguraciones()
		self.espaciadoconectores = 25  # El original es de 22.
		self.pos_det_entradas = Izquierda_abajo
		self.pos_det_salidas = Derecha_arriba

	def initZocalos(self, entradas, salidas, reset=True):
		# Creación de zócalos para las entradas y salidas.

		if reset:
			# Limpiar los zócalos viejos.
			if hasattr(self, 'entradas') and hasattr(self, 'salidas'):
				# Quitar zócalos de la escena.
				for zocalo in (self.entradas + self.salidas):
					self.escena.GraficosEsc.removeItem(zocalo.GraficosZocalos)
				self.entradas = []
				self.salidas = []

		self.valores_entrantes = []
		self.valores = []
		self.espaciado_entradas = []
		self.espaciado_salidas = []

		for zocalo in entradas:
			self.espaciado_entradas.append(0)
			self.valores_entrantes.append(None)

		for zocalo in salidas:
			self.espaciado_salidas.append(0)
			self.valores.append(None)

		if DEBUG:
			print(self.espaciado_entradas)
			print(self.espaciado_salidas)
			print(self.valores)

		self.ediciones_de_espaciado()

		# Creación de los nuevos zócalos.
		contador = 0
		for objeto in entradas:
			zocalo = self.__class__.ClasedeZocalo(
				nodo = self, indice = contador, posicion = self.pos_det_entradas,
				tipo_zocalo = objeto, multiconexion = self.entradas_multiconexion,
				cantidad_en_el_lado_actual = len(entradas), esEntrada = True, espaciado_extra = self.espaciado_entradas
				)
			contador += 1
			self.entradas.append(zocalo)

		contador = 0
		for objeto in salidas:
			zocalo = self.__class__.ClasedeZocalo(
				nodo = self, indice = contador, posicion = self.pos_det_salidas,
				tipo_zocalo = objeto, multiconexion = self.salidas_multiconexion,
				cantidad_en_el_lado_actual = len(salidas), esEntrada = False, espaciado_extra = self.espaciado_salidas
				)
			contador += 1
			self.salidas.append(zocalo)

	def obtener_posicion_zocalo(self, indice, posicion, radio, num_out_of = 1, lista_de_espaciado = []):
		x = (
				self.zocalos_offsets[posicion]
				if posicion in (Izquierda_arriba, Izquierda_centro, Izquierda_abajo)
				else self.Nodograficas.anchoNodo + self.zocalos_offsets[posicion]
				)

		espaciado = None
		try:
			if type(lista_de_espaciado[indice]) in (int, float):
				espaciado = int(lista_de_espaciado[indice])
			else:
				espaciado = 0
		except IndexError as e:
			espaciado = 0

		if posicion in (Izquierda_abajo, Derecha_abajo):
			# Comenzando desde abajo.
			y = (
				self.Nodograficas.altoNodoparaCalculos
				- self.Nodograficas.redondezdelaOrilladelNodo
				- self.Nodograficas.sangria_vertical_del_titulo
				- radio
				- (((num_out_of - 1) - indice) * self.espaciadoconectores)
				- espaciado
				)
		elif posicion in (Izquierda_centro, Derecha_centro):
			no_de_zocalos = num_out_of
			altura_del_nodo = self.Nodograficas.altoNodoparaCalculos
			altura_no_usable = self.Nodograficas.alturaTituloNodo + 2 * self.Nodograficas.sangria_vertical_del_titulo + self.Nodograficas.sangria_de_la_orilla
			altura_disponible = altura_del_nodo - altura_no_usable

			altura_total_de_todos_los_zocalos = num_out_of * self.espaciadoconectores
			nueva_altura = altura_disponible - altura_total_de_todos_los_zocalos

			y = altura_no_usable + altura_disponible / 2.0 + (indice - 0.5) * self.espaciadoconectores
			if no_de_zocalos > 1:
				y -= self.espaciadoconectores * (no_de_zocalos - 1) / 2

		elif posicion in (Izquierda_arriba, Derecha_arriba):
			# Comenzando desde arriba.
			y = (
					self.Nodograficas.alturaTituloNodo
					+ self.Nodograficas.sangria_vertical_del_titulo
					+ self.Nodograficas.redondezdelaOrilladelNodo
					+ (indice * self.espaciadoconectores)
					+ radio
					+ espaciado
					)
		else:
			# Esto nunca debe pasar.
			y = 0

		return [x, y]

	def ediciones_de_espaciado(self):
		self.editor_de_espaciado(0, 2, 25)

	def editor_de_espaciado(self, indice, lista: list | int, valor):
		if type(lista) is int:
			if lista == 1:
				lista = self.espaciado_entradas
			elif lista == 2:
				lista = self.espaciado_salidas
		else:
			pass

		indice_fun = indice
		contador = indice_fun - 1
		for elemento in lista[indice_fun:]:
			contador += 1
			lista[lista.index(elemento, contador)] += valor

		if DEBUG:
			print("Los ajustes de entradas son:", self.espaciado_entradas)
			print("Los ajustes de salidas son:", self.espaciado_salidas)

	def obtenerPosiciondeZocaloenEscena(self, zocalo):
		pos_nodo = self.Nodograficas.pos()
		pos_zocalo = self.obtener_posicion_zocalo(
				zocalo.indice, zocalo.posicion, zocalo.GraficosZocalos.radio, zocalo.cantidad_en_el_lado_actual,
				zocalo.espaciado_extra
				)
		return (pos_nodo.x() + pos_zocalo[0], pos_nodo.y() + pos_zocalo[1])

	def actualizacion(self):
		self.contenido.objeto_1.textChanged.connect(self.DatosdeEntradaCambiados)
		self.contenido.objeto_2.textChanged.connect(self.DatosdeEntradaCambiados)
		self.contenido.objeto_3.stateChanged.connect(self.DatosdeEntradaCambiados)
		self.contenido.objeto_4.currentTextChanged.connect(self.DatosdeEntradaCambiados)

	def ImplementarEvaluacion(self):
		self.EvaluacionNumerica(self.contenido.objeto_1)
		self.EvaluacionNumerica(self.contenido.objeto_2)
		self.EvaluacionBooleana(self.contenido.objeto_3)
		self.EvaluacionListado(self.contenido.objeto_4)
		self.evaluarHijos()

	def evaluar(self):
		# Actualiza las posiciones de los zócalos.
		for zocalo in self.entradas + self.salidas:
			zocalo.definir_posicion_del_zocalo()
		try:
			evaluacion = self.ImplementarEvaluacion()
			self.zocalos_tooltip()
			return evaluacion
		except ValueError as e:
			self.marcarInvalido()
			self.Nodograficas.setToolTip(str(e))
		except Exception as e:
			print("Exception")
			self.marcarInvalido()
			self.Nodograficas.setToolTip(str(e))
			dump_exception(e)

	def zocalos_tooltip(self):
		no_calculado = "El valor de zócalo aún no ha sido calculado"

		for zocalo in (self.entradas + self.salidas):
			if zocalo.esEntrada:
				nodo_de_entrada = self.obtenerEntrada(0)
				contrazocalo = self.obtenerContrazocalo(0)
				if not nodo_de_entrada:
					zocalo.GraficosZocalos.setToolTip(no_calculado)
				else:
					valor = self.textualizador(nodo_de_entrada.valores[contrazocalo.indice], True)
					zocalo.GraficosZocalos.setToolTip(valor)
			elif zocalo.esSalida:
				if zocalo.Zocaloconexiones != []:
					valor = self.valores[zocalo.indice]
					if valor is None:
						zocalo.GraficosZocalos.setToolTip(no_calculado)
					elif valor is not None:
						valor = self.textualizador(valor, True)
						zocalo.GraficosZocalos.setToolTip(valor)
					else:
						# En teoría, esta tooltip nunca debería salir.
						zocalo.GraficosZocalos.setToolTip("Puede haber un error.")
				else:
					zocalo.GraficosZocalos.setToolTip(no_calculado)
			else:
				# Esto es para evitar crasheos por si algún día llego a implementar los zocalos para redireccionar
				# conexiones.
				print("Hubo un problema al crear los tooltips de los zócalos. Revisa la evaluación del nodo base.")
				pass

	def textualizador(self, valor, especificacion: bool = False):
		respuesta_booleana = 'No deberías poder ver esta respuesta.'
		if type(valor) == Qt.CheckState:
			if valor == 0:
				respuesta_booleana = 'Falso'
			if valor == 1:
				respuesta_booleana = 'Indeterminado'
			if valor == 2:
				respuesta_booleana = 'Verdadero'

		if especificacion:
			if type(valor) == str:
				valor_resuelto = valor + ' (Cadena)'
			elif type(valor) == int:
				valor_resuelto = str(valor) + ' (Entero)'
			elif type(valor) == float:
				valor_resuelto = str(valor) + ' (Decimal)'
			elif type(valor) == Qt.CheckState:
				valor_resuelto = respuesta_booleana + ' (Booleana)'
		else:
			if type(valor) == Qt.CheckState:
				valor_resuelto = respuesta_booleana
			elif type(valor) == str:
				valor_resuelto = valor
			else:
				valor_resuelto = str(valor)

		return valor_resuelto

	def Evaluacion_de_texto(self, objeto):
		self.valores[objeto.zocalo] = objeto.text()

		self.marcarIndefinido(False)
		self.marcarInvalido(False)
		self.Nodograficas.setToolTip("")

		return self.valores[objeto.zocalo]

	def Evaluacion_de_enteros(self, objeto):
		if self.valores[objeto.zocalo] == '':
			self.valores[objeto.zocalo] = 0

		self.valores[objeto.zocalo] = int(objeto.text())
		self.marcarIndefinido(False)
		self.marcarInvalido(False)
		self.Nodograficas.setToolTip("")

		return self.valores[objeto.zocalo]

	def Evaluacion_de_decimales(self, objeto):
		if self.valores[objeto.zocalo] == '':
			self.valores[objeto.zocalo] = 0.0

		self.valores[objeto.zocalo] = float(objeto.text())
		self.marcarIndefinido(False)
		self.marcarInvalido(False)
		self.Nodograficas.setToolTip("")

		return self.valores[objeto.zocalo]

	def EvaluacionBooleana(self, objeto):
		self.valores[objeto.zocalo] = objeto.checkState()
		self.marcarIndefinido(False)
		self.marcarInvalido(False)

		return self.valores[objeto.zocalo]

	def EvaluacionListado(self, objeto):
		self.valores[objeto.zocalo] = objeto.currentText()
		self.marcarIndefinido(False)
		self.marcarInvalido(False)

		return self.valores[objeto.zocalo]

	def DatosdeConexionCambiados(self, conexion):
		try:
			conexion.GraficosDeConexion.definirColordesdeelZocalo()
			self.zocalos_tooltip()
		except AttributeError as e:
			if DEBUG:
				print(
						'Dibujaste una nueva conexión sobreescribiendo una existente y que al borrarse, ya no puede '
						'encontrarse ni actualizar su color. Por eso salta este error.'
						)

	def DatosdeEntradaCambiados(self, zocalo = None):
		self.marcarIndefinido()
		self.evaluar()

	def obtenerContrazocalo(self, indice=0):
		try:
			zocalo_entrada = self.entradas[indice]
			if len(zocalo_entrada.Zocaloconexiones) == 0: return None
			conexion_conectada = zocalo_entrada.Zocaloconexiones[0]
			contrazocalo = conexion_conectada.obtenerOtrosZocalos(self.entradas[indice])
			return contrazocalo
		except Exception as e:
			dump_exception(e)
			return None

	def serializacion(self):
		res = super().serializacion()
		res['Codigo_op'] = self.__class__.codigo_op
		return res

	def deserializacion(self, data, hashmap = {}, restaure_id = True):
		res = super().deserializacion(data, hashmap, restaure_id)
		return res