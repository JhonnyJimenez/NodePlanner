from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

VALIDANTE_NUMÉRICO = QRegExpValidator(QRegExp("^[-+]?[0-9]{1,3}(\s?[0-9]{3})*\.?[0-9]*([eE][-+]?[0-9]+)?$"))

