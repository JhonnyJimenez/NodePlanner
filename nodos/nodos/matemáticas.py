from nodos.categorías.entradas import *
from nodos.objetos.np_etiqueta import Etiqueta
from nodos.objetos.np_desplegable import Desplegable
from nodos.objetos.np_utilitarios import operaciones_matemáticas

OPERACIONES = [
				"Adicionar", "Sustraer", "Multiplicar", "Dividir", "Multiplicar y adicionar",
				"Potencia", "Logaritmo", "Raíz cuadrada", "Inverso de raíz cuadrada", "Absoluto",
				"Exponencial", "Mínimo", "Máximo", "Menor que", "Mayor que", "Signo", "Comparar",
				"Mínimo suave", "Máximo suave", "Redondear", "Piso", "Techo", "Truncar", "Fracción",
				"Resto", "Ciclo", "Adherir", "Ping, pong", "Seno", "Coseno", "Tangente", "Arco seno",
				"Arco coseno", "Arco tangente", "Arco tangente 2", "Seno hiperbólico",
				"Coseno, hiperbólico", "Tangente hiperbólica", "A radianes", "A grados"
				]

class ContenidodelNodoMatemático(ContenidodelosNodosdeEntrada):
	def contenido(self):

		self.contenido_de_salidas = [
				Etiqueta(self, 'Resultado', alineado = 3, llave = 'Resultado', zócalo = 0)
				]
		self.contenido_de_entradas = [
				Desplegable(self, 'Objeto 1', OPERACIONES, elementos_visibles = 6),
				Entrada(self, '0.5', 'Objeto 2', validante = VALIDANTE_NUMÉRICO, zócalo = 0),
				Entrada(self, '0.5', 'Objeto 3', validante = VALIDANTE_NUMÉRICO, zócalo = 1),
				Entrada(self, '0.5', 'Objeto 4', validante = VALIDANTE_NUMÉRICO, zócalo = 2),
				]


@registrar_nodo(NODO_MATEMÁTICO)
class NodoMatemático(NodosdeEntrada):
	codigo_op = NODO_MATEMÁTICO
	titulo_op = "Matemáticas"

	ClasedelContenidodeNodo = ContenidodelNodoMatemático

	Entradas = [1, 1, 1]
	Salidas = [1]

	FormaDeEntradas = ['Círculo', 'Círculo', 'Círculo']
	FormaDeSalidas = ['Círculo']

	def __init__(self, escena, titulo = titulo_op, entradas = Entradas, salidas = Salidas):
		super().__init__(escena, titulo, entradas, salidas)

	def ajustes_adicionales(self):
		self.entrada1 = self.contenido.contenido_de_entradas[1]
		self.entrada2 = self.contenido.contenido_de_entradas[2]
		self.entrada3 = self.contenido.contenido_de_entradas[3]

	def métodos_de_evaluación(self):
		operación = self.valores['Objeto 1']

		if operación in (
							"Raíz cuadrada", "Inverso de raíz cuadrada", "Absoluto", "Exponencial", "Signo",
							"Redondear", "Piso", "Techo", "Truncar", "Fracción", "Seno", "Coseno", "Tangente",
							"Arco seno", "Arco coseno", "Arco tangente", "Seno hiperbólico",
							"Coseno, hiperbólico", "Tangente hiperbólica", "A radianes", "A grados"
							):
			self.entrada2.ocultar()
			self.entrada3.ocultar()
			self.Nodograficas.altura_del_nodo = (
					self.Nodograficas.altura_del_título + (2 * self.Nodograficas.márgen) + self.entrada1.altura
					+ self.entrada1.posición_y
			)

		elif operación in ("Multiplicar y adicionar", "Comparar", "Mínimo suave", "Máximo suave", "Ciclo"):
			for elemento in (self.entrada2, self.entrada3):
				if not self.entradas[elemento.zócalo].Zocaloconexiones:
					elemento.mostrar()
			self.Nodograficas.altura_del_nodo = (
					self.Nodograficas.altura_del_título + (2 * self.Nodograficas.márgen) + self.entrada3.altura
					+ self.entrada3.posición_y
			)

		else:
			self.entrada3.ocultar()
			if not self.entradas[self.entrada2.zócalo].Zocaloconexiones:
				self.entrada2.mostrar()
			self.Nodograficas.altura_del_nodo = (
					self.Nodograficas.altura_del_título + (2 * self.Nodograficas.márgen) + self.entrada2.altura
					+ self.entrada2.posición_y
			)

		self.valores['Resultado'] = operaciones_matemáticas(
				operación, self.valores['Objeto 2'], self.valores['Objeto 3'], self.valores['Objeto 4']
				)

		return self.valores['Resultado']