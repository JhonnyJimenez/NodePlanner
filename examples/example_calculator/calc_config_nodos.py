from PyQt5.QtCore import *
from examples.example_calculator.calc_config import *
from examples.example_calculator.calc_nodo_base import *


imagen = "iconos/owoAwoo.png"

class CalcNodoEntrada_Contenido(ContenidoDelNodo):
	def initui(self):
		self.edit = QLineEdit("1", self)
		self.edit.setAlignment(Qt.AlignRight)
		self.edit.setObjectName(self.nodo.content_label_objname)

@registrar_nodo(NODO_ENTRADA)
class CalcNodoEntrada(CalcNodo):
	icono = imagen
	codigo_op = NODO_ENTRADA
	titulo_op = "Entrada"
	content_label_objname = "calc_nodo_entrada"
	
	def __init__(self, escena):
		super().__init__(escena, entradas=[], salidas=[3])
		
	def initClasesInternas(self):
		self.contenido = CalcNodoEntrada_Contenido(self)
		self.Nodograficas = GraphCalcNodo(self)
		
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

@registrar_nodo(NODO_SUMA)
class CalcNodoSuma(CalcNodo):
	icono = imagen
	codigo_op = NODO_SUMA
	titulo_op = "Suma"
	content_label = "+"
	content_label_objname = "calc_nodo_bg"

@registrar_nodo(NODO_RESTA)
class CalcNodoResta(CalcNodo):
	icono = imagen
	codigo_op = NODO_RESTA
	titulo_op = "Resta"
	content_label = "-"
	content_label_objname = "calc_nodo_bg"

@registrar_nodo(NODO_MULTIPLICACION)
class CalcNodoMulplicacion(CalcNodo):
	icono = imagen
	codigo_op = NODO_MULTIPLICACION
	titulo_op = "Multiplicación"
	content_label = "*"
	content_label_objname = "calc_nodo_mul"

@registrar_nodo(NODO_DIVISION)
class CalcNodoDivision(CalcNodo):
	icono = imagen
	codigo_op = NODO_DIVISION
	titulo_op = "División"
	content_label = "/"
	content_label_objname = "calc_nodo_div"
	
# Forma de registro mediante el llamado de su función.
# registrar_nodo_ahora(NODO_SUMA, CalcNodo_Suma)
