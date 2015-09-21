class Exception_UnknownJoint(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr("This joint was not found: %s"%self.value)
