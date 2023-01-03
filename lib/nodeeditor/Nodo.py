from collections import OrderedDict
from lib.nodeeditor.Seriabilizador import Serializable
from lib.nodeeditor.GraficosdelNodo import GraficosdelNodo
from lib.nodeeditor.ContenidodelNodo import ContenidoDelNodo
from lib.nodeeditor.Zocalos import Zocalo, IZQUIERDA_ARRIBA, IZQUIERDA_CENTRO, IZQUIERDA_ABAJO, DERECHA_ARRIBA, \
	DERECHA_CENTRO, DERECHA_ABAJO
from lib.nodeeditor.Utilidades import dump_exception

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
		
		self.init_clases_internas()
		self.init_configuraciones()
		
		self.titulo = titulo
		
		self.escena.agregar_nodo(self)
		self.escena.graficador_de_la_escena.addItem(self.Nodograficas)

		# Creación de conectores para entradas y salidas de nodos.
		self.entradas = []
		self.salidas = []
		self.init_zocalos(entradas, salidas)
		
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
	
	def definir_posición(self, x, y):
		self.Nodograficas.setPos(x, y)
	
	def init_clases_internas(self):
		clase_nodo_contenido = self.obtener_clase_de_contenido()
		clase_nodo_graficos = self.obtener_clase_de_graficos_de_nodo()
		if clase_nodo_contenido is not None: self.contenido = clase_nodo_contenido(self)
		if clase_nodo_graficos is not None: self.Nodograficas = clase_nodo_graficos(self)
	
	def obtener_clase_de_contenido(self):
		return self.__class__.ClasedelContenidodeNodo
	
	def obtener_clase_de_graficos_de_nodo(self):
		return self.__class__.ClaseGraficadeNodo
	
	def init_configuraciones(self):
		self.espaciadoconectores = 22
		
		self.pos_det_entradas = IZQUIERDA_ABAJO
		self.pos_det_salidas = DERECHA_ARRIBA
		self.entradas_multiconexion = False
		self.salidas_multiconexion = True
		self.zocalos_offsets = {
			IZQUIERDA_ARRIBA: -1,
			IZQUIERDA_CENTRO: -1,
			IZQUIERDA_ABAJO : -1,
			DERECHA_ARRIBA  : 1,
			DERECHA_CENTRO  : 1,
			DERECHA_ABAJO   : 1,
		}
	
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
			zocalo = self.__class__.ClasedeZocalo(nodo=self, indice=contador, posicion=self.pos_det_entradas,
												  tipo_zocalo=objeto, multiconexión=self.entradas_multiconexion,
												  cantidad_en_el_lado_actual=len(entradas), es_entrada=True
												  )
			contador += 1
			self.entradas.append(zocalo)
		
		contador = 0
		for objeto in salidas:
			zocalo = self.__class__.ClasedeZocalo(nodo=self, indice=contador, posicion=self.pos_det_salidas,
												  tipo_zocalo=objeto, multiconexión=self.salidas_multiconexion,
												  cantidad_en_el_lado_actual=len(salidas), es_entrada=False
												  )
			contador += 1
			self.salidas.append(zocalo)

	def datos_de_conexion_cambiados(self, conexion):
		pass
		
	def datos_de_entrada_cambiados(self, conexion):
		self.marcar_indefinido()
		self.marcar_descendencia_indefinido()
		
	def al_deserializar(self, data):
		pass
	
	def doble_cliqueo(self, event):
		pass
		
	def hacer_selección(self, nuevo_estado=True):
		self.Nodograficas.hacer_selección(nuevo_estado)
	
	def está_seleccionado(self):
		return self.Nodograficas.isSelected()
			
	def obtener_posicion_zocalo(self, indice, posicion, num_out_of=1):
		x = self.zocalos_offsets[posicion] if (posicion in (IZQUIERDA_ARRIBA, IZQUIERDA_CENTRO, IZQUIERDA_ABAJO)) else self.Nodograficas.anchura_del_nodo + self.zocalos_offsets[posicion]
		
		if posicion in (IZQUIERDA_ABAJO, DERECHA_ABAJO):
			# Comenzando desde abajo.
			y = self.Nodograficas.altura_del_nodo - self.Nodograficas.redondez_del_nodo - self.Nodograficas.sangría_vertical_del_título - (indice * self.espaciadoconectores)
		elif posicion in (IZQUIERDA_CENTRO, DERECHA_CENTRO):
			no_de_zocalos = num_out_of
			altura_del_nodo = self.Nodograficas.altura_del_nodo
			altura_no_usable = self.Nodograficas.altura_del_título + 2 * self.Nodograficas.sangría_vertical_del_título + self.Nodograficas.márgen
			altura_disponible = altura_del_nodo - altura_no_usable
			
			altura_total_de_todos_los_zocalos = num_out_of * self.espaciadoconectores
			nueva_altura = altura_disponible - altura_total_de_todos_los_zocalos
			
			y = altura_no_usable + altura_disponible / 2.0 + (indice - 0.5) * self.espaciadoconectores
			if no_de_zocalos > 1:
				y -= self.espaciadoconectores * (no_de_zocalos - 1) / 2
			
		elif posicion in (IZQUIERDA_ARRIBA, DERECHA_ARRIBA):
			# Comenzando desde arriba.
			y = self.Nodograficas.altura_del_título + self.Nodograficas.sangría_vertical_del_título + self.Nodograficas.redondez_del_nodo + (indice * self.espaciadoconectores)
		else:
			# Esto nunca debe pasar.
			y = 0
		
		return [x, y]
	
	def obtener_posición_de_zocalo_en_la_escena(self, zocalo):
		pos_nodo = self.Nodograficas.pos()
		pos_zocalo = self.obtener_posicion_zocalo(zocalo.indice, zocalo.posicion, zocalo.cantidad_en_el_lado_actual)
		return pos_nodo.x() + pos_zocalo[0], pos_nodo.y() + pos_zocalo[1]
	
	def actualizar_conexiones(self):
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
		self.escena.graficador_de_la_escena.removeItem(self.Nodograficas)
		self.Nodograficas = None
		if DEBUG: print('	Quitando el nodo de la escena.')
		self.escena.eliminar_nodo(self)
		if DEBUG: print('	Todo salió bien.')
	
	# Evaluación de nodos.
	def es_indefinido(self):
		return self._es_indefinido
	
	def marcar_indefinido(self, nuevo_valor=True):
		self._es_indefinido = nuevo_valor
		if self._es_indefinido: self.sobremarcar_indefinido()
		
	def sobremarcar_indefinido(self): pass
	
	def marcar_hijo_indefinido(self, nuevo_valor=True):
		for nodo_hijo in self.obtener_nodos_hijos():
			nodo_hijo.marcar_indefinido(nuevo_valor)
			
	def marcar_descendencia_indefinido(self, nuevo_valor=True):
		for nodo_hijo in self.obtener_nodos_hijos():
			nodo_hijo.marcar_indefinido(nuevo_valor)
			nodo_hijo.marcar_descendencia_indefinido(nuevo_valor)
		
	def es_inválido(self):
		return self._es_invalido
	
	def marcar_inválido(self, nuevo_valor=True):
		self._es_invalido = nuevo_valor
		if self._es_invalido: self.sobremarcar_inválido()
		
	def sobremarcar_inválido(self): pass
	
	def marcar_hijo_inválido(self, nuevo_valor=True):
		for nodo_hijo in self.obtener_nodos_hijos():
			nodo_hijo.marcar_inválido(nuevo_valor)
	
	def marcar_descendencia_inválido(self, nuevo_valor=True):
		for nodo_hijo in self.obtener_nodos_hijos():
			nodo_hijo.marcar_inválido(nuevo_valor)
			nodo_hijo.marcar_descendencia_inválido(nuevo_valor)
	
	def evaluación(self, indice=0):
		self.marcar_indefinido(False)
		self.marcar_inválido(False)
		return 0
	
	def evaluar_hijos(self):
		for nodo in self.obtener_nodos_hijos():
			nodo.evaluación()
	
	# Funciones que pasan a través de los nodos.
	def obtener_nodos_hijos(self):
		# original: if self.salidas == []: return []
		if not self.salidas: return []
		lista_de_nodos_hijos = []
		for ix in range(len(self.salidas)):
			for conexion in self.salidas[ix].Zocaloconexiones:
				nodo_hijo = conexion.obtener_otros_zocalos(self.salidas[0]).nodo
				lista_de_nodos_hijos.append(nodo_hijo)
		return lista_de_nodos_hijos
	
	def obtener_entrada(self, indice=0):
		try:
			zocalo_entrada = self.entradas[indice]
			if len(zocalo_entrada.Zocaloconexiones) == 0: return None
			conexion_conectada = zocalo_entrada.Zocaloconexiones[0]
			contrazocalo = conexion_conectada.obtener_otros_zocalos(self.entradas[indice])
			return contrazocalo.nodo
		except Exception as e:
			dump_exception(e)
			return None
		
	def obtener_multiples_entradas(self, indice=0):
		entradas = []
		for conexion in self.entradas[indice].Zocaloconexiones:
			otro_zocalo = conexion.obtener_otros_zocalos(self.entradas[indice])
			entradas.append(otro_zocalo.nodo)
		return entradas
	
	def obtener_multiples_salidas(self, indice=0):
		salidas = []
		for conexion in self.salidas[indice].Zocaloconexiones:
			otro_zocalo = conexion.obtener_otros_zocalos(self.salidas[indice])
			salidas.append(otro_zocalo.nodo)
		return salidas
	
	# Funciones de serialización.
	def serialización(self):
		entradas, salidas = [], []
		for zocalo in self.entradas: entradas.append(zocalo.serialización())
		for zocalo in self.salidas: salidas.append(zocalo.serialización())
		serializado_del_contenido = self.contenido.serialización() if isinstance(self.contenido, Serializable) else {}
		return OrderedDict([
			('ID', self.id),
			('Título', self.titulo),
			('Posición X', self.Nodograficas.scenePos().x()),
			('Posición Y', self.Nodograficas.scenePos().y()),
			('Entradas', entradas),
			('Salidas', salidas),
			('Contenido', serializado_del_contenido),
		])
	
	def deserialización(self, data, hashmap={}, restaure_id=True, *args, **kwargs):
		try:
			if restaure_id: self.id = data['ID']
			hashmap[data['ID']] = self
			
			self.definir_posición(data['Posición X'], data['Posición Y'])
			self.titulo = data['Título']
			
			data['Entradas'].sort(key=lambda Zocalo: Zocalo['Índice'] + Zocalo['Posición'] * 10000)
			data['Salidas'].sort(key=lambda Zocalo: Zocalo['Índice'] + Zocalo['Posición'] * 10000)
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
					encontrado = self.__class__.ClasedeZocalo(nodo=self, indice=Zocalo_data['Índice'],
															  posicion=Zocalo_data['Posición'],
															  tipo_zocalo=Zocalo_data['Tipo de zócalo'],
															  cantidad_en_el_lado_actual=num_entradas, es_entrada=True)
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
					encontrado = self.__class__.ClasedeZocalo(nodo=self, indice=Zocalo_data['Índice'],
															  posicion=Zocalo_data['Posición'],
															  tipo_zocalo=Zocalo_data['Tipo de zócalo'],
															  cantidad_en_el_lado_actual=num_salidas, es_entrada=False)
					self.salidas.append(encontrado)
				encontrado.deserialización(Zocalo_data, hashmap, restaure_id)
		except Exception as e: dump_exception(e)
		
		# También deserializa el contenido del nodo.
		if isinstance(self.contenido, Serializable):
			res = self.contenido.deserialización(data['Contenido'], hashmap)
			return res

		return True
	