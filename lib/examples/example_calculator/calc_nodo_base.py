from PyQt5.QtGui import QImage
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QLabel
from lib.nodeeditor.Nodo import Nodo
from lib.nodeeditor.ContenidodelNodo import ContenidoDelNodo
from lib.nodeeditor.GraficosdelNodo import GraficosdelNodo
from lib.nodeeditor.Zocalos import IZQUIERDA_CENTRO, DERECHA_CENTRO
from lib.nodeeditor.Utilidades import dump_exception


class GraphCalcNodo(GraficosdelNodo):
	def init_sizes(self):
		super().init_sizes()
		self.anchura_del_nodo = 160
		self.altura_del_nodo = 74
		self.redondez_del_nodo = 6
		self.márgen = 0
		self.sangría_del_título = 8
		self.sangría_vertical_del_título = 10
		
	def init_assets(self):
		super().init_assets()
		self.iconos = QImage("iconos/status_icons.png")
		
	def paint(self, dibujante, estilo: QStyleOptionGraphicsItem, widget=None):
		super().paint(dibujante, estilo, widget)
		
		offset = 24.0
		if self.nodo.es_indefinido(): offset = 0.0
		if self.nodo.es_inválido(): offset = 48.0
		
		dibujante.drawImage(
			QRectF(-10, -10, 24.0, 24.0),
			self.iconos,
			QRectF(offset, 0, 24.0, 24.0)
		)

class CalcContenido(ContenidoDelNodo):
	def init_ui(self):
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
		self.marcar_indefinido()
		
	def init_configuraciones(self):
		super().init_configuraciones()
		self.pos_det_entradas = IZQUIERDA_CENTRO
		self.pos_det_salidas = DERECHA_CENTRO
		
	def realizar_operación(self, entrada1, entrada2):
		return 123
	
	def implementar_evaluación(self):
		e1 = self.obtener_entrada(0)
		e2 = self.obtener_entrada(1)
		
		if e1 is None or e2 is None:
			self.marcar_inválido()
			self.marcar_descendencia_indefinido()
			self.Nodograficas.setToolTip("Conecte todas las entradas, por favor")
			return None
		
		else:
			val = self.realizar_operación(e1.evaluación(), e2.evaluación())
			self.valor = val
			self.marcar_indefinido(False)
			self.marcar_inválido(False)
			self.Nodograficas.setToolTip("")
			
			self.marcar_descendencia_indefinido()
			self.evaluar_hijos()
			
			return val
	
	def evaluación(self):
		if not self.es_indefinido() and not self.es_inválido():
			# print(" _> devolver valor %s en cache:" % self.__class__.__name__, self.valor)
			return self.valor
		
		try:
			
			val = self.implementar_evaluación()
			return val
		except ValueError as e:
			self.marcar_inválido()
			self.Nodograficas.setToolTip(str(e))
			self.marcar_descendencia_indefinido()
		except Exception as e:
			self.marcar_inválido()
			self.Nodograficas.setToolTip(str(e))
			dump_exception(e)
		
	def datos_de_entrada_cambiados(self, zocalo=None):
		# print("%s::__DatosdeEntradaCambiados (Nodo base)" % self.__class__.__name__)
		self.marcar_indefinido()
		self.evaluación()
		
	def serialización(self):
		res = super().serialización()
		res['Código op'] = self.__class__.codigo_op
		return res
	
	def deserialización(self, data, hashmap={}, restaure_id=True):
		res = super().deserialización(data, hashmap, restaure_id)
		# print("Deserializando CalcNodo '%s'" % self.__class__.__name__, "res:", res)
		return res
		