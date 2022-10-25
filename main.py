import sys
from PyQt5.QtWidgets import *
from Ventana_principal import EditorDeNodos

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = EditorDeNodos()
    sys.exit(app.exec())
