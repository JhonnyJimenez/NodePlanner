from GraficosdeConexion import *

conexion_recta = 1
conexion_bezier = 2

class Conexion:
	def __init__(self, escena, conector_origen, conector_final, tipo=conexion_recta):
		
		self.escena = escena
		
		self.conector_origen = conector_origen
		self.conector_final = conector_final
		
		self.GraficosDeConexion = ConexionLRecta(self) if tipo==conexion_recta else ConexionLBezier(self)
		
		self.escena.GraficosEsc.addItem(self.GraficosDeConexion)
	