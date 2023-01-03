import math
import numpy
from nodos.categorías.entradas import *
from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_desplegable import Desplegable

imagen = "C:/Users/Maste/Downloads/icons/square foot.svg"


class ContenidodelNodoMatemático(ContenidodelosNodosdeEntrada):
	def controles(self):
		super().controles()
		self.placeholder(5)

	def contenido(self):
		self.objeto_0 = Etiqueta(
				self, índice = 0, zócalo_de_salida = 0, texto_inicial = 'Resultado', alineado = 'Derecha'
				)
		operaciones = [
				"Adicionar", "Sustraer", "Multiplicar", "Dividir", "Multiplicar y adicionar",
				"Potencia", "Logaritmo", "Raíz cuadrada", "Inverso de raíz cuadrada", "Absoluto",
				"Exponencial", "Mínimo", "Máximo", "Menor que", "Mayor que", "Signo", "Comparar",
				"Mínimo suave", "Máximo suave", "Redondear", "Piso", "Techo", "Truncar", "Fracción",
				"Resto", "Ciclo", "Adherir", "Ping, pong", "Seno", "Coseno", "Tangente", "Arco seno",
				"Arco coseno", "Arco tangente", "Arco tangente 2", "Seno hiperbólico",
				"Coseno, hiperbólico", "Tangente hiperbólica", "A radianes", "A grados"
				]
		self.objeto_1 = Desplegable(self, índice = 1, lista = operaciones, valor_inicial = 8)
		self.objeto_2 = Entrada(
				self, índice = 2, zócalo_de_entrada = 0, texto_inicial = '0.5', validante = VALIDANTE_NUMÉRICO
				)
		self.objeto_3 = Entrada(
				self, índice = 3, zócalo_de_entrada = 1, texto_inicial = '0.5', validante = VALIDANTE_NUMÉRICO
				)
		self.objeto_4 = Entrada(
				self, índice = 4, zócalo_de_entrada = 2, texto_inicial = '0.5', validante = VALIDANTE_NUMÉRICO
				)


@registrar_nodo(NODO_MATEMÁTICO)
class NodoMatemático(NodosdeEntrada):
	icono = imagen
	codigo_op = NODO_MATEMÁTICO
	titulo_op = "Matemáticas"

	ClasedelContenidodeNodo = ContenidodelNodoMatemático

	Entradas = [1, 1, 1]
	Salidas = [1]

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		self.control1 = True
		self.control2 = True
		self.control3 = False
		super().__init__(escena, titulo, entradas, salidas)

	def métodos_de_evaluación(self):
		operación = self.valores_internos[1]

		if operación in (
							"Raíz cuadrada", "Inverso de raíz cuadrada", "Absoluto", "Exponencial", "Signo",
							"Redondear", "Piso", "Techo", "Truncar", "Fracción", "Seno", "Coseno", "Tangente",
							"Arco seno", "Arco coseno", "Arco tangente", "Seno hiperbólico",
							"Coseno, hiperbólico", "Tangente hiperbólica", "A radianes", "A grados"
							):
			self.contenido.objeto_3.autoocultarse()
			self.contenido.objeto_4.autoocultarse()
			self.Nodograficas.altura_del_nodo = (
					self.Nodograficas.altura_del_título + (2 * self.Nodograficas.márgen) + self.contenido.objeto_2.alto
					+ self.contenido.objeto_2.posición_y
			)

		elif operación in ("Multiplicar y adicionar", "Comparar", "Mínimo suave", "Máximo suave", "Ciclo"):
			for elemento in (self.contenido.objeto_3, self.contenido.objeto_4):
				if not self.entradas[elemento.zócalo_de_entrada].Zocaloconexiones:
					elemento.automostrarse()
			self.Nodograficas.altura_del_nodo = (
					self.Nodograficas.altura_del_título + (2 * self.Nodograficas.márgen) + self.contenido.objeto_4.alto
					+ self.contenido.objeto_4.posición_y
			)

		else:
			self.contenido.objeto_4.autoocultarse()
			if not self.entradas[self.contenido.objeto_3.zócalo_de_entrada].Zocaloconexiones:
				self.contenido.objeto_3.automostrarse()
			self.Nodograficas.altura_del_nodo = (
					self.Nodograficas.altura_del_título + (2 * self.Nodograficas.márgen) + self.contenido.objeto_3.alto
					+ self.contenido.objeto_3.posición_y
			)
			
		self.valores_a_evaluar = [0.5, 0.5, 0.5]

		if self.valores_de_entrada[0] is None:
			self.valores_a_evaluar[0] = self.valores_internos[2]
		else:
			self.valores_a_evaluar[0] = self.valores_de_entrada[0]

		if self.valores_de_entrada[1] is None:
			self.valores_a_evaluar[1] = self.valores_internos[3]
		else:
			self.valores_a_evaluar[1] = self.valores_de_entrada[1]

		if self.valores_de_entrada[2] is None:
			self.valores_a_evaluar[2] = self.valores_internos[4]
		else:
			self.valores_a_evaluar[2] = self.valores_de_entrada[2]

		self.valores_de_salida[0] = self.operaciones_matemáticas(operación, *self.valores_a_evaluar)

		return self.valores_de_salida

	def operaciones_matemáticas(self, operación, x, y, z):
		if operación == "Adicionar":
			resultado = x + y

		elif operación == "Sustraer":
			resultado = x - y

		elif operación == "Multiplicar":
			resultado = x * y

		elif operación == "Dividir":
			try:
				resultado = x / y
			except ZeroDivisionError:
				resultado = x

		elif operación == "Multiplicar y adicionar":
			resultado = (x * y) + z

		elif operación == "Potencia":
			resultado = pow(x, y)

		elif operación == "Logaritmo":
			resultado = math.log(x, y)

		elif operación == "Raíz cuadrada":
			resultado = math.sqrt(x)

		elif operación == "Inverso de raíz cuadrada":
			resultado = 1 / math.sqrt(x)

		elif operación == "Absoluto":
			resultado = abs(x)

		elif operación == "Exponencial":
			resultado = math.exp(x)

		elif operación == "Mínimo":
			resultado = min(x, y)

		elif operación == "Máximo":
			resultado = max(x, y)

		elif operación == "Menor que":
			if x < y:
				resultado = 1
			else:
				resultado = 0

		elif operación == "Mayor que":
			if x > y:
				resultado = 1
			else:
				resultado = 0

		elif operación == "Signo":
			if x > 0:
				resultado = 1
			elif x == 0:
				resultado = 0
			else:
				resultado = -1

		elif operación == "Comparar":
			mínimo = (y - z)
			máximo = (y + z)
			if mínimo <= x <= máximo:
				resultado = 1
			else:
				resultado = 0

		elif operación == "Mínimo suave":
			resultado = "Aún no implementado."

		elif operación == "Máximo suave":
			resultado = "Aún no implementado."

		elif operación == "Redondear":
			decimales, entero = math.modf(x)
			if decimales >= 0.5:
				resultado = int(x) + 1
			else:
				resultado = int(x)

		elif operación == "Piso":
			resultado = int(x) + 1

		elif operación == "Techo":
			resultado = int(x)

		elif operación == "Truncar":
			decimales, resultado = math.modf(x)

		elif operación == "Fracción":
			resultado, entero = math.modf(x)

		elif operación == "Resto":
			resultado = x % y

		elif operación == "Ciclo":
			resultado = "Aún no implementado."

		elif operación == "Adherir":
			resultado = "Aún no implementado."

		elif operación == "Ping pong":
			resultado = "Aún no implementado."

		elif operación == "Seno":
			resultado = math.sin(x)

		elif operación == "Coseno":
			resultado = math.cos(x)

		elif operación == "Tangente":
			resultado = math.tan(x)

		elif operación == "Arco seno":
			resultado = numpy.arcsin(x)

		elif operación == "Arco coseno":
			resultado = numpy.arccos(x)

		elif operación == "Arco tangente":
			resultado = numpy.arctan(x)

		elif operación == "Arco tangente 2":
			resultado = numpy.arctan2(x, y)

		elif operación == "Seno hiperbólico":
			resultado = numpy.sinh(x)

		elif operación == "Coseno hiperbólico":
			resultado = numpy.cosh(x)

		elif operación == "Tangente hiperbólica":
			resultado = numpy.tanh(x)

		elif operación == "A radianes":
			resultado = math.radians(x)

		elif operación == "A grados":
			resultado = math.degrees(x)

		else:
			resultado = "¿Cómo sacaste esta opción?"


		if type(resultado) is float:
			decimales, entero = math.modf(resultado)

			if decimales == 0.0:
				resultado = int(entero)

		return resultado