import os
import json
from PyQt5.QtWidgets import *
from nodeeditor.Widget_de_nodos import EditorDeNodos
from nodeeditor.Botones import CuadroDialogo


class Ventana(QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.filename = None
		
		self.initUI()
		
#		QApplication.instance().clipboard().dataChanged.connect(self.onClipboardChange)

#	def onClipboardChange(self):
#		clip = QApplication.instance().clipboard()
#		print("Clipboard changed:", clip.text())
		
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
		menu_edicion.addAction(self.crearact('&Cortar', 'Ctrl+X', 'Corta elementos seleccionados.', self.CortarMEditar))
		menu_edicion.addAction(self.crearact('Cop&iar', 'Ctrl+C', 'Copia elementos seleccionados.', self.CopiarMEditar))
		menu_edicion.addAction(self.crearact('&Pegar', 'Ctrl+V', 'Pega el último elemento del portapapeles', self.PegarMEditar))
		menu_edicion.addSeparator()
		menu_edicion.addAction(self.crearact('&Eliminar', 'Del', 'Elimina los elementos seleccionados.', self.EliminarMEditar))
		
		Editor_de_nodos = EditorDeNodos(self)
		Editor_de_nodos.escena.addelementosmodificadoslistener(self.cambiarTitulo)
		self.setCentralWidget(Editor_de_nodos)
		
		# Barra de estado.
		self.statusBar().showMessage("")
		self.status_mouse_pos = QLabel("")
		self.statusBar().addPermanentWidget(self.status_mouse_pos)
		Editor_de_nodos.Vista.cambioPosEscena.connect(self.NuevaPosEscena)

		# Tamaño de la ventana
		self.setGeometry(100, 100, 800, 600)
		self.cambiarTitulo()
		self.show()
		
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
		