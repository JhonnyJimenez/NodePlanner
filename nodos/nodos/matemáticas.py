from nodos.categorías.entradas import *
from np_enlistado_de_nodos import *

imagen = "C:/Users/Maste/Downloads/icons/square foot.svg"


class Matemáticas_Graficador(Entradas_Graficador):
	def initSizes(self):
		super().initSizes()
		self.anchoNodo = 120
		self.altoNodo = 164
		self.altoNodoparaCalculos = self.altoNodo

		self.calculo_de_altura_disponible()


class Matemáticas_Contenido(Entradas_Contenido):
	def contenidos(self):

		self.etiqueta_1 = self.etiqueta("Resultado", "Derecha")
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
		self.objeto_2 = self.entrada_de_línea(1, "0.500", validante = QDoubleValidator())
		self.objeto_3 = self.entrada_de_línea(2, "0.500", validante = QDoubleValidator())
		self.objeto_4 = self.entrada_de_línea(3, "0.500", validante = QDoubleValidator())

	def lista_a_serializar(self, res):
		res['Objeto_1'] = self.objeto_1.currentText()
		res['Objeto_2'] = self.objeto_2.text()
		res['Objeto_3'] = self.objeto_3.text()
		res['Objeto_4'] = self.objeto_4.text()

	def lista_a_desearializar(self, data):
		self.objeto_1.setCurrentText(data['Objeto_1'])
		self.objeto_2.setText(data['Objeto_2'])
		self.objeto_3.setText(data['Objeto_3'])
		self.objeto_4.setText(data['Objeto_4'])

@registrar_nodo(NODO_MATEMÁTICO)
class Matemáticas(Entradas):
	icono = imagen
	codigo_op = NODO_MATEMÁTICO
	titulo_op = "Matemáticas"
	content_label_objname = "Matemáticas"

	ClaseGraficadeNodo = Matemáticas_Graficador
	ClasedelContenidodeNodo = Matemáticas_Contenido

	def __init__(self, escena, titulo = titulo_op, entradas = [2, 2, 2], salidas = [2]):
		super().__init__(escena, titulo, entradas, salidas)

	def actualizacion(self):
		self.contenido.objeto_1.currentTextChanged.connect(self.DatosdeEntradaCambiados)
		self.contenido.objeto_2.textChanged.connect(self.DatosdeEntradaCambiados)
		self.contenido.objeto_3.textChanged.connect(self.DatosdeEntradaCambiados)

	def ImplementarEvaluacion(self):
		operacion = self.contenido.objeto_1.currentText()

		self.oculto_por_metodo_2 = False
		self.oculto_por_metodo_3 = False

		if operacion in (
				"Raíz cuadrada", "Inverso de raíz cuadrada", "Absoluto", "Exponencial", "Signo",
				"Redondear", "Piso", "Techo", "Truncar", "Fracción", "Seno", "Coseno", "Tangente",
				"Arco seno", "Arco coseno", "Arco tangente", "Seno hiperbólico",
				"Coseno, hiperbólico", "Tangente hiperbólica", "A radianes", "A grados"
				):
			self.ocultar_entrada_3()
			self.ocultar_entrada_2()
		elif operacion in ("Multiplicar y adicionar", "Comparar", "Mínimo suave", "Máximo suave", "Ciclo"):
			self.mostrar_entrada_2()
			self.mostrar_entrada_3()
		else:
			self.ocultar_entrada_3()
			self.mostrar_entrada_2()

		entrada_1 = self.obtenerContrazocalo(0)
		entrada_2 = self.obtenerContrazocalo(1)
		entrada_3 = self.obtenerContrazocalo(2)

		if entrada_1 is not None:
			self.contenido.objeto_2.setVisible(False)
			valor_1 = entrada_1.nodo.valores[entrada_1.indice]
		else:
			self.contenido.objeto_2.setVisible(True)
			valor_1 = self.contenido.objeto_2.text()

		if not self.oculto_por_metodo_2:
			if entrada_2 is not None:
				self.contenido.objeto_3.setVisible(False)
				valor_2 = entrada_2.nodo.valores[entrada_2.indice]
			else:
				self.contenido.objeto_3.setVisible(True)
				valor_2 = self.contenido.objeto_3.text()
		else:
			valor_2 = 0.5

		if not self.oculto_por_metodo_3:
			if entrada_3 is not None:
				self.contenido.objeto_4.setVisible(False)
				valor_3 = entrada_3.nodo.valores[entrada_3.indice]
			else:
				self.contenido.objeto_4.setVisible(True)
				valor_3 = self.contenido.objeto_4.text()
		else:
			valor_3 = 0.5

		if self.oculto_por_metodo_2 and self.oculto_por_metodo_3:
			self.Nodograficas.altoNodo = 114
		elif self.oculto_por_metodo_3:
			self.Nodograficas.altoNodo = 139
		else:
			self.Nodograficas.altoNodo = 164

		self.definir_entradas(operacion, valor_1, valor_2, valor_3)

		valor_1 = self.valores_entrantes[0]
		valor_2 = self.valores_entrantes[1]
		valor_3 = self.valores_entrantes[2]

		if (type(valor_1) is str and type(valor_2) is not str) or (type(valor_1) is not str and type(valor_2) is str):
			resultado = 0
		else:
			resultado = self.operaciones_matemáticas(operacion, valor_1, valor_2, valor_3)

		self.valores[0] = resultado

		self.marcarIndefinido(False)
		self.marcarInvalido(False)
		self.Nodograficas.setToolTip("")
		self.evaluarHijos()

		return self.valores[0]

	def operaciones_matemáticas(self, seleccionador, valor_1, valor_2, valor_3 = 0.5):
		if seleccionador == "Adicionar":
			resultado = valor_1 + valor_2
			if type(resultado) is not str:
				resultado = self.limpieza(resultado)

		elif seleccionador == "Sustraer":
			resultado = valor_1 - valor_2
			resultado = self.limpieza(resultado)

		elif seleccionador == "Multiplicar":
			resultado = valor_1 * valor_2
			resultado = self.limpieza(resultado)

		elif seleccionador == "Dividir":
			try:
				resultado_base = valor_1 / valor_2
			except ZeroDivisionError:
				resultado_base = valor_1
			resultado = self.limpieza(resultado_base)

		elif seleccionador == "Multiplicar y adicionar":
			resultado = (valor_1 * valor_2) + valor_3
			resultado = self.limpieza(resultado)

		elif seleccionador == "Potencia":
			resultado = pow(valor_1, valor_2)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Logaritmo":
			resultado = math.log(valor_1, valor_2)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Raíz cuadrada":
			resultado = math.sqrt(valor_1)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Inverso de raíz cuadrada":
			resultado = 1 / math.sqrt(valor_1)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Absoluto":
			resultado = abs(valor_1)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Exponencial":
			resultado = math.exp(valor_1)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Mínimo":
			resultado = min(valor_1, valor_2)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Máximo":
			resultado = max(valor_1, valor_2)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Menor que":
			if valor_1 < valor_2:
				resultado = 1
			else:
				resultado = 0
			resultado = self.limpieza(resultado)

		elif seleccionador == "Mayor que":
			if valor_1 > valor_2:
				resultado = 1
			else:
				resultado = 0
			resultado = self.limpieza(resultado)

		elif seleccionador == "Signo":
			if valor_1 > 0:
				resultado = 1
			elif valor_1 == 0:
				resultado = 0
			else:
				resultado = -1
			resultado = self.limpieza(resultado)

		elif seleccionador == "Comparar":
			min = (valor_2 - valor_3)
			max = (valor_2 + valor_3)
			if valor_1 >= min and valor_1 <= max:
				resultado = 1
			else:
				resultado = 0
			resultado = self.limpieza(resultado)

		elif seleccionador == "Mínimo suave":
			resultado = "Aún no implementado."

		elif seleccionador == "Máximo suave":
			resultado = "Aún no implementado."

		elif seleccionador == "Redondear":
			decimales, entero = math.modf(valor_1)
			if decimales >= 0.5:
				resultado = int(valor_1) + 1
			else:
				resultado = int(valor_1)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Piso":
			resultado = int(valor_1) + 1
			resultado = self.limpieza(resultado)

		elif seleccionador == "Techo":
			resultado = int(valor_1)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Truncar":
			decimales, resultado = math.modf(valor_1)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Fracción":
			resultado, entero = math.modf(valor_1)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Resto":
			resultado = valor_1 % valor_2
			resultado = self.limpieza(resultado)

		elif seleccionador == "Ciclo":
			resultado = "Aún no implementado."

		elif seleccionador == "Adherir":
			resultado = "Aún no implementado."

		elif seleccionador == "Ping pong":
			resultado = "Aún no implementado."

		elif seleccionador == "Seno":
			resultado = math.sin(valor_1)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Coseno":
			resultado = math.cos(valor_1)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Tangente":
			resultado = math.tan(valor_1)
			resultado = self.limpieza(resultado)

		elif seleccionador == "Arco seno":
			resultado = numpy.arcsin(valor_1)

		elif seleccionador == "Arco coseno":
			resultado = numpy.arccos(valor_1)

		elif seleccionador == "Arco tangente":
			resultado = numpy.arctan(valor_1)

		elif seleccionador == "Arco tangente 2":
			resultado = numpy.arctan2(valor_1, valor_2)

		elif seleccionador == "Seno hiperbólico":
			resultado = numpy.sinh(valor_1)

		elif seleccionador == "Coseno hiperbólico":
			resultado = numpy.cosh(valor_1)

		elif seleccionador == "Tangente hiperbólica":
			resultado = numpy.tanh(valor_1)

		elif seleccionador == "A radianes":
			resultado = math.radians(valor_1)

		elif seleccionador == "A grados":
			resultado = math.degrees(valor_1)

		else:
			resultado = "¿Cómo sacaste esta opción?"

		return resultado

	def definir_entradas(self, operacion, *args):
		valor_por_defecto = 0.5
		nuevos_valores = []
		contador = -1
		for valor in args:
			contador += 1
			if valor is None:
				valor = valor_por_defecto
				print("Indice %s: Valor por defecto" % contador)
			else:
				try:
					if valor in ('-', '.', ''):
						valor = 0
					else:
						valor = float(valor)
				except:
					if operacion == 'Adicionar' and type(valor) == str:
						pass
					else:
						valor = valor_por_defecto
						print("Indice %s: Error" % contador)
			nuevos_valores.append(valor)
		self.valores_entrantes = nuevos_valores
		return self.valores_entrantes

	def limpieza(self, resultado: float):
		decimales, entero = math.modf(resultado)
		if decimales == 0.0:
			resultado = int(resultado)
			return resultado

		cantidad_digitos = len(str(resultado))
		punto = str(resultado).find(".") + 1
		decimales = cantidad_digitos - punto

		resultado = (round(resultado, decimales))
		return resultado

	def ocultar_entrada_3(self):
		self.entradas[2].quitar_todas_las_conexiones(True)
		self.contenido.objeto_4.setVisible(False)
		self.entradas[2].GraficosZocalos.setVisible(False)
		self.oculto_por_metodo_3 = True

	def mostrar_entrada_3(self):
		self.entradas[2].GraficosZocalos.setVisible(True)
		self.contenido.objeto_4.setVisible(True)
		self.oculto_por_metodo_3 = False

	def ocultar_entrada_2(self):
		self.entradas[1].quitar_todas_las_conexiones(True)
		self.entradas[1].GraficosZocalos.setVisible(False)
		self.contenido.objeto_3.setVisible(False)
		self.oculto_por_metodo_2 = True

	def mostrar_entrada_2(self):
		self.entradas[1].GraficosZocalos.setVisible(True)
		self.contenido.objeto_3.setVisible(True)
		self.oculto_por_metodo_2 = False