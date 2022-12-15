import math
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainterPath


Conexion_CP_Redondez = 100

class GraficosdeLineaBasedeConexion:
	def __init__(self, owner):
		self.owner = owner
		
	def calculo_de_ruta(self):
		return None

class EnrutadorRecto(GraficosdeLineaBasedeConexion):
	def calculo_de_ruta(self):
		ruta = QPainterPath(QPointF(self.owner.posicion_origen[0], self.owner.posicion_origen[1]))
		ruta.lineTo(self.owner.posicion_destino[0], self.owner.posicion_destino[1])
		return ruta


class EnrutadorBezier(GraficosdeLineaBasedeConexion):
	def calculo_de_ruta(self):
		o = self.owner.posicion_origen
		d = self.owner.posicion_destino
		dist = (d[0] - o[0]) * 0.5
		
		cpx_o = +dist
		cpx_d = -dist
		cpy_o = 0
		cpy_d = 0
		
		if self.owner.linea.zocalo_origen is not None:
			zoc_ini = self.owner.linea.zocalo_origen.esEntrada
			zoc_fin = self.owner.linea.zocalo_origen.esSalida
			
			if (o[0] > d[0] and zoc_fin) or (o[0] < d[0] and zoc_ini):
				cpx_d *= -1
				cpx_o *= -1
				
				cpy_d = (
								(o[1] - d[1]) / math.fabs(
							(o[1] - d[1]) if (o[1] - d[1]) != 0 else 0.00001
						)
						) * Conexion_CP_Redondez
				cpy_o = (
								(d[1] - o[1]) / math.fabs(
							(d[1] - o[1]) if (d[1] - o[1]) != 0 else 0.00001
						)
						) * Conexion_CP_Redondez
		
		ruta = QPainterPath(QPointF(self.owner.posicion_origen[0], self.owner.posicion_origen[1]))
		ruta.cubicTo(o[0] + cpx_o, o[1] + cpy_o, d[0] + cpx_d, d[1] + cpy_d, self.owner.posicion_destino[0],
					 self.owner.posicion_destino[1])
		return ruta
