from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from lib.nodeeditor.Nodo import Nodo
from lib.nodeeditor.ContenidodelNodo import ContenidoDelNodo
from lib.nodeeditor.GraficosdelNodo import GraficosdelNodo
from lib.nodeeditor.Zocalos import Izquierda_centro, Derecha_centro
from lib.nodeeditor.Utilidades import dump_exception


class GraphCalcNodo(GraficosdelNodo):
	def initSizes(self):
		super().initSizes()
		self.anchoNodo = 160
		self.altoNodo = 74
		self.redondezdelaOrilladelNodo = 6
		self.sangria_de_la_orilla = 0
		self.sangria_del_titulo = 8
		self.sangria_vertical_del_titulo = 10
		
	def initAssets(self):
		super().initAssets()
		self.iconos = QImage("iconos/status_icons.png")
		
	def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
		super().paint(painter, QStyleOptionGraphicsItem, widget)
		
		offset = 24.0
		if self.nodo.esIndefinido(): offset = 0.0
		if self.nodo.esInvalido(): offset = 48.0
		
		painter.drawImage(
			QRectF(-10, -10, 24.0, 24.0),
			self.iconos,
			QRectF(offset, 0, 24.0, 24.0)
		)

class CalcContenido(ContenidoDelNodo):
	def initui(self):
		lbl = QLabel(self.nodo.content_label, self)
		lbl.setObjectName(self.nodo.content_label_objname)

class CalcNodo(Nodo):
	icono = ""
	codigo_op = 0
	titulo_op = "Indefinido"
	content_label = None
	content_label_objname = "calc_nodo_bg"
	
	ClaseGraficadeNodo = GraphCalcNodo
	ClasedelContenidodeNodo = CalcContenido
	
	def __init__(self, escena, entradas=[2, 2], salidas=[1]):
		super().__init__(escena, self.__class__.titulo_op, entradas, salidas)
		
		self.valor = None
		
		# Es realmente importante marcar los nodos indefinidos por defecto.
		self.marcarIndefinido()
		
	def initConfiguraciones(self):
		super().initConfiguraciones()
		self.pos_det_entradas = Izquierda_centro
		self.pos_det_salidas = Derecha_centro
		
	def realizarOperacion(self, entrada1, entrada2):
		return 123
	
	def ImplementacionEvaluacion(self):
		e1 = self.obtenerEntrada(0)
		e2 = self.obtenerEntrada(1)
		
		if e1 is None or e2 is None:
			self.marcarInvalido()
			self.marcarDescendenciaIndefinido()
			self.Nodograficas.setToolTip("Conecte todas las entradas, por favor")
			return None
		
		else:
			val = self.realizarOperacion(e1.evaluar(), e2.evaluar())
			self.valor = val
			self.marcarIndefinido(False)
			self.marcarInvalido(False)
			self.Nodograficas.setToolTip("")
			
			self.marcarDescendenciaIndefinido()
			self.evaluarHijos()
			
			return val
	
	def evaluar(self):
		if not self.esIndefinido() and not self.esInvalido():
			# print(" _> devolver valor %s en cache:" % self.__class__.__name__, self.valor)
			return self.valor
		
		try:
			
			val = self.ImplementacionEvaluacion()
			return val
		except ValueError as e:
			self.marcarInvalido()
			self.Nodograficas.setToolTip(str(e))
			self.marcarDescendenciaIndefinido()
		except Exception as e:
			self.marcarInvalido()
			self.Nodograficas.setToolTip(str(e))
			dump_exception(e)
		
	def DatosdeEntradaCambiados(self, zocalo=None):
		# print("%s::__DatosdeEntradaCambiados (Nodo base)" % self.__class__.__name__)
		self.marcarIndefinido()
		self.evaluar()
		
	def serializacion(self):
		res = super().serializacion()
		res['Codigo_op'] = self.__class__.codigo_op
		return res
	
	def deserializacion(self, data, hashmap={}, restaure_id=True):
		res = super().deserializacion(data, hashmap, restaure_id)
		# print("Deserializando CalcNodo '%s'" % self.__class__.__name__, "res:", res)
		return res
		