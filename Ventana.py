import os
from PyQt5.QtWidgets import *
from Editor_de_nodos_Widget import EditorDeNodos

class Ventana(QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.initUI()
		
		self.filename = None
		
	def crearact(self, nombre, atajo, ayuda, metodo):
		act = QAction(nombre, self)
		act.setShortcut(atajo)
		act.setToolTip(ayuda)
		act.triggered.connect(metodo)
		return act
	
	def initUI(self):
		menu_principal = self.menuBar()
		
		# Inicialización del menú.
		# Menú archivo.
		menu_archivo = menu_principal.addMenu('&Archivo')
		menu_archivo.addAction(self.crearact('&Nuevo', 'Ctrl+N', 'Crea nuevas gráficas', self.NuevoArchivo))
		menu_archivo.addSeparator()
		menu_archivo.addAction(self.crearact('&Abrir', 'Ctrl+A', 'Abre un archivo', self.AbrirArchivo))
		menu_archivo.addAction(self.crearact('&Guardar', 'Ctrl+G', 'Guarda el proyecto actual', self.GuardarArchivo))
		menu_archivo.addAction(self.crearact('G&uardar como...', 'Ctrl+Shift+G', 'Guarda el proyecto como...', self.GuardarArchivoComo))
		menu_archivo.addSeparator()
		menu_archivo.addAction(self.crearact('&Salir', 'Ctrl+Q', 'Crea nuevas gráficas', self.close))
		
		# Menú edición.
		menu_edicion = menu_principal.addMenu('&Edición')
		menu_edicion.addAction(self.crearact('&Deshacer', 'Ctrl+Z', 'Deshace la última acción.', self.DeshacerMEditar))
		menu_edicion.addAction(self.crearact('&Rehacer', 'Ctrl+Y', 'Rehace la última acción.', self.RehacerMEditar))
		menu_edicion.addSeparator()
		menu_edicion.addAction(self.crearact('&Eliminar', 'Del', 'Elimina los elementos seleccionados.', self.EliminarMEditar))
	#	menu_edicion.addAction(self.crearact('&Cortar', 'Ctrl+X', 'Corta elementos seleccionados.', self.NuevoArchivo))
	#	menu_edicion.addAction(self.crearact('Cop&iar', 'Ctrl+C', 'Copia elementos seleccionados.', self.NuevoArchivo))
	#	menu_edicion.addAction(self.crearact('&Pegar', 'Ctrl+P', 'Pega el último elemento del portapapeles', self.NuevoArchivo))
		
		Editor_de_nodos = EditorDeNodos(self)
		self.setCentralWidget(Editor_de_nodos)
		
		# Barra de estado.
		self.statusBar().showMessage("")
		self.status_mouse_pos = QLabel("")
		self.statusBar().addPermanentWidget(self.status_mouse_pos)
		Editor_de_nodos.Vista.cambioPosEscena.connect(self.NuevaPosEscena)

		# Tamaño de la ventana
		self.setGeometry(100, 100, 800, 600)
		self.setWindowTitle("NodePlanner - Versión alpha")
		self.show()
		
	def NuevaPosEscena(self, x, y):
		self.status_mouse_pos.setText("Posición: [%d, %d]" % (x, y))
		
	def NuevoArchivo(self):
		self.centralWidget().escena.limpiarEscena()
		
	def AbrirArchivo(self):
		fname, filter = QFileDialog.getOpenFileName(self, 'Abrir')
		if fname == '':
			return
		if os.path.isfile(fname):
			self.centralWidget().escena.abrirArchivo(fname)
	
	def GuardarArchivo(self):
		if self.filename is None: return self.GuardarArchivoComo()
		self.centralWidget().escena.guardarArchivo(self.filename)
		self.statusBar().showMessage("Guardado éxitosamente en %s" % self.filename)
	
	def GuardarArchivoComo(self):
		fname, filter = QFileDialog.getSaveFileName(self, 'Guardar como')
		if fname == '':
			return
		self.filename = fname
		self.GuardarArchivo()
		
	def DeshacerMEditar(self):
		self.centralWidget().escena.historial.deshacer()
		
	def RehacerMEditar(self):
		self.centralWidget().escena.historial.rehacer()
	
	def EliminarMEditar(self):
		self.centralWidget().escena.GraficosEsc.views()[0].eliminarSeleccionado()
	
	def random2(self):
		print('Menú Guardar como presionado')

