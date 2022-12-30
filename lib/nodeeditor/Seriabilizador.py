class Serializable:
	def __init__(self):
		self.id = id(self)
	
	def serialización(self):
		raise NotImplemented()
	
	def deserialización(self, data, hashmap={}):
		raise NotImplemented()
	