import traceback
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint

def dump_exception(e):
	print("EXCEPTION:", e)
	traceback.print_tb(e.__traceback__)


def loadstylesheets(*args):
	res = ''
	
	for arg in args:
		# print('Style loading:', arg)
		file = QFile(arg)
		file.open(QFile.ReadOnly | QFile.Text)
		stylesheet = file.readAll()
		res += "\n" + str(stylesheet, encoding='utf-8')
	QApplication.instance().setStyleSheet(res)
	