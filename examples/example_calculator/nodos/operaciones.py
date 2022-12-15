from PyQt5.QtCore import *
from examples.example_calculator.calc_config import *
from examples.example_calculator.calc_nodo_base import *
from nodeeditor.Utilidades import dump_exception

imagen = "iconos/owoAwoo.png"


@registrar_nodo(NODO_SUMA)
class CalcNodoSuma(CalcNodo):
	icono = imagen
	codigo_op = NODO_SUMA
	titulo_op = "Suma"
	content_label = "+"
	content_label_objname = "calc_nodo_bg"
	
	def realizarOperacion(self, entrada1, entrada2):
		return entrada1 + entrada2


@registrar_nodo(NODO_RESTA)
class CalcNodoResta(CalcNodo):
	icono = imagen
	codigo_op = NODO_RESTA
	titulo_op = "Resta"
	content_label = "-"
	content_label_objname = "calc_nodo_bg"
	
	def realizarOperacion(self, entrada1, entrada2):
		return entrada1 - entrada2


@registrar_nodo(NODO_MULTIPLICACION)
class CalcNodoMulplicacion(CalcNodo):
	icono = imagen
	codigo_op = NODO_MULTIPLICACION
	titulo_op = "Multiplicación"
	content_label = "*"
	content_label_objname = "calc_nodo_mul"
	
	def realizarOperacion(self, entrada1, entrada2):
		return entrada1 * entrada2


@registrar_nodo(NODO_DIVISION)
class CalcNodoDivision(CalcNodo):
	icono = imagen
	codigo_op = NODO_DIVISION
	titulo_op = "División"
	content_label = "/"
	content_label_objname = "calc_nodo_div"
	
	def realizarOperacion(self, entrada1, entrada2):
		if 0 in (entrada1, entrada2):
			if entrada1 == 0 and entrada2 == 0:
				return "ERROR"
			else:
				return entrada1 if entrada1 != 0 else entrada2
		else:
			return entrada1 / entrada2

# Forma de registro mediante el llamado de su función.
# registrar_nodo_ahora(NODO_SUMA, CalcNodo_Suma)