import os
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMdiArea, QWidget, QAction, QFileDialog, QMessageBox, QDockWidget
from PyQt5.QtCore import Qt, QSignalMapper

from lib.nodeeditor.Ventana import Ventana
from lib.nodeeditor.Utilidades import dump_exception, loadstylesheets, pp
from lib.nodeeditor.Conexiones import Conexion
from lib.nodeeditor.ValidantesdeConexion import *
# Conexion.agregar_validantes_de_conexiones(edge_validator_debug)
Conexion.agregar_validantes_de_conexiones(invalidar_conexion_de_doble_entrada_o_salida)
Conexion.agregar_validantes_de_conexiones(invalidar_conexiones_entre_el_mismo_nodo)

from lib.examples.example_calculator.calc_subventana import SubVenCalc
from lib.examples.example_calculator.calc_drag_listbox import Listbox
from lib.examples.example_calculator.calc_config import *
# Boton de cerrado para la skin negra.
import lib.examples.example_calculator.qss.nodeeditor_dark_resources


DEBUG = False


class VenCalc(Ventana):
	def init_ui(self):
		self.compania = 'Blenderfreak'
		self.nombre_del_producto = 'Calculadora de nodos'
		
		self.styleSheet_filename = os.path.join(os.path.dirname(__file__), "qss/editordenodos.qss")
		loadstylesheets(
			os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss"),
			self.styleSheet_filename,
		)
		
		self.icono_vacio = QIcon(".")
		
		if DEBUG:
			print("nodos registrados:")
			pp(CALC_NODOS)
		
		self.mdiArea = QMdiArea()
		self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.mdiArea.setViewMode(QMdiArea.TabbedView)
		self.mdiArea.setDocumentMode(True)
		self.mdiArea.setTabsClosable(True)
		self.mdiArea.setTabsMovable(True)
		self.setCentralWidget(self.mdiArea)
		
		self.mdiArea.subWindowActivated.connect(self.actualizar_menus)
		self.windowMapper = QSignalMapper(self)
		self.windowMapper.mapped[QWidget].connect(self.configurar_subventana_activa)
		
		self.crear_dock_de_nodos()
		
		self.crear_acciones()
		self.crear_menús()
		self.crear_barra_de_herramientas()
		self.crear_barra_de_estado()
		self.actualizar_menus()
		
		self.leer_configuraciones()
		
		self.setWindowTitle("Ejemplo: \"Calculadora con nodos\"")
		
	def closeEvent(self, event):
		self.mdiArea.closeAllSubWindows()
		if self.mdiArea.currentSubWindow():
			event.ignore()
		else:
			self.escribir_configuraciones()
			event.accept()
			# hacky fix for PyQt 5.14.x
			import sys
			sys.exit(0)

	def crear_acciones(self):
		super().crear_acciones()
		
		self.ActCerrar = QAction("C&errar", self, statusTip="Cierra la ventana activa.", triggered=self.mdiArea.closeActiveSubWindow)
		self.ActCerrarTodas = QAction("Ce&rrar todas", self, statusTip="Cierra todas las ventanas.", triggered=self.mdiArea.closeAllSubWindows)
		self.ActTile = QAction("&Apilada", self, statusTip="Apila las ventanas.", triggered=self.mdiArea.tileSubWindows)
		self.ActCascade = QAction("&Cascada", self, statusTip="Coloca las ventanas en cascada.", triggered=self.mdiArea.cascadeSubWindows)
		self.ActVenSig = QAction("S&iguiente", self, shortcut=QKeySequence.NextChild, statusTip="Activa la siguiente ventana.", triggered=self.mdiArea.activateNextSubWindow)
		self.ActVenAnt = QAction("A&nterior", self, shortcut=QKeySequence.PreviousChild, statusTip="Activa la ventana anterior.", triggered=self.mdiArea.activatePreviousSubWindow)
		self.ActSeparator = QAction(self)
		self.ActSeparator.setSeparator(True)
		
		self.MSobre = QAction("&About", self, statusTip="Muestra una ventana con información de la aplicación.", triggered=self.sobre)
	
	def obtener_actual_editor_de_nodos(self):
		# Estamos devolviendo el widget de nodos aquí...
		subventana_activa = self.mdiArea.activeSubWindow()
		if subventana_activa:
			return subventana_activa.widget()
		return None
	
	def nuevo_archivo(self):
		try:
			subven = self.crear_subventana()
			subven.show()
		except Exception as e: dump_exception(e)
		
	def abrir_archivo(self):
		fnames, filter = QFileDialog.getOpenFileNames(self, 'Abrir', self.obtener_directorio_filedialog(), self.obtener_filtro_filedialog())
		
		try:
			for fname in fnames:
				if fname:
					existing = self.encontrar_subventana(fname)
					if existing:
						self.mdiArea.setActiveSubWindow(existing)
					else:
						# Necesitaremos crear una nueva subventana y abrir el archivo.
						editor_de_nodos = SubVenCalc()
						if editor_de_nodos.leer_archivo(fname):
							self.statusBar().showMessage("Archivo abierto: %s" % fname, 5000)
							editor_de_nodos.definir_título()
							subven = self.crear_subventana(editor_de_nodos)
							subven.show()
						else:
							editor_de_nodos.close()
		except Exception as e: dump_exception(e)
		
	def sobre(self):
		QMessageBox.about(self, "Sobre el ejemplo \"Calculadora de nodos\"",
						  "El ejemplo <b>Calculadora con nodos</b> demuestra cómo escribir múltiples "
						  "aplicaciones de interfaz de documentos usando PyQt5 y NodeEditor. Para más información "
						  "visita: <a href='https://www.blenderfreak.com/'>www.BlenderFreak.com</a>.")

	def crear_menús(self):
		super().crear_menús()
		
		self.menu_ventana = self.menuBar().addMenu("&Ventana")
		self.menu_ventana.aboutToShow.connect(self.actualizar_menu_ventana)
		
		self.menuBar().addSeparator()
		
		self.menu_ayuda = self.menuBar().addMenu("&Ayuda")
		self.menu_ayuda.addAction(self.MSobre)
		
		self.menú_edición.aboutToShow.connect(self.actualizar_menu_editar)
	
	def actualizar_menus(self):
		activo = self.obtener_actual_editor_de_nodos()
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
		
		self.actualizar_menu_editar()
		self.actualizar_menu_ventana()
	
	def actualizar_menu_editar(self):
		try:
			activo = self.obtener_actual_editor_de_nodos()
			haysubventanas = (activo is not None)
			
			self.ActPegar.setEnabled(haysubventanas)
			
			self.ActCortar.setEnabled(haysubventanas and activo.hay_algo_seleccionado())
			self.ActCopiar.setEnabled(haysubventanas and activo.hay_algo_seleccionado())
			self.ActEliminar.setEnabled(haysubventanas and activo.hay_algo_seleccionado())
			
			self.act_deshacer.setEnabled(haysubventanas and activo.habilitar_deshacer())
			self.ActRehacer.setEnabled(haysubventanas and activo.habilitar_rehacer())
			
		except Exception as e: dump_exception(e)
	
	def actualizar_menu_ventana(self):
		self.menu_ventana.clear()
		
		barra_lateral_de_nodos = self.menu_ventana.addAction("Barra de nodos")
		barra_lateral_de_nodos.setCheckable(True)
		barra_lateral_de_nodos.triggered.connect(self.barra_lateral_de_nodos)
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
			
			text = "%d %s" % (i + 1, child.obtener_nombre_amigable_al_usuario())
			if i < 9:
				text = '&' + text
			
			action = self.menu_ventana.addAction(text)
			action.setCheckable(True)
			action.setChecked(child is self.obtener_actual_editor_de_nodos())
			action.triggered.connect(self.windowMapper.map)
			self.windowMapper.setMapping(action, window)
		
	def barra_lateral_de_nodos(self):
		if self.dockNodos.isVisible():
			self.dockNodos.hide()
		else:
			self.dockNodos.show()
	
	def crear_barra_de_herramientas(self):
		pass
	
	def crear_dock_de_nodos(self):
		self.widgetListadeNodos = Listbox()
		
		self.dockNodos = QDockWidget("nodos")
		self.dockNodos.setWidget(self.widgetListadeNodos)
		self.dockNodos.setFloating(False)
		
		self.addDockWidget(Qt.RightDockWidgetArea, self.dockNodos)
	
	def crear_barra_de_estado(self):
		self.statusBar().showMessage("Listo")
	
	def crear_subventana(self, subwidget=None):
		editor_de_nodos = subwidget if subwidget is not None else SubVenCalc()
		subven = self.mdiArea.addSubWindow(editor_de_nodos)
		subven.setWindowIcon(self.icono_vacio)
		editor_de_nodos.escena.historial.historial_nuevo()
		editor_de_nodos.escena.historial.marca_inicial_del_historial()
		# editor_de_nodos.escena.agregar_objeto_seleccionado_listener(self.actualizar_menu_editar)
		# editor_de_nodos.escena.agregar_objetos_no_seleccionados_listener(self.actualizar_menu_editar)
		editor_de_nodos.escena.historial.agregar_modificadores_del_historial_listeners(self.actualizar_menu_editar)
		editor_de_nodos.agregar_close_event_listeners(self.cerrar_subventana)
		return subven
	
	def cerrar_subventana(self, widget, event):
		existe = self.encontrar_subventana(widget.filename)
		self.mdiArea.setActiveSubWindow(existe)
		
		if self.confirmar_cierre():
			event.accept()
		else:
			event.ignore()
	
	def encontrar_subventana(self, filename):
		for ventana in self.mdiArea.subWindowList():
			if ventana.widget().filename == filename:
				return ventana
		return None
	
	def configurar_subventana_activa(self, ventana):
		if ventana:
			self.mdiArea.setActiveSubWindow(ventana)
			