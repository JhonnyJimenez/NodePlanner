from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
from lib.examples.example_calculator.calc_config import *
from lib.examples.example_calculator.calc_nodo_base import CalcNodo, GraphCalcNodo, ContenidoDelNodo
from lib.nodeeditor.Utilidades import dump_exception

imagen = "iconos/owoAwoo.png"


class CalcNodoEntradaContenido(ContenidoDelNodo):
	def init_ui(self):
		self.edit = QLineEdit("1", self)
		self.edit.setAlignment(Qt.AlignRight)
		self.edit.setObjectName(self.nodo.content_label_objname)
	
	def serialización(self):
		res = super().serialización()
		res['Valor'] = self.edit.text()
		return res
	
	def deserialización(self, data, hashmap={}):
		res = super().deserialización(data, hashmap)
		try:
			valor = data['Valor']
			self.edit.setText(valor)
			return True
		except Exception as e:
			dump_exception(e)
		return res


@registrar_nodo(NODO_ENTRADA)
class CalcNodoEntrada(CalcNodo):
	icono = imagen
	codigo_op = NODO_ENTRADA
	titulo_op = "Entrada"
	content_label_objname = "calc_nodo_entrada"
	
	def __init__(self, escena):
		super().__init__(escena, entradas=[], salidas=[3])
		self.evaluación()
	
	def init_clases_internas(self):
		self.contenido = CalcNodoEntradaContenido(self)
		self.Nodograficas = GraphCalcNodo(self)
		self.contenido.edit.textChanged.connect(self.datos_de_entrada_cambiados)
		
	def implementar_evaluación(self):
		valor_ingresado = self.contenido.edit.text()
		valor_seguro = float(valor_ingresado)
		self.valor = valor_seguro
		self.marcar_indefinido(False)
		self.marcar_inválido(False)
		
		self.marcar_descendencia_inválido(False)
		self.marcar_descendencia_indefinido()
		
		self.Nodograficas.setToolTip("")
		
		self.evaluar_hijos()
		
		return self.valor