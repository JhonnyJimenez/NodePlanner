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