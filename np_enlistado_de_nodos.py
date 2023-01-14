LISTBOX_MIMETYPE = "application/x-item"

NODO_BASE = 0

# 1 - 5
CATEGORÍA_ENTRADAS = 1
NODO_ENTRADA_NÚMERO = 2
NODO_ENTRADA_CADENA = 3
NODO_ENTRADA_BOOLEANA = 4
NODO_MATEMÁTICO = 5

# 6 - 7
CATEGORÍA_SALIDAS = 6
NODO_SALIDA = 7

# 8 - 14
CATEGORÍA_ASTRONOMÍA = 8
NODO_UNIVERSO = 9
NODO_AGRUPACIÓN = 10
NODO_GALAXIA = 11
NODO_SISTEMA = 12
NODO_ESTRELLA = 13
NODO_CELESTE = 14

# 15 - ???
CATEGORÍA_CRONISTAS = 15

NODO_PLACEHOLDER1 = 1001
NODO_PLACEHOLDER2 = 1002
NODO_PLACEHOLDER3 = 1003
NODO_PLACEHOLDER4 = 1004
NODO_PLACEHOLDER5 = 1005
NODO_PLACEHOLDER6 = 1006
NODO_PLACEHOLDER7 = 1007
NODO_PLACEHOLDER8 = 1008
NODO_PLACEHOLDER9 = 1009
NODO_PLACEHOLDER10 = 1010

NODEPLANNER_NODOS = {

		}


class ConfException(Exception):
	pass


class NododeRegistroInvalido(ConfException):
	pass


class CodigoopNoRegistrado(ConfException):
	pass


def registrar_nodo_ahora(codigo_op, class_reference):
	if codigo_op in NODEPLANNER_NODOS:
		raise NododeRegistroInvalido(
			"Registro del nodo '%s' duplicado. %s ya existe" % (
					codigo_op, NODEPLANNER_NODOS[codigo_op]
					)
			)
	NODEPLANNER_NODOS[codigo_op] = class_reference


def registrar_nodo(codigo_op):
	def decorator(original_class):
		registrar_nodo_ahora(codigo_op, original_class)
		return original_class

	return decorator


def obtener_clase_del_codigo_op(codigo_op):
	if codigo_op not in NODEPLANNER_NODOS:
		raise CodigoopNoRegistrado("El código op '%d' no está registrado" % codigo_op)
	return NODEPLANNER_NODOS[codigo_op]


# Importado de todos los nodos y su registro.
from nodos.nodo_base.np_nodo_base import NodoBase
from nodos.categorías import *
from nodos.nodos import *