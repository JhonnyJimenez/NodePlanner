DEBUG = False


def imprimir_error(*args):
	if DEBUG: print("Error de validación de conexión:", *args)

def debug_de_validacion_de_conexion(entrada, salida):
	print("VALIDANDO:")
	print(entrada, "entrada" if entrada.esEntrada else "salida",  "del nodo", entrada.nodo)
	for zocalo in entrada.nodo.entradas + entrada.nodo.salidas: print("\t", zocalo, "entrada" if zocalo.esEntrada else "salida")
	print(salida, "entrada" if salida.esEntrada else "salida", "del nodo", salida.nodo)
	for zocalo in salida.nodo.entradas + salida.nodo.salidas: print("\t", zocalo, "entrada" if zocalo.esEntrada else "salida")
	
	return True

def invalidar_conexion_de_doble_entrada_o_salida(entrada, salida):
	if entrada.esSalida and salida.esSalida:
		imprimir_error("Conectando dos salidas")
		return False
		
	if entrada.esEntrada and salida.esEntrada:
		imprimir_error("Conectando dos entradas")
		return False
		
	return True

def invalidar_conexiones_entre_el_mismo_nodo(entrada, salida):
	if entrada.nodo == salida.nodo:
		imprimir_error("Conectando el mismo nodo")
		return False
	
	return True