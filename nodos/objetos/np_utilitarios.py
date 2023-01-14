import math
import numpy
import mpmath
from PyQt5.QtCore import Qt

NODOS_NO_DISPONIBLES = [0, 1, 6, 8]


def tratado_de_datos(dato_a_tratar, especificación: bool = False):

	if dato_a_tratar is None:
		pass

	elif type(dato_a_tratar) in (int, float):
		decimales, entero = math.modf(dato_a_tratar)

		if dato_a_tratar > 99999999999 or len(str(decimales)) > 6:
			dato_a_tratar = format(dato_a_tratar, '.10e')
			if especificación:
				dato_a_tratar += ' (Científico de Python)'

		elif type(dato_a_tratar) is int:
			dato_a_tratar = "{:,}".format(dato_a_tratar)
			dato_a_tratar = dato_a_tratar.replace(",", " ")
			if especificación:
				dato_a_tratar += ' (Entero de Python)'

		elif type(dato_a_tratar) is float:
			dato_a_tratar = "{:,}".format(dato_a_tratar)
			dato_a_tratar = dato_a_tratar.replace(",", " ")
			if especificación:
				dato_a_tratar += ' (Float de Python)'

	elif type(dato_a_tratar) is str:
		if dato_a_tratar != '':
			if especificación:
				dato_a_tratar += ' (Cadena)'
		else:
			dato_a_tratar = 'Cadena vacía.'

	elif type(dato_a_tratar) is bool:
		if dato_a_tratar is True:
			dato_a_tratar = 'Verdadero'
		else:
			dato_a_tratar = 'Falso'
		if especificación:
			dato_a_tratar += ' (Booleana de Python)'

	elif type(dato_a_tratar) is mpmath.mpf:
		decimales = mpmath.frac(dato_a_tratar)
		dato_a_tratar = mpmath.nstr(dato_a_tratar, n = 12)

		# Si es número científico:
		if dato_a_tratar.find("e") != -1:
			dato_1, dato_2 = dato_a_tratar.split('e')
			decimal_c = mpmath.frac(dato_1)
			if decimal_c == mpmath.mpf('0'):
				dato_1 = dato_1[0:-2]
			dato_a_tratar = dato_1 + 'e' + dato_2
			if especificación:
				dato_a_tratar += ' (Científico de mpmath)'

		elif decimales == mpmath.mpf('0'):
			dato_a_tratar = formato_para_enteros(dato_a_tratar)
			if especificación:
				dato_a_tratar += ' (Entero de mpmath)'

		else:
			dato_1, dato_2 = dato_a_tratar.split('.')
			dato_1 = formato_para_enteros(dato_1, False)
			dato_a_tratar = dato_1 + '.' + dato_2
			if especificación:
				dato_a_tratar += ' (Decimal de mpmath)'

	elif type(dato_a_tratar) is Qt.CheckState:
		if dato_a_tratar == 0:
			dato_a_tratar = 'Falso'
		if dato_a_tratar == 1:
			dato_a_tratar = 'Indeterminado'
		if dato_a_tratar == 2:
			dato_a_tratar = 'Verdadero'
		if especificación:
			dato_a_tratar += ' (Booleana de Qt)'

	else:
		dato_a_tratar = 'El tipo de datos %s no ha sido tratado.' % str(type(dato_a_tratar).__name__)

	dato_tratado = dato_a_tratar

	return dato_tratado

def conversor_númerico_python(cadena):
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

def conversor_númerico_mpmath(cadena):
	try:
		valor_a_tratar = cadena.replace(" ", "")
		valor = mpmath.mpf(valor_a_tratar)
		return valor
	except ValueError:
		return 0

def formato_para_enteros(cadena, recorte_para_mpmath = True):
	if recorte_para_mpmath:
		# Elimina la parte decimal previamente comprobada como 0.0
		cadena = cadena[0:-2]
	# Invierte el orden de la cadena.
	cadena = cadena[::-1]

	dato_nuevo = []
	for letra in cadena:
		dato_nuevo.append(letra)

	# Añade el espacio donde corresponde.
	contador = 0
	for letra in dato_nuevo:
		if contador % 3 == 2:
			dato_nuevo[contador] = letra + ' '
		contador += 1

	# Remueve el espacio inicial en caso el número tenga una cantidad de dígitos múltiplo de 3.
	if len(dato_nuevo) % 3 == 0:
		dato_nuevo[-1] = dato_nuevo[-1][0]

	# Crea la cadena nueva
	cadena = "".join(dato_nuevo)

	# Invierte la cadena nuevamente para restaurarla.
	cadena = cadena[::-1]
	return cadena

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

def matemáticas_nativas(operación, x, y, z, *args):
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

def matemáticas_con_mpmath(operación, *args):
	x = args[0]
	y = args[1]
	z = args[2]

	resultado = mpmath.mpf('0')

	with mpmath.workdps(100):
		try:
			if operación == "Adicionar":
				resultado = mpmath.fadd(x, y)

			elif operación == "Sustraer":
				resultado = mpmath.fsub(x, y)

			elif operación == "Multiplicar":
				resultado = mpmath.fmul(x, y)

			elif operación == "Dividir":
				try:
					resultado = mpmath.fdiv(x, y)
				except ZeroDivisionError:
					resultado = x

			elif operación == "Multiplicar y adicionar":
				resultado = mpmath.fadd(mpmath.fmul(x, y), z)

			elif operación == "Potencia":
				resultado = mpmath.power(x, y)

			elif operación == "Logaritmo":
				resultado = mpmath.log(x, y)

			elif operación == "Raíz cuadrada":
				resultado = mpmath.sqrt(x)

			elif operación == "Inverso de raíz cuadrada":
				resultado = mpmath.fdiv(mpmath.mpf('1'), mpmath.sqrt(x))

			elif operación == "Absoluto":
				resultado = mpmath.fabs(x)

			elif operación == "Exponencial":
				resultado = mpmath.exp(x)

			elif operación == "Mínimo":
				resultado = min(x, y)

			elif operación == "Máximo":
				resultado = max(x, y)

			elif operación == "Menor que":
				if x < y:
					resultado = mpmath.mpf('1')
				else:
					resultado = mpmath.mpf('0')

			elif operación == "Mayor que":
				if x > y:
					resultado = mpmath.mpf('1')
				else:
					resultado = mpmath.mpf('0')

			elif operación == "Signo":
				resultado = mpmath.sign(x)

			elif operación == "Comparar":
				mínimo = mpmath.fsub(y, z)
				máximo = mpmath.fadd(y, z)
				if mínimo <= x <= máximo:
					resultado = mpmath.mpf('1')
				else:
					resultado = mpmath.mpf('0')

			elif operación == "Mínimo suave":
				resultado = "Aún no implementado."

			elif operación == "Máximo suave":
				resultado = "Aún no implementado."

			elif operación == "Redondear":
				resultado = mpmath.nint(x)

			elif operación in ("Piso", "Truncar"):
				resultado = mpmath.floor(x)

			elif operación == "Techo":
				resultado = mpmath.ceil(x)

			elif operación == "Fracción":
				resultado = mpmath.frac(x)

			elif operación == "Resto":
				resultado = mpmath.fmod(x, y)

			elif operación == "Ciclo":
				resultado = "Aún no implementado."

			elif operación == "Adherir":
				resultado = "Aún no implementado."

			elif operación == "Ping pong":
				resultado = "Aún no implementado."

			elif operación == "Seno":
				resultado = mpmath.sin(x)

			elif operación == "Coseno":
				resultado = mpmath.cos(x)

			elif operación == "Tangente":
				resultado = mpmath.tan(x)

			# Posibles mpc.
			elif operación == "Arco seno":
				resultado = mpmath.asin(x)

			elif operación == "Arco coseno":
				resultado = mpmath.acos(x)

			elif operación == "Arco tangente":
				resultado = mpmath.atan(x)

			elif operación == "Arco tangente 2":
				resultado = mpmath.atan2(x, y)

			elif operación == "Seno hiperbólico":
				resultado = mpmath.sinh(x)

			elif operación == "Coseno hiperbólico":
				resultado = mpmath.cosh(x)

			elif operación == "Tangente hiperbólica":
				resultado = mpmath.tanh(x)

			elif operación == "A radianes":
				resultado = mpmath.radians(x)

			elif operación == "A grados":
				resultado = mpmath.degrees(x)

			else:
				resultado = "¿Cómo sacaste esta opción?"
		except TypeError:
			if operación == "Adicionar":
				if type(x) is str and type(y) is str:
					resultado = x + y
				elif type(x) is str and type(y) is mpmath.mpf:
					resultado = y
				elif type(y) is str and type(x) is mpmath.mpf:
					resultado = x
			elif operación == "Multiplicar":
				if type(x) is str and type(y) is str:
					resultado = 0
				elif type(x) is str and type(y) is mpmath.mpf:
					resultado = x * int(y)
				elif type(y) is str and type(x) is mpmath.mpf:
					resultado = int(x) * y
			elif operación == "Multiplicar y adicionar":
				if type(z) is str:
					if type(x) is mpmath.mpf and type(y) is mpmath.mpf:
						resultado = mpmath.fmul(x, y)
					elif type(x) is str and type(y) is str:
						resultado = z
					elif type(x) is str and type(y) is mpmath.mpf:
						resultado = (x * int(y)) + z
					elif type(y) is str and type(x) is mpmath.mpf:
						resultado = (int(x) * y) + z

				elif type(z) is mpmath.mpf:
					if type(x) is str and type(y) is mpmath.mpf:
						resultado = x * int(y)
					elif type(y) is str and type(x) is mpmath.mpf:
						resultado = int(x) * y
			else:
				resultado = mpmath.mpf('0')

	if type(resultado) is mpmath.mpc:
		resultado = mpmath.re(resultado)

	return resultado