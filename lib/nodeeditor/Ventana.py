import os
import json
from PyQt5.QtWidgets import QMainWindow, QLabel, QAction, QFileDialog, QApplication
from PyQt5.QtCore import QSize, QSettings, QPoint
from lib.nodeeditor.Widget_de_nodos import EditordeNodos
from lib.nodeeditor.Utilidades import CuadroDialogo

from np_idioma import *


class Ventana(QMainWindow):
	ClaseEditordeNodos = EditordeNodos
	
	def __init__(self):
		super().__init__()
		self.init_ui()
		
#		QApplication.instance().clipboard().dataChanged.connect(self.onClipboardChange)

#	def onClipboardChange(self):
#		clip = QApplication.instance().clipboard()
#		print("Clipboard changed:", clip.text())
	
	def init_ui(self):
		self.compania = 'Blenderfreak'
		self.nombre_del_producto = 'Editor de nodos'
		
		self.crear_acciones()
		self.crear_menús()
		
		self.editor_de_nodos = self.__class__.ClaseEditordeNodos(self)
		self.editor_de_nodos.escena.agregar_elementos_modificados_listener(self.definir_título)
		self.setCentralWidget(self.editor_de_nodos)
		
		self.crear_barra_de_estado()

		# Tamaño de la ventana
		# self.setGeometry(100, 100, 800, 600)
		self.definir_título()
		self.show()
		
	def sizeHint(self):
		return QSize(800, 600)
		
	def crear_barra_de_estado(self):
		self.statusBar().showMessage("")
		self.status_mouse_pos = QLabel("")
		self.statusBar().addPermanentWidget(self.status_mouse_pos)
		self.editor_de_nodos.Vista.cambioPosEscena.connect(self.nueva_pos_de_la_escena)
		
	def crear_acciones(self):
		self.ActNuevo = QAction(
				ACT_NUEVO, self, shortcut = 'Ctrl+N', statusTip = ACT_NUEVO_DESCRIPCIÓN, triggered = self.nuevo_archivo
				)
		self.ActAbrir = QAction(
				ACT_ABRIR, self, shortcut = 'Ctrl+A', statusTip = ACT_ABRIR_DESCRIPCIÓN, triggered = self.abrir_archivo
				)
		self.ActGuardar = QAction(
				ACT_GUARDAR, self, shortcut = 'Ctrl+G', statusTip = ACT_GUARDAR_DESCRIPCIÓN,
				triggered = self.guardar_archivo
				)
		self.ActGuardarComo = QAction(
				ACT_GUARDAR_COMO, self, shortcut = 'Ctrl+Shift+G', statusTip = ACT_GUARDAR_COMO_DESCRIPCIÓN,
				triggered = self.guardar_archivo_como
				)
		self.ActSalir = QAction(
				ACT_SALIR, self, shortcut = 'Ctrl+Q', statusTip = ACT_SALIR_DESCRIPCIÓN, triggered = self.close
				)

		self.act_deshacer = QAction(
				ACT_DESHACER, self, shortcut = 'Ctrl+Z', statusTip = ACT_DESHACER_DESCRIPCIÓN,
				triggered = self.deshacer_del_menu_editar
				)
		self.ActRehacer = QAction(
				ACT_REHACER, self, shortcut = 'Ctrl+Y', statusTip = ACT_REHACER_DESCRIPCIÓN,
				triggered = self.rehacer_del_menu_editar
				)
		self.ActCortar = QAction(
				ACT_CORTAR, self, shortcut = 'Ctrl+X', statusTip = ACT_CORTAR_DESCRIPCIÓN,
				triggered = self.cortar_del_menu_editar
				)
		self.ActCopiar = QAction(
				ACT_COPIAR, self, shortcut = 'Ctrl+C', statusTip = ACT_COPIAR_DESCRIPCIÓN,
				triggered = self.copiar_del_menu_editar
				)
		self.ActPegar = QAction(
				ACT_PEGAR, self, shortcut = 'Ctrl+V', statusTip = ACT_PEGAR_DESCRIPCIÓN,
				triggered = self.pegar_del_menu_editar
				)
		self.ActEliminar = QAction(
				ACT_ELIMINAR, self, shortcut = 'Del', statusTip = ACT_ELIMINAR_DESCRIPCIÓN,
				triggered = self.eliminar_del_menu_editar
				)
		
	def crear_menús(self):
		# Inicialización del menú.
		menu_principal = self.menuBar()
		self.menú_archivo(menu_principal)
		self.menú_editar(menu_principal)
		
	def menú_archivo(self, menu_superior):
		self.menú_archivo = menu_superior.addMenu(MENÚ_ARCHIVO)
		self.menú_archivo.addAction(self.ActNuevo)
		self.menú_archivo.addSeparator()
		self.menú_archivo.addAction(self.ActAbrir)
		self.menú_archivo.addAction(self.ActGuardar)
		self.menú_archivo.addAction(self.ActGuardarComo)
		self.menú_archivo.addSeparator()
		self.menú_archivo.addAction(self.ActSalir)
		
	def menú_editar(self, menu_superior):
		self.menú_edición = menu_superior.addMenu(MENÚ_EDITAR)
		self.menú_edición.addAction(self.act_deshacer)
		self.menú_edición.addAction(self.ActRehacer)
		self.menú_edición.addSeparator()
		self.menú_edición.addAction(self.ActCortar)
		self.menú_edición.addAction(self.ActCopiar)
		self.menú_edición.addAction(self.ActPegar)
		self.menú_edición.addSeparator()
		self.menú_edición.addAction(self.ActEliminar)
	
	def definir_título(self):
		título = "Editor de nodos"
		título += " - "
		título += self.obtener_actual_editor_de_nodos().obtener_nombre_amigable_al_usuario()
		
		self.setWindowTitle(título)

	
	def closeEvent(self, event):
		if self.confirmar_cierre():
			event.accept()
		else:
			event.ignore()
			
	def obtener_actual_editor_de_nodos(self):
		return self.centralWidget()
	
	def archivo_modificado(self):
		editor_de_nodos = self.obtener_actual_editor_de_nodos()
		return editor_de_nodos.escena.hay_cambios() if editor_de_nodos else False
			
	def confirmar_cierre(self):
		if not self.archivo_modificado():
			return True
		
		res = CuadroDialogo(self, "Warning", TÍTULO_CIERRE, MENSAJE_CIERRE, None,
							BOTON_CIERRE_1, BOTON_CIERRE_2, BOTON_CIERRE_3)

		if res.checkout == BOTON_CIERRE_1:
			return self.guardar_archivo()
		elif res.checkout == BOTON_CIERRE_3:
			return False
		
		return True
		
	def nueva_pos_de_la_escena(self, x, y):
		self.status_mouse_pos.setText("Posición: [%d, %d]" % (x, y))
		
	def obtener_directorio_filedialog(self):
		return ''
	
	def obtener_filtro_filedialog(self):
		return 'Graph (*.json);;All files (*)'
		
	def nuevo_archivo(self):
		if self.confirmar_cierre():
			self.obtener_actual_editor_de_nodos().nuevo_archivo()
			self.definir_título()
			
		
	def abrir_archivo(self):
		if self.confirmar_cierre():
			fname, filter = QFileDialog.getOpenFileName(self, TÍTULO_DIÁLOGO_ABRIR)
			if fname != '' and os.path.isfile(fname):
				self.obtener_actual_editor_de_nodos().leer_archivo(fname)
				self.definir_título()
	
	def guardar_archivo(self):
		actual_editor_de_nodos = self.obtener_actual_editor_de_nodos()
		if actual_editor_de_nodos is not None:
			if not actual_editor_de_nodos.hay_nombre_de_archivo(): return self.guardar_archivo_como()
	
			actual_editor_de_nodos.guardar_archivo()
			self.statusBar().showMessage("%s %s" % (MENSAJE_5, actual_editor_de_nodos.filename), 5000)
			
			# Soporte para aplicaciones MDI.
			if hasattr(actual_editor_de_nodos, "definir_título"): actual_editor_de_nodos.definir_título()
			else: self.definir_título()
			return True
	
	def guardar_archivo_como(self):
		actual_editor_de_nodos = self.obtener_actual_editor_de_nodos()
		if actual_editor_de_nodos is not None:
			fname, filter = QFileDialog.getSaveFileName(self, TÍTULO_DIÁLOGO_GUARDAR, self.obtener_directorio_filedialog(),
			                                            self.obtener_filtro_filedialog())
			if fname == '': return False
			
			self.antes_de_guardar_como(actual_editor_de_nodos, fname)
			actual_editor_de_nodos.guardar_archivo(fname)
			self.statusBar().showMessage("%s %s" % (MENSAJE_5, actual_editor_de_nodos.filename), 5000)

			# Soporte para aplicaciones MDI.
			if hasattr(actual_editor_de_nodos, "definir_título"): actual_editor_de_nodos.definir_título()
			else: self.definir_título()
			return True
		
	def antes_de_guardar_como(self, editor_actual, nombre_de_archivo):
		pass
		
	def deshacer_del_menu_editar(self):
		if self.obtener_actual_editor_de_nodos():
			self.obtener_actual_editor_de_nodos().escena.historial.deshacer()
		
	def rehacer_del_menu_editar(self):
		if self.obtener_actual_editor_de_nodos():
			self.obtener_actual_editor_de_nodos().escena.historial.rehacer()
	
	def eliminar_del_menu_editar(self):
		if self.obtener_actual_editor_de_nodos():
			self.obtener_actual_editor_de_nodos().escena.obtener_vista().eliminar_seleccionado()
	
	def cortar_del_menu_editar(self):
		if self.obtener_actual_editor_de_nodos():
			data = self.obtener_actual_editor_de_nodos().escena.portapapeles.serializar_seleccionado(delete=True)
			str_data = json.dumps(data, indent=4)
			QApplication.instance().clipboard().setText(str_data)

	def copiar_del_menu_editar(self):
		if self.obtener_actual_editor_de_nodos():
			data = self.obtener_actual_editor_de_nodos().escena.portapapeles.serializar_seleccionado(delete=False)
			str_data = json.dumps(data, indent=4)
			QApplication.instance().clipboard().setText(str_data)
		
	def pegar_del_menu_editar(self):
		if self.obtener_actual_editor_de_nodos():
			raw_data = QApplication.instance().clipboard().text()
			
			try:
				data = json.loads(raw_data)
			except ValueError as e:
				print("¡Pegaste datos og inválidos!", e)
				return
	
			# Verificar si los datos json son correctos.
			if "nodos" not in data:
				print("¡Los datos no contienen ningún nodo!")
				return
			
			return self.obtener_actual_editor_de_nodos().escena.portapapeles.deserialización_desde_el_portapapeles(data)
	
	def leer_configuraciones(self):
		config = QSettings(self.compania, self.nombre_del_producto)
		pos = config.value('pos', QPoint(200, 200))
		size = config.value('size', QSize(400, 400))
		self.move(pos)
		self.resize(size)
	
	def escribir_configuraciones(self):
		config = QSettings(self.compania, self.nombre_del_producto)
		config.setValue('pos', self.pos())
		config.setValue('size', self.size())