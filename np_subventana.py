from PyQt5.QtWidgets import QAction, QMenu, QGraphicsProxyWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QDataStream, QIODevice, Qt

from lib.nodeeditor.Widget_de_nodos import EditordeNodos
from lib.nodeeditor.Utilidades import dump_exception
from lib.nodeeditor.Conexiones import bezier, recta
from lib.nodeeditor.GraficosVista import MODO_DIBUJO

from np_idioma import *
from np_enlistado_de_nodos import *
from nodos.categorías.salidas import Salidas

DEBUG = False
DEBUG_CONTEXT = False


class NodePlannerSubVentana(EditordeNodos):
	def __init__(self):
		super().__init__()
		# self.setAttribute(Qt.WA_DeleteOnClose)

		self.definir_título()

		self.init_nueva_opción_de_nodo()

		self.escena.agregar_elementos_modificados_listener(self.definir_título)
		self.escena.historial.agregar_restaurado_del_historial_listeners(self.al_restaurar_historial)
		self.escena.agregar_dragenter_listener(self.arrastrar)
		self.escena.agregar_drop_listener(self.soltar)
		self.escena.definir_selector_de_clases_de_nodos(self.obtener_clase_del_nodo_de_datos)

		self._close_event_listeners = []

	def obtener_clase_del_nodo_de_datos(self, data):
		if 'Codigo_op' not in data:
			return None
		return obtener_clase_del_codigo_op(data['Codigo_op'])

	def hacer_evaluación_de_salidas(self):
		# Evaluar todos los nodos de salida.
		for nodo in self.escena.nodos:
			if isinstance(nodo, Salidas):
				nodo.evaluación()

	def al_restaurar_historial(self):
		self.hacer_evaluación_de_salidas()

	def leer_archivo(self, filename):
		if super().leer_archivo(filename):
			self.hacer_evaluación_de_salidas()
			return True

		return False

	def init_nueva_opción_de_nodo(self):
		self.opciones_de_nodos = {}
		keys = list(NODEPLANNER_NODOS.keys())
		keys.sort()
		for key in keys:
			nodo = NODEPLANNER_NODOS[key]
			self.opciones_de_nodos[nodo.codigo_op] = QAction(QIcon(nodo.icono), nodo.titulo_op)
			self.opciones_de_nodos[nodo.codigo_op].setData(nodo.codigo_op)

	def init_menú_contextual_de_los_nodos(self):
		menu_contextual = QMenu(self)
		keys = list(NODEPLANNER_NODOS.keys())
		keys.sort()
		for key in keys:
			menu_contextual.addAction(self.opciones_de_nodos[key])
		return menu_contextual

	def definir_título(self):
		self.setWindowTitle(self.obtener_nombre_amigable_al_usuario())

	def agregar_close_event_listeners(self, callback):
		self._close_event_listeners.append(callback)

	def closeEvent(self, event):
		for callback in self._close_event_listeners:
			callback(self, event)

	def arrastrar(self, event):
		if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
			event.acceptProposedAction()
		else:
			# print("... Arrastre de objeto denegado")
			event.setAccepted(False)

	def soltar(self, event):
		if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
			event_data = event.mimeData().data(LISTBOX_MIMETYPE)
			data_stream = QDataStream(event_data, QIODevice.ReadOnly)
			pixmap = QPixmap()
			data_stream >> pixmap
			codigo_op = data_stream.readInt()
			text = data_stream.readQString()

			mouse_pos = event.pos()
			escena_pos = self.escena.graficador_de_la_escena.views()[0].mapToScene(mouse_pos)

			if DEBUG:
				print("Objeto soltado: [%d] '%s'" % (codigo_op, text), "Mouse:", mouse_pos, "Escena:", escena_pos)

			try:
				nodo = obtener_clase_del_codigo_op(codigo_op)(self.escena)
				nodo.definir_posición(escena_pos.x(), escena_pos.y())
				self.escena.historial.almacenar_historial(
					"Creación de un nodo: %s" % nodo.__class__.__name__, set_modified = True
					)
			except Exception as e:
				dump_exception(e)

			event.setDropAction(Qt.MoveAction)
			event.accept()
		else:
			# print("El archivo soltado fue ignorado: formato requerido: %d" % LISTBOX_MIMETYPE)
			event.ignore()

	def contextMenuEvent(self, event):
		try:
			objeto = self.escena.obtener_objeto_en_la_posición(event.pos())
			if DEBUG_CONTEXT:
				print(objeto)

			if type(objeto) == QGraphicsProxyWidget:
				objeto = objeto.widget()

			if hasattr(objeto, 'nodo') or hasattr(objeto, 'zocalo'):
				self.control_menú_contextual_de_los_nodos(event)
			elif hasattr(objeto, 'linea'):
				self.control_menú_contextual_de_línea(event)
			# elif objeto is None:
			else:
				self.control_menu_contextual_del_nuevo_nodo(event)

			return super().contextMenuEvent(event)
		except Exception as e:
			dump_exception(e)

	def control_menú_contextual_de_los_nodos(self, event):
		if DEBUG_CONTEXT:
			print("Menú contextual: NODO")
		menu_contextual = QMenu(self)
		opción_indefinido = menu_contextual.addAction(MARCAR_INDEFINIDO)
		opción_descendencia_indefinido = menu_contextual.addAction(MARCAR_DESCENDENCIA_INDEFINIDO)
		opción_invalido = menu_contextual.addAction(MARCAR_INVÁLIDO)
		opción_desmarcar_inválido = menu_contextual.addAction(DESMARCAR_INVÁLIDO)
		opción_evaluado = menu_contextual.addAction(MARCAR_EVALUADO)
		acción = menu_contextual.exec_(self.mapToGlobal(event.pos()))

		seleccionado = None
		objeto = self.escena.obtener_objeto_en_la_posición(event.pos())
		if type(objeto) == QGraphicsProxyWidget:
			objeto = objeto.widget()

		if hasattr(objeto, 'nodo'):
			seleccionado = objeto.nodo
		if hasattr(objeto, 'zocalo'):
			seleccionado = objeto.zocalo.nodo

		if DEBUG_CONTEXT:
			print("Objeto obtenido:", seleccionado)
		if seleccionado and acción == opción_indefinido:
			seleccionado.marcarIndefinido()
		if seleccionado and acción == opción_descendencia_indefinido:
			seleccionado.marcarDescendenciaIndefinido()
		if seleccionado and acción == opción_invalido:
			seleccionado.marcarInvalido()
		if seleccionado and acción == opción_desmarcar_inválido:
			seleccionado.marcarInvalido(False)
		if seleccionado and acción == opción_evaluado:
			val = seleccionado.evaluar()
			if DEBUG_CONTEXT:
				print("EVALUADO:", val)

	def control_menú_contextual_de_línea(self, event):
		if DEBUG_CONTEXT:
			print("Menú contextual: LINEA")
		menu_contextual = QMenu(self)
		opción_bezier = menu_contextual.addAction(LÍNEA_BEZIER)
		opción_recta = menu_contextual.addAction(LÍNEA_RECTA)
		acción = menu_contextual.exec_(self.mapToGlobal(event.pos()))

		seleccionado = None
		objeto = self.escena.obtener_objeto_en_la_posición(event.pos())
		if hasattr(objeto, 'linea'):
			seleccionado = objeto.linea

		if seleccionado and acción == opción_bezier:
			seleccionado.tipo_de_conexion = bezier
		if seleccionado and acción == opción_recta:
			seleccionado.tipo_de_conexion = recta

	# Funciones de apoyo.
	def definir_zocalo_objetivo_en_el_nodo(self, flag_ya_dibujado, nuevo_calcnodo):
		zocalo_objetivo = None
		if flag_ya_dibujado:
			if len(nuevo_calcnodo.entradas) > 0:
				zocalo_objetivo = nuevo_calcnodo.entradas[0]
		else:
			if len(nuevo_calcnodo.salidas) > 0:
				zocalo_objetivo = nuevo_calcnodo.salidas[0]
		return zocalo_objetivo

	def finalizar_nuevo_estado_del_nodo(self, nuevo_calcnodo):
		self.escena.hacer_deseleccionar_objetos()
		nuevo_calcnodo.Nodograficas.hacer_selección()
		nuevo_calcnodo.Nodograficas.seleccionado()

	def control_menu_contextual_del_nuevo_nodo(self, event):
		if DEBUG_CONTEXT:
			print("Menú contextual: NUEVO NODO")
		menu_contextual = self.init_menú_contextual_de_los_nodos()
		accion = menu_contextual.exec_(self.mapToGlobal(event.pos()))

		if accion is not None:
			nuevo_calcnodo = obtener_clase_del_codigo_op(accion.data())(self.escena)
			pos_escena = self.escena.obtener_vista().mapToScene(event.pos())
			nuevo_calcnodo.definir_posición(pos_escena.x(), pos_escena.y())
			if DEBUG_CONTEXT:
				print("Nodo seleccionado:", nuevo_calcnodo)

			if self.escena.obtener_vista().modo == MODO_DIBUJO:
				# Cuando se dibuja una conexion:
				zocalo_objetivo = self.definir_zocalo_objetivo_en_el_nodo(
					self.escena.obtener_vista().dibujado.zocalo_inicial_de_dibujado.es_salida, nuevo_calcnodo
					)
				if zocalo_objetivo is not None:
					self.escena.obtener_vista().dibujado.finalizar_dibujado_de_conexión(zocalo_objetivo.GraficosZocalos)
				self.finalizar_nuevo_estado_del_nodo()

			else:
				self.escena.historial.almacenar_historial("Nodo %s creado" % nuevo_calcnodo.__class__.__name__)
