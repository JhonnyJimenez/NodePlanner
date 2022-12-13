from PyQt5.QtCore import *
from examples.example_calculator.calc_config import *
from examples.example_calculator.calc_nodo_base import *
from nodeeditor.Utilidades import dump_exception

imagen = "iconos/owoAwoo.png"


class CalcNodoEntrada_Contenido(ContenidoDelNodo):
	def initui(self):
		self.edit = QLineEdit("1", self)
		self.edit.setAlignment(Qt.AlignRight)
		self.edit.setObjectName(self.nodo.content_label_objname)
	
	def serializacion(self):
		res = super().serializacion()
		res['Valor'] = self.edit.text()
		return res
	
	def deserializacion(self, data, hashmap={}):
		res = super().deserializacion(data, hashmap)
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
		self.evaluar()
	
	def initClasesInternas(self):
		self.contenido = CalcNodoEntrada_Contenido(self)
		self.Nodograficas = GraphCalcNodo(self)
		self.contenido.edit.textChanged.connect(self.DatosdeEntradaCambiados)