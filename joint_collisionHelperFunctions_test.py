from location import *
from span import *
from mfStructure import *
from joint_collisionHelperFunctions import *
	
def test_joint_collisions():
	p = True
	# -- LINES --
	#No-check cases
	if checkForCollisionSurface(True,False,[location(0,0,0),location(1,1,1)],'NULL',[location(0,0,0),location(1,1,1)],'NULL',1.0):
		print "ERROR on joint collisions test 1"
		p = False	
	
	if checkForCollisionSurface(False,True,[location(0,0,0),location(1,1,1)],'NULL',[location(0,0,0),location(1,1,1)],'NULL',1.0):
		print "ERROR on joint collisions test 2"
		p = False	
	#Single line on top of itself
	if not checkForCollisionSurface(True,True,[location(0,0,0),location(1,1,1)],'NULL',[location(0,0,0),location(1,1,1)],'NULL',1.0):
		print "ERROR on joint collisions test 3"
		p = False	
	#Short line within a large line
	if not checkForCollisionSurface(True,True,[location(0,0,0),location(1,0.0,0.0)],'NULL',[location(0.5,0,0),location(0.6,0,0)],'NULL',0.1):
		print "ERROR on joint collisions test 4"
		p = False	
	#Short line away from the large one
	if checkForCollisionSurface(True,True,[location(0,0,0),location(1,0.0,0.0)],'NULL',[location(0.5,1,1),location(0.6,1,0)],'NULL',0.1):
		print "ERROR on joint collisions test 5"
		p = False	
	#Line coming in from the end
	if not checkForCollisionSurface(True,True,[location(0,0,0),location(1,0.0,0.0)],'NULL',[location(1.5,0.01,0.01),location(0.6,0.01,0.01)],'NULL',0.1):
		print "ERROR on joint collisions test 6"
		p = False	
	#Line coming in at an angle
	if not checkForCollisionSurface(True,True,[location(-2,-2,-2),location(2,2,2)],'NULL',[location(0.6,0.5,0.5),location(2,0,0)],'NULL',0.2):
		print "ERROR on joint collisions test 7"
		p = False	
	#Line coming in at an angle but the radius is too small
	if checkForCollisionSurface(True,True,[location(-2,-2,-2),location(2,2,2)],'NULL',[location(0.6,0.5,0.5),location(2,0,0)],'NULL',0.07):
		print "ERROR on joint collisions test 8"
		p = False	
	# -- Plane vs. line --
	#Simple plane with line through it
	if not checkForCollisionSurface(True,True,[location(0,0,0),location(0,1,0)],[location(0,0,0),location(1,0,0)],[location(0.5,0.5,-1),location(0.5,0.5,1)],'NULL',0.07):
		print "ERROR on joint collisions test 9"
		p = False	
	#Simple plane with line through it but missing
	if checkForCollisionSurface(True,True,[location(0,0,0),location(0,1,0)],[location(0,0,0),location(1,0,0)],[location(1,1,-1),location(1,1,1)],'NULL',0.07):
		print "ERROR on joint collisions test 10"
		p = False	
	#Simple plane with line getting close to it
	if not checkForCollisionSurface(True,True,[location(0,0,0),location(0,1,0)],[location(0,0,0),location(1,0,0)],[location(0.5,0.5,0.1),location(0.5,0.5,1)],'NULL',0.2):
		print "ERROR on joint collisions test 11"
		p = False	
	#Simple plane with line getting close to it but not close enough
	if checkForCollisionSurface(True,True,[location(0,0,0),location(0,1,0)],[location(0,0,0),location(1,0,0)],[location(0.5,0.5,0.3),location(0.5,0.5,1)],'NULL',0.2):
		print "ERROR on joint collisions test 12"
		p = False	
	#Simple plane with angled line from below
	if not checkForCollisionSurface(True,True,[location(0,0,0),location(0,1,0)],[location(0,0,0),location(1,0,0)],[location(1,1,1),location(0,0,-1)],'NULL',0.2):
		print "ERROR on joint collisions test 13"
		p = False	
	#Angled plane with line getting close
	if checkForCollisionSurface(True,True,[location(100,10,0),location(100,20,-40)],[location(100,10,0),location(100,0,40)],[location(0.5,0.5,0.3),location(0.5,0.5,1)],'NULL',0.2):
		print "ERROR on joint collisions test 14"
		p = False	
	#Angled plane with line hitting and edge
	if not checkForCollisionSurface(True,True,[location(100,10,0),location(100,20,-40)],[location(100,10,0),location(100,0,40)],[location(0.5,0.5,0.3),location(100,0,40)],'NULL',0.2):
		print "ERROR on joint collisions test 15"
		p = False	
	#Angled plane with line skimming the center
	if not checkForCollisionSurface(True,True,[location(100,10,0),location(0,20,-40)],[location(100,10,0),location(100,0,40)],[location(110,5.1,20),location(-10,5.0,20)],'NULL',0.2):
		print "ERROR on joint collisions test 16"
		p = False	
	#Angled plane with line skimming the center
	if checkForCollisionSurface(True,True,[location(100,10,0),location(0,20,-40)],[location(100,10,0),location(100,0,40)],[location(110,5.3,20),location(-10,5.4,20)],'NULL',0.2):
		print "ERROR on joint collisions test 17"
		p = False
	# -- Plane on plane
	#Angled plane with angled plane larger than it
	if not checkForCollisionSurface(True,True,[location(100,10,0),location(0,20,-40)],[location(100,10,0),location(100,0,40)],[location(0,0,0),location(0,100,0)],[location(0,0,0),location(1000,0,0)],0.2):
		print "ERROR on joint collisions test 18"
		p = False	
	#Angled plane with angled plane that doesn't intersect
	if checkForCollisionSurface(True,True,[location(100,10,0),location(0,20,-40)],[location(100,10,0),location(100,0,40)],[location(0,20,0),location(0,120,0)],[location(0,20,0),location(1000,20,0)],0.2):
		print "ERROR on joint collisions test 19"
		p = False	
	#Angled plane with angled plane that's in range
	if not checkForCollisionSurface(True,True,[location(0,0,0),location(-100,0,0)],[location(0,0,0),location(0,0,-100)],[location(0,-0.1,0),location(-100,-0.1,0)],[location(0,-0.1,0),location(0,-0.1,-100)],0.2):
		print "ERROR on joint collisions test 20"
		p = False	
	#Angled plane with angled plane that's not in range
	if checkForCollisionSurface(True,True,[location(0,0,0),location(-100,0,0)],[location(0,0,0),location(0,0,-100)],[location(0,-0.1,0),location(-100,-0.1,0)],[location(0,-0.1,0),location(0,-0.1,-100)],0.08):
		print "ERROR on joint collisions test 21"
		p = False	
	
	#Angled plane with angled plane that's barely in range
	if not checkForCollisionSurface(True,True,[location(0,0,0),location(-100,0,0)],[location(0,0,0),location(0,0,-100)],[location(0,-0.1,0),location(-100,-0.1,0)],[location(0,-0.1,0),location(0,-0.1,-100)],0.1001):
		print "ERROR on joint collisions test 22"
		p = False	
	#Angled plane with angled plane that's barely not in range
	if checkForCollisionSurface(True,True,[location(0,0,0),location(-100,0,0)],[location(0,0,0),location(0,0,-100)],[location(0,-0.1,0),location(-100,-0.1,0)],[location(0,-0.1,0),location(0,-0.1,-100)],0.0999):
		print "ERROR on joint collisions test 23"
		p = False
	# -- Now real objects --
	#Object that has no collisions
	s = mfStructure('a',[0,0,0],'b',[1,0,0])
	s.collisionMargin = 0.01
	s.add2DJoint('c','a',1,'b',math.sqrt(2),[0,1,0],'f',cd=True)
	s.addJoint('d','a',1,'c',math.sqrt(2),'b',math.sqrt(2),cd=True)
	s.computeLocations()
	if s.checkForCollisions():			
		print "ERROR on joint collisions test 24"
		p = False
	s.addJoint('e','a',math.sqrt(2),'d',math.sqrt(3),'c',1,cd=True)
	s.computeLocations()
	if s.checkForCollisions():
		print "ERROR on joint collisions test 25"
		p = False
	s.add1DJoint('f','a',10,'d')
	s.add2DJoint('g','f',1,'c',10,'a','f')
	s.add1DJoint('h','c',11,'g')
	s.addJoint('j','h',math.sqrt(11*11+1),'g',math.sqrt(10*10+1),'f',math.sqrt(10*10+1+1),cd=True)
	s.computeLocations()
	if not s.checkForCollisions():
		print "ERROR on joint collisions test 26"	
		p = False
#if not j.internal_checkForCollisionEdge([location(0,0,0),location(1,1,1)],[location(0.0,0.0,0.0),location(1.0,1.0,1.0)],1.0):
	#if not j.internal_checkForCollisionEdge([location(0,0,0),location(1,1,1)],[location(0.0,0.0,0.0),location(1.0,1.0,1.0)],1.0):
	#	print "ERROR on joint collisions test 4"
	#	p = False	
	#Check for various combinations of central collisions
	#Check for combinations of edge collisions
	#j.internal_checkForCollisionSurfaces(True,True,lineA,lineB,otherLineA,otherLineB,minDistance):
		
	#def internal_checkForCollisionPlane(self,lineA,lineB,colLine,minDistance,debugPrint=False):
	#def internal_checkForCollisionEdge(self,line,otherLine,minDistance):
	return p
