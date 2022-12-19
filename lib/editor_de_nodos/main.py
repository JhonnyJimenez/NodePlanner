import sys
from PyQt6.QtWidgets import QApplication
from ventana import EditorDeNodos


if __name__ == '__main__':
	programa = QApplication(sys.argv)

	ventana = EditorDeNodos()

	sys.exit(programa.exec())
