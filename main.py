import sys
from PyQt5.QtWidgets import *
from Ventana_principal import EditorDeNodos

# Al ejecutar un programa, Python guarda «__main__» en la variable __name__
# si el módulo que se está ejecutando es el programa principal.

if __name__ == '__main__':
	programa = QApplication(sys.argv)
	ventana = EditorDeNodos()
	sys.exit(programa.exec())
