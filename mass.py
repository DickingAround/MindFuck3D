from location import *

class mass(location):
	m = 0.0
	def __init__(self,x,y,z,m):
		self.x = x
		self.y = y
		self.z = z
		self.m = m

	def toString(self):
		return "X:%f\tY:%f\tZ:%f\tM:%f"%(self.x,self.y,self.z,self.m)
	
	def addMass(self,x,y,z,m,debugPrint=False):
		if debugPrint:
			print "x:%s,y:%s,z:%s,m:%s"%(x,y,z,m)	
			print "self: x:%s,y:%s,z:%s,m:%s"%(self.x,self.y,self.z,self.m)	
		if(m != 0):
			self.x = (x*m)/(m+self.m) + (self.x*self.m)/(m+self.m)
			self.y = (y*m)/(m+self.m) + (self.y*self.m)/(m+self.m)
			self.z = (z*m)/(m+self.m) + (self.z*self.m)/(m+self.m)
			self.m = m+self.m #must be at the end

def test_mass():
	p = True
	m = mass(0.0,0.0,0.0,0.0)
	for x,y,z,ma in [[0,1,1,2],[6,2,5,8],[30,30,30,0],[0,1,1,2]]:
		m.addMass(x,y,z,ma)
        if(m.x != 4):
                print "ERROR on mass test 1 m.x: %f"%m.x
                p = False
        if(m.m != 12):
                print "ERROR on mass test 2 m.m: %f"%m.m
                p = False
        return p
