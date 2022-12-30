from PyQt5.QtWidgets import QLabel, QLineEdit, QCheckBox, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from lib.nodeeditor.ContenidodelNodo import ContenidoDelNodo
from lib.nodeeditor.Utilidades import dump_exception

CREANDO = False


class NodoBaseContenido(ContenidoDelNodo):
	pass
	# def init_ui(self):
	# 	self.configuraciones()
	# 	self.posicion_libre = [0]
	# 	self.lista_de_contenidos = []
	# 	self.contenidos()
	#
	# 	self.calculo_de_altura = (
	# 			(self.posicion_libre[-1] - self.espaciado_entre_objetos_del_nodo)
	# 			+ (self.sangria_de_la_orilla * 2) + self.alturaTituloNodo
	# 	)
	#
	# 	if CREANDO:
	# 		print("La altura del nodo %s debe ser:" % self.nodo.__class__.__name__, self.calculo_de_altura)
	#
	# def contenidos(self):
	# 	self.etiqueta_1 = self.etiqueta("Tipos de entrada", 'Centro')
	# 	self.objeto_1 = self.entrada_de_línea(1, "Cadena")
	# 	self.objeto_2 = self.entrada_de_línea(2, '0', 'Entero')
	# 	self.objeto_3 = self.entrada_booleana(3, 1, "Booleana", True)
	# 	self.objeto_4 = self.lista_desplegable(4, 'Lista')
	#
	# def etiqueta(self, texto_inicial = None, alineado: int | str = 1, fuente = None, altura: int = None):
	# 	etiqueta = QLabel(texto_inicial, self)
	#
	# 	if fuente is None:
	# 		fuente = self.fuente
	# 	if altura is None:
	# 		altura = self.altura_por_defecto
	# 	etiqueta.posicion_y = self.posicion_libre[-1]
	#
	# 	etiqueta.setStyleSheet('padding-left: 1px; background: transparent')
	# 	etiqueta.setGeometry(0, etiqueta.posicion_y, self.ancho_disponible, altura)
	# 	if alineado in (1, 'Izquierda'):
	# 		etiqueta.setAlignment(Qt.AlignLeft)
	# 	elif alineado in (2, 'Centro'):
	# 		etiqueta.setAlignment(Qt.AlignCenter)
	# 	elif alineado in (3, 'Derecha'):
	# 		etiqueta.setAlignment(Qt.AlignRight)
	# 	etiqueta.setFont(fuente)
	# 	self.posicion_libre.append(etiqueta.posicion_y + altura + self.espaciado_entre_objetos_del_nodo)
	# 	self.lista_de_contenidos.append(etiqueta)
	# 	return etiqueta
	#
	# def entrada_de_línea(
	# 		self, zocalo: int = None, texto_inicial: object = '', texto_etiqueta: str = None, validante: object = None,
	# 		altura: int = None, fuente: object = None
	# 		):
	# 	línea = QLineEdit(texto_inicial, self)
	#
	# 	if fuente is None:
	# 		fuente = self.fuente
	# 	if altura is None:
	# 		altura = self.altura_por_defecto
	# 	línea.altura = altura
	# 	línea.posicion_y = self.posicion_libre[-1]
	#
	# 	if zocalo == 0:
	# 		línea.zocalo = zocalo
	# 	elif zocalo is None:
	# 		pass
	# 	else:
	# 		línea.zocalo = zocalo - 1
	#
	# 	if texto_etiqueta == '' or texto_etiqueta is None:
	# 		línea.setGeometry(0, línea.posicion_y, self.ancho_disponible, línea.altura)
	# 	else:
	# 		if texto_etiqueta[-1] != ':':
	# 			texto_etiqueta += ':'
	# 		línea.etiqueta = QLabel(texto_etiqueta, self)
	# 		línea.etiqueta.setGeometry(0, línea.posicion_y, self.ancho_etiqueta, línea.altura)
	# 		línea.etiqueta.setStyleSheet('padding-left: 1px; background: transparent')
	# 		línea.etiqueta.setAlignment(Qt.AlignVCenter)
	# 		línea.etiqueta.setFont(fuente)
	# 		línea.setGeometry(
	# 				self.ubicación_elemento,
	# 				línea.posicion_y,
	# 				self.ancho_elemento,
	# 				línea.altura
	# 				)
	#
	# 	línea.setAlignment(Qt.AlignCenter)
	#
	# 	línea.setFont(fuente)
	# 	línea.setValidator(validante)
	# 	self.posicion_libre.append(línea.posicion_y + línea.altura + self.espaciado_entre_objetos_del_nodo)
	# 	self.lista_de_contenidos.append(línea)
	# 	return línea
	#
	# def entrada_booleana(
	# 		self, zocalo: int = None, valor_inicial: int = 0, texto_etiqueta: str = 'Valor',
	# 		indeterminado: bool = False, altura: int = 20, fuente = None
	# 		):
	# 	booleana = QCheckBox(texto_etiqueta, self)
	#
	# 	if fuente is None:
	# 		fuente = self.fuente
	# 	if altura is None:
	# 		altura = self.altura_por_defecto
	# 	booleana.posicion_y = self.posicion_libre[-1]
	#
	# 	if zocalo == 0:
	# 		booleana.zocalo = zocalo
	# 	elif zocalo is None:
	# 		pass
	# 	else:
	# 		booleana.zocalo = zocalo - 1
	#
	# 	booleana.setGeometry(0, booleana.posicion_y, self.ancho_disponible, altura)
	# 	booleana.setStyleSheet('padding-left: 1px; color: #fff; background: transparent')
	# 	booleana.setTristate(indeterminado)
	# 	booleana.setCheckState(valor_inicial)
	# 	booleana.setFont(fuente)
	# 	self.posicion_libre.append(booleana.posicion_y + altura + self.espaciado_entre_objetos_del_nodo)
	# 	self.lista_de_contenidos.append(booleana)
	# 	return booleana
	#
	# def lista_desplegable(
	# 		self, zocalo = None, texto_etiqueta: str = None, elementos_visibles: int = 10, listado: list = None,
	# 		separadores: list = None, popup: bool = False, fuente = None, altura: str = 20
	# 		):
	# 	lista = QComboBox(self)
	#
	# 	if fuente is None:
	# 		fuente = self.fuente
	# 	if altura is None:
	# 		altura = self.altura_por_defecto
	# 	lista.posicion_y = self.posicion_libre[-1]
	#
	# 	if zocalo == 0:
	# 		lista.zocalo = zocalo
	# 	elif zocalo is None:
	# 		pass
	# 	else:
	# 		lista.zocalo = zocalo - 1
	#
	# 	if texto_etiqueta == '' or texto_etiqueta is None:
	# 		lista.setGeometry(0, lista.posicion_y, self.ancho_disponible, altura)
	# 	else:
	# 		if texto_etiqueta[-1] != ':':
	# 			texto_etiqueta += ':'
	# 		etiqueta = QLabel(texto_etiqueta, self)
	# 		etiqueta.setGeometry(0, lista.posicion_y, self.ancho_etiqueta, altura)
	# 		etiqueta.setStyleSheet('padding-left: 1px; background: transparent')
	# 		etiqueta.setAlignment(Qt.AlignVCenter)
	# 		etiqueta.setFont(fuente)
	# 		lista.setGeometry(
	# 				self.ubicación_elemento,
	# 				lista.posicion_y,
	# 				self.ancho_elemento,
	# 				altura
	# 				)
	#
	# 	lista_por_defecto = [
	# 			"Objeto 1", "Objeto 2", "Objeto 3", "Objeto 4", "Objeto 5", "Objeto 6", "Objeto 7", "Objeto 8",
	# 			"Objeto 9", "Objeto 10", "Objeto 11",
	# 			]
	# 	if listado is not None:
	# 		if len(listado) != 0:
	# 			lista.addItems(listado)
	# 		else:
	# 			lista.addItems(lista_por_defecto)
	# 	else:
	# 		lista.addItems(lista_por_defecto)
	#
	# 	cantidad_separadores = 0
	# 	if separadores is not None:
	# 		if len(separadores) != 0:
	# 			for separador in separadores:
	# 				cantidad_separadores += 1
	# 				lista.insertSeparator(separador)
	#
	# 	lista.setMaxVisibleItems(elementos_visibles + cantidad_separadores)
	#
	# 	if not popup:
	# 		lista.setStyleSheet('combobox-popup: 0; background: #808080')
	#
	# 	self.posicion_libre.append(lista.posicion_y + altura + self.espaciado_entre_objetos_del_nodo)
	# 	self.lista_de_contenidos.append(lista)
	# 	return lista
	#
	# def configuraciones(self):
	# 	self.redondezdelaOrilladelNodo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).redondezdelaOrilladelNodo
	# 	self.sangria_de_la_orilla = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).sangria_de_la_orilla
	# 	self.alturaTituloNodo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).alturaTituloNodo
	# 	self.sangria_del_titulo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).sangria_del_titulo
	# 	self.sangria_vertical_del_titulo = self.nodo.obtenerClasedeGraficosdeNodo()(
	# 		self.nodo
	# 		).sangria_vertical_del_titulo
	# 	self.anchoNodo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).anchoNodo
	# 	self.altoNodo = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).altoNodo
	#
	# 	self.altura_disponible = self.nodo.obtenerClasedeGraficosdeNodo()(self.nodo).altura_disponible
	# 	self.ancho_disponible = int(self.anchoNodo - (2 * self.sangria_de_la_orilla))
	# 	self.espaciado_entre_objetos_del_nodo = 5
	# 	self.altura_por_defecto = 20
	#
	# 	# Tamaños para elementos con etiquetas.
	# 	self.separación = 1
	# 	self.divisor = 3
	# 	self.proporción = (self.ancho_disponible // self.divisor)
	#
	# 	self.ancho_etiqueta = self.proporción - self.separación
	# 	self.ubicación_elemento = self.proporción + self.separación
	# 	self.ancho_elemento = (self.proporción * (self.divisor - 1)) - self.separación
	#
	# 	# Fuente
	# 	self.fuente = QFont("Ubuntu")
	#
	# def serialización(self):
	# 	res = super().serialización()
	# 	self.lista_a_serializar(res)
	# 	return res
	#
	# def deserialización(self, data, hashmap = {}):
	# 	res = super().deserialización(data, hashmap)
	# 	try:
	# 		self.lista_a_desearializar(data)
	# 		return True
	# 	except Exception as e:
	# 		dump_exception(e)
	# 	return res
	#
	# def lista_a_serializar(self, res):
	# 	res['Objeto_1'] = self.objeto_1.text()
	# 	res['Objeto_2'] = self.objeto_2.text()
	# 	res['Objeto_3'] = self.objeto_3.checkState()
	# 	res['Objeto_4'] = self.objeto_4.currentText()
	#
	# def lista_a_desearializar(self, data):
	# 	self.objeto_1.setText(data['Objeto_1'])
	# 	self.objeto_2.setText(data['Objeto_2'])
	# 	self.objeto_3.setCheckState(data['Objeto_3'])
	# 	self.objeto_4.setCurrentText(data['Objeto_4'])
