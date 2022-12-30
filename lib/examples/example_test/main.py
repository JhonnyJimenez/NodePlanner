import os
import sys
import inspect
from PyQt5.QtWidgets import *
# La siguiente linea tiene que estar antes que las importaciones locales ya que este archivo está en una ruta diferente.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from lib.nodeeditor.Utilidades import loadstylesheets
from lib.nodeeditor.Ventana import Ventana

# Al ejecutar un programa, Python guarda «__main__» en la variable __name__
# si el módulo que se está ejecutando es el programa principal.

if __name__ == '__main__':
	programa = QApplication(sys.argv)
	
	ventana = Ventana()
	ventana.editor_de_nodos.agregado_de_nodos()
	module_path = os.path.dirname(inspect.getfile(ventana.__class__))
	
	loadstylesheets(os.path.join(module_path, 'qss/EstiloNodo.qss'))
	
	sys.exit(programa.exec())
