from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.Nodo import Nodo
from nodeeditor.ContenidodelNodo import ContenidoDelNodo
from nodeeditor.GraficosdelNodo import GraficosdelNodo
from nodeeditor.Zocalos import Izquierda_centro, Derecha_centro
from nodeeditor.Utilidades import dump_exception


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
	
	def __init__(self, escena, entradas=[2, 2], salidas=[1]):
		super().__init__(escena, self.__class__.titulo_op, entradas, salidas)
		
		self.valor = None
		
		# Es realmente importante marcar los nodos indefinidos por defecto.
		self.marcarIndefinido()
	
	def initClasesInternas(self):
		self.contenido = CalcContenido(self)
		self.Nodograficas = GraphCalcNodo(self)
		
	def initConfiguraciones(self):
		super().initConfiguraciones()
		self.pos_det_entradas = Izquierda_centro
		self.pos_det_salidas = Derecha_centro
		
	def ImplementacionEvaluacion(self):
		return 123
	
	def evaluar(self):
		if not self.esIndefinido() and not self.esInvalido():
			print(" _> devolver valor %s en cache:" % self.__class__.__name__, self.valor)
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
		
		
	def DatosdeEntradaCambiados(self, nueva_conexion):
		print("%s::__DatosdeEntradaCambiados (Nodo base)" % self.__class__.__name__)
		self.marcarIndefinido()
		self.evaluar()
		
	def serializacion(self):
		res = super().serializacion()
		res['Codigo_op'] = self.__class__.codigo_op
		return res
	
	def deserializacion(self, data, hashmap={}, restaure_id=True):
		res = super().deserializacion(data, hashmap, restaure_id)
		print("Deserializando CalcNodo '%s'" % self.__class__.__name__, "res:", res)
		return res
		