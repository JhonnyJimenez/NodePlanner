from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class CuadroDialogo(QMessageBox):
	def __init__(self, parent, tipo: str, titulo: str, contenido: str, ruta_icono: str = None, *args):
		super().__init__(parent)
		
		self.setWindowTitle(titulo)
		self.setText(contenido)
		self.tipo(tipo, ruta_icono)
		self.botones(*args)
		self.checkout = None
		
		self.exec()

		
	def tipo(self, tipo, ruta_icono="Warning"):
		if tipo == "Question":
			self.setIcon(QMessageBox.Question)
		elif tipo == "Information":
			self.setIcon(QMessageBox.Information)
		elif tipo == "Warning":
			self.setIcon(QMessageBox.Warning)
		elif tipo == "Critical":
			self.setIcon(QMessageBox.Critical)
		elif tipo == "Custom":
			self.icono = QPixmap(ruta_icono).scaled(75, 75, 1, 1)
			self.setIconPixmap(self.icono)
	
	def botones(self, *args):
		for argumento in args:
			self.addButton(argumento, QMessageBox.AcceptRole)
			self.buttonClicked.connect(self.clickcheck)
		
	def clickcheck(self, i):
		self.checkout = i.text()
		