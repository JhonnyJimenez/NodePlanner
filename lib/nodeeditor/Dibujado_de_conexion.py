from lib.nodeeditor.GraficosdeZocalos import GraficosdeZocalos
from lib.nodeeditor.Conexiones import Conexion, bezier
from lib.nodeeditor.Utilidades import dump_exception

DEBUG = False


class DibujadodeConexion:
	def __init__(self, graficos_vista):
		self.graficos_vista = graficos_vista
		# Inicializado de variables que usaremos en esta clase.
		self.dibujar_conexion = None
		self.zocalo_inicial_de_dibujado = None
		
	def obtener_clase_de_conexión(self):
		return self.graficos_vista.escena.escena.obtener_clase_de_conexión()
	
	def actualizar_destino(self, x, y):
		if self.dibujar_conexion is not None and self.dibujar_conexion.graficador_de_conexiones is not None:
			self.dibujar_conexion.graficador_de_conexiones.punto_destino(x, y)
			self.dibujar_conexion.graficador_de_conexiones.update()
		else:
			print("    Quiero actualizar self.dibujar_conexion.graficador_de_conexiones, ¡¡¡pero no hay nada!!!")
			
	def comenzar_dibujado_de_conexión(self, objeto):
		try:
			if DEBUG: print('Vista: CDibujadoConexion - Comienza a dibujar la conexión.')
			if DEBUG: print('Vista: CDibujadoConexion -  Zócalo inicial asignado a:', objeto.zocalo)
			# self.conexion_anterior = objeto.zocalo.Zocaloconexiones
			self.zocalo_inicial_de_dibujado = objeto.zocalo
			self.dibujar_conexion = self.obtener_clase_de_conexión()(objeto.zocalo.nodo.escena, objeto.zocalo, None, bezier)
			self.dibujar_conexion.graficador_de_conexiones.hacer_no_seleccionable()
			if DEBUG: print('Vista: CDibujadoConexion - Dibujado:', self.dibujar_conexion)
		except Exception as e: dump_exception(e)
	
	def finalizar_dibujado_de_conexión(self, objeto):
		# Salida rápida - si se cliquea en cualquier cosa que no sea un zocalo.
		if not isinstance(objeto, GraficosdeZocalos):
			self.graficos_vista.reiniciar_modo()
			if DEBUG: print('Vista: FDibujadoConexion - Fin rápido de dibujado')
			self.dibujar_conexion.quitar(silencioso=True)
			self.dibujar_conexion = None
		
		# Clicado en zócalo.
		if isinstance(objeto, GraficosdeZocalos):
			
			# Confirmación para una conexion válida.
			if not self.dibujar_conexion.validar_conexión(self.zocalo_inicial_de_dibujado, objeto.zocalo):
				# print("Conexion no válida")
				return False
		
			# Proceso regular de dibujado:
			# Devuelve verdadero si se salta el resto del código
			self.graficos_vista.reiniciar_modo()
		
			if DEBUG: print('Vista: FDibujadoConexion - Termina de dibujar la conexión.')
			self.dibujar_conexion.quitar(silencioso=True)
			self.dibujar_conexion = None
		
			try:
				if objeto.zocalo != self.zocalo_inicial_de_dibujado:
				# Si soltamos el dibujado sobre un zocalo distinto al de inicio
				
					# Primero quitamos las conexiones viejas y enviamos notificacion.
					for zocalo in (objeto.zocalo, self.zocalo_inicial_de_dibujado):
						if not zocalo.es_multiconexión:
							if zocalo.es_entrada:
								# print("Quitando SILENCIOSAMENTE conexiones de los zocalos de entrada (esEntrada y !esmulticonexion) [Comienza dibujado]:", objeto.zocalo.Zocaloconexiones)
								zocalo.quitar_todas_las_conexiones(silencioso=True)
							else:
								zocalo.quitar_todas_las_conexiones(silencioso=False)
				
					# Crear nuevas conexiones.
					nueva_conexion = self.obtener_clase_de_conexión()(objeto.zocalo.nodo.escena,
					                                                  self.zocalo_inicial_de_dibujado, objeto.zocalo,
					                                                  tipo_de_conexion=bezier)
					if DEBUG: print('Vista: FDibujadoConexion - Nueva conexión creada:', nueva_conexion, 'conecta',
									nueva_conexion.zocalo_origen, 'y', nueva_conexion.zocalo_final)
				
					# Manda notificaciones para la nueva conexion.
					for zocalo in [self.zocalo_inicial_de_dibujado, objeto.zocalo]:
						zocalo.nodo.datos_de_conexion_cambiados(nueva_conexion)
						# Adición mía para que el zócalo de salida también fuerce una evaluación.
						try:
							if zocalo.es_salida: zocalo.nodo.datos_de_salida_cambiados()
							# if zocalo.es_salida: zocalo.nodo.datos_de_salida_cambiados(zocalo)
						except AttributeError:
							print('Error porque el método datos de salida cambiados es una adición mía fuera del nodo'
							      ' base.')
						if zocalo.es_entrada: zocalo.nodo.datos_de_entrada_cambiados(zocalo)

					
					self.graficos_vista.escena.escena.historial.almacenar_historial("Conexion creada mediante dibujado",
					                                                                set_modified =True)
					return True
			except Exception as e: dump_exception(e)
		
		if DEBUG: print('Vista: FDibujadoConexion - Todo bien')
		return False
	