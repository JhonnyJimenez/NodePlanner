from PyQt5.QtWidgets import QLineEdit, QLabel, QCheckBox, QComboBox, QCalendarWidget, QDateEdit
from PyQt5.QtGui import QColor, QPainter, QBrush, QImage, QFont, QDoubleValidator
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
		QColor("#FFcca6d6"),  # 0. Zócalo para listas desplegables
		QColor("#FF598c5c"),  # 1. Zócalo númerico
		QColor("#FFcca6d6"),  # 2. Zócalo booleano
		QColor("#FF6363c7"),  # 3. Zócalo vectorial
		QColor("#FF70b2ff"),  # 4. Zócalo de texto
		QColor("#FFc7c729"),  # 5. Zócalo de color
		QColor("#FFed9e5c"),  # 6. Zócalo de objeto
		QColor("#FF633863"),  # 7. Zócalo de imagen
		QColor("#FF00d6a3"),  # 8. Zócalo de geometría (Únicamente para zócalos de entrada en un nodo Salida)
		QColor("#FFf5f5f5"),  # 9. Zócalo de colecciones
		QColor("#FF9e4fa3"),  # 10. Zócalo de texturas
		QColor("#FFeb7582"),  # 11. Zócalo de material
		]

USOS_DE_ZOCALOS = [
		"Zócalo decimal",
		"Zócalo entero",
		"Zócalo booleano",
		"Zócalo vectorial",
		"Zócalo de texto",
		"Zócalo de color",
		"Zócalo de objeto",
		"Zócalo de imagen",
		"Zócalo de geometría",
		"Zócalo de colecciones",
		"Zócalo de texturas",
		"Zócalo de material",
		]

ZOCALOS_ROMBOS = [0, 1, 2, 3, 5]


class NodoBase_Zocalos_Graficador(GraficosDeZocalos):
	def initAssets(self):
		super().initAssets()
		self.setToolTip(USOS_DE_ZOCALOS[self.tipo_zocalo])

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
		self.calculo_de_altura_disponible()

	def calculo_de_altura_disponible(self):
		self.altura_disponible = int(self.altoNodo - (2 * self.sangria_de_la_orilla) - self.alturaTituloNodo)
		return self.altura_disponible

	def initAssets(self):
		super().initAssets()
		self.iconos = QImage("lib/examples/example_calculator/iconos/status_icons.png")
		self._relleno_fondo_nodo = QBrush(QColor("#FF303030"))

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
		muestra1 = self.etiqueta("Tipos de entrada", 'Centro')
		muestra2 = self.entrada_de_línea(1, "Cadena")
		muestra3 = self.entrada_de_línea(2, '0', 'Númerica', QDoubleValidator())
		muestra4 = self.entrada_booleana(3, 1, "Booleana", True)
		muestra5 = self.lista_desplegable('Lista')

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
			línea.zocalo = 0
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
			booleana.zocalo = 0
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
			self, texto_etiqueta: str = None, elementos_visibles: int = 10, listado: list = None,
			separadores: list = None, popup: bool = False, fuente = None, altura: str = 20
			):
		if fuente is None:
			fuente = self.fuente
		if altura is None:
			altura = self.altura_por_defecto
		posicion_y = self.posicion_libre[-1]

		lista = QComboBox(self)
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

	def __init__(self, escena, titulo = titulo_op, entradas=[4, 2, 3, 0], salidas=[4, 2, 3, 0]):
		super().__init__(escena, titulo, entradas, salidas)
		self.marcarIndefinido()
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

		self.valores = []
		self.espaciado_entradas = []
		self.espaciado_salidas = []

		for zocalo in entradas:
			self.espaciado_entradas.append(0)

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
				self.Nodograficas.altoNodo
				- self.Nodograficas.redondezdelaOrilladelNodo
				- self.Nodograficas.sangria_vertical_del_titulo
				- radio
				- (((num_out_of - 1) - indice) * self.espaciadoconectores)
				- espaciado
				)
		elif posicion in (Izquierda_centro, Derecha_centro):
			no_de_zocalos = num_out_of
			altura_del_nodo = self.Nodograficas.altoNodo
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
		# Este método no se está usando. Si se llega a necesitar, hay que recordar cambiar los datos que requiere por
		# las modificaciones que le hice al método "obtener_posicion_zocalo".
		pass

	def ImplementarEvaluacion(self):
		pass

	def evaluar(self):
		try:
			evaluacion = self.ImplementarEvaluacion()
			return evaluacion
		except ValueError as e:
			self.marcarInvalido()
			self.Nodograficas.setToolTip(str(e))
		except Exception as e:
			self.marcarInvalido()
			self.Nodograficas.setToolTip(str(e))
			dump_exception(e)

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