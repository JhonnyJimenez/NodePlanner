from PyQt5.QtWidgets import *

from np_nodo_base import *

imagen = "C:/Users/Maste/Downloads/icons/square foot.svg"

class Operaciones_Graficador(NodoBase_Graficador):
	def initSizes(self):
		super().initSizes()
		self.anchoNodo = 120
		self.altoNodo = 54
		self.calculo_de_altura_disponible()

	def initAssets(self):
		super().initAssets()
		self._relleno_titulo_nodo = QBrush(QColor("#FF246283"))


class Operaciones_Contenido(NodoBase_Contenido):
	def initui(self):
		super().initui()
		self.objetos()

	def objetos(self):
		opciones = [
				"Adicionar", "Sustraer", "Multiplicar", "Dividir", "Multiplicar y adicionar",
				"Potencia", "Logaritmo", "Raíz cuadrada", "Inverso de raíz cuadrada", "Absoluto",
				"Exponencial", "Mínimo", "Máximo", "Menor que", "Mayor que", "Signo", "Comparar",
				"Mínimo suave", "Máximo suave", "Redondear", "Piso", "Techo", "Truncar", "Fracción",
				"Resto", "Ciclo", "Adherir", "Ping, pong", "Seno", "Coseno", "Tangente", "Arco seno",
				"Arco coseno", "Arco tangente", "Arco tangente 2", "Seno hiperbólico",
				"Coseno, hiperbólico", "Tangente hiperbólica", "A radianes", "A grados"
				]
		self.lista_despegable = self.despegable(opciones)

	def despegable(self, lista: list = []):
		objeto = QComboBox(self)
		objeto.setGeometry(5, 5, self.anchoNodo - 14, 20)
		objeto.addItems(lista)
		objeto.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLength)
		objeto.setMaxVisibleItems(6)
		return objeto

@registrar_nodo(CATEGORIA_OPERACIONES)
class Operaciones(NodoBase):
	icono = imagen
	codigo_op = CATEGORIA_OPERACIONES
	titulo_op = "Operación"
	content_label_objname = "Operaciones"

	ClaseGraficadeNodo = Operaciones_Graficador
	ClasedelContenidodeNodo = Operaciones_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [], salidas = []):
		super().__init__(escena, titulo, entradas, salidas)
		self.contenido.lista_despegable.currentTextChanged.connect(self.DatosdeEntradaCambiados)

	def DatosdeEntradaCambiados(self, zocalo = None):
		super().DatosdeEntradaCambiados(zocalo)
		print(self.contenido.lista_despegable.currentText())