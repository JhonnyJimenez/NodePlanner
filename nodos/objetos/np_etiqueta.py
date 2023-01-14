from PyQt5.QtWidgets import QLabel
from nodos.objetos.np_objeto_base import ObjetodeNodePlanner
from nodos.objetos.np_utilitarios import tratado_de_datos, alineador
from np_constantes import NOMBRE_DEL_PRODUCTO


class Etiqueta(ObjetodeNodePlanner):
	def __init__(
			self, elemento_padre = None, texto: str = NOMBRE_DEL_PRODUCTO, llave: str = None, alineado: str | int = 2,
			especificación: bool = False, es_entrada: bool = False, **kwargs
			):
		self.texto = texto
		self.alineado = alineado
		self.especificación = especificación  # Aún no implemento esto.
		self.valor_recibido = None
		super().__init__(elemento_padre, llave = llave, es_entrada = es_entrada, **kwargs)

	def definir_objeto(self):
		return QLabel(self.texto, self.elemento_padre)

	def estilo(self):
		self.objeto.setStyleSheet('padding-left: 1px; background: transparent')
		alineador(self.objeto, self.alineado)

	def widget_conectado(self):
		if (
				self.zócalo is not None and self.es_entrada
				and self.elemento_padre.nodo.entradas[self.zócalo].Zocaloconexiones != []
		):
			nodo = self.elemento_padre.nodo.obtener_entrada(self.zócalo)
			contrazócalo = self.elemento_padre.nodo.obtener_contrazócalo(self.zócalo)
			self.valor_recibido = nodo.valores[nodo.diccionarios['Salidas'][contrazócalo.indice]]
			valor = tratado_de_datos(self.valor_recibido, self.especificación)
			self.objeto.setText(valor)

	def widget_desconectado(self):
		if (
				self.zócalo is not None and self.es_entrada
				and self.elemento_padre.nodo.entradas[self.zócalo].Zocaloconexiones == []
		):
			self.objeto.setText(self.texto)
