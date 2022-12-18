from collections import OrderedDict
from lib.nodeeditor.Seriabilizador import Serializable
from lib.nodeeditor.GraficosdeConexion import *
from lib.nodeeditor.Utilidades import dump_exception

recta = 1
bezier = 2

DEBUG = False
DEBUGZOCALOS = DEBUG


class Conexion(Serializable):
	Validantes_de_conexion = []
	
	def __init__(self, escena, zocalo_origen=None, zocalo_final=None, tipo_de_conexion=bezier):
		super().__init__()
		self.escena = escena
		
		# Ini por defecto
		self._zocalo_origen = None
		self._zocalo_final = None
		
		self.zocalo_origen = zocalo_origen
		self.zocalo_final = zocalo_final
		self._tipo_de_conexion = tipo_de_conexion
		
		# Crear instancia de Graficos de conexión.
		self.GraficosDeConexion = self.crearInstanciadeClasedeConexion()
		
		self.escena.agregarconexion(self)
	
	def __str__(self):
		return "<Conexion %s..%s -- S:%s E:%s>" % (hex(id(self))[2:5], hex(id(self))[-3:], self.zocalo_origen, self.zocalo_final)
	
	@property
	def zocalo_origen(self): return self._zocalo_origen
	
	@zocalo_origen.setter
	def zocalo_origen(self, value):
		# Si hemos asignado a algún zócalo antes, lo eliminamos de ese zócalo.
		if self._zocalo_origen is not None:
			self._zocalo_origen.quitar_conexiones(self)
		
		# Asignado de un nuevo zócalo inicial.
		self._zocalo_origen = value
		# Añadir una conexión a la clase Zócalo.
		if self.zocalo_origen is not None:
			self.zocalo_origen.agregar_conexion(self)
			
	@property
	def zocalo_final(self): return self._zocalo_final
	
	@zocalo_final.setter
	def zocalo_final(self, value):
		# Si hemos asignado a algún zócalo antes, lo eliminamos de ese zócalo.
		if self._zocalo_final is not None:
			self._zocalo_final.quitar_conexiones(self)
		
		# Asignado de un nuevo zócalo final.
		self._zocalo_final = value
		# Añadir una conexión a la clase Zócalo.
		if self.zocalo_final is not None:
			self.zocalo_final.agregar_conexion(self)
			
	@property
	def tipo_de_conexion(self):
		return self._tipo_de_conexion
	
	@tipo_de_conexion.setter
	def tipo_de_conexion(self, value):
		# Se asigna un nuevo valor.
		self._tipo_de_conexion = value
		
		# Actualizar el calculador de ruta.
		self.GraficosDeConexion.crearCalculadordeRutadeConexion()
		
		if self.zocalo_origen is not None:
			self.posiciones_actualizadas()
			
	@classmethod
	def obtenerValidantesdeConexion(cls):
		return cls.Validantes_de_conexion
	
	@classmethod
	def agregarValidantesdeConexion(cls, validator_callback):
		cls.Validantes_de_conexion.append(validator_callback)
	
	@classmethod
	def validarConexion(cls, zocalo_origen, zocalo_final):
		for validantes in cls.obtenerValidantesdeConexion():
			if not validantes(zocalo_origen, zocalo_final):
				return False
		return True
			
	def reconectar(self, del_zocalo, al_zocalo):
		if self.zocalo_origen == del_zocalo:
			self.zocalo_origen = al_zocalo
		if self.zocalo_final == del_zocalo:
			self.zocalo_final = al_zocalo
		
	def obtenerClasedeGraficosdeConexion(self):
		return GraficosdeConexion
		
	def crearInstanciadeClasedeConexion(self):
		self.GraficosDeConexion = self.obtenerClasedeGraficosdeConexion()(self)
		self.escena.GraficosEsc.addItem(self.GraficosDeConexion)
		if self.zocalo_origen is not None:
			self.posiciones_actualizadas()
		return self.GraficosDeConexion
	
	def obtenerOtrosZocalos(self, zocalo_conocido):
		return self.zocalo_origen if zocalo_conocido == self.zocalo_final else self.zocalo_final
	
	def hacerSeleccion(self, nuevo_estado=True):
		self.GraficosDeConexion.hacerSeleccion(nuevo_estado)
	
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
		# if self.zocalo_origen is not None:
			# self.zocalo_origen.quitar_conexiones(None)
		# if self.zocalo_final is not None:
			# self.zocalo_final.quitar_conexiones(None)
		self.zocalo_final = None
		self.zocalo_origen = None
		
	def quitar(self, zocalo_silenciado=None, silencioso=False):
		zocalos_antiguos = [self.zocalo_origen, self.zocalo_final]
		
		if DEBUG: print(" - Ocultando conexiones")
		self.GraficosDeConexion.hide()
		
		if DEBUG: print("	Quitando los gráficos de las conexiones.", self.GraficosDeConexion)
		self.escena.GraficosEsc.removeItem(self.GraficosDeConexion)
		if DEBUG: print("   Graficos de conexión:", self.GraficosDeConexion)
		
		self.escena.GraficosEsc.update()
		
		if DEBUG:
			print('@ Quitando la conexión', self)
			print('	Quitando conexiones de todos los zócalos.')
		self.quitar_de_zocalos()
		if DEBUG: print('	Quitando conexiones de la escena.')
		try:
			self.escena.eliminarconexion(self)
		except ValueError:
			pass
		if DEBUG: print('	Todo salió bien.')
		
		try:
			# Notificar a los nodos desde los viejos zócalos.
			for zocalo in zocalos_antiguos:
				if zocalo and zocalo.nodo:
					if silencioso:
						continue
					if zocalo_silenciado is not None and zocalo == zocalo_silenciado:
						continue
						
					# Notificar a los nodos de los zócalos.
					zocalo.nodo.DatosdeConexionCambiados(self)
					if zocalo.esEntrada: zocalo.nodo.DatosdeEntradaCambiados(zocalo)
		except Exception as e: dump_exception(e)
		
	def serializacion(self):
		return OrderedDict([
			('id', self.id),
			('Tipo_de_conexion', self.tipo_de_conexion),
			('Zocalo_de_origen', self.zocalo_origen.id if self.zocalo_origen is not None else None),
			('Zocalo_de_destino', self.zocalo_final.id if self.zocalo_final is not None else None),
		])
	
	def deserializacion(self, data, hashmap={}, restaure_id=True, *args, **kwargs):
		if restaure_id: self.id = data['id']
		self.zocalo_origen = hashmap[data['Zocalo_de_origen']]
		self.zocalo_final = hashmap[data['Zocalo_de_destino']]
		self.tipo_de_conexion = data['Tipo_de_conexion']

# Ejemplo de uso de validantes para conexiones.
# Puedes registrar (en mi codigo lo llame «agregar») los validantes que  gustes, pero...
# Sin embargo, si usas una conexion sobreescrita, tienes que llamar obtenerValidantesdeConexion en la clase sobreescrita.

from lib.nodeeditor.ValidantesdeConexion import *
# Conexion.agregarValidantesdeConexion(edge_validator_debug)
Conexion.agregarValidantesdeConexion(invalidar_conexion_de_doble_entrada_o_salida)
Conexion.agregarValidantesdeConexion(invalidar_conexiones_entre_el_mismo_nodo)
