import traceback
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint


def dump_exception(e=None):
	# print("%s EXCEPTION:" % e.__class__.__name__, e)
	# traceback.print_tb(e.__traceback__)
	traceback.print_exc()


def loadstylesheets(*args):
	res = ''
	
	for arg in args:
		# print('Style loading:', arg)
		file = QFile(arg)
		file.open(QFile.ReadOnly | QFile.Text)
		stylesheet = file.readAll()
		res += "\n" + str(stylesheet, encoding='utf-8')
	QApplication.instance().setStyleSheet(res)


def debugnames(posicion):
	if posicion == 1:
		return "arriba a la izquierda"
	elif posicion == 2:
		return "abajo a la izquierda"
	elif posicion == 3:
		return "arriba a la derecha"
	elif posicion == 4:
		return "abajo a la derecha"
	else:
		return "en una posición desconocida"
	

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
		