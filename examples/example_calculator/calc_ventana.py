import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from nodeeditor.Utilidades import dump_exception, loadstylesheets, pp
from nodeeditor.Ventana import Ventana
from examples.example_calculator.calc_subventana import SubVenCalc
from examples.example_calculator.calc_drag_listbox import Listbox
from examples.example_calculator.calc_config import *

# Imágenes para la skin negra.
import examples.example_calculator.qss.nodeeditor_dark_resources

DEBUG = False


class VenCalc(Ventana):
	def initUI(self):
		self.compania = 'Blenderfreak'
		self.nombre_del_producto = 'Calculadora de nodos'
		
		self.styleSheet_filename = os.path.join(os.path.dirname(__file__), "qss/editordenodos.qss")
		loadstylesheets(
			os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss"),
			self.styleSheet_filename,
		)
		
		self.icono_vacio = QIcon(".")
		
		if DEBUG:
			print("Nodos registrados:")
			pp(CALC_NODOS)
		
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
		
		self.crearDockdeNodos()
		
		self.crearAcciones()
		self.crearMenus()
		self.crearBarradeHerramientas()
		self.crearBarradeEstado()
		self.actualizarMenus()
		
		self.leerConfigs()
		
		self.setWindowTitle("Ejemplo: \"Calculadora con nodos\"")
		
	def closeEvent(self, event):
		self.mdiArea.closeAllSubWindows()
		if self.mdiArea.currentSubWindow():
			event.ignore()
		else:
			self.escribirConfigs()
			event.accept()
			# hacky fix for PyQt 5.14.x
			import sys
			sys.exit(0)

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
	
	def obtenerActualEditordeNodos(self):
		# Estamos devolviendo el widget de nodos aquí...
		subventanaActiva = self.mdiArea.activeSubWindow()
		if subventanaActiva:
			return subventanaActiva.widget()
		return None
	
	def NuevoArchivo(self):
		try:
			subven = self.crearSubVentana()
			subven.show()
		except Exception as e: dump_exception(e)
		
	def AbrirArchivo(self):
		fnames, filter = QFileDialog.getOpenFileNames(self, 'Abrir', self.obtenerDirectorioFileDialog(), self.obtenerFiltroFileDialog())
		
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
							subven = self.crearSubVentana(editor_de_nodos)
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
		
		self.menu_ventana = self.menuBar().addMenu("&Ventana")
		self.menu_ventana.aboutToShow.connect(self.actualizarMenuVentana)
		
		self.menuBar().addSeparator()
		
		self.menu_ayuda = self.menuBar().addMenu("&Ayuda")
		self.menu_ayuda.addAction(self.MSobre)
		
		self.menu_edicion.aboutToShow.connect(self.actualizarMenuEditar)
	
	def actualizarMenus(self):
		activo = self.obtenerActualEditordeNodos()
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
		
		self.actualizarMenuEditar()
		self.actualizarMenuVentana()
	
	def actualizarMenuEditar(self):
		try:
			activo = self.obtenerActualEditordeNodos()
			haysubventanas = (activo is not None)
			
			self.ActPegar.setEnabled(haysubventanas)
			
			self.ActCortar.setEnabled(haysubventanas and activo.hayAlgoSeleccionado())
			self.ActCopiar.setEnabled(haysubventanas and activo.hayAlgoSeleccionado())
			self.ActEliminar.setEnabled(haysubventanas and activo.hayAlgoSeleccionado())
			
			self.ActDeshacer.setEnabled(haysubventanas and activo.habilitarDeshacer())
			self.ActRehacer.setEnabled(haysubventanas and activo.habilitarRehacer())
			
		except Exception as e: dump_exception(e)
	
	def actualizarMenuVentana(self):
		self.menu_ventana.clear()
		
		barra_lateral_de_nodos = self.menu_ventana.addAction("Barra de nodos")
		barra_lateral_de_nodos.setCheckable(True)
		barra_lateral_de_nodos.triggered.connect(self.barraLateraldeNodos)
		barra_lateral_de_nodos.setChecked(self.dockNodos.isVisible())
		
		self.menu_ventana.addSeparator()
		
		self.menu_ventana.addAction(self.ActCerrar)
		self.menu_ventana.addAction(self.ActCerrarTodas)
		self.menu_ventana.addSeparator()
		self.menu_ventana.addAction(self.ActTile)
		self.menu_ventana.addAction(self.ActCascade)
		self.menu_ventana.addSeparator()
		self.menu_ventana.addAction(self.ActVenSig)
		self.menu_ventana.addAction(self.ActVenAnt)
		self.menu_ventana.addAction(self.ActSeparator)
		
		windows = self.mdiArea.subWindowList()
		self.ActSeparator.setVisible(len(windows) != 0)
		
		for i, window in enumerate(windows):
			child = window.widget()
			
			text = "%d %s" % (i + 1, child.obtenerNombreAmigablealUsuario())
			if i < 9:
				text = '&' + text
			
			action = self.menu_ventana.addAction(text)
			action.setCheckable(True)
			action.setChecked(child is self.obtenerActualEditordeNodos())
			action.triggered.connect(self.windowMapper.map)
			self.windowMapper.setMapping(action, window)
		
	def barraLateraldeNodos(self):
		if self.dockNodos.isVisible():
			self.dockNodos.hide()
		else:
			self.dockNodos.show()
	
	def crearBarradeHerramientas(self):
		pass
	
	def crearDockdeNodos(self):
		self.widgetListadeNodos = Listbox()
		
		self.dockNodos = QDockWidget("Nodos")
		self.dockNodos.setWidget(self.widgetListadeNodos)
		self.dockNodos.setFloating(False)
		
		self.addDockWidget(Qt.RightDockWidgetArea, self.dockNodos)
	
	def crearBarradeEstado(self):
		self.statusBar().showMessage("Listo")
	
	def crearSubVentana(self, subwidget=None):
		editor_de_nodos = subwidget if subwidget is not None else SubVenCalc()
		subven = self.mdiArea.addSubWindow(editor_de_nodos)
		subven.setWindowIcon(self.icono_vacio)
		editor_de_nodos.escena.historial.historial_nuevo()
		editor_de_nodos.escena.historial.marcaInicialdelHistorial()
		# editor_de_nodos.escena.agregarObjetoSeleccionadoListener(self.actualizarMenuEditar)
		# editor_de_nodos.escena.agregarObjetosNoSeleccionadosListener(self.actualizarMenuEditar)
		editor_de_nodos.escena.historial.agregarmodificadoresdelhistorialisteners(self.actualizarMenuEditar)
		editor_de_nodos.agregarCloseEventListeners(self.cerrarSubVentana)
		return subven
	
	def cerrarSubVentana(self, widget, event):
		existe = self.encontrarSubVentana(widget.filename)
		self.mdiArea.setActiveSubWindow(existe)
		
		if self.confirmarCierre():
			event.accept()
		else:
			event.ignore()
	
	def encontrarSubVentana(self, filename):
		for window in self.mdiArea.subWindowList():
			if window.widget().filename == filename:
				return window
		return None
	
	def configSubVentanaActiva(self):
		if window:
			self.mdiArea.setActiveSubWindow(window)