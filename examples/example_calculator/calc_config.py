LISTBOX_MIMETYPE = "application/x-item"


NODO_ENTRADA = 1
NODO_SALIDA = 2
NODO_SUMA = 3
NODO_RESTA = 4
NODO_MULTIPLICACION = 5
NODO_DIVISION = 6

CALC_NODOS = {
}

class ConfException(Exception): pass
class NododeRegistroInvalido(ConfException): pass
class CodigoopNoRegistrado(ConfException): pass

def registrar_nodo_ahora(codigo_op, class_reference):
	if codigo_op in CALC_NODOS:
		raise NododeRegistroInvalido("Registro del nodo '%s' duplicado. %s ya existe" %(
			codigo_op, CALC_NODOS[codigo_op]
		))
	CALC_NODOS[codigo_op] = class_reference
	
def registrar_nodo(codigo_op):
	def decorator(original_class):
		registrar_nodo_ahora(codigo_op, original_class)
		return original_class
	return decorator

def obtener_clase_del_codigo_op(codigo_op):
	if codigo_op not in CALC_NODOS: raise CodigoopNoRegistrado("El código op '%d' no está registrado" % codigo_op)
	return CALC_NODOS[codigo_op]
	