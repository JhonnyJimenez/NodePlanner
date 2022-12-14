from nodeeditor.GraficosDeZocalos import GraficosDeZocalos
from nodeeditor.Conexiones import Conexion, bezier
from nodeeditor.Utilidades import dump_exception

DEBUG = False


class DibujadodeConexion:
	def __init__(self, graficos_vista):
		self.graficos_vista = graficos_vista
		
	def obtenerClasedeConexion(self):
		return self.graficos_vista.escena.escena.obtenerClasedeConexion()
	
	def actualizarDestino(self, x, y):
		if self.dibujar_conexion is not None and self.dibujar_conexion.GraficosDeConexion is not None:
			self.dibujar_conexion.GraficosDeConexion.punto_destino(x, y)
			self.dibujar_conexion.GraficosDeConexion.update()
		else:
			print("    Quiero actualizar self.dibujar_conexion.GraficosDeConexion, ¡¡¡pero no hay nada!!!")
			
	def ComenzarDibujadoConexion(self, objeto):
		try:
			if DEBUG: print('Vista: CDibujadoConexion - Comienza a dibujar la conexión.')
			if DEBUG: print('Vista: CDibujadoConexion -  Zócalo inicial asignado a:', objeto.zocalo)
			# self.conexion_anterior = objeto.zocalo.Zocaloconexiones
			self.zocalo_inicial_de_dibujado = objeto.zocalo
			self.dibujar_conexion = self.obtenerClasedeConexion()(objeto.zocalo.nodo.escena, objeto.zocalo, None, bezier)
			self.dibujar_conexion.GraficosDeConexion.hacerNoSeleccionable()
			if DEBUG: print('Vista: CDibujadoConexion - Dibujado:', self.dibujar_conexion)
		except Exception as e: dump_exception(e)
	
	def FinalizarDibujadoConexion(self, objeto):
		# Devuelve verdadero si se salta el resto del código
		self.graficos_vista.reiniciarModo()
		
		if DEBUG: print('Vista: FDibujadoConexion - Termina de dibujar la conexión.')
		self.dibujar_conexion.quitar(silencioso=True)
		self.dibujar_conexion = None
		
		try:
			if isinstance(objeto, GraficosDeZocalos):
				if objeto.zocalo != self.zocalo_inicial_de_dibujado:
					# Si soltamos el dibujado sobre un zocalo distinto al de inicio
					
					# Primero quitamos las conexiones viejas y enviamos notificacion.
					for zocalo in (objeto.zocalo, self.zocalo_inicial_de_dibujado):
						if not zocalo.esmulticonexion:
							if zocalo.esEntrada:
								# print("Quitando SILENCIOSAMENTE conexiones de los zocalos de entrada (esEntrada y !esmulticonexion) [Comienza dibujado]:", objeto.zocalo.Zocaloconexiones)
								zocalo.quitar_todas_las_conexiones(silencioso=True)
							else:
								zocalo.quitar_todas_las_conexiones(silencioso=False)
					
					# Crear nuevas conexiones.
					nueva_conexion = self.obtenerClasedeConexion()(objeto.zocalo.nodo.escena,
																   self.zocalo_inicial_de_dibujado, objeto.zocalo,
																   tipo_de_conexion=bezier)
					if DEBUG: print('Vista: FDibujadoConexion - Nueva conexión creada:', nueva_conexion, 'conecta',
									nueva_conexion.zocalo_origen, 'y', nueva_conexion.zocalo_final)
					
					# Manda notificaciones para la nueva conexion.
					for zocalo in [self.zocalo_inicial_de_dibujado, objeto.zocalo]:
						zocalo.nodo.DatosdeConexionCambiados(nueva_conexion)
						if zocalo.esEntrada: zocalo.nodo.DatosdeEntradaCambiados(zocalo)
					
					self.graficos_vista.escena.escena.historial.almacenarHistorial("Conexion creada mediante dibujado",
																			setModified=True)
					return True
		except Exception as e: dump_exception(e)
		
		if DEBUG: print('Vista: FDibujadoConexion - Todo bien')
		return False
	