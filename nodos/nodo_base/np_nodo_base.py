from lib.nodeeditor.Nodo import *

from np_enlistado_de_nodos import *
from nodos.nodo_base.np_zocalos import NodoBaseZocalos
from nodos.nodo_base.np_nodo_graficador import NodoBaseGraficador
from nodos.nodo_base.np_nodo_contenido import NodoBaseContenido

DEBUG = False

imagen = "C:/Users/Maste/Downloads/icons/help (2).svg"

@registrar_nodo(NODO_BASE)
class NodoBase(Nodo):
	icono = imagen
	codigo_op = NODO_BASE
	titulo_op = "Nodo base"

	ClaseGraficadeNodo = NodoBaseGraficador
	ClasedelContenidodeNodo = NodoBaseContenido
	ClasedeZocalo = NodoBaseZocalos

	def __init__(self, escena, titulo = titulo_op, entradas=[], salidas=[4, 1, 3, 5]):
		super().__init__(escena, titulo, entradas, salidas)
		# self.marcarIndefinido()
		# self.actualizacion()
		# self.evaluación()

	# def initConfiguraciones(self):
	# 	super().initConfiguraciones()
	# 	self.espaciadoconectores = 25  # El original es de 22.
	# 	self.pos_det_entradas = Izquierda_abajo
	# 	self.pos_det_salidas = Derecha_arriba
	#
	# def initZocalos(self, entradas, salidas, reset=True):
	# 	# Creación de zócalos para las entradas y salidas.
	#
	# 	if reset:
	# 		# Limpiar los zócalos viejos.
	# 		if hasattr(self, 'entradas') and hasattr(self, 'salidas'):
	# 			# Quitar zócalos de la escena.
	# 			for zocalo in (self.entradas + self.salidas):
	# 				self.escena.graficador_de_la_escena.removeItem(zocalo.GraficosZocalos)
	# 			self.entradas = []
	# 			self.salidas = []
	#
	# 	self.valores_entrantes = []
	# 	self.valores = []
	# 	self.espaciado_entradas = []
	# 	self.espaciado_salidas = []
	#
	# 	for zocalo in entradas:
	# 		self.espaciado_entradas.append(0)
	# 		self.valores_entrantes.append(None)
	#
	# 	for zocalo in salidas:
	# 		self.espaciado_salidas.append(0)
	# 		self.valores.append(None)
	#
	# 	if DEBUG:
	# 		print(self.espaciado_entradas)
	# 		print(self.espaciado_salidas)
	# 		print(self.valores)
	#
	# 	self.ediciones_de_espaciado()
	#
	# 	# Creación de los nuevos zócalos.
	# 	contador = 0
	# 	for objeto in entradas:
	# 		zocalo = self.__class__.ClasedeZocalo(
	# 			nodo = self, indice = contador, posicion = self.pos_det_entradas,
	# 			tipo_zocalo = objeto, multiconexion = self.entradas_multiconexion,
	# 			cantidad_en_el_lado_actual = len(entradas), esEntrada = True, espaciado_extra = self.espaciado_entradas
	# 			)
	# 		contador += 1
	# 		self.entradas.append(zocalo)
	#
	# 	contador = 0
	# 	for objeto in salidas:
	# 		zocalo = self.__class__.ClasedeZocalo(
	# 			nodo = self, indice = contador, posicion = self.pos_det_salidas,
	# 			tipo_zocalo = objeto, multiconexion = self.salidas_multiconexion,
	# 			cantidad_en_el_lado_actual = len(salidas), esEntrada = False, espaciado_extra = self.espaciado_salidas
	# 			)
	# 		contador += 1
	# 		self.salidas.append(zocalo)
	#
	# def obtener_posicion_zocalo(self, indice, posicion, radio, num_out_of = 1, lista_de_espaciado = []):
	# 	x = (
	# 			self.zocalos_offsets[posicion]
	# 			if posicion in (Izquierda_arriba, Izquierda_centro, Izquierda_abajo)
	# 			else self.Nodograficas.anchoNodo + self.zocalos_offsets[posicion]
	# 			)
	#
	# 	espaciado = None
	# 	try:
	# 		if type(lista_de_espaciado[indice]) in (int, float):
	# 			espaciado = int(lista_de_espaciado[indice])
	# 		else:
	# 			espaciado = 0
	# 	except IndexError as e:
	# 		espaciado = 0
	#
	# 	if posicion in (Izquierda_abajo, Derecha_abajo):
	# 		# Comenzando desde abajo.
	# 		y = (
	# 			self.Nodograficas.altoNodoparaCalculos
	# 			- self.Nodograficas.redondezdelaOrilladelNodo
	# 			- self.Nodograficas.sangria_vertical_del_titulo
	# 			- (radio * 1.5)
	# 			- (((num_out_of - 1) - indice) * self.espaciadoconectores)
	# 			- espaciado
	# 			)
	# 	elif posicion in (Izquierda_centro, Derecha_centro):
	# 		no_de_zocalos = num_out_of
	# 		altura_del_nodo = self.Nodograficas.altoNodoparaCalculos
	# 		altura_no_usable = self.Nodograficas.alturaTituloNodo + 2 * self.Nodograficas.sangria_vertical_del_titulo + self.Nodograficas.sangria_de_la_orilla
	# 		altura_disponible = altura_del_nodo - altura_no_usable
	#
	# 		altura_total_de_todos_los_zocalos = num_out_of * self.espaciadoconectores
	# 		nueva_altura = altura_disponible - altura_total_de_todos_los_zocalos
	#
	# 		y = altura_no_usable + altura_disponible / 2.0 + (indice - 0.5) * self.espaciadoconectores
	# 		if no_de_zocalos > 1:
	# 			y -= self.espaciadoconectores * (no_de_zocalos - 1) / 2
	#
	# 	elif posicion in (Izquierda_arriba, Derecha_arriba):
	# 		# Comenzando desde arriba.
	# 		y = (
	# 				self.Nodograficas.alturaTituloNodo
	# 				+ self.Nodograficas.sangria_vertical_del_titulo
	# 				+ self.Nodograficas.redondezdelaOrilladelNodo
	# 				+ (indice * self.espaciadoconectores)
	# 				+ (radio * 1.5)
	# 				+ espaciado
	# 				)
	# 	else:
	# 		# Esto nunca debe pasar.
	# 		y = 0
	#
	# 	return [x, y]
	#
	# def ediciones_de_espaciado(self):
	# 	self.editor_de_espaciado(0, 2, 25)
	#
	# def editor_de_espaciado(self, indice, lista: list | int, valor):
	# 	if type(lista) is int:
	# 		if lista == 1:
	# 			lista = self.espaciado_entradas
	# 		elif lista == 2:
	# 			lista = self.espaciado_salidas
	# 	else:
	# 		pass
	#
	# 	indice_fun = indice
	# 	contador = indice_fun - 1
	# 	for elemento in lista[indice_fun:]:
	# 		contador += 1
	# 		lista[lista.index(elemento, contador)] += valor
	#
	# 	if DEBUG:
	# 		print("Los ajustes de entradas son:", self.espaciado_entradas)
	# 		print("Los ajustes de salidas son:", self.espaciado_salidas)
	#
	# def obtenerPosiciondeZocaloenEscena(self, zocalo):
	# 	pos_nodo = self.Nodograficas.pos()
	# 	pos_zocalo = self.obtener_posicion_zocalo(
	# 			zocalo.indice, zocalo.posicion, zocalo.GraficosZocalos.radio, zocalo.cantidad_en_el_lado_actual,
	# 			zocalo.espaciado_extra
	# 			)
	# 	return (pos_nodo.x() + pos_zocalo[0], pos_nodo.y() + pos_zocalo[1])
	#
	# def actualizacion(self):
	# 	self.contenido.objeto_1.textChanged.connect(self.DatosdeEntradaCambiados)
	# 	self.contenido.objeto_2.textChanged.connect(self.DatosdeEntradaCambiados)
	# 	self.contenido.objeto_3.stateChanged.connect(self.DatosdeEntradaCambiados)
	# 	self.contenido.objeto_4.currentTextChanged.connect(self.DatosdeEntradaCambiados)
	#
	# def ImplementarEvaluacion(self):
	# 	self.Evaluacion_de_texto(self.contenido.objeto_1)
	# 	self.evaluacion_númerica(self.contenido.objeto_2)
	# 	self.EvaluacionBooleana(self.contenido.objeto_3)
	# 	self.EvaluacionListado(self.contenido.objeto_4)
	# 	self.evaluarHijos()
	#
	# def evaluación(self):
	# 	# Actualiza las posiciones de los zócalos.
	# 	for zocalo in self.entradas + self.salidas:
	# 		zocalo.definir_posicion_del_zocalo()
	# 	try:
	# 		evaluacion = self.ImplementarEvaluacion()
	# 		self.zocalos_tooltip()
	# 		return evaluacion
	# 	except ValueError as e:
	# 		self.marcarInvalido()
	# 		self.Nodograficas.setToolTip(str(e))
	# 	except Exception as e:
	# 		print("Exception")
	# 		self.marcarInvalido()
	# 		self.Nodograficas.setToolTip(str(e))
	# 		dump_exception(e)
	#
	# def zocalos_tooltip(self):
	# 	no_calculado = "El valor de zócalo aún no ha sido calculado"
	#
	# 	for zocalo in (self.entradas + self.salidas):
	# 		if zocalo.esEntrada:
	# 			nodo_de_entrada = self.obtenerEntrada(zocalo.indice)
	# 			contrazocalo = self.obtenerContrazocalo(zocalo.indice)
	# 			if not nodo_de_entrada:
	# 				zocalo.GraficosZocalos.setToolTip(no_calculado)
	# 			else:
	# 				valor = self.textualizador(nodo_de_entrada.valores[contrazocalo.indice], True)
	# 				zocalo.GraficosZocalos.setToolTip(valor)
	# 		elif zocalo.esSalida:
	# 			if zocalo.Zocaloconexiones != []:
	# 				valor = self.valores[zocalo.indice]
	# 				if valor is None:
	# 					zocalo.GraficosZocalos.setToolTip(no_calculado)
	# 				elif valor is not None:
	# 					valor = self.textualizador(valor, True)
	# 					zocalo.GraficosZocalos.setToolTip(valor)
	# 				else:
	# 					# En teoría, esta tooltip nunca debería salir.
	# 					zocalo.GraficosZocalos.setToolTip("Puede haber un error.")
	# 			else:
	# 				zocalo.GraficosZocalos.setToolTip(no_calculado)
	# 		else:
	# 			# Esto es para evitar crasheos por si algún día llego a implementar los zocalos para redireccionar
	# 			# conexiones.
	# 			print("Hubo un problema al crear los tooltips de los zócalos. Revisa la evaluación del nodo base.")
	# 			pass
	#
	# def textualizador(self, valor, especificacion: bool = False):
	# 	respuesta_booleana = 'No deberías poder ver esta respuesta.'
	# 	if type(valor) == Qt.CheckState:
	# 		if valor == 0:
	# 			respuesta_booleana = 'Falso'
	# 		if valor == 1:
	# 			respuesta_booleana = 'Indeterminado'
	# 		if valor == 2:
	# 			respuesta_booleana = 'Verdadero'
	#
	# 	if especificacion:
	# 		if type(valor) == str:
	# 			valor_resuelto = valor + ' (Cadena)'
	# 		elif type(valor) == int:
	# 			valor_resuelto = self.formato_de_números(valor)
	# 			valor_resuelto += ' (Entero)'
	# 		elif type(valor) == float:
	# 			valor_resuelto = self.formato_de_números(valor)
	# 			valor_resuelto += ' (Decimal)'
	# 		elif type(valor) == Qt.CheckState:
	# 			valor_resuelto = respuesta_booleana + ' (Booleana)'
	# 	else:
	# 		if type(valor) == Qt.CheckState:
	# 			valor_resuelto = respuesta_booleana
	# 		elif type(valor) == str:
	# 			valor_resuelto = valor
	# 		else:
	# 			valor_resuelto = self.formato_de_números(valor)
	#
	# 	return valor_resuelto
	#
	# def formato_de_números(self, número: float | int):
	# 	número = "{:,}".format(número)
	# 	número = número.replace(",", " ")
	# 	return número
	#
	# def Evaluacion_de_texto(self, objeto):
	# 	self.valores[objeto.zocalo] = objeto.text()
	#
	# 	self.marcarIndefinido(False)
	# 	self.marcarInvalido(False)
	# 	self.Nodograficas.setToolTip("")
	#
	# 	return self.valores[objeto.zocalo]
	#
	# def evaluacion_númerica(self, objeto):
	# 	if objeto.text() in ('', '.', '-', '+'):
	# 		valor = 0
	# 	else:
	# 		valor = "".join(objeto.text().split())
	#
	# 	valor = float(valor)
	#
	# 	decimales, entero = math.modf(valor)
	#
	# 	if decimales == 0.0:
	# 		valor = int(valor)
	#
	# 	self.valores[objeto.zocalo] = valor
	# 	self.marcarIndefinido(False)
	# 	self.marcarInvalido(False)
	# 	self.Nodograficas.setToolTip("")
	#
	# 	return self.valores[objeto.zocalo]
	#
	# def EvaluacionBooleana(self, objeto):
	# 	self.valores[objeto.zocalo] = objeto.checkState()
	# 	self.marcarIndefinido(False)
	# 	self.marcarInvalido(False)
	#
	# 	return self.valores[objeto.zocalo]
	#
	# def EvaluacionListado(self, objeto):
	# 	self.valores[objeto.zocalo] = objeto.currentText()
	# 	self.marcarIndefinido(False)
	# 	self.marcarInvalido(False)
	#
	# 	return self.valores[objeto.zocalo]
	#
	# def DatosdeConexionCambiados(self, conexion):
	# 	try:
	# 		conexion.graficador_de_conexiones.definir_color_desde_el_zocalo()
	# 		self.zocalos_tooltip()
	# 	except AttributeError as e:
	# 		if DEBUG:
	# 			print(
	# 					'Dibujaste una nueva conexión sobreescribiendo una existente y que al borrarse, ya no puede '
	# 					'encontrarse ni actualizar su color. Por eso salta este error.'
	# 					)
	#
	# def DatosdeEntradaCambiados(self, zocalo = None):
	# 	self.marcarIndefinido()
	# 	self.evaluación()
	#
	# def obtenerContrazocalo(self, indice=0):
	# 	try:
	# 		zocalo_entrada = self.entradas[indice]
	# 		if len(zocalo_entrada.Zocaloconexiones) == 0: return None
	# 		conexion_conectada = zocalo_entrada.Zocaloconexiones[0]
	# 		contrazocalo = conexion_conectada.obtener_otros_zocalos(self.entradas[indice])
	# 		return contrazocalo
	# 	except Exception as e:
	# 		dump_exception(e)
	# 		return None
	#
	# def serialización(self):
	# 	res = super().serialización()
	# 	res['Codigo_op'] = self.__class__.codigo_op
	# 	return res
	#
	# def deserialización(self, data, hashmap = {}, restaure_id = True, *args, **kwargs):
	# 	res = super().deserialización(data, hashmap, restaure_id)
	# 	return res