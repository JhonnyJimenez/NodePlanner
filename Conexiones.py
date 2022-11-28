from collections import OrderedDict
from Seriabilizador import Serializable
from GraficosdeConexion import *

recta = 1
bezier = 2

DEBUG = False
DEBUGZOCALOS = DEBUG

class Conexion(Serializable):
	def __init__(self, escena, zocalo_origen=None, zocalo_final=None, tipo_de_conexion=bezier):
		super().__init__()
		self.escena = escena
		
		self.zocalo_origen = zocalo_origen
		self.zocalo_final = zocalo_final
		self.tipo_de_conexion = tipo_de_conexion
		
		self.escena.agregarconexion(self)
	
	def __str__(self):
		return "<Conexion %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
	
	@property
	def zocalo_origen(self): return self._zocalo_origen
	
	@zocalo_origen.setter
	def zocalo_origen(self, value):
		self._zocalo_origen = value
		if self.zocalo_origen is not None:
			self.zocalo_origen.conexion = self
			
	@property
	def zocalo_final(self): return self._zocalo_final
	
	@zocalo_final.setter
	def zocalo_final(self, value):
		self._zocalo_final = value
		if self.zocalo_final is not None:
			self.zocalo_final.conexion = self
			
	@property
	def tipo_de_conexion(self): return self._tipo_de_conexion
	
	@tipo_de_conexion.setter
	def tipo_de_conexion(self, value):
		if hasattr(self, 'GraficosDeConexion') and self.GraficosDeConexion is not None:
			self.escena.GraficosEsc.removeItem(self.GraficosDeConexion)
		
		self._tipo_de_conexion = value
		if self.tipo_de_conexion == recta:
			self.GraficosDeConexion = ConexionLRecta(self)
		elif self.tipo_de_conexion == bezier:
			self.GraficosDeConexion = ConexionLBezier(self)
		else:
			self.GraficosDeConexion = ConexionLBezier(self)
			
		self.escena.GraficosEsc.addItem(self.GraficosDeConexion)
		
		if self.zocalo_origen is not None:
			self.posiciones_actualizadas()
	
	def posiciones_actualizadas(self):
		posicion_base = self.zocalo_origen.posicion_zocalo()
		posicion_base[0] += self.zocalo_origen.nodo.Nodograficas.pos().x()
		posicion_base[1] += self.zocalo_origen.nodo.Nodograficas.pos().y()
		self.GraficosDeConexion.punto_origen(*posicion_base)
		if self.zocalo_final is not None:
			posicion_final = self.zocalo_final.posicion_zocalo()
			posicion_final[0] += self.zocalo_final.nodo.Nodograficas.pos().x()
			posicion_final[1] += self.zocalo_final.nodo.Nodograficas.pos().y()
			self.GraficosDeConexion.punto_destino(*posicion_final)
		else:
			self.GraficosDeConexion.punto_destino(*posicion_base)
			
		if DEBUGZOCALOS:
			print(" Origen:", self.zocalo_origen)
			print(" Final:", self.zocalo_final)
			
		self.GraficosDeConexion.update()
	
	def quitar_de_zocalos(self):
		if self.zocalo_origen is not None:
			self.zocalo_origen.conexion = None
		if self.zocalo_final is not None:
			self.zocalo_final.conexion = None
		self.zocalo_final = None
		self.zocalo_origen = None
		
	def quitar(self):
		if DEBUG: print('@ Quitando la conexión', self)
		if DEBUG: print('	Quitando conexiones de todos los zócalos.')
		self.quitar_de_zocalos()
		if DEBUG: print('	Quitando los gráficos de las conexiones.')
		self.escena.GraficosEsc.removeItem(self.GraficosDeConexion)
		self.GraficosDeConexion = None
		if DEBUG: print('	Quitando conexiones de la escena.')
		try:
			self.escena.eliminarconexion(self)
		except ValueError:
			pass
		if DEBUG: print('	Todo salió bien.')
	
	def serializacion(self):
		return OrderedDict([
			('id', self.id),
			('Tipo_de_conexion', self.tipo_de_conexion),
			('Zocalo_de_origen', self.zocalo_origen.id),
			('Zocalo_de_destino', self.zocalo_final.id),
		])
	
	def deserializacion(self, data, hashmap={}, restaure_id=True):
		if restaure_id: self.id = data['id']
		self.zocalo_origen = hashmap[data['Zocalo_de_origen']]
		self.zocalo_final = hashmap[data['Zocalo_de_destino']]
		self.tipo_de_conexion = data['Tipo_de_conexion']