from location import *
from span import *

def movePoints(vector,locList):
	for l in locList:
		l.add(vector)
	return vector
def moveToOrigin(loc,locList):
	inv = loc.copy()
	inv.negative()
	for l in locList:
		l.add(inv)
	return inv
#WARNING: Modifies the inverse
def moveToOrigin_reverse(loc,inv):
	inv.negative()
	loc.add(inv)
def rotateYToXYPlane(loc,locList):#This function assumes we always want to move to positive X because we don't use it any other way
	rotationAngle = math.atan2(-loc.z,loc.x)
	for l in locList:
		l.rotateY(rotationAngle)
	return rotationAngle
def rotateYToXYPlane_reverse(loc,angle):
	loc.rotateY(-angle)	
def rotateZToXZPlane(loc,locList):#This fucntion assumes we always want to move to positive X because we don't use it any other way
	rotationAngle = math.atan2(loc.y,loc.x)
	for l in locList:
		l.rotateZ(rotationAngle)
	return rotationAngle
def rotateZToXZPlane_reverse(loc,angle):
	loc.rotateZ(-angle)
def rotateXToXYPlane(loc,locList,yIsPos=True):
	if(yIsPos):
		rotationAngle = math.atan2(loc.z,loc.y)
	else:
		rotationAngle = -math.atan2(loc.z,-loc.y)#We're actually going the other direction now
	for l in locList:
		l.rotateX(rotationAngle)
	return rotationAngle
def rotateXToXYPlane_reverse(loc,angle):
	loc.rotateX(-angle) 
def solveForXY(locA,lenA,locB,lenB):
       	Lab = locB.x - locA.x #Right here, we don't know the distance between the old points, we rely on them having been computed correctly.
       	Lal = lenA 
	Lpmax = lenB
	Y = tolerantSqrt(math.pow(Lpmax,2.0) - math.pow((Lal*Lal - Lab*Lab - Lpmax*Lpmax)/(-2.0*Lab),2.0))
       	#By definition of the directions chose, this point is always above the line	
	locC = location(0.0,0.0,0.0)
	locC.y = -Y #Because of the rotation we did, the Y is always in the negative in this space
	if(Lpmax*Lpmax >= (Lab*Lab + Lal*Lal)): #The angle on point 1 is going to be obtuse
		try:
			locC.x = -tolerantSqrt(Lal*Lal - Y*Y)
		except:
			print "ERROR: Lal:%f, Y:%f"%(Lal,Y)
			raise
	else:	#The angle on point 1 is acute
		try:	
			locC.x = tolerantSqrt(Lal*Lal - Y*Y)	
		except:
			print "ERROR: Lal:%f, Y:%f"%(Lal,Y)
			raise
	#print "Lpmax: %f, Lal:%f, Lab:%f, NewX:%f"%(Lpmax,Lal,Lab,locC.x)
	return locC.x, locC.y
tolerance = 0.000000001
def tolerantSqrt(a,handleExceptions=False):
	if(a < 0.0 and a > -tolerance):
		return 0
	else:
		if handleExceptions:
			if a < 0.0:
				return 'NULL'
		return math.sqrt(a)
def isEssentiallyZero(a):
	if(a > tolerance or a < -tolerance):
		return False
	else:
		return True
def copyPoints(*args):
	r = []
	for pt in args:
		r.append(pt.copy())
	return r

def frange(a,b,steps):
        r = []
        d = 1.0*(b-a)/(steps-1)
        for i in range(int(steps)):
                r.append(a+i*d) 
        return r

