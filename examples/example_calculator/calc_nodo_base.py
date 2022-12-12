from PyQt5.QtWidgets import *
from nodeeditor.Nodo import Nodo
from nodeeditor.ContenidodelNodo import ContenidoDelNodo
from nodeeditor.GraficosdelNodo import GraficosdelNodo


class GraphCalcNodo(GraficosdelNodo):
	def initSizes(self):
		super().initSizes()
		self.anchoNodo = 160
		self.altoNodo = 74
		self.redondezNodo = 5
		self._sangria = 8


class CalcContenido(ContenidoDelNodo):
	def initui(self):
		lbl = QLabel(self.nodo.content_label, self)
		lbl.setObjectName(self.nodo.content_label_objname)

class CalcNodo(Nodo):
	def __init__(self, escena, codigo_operacion, titulo_operacion, content_label="", content_label_objname="calc_nodo_bg", entradas=[2, 2], salidas=[1]):
		self.codigo_operacion = codigo_operacion
		self.titulo_operacion = titulo_operacion
		self.content_label = content_label
		self.content_label_objname = content_label_objname
		
		super().__init__(escena, self.titulo_operacion, entradas, salidas)
	
	def initClasesInternas(self):
		self.contenido = CalcContenido(self)
		self.Nodograficas = GraphCalcNodo(self)