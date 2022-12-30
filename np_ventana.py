import os
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMdiArea, QWidget, QAction, QFileDialog, QMessageBox, QDockWidget
from PyQt5.QtCore import Qt, QSignalMapper, QSettings, QPoint, QSize

from lib.nodeeditor.Ventana import Ventana
from lib.nodeeditor.Utilidades import dump_exception, loadstylesheets
from lib.nodeeditor.Conexiones import Conexion
from lib.nodeeditor.ValidantesdeConexion import *
Conexion.agregar_validantes_de_conexiones(invalidar_conexion_de_doble_entrada_o_salida)
Conexion.agregar_validantes_de_conexiones(invalidar_conexiones_entre_el_mismo_nodo)

from np_constantes import *
from np_idioma import *
from np_subventana import NodePlannerSubVentana
from np_lista import Lista

# Boton de cerrado para la skin negra.
import qss.nodeeditor_dark_resources


class NodePlannerVentana(Ventana):
	def init_ui(self):
		self.compania = None
		self.nombre_del_producto = NOMBRE_DEL_PRODUCTO

		loadstylesheets(
			os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss"),
			"qss/EstiloNodo.qss",
		)

		self.icono_vacío = QIcon(".")

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

		self.setWindowTitle(NOMBRE_DEL_PRODUCTO)

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

		self.ActCerrar = QAction(
			ACT_CERRAR, self, statusTip = ACT_CERRAR_DESCRIPCIÓN, triggered = self.mdiArea.closeActiveSubWindow
			)
		self.ActCerrarTodas = QAction(
			ACT_CERRAR_TODAS, self, statusTip = ACT_CERRAR_TODAS_DESCRIPCIÓN, triggered = self.mdiArea.closeAllSubWindows
			)
		self.ActTile = QAction(
			ACT_TILE, self, statusTip = ACT_TILE_DESCRIPCIÓN, triggered = self.mdiArea.tileSubWindows
			)
		self.ActCascade = QAction(
			ACT_CASCADE, self, statusTip = ACT_CASCADE_DESCRIPCIÓN, triggered = self.mdiArea.cascadeSubWindows
			)
		self.ActVenSig = QAction(
			ACT_VEN_SIG, self, shortcut = QKeySequence.NextChild, statusTip = ACT_VEN_SIG_DESCRIPCIÓN,
			triggered = self.mdiArea.activateNextSubWindow
			)
		self.ActVenAnt = QAction(
			ACT_VEN_ANT, self, shortcut = QKeySequence.PreviousChild, statusTip = ACT_VEN_ANT_DESCRIPCIÓN,
			triggered = self.mdiArea.activatePreviousSubWindow
			)
		self.ActSeparator = QAction(self)
		self.ActSeparator.setSeparator(True)

		self.MSobre = QAction(
			M_SOBRE, self, statusTip = M_SOBRE_DESCRIPCIÓN, triggered = self.sobre
			)

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
		fnames, filter = QFileDialog.getOpenFileNames(
			self, TÍTULO_DIÁLOGO_ABRIR, self.obtener_directorio_filedialog(), self.obtener_filtro_filedialog()
			)

		try:
			for fname in fnames:
				if fname:
					existing = self.encontrar_subventana(fname)
					if existing:
						self.mdiArea.setActiveSubWindow(existing)
					else:
						# Necesitaremos crear una nueva subventana y abrir el archivo.
						editor_de_nodos = NodePlannerSubVentana()
						if editor_de_nodos.leer_archivo(fname):
							self.statusBar().showMessage("%s %s" % (MENSAJE_1, fname), 5000)
							editor_de_nodos.definir_título()
							subven = self.crear_subventana(editor_de_nodos)
							subven.show()
						else:
							editor_de_nodos.close()
		except Exception as e: dump_exception(e)

	def sobre(self):
		QMessageBox.about(self, MENSAJE_2, MENSAJE_3)

	def crear_menús(self):
		super().crear_menús()

		self.menu_ventana = self.menuBar().addMenu(MENU_VENTANA)
		self.menu_ventana.aboutToShow.connect(self.actualizar_menu_ventana)

		self.menuBar().addSeparator()

		self.menu_ayuda = self.menuBar().addMenu(MENU_AYUDA)
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

		barra_lateral_de_nodos = self.menu_ventana.addAction(BARRA_DE_NODOS)
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
		self.widgetListadeNodos = Lista()

		self.dockNodos = QDockWidget(DOCK_DE_NODOS)
		self.dockNodos.setWidget(self.widgetListadeNodos)
		self.dockNodos.setFloating(False)

		self.addDockWidget(Qt.RightDockWidgetArea, self.dockNodos)

	def crear_barra_de_estado(self):
		self.statusBar().showMessage(MENSAJE_4)

	def crear_subventana(self, subwidget = None):
		editor_de_nodos = subwidget if subwidget is not None else NodePlannerSubVentana()
		subven = self.mdiArea.addSubWindow(editor_de_nodos)
		subven.setWindowIcon(self.icono_vacío)
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

	def leer_configuraciones(self):
		config = QSettings(self.nombre_del_producto)
		pos = config.value('pos', QPoint(200, 200))
		size = config.value('size', QSize(400, 400))
		self.move(pos)
		self.resize(size)

	def escribir_configuraciones(self):
		config = QSettings(self.nombre_del_producto)
		config.setValue('pos', self.pos())
		config.setValue('size', self.size())
