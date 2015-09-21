from joint import *
import joint_generalHelperFunctions as jgh
from mfStructure import *
from Exception_DuplicateNamedJoint import *
from Exception_UnknownJoint import *
def test_joint_locationComputation():
	p = True
	#Test case: Exception in joint naming: not found
	t = False
	s = mfStructure('a',[0,0,0],'b',[0,0,1])
	try:
		s.add2DJoint('c','a',1,'x',1,[0,0,10],'f')	
	except Exception_UnknownJoint:
		t = True
	if t == False:
		print "ERROR on test case -1: Joint naming"
		p = False
	
	#Test case: Exception in joint naming: Already exists
	t = False
	s = mfStructure('a',[0,0,0],'b',[0,0,1])
	try:
		s.add2DJoint('b','a',1,'b',1,[0,0,10],'f')	
	except Exception_DuplicateNamedJoint:
		t = True
	if t == False:
		print "ERROR on test case 0: Joint naming"
		p = False
	
	#Test case: Rotation
	l1 = location(0,1.0/math.sqrt(2),1.0/math.sqrt(2)) #Y=1, Z=1
	l2 = location(0,1.0/math.sqrt(2),-1.0/math.sqrt(2))
	inv = jgh.rotateXToXYPlane(l1,[l2],yIsPos=True)
	if(l2.z < -1.1 or l2.z > -0.9 or l2.y > 0.1 or l2.y < -0.1 or l2.x > 0.1 or l2.x < -0.1):
		p = False
		print "ERROR on test case 1a: %s"%l2.toString()
	jgh.rotateXToXYPlane_reverse(l2,inv)
	if(l2.z	< -0.8 or l2.z > -0.7 or l2.y > 0.8 or l2.y < 0.7):
		p = False
		print "ERROR on test case 1b: %s"%l2.toString()
	inv = jgh.rotateXToXYPlane(l1,[l2],yIsPos=False)
        if(l2.z < 0.9 or l2.z > 1.1 or l2.y > 0.1 or l2.y < -0.1 or l2.x > 0.1 or l2.x < -0.1):
                p = False
                print "ERROR on test case 1c: %s"%l2.toString()

	#Test case: Rotation
	l1 = location(0,100,-1)
	l2 = location(-1,-100,0)
	inv = jgh.rotateYToXYPlane(l1,[l2])
	if(l2.z > -0.9 or l2.z < -1.1 or l2.x > 0.1 or l2. x < -0.1):
		p = False
		print "ERROR on test case 2: %s"%l2.toString()	
	
	#Test case: Rotation
	l1 = location(-1.0,-1.0,0.0)
	l2 = location(1.0,-1.0,0)
	inv = jgh.rotateZToXZPlane(l1,[l2])
	if(l2.z < -0.1 or l2.z > 0.1 or l2.x < -0.1 or l2.x > 0.1 or l2.y > math.sqrt(2)+0.01 or l2.y < math.sqrt(2)-0.01):
		p = False
		print "ERROR on test case 3: %s"%l2.toString()	

	#Test case: Line
	j = joint()
	j.jointA = location(0,4,0)
	j.jointB = location(1,1,1)
	j.spanA = span( 2.0)
	j.computeLocation()
	if(j.x > 0.61 or j.x < 0.60 or j.y > 2.2 or j.y < 2.1 or j.z > 0.61 or j.z < 0.60):
		p = False
		print "ERROR on test case 4: %s"%j.toString()

	#Test case: 2D joint
	j = joint()
	j.jointA = location(1.0,1.0,0.0)
	j.jointB = location(0.0,1.0,0.0)	
	j.jointC = location(0.0,1.0,0.0)
	j.spanA = span(math.sqrt(2.0))
	j.spanB = span(1.0)
	j.farOrNear = 'f'
	j.computeLocation()
	if(j.x > 0.01 or j.x < -0.01 or j.y > 1.01 or j.y < -0.99 or j.z > 1.01 or j.z < 0.99):
		p = False
		print "ERROR on test case 5: %s"%j.toString()
	
	#Test case: 2D joint
	j = joint()
	j.jointA = location(0.0,1.0,0.0)	
	j.jointB = location(4.0,1.0,0.0)	
	j.jointC = location(0.5,6.0,-2.0)
	j.spanA = span(4.0)
	j.spanB = span(4.0)
	j.farOrNear = 'f'
	j.computeLocation()
	if(j.x > 2.01 or j.x < 1.99 or j.y < -2.22 or j.y > -2.21 or j.z > 1.29 or j.z < 1.285):
		p = False
		print "ERROR on test case 6: %s"%j.toString()

	#Test case: 2D joint
	j = joint()
	j.jointA = location(0.0,1.0,0.0)	
	j.jointB = location(4.0,1.0,0.0)	
	j.jointC = location(0.5,6.0,-2.0)
	j.spanA = span(4.0)
	j.spanB = span(4.0)
	j.farOrNear = 'n'
	j.computeLocation()
	if(j.x > 2.01 or j.x < 1.99 or j.y > 4.22 or j.y < 4.21 or j.z < -1.29 or j.z > -1.285):
		p = False
		print "ERROR on test case 7: %s"%j.toString()

	#Test case: 3D joint
	j = joint()
	j.jointA = location(1.0,0,0)
	j.jointB = location(0.0,1.0,0.0)
	j.jointC = location(0.0,0.0,1.0)
	j.spanA = span(1.0)
	j.spanB = span(math.sqrt(1+1+1))
	j.spanC = span(1.0)
	j.computeLocation()
	if(j.x > 1.01 or j.x < 0.99 or j.y > 0.01 or j.y < -0.01 or j.z > 1.01 or j.z < 0.99):
		p = False
		print "ERROR on test case 8: %s"%j.toString() 

	#Test case: 3D joint
	j = joint()
	j.jointA = location(0.0,2.0,2.0)
	j.jointB = location(-1.0,1.0,0.0)
	j.jointC = location(4.0,0.0,0.0)
	j.spanA = span(4.0)
	j.spanB = span(3.0)
	j.spanC = span(3.0)
	j.computeLocation()
	if(j.x > 1.198 or j.x < 1.19 or j.y > -1.013 or j.y < -1.014 or j.z > -0.34 or j.z < -0.35):
		p = False
		print "ERROR on test case 9: %s"%j.toString() 

	#Test case: 3D joint
	j = joint()
	j.jointA = location(0,0,0)
	j.jointB = location(1,0,0)
	j.jointC = location(.5,-math.sqrt(3)/2.0,0.0)
	j.spanA = span(1.0)
	j.spanB = span(math.sqrt(2.0))
	j.spanC = span(math.sqrt(2.0))
	j.computeLocation()
	if(j.x > 0.01 or j.x < -0.01 or j.y > 0.01 or j.y < -0.01 or j.z > -0.99 or j.z < -1.01):
                p = False
                print "ERROR on test case 10: %s"%j.toString()	
	return p	
