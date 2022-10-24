import sys
from PyQt6.QtWidgets import *
from Ventanas import EditorDeNodos

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = EditorDeNodos()
    sys.exit(app.exec())
