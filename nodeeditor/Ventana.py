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
		
		self.filename = None
		
		self.initUI()
		
#		QApplication.instance().clipboard().dataChanged.connect(self.onClipboardChange)

#	def onClipboardChange(self):
#		clip = QApplication.instance().clipboard()
#		print("Clipboard changed:", clip.text())
	
	def initUI(self):
		self.crearAcciones()
		self.crearMenus()
		
		self.Editor_de_nodos = EditorDeNodos(self)
		self.Editor_de_nodos.escena.addelementosmodificadoslistener(self.cambiarTitulo)
		self.setCentralWidget(self.Editor_de_nodos)
		
		self.crearBarradeEstado()

		# Tamaño de la ventana
		self.setGeometry(100, 100, 800, 600)
		self.cambiarTitulo()
		self.show()
		
	def crearBarradeEstado(self):
		self.statusBar().showMessage("")
		self.status_mouse_pos = QLabel("")
		self.statusBar().addPermanentWidget(self.status_mouse_pos)
		self.Editor_de_nodos.Vista.cambioPosEscena.connect(self.NuevaPosEscena)
		
	def crearAcciones(self):
		self.MNuevo = QAction('&Nuevo', self, shortcut='Ctrl+N', statusTip='Crea nuevas gráficas', triggered=self.NuevoArchivo)
		self.MAbrir = QAction('&Abrir', self, shortcut='Ctrl+A', statusTip='Abre un archivo', triggered=self.AbrirArchivo)
		self.MGuardar = QAction('&Guardar', self, shortcut='Ctrl+G', statusTip='Guarda el proyecto actual', triggered=self.GuardarArchivo)
		self.MGuardarComo = QAction('G&uardar como...', self, shortcut='Ctrl+Shift+G', statusTip='Guarda el proyecto como...', triggered=self.GuardarArchivoComo)
		self.MSalir = QAction('&Salir', self, shortcut='Ctrl+Q', statusTip='Crea nuevas gráficas', triggered=self.close)
		
		self.MDeshacer = QAction('&Deshacer', self, shortcut='Ctrl+Z', statusTip='Deshace la última acción.', triggered=self.DeshacerMEditar)
		self.MRehacer = QAction('&Rehacer', self, shortcut='Ctrl+Y', statusTip='Rehace la última acción.', triggered=self.RehacerMEditar)
		self.MCortar = QAction('&Cortar', self, shortcut='Ctrl+X', statusTip='Corta elementos seleccionados.', triggered=self.CortarMEditar)
		self.MCopiar = QAction('Cop&iar', self, shortcut='Ctrl+C', statusTip='Copia elementos seleccionados.', triggered=self.CopiarMEditar)
		self.MPegar = QAction('&Pegar', self, shortcut='Ctrl+V', statusTip='Pega el último elemento del portapapeles', triggered=self.PegarMEditar)
		self.MEliminar = QAction('&Eliminar', self, shortcut='Del', statusTip='Elimina los elementos seleccionados.', triggered=self.EliminarMEditar)
		
	def crearMenus(self):
		menu_principal = self.menuBar()
		
		# Inicialización del menú.
		# Menú archivo.
		self.menu_archivo = menu_principal.addMenu('&Archivo')
		self.menu_archivo.addAction(self.MNuevo)
		self.menu_archivo.addSeparator()
		self.menu_archivo.addAction(self.MAbrir)
		self.menu_archivo.addAction(self.MGuardar)
		self.menu_archivo.addAction(self.MGuardarComo)
		self.menu_archivo.addSeparator()
		self.menu_archivo.addAction(self.MSalir)
		
		# Menú edición.
		self.menu_edicion = menu_principal.addMenu('&Edición')
		self.menu_edicion.addAction(self.MDeshacer)
		self.menu_edicion.addAction(self.MRehacer)
		self.menu_edicion.addSeparator()
		self.menu_edicion.addAction(self.MCortar)
		self.menu_edicion.addAction(self.MCopiar)
		self.menu_edicion.addAction(self.MPegar)
		self.menu_edicion.addSeparator()
		self.menu_edicion.addAction(self.MEliminar)
	
	def cambiarTitulo(self):
		titulo = "NodePlanner - Versión alpha: "
		if self.filename is None:
			titulo += "Nuevo"
		else:
			titulo += os.path.basename(self.filename)
		
		if self.centralWidget().escena.elementos_modificados:
			titulo += "*"
			
		self.setWindowTitle(titulo)

	
	def closeEvent(self, event):
		if self.confirmacion():
			event.accept()
		else:
			event.ignore()
			
	def ArchivoModificado(self):
		return self.centralWidget().escena.elementos_modificados
			
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
			self.centralWidget().escena.limpiarEscena()
			self.filename = None
			self.cambiarTitulo()
			
		
	def AbrirArchivo(self):
		if self.confirmacion():
			fname, filter = QFileDialog.getOpenFileName(self, 'Abrir')
			if fname == '':
				return
			if os.path.isfile(fname):
				self.centralWidget().escena.abrirArchivo(fname)
				self.filename = fname
				self.cambiarTitulo()
	
	def GuardarArchivo(self):
		if self.filename is None: return self.GuardarArchivoComo()
		self.centralWidget().escena.guardarArchivo(self.filename)
		self.statusBar().showMessage("Guardado éxitosamente en %s" % self.filename)
		return True
	
	def GuardarArchivoComo(self):
		fname, filter = QFileDialog.getSaveFileName(self, 'Guardar como')
		if fname == '':
			return False
		self.filename = fname
		self.GuardarArchivo()
		return True
		
	def DeshacerMEditar(self):
		self.centralWidget().escena.historial.deshacer()
		
	def RehacerMEditar(self):
		self.centralWidget().escena.historial.rehacer()
	
	def EliminarMEditar(self):
		self.centralWidget().escena.GraficosEsc.views()[0].eliminarSeleccionado()
	
	def CortarMEditar(self):
		data = self.centralWidget().escena.portapapeles.serializacionSeleccionado(delete=True)
		str_data = json.dumps(data, indent=4)
		QApplication.instance().clipboard().setText(str_data)

	def CopiarMEditar(self):
		data = self.centralWidget().escena.portapapeles.serializacionSeleccionado(delete=False)
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
		
		self.centralWidget().escena.portapapeles.deserializacionDesdePortapapeles(data)
	
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