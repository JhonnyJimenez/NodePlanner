import os
import sys
from PyQt5.QtWidgets import *

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from lib.examples.example_calculator.calc_ventana import VenCalc

# Al ejecutar un programa, Python guarda «__main__» en la variable __name__
# si el módulo que se está ejecutando es el programa principal.

if __name__ == '__main__':
	programa = QApplication(sys.argv)
	
	# print(QStyleFactory.keys())
	programa.setStyle("Fusion")
	
	ventana = VenCalc()
	ventana.show()
	
	sys.exit(programa.exec())
