from GraficosdeConexion import *

recta = 1
bezier = 2

DEBUG = False
DEBUGZOCALOS = False

class Conexion:
	def __init__(self, escena, zocalo_origen, zocalo_final, tipo_de_conexion=bezier):
		
		self.escena = escena
		
		self.zocalo_origen = zocalo_origen
		self.zocalo_final = zocalo_final
		
		self.zocalo_origen.conexion = self
		if self.zocalo_final is not None:
			self.zocalo_final.conexion = self
		
		self.GraficosDeConexion = ConexionLRecta(self) if tipo_de_conexion == recta else ConexionLBezier(self)
		
		self.posiciones_actualizadas()
		
		if DEBUG: print("Conexión:", self.GraficosDeConexion.posicion_origen, "a", self.GraficosDeConexion.posicion_destino)
		
		self.escena.GraficosEsc.addItem(self.GraficosDeConexion)
		self.escena.agregarconexion(self)
	
	def __str__(self):
		return "<Conexion %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
	
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
		self.quitar_de_zocalos()
		self.escena.GraficosEsc.removeItem(self.GraficosDeConexion)
		self.GraficosDeConexion = None
		self.escena.eliminarconexion(self)