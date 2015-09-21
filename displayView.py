import math
import sys
from location import *
class displayView():
	#Basic information about the display
	xDisplacement = 0.0
	yDisplacement = 0.0
	xSize = 0.0
	ySize = 0.0
	
	#Information about the perspective
	xRotate = 0.0 
	yRotate = 0.0	
	zRotate = 0.0 #This is unused
	margin = 1.1

	#Information about the thing being displayed
	xMin = sys.float_info.max
	xMax = -sys.float_info.max
	yMin = sys.float_info.max
	yMax = -sys.float_info.max
	zMin = sys.float_info.max
	zMax = -sys.float_info.max
	xCenter = 0.0
	xCenter = 0.0
	yCenter = 0.0

	def __init__(self,xDisp,yDisp,xSi,ySi,perspective):
		self.xSize = xSi	
		self.ySize = ySi
		self.xDisplacement = xDisp
		self.yDisplacement = yDisp
		self.xRotate = perspective[0]
		self.yRotate = perspective[1]
		self.zRotate = perspective[2]	
	def computeCenter(self):
		self.xCenter = (self.xMax + self.xMin)/2.0
		self.yCenter = (self.yMax + self.yMin)/2.0	
		self.zCenter = (self.zMax + self.zMin)/2.0
	def checkSizeAndCenter(self,loc):
		newLoc = self.rotateViewOnLocation(loc)
		#newLoc = loc
		if(newLoc.x < self.xMin):
			self.xMin = newLoc.x
		if(newLoc.x > self.xMax):
			self.xMax = newLoc.x
		if(newLoc.y < self.yMin):
			self.yMin = newLoc.y
		if(newLoc.y > self.yMax):
			self.yMax = newLoc.y
		if(newLoc.z < self.zMin):
			self.zMin = newLoc.z
		if(newLoc.z > self.zMax):
			self.zMax = newLoc.z		
		#Return the max size so far, size will be shared among all to keep perspective
		xSize = self.xMax-self.xMin
		ySize = self.yMax-self.yMin
		zSize = self.zMax-self.zMin
		#if( zSize > xSize and zSize > ySize): -- this is post-perspective
		#	return zSize
		if( xSize > ySize):
			return xSize
		else:
			return ySize
	def resetCenters(self):
		self.xMin = sys.float_info.max
		self.xMax = -sys.float_info.max
		self.yMin = sys.float_info.max
		self.yMax = -sys.float_info.max
		self.zMin = sys.float_info.max
		self.zMax = -sys.float_info.max
		
	def getDisplayCoordinates(self,structDisp,loc):
		newLoc = loc.copy()
		#Center it -- We don't center it first because the center is computed based on the perspective
		#newLoc.add(location(-self.xCenter,-self.yCenter,-self.zCenter))
		#Rotate it
		newLoc.rotateY(self.yRotate*math.pi*2.0)
		newLoc.rotateX(-self.xRotate*math.pi*2.0)
		#Resize it for display
		newLoc.add(location(-self.xCenter,-self.yCenter,0.0))#This z part doesn't matter since we already rotated
		newLoc.x = self.internal_sizeAndPlaceForDisplay(newLoc.x,structDisp.imageResize,True)
		newLoc.y = self.internal_sizeAndPlaceForDisplay(newLoc.y,structDisp.imageResize,False)
		return newLoc	
	def getDisplayCoordinates_old(self,structDisp,loc):
		#Modify to the view
		newLoc = self.rotateViewOnLocation(loc)
		#print "rotated: %s"%newLoc.toString()
		#Modify to meet the screen
		newLoc.x = self.internal_modDimension(newLoc.x,self.xCenter,structDisp.imageResize,True)	
		newLoc.y = self.internal_modDimension(newLoc.y,self.yCenter,structDisp.imageResize,False)
		return newLoc	
	def rotateViewOnLocation(self,locat):
		#TODO: Do this right later
		loc = locat.copy()
		#NOTE: I think all my rotations are actually wrong and not by the right-hand rule..
		loc.rotateY(self.yRotate*math.pi*2.0)
		loc.rotateX(-self.xRotate*math.pi*2.0)
		return loc	

	def internal_sizeAndPlaceForDisplay(self,val,size,isX):
		if(isX):
			#print "val:%f, xSize: %f, displace: %f"%(val,self.xSize,self.xDisplacement)
			val = (val/(size*self.margin))*self.xSize + self.xDisplacement + self.xSize/2.0
		else:
			val = -(val/(size*self.margin))*self.ySize + self.yDisplacement + self.ySize/2.0
		return val
	def internal_modDimension(self,val,center,size,isX):
		#Bring to the 0-1 dimension
		#print "val:%f, center:%f, size:%f, margin:%f"%(val,center,size,self.margin)	
		val = (val-center)/(size*self.margin)
		#Place on the screen
		if(isX):
			#print "val:%f, xSize: %f, displace: %f"%(val,self.xSize,self.xDisplacement)
			val = (val)*self.xSize + self.xDisplacement + self.xSize/2.0
		else:
			val = -(val)*self.ySize + self.yDisplacement + self.ySize/2.0
		return val
