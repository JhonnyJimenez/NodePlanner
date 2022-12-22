from PyQt5.QtGui import QColor, QPainter, QBrush, QImage, QDoubleValidator
from PyQt5.QtCore import Qt, QPointF, QRectF

from lib.nodeeditor.Nodo import Nodo
from lib.nodeeditor.Utilidades import dump_exception
from lib.nodeeditor.ContenidodelNodo import ContenidoDelNodo
from lib.nodeeditor.GraficosdelNodo import GraficosdelNodo
from lib.nodeeditor.Zocalos import *

from np_enlistado_de_nodos import *

imagen = "C:/Users/Maste/Downloads/icons/help (2).svg"

COLORES_DE_ZOCALOS = [
		QColor("#FFcca6d6"),  # 0. Zócalo decimal
		QColor("#FF598c5c"),  # 1. Zócalo entero
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


class NodoBase_Graficador(GraficosdelNodo):
	def initSizes(self):
		super().initSizes()

		self.cantidad_de_zocalos = 24
		self.tamaño_widget = 20
		self.espaciado_widgets = 5
		self.tamaño_extra = 0

		self.anchoNodo = 180
		self.altoNodo = 240
		self.redondezdelaOrilladelNodo = 6
		self.sangria_de_la_orilla = 0
		self.sangria_del_titulo = 10
		self.sangria_vertical_del_titulo = 10

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


class NodoBase_Contenido(ContenidoDelNodo):
	def initui(self):
		self.anchoNodo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).anchoNodo
		self.altoNodo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).altoNodo
		self.redondezdelaOrilladelNodo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).redondezdelaOrilladelNodo
		self.sangria_de_la_orilla = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).sangria_de_la_orilla
		self.alturaTituloNodo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).alturaTituloNodo
		self.sangria_del_titulo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).sangria_del_titulo
		self.sangria_vertical_del_titulo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).sangria_vertical_del_titulo


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

	def __init__(self, escena, titulo = titulo_op, entradas=[], salidas=[]):
		super().__init__(escena, titulo, entradas, salidas)
		self.valores = []
		if len(self.salidas) != 0:
			for zocalo in self.salidas:
				self.valores.append(None)

		self.marcarIndefinido()

	def initConfiguraciones(self):
		super().initConfiguraciones()
		# self.espaciadoconectores = 25
		self.pos_det_entradas = Izquierda_abajo
		self.pos_det_salidas = Derecha_arriba

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