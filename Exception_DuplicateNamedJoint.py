class Exception_DuplicateNamedJoint(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr("This joint already exists: %s"%self.value)
