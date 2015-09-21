import math
class location:
	x = 0.0
	y = 0.0
	z = 0.0
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
	def copy(self):
		return location(self.x, self.y, self.z)
	def add(self,loc):
		self.x = self.x + loc.x
		self.y = self.y + loc.y
		self.z = self.z + loc.z
	def divide(self,n):
		self.x = self.x / n
		self.y = self.y / n
		self.z = self.z / n
	def negative(self):
		self.x = -self.x
		self.y = -self.y
		self.z = -self.z
	#All rotations are clockwise facing toward the negative axis
	def rotateY(self,angle):
		tmpX = self.x*math.cos(angle) - self.z*math.sin(angle)
		tmpZ = self.x*math.sin(angle) + self.z*math.cos(angle)
		self.x = tmpX
		self.z = tmpZ
	def rotateZ(self,angle):
                tmpY = self.y*math.cos(angle) - self.x*math.sin(angle)
                tmpX = self.y*math.sin(angle) + self.x*math.cos(angle)
                self.x = tmpX
                self.y = tmpY
	def rotateX(self,angle):
                tmpZ = self.z*math.cos(angle) - self.y*math.sin(angle)
                tmpY = self.z*math.sin(angle) + self.y*math.cos(angle)
                self.z = tmpZ
                self.y = tmpY
	def findAverage(self,otherLoc):
		cpy = self.copy()
		cpy.add(otherLoc)
		cpy.divide(2)
		return cpy
	def findLength(self,otherLoc):
		return math.sqrt(math.pow(self.x-otherLoc.x,2) + math.pow(self.y-otherLoc.y,2) + math.pow(self.z-otherLoc.z,2)) 
	def toString(self):
		return "X:%s,Y:%s,Z:%s"%(self.x,self.y,self.z)
