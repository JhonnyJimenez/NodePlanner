import math
from PyQt5.QtCore import *
from examples.example_calculator.calc_config import *
from examples.example_calculator.calc_nodo_base import *
from nodeeditor.Utilidades import dump_exception

imagen = "iconos/owoAwoo.png"


class CalcNodoSalida_Contenido(ContenidoDelNodo):
	def initui(self):
		self.lbl = QLabel("42", self)
		self.lbl.setAlignment(Qt.AlignLeft)
		self.lbl.setObjectName(self.nodo.content_label_objname)


@registrar_nodo(NODO_SALIDA)
class CalcNodoSalida(CalcNodo):
	icono = imagen
	codigo_op = NODO_SALIDA
	titulo_op = "Salida"
	content_label_objname = "calc_nodo_salida"
	
	def __init__(self, escena):
		super().__init__(escena, entradas=[1], salidas=[])
	
	def initClasesInternas(self):
		self.contenido = CalcNodoSalida_Contenido(self)
		self.Nodograficas = GraphCalcNodo(self)
		
	def ImplementacionEvaluacion(self):
		nodo_de_entrada = self.obtenerEntrada(0)
		if not nodo_de_entrada:
			self.Nodograficas.setToolTip("No hay un nodo conectado.")
			self.marcarInvalido()
			return
		
		val = nodo_de_entrada.evaluar()
		
		if val is None:
			self.Nodograficas.setToolTip("Los datos en la entrada no son un número.")
			self.marcarInvalido()
			return
		
		if val == "ERROR":
			self.contenido.lbl.setText(val)
			return
		
		decimal, entero = math.modf(val)
		self.contenido.lbl.setText("%s" % (int(val) if decimal == 0.0 else round(val, 3)))
		self.marcarInvalido(False)
		self.marcarIndefinido(False)
		self.Nodograficas.setToolTip("")
		
		return val