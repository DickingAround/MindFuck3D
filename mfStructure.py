from joint import *
from displayProperties import *
from Exception_DuplicateNamedJoint import *
from mass import *
from Exception_UnknownJoint import *
class mfStructure(object):
	jointA = 'NULL'
	jointB = 'NULL'
	jDisplayProperties = 'NULL'
	jointList = []
	jointDictionary = {}
	collisionMargin = 0.0
	checkAllForCollisions = False
	#Special values
	#trying this - computationalTolerance = 0.00000001
	defaultDensity = 'NULL'
	defaultDisplayProperties = 'NULL'
	defaultCollisionChecking = False
	def __init__(self,nameA,locA,nameB,locB,jDispProps='NULL'):
		self.jointDictionary = {} #Having to do this annoys me
		self.jointList = []
		self.jointA = joint()
		self.jointA.name = nameA
		self.jointA.x = locA[0]
		self.jointA.y = locA[1]
		self.jointA.z = locA[2]	
		self.jointB = joint()
		self.jointB.name = nameB
		self.jointB.x = locB[0]
		self.jointB.y = locB[1]
		self.jointB.z = locB[2]	
		self.jointDictionary[self.jointA.name] = self.jointA
		self.jointDictionary[self.jointB.name] = self.jointB
		jDisplayProperties = jDispProps
		self.defaultDensity = 'NULL'
		self.defaultDisplayProperties = 'NULL'
		self.defaultCollisionChecking = False
	# ARGS: NewJointName, jointA, lengthA, jointB, lengthB, jointC, lengthC
	def addJoint(self, *args,  **kwargs):
		j = self.internal_makeJointWithNoConnections(args[0])	
		jointList = self.internal_checkJointNames([args[1],args[3],args[5]])
		isClockwise = kwargs.get('isClockwise',True)
		j.jointA = jointList[0]
		j.spanA = span(args[2])
		if isClockwise:
			j.jointB = jointList[1] 
			j.spanB = span(args[4])
			j.jointC = jointList[2] 
			j.spanC = span(args[6])
		else:
			j.jointC = jointList[1] 
			j.spanC = span(args[4])
			j.jointB = jointList[2] 
			j.spanB = span(args[6])
		j.computeDimensions = 3
		self.internal_setCollisionDetection(j,kwargs)
		self.internal_setDisplayProps(j,kwargs)#Must happen after span setting
		self.internal_setDensity(j,kwargs)
	def add2DJoint(self, *args, **kwargs):
		j = self.internal_makeJointWithNoConnections(args[0])
		jointList = self.internal_checkJointNames([args[1],args[3],args[5]])
		j.jointA = jointList[0] 
		j.jointB = jointList[1] 
		j.jointC = jointList[2]
		#if isinstance(args[5],basestring):#Are they referencing a existing location or defining a new one?
		#	self.internal_checkJointNames([args[5]])
		#	j.jointC = self.jointDictionary[args[5]]
		#else:
		#	j.jointC = location(args[5][0],args[5][1],args[5][2])
		j.spanA = span(args[2])
		j.spanB = span(args[4])
		j.farOrNear = args[6] #Must be 'f' or 'n'
		j.computeDimensions = 2
		self.internal_setCollisionDetection(j,kwargs)
		self.internal_setDisplayProps(j,kwargs)#Must happen after span setting
		self.internal_setDensity(j,kwargs)
	def add1DJoint(self, *args, **kwargs):
		j = self.internal_makeJointWithNoConnections(args[0])	
		jointList = self.internal_checkJointNames([args[1],args[3]])
		j.jointA = jointList[0]
		j.jointB = jointList[1]
		j.spanA = span(args[2])
		j.computeDimensions = 1
		self.internal_setCollisionDetection(j,kwargs)
		self.internal_setDisplayProps(j,kwargs)#Must happen after span setting
		self.internal_setDensity(j,kwargs)
	def internal_checkJointNames(self,names):
		r = []
		for name in names:
			if isinstance(name,list):
				r.append(location(name[0],name[1],name[2]))
			elif name in self.jointDictionary:
				r.append(self.jointDictionary[name])
			else:
				raise Exception_UnknownJoint(name)
		return r
	def internal_makeJointWithNoConnections(self,name):
		j = joint()
		if name in self.jointDictionary:
			raise Exception_DuplicateNamedJoint(name)
		j.name = name
		self.jointDictionary[j.name] = j
		self.jointList.append(j)
		return j
	def internal_setDisplayProps(self,j,props):
		if self.defaultDisplayProperties != 'NULL':
			if j.spanA != 'NULL':
				j.spanA.displayProps = self.defaultDisplayProperties
			if j.spanB != 'NULL':
				j.spanB.displayProps = self.defaultDisplayProperties
			if j.spanC != 'NULL':
				j.spanC.displayProps = self.defaultDisplayProperties
		#These will then override the defaults
		if 'dp' in props:
			if j.spanA != 'NULL':
				j.spanA.displayProps = props['dp']
			if j.spanB != 'NULL':
				j.spanB.displayProps = props['dp']
			if j.spanC != 'NULL':
				j.spanC.displayProps = props['dp']
		if 'dpA' in props:
			j.spanA.displayProps = props['dpA']
		if 'dpB' in props:
			j.spanB.displayProps = props['dpB']
		if 'dpC' in props:
			j.spanC.displayProps = props['dpC']
	def internal_setDensity(self,j,props):
		if self.defaultDensity != 'NULL':
			if j.spanA != 'NULL':
				j.spanA.density = self.defaultDensity
			if j.spanB != 'NULL':
				j.spanB.density = self.defaultDensity
			if j.spanC != 'NULL':
				j.spanC.density = self.defaultDensity
		#These will then override the defaults
		if 'den' in props:
			if j.spanA != 'NULL':
				j.spanA.density = props['den']
			if j.spanB != 'NULL':
				j.spanB.density = props['den']
			if j.spanC != 'NULL':
				j.spanC.density = props['den']
		if 'denA' in props:
			j.spanA.density = props['denA']
		if 'denB' in props:
			j.spanB.density = props['denB']
		if 'denC' in props:
			j.spanC.density = props['denC']
	def internal_setCollisionDetection(self,j,props):
		if self.defaultCollisionChecking:
			j.colDetectAB = True
			j.colDetectBC = True
			j.colDetectCA = True
		if 'cd' in props:
			if props['cd'] == True:
				j.colDetectAB = True
				j.colDetectBC = True
				j.colDetectCA = True
			if props['cd'] == False:
				j.colDetectAB = False
				j.colDetectBC = False
				j.colDetectCA = False
	def getSpan(self,nameA,nameB):
		jA = self.jointDictionary[nameA]
		jB = self.jointDictionary[nameB]
		if jA.jointA == jB:
			return jA.spanA
		if jA.jointB == jB:
			return jA.spanB
		if jA.jointC == jB:
			return jA.spanC
		if jB.jointA == jA:
			return jB.spanA
		if jB.jointB == jA:
			return jB.spanB
		if jB.jointC == jA:
			return jB.spanC
		else:
			return 'NULL'		
	def getJoint(self,name):
		self.internal_checkJointNames([name])
		return self.jointDictionary[name]	
	def checkForCollisions(self):
		for jointA in self.jointList:
			if jointA.colDetectAB or jointA.colDetectBC or jointA.colDetectCA or self.checkAllForCollisions:
				for jointB in self.jointList:
					if jointB.colDetectAB or jointB.colDetectBC or jointB.colDetectCA or self.checkAllForCollisions:
						if jointA.checkForCollision(jointB,self.collisionMargin):
							return True
		return False
	def computeLocations(self):
		for joint in self.jointList:
			joint.computeLocation()
	#Return: list[pointA,pointB,span)
	def getLinesList(self):
		self.computeLocations()	
		l = []
		l.append([self.jointA,self.jointB,self.jDisplayProperties])
		for j in self.jointList:
			l.append([j,j.jointA,j.spanA])
			if(j.computeDimensions == 2 or j.computeDimensions == 3):
				l.append([j,j.jointB,j.spanB])
			if(j.computeDimensions == 3): #This might be a 1D or 2D joint
				l.append([j,j.jointC,j.spanC])
		return l
	def getCenterOfMass(self):
		m = mass(0,0,0,0)
		for joint in self.jointList:
			center = joint.findAverage(joint.jointA)
			ma = joint.spanA.getMass()
			if ma != 'NULL':
				m.addMass(center.x,center.y,center.z,ma)
			if joint.computeDimensions == 2:
				center = joint.findAverage(joint.jointB)
				ma = joint.spanB.getMass()
				if ma != 'NULL':
					m.addMass(center.x,center.y,center.z,ma)
			if joint.computeDimensions == 3:
				center = joint.findAverage(joint.jointB)
				ma = joint.spanB.getMass()
				if ma != 'NULL':
					m.addMass(center.x,center.y,center.z,ma)
				center = joint.findAverage(joint.jointC)
				ma = joint.spanC.getMass()
				if ma != 'NULL':
					m.addMass(center.x,center.y,center.z,ma)
		return m
					
	def getJointPointers(self):
		print "getting pointers"
		l = []
		l.append(self.jointA)
		l.append(self.jointB)
		for j in self.jointList:
			l.append(j)
		return l
	#loc1 loc2
	#name params
	#def buildFromString(str):
	#	lines = str.split('\n')	
	#	seedLine = lines[0].split(' ')
	#	locACoords = seedLine[0].split(',')
	#	locA = location(float(locACoords[0]),float(locACoords[1]),float(locACoords[2]))
	#	locBCoords = seedLine[1].split(',')
	#	locB = location(float(locBCoords[0]),float(locBCoords[1]),float(locBCoords[2]))
	#	s = structureSeed(locA,locB)
	#	for line in lines[1::]:
	#		#Name Ds 3param, 6param
	#		params = line.split(' ')
	#		if(params[1] == 1): #line
	#			s.addJoint(
			
def test_structureSeed_pyramid():
	s = mfStructure('a',[0.0,0.0,0.0],'b',[10.0,0.0,0.0])
	s.add1DJoint('c','a',10.0,[0.0,0.0,-10.0])
	s.add1DJoint('d','b',10.0,[10.0,0.0,-10.0])
	s.addJoint('e','a',10.0,'b',10.0,'c',7.0)
	s.add1DJoint('f','a',10.0,[0.0,10.0,0.0])
	return s

def test_structureSeed():
	highLightDisProp = displayProperties([100,100,255],7)	
	s = structureSeed(location(0.0,0.0,0.0),location(-math.sqrt(2.0),0.0,0.0))#Seed spand is always assumed to lie on the X-axis, expanding onto the Y axis
	leftHipFrontJ = s.jointA
	leftHipBackJ = s.jointB
	leftActJ = s.addJoint(leftHipFrontJ, 1.0, leftHipBackJ, math.sqrt(2), location(0.0,0.0,1.0), 'f', dispPropA='hi', dispPropB='hi',dispPropC='hi')#highLightDisProp) #2D joint, with a throw-away poitn for reference	
	#leftFootJ = s.addJoint(leftHipFrontJ, 3.0, leftActJ) #Missing the last data asssumes a direction
	#The Joints moving to the middle	
	#centerTopJ = s.addJoint(leftHipFrontJ,1.0, leftHipBackJ, math.sqrt(2.0), leftActJ, math.sqrt(2.0))
	#centerBottomJ = s.addJoint(centerTopJ, 1.0,leftHipBackJ,math.sqrt(3.0),leftHipFrontJ,math.sqrt(2.0))
	#Now spanning to the right foor
	#rightHipBackJ = s.addJoint(centerTopJ, math.sqrt(2.0),leftActJ, 2.0, centerBottomJ, math.sqrt(3.0))
	#rightHipFrontJ = s.addJoint(centerTopJ, 1.0, rightHipBackJ, 1.0, centerBottomJ, math.sqrt(2.0))
	#rightActJ = s.addJoint(rightHipFrontJ, 1.0, rightHipBackJ, math.sqrt(2), centerTopJ, math.sqrt(2.0))
	#rightFootJ = s.addJoint(rightHipFrontJ, 3.0, rightActJ)	
	return s	
