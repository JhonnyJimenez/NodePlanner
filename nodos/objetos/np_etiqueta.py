from PyQt5.QtWidgets import QLabel
from nodos.objetos.np_objeto_base import ObjetodeNodePlanner
from nodos.objetos.np_utilitarios import tratado_de_datos_para_tooltip


class Etiqueta(ObjetodeNodePlanner):
	def objeto(self):
		return QLabel

	def parámetros(self):
		return self.texto_inicial, self.elemento_padre

	def estilo(self):
		self.objeto.setStyleSheet('padding-left: 1px; background: transparent')

	def contenido_del_objeto(self):
		self.elemento_padre.lista_de_información[self.índice] = self.objeto.text()

	def ocultado_por_entrada(self):
		if self.zócalo_de_entrada is not None and self.elemento_padre.nodo.entradas[self.zócalo_de_entrada].Zocaloconexiones != []:
			texto = self.elemento_padre.nodo.valores_de_entrada
			texto_arreglado = tratado_de_datos_para_tooltip(texto, self.especificación)
			valor = texto_arreglado[self.zócalo_de_entrada]
			self.objeto.setText(valor)

	def mostrado_por_entrada(self):
		if self.zócalo_de_entrada is not None and self.elemento_padre.nodo.entradas[self.zócalo_de_entrada].Zocaloconexiones == []:
			self.objeto.setText(self.texto_inicial)