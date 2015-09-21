from location import *
from span import *
from joint import *
import joint_generalHelperFunctions as jgh
def computeLocation(j):
	try:
		if(j.spanB == 'NULL'): #is a line
			locD = computeLocationAsLine(j)
		elif(j.farOrNear == 'n' or j.farOrNear == 'f'): #is a 2D point
			locD = computeLocationAs2D(j)
		else: #Is a full-on 3-d joint
			locD = computeLocationAs3D(j)
		j.x = locD.x
		j.y = locD.y
		j.z = locD.z
	except:
		print "Does not compute."
		#print j.toString()
		raise

#Extending from joint A on the vector of joint B
def computeLocationAsLine(j):
	#STEP 0: Compute jointB's unit vector
	inv = j.jointA.copy()
	locA = j.jointA.copy()
	locB = j.jointB.copy()
	inv.negative()
	locB.add(inv)
	l = locB.findLength(location(0,0,0))
	#STEP 1: Multiply new span length times the unit vector
	locD = location(locA.x + locB.x * j.spanA.l/l, locA.y + locB.y * j.spanA.l/l, locA.z + locB.z * j.spanA.l/l)
	return locD

def computeLocationAs3D(j,debugPrint=False):
	#debugPrint = True
	#print "NAME IS: %s"%j.name
	#STEP 0: Copy initial points so they never drift with repeated transformations
	#STEP 1: Translate to make point 1 the origin
	#STEP 2: Rotate around Y axis till point 2 lies in Z=0 plane
	#STEP 3: Rotate around Z axis till point 2 lies in Y=0 plane (now must be on the X-axis)
	#STEP 4: Solve for point 4(new point)'s to find the X and Y. The X here will end up being the real X in this space. The Y is simply the radius.
	#STEP 5: The problem now starts over, remaking a new point A and B
	#STEP 6: Translate to make point newA's X=0
	#STEP 7: Rotate around Y axis 90 degrees to make the solution circle lie at Z=0
	#STEP 8: Rotate around Z axis till point newB liest on the Y=0 plane (it now must be on the X-axis)
	#STEP 9: Solve for point 4(new point)'s to find the new X and Y locations. The transformations we've already done will fill out all the other data found along the way.
	#STEP 10: Build the solution
	#STEP 11: Back out all transformations

	#STEP 0:	
	locA,locB,locC = copyAllJoints(j)	
	#STEP 1: 
	step1Inverse = jgh.moveToOrigin(locA,[locA,locB,locC])
	if(debugPrint):
		print "step 1"	
		print locA.toString()
		print locB.toString()
		print locC.toString()
	#STEP 2:
	step2Inverse = jgh.rotateYToXYPlane(locB,[locA,locB,locC])	 
	if(debugPrint):
		print "step 2"	
		print locA.toString()
		print locB.toString()
		print locC.toString()

	#STEP 3:
	step3Inverse = jgh.rotateZToXZPlane(locB,[locA,locB,locC])
	if(debugPrint):
		print "step 3"	
		print locA.toString()
		print locB.toString()
		print locC.toString()

	#STEP 4:
	x,y = jgh.solveForXY(locA,j.spanA.l,locB,j.spanB.l)	
	if(debugPrint):
		print "step 4"
		print "x:%f, y:%f"%(x,y)
	#STEP 5: REMAKE PROBLEM:
	#  remake A
	newSpanA = math.fabs(y)
	newLocA = location(x,0.0,0.0)
	#  remake B: it's projection onto the X=whatever plane
	newSpanB = jgh.tolerantSqrt(math.pow(j.spanC.l,2) - math.pow(locC.x - x,2))
	newLocB = location(x,locC.y, locC.z)
	if(debugPrint):
		print "step 5"	
		print newLocA.toString()
		print newLocB.toString()
		print locC.toString()
		print newSpanA
		print newSpanB

	#STEP 6:
	step6Inverse = jgh.moveToOrigin(newLocA,[newLocA,newLocB])
	if(debugPrint):
		print "step 6"	
		print newLocA.toString()
		print newLocB.toString()
		print locC.toString()

	#STEP 7:
	step7Inverse = jgh.rotateYToXYPlane(location(0.0,0.0,-1.0),[newLocA,newLocB])#newLocB,[newLocA,newLocB])
	if(debugPrint):
		print "step 7"	
		print newLocA.toString()
		print newLocB.toString()
		print locC.toString()
	#STEP 8:
	step8Inverse = jgh.rotateZToXZPlane(newLocB,[newLocA,newLocB])
	if(debugPrint):
		print "step 8"	
		print newLocA.toString()
		print newLocB.toString()
		print locC.toString()
	#STEP 9:
	newX,newY = jgh.solveForXY(newLocA,newSpanA,newLocB,newSpanB)
	if(debugPrint):
		print "X: %f,  Y: %f"%(newX,newY)
	#BUILD SOLUTION	
	locD = location(newX,-newY,0)#Why is this negative? check your right hand rules when building, the solve function goes in the negative Y when we want it positive	
	#STEP 8-inverse:
	jgh.rotateZToXZPlane_reverse(locD,step8Inverse)
	if(debugPrint):
		print "step 8 inverse"	
		print locD.toString()
	#STEP 7-inverse:	
	jgh.rotateYToXYPlane_reverse(locD,step7Inverse)	
	if(debugPrint):
		print "step 7 inverse"
		print locD.toString()
	#STEP 6-inverse:
	jgh.moveToOrigin_reverse(locD,step6Inverse)	
	if(debugPrint):
		print "step 6 inverse"
		print locD.toString()
	#STEP 3-inverse:
	jgh.rotateZToXZPlane_reverse(locD,step3Inverse)	
	if(debugPrint):
		print "step 3 inverse"
		print locD.toString()
	#STEP 2-inverse:
	jgh.rotateYToXYPlane_reverse(locD,step2Inverse)	
	if(debugPrint):
		print "step 2 inverse"
		print locD.toString()
	#STEP 1-inverse:
	jgh.moveToOrigin_reverse(locD,step1Inverse)	
	if(debugPrint):
		print "step 1 inverse"
		print locD.toString()
	#RETURN: The main function will set this object to have the location of locD
	return locD	

def computeLocationAs2D(j):
	#STEP 0: Copy initial points so they never drift with repeated transformations
	#STEP 1: Translate to make point 1 the origin
	#STEP 2: Rotate around Y axis till point 2 lies in Z=0 plane
	#STEP 3: Rotate around Z axis till point 2 lies in Y=0 plane (now must be on the X-axis)
	#STEP 4: Rotate around X axis till point 3 lies in Z=0 plane
	#STEP 4: Solve for X and Y 
	#STEP 5: Build the solution
	#STEP 6: Back out all transformations

	#STEP 0:	
	locA,locB,locC = copyAllJoints(j)	
	#STEP 1: 
	step1Inverse = jgh.moveToOrigin(locA,[locA,locB,locC])
	#STEP 2:
	step2Inverse = jgh.rotateYToXYPlane(locB,[locA,locB,locC])	 
	#STEP 3:
	step3Inverse = jgh.rotateZToXZPlane(locB,[locA,locB,locC])
	#STEP 4:
	if(j.farOrNear == 'n'):
		yIsPositive = False
	else:
		yIsPositive = True
	step4Inverse = jgh.rotateXToXYPlane(locC,[locA,locB,locC],yIsPos=yIsPositive)
	#STEP 5:
	x,y = jgh.solveForXY(locA,j.spanA.l,locB,j.spanB.l)	
	#BUILD SOLUTION	
	locD = location(x,y,0)	
	#STEP 4-inverse:
	jgh.rotateXToXYPlane_reverse(locD,step4Inverse)
	#STEP 3-inverse:
	jgh.rotateZToXZPlane_reverse(locD,step3Inverse)	
	#STEP 2-inverse:
	jgh.rotateYToXYPlane_reverse(locD,step2Inverse)	
	#STEP 1-inverse:
	jgh.moveToOrigin_reverse(locD,step1Inverse)	
	#RETURN: The main function will set this object to have the location of locD
	return locD


def copyAllJoints(j):
	return jgh.copyPoints(j.jointA,j.jointB,j.jointC)

				
def test_joint_locationComputation():
	p = True
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
