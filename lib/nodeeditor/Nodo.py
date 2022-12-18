from collections import OrderedDict
from lib.nodeeditor.Seriabilizador import Serializable
from lib.nodeeditor.GraficosdelNodo import GraficosdelNodo
from lib.nodeeditor.ContenidodelNodo import ContenidoDelNodo
from lib.nodeeditor.Zocalos import *
from lib.nodeeditor.Utilidades import dump_exception, pp

DEBUG = False


class Nodo(Serializable):
	ClaseGraficadeNodo = GraficosdelNodo
	ClasedelContenidodeNodo = ContenidoDelNodo
	ClasedeZocalo = Zocalo
	
	def __init__(self, escena, titulo="Nodo desconocido", entradas=[], salidas=[]):
		super().__init__()
		self._titulo = titulo
		self.escena = escena
		
		# Por si las moscas.
		self.contenido = None
		self.Nodograficas = None
		
		self.initClasesInternas()
		self.initConfiguraciones()
		
		self.titulo = titulo
		
		self.escena.agregarnodo(self)
		self.escena.GraficosEsc.addItem(self.Nodograficas)
		
		# Creación de conectores para entradas y salidas de nodos.
		self.entradas = []
		self.salidas = []
		self.initZocalos(entradas, salidas)
		
		# Cosas de evaluación.
		self._es_indefinido = False
		self._es_invalido = False
	
	def __str__(self):
		return "<%s:%s %s..%s>" % (self.titulo, self.__class__.__name__, hex(id(self))[2:5], hex(id(self))[-3:])
	
	@property
	def titulo(self):
		return self._titulo
	
	@titulo.setter
	def titulo(self, valor):
		self._titulo = valor
		self.Nodograficas.nombre = self._titulo
	
	@property
	def pos(self):
		return self.Nodograficas.pos()  # QPoint
	
	def definirposicion(self, x, y):
		self.Nodograficas.setPos(x, y)
	
	def initClasesInternas(self):
		clase_nodo_contenido = self.obtenerClasedeContenido()
		clase_nodo_graficos = self.obtenerClasedeGraficosdeNodo()
		if clase_nodo_contenido is not None: self.contenido = clase_nodo_contenido(self)
		if clase_nodo_graficos is not None: self.Nodograficas = clase_nodo_graficos(self)
	
	def obtenerClasedeContenido(self):
		return self.__class__.ClasedelContenidodeNodo
	
	def obtenerClasedeGraficosdeNodo(self):
		return self.__class__.ClaseGraficadeNodo
	
	def initConfiguraciones(self):
		self.espaciadoconectores = 22
		
		self.pos_det_entradas = Izquierda_abajo
		self.pos_det_salidas = Derecha_arriba
		self.entradas_multiconexion = False
		self.salidas_multiconexion = True
		self.zocalos_offsets = {
			Izquierda_arriba: -1,
			Izquierda_centro: -1,
			Izquierda_abajo: -1,
			Derecha_arriba: 1,
			Derecha_centro: 1,
			Derecha_abajo: 1,
		}
	
	def initZocalos(self, entradas, salidas, reset=True):
		# Creación de zócalos para las entradas y salidas.
		
		if reset:
			# Limpiar los zócalos viejos.
			if hasattr(self, 'entradas') and hasattr(self, 'salidas'):
				# Quitar zócalos de la escena.
				for zocalo in (self.entradas + self.salidas):
					self.escena.GraficosEsc.removeItem(zocalo.GraficosZocalos)
				self.entradas = []
				self.salidas = []
				
		# Creación de los nuevos zócalos.
		contador = 0
		for objeto in entradas:
			zocalo = self.__class__.ClasedeZocalo(nodo=self, indice=contador, posicion=self.pos_det_entradas,
												  tipo_zocalo=objeto, multiconexion=self.entradas_multiconexion,
												  cantidad_en_el_lado_actual=len(entradas), esEntrada=True
												  )
			contador += 1
			self.entradas.append(zocalo)
		
		contador = 0
		for objeto in salidas:
			zocalo = self.__class__.ClasedeZocalo(nodo=self, indice=contador, posicion=self.pos_det_salidas,
												  tipo_zocalo=objeto, multiconexion=self.salidas_multiconexion,
												  cantidad_en_el_lado_actual=len(salidas), esEntrada=False
												  )
			contador += 1
			self.salidas.append(zocalo)

	def DatosdeConexionCambiados(self, conexion):
		pass
		
	def DatosdeEntradaCambiados(self, conexion):
		self.marcarIndefinido()
		self.marcarDescendenciaIndefinido()
		
	def AlDeserializar(self, data):
		pass
	
	def DobleCliqueo(self, event):
		pass
		
	def hacerSeleccion(self, nuevo_estado=True):
		self.Nodograficas.hacerSeleccion(nuevo_estado)
	
	def estaSeleccionado(self):
		return self.Nodograficas.isSelected()
			
	def obtener_posicion_zocalo(self, indice, posicion, num_out_of=1):
		x = self.zocalos_offsets[posicion] if (posicion in (Izquierda_arriba, Izquierda_centro, Izquierda_abajo)) else self.Nodograficas.anchoNodo + self.zocalos_offsets[posicion]
		
		if posicion in (Izquierda_abajo, Derecha_abajo):
			# Comenzando desde abajo.
			y = self.Nodograficas.altoNodo - self.Nodograficas.redondezdelaOrilladelNodo - self.Nodograficas.sangria_vertical_del_titulo - (indice * self.espaciadoconectores)
		elif posicion in (Izquierda_centro, Derecha_centro):
			no_de_zocalos = num_out_of
			altura_del_nodo = self.Nodograficas.altoNodo
			altura_no_usable = self.Nodograficas.alturaTituloNodo + 2 * self.Nodograficas.sangria_vertical_del_titulo + self.Nodograficas.sangria_de_la_orilla
			altura_disponible = altura_del_nodo - altura_no_usable
			
			altura_total_de_todos_los_zocalos = num_out_of * self.espaciadoconectores
			nueva_altura = altura_disponible - altura_total_de_todos_los_zocalos
			
			y = altura_no_usable + altura_disponible / 2.0 + (indice - 0.5) * self.espaciadoconectores
			if no_de_zocalos > 1:
				y -= self.espaciadoconectores * (no_de_zocalos - 1) / 2
			
		elif posicion in (Izquierda_arriba, Derecha_arriba):
			# Comenzando desde arriba.
			y = self.Nodograficas.alturaTituloNodo + self.Nodograficas.sangria_vertical_del_titulo + self.Nodograficas.redondezdelaOrilladelNodo + (indice * self.espaciadoconectores)
		else:
			# Esto nunca debe pasar.
			y = 0
		
		return [x, y]
	
	def obtenerPosiciondeZocaloenEscena(self, zocalo):
		pos_nodo = self.Nodograficas.pos()
		pos_zocalo = self.obtener_posicion_zocalo(zocalo.indice, zocalo.posicion, zocalo.cantidad_en_el_lado_actual)
		return (pos_nodo.x() + pos_zocalo[0], pos_nodo.y() + pos_zocalo[1])
	
	def actualizarconexiones(self):
		for zocalo in self.entradas + self.salidas:
			# if zocalo.tieneconexiones():
			for conexion in zocalo.Zocaloconexiones:
				conexion.posiciones_actualizadas()
				
	def quitar(self):
		if DEBUG: print('> Quitando el nodo', self)
		if DEBUG: print('	Quitando todos las conexiones de los zócalos.')
		for zocalo in (self.entradas + self.salidas):
			# zocalo.quitar_todas_las_conexiones(silencioso=True)
			# if zocalo.tieneconexiones():
			for conexion in zocalo.Zocaloconexiones.copy():
				if DEBUG: print('		Quitando', conexion, 'del', zocalo)
				conexion.quitar()
		if DEBUG: print('	Quitando los gráficos del nodo.')
		self.escena.GraficosEsc.removeItem(self.Nodograficas)
		self.Nodograficas = None
		if DEBUG: print('	Quitando el nodo de la escena.')
		self.escena.eliminarnodo(self)
		if DEBUG: print('	Todo salió bien.')
	
	# Evaluación de nodos.
	def esIndefinido(self):
		return self._es_indefinido
	
	def marcarIndefinido(self, nuevo_valor=True):
		self._es_indefinido = nuevo_valor
		if self._es_indefinido: self.sobremarcarIndefinido()
		
	def sobremarcarIndefinido(self): pass
	
	def marcarHijoIndefinido(self, nuevo_valor=True):
		for nodo_hijo in self.obtenerNodosHijos():
			nodo_hijo.marcarIndefinido(nuevo_valor)
			
	def marcarDescendenciaIndefinido(self, nuevo_valor=True):
		for nodo_hijo in self.obtenerNodosHijos():
			nodo_hijo.marcarIndefinido(nuevo_valor)
			nodo_hijo.marcarDescendenciaIndefinido(nuevo_valor)
		
	def esInvalido(self):
		return self._es_invalido
	
	def marcarInvalido(self, nuevo_valor=True):
		self._es_invalido = nuevo_valor
		if self._es_invalido: self.sobremarcarInvalido()
		
	def sobremarcarInvalido(self): pass
	
	def marcarHijoInvalido(self, nuevo_valor=True):
		for nodo_hijo in self.obtenerNodosHijos():
			nodo_hijo.marcarInvalido(nuevo_valor)
	
	def marcarDescendenciaInvalido(self, nuevo_valor=True):
		for nodo_hijo in self.obtenerNodosHijos():
			nodo_hijo.marcarInvalido(nuevo_valor)
			nodo_hijo.marcarDescendenciaInvalido(nuevo_valor)
	
	def evaluar(self, indice=0):
		self.marcarIndefinido(False)
		self.marcarInvalido(False)
		return 0
	
	def evaluarHijos(self):
		for nodo in self.obtenerNodosHijos():
			nodo.evaluar()
	
	# Funciones que pasan a través de los nodos.
	def obtenerNodosHijos(self):
		if self.salidas == []: return []
		lista_de_nodos_hijos = []
		for ix in range(len(self.salidas)):
			for conexion in self.salidas[ix].Zocaloconexiones:
				nodo_hijo = conexion.obtenerOtrosZocalos(self.salidas[0]).nodo
				lista_de_nodos_hijos.append(nodo_hijo)
		return lista_de_nodos_hijos
	
	def obtenerEntrada(self, indice=0):
		try:
			zocalo_entrada = self.entradas[indice]
			if len(zocalo_entrada.Zocaloconexiones) == 0: return None
			conexion_conectada = zocalo_entrada.Zocaloconexiones[0]
			contrazocalo = conexion_conectada.obtenerOtrosZocalos(self.entradas[indice])
			return contrazocalo.nodo
		except Exception as e:
			dump_exception(e)
			return None
		
	def obtenerMultiplesEntradas(self, indice=0):
		entradas = []
		for conexion in self.entradas[indice].Zocaloconexiones:
			otro_zocalo = conexion.obtenerOtrosZocalos(self.entradas[indice])
			entradas.append(otro_zocalo.nodo)
		return entradas
	
	def obtenerMultiplesSalidas(self, indice=0):
		salidas = []
		for conexion in self.salidas[indice].Zocaloconexiones:
			otro_zocalo = conexion.obtenerOtrosZocalos(self.salidas[indice])
			salidas.append(otro_zocalo.nodo)
		return salidas
	
	# Funciones de serialización.
	def serializacion(self):
		entradas, salidas = [], []
		for Zocalo in self.entradas: entradas.append(Zocalo.serializacion())
		for Zocalo in self.salidas: salidas.append(Zocalo.serializacion())
		serializado_del_contenido = self.contenido.serializacion() if isinstance(self.contenido, Serializable) else {}
		return OrderedDict([
			('id', self.id),
			('Titulo', self.titulo),
			('Pos_x', self.Nodograficas.scenePos().x()),
			('Pos_y', self.Nodograficas.scenePos().y()),
			('Entradas', entradas),
			('Salidas', salidas),
			('Contenido', serializado_del_contenido),
		])
	
	def deserializacion(self, data, hashmap={}, restaure_id=True, *args, **kwargs):
		try:
			if restaure_id: self.id = data['id']
			hashmap[data['id']] = self
			
			self.definirposicion(data['Pos_x'], data['Pos_y'])
			self.titulo = data['Titulo']
			
			data['Entradas'].sort(key=lambda Zocalo: Zocalo['Indice'] + Zocalo['Posicion'] * 10000)
			data['Salidas'].sort(key=lambda Zocalo: Zocalo['Indice'] + Zocalo['Posicion'] * 10000)
			num_entradas = len(data['Entradas'])
			num_salidas = len(data['Salidas'])
			
			# Una forma de hacer esto es borrar los zocalos existentes. Pero cuando lo hacemos, la deserialización
			# debe ser reescrita por cada uno de los zocalos que se definan en el constructor de un nodo...
			# La segunda forma de hacerlo es reusar los zocalos existentes, así no se crean nuevos si no es necesario.
			
			for Zocalo_data in data['Entradas']:
				# Forma 1: Borrar y crear nuevos nodos.
				# nuevo_zocalo = self.__class__.ClasedeZocalo(nodo=self, indice=Zocalo_data['Indice'],
				#											posicion=Zocalo_data['Posicion'],
				#											tipo_zocalo=Zocalo_data['Tipo_de_zocalo'],
				#											cantidad_en_el_lado_actual=num_entradas, esEntrada=True)
				# nuevo_zocalo.deserializacion(Zocalo_data, hashmap, restaure_id)
				# self.entradas.append(nuevo_zocalo)
				
				# Forma 2: Usar los zocalos existentes y crear los faltantes.
				encontrado = None
				for zocalo in self.entradas:
					if zocalo.indice == Zocalo_data['Indice']:
						encontrado = zocalo
						break
				if encontrado is None:
					encontrado = self.__class__.ClasedeZocalo(nodo=self, indice=Zocalo_data['Indice'],
															  posicion=Zocalo_data['Posicion'],
															  tipo_zocalo=Zocalo_data['Tipo_de_zocalo'],
															  cantidad_en_el_lado_actual=num_entradas, esEntrada=True)
					self.entradas.append(encontrado)
				encontrado.deserializacion(Zocalo_data, hashmap, restaure_id)
			
			for Zocalo_data in data['Salidas']:
				# Forma 1: Borrar y crear nuevos nodos.
				# nuevo_zocalo = self.__class__.ClasedeZocalo(nodo=self, indice=Zocalo_data['Indice'],
				#											posicion=Zocalo_data['Posicion'],
				#											tipo_zocalo=Zocalo_data['Tipo_de_zocalo'],
				#											cantidad_en_el_lado_actual=num_salidas, esEntrada=False)
				# nuevo_zocalo.deserializacion(Zocalo_data, hashmap, restaure_id)
				# self.salidas.append(nuevo_zocalo)
				
				# Forma 2: Usar los zocalos existentes y crear los faltantes.
				encontrado = None
				for zocalo in self.salidas:
					if zocalo.indice == Zocalo_data['Indice']:
						encontrado = zocalo
						break
				if encontrado is None:
					encontrado = self.__class__.ClasedeZocalo(nodo=self, indice=Zocalo_data['Indice'],
															  posicion=Zocalo_data['Posicion'],
															  tipo_zocalo=Zocalo_data['Tipo_de_zocalo'],
															  cantidad_en_el_lado_actual=num_salidas, esEntrada=False)
					self.salidas.append(encontrado)
				encontrado.deserializacion(Zocalo_data, hashmap, restaure_id)
		except Exception as e: dump_exception(e)
		
		# También deserializa el contenido del nodo.
		if isinstance(self.contenido, Serializable):
			res = self.contenido.deserializacion(data['Contenido'], hashmap)
			return res

		return True
	