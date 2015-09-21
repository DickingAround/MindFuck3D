from joint import *
class span:
	l = 'NULL'
	displayProps = 'NULL'
	density = 'NULL'
	def __init__(self,length, displayProps='NULL'):
		self.l = length
		self.displayProps = displayProps	
	def getMass(self):
		if self.density != 'NULL':
			return self.density*self.l
		else:
			return 'NULL'
