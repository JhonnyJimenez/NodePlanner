import math
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from lib.examples.example_calculator.calc_config import *
from lib.examples.example_calculator.calc_nodo_base import CalcNodo, GraphCalcNodo, ContenidoDelNodo

imagen = "iconos/owoAwoo.png"


class CalcNodoSalidaContenido(ContenidoDelNodo):
	def init_ui(self):
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
	
	def init_clases_internas(self):
		self.contenido = CalcNodoSalidaContenido(self)
		self.Nodograficas = GraphCalcNodo(self)
		
	def implementar_evaluación(self):
		nodo_de_entrada = self.obtener_entrada(0)
		if not nodo_de_entrada:
			self.Nodograficas.setToolTip("No hay un nodo conectado.")
			self.marcar_inválido()
			return
		
		val = nodo_de_entrada.evaluación()
		
		if val is None:
			self.Nodograficas.setToolTip("Los datos en la entrada no son un número.")
			self.marcar_inválido()
			return
		
		if val == "ERROR":
			self.contenido.lbl.setText(val)
			return
		
		decimal, entero = math.modf(val)
		self.contenido.lbl.setText("%s" % (int(val) if decimal == 0.0 else round(val, 3)))
		self.marcar_inválido(False)
		self.marcar_indefinido(False)
		self.Nodograficas.setToolTip("")
		
		return val