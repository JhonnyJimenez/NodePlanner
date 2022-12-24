from nodos.categorías.entradas import *
from np_enlistado_de_nodos import *

imagen = "C:/Users/Maste/Downloads/icons/square foot.svg"


class Matemáticas_Graficador(Entradas_Graficador):
	def initSizes(self):
		super().initSizes()
		self.anchoNodo = 120
		self.altoNodo = 64

		self.calculo_de_altura_disponible()


class Matemáticas_Contenido(Entradas_Contenido):
	def contenidos(self):
		operaciones = [
				"Adicionar", "Sustraer", "Multiplicar", "Dividir", "Multiplicar y adicionar",
				"Potencia", "Logaritmo", "Raíz cuadrada", "Inverso de raíz cuadrada", "Absoluto",
				"Exponencial", "Mínimo", "Máximo", "Menor que", "Mayor que", "Signo", "Comparar",
				"Mínimo suave", "Máximo suave", "Redondear", "Piso", "Techo", "Truncar", "Fracción",
				"Resto", "Ciclo", "Adherir", "Ping, pong", "Seno", "Coseno", "Tangente", "Arco seno",
				"Arco coseno", "Arco tangente", "Arco tangente 2", "Seno hiperbólico",
				"Coseno, hiperbólico", "Tangente hiperbólica", "A radianes", "A grados"
				]
		self.objeto_1 = self.lista_desplegable(elementos_visibles = 8, listado = operaciones)
		self.objeto_2 = self.entrada_de_línea(1, 0.500, validante = QDoubleValidator())
		self.objeto_3 = self.entrada_de_línea(1, 0.500, validante = QDoubleValidator())

	def lista_a_serializar(self, res):
		res['Objeto_1'] = self.objeto_1.currentText()
		res['Objeto_2'] = self.objeto_2.text()
		res['Objeto_3'] = self.objeto_3.text()

	def lista_a_desearializar(self, data):
		self.objeto_1.setCurrentText(data['Objeto_1'])
		self.objeto_2.setText(data['Objeto_2'])
		self.objeto_3.setText(data['Objeto_3'])

@registrar_nodo(NODO_MATEMÁTICO)
class Matemáticas(Entradas):
	icono = imagen
	codigo_op = NODO_MATEMÁTICO
	titulo_op = "Operación"
	content_label_objname = "Operaciones"

	ClaseGraficadeNodo = Matemáticas_Graficador
	ClasedelContenidodeNodo = Matemáticas_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [], salidas = []):
		super().__init__(escena, titulo, entradas, salidas)

	def actualizacion(self):
		self.contenido.objeto_1.currentTextChanged.connect(self.DatosdeEntradaCambiados)

	def DatosdeEntradaCambiados(self, zocalo = None):
		super().DatosdeEntradaCambiados(zocalo)
		print(self.contenido.objeto_1.currentText())

	def ImplementarEvaluacion(self):
		pass