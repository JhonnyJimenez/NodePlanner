import sys
from PyQt5.QtWidgets import QApplication
from np_ventana import NodePlannerVentana

if __name__ == '__main__':
	programa = QApplication(sys.argv)

	programa.setStyle("fusion")
	ventana = NodePlannerVentana()
	ventana.show()

	sys.exit(programa.exec())