import sys
from PyQt6.QtWidgets import *

if __name__ == '__main__':
    app = QApplication(sys.argv)

    label = QLabel("¡Hola, mundo!")
    label.show()

    sys.exit(app.exec())
