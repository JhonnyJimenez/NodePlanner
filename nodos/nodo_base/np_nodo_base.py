from lib.nodeeditor.Seriabilizador import Serializable
from lib.nodeeditor.Nodo import Nodo
from lib.nodeeditor.Zocalos import IZQUIERDA_ARRIBA, IZQUIERDA_CENTRO, IZQUIERDA_ABAJO
from lib.nodeeditor.Utilidades import dump_exception

from np_enlistado_de_nodos import *
from nodos.nodo_base.np_zocalos import ZócalosdelNodoBase
from nodos.nodo_base.np_nodo_graficador import GraficadordelNodoBase
from nodos.nodo_base.np_nodo_contenido import ContenidodelNodoBase

from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_utilitarios import tratado_de_datos

DEBUG = False

@registrar_nodo(NODO_BASE)
class NodoBase(Nodo):
	icono = "iconos/nodo base.svg"
	codigo_op = NODO_BASE
	titulo_op = "Nodo base"

	ClaseGraficadeNodo = GraficadordelNodoBase
	ClasedelContenidodeNodo = ContenidodelNodoBase
	ClasedeZocalo = ZócalosdelNodoBase

	Entradas = [1, 4, 3]
	Salidas = [1, 4, 3, 5]

	FormadeEntradas = ['Círculo', 'Círculo', 'Círculo', 'Círculo', 'Circulo', 'Círculo', 'Círculo', 'Círculo', 'Círculo', 'Circulo', 'Círculo', 'Círculo', 'Círculo', 'Círculo', 'Circulo', 'Círculo', 'Círculo', 'Círculo', 'Círculo', 'Circulo']
	FormadeSalidas = ['Círculo', 'Círculo', 'Círculo', 'Círculo', 'Circulo', 'Círculo', 'Círculo', 'Círculo', 'Círculo', 'Circulo', 'Círculo', 'Círculo', 'Círculo', 'Círculo', 'Circulo', 'Círculo', 'Círculo', 'Círculo', 'Círculo', 'Circulo']

	Entradas_multiconexión = []
	Salidas_multiconexión = []

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		# Conteo de errores:
		self.errores_graves = 0
		self.errores_menores = 0

		self.entradas_a_ocultar = []
		self.salidas_a_ocultar = []

		super().__init__(escena, titulo, entradas, salidas)
		self.descendencia = set()
		self.valores = self.contenido.valores
		self.diccionarios = self.contenido.diccionarios
		self.ajustes_adicionales()
		self.control_de_zócalos()

		# Evaluación inicial.
		self.marcar_indefinido()
		if self.escena.deserializando is False:
			# Método para poder añadir métodos antes de la evaluación en nodos instanciados a partir de este.
			self.evaluación_inicial()

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
					multiconexión = self.zócalo_multiconexión(self.__class__.Entradas_multiconexión, contador, self.entradas_multiconexion),
					cantidad_en_el_lado_actual = len(entradas),
					es_entrada = True,
					forma = self.__class__.FormadeEntradas[contador] if self.__class__.FormadeEntradas[contador] is not None else 'Círculo'
				)
			contador += 1
			self.entradas.append(zocalo)

		contador = 0
		for objeto in salidas:
			zocalo = self.__class__.ClasedeZocalo(
					nodo = self, indice = contador, posicion = self.pos_det_salidas, tipo_zocalo = objeto,
					multiconexión = self.zócalo_multiconexión(self.__class__.Salidas_multiconexión, contador, self.salidas_multiconexion),
					cantidad_en_el_lado_actual = len(salidas),
					es_entrada = False,
					forma = self.__class__.FormadeSalidas[contador] if self.__class__.FormadeSalidas[contador] is not None else 'Círculo'
				)
			contador += 1
			self.salidas.append(zocalo)

	def zócalo_multiconexión(self, lista: list, contador: int, valor_por_defecto: bool):
		try:
			if lista[contador] not in (None, ''):
				es_multiconexión = lista[contador]
			else:
				es_multiconexión = valor_por_defecto
		except IndexError:
			es_multiconexión = valor_por_defecto

		return es_multiconexión

	def obtener_posicion_zocalo(self, indice, posición, num_out_of = 1, *args):
		es_entrada = args[0]

		x = (
				self.zocalos_offsets[posición]
				if posición in (IZQUIERDA_ARRIBA, IZQUIERDA_CENTRO, IZQUIERDA_ABAJO)
				else self.Nodograficas.anchura_del_nodo + self.zocalos_offsets[posición]
		)

		techo = self.Nodograficas.altura_del_título + self.Nodograficas.márgen

		if es_entrada:
			altura = self.contenido.posicionador_de_entradas[indice]
		else:
			altura = self.contenido.posicionador_de_salidas[indice]

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

	def ajustes_adicionales(self):
		pass

	def obtener_descendencia(self):
		nodos_padres = self.obtener_nodos_padres()
		nodos_hijos = self.obtener_nodos_hijos()

		for nodo in nodos_hijos:
			self.descendencia.add(nodo)
			for padre in nodos_padres:
				padre.descendencia.add(nodo)

		return self.descendencia

	def obtener_nodos_padres(self):
		if not self.entradas: return []
		lista_de_nodos_padres = []
		for ix in range(len(self.entradas)):
			for conexion in self.entradas[ix].Zocaloconexiones:
				nodo_padre = conexion.obtener_otros_zocalos(self.entradas[0]).nodo
				lista_de_nodos_padres.append(nodo_padre)
		return lista_de_nodos_padres

	def control_de_zócalos(self):
		for indice in self.entradas_a_ocultar:
			self.entradas[indice].GraficosZocalos.hide()

		for indice in self.salidas_a_ocultar:
			self.salidas[indice].GraficosZocalos.hide()

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

	def evaluación_inicial(self):
		self.evaluación(False)

	def datos_de_entrada_cambiados(self, conexión = None):
		if self.escena.deserializando is False:
			self.marcar_indefinido()
			self.evaluación()

	def datos_de_salida_cambiados(self):
		self.marcar_indefinido()
		self.evaluación(False)

	def evaluación(self, evaluar_hijos = True):
		try:
			self.datos_de_entrada()                     # Esto tiene que ir antes de la evaluación porque si no, la
														# evaluación solo escogerá los valores internos en nodos hijos.
			self.ajustes_preevaluación()
			self.valores_preevaluación = self.valores.copy()
			evaluación = self.métodos_de_evaluación()

			try:
				for elemento in self.contenido.contenido_de_entradas:   # Esto originalmente estaba en datos de conexión
					elemento.widget_conectado()                         # cambiados. Es para ocultar los widgets de
					elemento.widget_desconectado()                      # entrada
			except AttributeError:                                      # que tienen conexiones. Pero dado que por la
				pass                                                    # arquitectura siempre se realiza una evaluación
																		# cuando se conecta algo, se movió acá junto con
																		# el sistema que solo actualizaba las etiquetas.

			self.tooltips_de_los_zocalos()
			self.descendencia = self.obtener_descendencia()
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

	def datos_de_entrada(self):
		for zócalo in self.entradas:
			if len(zócalo.Zocaloconexiones) == 1 and zócalo.es_multiconexión is False:
				contranodo = self.obtener_entrada(zócalo.indice)
				contrazócalo = self.obtener_contrazócalo(zócalo.indice)
				try:
					self.valores[self.diccionarios['Entradas'][zócalo.indice]] = contranodo.valores[
						contranodo.diccionarios['Salidas'][contrazócalo.indice]
					]
				except KeyError:
					pass
			elif zócalo.Zocaloconexiones:
				indexador = self.obtener_multiples_datos(zócalo.indice)
				self.valores[self.diccionarios['Entradas'][zócalo.indice]] = []
				listado = self.valores[self.diccionarios['Entradas'][zócalo.indice]]
				for elemento in indexador:
					contranodo = elemento['nodo']
					contrazócalo = elemento['zócalo']
					try:
						valor = contranodo.valores[contranodo.diccionarios['Salidas'][contrazócalo.indice]]
						listado.append(valor)
					except KeyError:
						listado.append('Dato perdido por error de sistema')
			else:
				for elemento in self.contenido.contenido_de_entradas:
					try:
						if elemento.llave == self.diccionarios['Entradas'][zócalo.indice]:
							elemento.contenido()
							break
					except KeyError:
						pass

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
		
	def obtener_multiples_datos(self, indice=0):
		contrazócalos = []
		for conexion in self.entradas[indice].Zocaloconexiones:
			otro_zocalo = conexion.obtener_otros_zocalos(self.entradas[indice])
			contrazócalos.append(
				{'nodo': otro_zocalo.nodo,
     			'zócalo': otro_zocalo
				}
			)
		return contrazócalos

	def ajustes_preevaluación(self):
		pass

	def métodos_de_evaluación(self):
		pass

	def tooltips_de_los_zocalos(self):
		no_evaluado = 'El valor del zócalo aún no ha sido calculado.'
		error_de_cálculo = 'Error de cálculo.'

		zócalos = self.entradas + self.salidas
		cantidad_de_conexiones = 0

		self.valores_postevaluación = self.valores.copy()

		for llave in self.valores_preevaluación:
			self.valores_preevaluación[llave] = tratado_de_datos(self.valores_preevaluación[llave], True)

		for llave in self.valores_postevaluación:
			self.valores_postevaluación[llave] = tratado_de_datos(self.valores_postevaluación[llave], True)

		for zócalo in zócalos:
			if len(zócalo.Zocaloconexiones) != 0:
				cantidad_de_conexiones += 1
				break

		# Tooltip si el nodo no está conectado a nada.
		if cantidad_de_conexiones == 0:
			for zócalo in zócalos:
				zócalo.GraficosZocalos.setToolTip(no_evaluado)
		else:
			for zócalo in self.salidas:
				if zócalo.GraficosZocalos.isVisible():
					# En caso un cálculo de la evaluación de None, cosa que solo pasaría si se me pasa (espero),
					# el tooltip me avisará.
					if zócalo.Zocaloconexiones and self.valores[self.diccionarios['Salidas'][zócalo.indice]] is None:
						zócalo.GraficosZocalos.setToolTip(error_de_cálculo)
						self.errores_graves += 1

					# Seteo del tooltip solo en caso esté conectado el zócalo.
					elif zócalo.Zocaloconexiones and self.valores[self.diccionarios['Salidas'][zócalo.indice]] is not None:
						zócalo.GraficosZocalos.setToolTip(
								self.valores_postevaluación[self.diccionarios['Salidas'][zócalo.indice]]
								)
					else:
						zócalo.GraficosZocalos.setToolTip(no_evaluado)


			for zócalo in self.entradas:
				if zócalo.GraficosZocalos.isVisible():
					try:
						if (
								zócalo.Zocaloconexiones
								and self.valores_preevaluación[self.diccionarios['Entradas'][zócalo.indice]] is None
						):
							zócalo.GraficosZocalos.setToolTip(error_de_cálculo)
							self.errores_graves += 1

						elif zócalo.Zocaloconexiones:
							# Aquí se muestran los valores de la salida conectada. Estamos usando la lista de valores de
							# entrada.
							zócalo.GraficosZocalos.setToolTip(
									self.valores_preevaluación[self.diccionarios['Entradas'][zócalo.indice]]
									)
						else:
							if self.valores_preevaluación[self.diccionarios['Entradas'][zócalo.indice]] is not None:
								zócalo.GraficosZocalos.setToolTip(
										self.valores_preevaluación[self.diccionarios['Entradas'][zócalo.indice]]
										)
							else:
								zócalo.GraficosZocalos.setToolTip(error_de_cálculo)
								self.errores_graves += 1
					except KeyError:
						for elemento in self.contenido.contenido_de_entradas:
							if elemento.zócalo is None:
								pass
							elif isinstance(elemento, Etiqueta) and zócalo.indice == elemento.zócalo:
								zócalo.GraficosZocalos.setToolTip(tratado_de_datos(elemento.valor_recibido, True))
								break
							elif zócalo.indice == elemento.zócalo:
								zócalo.GraficosZocalos.setToolTip('El elemento asignado a la entrada %s (%s) le falta llave o se le asignó este'
									      ' zócalo por error.' % (zócalo.indice + 1, elemento.__class__.__name__))
								if DEBUG:
									print('El elemento asignado a la entrada %s (%s) le falta llave o se le asignó este'
									      ' zócalo por error.' % (zócalo.indice + 1, elemento.__class__.__name__))
								break

	def serialización(self):
		res = super().serialización()
		res['Código'] = self.__class__.codigo_op
		return res

	def deserialización(self, data, hashmap = {}, restaure_id = True, *args, **kwargs):
		try:
			if restaure_id: self.id = data['ID']
			hashmap[data['ID']] = self

			self.definir_posición(data['Posición X'], data['Posición Y'])
			self.titulo = data['Título']

			data['Entradas'].sort(key = lambda Zocalo: Zocalo['Índice'] + Zocalo['Posición'] * 10000)
			data['Salidas'].sort(key = lambda Zocalo: Zocalo['Índice'] + Zocalo['Posición'] * 10000)
			num_entradas = len(data['Entradas'])
			num_salidas = len(data['Salidas'])

			# Una forma de hacer esto es borrar los zocalos existentes. Pero cuando lo hacemos, la deserialización
			# debe ser reescrita por cada uno de los zocalos que se definan en el constructor de un nodo...
			# La segunda forma de hacerlo es reusar los zocalos existentes, así no se crean nuevos si no es necesario.

			for Zocalo_data in data['Entradas']:
				# Forma 1: Borrar y crear nuevos nodos.
				# nuevo_zocalo = self.__class__.ClasedeZocalo(nodo=self, indice=Zocalo_data['Índice'],
				#											posicion=Zocalo_data['Posición'],
				#											tipo_zocalo=Zocalo_data['Tipo de zócalo'],
				#											cantidad_en_el_lado_actual=num_entradas, es_entrada=True)
				# nuevo_zocalo.deserialización(Zocalo_data, hashmap, restaure_id)
				# self.entradas.append(nuevo_zocalo)

				# Forma 2: Usar los zocalos existentes y crear los faltantes.
				encontrado = None
				for zocalo in self.entradas:
					if zocalo.indice == Zocalo_data['Índice']:
						encontrado = zocalo
						break
				if encontrado is None:
					encontrado = self.__class__.ClasedeZocalo(
						nodo = self, indice = Zocalo_data['Índice'],
						posicion = Zocalo_data['Posición'],
						tipo_zocalo = Zocalo_data['Tipo de zócalo'],
						cantidad_en_el_lado_actual = num_entradas, es_entrada = True, forma = Zocalo_data['Forma']
						)
					self.entradas.append(encontrado)
				encontrado.deserialización(Zocalo_data, hashmap, restaure_id)

			for Zocalo_data in data['Salidas']:
				# Forma 1: Borrar y crear nuevos nodos.
				# nuevo_zocalo = self.__class__.ClasedeZocalo(nodo=self, indice=Zocalo_data['Índice'],
				#											posicion=Zocalo_data['Posición'],
				#											tipo_zocalo=Zocalo_data['Tipo de zócalo'],
				#											cantidad_en_el_lado_actual=num_salidas, es_entrada=False)
				# nuevo_zocalo.deserialización(Zocalo_data, hashmap, restaure_id)
				# self.salidas.append(nuevo_zocalo)

				# Forma 2: Usar los zocalos existentes y crear los faltantes.
				encontrado = None
				for zocalo in self.salidas:
					if zocalo.indice == Zocalo_data['Índice']:
						encontrado = zocalo
						break
				if encontrado is None:
					encontrado = self.__class__.ClasedeZocalo(
						nodo = self, indice = Zocalo_data['Índice'],
						posicion = Zocalo_data['Posición'],
						tipo_zocalo = Zocalo_data['Tipo de zócalo'],
						cantidad_en_el_lado_actual = num_salidas, es_entrada = False, forma = Zocalo_data['Forma']
						)
					self.salidas.append(encontrado)
				encontrado.deserialización(Zocalo_data, hashmap, restaure_id)
		except Exception as e: dump_exception(e)

		# También deserializa el contenido del nodo.
		if isinstance(self.contenido, Serializable):
			res = self.contenido.deserialización(data['Contenido'], hashmap)
			return res

		return True
