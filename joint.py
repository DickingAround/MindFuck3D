from location import *
from span import *
#import th
import joint_generalHelperFunctions as jgh
import joint_collisionHelperFunctions as jch
import joint_locationHelperFunctions as jlh

class joint(location):
	spanA = 'NULL'	
	spanB = 'NULL'
	spanC = 'NULL'
	jointA = 'NULL'
	jointB = 'NULL'
	jointC = 'NULL'
	farOrNear = 'NULL'
	computeDimensions = 0
	name = 'NULL'
	colDetectAB = False
	colDetectBC = False
	colDetectCA = False
	def __init__(self):
		#super().__init__(0.0,0.0,0.0)
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		#There is no real constructor because a joint's inital location is unknwon. It must be computed.
	def toString(self):
		#TODO: Only covers the 3D case
		if(self.computeDimensions == 3):
			s = "x,y,z: %f,%f,%f \t xA,yA,zA,span: %f,%f,%f,%f \t xB,yB,zB,span: %f,%f,%f,%f \t xC,yC,zC,span: %f,%f,%f,%f"%(self.x,self.y,self.z,self.jointA.x,self.jointA.y,self.jointA.z,self.spanA.l, self.jointB.x,self.jointB.y,self.jointB.z,self.spanB.l, self.jointC.x,self.jointC.y,self.jointC.z,self.spanC.l)
		elif(self.computeDimensions == 2):
			s = "x,y,z: %f,%f,%f \t xA,yA,zA,span: %f,%f,%f,%f \t xB,yB,zB,span: %f,%f,%f,%f \t xC,yC,zC: %f,%f,%f \t farOrNear:%s"%(self.x,self.y,self.z,self.jointA.x,self.jointA.y,self.jointA.z,self.spanA.l, self.jointB.x,self.jointB.y,self.jointB.z,self.spanB.l, self.jointC.x,self.jointC.y,self.jointC.z,self.farOrNear)
		else:
			s = "x,y,z: %f,%f,%f"%(self.x,self.y,self.z)
		return s
	def computeLocation(self):
		jlh.computeLocation(self)
	
	def checkForCollision(self,otherJoint,minDistance):
		return jch.checkForCollision(self,otherJoint,minDistance)
	
				
