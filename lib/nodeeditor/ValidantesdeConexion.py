DEBUG = False


def imprimir_error(*args):
	if DEBUG: print("Error de validación de conexión:", *args)

def debug_de_validacion_de_conexion(zócalo_origen, zócalo_destino):
	print("VALIDANDO:")
	print(zócalo_origen, "zócalo_origen" if zócalo_origen.es_entrada else "zócalo_destino", "del nodo", zócalo_origen.nodo)
	for zocalo in zócalo_origen.nodo.entradas + zócalo_origen.nodo.salidas: print("\t", zocalo, "zócalo_origen" if zocalo.es_entrada else "zócalo_destino")
	print(zócalo_destino, "zócalo_origen" if zócalo_destino.es_entrada else "zócalo_destino", "del nodo", zócalo_destino.nodo)
	for zocalo in zócalo_destino.nodo.entradas + zócalo_destino.nodo.salidas: print("\t", zocalo, "zócalo_origen" if zocalo.es_entrada else "zócalo_destino")
	
	return True

def invalidar_conexion_de_doble_entrada_o_salida(zócalo_origen, zócalo_destino):
	if zócalo_origen.es_salida and zócalo_destino.es_salida:
		imprimir_error("Conectando dos salidas.")
		return False
		
	if zócalo_origen.es_entrada and zócalo_destino.es_entrada:
		imprimir_error("Conectando dos entradas.")
		return False
		
	return True

def invalidar_conexiones_entre_el_mismo_nodo(zócalo_origen, zócalo_destino):
	if zócalo_origen.nodo == zócalo_destino.nodo:
		imprimir_error("Conectando el mismo nodo.")
		return False
	
	return True


def invalidar_conexiones_a_nodos_padres(zócalo_origen, zócalo_destino):
	if zócalo_origen.es_salida and zócalo_origen.nodo in zócalo_destino.nodo.descendencia:
		imprimir_error("Conectando un nodo hijo con su padre.")
		return False
	elif zócalo_origen.es_entrada and zócalo_destino.nodo in zócalo_origen.nodo.descendencia:
		imprimir_error("Conectando un nodo padre con su hijo.")
		return False

	return True