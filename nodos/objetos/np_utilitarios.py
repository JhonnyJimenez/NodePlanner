from PyQt5.QtCore import Qt

def tratado_de_datos_para_tooltip(lista_a_tratar: list, especificación: bool = False):
	valores_tratados = []
	for valor in lista_a_tratar:
		if valor is None:
			valores_tratados.append(valor)

		elif type(valor) is int:
			valor = "{:,}".format(valor)
			valor = valor.replace(",", " ")
			if especificación:
				valor += ' (Entero)'
			valores_tratados.append(valor)

		elif type(valor) is float:
			valor = "{:,}".format(valor)
			valor = valor.replace(",", " ")
			if especificación:
				valor += ' (Decimal)'
			valores_tratados.append(valor)

		elif type(valor) is str:
			if valor != '':
				if especificación:
					valor += ' (Cadena)'
			else:
				valor = 'Cadena vacía.'
			valores_tratados.append(valor)

		elif type(valor) is Qt.CheckState:
			if valor == 0:
				valor = 'Falso'
			if valor == 1:
				valor = 'Indeterminado'
			if valor == 2:
				valor = 'Verdadero'
			if especificación:
				valor += ' (Booleana)'
			valores_tratados.append(valor)

		else:
			valores_tratados.append('El tipo de datos %s no ha sido tratado.' % str(type(valor).__name__))

	return valores_tratados