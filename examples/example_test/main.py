import os
import sys
import inspect
from PyQt5.QtWidgets import *

from nodeeditor.Utilidades import loadstylesheets
from nodeeditor.Ventana import Ventana

# Al ejecutar un programa, Python guarda «__main__» en la variable __name__
# si el módulo que se está ejecutando es el programa principal.

if __name__ == '__main__':
	programa = QApplication(sys.argv)
	
	ventana = Ventana()
	module_path = os.path.dirname(inspect.getfile(ventana.__class__))
	
	loadstylesheets(os.path.join(module_path, 'qss/EstiloNodo.qss'))
	
	sys.exit(programa.exec())
