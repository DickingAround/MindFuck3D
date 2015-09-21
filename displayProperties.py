class displayProperties:
	color = [255,255,255]
	thickness = 1
	def __init__(self, color, thickness):
		self.color = color
		self.thickness = thickness
	def copy(self):
		d = displayProperties([self.color[0],self.color[1],self.color[2]],self.thickness)
		return d
