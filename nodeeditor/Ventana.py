import os
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from nodeeditor.Widget_de_nodos import EditorDeNodos
from nodeeditor.Botones import CuadroDialogo


class Ventana(QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.compania = 'Blenderfreak'
		self.nombre_del_producto = 'Editor de nodos'
		
		self.initUI()
		
#		QApplication.instance().clipboard().dataChanged.connect(self.onClipboardChange)

#	def onClipboardChange(self):
#		clip = QApplication.instance().clipboard()
#		print("Clipboard changed:", clip.text())
	
	def initUI(self):
		self.crearAcciones()
		self.crearMenus()
		
		self.Editor_de_nodos = EditorDeNodos(self)
		self.Editor_de_nodos.escena.addelementosmodificadoslistener(self.definirtitulo)
		self.setCentralWidget(self.Editor_de_nodos)
		
		self.crearBarradeEstado()

		# Tamaño de la ventana
		self.setGeometry(100, 100, 800, 600)
		self.definirtitulo()
		self.show()
		
	def crearBarradeEstado(self):
		self.statusBar().showMessage("")
		self.status_mouse_pos = QLabel("")
		self.statusBar().addPermanentWidget(self.status_mouse_pos)
		self.Editor_de_nodos.Vista.cambioPosEscena.connect(self.NuevaPosEscena)
		
	def crearAcciones(self):
		self.ActNuevo = QAction('&Nuevo', self, shortcut='Ctrl+N', statusTip='Crea nuevas gráficas', triggered=self.NuevoArchivo)
		self.ActAbrir = QAction('&Abrir', self, shortcut='Ctrl+A', statusTip='Abre un archivo', triggered=self.AbrirArchivo)
		self.ActGuardar = QAction('&Guardar', self, shortcut='Ctrl+G', statusTip='Guarda el proyecto actual', triggered=self.GuardarArchivo)
		self.ActGuardarComo = QAction('G&uardar como...', self, shortcut='Ctrl+Shift+G', statusTip='Guarda el proyecto como...', triggered=self.GuardarArchivoComo)
		self.ActSalir = QAction('&Salir', self, shortcut='Ctrl+Q', statusTip='Crea nuevas gráficas', triggered=self.close)
		
		self.ActDeshacer = QAction('&Deshacer', self, shortcut='Ctrl+Z', statusTip='Deshace la última acción.', triggered=self.DeshacerMEditar)
		self.ActRehacer = QAction('&Rehacer', self, shortcut='Ctrl+Y', statusTip='Rehace la última acción.', triggered=self.RehacerMEditar)
		self.ActCortar = QAction('&Cortar', self, shortcut='Ctrl+X', statusTip='Corta elementos seleccionados.', triggered=self.CortarMEditar)
		self.ActCopiar = QAction('Cop&iar', self, shortcut='Ctrl+C', statusTip='Copia elementos seleccionados.', triggered=self.CopiarMEditar)
		self.ActPegar = QAction('&Pegar', self, shortcut='Ctrl+V', statusTip='Pega el último elemento del portapapeles', triggered=self.PegarMEditar)
		self.ActEliminar = QAction('&Eliminar', self, shortcut='Del', statusTip='Elimina los elementos seleccionados.', triggered=self.EliminarMEditar)
		
	def crearMenus(self):
		menu_principal = self.menuBar()
		
		# Inicialización del menú.
		# Menú archivo.
		self.menu_archivo = menu_principal.addMenu('&Archivo')
		self.menu_archivo.addAction(self.ActNuevo)
		self.menu_archivo.addSeparator()
		self.menu_archivo.addAction(self.ActAbrir)
		self.menu_archivo.addAction(self.ActGuardar)
		self.menu_archivo.addAction(self.ActGuardarComo)
		self.menu_archivo.addSeparator()
		self.menu_archivo.addAction(self.ActSalir)
		
		# Menú edición.
		self.menu_edicion = menu_principal.addMenu('&Edición')
		self.menu_edicion.addAction(self.ActDeshacer)
		self.menu_edicion.addAction(self.ActRehacer)
		self.menu_edicion.addSeparator()
		self.menu_edicion.addAction(self.ActCortar)
		self.menu_edicion.addAction(self.ActCopiar)
		self.menu_edicion.addAction(self.ActPegar)
		self.menu_edicion.addSeparator()
		self.menu_edicion.addAction(self.ActEliminar)
	
	def definirtitulo(self):
		titulo = "NodePlanner - Versión alpha: "
		titulo += self.obtenerActualEditordeNodos().obtenerNombreAmigablealUsuario()
		
		self.setWindowTitle(titulo)

	
	def closeEvent(self, event):
		if self.confirmacion():
			event.accept()
		else:
			event.ignore()
			
	def obtenerActualEditordeNodos(self):
		return self.centralWidget()
	
	def ArchivoModificado(self):
		return self.obtenerActualEditordeNodos().escena.elementos_modificados
			
	def confirmacion(self):
		if not self.ArchivoModificado():
			return True
		
		res = CuadroDialogo(self, "Warning", "¿Quiere guardar el documento?",
							"¿Quiere guardar los cambios realizados en este documento?\nSe perderán sus cambios si no los guarda.",
							None,
							"Guardar", "No guardar", "Cancelar")

		if res.checkout == "Guardar":
			return self.GuardarArchivo()
		elif res.checkout == "Cancelar":
			return False
		
		return True

		
	def NuevaPosEscena(self, x, y):
		self.status_mouse_pos.setText("Posición: [%d, %d]" % (x, y))
		
	def NuevoArchivo(self):
		if self.confirmacion():
			self.obtenerActualEditordeNodos().escena.limpiarEscena()
			self.obtenerActualEditordeNodos().filename = None
			self.definirtitulo()
			
		
	def AbrirArchivo(self):
		if self.confirmacion():
			fname, filter = QFileDialog.getOpenFileName(self, 'Abrir')
			if fname != '' and os.path.isfile(fname):
				self.obtenerActualEditordeNodos().leerarchivo(fname)
				self.definirtitulo()
	
	def GuardarArchivo(self):
		actual_editor_de_nodos = self.obtenerActualEditordeNodos()
		if actual_editor_de_nodos is not None:
			if not actual_editor_de_nodos.confirmarsihaynombredearchivo(): return self.GuardarArchivoComo()
	
			actual_editor_de_nodos.guardararchivo()
			self.statusBar().showMessage("Guardado éxitosamente en %s" % actual_editor_de_nodos.filename, 5000)
			
			# Soporte para aplicaciones MDI.
			if hasattr(actual_editor_de_nodos, "definirtitulo"): actual_editor_de_nodos.definirtitulo()
			else: self.definirtitulo()
			return True
	
	def GuardarArchivoComo(self):
		actual_editor_de_nodos = self.obtenerActualEditordeNodos()
		if actual_editor_de_nodos is not None:
			fname, filter = QFileDialog.getSaveFileName(self, 'Guardar como')
			if fname == '': return False

			actual_editor_de_nodos.guardararchivo(fname)
			self.statusBar().showMessage("Guardado éxitosamente en %s" % actual_editor_de_nodos.filename, 5000)

			# Soporte para aplicaciones MDI.
			if hasattr(actual_editor_de_nodos, "definirtitulo"): actual_editor_de_nodos.definirtitulo()
			else: self.definirtitulo()
			return True
		
	def DeshacerMEditar(self):
		self.obtenerActualEditordeNodos().escena.historial.deshacer()
		
	def RehacerMEditar(self):
		self.obtenerActualEditordeNodos().escena.historial.rehacer()
	
	def EliminarMEditar(self):
		self.obtenerActualEditordeNodos().escena.GraficosEsc.views()[0].eliminarSeleccionado()
	
	def CortarMEditar(self):
		data = self.obtenerActualEditordeNodos().escena.portapapeles.serializacionSeleccionado(delete=True)
		str_data = json.dumps(data, indent=4)
		QApplication.instance().clipboard().setText(str_data)

	def CopiarMEditar(self):
		data = self.obtenerActualEditordeNodos().escena.portapapeles.serializacionSeleccionado(delete=False)
		str_data = json.dumps(data, indent=4)
		QApplication.instance().clipboard().setText(str_data)
		
	def PegarMEditar(self):
		raw_data = QApplication.instance().clipboard().text()
		
		try:
			data = json.loads(raw_data)
		except ValueError as e:
			print("¡Pegaste datos og inválidos!", e)
			return

		# Verificar si los datos json son correctos.
		if "Nodos" not in data:
			print("¡Los datos no contienen ningún nodo!")
			return
		
		self.obtenerActualEditordeNodos().escena.portapapeles.deserializacionDesdePortapapeles(data)
	
	def leerConfigs(self):
		config = QSettings(self.compania, self.nombre_del_producto)
		pos = config.value('pos', QPoint(200, 200))
		size = config.value('size', QSize(400, 400))
		self.move(pos)
		self.resize(size)
	
	def escribirConfigs(self):
		config = QSettings(self.compania, self.nombre_del_producto)
		config.setValue('pos', self.pos())
		config.setValue('size', self.size())