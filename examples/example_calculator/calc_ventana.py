import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from nodeeditor.Utilidades import dump_exception, loadstylesheets
from nodeeditor.Ventana import Ventana
from examples.example_calculator.calc_subventana import SubVenCalc

# Imágenes para la skin negra.
import examples.example_calculator.qss.nodeeditor_dark_resources


class VenCalc(Ventana):
	def initUI(self):
		self.compania = 'Blenderfreak'
		self.nombre_del_producto = 'Calculadora de nodos'
		
		self.styleSheet_filename = os.path.join(os.path.dirname(__file__), "qss/editordenodos.qss")
		loadstylesheets(
			os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss"),
			self.styleSheet_filename,
		)
		
		self.mdiArea = QMdiArea()
		self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.mdiArea.setViewMode(QMdiArea.TabbedView)
		self.mdiArea.setDocumentMode(True)
		self.mdiArea.setTabsClosable(True)
		self.mdiArea.setTabsMovable(True)
		self.setCentralWidget(self.mdiArea)
		
		self.mdiArea.subWindowActivated.connect(self.actualizarMenus)
		self.windowMapper = QSignalMapper(self)
		self.windowMapper.mapped[QWidget].connect(self.configSubVentanaActiva)
		
		self.crearAcciones()
		self.crearMenus()
		self.crearBarradeHerramientas()
		self.crearBarradeEstado()
		self.actualizarMenus()
		
		self.crearDockdeNodos()
		
		self.leerConfigs()
		
		self.setWindowTitle("Ejemplo: \"Calculadora con nodos\"")
		
	def closeEvent(self, event):
		self.mdiArea.closeAllSubWindows()
		if self.mdiArea.currentSubWindow():
			event.ignore()
		else:
			self.escribirConfigs()
			event.accept()
	
	def actualizarMenus(self):
		print("Menús actualizados")
		activo = self.subVentanaActiva()
		haysubventanas = (activo is not None)
		
		self.ActGuardar.setEnabled(haysubventanas)
		self.ActGuardarComo.setEnabled(haysubventanas)
		self.ActCerrar.setEnabled(haysubventanas)
		self.ActCerrarTodas.setEnabled(haysubventanas)
		self.ActTile.setEnabled(haysubventanas)
		self.ActCascade.setEnabled(haysubventanas)
		self.ActVenSig.setEnabled(haysubventanas)
		self.ActVenAnt.setEnabled(haysubventanas)
		self.ActSeparator.setEnabled(haysubventanas)
	
	def actualizarMenuVentana(self):
		self.MenuVentana.clear()
		self.MenuVentana.addAction(self.ActCerrar)
		self.MenuVentana.addAction(self.ActCerrarTodas)
		self.MenuVentana.addSeparator()
		self.MenuVentana.addAction(self.ActTile)
		self.MenuVentana.addAction(self.ActCascade)
		self.MenuVentana.addSeparator()
		self.MenuVentana.addAction(self.ActVenSig)
		self.MenuVentana.addAction(self.ActVenAnt)
		self.MenuVentana.addAction(self.ActSeparator)
		
		windows = self.mdiArea.subWindowList()
		self.ActSeparator.setVisible(len(windows) != 0)
	
		for i, window in enumerate(windows):
			child = window.widget()
			
			text = "%d %s" % (i + 1, child.obtenerNombreAmigablealUsuario())
			if i < 9:
				text = '&' + text
		
			action = self.MenuVentana.addAction(text)
			action.setCheckable(True)
			action.setChecked(child is self.subVentanaActiva())
			action.triggered.connect(self.windowMapper.map)
			self.windowMapper.setMapping(action, window)

	def crearAcciones(self):
		super().crearAcciones()
		
		self.ActCerrar = QAction("C&errar", self, statusTip="Cierra la ventana activa.", triggered=self.mdiArea.closeActiveSubWindow)
		self.ActCerrarTodas = QAction("Ce&rrar todas", self, statusTip="Cierra todas las ventanas.", triggered=self.mdiArea.closeAllSubWindows)
		self.ActTile = QAction("&Apilada", self, statusTip="Apila las ventanas.", triggered=self.mdiArea.tileSubWindows)
		self.ActCascade = QAction("&Cascada", self, statusTip="Coloca las ventanas en cascada.", triggered=self.mdiArea.cascadeSubWindows)
		self.ActVenSig = QAction("S&iguiente", self, shortcut=QKeySequence.NextChild, statusTip="Activa la siguiente ventana.", triggered=self.mdiArea.activateNextSubWindow)
		self.ActVenAnt = QAction("A&nterior", self, shortcut=QKeySequence.PreviousChild, statusTip="Activa la ventana anterior.", triggered=self.mdiArea.activatePreviousSubWindow)
		self.ActSeparator = QAction(self)
		self.ActSeparator.setSeparator(True)
		
		self.MSobre = QAction("&About", self, statusTip="Muestra una ventana con información de la aplicación.", triggered=self.sobre)
	
	def NuevoArchivo(self):
		try:
			subven = self.crearSubVentana()
			subven.show()
		except Exception as e: dump_exception(e)
		
	def GuardarArchivo(self):
		ActualEditordeNodos = self.subVentanaActiva()
		if ActualEditordeNodos:
			if not ActualEditordeNodos.confirmarsihaynombredearchivo():
				return self.GuardarArchivoComo()
			else:
				ActualEditordeNodos.guardararchivo() # No pasamos el nombre, mantener el nombre.
				self.statusBar().showMessage("Guardado satisfactoriamente en %s" % ActualEditordeNodos.filename, 5000)
				ActualEditordeNodos.definirtitulo()
				return True
	
	def GuardarArchivoComo(self):
		ActualEditordeNodos = self.subVentanaActiva()
		if ActualEditordeNodos:
			fname, filter = QFileDialog.getSaveFileName(self, "Guarda el archivo actual.")
			
			if fname == '': return False
			
			ActualEditordeNodos.guardararchivo(fname)
			ActualEditordeNodos.definirtitulo()
			self.statusBar().showMessage("Guardado satisfactoriamente como %s" % fname, 5000)
		
	def AbrirArchivo(self):
		fnames, filter = QFileDialog.getOpenFileNames(self, 'Abrir')
		
		try:
			for fname in fnames:
				if fname:
					existing = self.encontrarSubVentana(fname)
					if existing:
						self.mdiArea.setActiveSubWindow(existing)
					else:
						# Necesitaremos crear una nueva subventana y abrir el archivo.
						editor_de_nodos = SubVenCalc()
						if editor_de_nodos.leerarchivo(fname):
							self.statusBar().showMessage("Archivo abierto: %s" % fname, 5000)
							editor_de_nodos.definirtitulo()
							subven = self.mdiArea.addSubWindow(editor_de_nodos)
							subven.show()
						else:
							editor_de_nodos.close()
		except Exception as e: dump_exception(e)
		
	def sobre(self):
		QMessageBox.about(self, "Sobre el ejemplo \"Calculadora de nodos\"",
						  "El ejemplo <b>Calculadora con nodos</b> demuestra cómo escribir múltiples "
						  "aplicaciones de interfaz de documentos usando PyQt5 y NodeEditor. Para más información "
						  "visita: <a href='https://www.blenderfreak.com/'>www.BlenderFreak.com</a>.")

	def crearMenus(self):
		super().crearMenus()
		
		self.MenuVentana = self.menuBar().addMenu("&Ventana")
		self.actualizarMenuVentana()
		self.MenuVentana.aboutToShow.connect(self.actualizarMenuVentana)
		
		self.menuBar().addSeparator()
		
		self.MenuAyuda = self.menuBar().addMenu("&Ayuda")
		self.MenuAyuda.addAction(self.MSobre)
	
	def crearBarradeHerramientas(self):
		pass
	
	def crearDockdeNodos(self):
		self.listadeWidget = QListWidget()
		self.listadeWidget.addItem("Sumar")
		self.listadeWidget.addItem("Restar")
		self.listadeWidget.addItem("Multiplicar")
		self.listadeWidget.addItem("Dividir")
		
		self.objetos = QDockWidget("Nodos")
		self.objetos.setWidget(self.listadeWidget)
		self.objetos.setFloating(False)
		
		self.addDockWidget(Qt.RightDockWidgetArea, self.objetos)
	
	def crearBarradeEstado(self):
		self.statusBar().showMessage("Listo")
	
	def crearSubVentana(self):
		editor_de_nodos = SubVenCalc()
		subven = self.mdiArea.addSubWindow(editor_de_nodos)
		return subven
	
	def encontrarSubVentana(self, filename):
		for window in self.mdiArea.subWindowList():
			if window.widget().filename == filename:
				return window
		return None
	
	def subVentanaActiva(self):
		# Estamos devolviendo el widget de nodos aquí...
		subventanaActiva = self.mdiArea.activeSubWindow()
		if subventanaActiva:
			return subventanaActiva.widget()
		return None
	
	def configSubVentanaActiva(self):
		if window:
			self.mdiArea.setActiveSubWindow(window)