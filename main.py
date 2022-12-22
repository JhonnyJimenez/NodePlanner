import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from np_ventana import NodePlannerVentana

if __name__ == '__main__':
	programa = QApplication(sys.argv)

	programa .setStyle("Fusion")
	ventana = NodePlannerVentana()
	ventana.show()

	sys.exit(programa.exec())