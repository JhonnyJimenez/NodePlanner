class Serializable():
	def __init__(self):
		self.id = id(self)
	
	def serializacion(self):
		raise NotImplemented()
	
	def deserializacion(self, data, hashmap={}):
		raise NotImplemented()
	