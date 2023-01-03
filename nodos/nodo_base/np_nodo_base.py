from lib.nodeeditor.Nodo import Nodo
from lib.nodeeditor.Zocalos import IZQUIERDA_ARRIBA, IZQUIERDA_CENTRO, IZQUIERDA_ABAJO
from lib.nodeeditor.Utilidades import dump_exception

from np_enlistado_de_nodos import *
from nodos.objetos.np_utilitarios import tratado_de_datos_para_tooltip
from nodos.nodo_base.np_zocalos import ZócalosdelNodoBase
from nodos.nodo_base.np_nodo_graficador import GraficadordelNodoBase
from nodos.nodo_base.np_nodo_contenido import ContenidodelNodoBase

DEBUG = False

imagen = "C:/Users/Maste/Downloads/icons/help (2).svg"

# @registrar_nodo(NODO_BASE)
class NodoBase(Nodo):
	icono = imagen
	codigo_op = NODO_BASE
	titulo_op = "Nodo base"

	ClaseGraficadeNodo = GraficadordelNodoBase
	ClasedelContenidodeNodo = ContenidodelNodoBase
	ClasedeZocalo = ZócalosdelNodoBase

	Entradas = [0, 1, 4, 3]
	Salidas = [1, 4, 3, 5]

	# Incluir un tipo de zócalo aquí elimina el rombito pequeño, si el tipo de nodo es un rombo.
	Rombitos = [
			[],  # Entradas
			[]   # Salidas
			]

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):

		self.conteo_de_errores()
		self.inicializado_de_valores(entradas, salidas)

		self.entradas_a_ocultar = []
		self.salidas_a_ocultar = []
		super().__init__(escena, titulo, entradas, salidas)
		self.control_de_zócalos()

		# Evaluación inicial.
		self.marcar_indefinido()
		# Método para poder añadir métodos antes de la evaluación en nodos instanciados a partir de este.
		self.evaluación_inicial()

	def evaluación_inicial(self):
		self.evaluación(False)

	def conteo_de_errores(self):
		self.errores_graves = 0
		self.errores_menores = 0

	def inicializado_de_valores(self, entradas, salidas):
		self.valores_de_entrada = []    # Para los valores que vienen de otros nodos.
		self.valores_de_salida = []     # Para los valores que el nodo enviará o otros.

		for zócalo in entradas:
			self.valores_de_entrada.append(None)
		for zócalo in salidas:
			self.valores_de_salida.append(None)

	def init_zocalos(self, entradas, salidas, reset=True):
		# Creación de zócalos para las entradas y salidas.

		if reset:
			# Limpiar los zócalos viejos.
			if hasattr(self, 'entradas') and hasattr(self, 'salidas'):
				# Quitar zócalos de la escena.
				for zocalo in (self.entradas + self.salidas):
					self.escena.graficador_de_la_escena.removeItem(zocalo.GraficosZocalos)
				self.entradas = []
				self.salidas = []

		# Creación de los nuevos zócalos.
		contador = 0
		for objeto in entradas:
			zocalo = self.__class__.ClasedeZocalo(
				nodo = self, indice = contador, posicion = self.pos_det_entradas, tipo_zocalo = objeto,
					multiconexión = self.entradas_multiconexion, cantidad_en_el_lado_actual = len(entradas),
					es_entrada = True, rombito = False if objeto in self.__class__.Rombitos[0] else True
				)
			contador += 1
			self.entradas.append(zocalo)

		contador = 0
		for objeto in salidas:
			zocalo = self.__class__.ClasedeZocalo(
				nodo = self, indice = contador, posicion = self.pos_det_salidas, tipo_zocalo = objeto,
				multiconexión = self.salidas_multiconexion, cantidad_en_el_lado_actual = len(salidas),
				es_entrada = False, rombito = False if objeto in self.__class__.Rombitos[1] else True
				)
			contador += 1
			self.salidas.append(zocalo)

	def obtener_posicion_zocalo(self, indice, posición, num_out_of = 1, *args):
		es_entrada = args[0]

		x = (
				self.zocalos_offsets[posición]
				if posición in (IZQUIERDA_ARRIBA, IZQUIERDA_CENTRO, IZQUIERDA_ABAJO)
				else self.Nodograficas.anchura_del_nodo + self.zocalos_offsets[posición]
		)

		techo = self.Nodograficas.altura_del_título + self.Nodograficas.márgen

		if es_entrada:
			altura = self.contenido.lista_de_posiciones_de_entradas[indice]
		else:
			altura = self.contenido.lista_de_posiciones_de_salidas[indice]

		if altura is None:
			altura = 0 - techo
			if es_entrada:
				self.entradas_a_ocultar.append(indice)
			else:
				self.salidas_a_ocultar.append(indice)

		y = (techo + altura)

		return [x, y]

	def obtener_posición_de_zocalo_en_la_escena(self, zocalo):
		pos_nodo = self.Nodograficas.pos()
		pos_zocalo = self.obtener_posicion_zocalo(
				zocalo.indice, zocalo.posicion, zocalo.cantidad_en_el_lado_actual, zocalo.es_entrada
				)
		return pos_nodo.x() + pos_zocalo[0], pos_nodo.y() + pos_zocalo[1]

	def control_de_zócalos(self):
		for indice in self.entradas_a_ocultar:
			self.entradas[indice].GraficosZocalos.setVisible(False)

		for indice in self.salidas_a_ocultar:
			self.salidas[indice].GraficosZocalos.setVisible(False)

	def control_de_errores(self):
		if self.errores_graves > 0:
			self.marcar_inválido()
		elif self.errores_menores > 0:
			self.marcar_indefinido()
		else:
			self.marcar_indefinido(False)
			self.marcar_inválido(False)
			self.Nodograficas.setToolTip("")

		self.errores_graves = 0
		self.errores_menores = 0

	def datos_de_conexion_cambiados(self, conexion):
		try:
			conexion.graficador_de_conexiones.definir_color_desde_el_zocalo()
		except AttributeError:
			if DEBUG:
				print(
						'Dibujaste una nueva conexión sobreescribiendo una existente y que al borrarse, ya no puede '
						'encontrarse ni actualizar su color. Por eso salta este error.'
						)
		# Yo pensaba que esto requería enviar una evaluación, pero resulta que al crear una conexión se llama a datos
		# de entrada cambiados y ese método ya trae una evaluación. Incluí un método de salidas cambiadas para
		# forzar una evaluación al nodo que envía datos y así actualizar los tooltips.

	def datos_de_entrada_cambiados(self, conexión):
		self.marcar_indefinido()
		self.evaluación()

	def datos_de_salida_cambiados(self):
		self.marcar_indefinido()
		self.evaluación(False)

	def evaluación(self, evaluar_hijos = True):
		try:
			self.obtención_de_datos_de_las_entradas()   # Esto tiene que ir antes de la evaluación porque si no, la
														# evaluación solo escogerá los valores internos en nodos hijos.
			self.valores_internos = self.contenido.lista_de_información
			self.valores_de_evaluación()

			evaluación = self.métodos_de_evaluación()

			for elemento in self.contenido.lista_de_contenidos:     # Esto originalmente estaba en datos de conexión
				elemento.ocultado_por_entrada()						# cambiados. Es para ocultar los widgets de entrada
				elemento.mostrado_por_entrada()						# que tienen conexiones. Pero dado que por la
																	# arquitectura, siempre se realiza una evaluación
																	# cuando se conecta algo, se movió acá, junto con
																	# el sistema que solo actualizaba las etiquetas.

			self.tooltips_de_los_zocalos()
			self.control_de_errores()
			if self.obtener_nodos_hijos() and evaluar_hijos is True:
				self.evaluar_hijos()
			return evaluación
		except ValueError:
			self.errores_graves += 1
			self.control_de_errores()
			self.Nodograficas.setToolTip(str(ValueError))
		except Exception as e:
			print("Exception")
			self.errores_graves += 1
			self.control_de_errores()
			self.Nodograficas.setToolTip(str(Exception))
			dump_exception(e)

	def obtención_de_datos_de_las_entradas(self):
		for entrada in self.entradas:
			if entrada.Zocaloconexiones:
				nodo = self.obtener_entrada(entrada.indice)
				contrazocalo = self.obtener_contrazócalo(entrada.indice)
				self.valores_de_entrada[entrada.indice] = nodo.valores_de_salida[contrazocalo.indice]
			else:
				self.valores_de_entrada[entrada.indice] = None

	def obtener_contrazócalo(self, indice = 0):
		try:
			zocalo_entrada = self.entradas[indice]
			if len(zocalo_entrada.Zocaloconexiones) == 0: return None
			conexion_conectada = zocalo_entrada.Zocaloconexiones[0]
			contrazocalo = conexion_conectada.obtener_otros_zocalos(self.entradas[indice])
			return contrazocalo
		except Exception:
			print(str(Exception))
			return None

	def valores_de_evaluación(self):
		for elemento in self.contenido.lista_de_contenidos:
			if elemento.zócalo_de_salida is not None:
				try:
					if elemento.zócalo_de_entrada is not None and self.entradas[elemento.zócalo_de_entrada].Zocaloconexiones:
						self.valores_de_salida[elemento.zócalo_de_salida] = self.valores_de_entrada[elemento.zócalo_de_entrada]
					else:
						# Por defecto, los elementos que no comparten posición escriben su valor siempre.
						if not elemento.comparte_posición:
							self.valores_de_salida[elemento.zócalo_de_salida] = self.valores_internos[elemento.índice]
						# Y si alguien llega aquí es porque comparte posición, en cuyo caso, solo si son visibles,
						# sobreescribirán el dato de la salida que comparten.
						elif not elemento.autooculto:
							self.valores_de_salida[elemento.zócalo_de_salida] = self.valores_internos[elemento.índice]

				except IndexError:
					print('La lista de valores de salida está vacía. Eso significa que el zócalo requerido no existe.')
			else:
				pass
		return self.valores_de_salida

	def métodos_de_evaluación(self):
		pass

	def tooltips_de_los_zocalos(self):
		no_evaluado = 'El valor del zócalo aún no ha sido calculado.'
		error_de_cálculo = 'Error de cálculo.'

		zócalos = self.entradas + self.salidas
		cantidad_de_conexiones = 0

		self.entradas_tratadas = tratado_de_datos_para_tooltip(self.valores_de_entrada, True)
		self.internos_tratados = tratado_de_datos_para_tooltip(self.valores_internos, True)
		self.salidas_tratadas = tratado_de_datos_para_tooltip(self.valores_de_salida, True)

		for zócalo in zócalos:
			if len(zócalo.Zocaloconexiones) != 0:
				cantidad_de_conexiones += 1

		# Tooltip si el nodo no está conectado a nada.
		if cantidad_de_conexiones == 0:
			for zócalo in zócalos:
				zócalo.GraficosZocalos.setToolTip(no_evaluado)
		else:
			for zócalo in self.salidas:
				# En caso un cálculo de la evaluación de None, cosa que solo pasaría si se me pasa (espero),
				# el tooltip me avisará.
				if zócalo.Zocaloconexiones and self.valores_de_salida[zócalo.indice] is None:
					zócalo.GraficosZocalos.setToolTip(error_de_cálculo)
					self.errores_graves += 1

				# Seteo del tooltip solo en caso esté conectado el zócalo.
				elif zócalo.Zocaloconexiones and self.valores_de_salida[zócalo.indice] is not None:
					zócalo.GraficosZocalos.setToolTip(self.salidas_tratadas[zócalo.indice])
				else:
					zócalo.GraficosZocalos.setToolTip(no_evaluado)


			for zócalo in self.entradas:
				if zócalo.Zocaloconexiones and self.valores_de_entrada[zócalo.indice] is None:
					zócalo.GraficosZocalos.setToolTip(error_de_cálculo)
					self.errores_graves += 1

				elif zócalo.Zocaloconexiones:
					# Aquí se muestran los valores de la salida conectada. Estamos usando la lista de valores de
					# entrada.
					zócalo.GraficosZocalos.setToolTip(self.entradas_tratadas[zócalo.indice])
				else:
					# Aquí obtenemos los valores internos.
					for elemento in self.contenido.lista_de_contenidos:
						if elemento.zócalo_de_entrada is not None:
							if zócalo.indice == elemento.zócalo_de_entrada:
								zócalo.GraficosZocalos.setToolTip(self.internos_tratados[elemento.índice])

	def serialización(self):
		res = super().serialización()
		res['Código'] = self.__class__.codigo_op
		return res

	def deserialización(self, data, hashmap = {}, restaure_id = True, *args, **kwargs):
		res = super().deserialización(data, hashmap, restaure_id)
		return res