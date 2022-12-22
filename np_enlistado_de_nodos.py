LISTBOX_MIMETYPE = "application/x-item"

NODO_BASE = 0

# 1 - 4
CATEGORIA_ENTRADAS = NODO_BASE + 1
NODO_ENTRADA_NÚMERO = CATEGORIA_ENTRADAS + 1
NODO_ENTRADA_CADENA = NODO_ENTRADA_NÚMERO + 1
NODO_ENTRADA_BOOLEANA = NODO_ENTRADA_CADENA + 1

# 5 - 6
CATEGORIA_SALIDAS = NODO_ENTRADA_BOOLEANA + 1
NODO_SALIDA = CATEGORIA_SALIDAS + 1

# 7 - ???
CATEGORIA_OPERACIONES = NODO_SALIDA + 1
DESCONOCIDO = CATEGORIA_OPERACIONES + 1

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
from np_nodo_base import NodoBase
from nodos.categorías import *
from nodos.nodos import *