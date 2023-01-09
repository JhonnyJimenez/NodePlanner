import math
import numpy
from PyQt5.QtCore import Qt

NODOS_NO_DISPONIBLES = [0, 1, 6]


def tratado_de_datos(dato_a_tratar, especificación: bool = False):

	if dato_a_tratar is None:
		pass

	elif type(dato_a_tratar) is int:
		dato_a_tratar = "{:,}".format(dato_a_tratar)
		dato_a_tratar = dato_a_tratar.replace(",", " ")
		if especificación:
			dato_a_tratar += ' (Entero)'

	elif type(dato_a_tratar) is float:
		dato_a_tratar = "{:,}".format(dato_a_tratar)
		dato_a_tratar = dato_a_tratar.replace(",", " ")
		if especificación:
			dato_a_tratar += ' (Decimal)'

	elif type(dato_a_tratar) is str:
		if dato_a_tratar != '':
			if especificación:
				dato_a_tratar += ' (Cadena)'
		else:
			dato_a_tratar = 'Cadena vacía.'

	elif type(dato_a_tratar) is Qt.CheckState:
		if dato_a_tratar == 0:
			dato_a_tratar = 'Falso'
		if dato_a_tratar == 1:
			dato_a_tratar = 'Indeterminado'
		if dato_a_tratar == 2:
			dato_a_tratar = 'Verdadero'
		if especificación:
			dato_a_tratar += ' (Booleana)'

	else:
		dato_a_tratar = 'El tipo de datos %s no ha sido tratado.' % str(type(dato_a_tratar).__name__)

	dato_tratado = dato_a_tratar

	return dato_tratado

def conversor_númerico(cadena):
	try:
		valor_a_tratar = cadena.replace(" ", "")
		valor = float(valor_a_tratar)
		decimales, entero = math.modf(valor)

		if decimales == 0.0:
			return int(valor)
		else:
			return valor
	except ValueError:
		return 0

def alineador(objeto, alineamiento):
	if alineamiento in (1, 'Izquierda'):
		objeto.setAlignment(Qt.AlignLeft)
	elif alineamiento in (2, 'Centro'):
		objeto.setAlignment(Qt.AlignCenter)
	elif alineamiento in (3, 'Derecha'):
		objeto.setAlignment(Qt.AlignRight)

def nodos_no_disponibles(keys, lista):
	for codigo in lista:
		keys.remove(codigo)

def operaciones_matemáticas(operación, x, y, z):
	resultado = 0

	try:
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
	except TypeError:
		if operación == "Adicionar":
			if type(x) is str and type(y) in (int, float):
				resultado = y
			elif type(y) is str and type(x) in (int, float):
				resultado = x
		elif operación == "Multiplicar":
			if type(x) and type(y) is str:
				resultado = 0
			elif type(x) is str and type(y) is float:
				resultado = x * int(y)
			elif type(y) is str and type(x) is float:
				resultado = int(x) * y
		elif operación == "Multiplicar y adicionar":
			if type(z) is str:
				if type(x) in (int, float) and type(y) in (int, float):
					resultado = x * y
				elif type(x) and type(y) is str:
					resultado = z
				elif type(x) is str and type(y) in (int, float):
					resultado = (x * int(y)) + z
				elif type(y) is str and type(x) in (int, float):
					resultado = (int(x) * y) + z

			elif type(z) in (int, float):
				if type(x) is str and type(y) in (int, float):
					resultado = x * int(y)
				elif type(y) is str and type(x) in (int, float):
					resultado = int(x) * y
		else:
			resultado = 0

	if type(resultado) is float:
		decimales, entero = math.modf(resultado)

		if decimales == 0.0:
			resultado = int(entero)

	return resultado