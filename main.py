import sys
from PyQt5.QtWidgets import *


from Ventana import Ventana

# Al ejecutar un programa, Python guarda «__main__» en la variable __name__
# si el módulo que se está ejecutando es el programa principal.

if __name__ == '__main__':
	programa = QApplication(sys.argv)
	ventana = Ventana()
	sys.exit(programa.exec())
