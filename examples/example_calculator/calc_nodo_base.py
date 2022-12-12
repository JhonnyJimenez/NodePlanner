from PyQt5.QtWidgets import *
from nodeeditor.Nodo import Nodo
from nodeeditor.ContenidodelNodo import ContenidoDelNodo
from nodeeditor.GraficosdelNodo import GraficosdelNodo
from nodeeditor.Zocalos import Izquierda_centro, Derecha_centro


class GraphCalcNodo(GraficosdelNodo):
	def initSizes(self):
		super().initSizes()
		self.anchoNodo = 160
		self.altoNodo = 74
		self.redondezdelaOrilladelNodo = 6
		self.sangria_de_la_orilla = 0
		self.sangria_del_titulo = 8
		self.sangria_vertical_del_titulo = 10
		


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
	
	def initClasesInternas(self):
		self.contenido = CalcContenido(self)
		self.Nodograficas = GraphCalcNodo(self)
		
	def initConfiguraciones(self):
		super().initConfiguraciones()
		self.pos_det_entradas = Izquierda_centro
		self.pos_det_salidas = Derecha_centro