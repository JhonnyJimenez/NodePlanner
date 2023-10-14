import math
import numpy
import mpmath
from PyQt5.QtCore import Qt

NODOS_NO_DISPONIBLES = [0, 1, 6, 8]
LISTA_DE_CALENDARIOS = set()

class UnidadDeMedida():
	def __init__(self, *args, **kwargs):
		self.llave = kwargs.get('numero')
		self.nombre = kwargs.get('nombre')
		self.es_absoluta = kwargs.get('es_absoluta')
		self.no_subunidad = kwargs.get('no_subunidad', mpmath.mpf(0))
		self.subunidades = kwargs.get('subunidades', mpmath.mpf(1))
		self.lista_de_nombres = kwargs.get('lista_de_nombres')

		# print("Llave:", self.llave, type(self.llave))
		# print("Nombre:", self.nombre, type(self.nombre))
		# print("es_absoluto:", self.es_absoluta, type(self.es_absoluta))
		# print("no_subunidad:", self.no_subunidad, type(self.no_subunidad))
		# print("Subunidades:", self.subunidades, type(self.subunidades))
		# print("Lista de nombres:", self.lista_de_nombres, type(self.lista_de_nombres))
		# print("----------------------------------------")
			 
	def __str__(self) -> str:
		return self.nombre

class Fecha():
	def __init__(self, *args, **kwargs):
		self.dato_inicial = kwargs.get('inicio')
		self.lista_de_unidades = kwargs.get('unidades')
		# print(self.lista_de_unidades)
		self.fechador()
		# self.fechador_original()
		self.fecha = str(kwargs.get('formato'))

	def excepciones(self):
		pass

	def fechador(self):

		for unidad_de_medida in self.lista_de_unidades.values():
			unidad_actual = unidad_de_medida
			llave = unidad_actual.llave
			subunidad = self.lista_de_unidades[unidad_actual.no_subunidad]
			self.lista_de_unidades[llave].unidades_superiores = []
			
			for unidad_revisada in self.lista_de_unidades.values():
				if unidad_revisada.no_subunidad == llave:
					self.lista_de_unidades[llave].unidades_superiores.append(unidad_revisada)

			# self.lista_de_unidades[llave].unidad_superior = True if (len(unidades_superiores) > 1 and llave == 0) or (len(unidades_superiores) > 0 and llave != 0) else False

			if llave == 0:
				dato_de_inicio = self.dato_inicial
			else:
				dato_de_inicio = subunidad.resultado

			self.lista_de_unidades[llave].resultado = self.divisor(dato_de_inicio, unidad_actual.subunidades)
			self.lista_de_unidades[llave].restos = {}

			for superior in self.lista_de_unidades[llave].unidades_superiores[1 if llave == 0 else 0:]:
				self.lista_de_unidades[llave].restos[superior.llave] = self.divisor(self.lista_de_unidades[llave].resultado, superior.subunidades, devolver = 'resto')

	def divisor(self, valor_a_procesar, valores_a_restar, devolver = 'resultado', contador = 1, resultado = 0):
		if type(valores_a_restar) is list:
			while valor_a_procesar > mpmath.mpf(0):
				self.excepciones()
				suma = sum(valores_a_restar)

				if valor_a_procesar > suma:
					multiplicador = mpmath.floor(mpmath.fdiv(valor_a_procesar, suma))
					valor_a_procesar = mpmath.fsub(valor_a_procesar, mpmath.fmul(multiplicador, suma))
					resultado += (multiplicador * len(valores_a_restar))
				elif valor_a_procesar < valores_a_restar[contador - 1]:
					break
				else:
					valor_a_procesar = mpmath.fsub(valor_a_procesar, valores_a_restar[contador - 1])
					if contador != len(valores_a_restar):
						contador += 1
					else:
						contador = 1
					resultado += 1
			resto = valor_a_procesar
		else:
			try:
				resultado = mpmath.fdiv(valor_a_procesar, valores_a_restar)
				resto = mpmath.fmod(valor_a_procesar, valores_a_restar)
			except ZeroDivisionError:
				resultado = mpmath.fdiv(valor_a_procesar, 1)
				resto = mpmath.fmod(valor_a_procesar, 1)
			resultado = mpmath.floor(resultado)
			resto = mpmath.floor(resto)
		if devolver == 'resultado':
			return resultado
		else:
			return resto



	# def fechador_original(self):
	# 	for elemento in self.unidades:
	# 		unidad = self.unidades[elemento]
	# 		for superior in self.unidades:
	# 			try:
	# 				# Si es la primera subunidad (numerada con el cero por defecto) y es una unidad absoluta, entonces buscará su superior y el divisor correspondiente para comenzar su conteo. En el caso opuesto, solo devolverá el número inicial.
	# 				if unidad.número == mpmath.mpf('0') and unidad.es_absoluta:
	# 					if unidad.llave == self.unidades[superior].no_subunidad:
	# 						unidad.dato = mpmath.fmod(self.inicio, self.unidades[superior].subunidades)
	# 						break 
	# 					else:
	# 						unidad.dato = self.inicio
	# 				# ----------------------------------------------------------------------------------------
	# 				else:
	# 					if unidad.número == mpmath.mpf('0'):
	# 						dato_divisor = self.inicio
	# 					else:
	# 						dato_divisor = self.unidades[unidad.no_subunidad].división_bruta
						
	# 					# if not unidad.es_constante:
	# 					# 	self.excepciones()
	# 					# 	contador = 0
	# 					# 	unidad.divisón_bruta = 0
	# 					# 	while dato_divisor <= mpmath.mpf(0):
	# 					# 		dato_divisor = mpmath.fsub(dato_divisor, unidad.subunidades[contador])
	# 					# 		if contador != (len(unidad.subunidades) - 1):
	# 					# 			contador += 1
	# 					# 		else:
	# 					# 			contador = 0
	# 					# 		unidad.división_bruta += 1
	# 					# else:
	# 					unidad.división_bruta = mpmath.floor(mpmath.fdiv(dato_divisor, unidad.subunidades))
						
	# 					if not unidad.es_absoluta:
	# 						if unidad.llave == self.unidades[superior].no_subunidad:
	# 							unidad.dato = mpmath.fmod(unidad.división_bruta, self.unidades[superior].subunidades)
	# 						else:
	# 							unidad.dato = unidad.división_bruta
	# 					else:
	# 						unidad.dato = unidad.división_bruta
	# 			except ZeroDivisionError:
	# 				unidad.dato = mpmath.mpf('45')

	def __str__(self) -> str:
		for elemento in self.lista_de_unidades.values():
			for superior in elemento.unidades_superiores[1 if elemento.llave == 0 else 0:]:
				self.fecha = self.fecha.replace('%' + '%s-%s' % (elemento.llave, superior.llave), str(tratado_de_datos(elemento.restos[superior.llave])))
			self.fecha = self.fecha.replace('%' + '%s' % elemento.llave, str(tratado_de_datos(elemento.resultado)))
		return self.fecha

# -------------------------------------------------------------------------

def cambios_al_inicio(escena):
	actualizador_de_calendaristas(escena)

def actualizador_de_calendaristas(escena):
	for nodo in escena.nodos:
		if nodo.__class__.__name__ == 'NodoCalendarista':
			for contenido in (
					nodo.contenido.contenido_de_salidas
					+ nodo.contenido.contenido_de_entradas
			):
				if hasattr(contenido, 'tipo') and contenido.tipo == 2:
					contenido.contenido()
			nodo.datos_de_entrada_cambiados()

def tratado_de_datos(dato_a_tratar, especificación: bool = False, serializado = False, de_lista = False):
	tipo = type(dato_a_tratar)

	if dato_a_tratar is None:
		if de_lista:
			dato_a_tratar = 'Dato nulo'
			if especificación:
				dato_a_tratar += ' (NoneType)'
		else:
			pass

	elif tipo in (int, float):
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

	elif tipo is str:
		if dato_a_tratar != '':
			if especificación:
				dato_a_tratar += ' (Cadena)'
		else:
			if not serializado:
				dato_a_tratar = 'Cadena vacía.'

	elif tipo is bool:
		if dato_a_tratar is True:
			dato_a_tratar = 'Verdadero'
		else:
			dato_a_tratar = 'Falso'
		if especificación:
			dato_a_tratar += ' (Booleana de Python)'

	elif tipo is mpmath.mpf:
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

	elif tipo is Qt.CheckState:
		if dato_a_tratar == 0:
			dato_a_tratar = 'Falso'
		if dato_a_tratar == 1:
			dato_a_tratar = 'Indeterminado'
		if dato_a_tratar == 2:
			dato_a_tratar = 'Verdadero'
		if especificación:
			dato_a_tratar += ' (Booleana de Qt)'

	elif tipo is UnidadDeMedida:
		dato_a_tratar = str(dato_a_tratar)
		if especificación:
			dato_a_tratar += ' (Unidad de tiempo)'

	elif tipo is Fecha:
	# 	nombre = dato_a_tratar.nombre
		dato_a_tratar = str(dato_a_tratar)
		if especificación:
			dato_a_tratar += ' (Fecha)'

	elif tipo is list:
		if len(dato_a_tratar) == 0:
			dato_a_tratar = 'Lista vacía'
		elif len(dato_a_tratar) == 1:
			dato_a_tratar = tratado_de_datos(dato_a_tratar[0], especificación)
		else:
			dato_tratado = ''
			contador = 0
			for elemento in dato_a_tratar:
				contador += 1
				if len(dato_a_tratar) == contador:
					dato_tratado += tratado_de_datos(elemento, especificación, de_lista = True)
				else:
					dato_tratado += (tratado_de_datos(elemento, especificación, de_lista = True) + '\n')
			dato_a_tratar = dato_tratado

	else:
		dato_a_tratar = 'El tipo de datos %s no ha sido tratado.' % str(tipo.__name__)

	return dato_a_tratar

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

def matemáticas_nativas(operación, *args):
	x = args[0]
	y = args[1]
	z = args[2]
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
			try:
				resultado = x % y
			except ZeroDivisionError:
				resultado = x

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
				try:
					resultado = mpmath.fmod(x, y)
				except ZeroDivisionError:
					resultado = x

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
					resultado = mpmath.mpf('0')
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

# --------------------------------------------
