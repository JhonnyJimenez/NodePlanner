from collections import OrderedDict
from nodeeditor.Seriabilizador import Serializable
from nodeeditor.GraficosdelNodo import GraficosdelNodo
from nodeeditor.ContenidodelNodo import ContenidoDelNodo
from nodeeditor.Zocalos import *


DEBUG = False


class Nodo(Serializable):
	def __init__(self, escena, titulo="Nodo desconocido", entradas=[], salidas=[]):
		super().__init__()
		self._titulo = titulo
		self.escena = escena
		
		self.contenido = ContenidoDelNodo(self)
		self.Nodograficas = GraficosdelNodo(self)
		self.titulo = titulo
		
		self.escena.agregarnodo(self)
		self.escena.GraficosEsc.addItem(self.Nodograficas)
		
		self.espaciadoconectores = 22
		
		# Creación de conectores para entradas y salidas de nodos.
		self.entradas = []
		self.salidas = []
		contador = 0
		for item in entradas:
			zocalos = Zocalo(nodo=self, indice=contador, posicion=Izquierda_abajo, tipo_zocalo=item, multiconexion=False)
			contador += 1
			self.entradas.append(zocalos)
			
		contador = 0
		for item in salidas:
			zocalos = Zocalo(nodo=self, indice=contador, posicion=Derecha_arriba, tipo_zocalo=item, multiconexion=True)
			contador += 1
			self.salidas.append(zocalos)
	
	def __str__(self):
		return "<Nodo %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
	
	@property
	def pos(self):
		return self.Nodograficas.pos()		#QPoint
	
	def definirposicion(self, x, y):
		self.Nodograficas.setPos(x, y)
	
	@property
	def titulo(self):
		return self._titulo

	@titulo.setter
	def titulo(self, valor):
		self._titulo = valor
		self.Nodograficas.nombre = self._titulo
			
	def obtener_posicion_zocalo(self, indice, posicion):
		x = 0 if (posicion in (Izquierda_arriba, Izquierda_abajo)) else self.Nodograficas.anchoNodo
		
		if posicion in (Izquierda_abajo, Derecha_abajo):
			# Comenzando desde abajo.
			y = self.Nodograficas.altoNodo - self.Nodograficas._sangria - self.Nodograficas.redondezNodo - (indice * self.espaciadoconectores)
		else:
			# Comenzando desde arriba.
			y = self.Nodograficas.alturaTituloNodo + self.Nodograficas._sangria + self.Nodograficas.redondezNodo + (indice * self.espaciadoconectores)
		
		return [x, y]
	
	def actualizarconexiones(self):
		for zocalo in self.entradas + self.salidas:
			# if zocalo.tieneconexiones():
			for conexion in zocalo.Zocaloconexiones:
				conexion.posiciones_actualizadas()
				
	def quitar(self):
		if DEBUG: print('> Quitando el nodo', self)
		if DEBUG: print('	Quitando todos las conexiones de los zócalos.')
		for zocalo in (self.entradas + self.salidas):
			# if zocalo.tieneconexiones():
			for conexion in zocalo.Zocaloconexiones:
				if DEBUG: print('		Quitando', conexion, 'del', zocalo)
				conexion.quitar()
		if DEBUG: print('	Quitando los gráficos del nodo.')
		self.escena.GraficosEsc.removeItem(self.Nodograficas)
		self.Nodograficas = None
		if DEBUG: print('	Quitando el nodo de la escena.')
		self.escena.eliminarnodo(self)
		if DEBUG: print('	Todo salió bien.')
	
	def serializacion(self):
		entradas, salidas = [], []
		for Zocalo in self.entradas: entradas.append(Zocalo.serializacion())
		for Zocalo in self.salidas: salidas.append(Zocalo.serializacion())
		return OrderedDict([
			('id', self.id),
			('Titulo', self.titulo),
			('Pos_x', self.Nodograficas.scenePos().x()),
			('Pos_y', self.Nodograficas.scenePos().y()),
			('Entradas', entradas),
			('Salidas', salidas),
			('Contenido', self.contenido.serializacion()),
		])
	
	def deserializacion(self, data, hashmap={}, restaure_id=True):
		if restaure_id: self.id = data['id']
		hashmap[data['id']] = self
		
		self.definirposicion(data['Pos_x'], data['Pos_y'])
		self.titulo =  data['Titulo']
		
		data['Entradas'].sort(key=lambda Zocalo: Zocalo['Indice'] + Zocalo['Posicion'] * 10000 )
		data['Salidas'].sort(key=lambda Zocalo: Zocalo['Indice'] + Zocalo['Posicion'] * 10000 )
		
		self.entradas = []
		for Zocalo_data in data['Entradas']:
			nuevo_zocalo = Zocalo(nodo=self, indice=Zocalo_data['Indice'], posicion=Zocalo_data['Posicion'],
								  tipo_zocalo=Zocalo_data['Tipo_de_zocalo'])
			nuevo_zocalo.deserializacion(Zocalo_data, hashmap, restaure_id)
			self.entradas.append(nuevo_zocalo)
		
		self.salidas = []
		for Zocalo_data in data['Salidas']:
			nuevo_zocalo = Zocalo(nodo=self, indice=Zocalo_data['Indice'], posicion=Zocalo_data['Posicion'],
								  tipo_zocalo=Zocalo_data['Tipo_de_zocalo'])
			nuevo_zocalo.deserializacion(Zocalo_data, hashmap, restaure_id)
			self.salidas.append(nuevo_zocalo)
			
		return True