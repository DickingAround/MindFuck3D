from location import *
from span import *
import joint_generalHelperFunctions as jgh

def checkForCollision(firstJoint,otherJoint,minDistance):
	#STEP 1: Assure this is not the same or an adacent joint
	firstJointList = [firstJoint,firstJoint.jointA,firstJoint.jointB,firstJoint.jointC]
	otherJointList = [otherJoint,otherJoint.jointA,otherJoint.jointB,otherJoint.jointC]
	for fj in firstJointList:
		for oj in otherJointList:
			if fj != 'NULL' and oj != 'NULL' and fj == oj:
				return False #don't even check the collision
				#Note: there's a bug here in which we'll check the reference joint for 2d joints
	#STEP 2: Check for collision
	lineA = [firstJoint, firstJoint.jointA]
	lineB = [firstJoint, firstJoint.jointB]
	lineC = [firstJoint, firstJoint.jointC]
	otherLineA = [otherJoint,otherJoint.jointA]
	otherLineB = [otherJoint,otherJoint.jointB]
	otherLineC = [otherJoint,otherJoint.jointC]
	if firstJoint.computeDimensions == 1:
		if otherJoint.computeDimensions == 1:	
			if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectAB,lineA,'NULL',otherLineA,'NULL',minDistance):
				return True
		if otherJoint.computeDimensions == 2:
			if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectAB,lineA,'NULL',otherLineA,otherLineB,minDistance):
				return True
		if otherJoint.computeDimensions == 3:
			if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectAB,lineA,'NULL',otherLineA,otherLineB,minDistance):
				return True
			if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectBC,lineA,'NULL',otherLineB,otherLineC,minDistance):
				return True
			#if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectCA,lineA,'NULL',otherLineA,otherLineB,minDistance): -- not needed since we're only doing edge detection here
	if firstJoint.computeDimensions == 2:
		if otherJoint.computeDimensions == 1:	
			if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectAB,lineA,lineB,otherLineA,'NULL',minDistance):
				return True
		if otherJoint.computeDimensions == 2:
			if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectAB,lineA,lineB,otherLineA,otherLineB,minDistance):
				return True
		if otherJoint.computeDimensions == 3:	
			if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectAB,lineA,lineB,otherLineA,otherLineB,minDistance):
				return True
			if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectBC,lineA,lineB,otherLineB,otherLineC,minDistance):
				return True
			#if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectCA,lineA,lineB,otherLineC,otherLineA,minDistance): -- not needed since we're only doing edge detection here
	if firstJoint.computeDimensions == 3:	
		if otherJoint.computeDimensions == 1:
			if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectAB,lineA,lineB,otherLineA,'NULL',minDistance):
				return False
			if checkForCollisionSurface(firstJoint.colDetectBC,otherJoint.colDetectBC,lineB,lineC,otherLineA,'NULL',minDistance):
				return False
			if checkForCollisionSurface(firstJoint.colDetectCA,otherJoint.colDetectCA,lineC,lineA,otherLineA,'NULL',minDistance):
				return False
		if otherJoint.computeDimensions == 2:
			if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectAB,lineA,lineB,otherLineA,otherLineB,minDistance):
				return True
			if checkForCollisionSurface(firstJoint.colDetectBC,otherJoint.colDetectAB,lineB,lineC,otherLineA,otherLineB,minDistance):
				return True
			if checkForCollisionSurface(firstJoint.colDetectCA,otherJoint.colDetectAB,lineC,lineA,otherLineA,otherLineB,minDistance):
				return True
		if otherJoint.computeDimensions == 3:
			#AB	
			if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectAB,lineA,lineB,otherLineA,otherLineB,minDistance):
				return True
			if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectBC,lineA,lineB,otherLineB,otherLineC,minDistance):
				return True	
			if checkForCollisionSurface(firstJoint.colDetectAB,otherJoint.colDetectCA,lineA,lineB,otherLineC,otherLineA,minDistance):
				return True
			#BC
			if checkForCollisionSurface(firstJoint.colDetectBC,otherJoint.colDetectAB,lineB,lineC,otherLineA,otherLineB,minDistance):
				return True
			if checkForCollisionSurface(firstJoint.colDetectBC,otherJoint.colDetectBC,lineB,lineC,otherLineB,otherLineC,minDistance):
				return True	
			if checkForCollisionSurface(firstJoint.colDetectBC,otherJoint.colDetectCA,lineB,lineC,otherLineC,otherLineA,minDistance):
				return True
			#CA
			if checkForCollisionSurface(firstJoint.colDetectCA,otherJoint.colDetectAB,lineC,lineA,otherLineA,otherLineB,minDistance):
				return True
			if checkForCollisionSurface(firstJoint.colDetectCA,otherJoint.colDetectBC,lineC,lineA,otherLineB,otherLineC,minDistance):
				return True	
			if checkForCollisionSurface(firstJoint.colDetectCA,otherJoint.colDetectCA,lineC,lineA,otherLineC,otherLineA,minDistance):
				return True
	return False	

#Checks the plane for direct collisions with 	
def checkForCollisionSurface(detectThis,detectOther,lineA,lineB,otherLineA,otherLineB,minDistance,debugPrint=False):
	if(detectThis and detectOther): #checking every span on the other joint...	
		if checkForCollisionPlane(lineA,lineB,otherLineA,minDistance):
			if debugPrint:
				print "Collision on 1: lineA:[%s,%s], lineB:[%s,%s], otherLineA:[%s,%s], minDistance:%f"%(lineA[0].name,lineA[1].name,lineB[0].name,lineB[1].name,otherLineA[0].name,otherLineA[1].name,minDistance)	
			return True
		if checkForCollisionPlane(lineA,lineB,otherLineB,minDistance):
			if debugPrint:
				print "Collision on 2: lineA:[%s,%s], lineB:[%s,%s], otherLineB:[%s,%s], minDistance:%f"%(lineA[0].name,lineA[1].name,lineB[0].name,lineB[1].name,otherLineB[0].name,otherLineB[1].name,minDistance)	
			return True
		if checkForCollisionPlane(otherLineA,otherLineB,lineA,minDistance):
			if debugPrint:
				print "Collision on 3: otherLineA:[%s,%s], otherLineB:[%s,%s], lineA:[%s,%s], minDistance:%f"%(otherLineA[0].name,otherLineA[1].name,otherLineB[0].name,otherLineB[1].name,lineA[0].name,lineA[1].name,minDistance)	
			return True
		if checkForCollisionPlane(otherLineA,otherLineB,lineB,minDistance):
			if debugPrint:
				print "Collision on 4: otherLineA:[%s,%s], otherLineB:[%s,%s], lineB:[%s,%s], minDistance:%f"%(otherLineA[0].name,otherLinesA[1].name,otherLineB[0].name,otherLineB[1].name,lineB[0].name,lineB[1].name,minDistance)	
			return True
		if checkForCollisionEdge(lineA,otherLineA,minDistance):
			if debugPrint:
				print "Collision on 5: lineA:[%s,%s], otherLineA:[%s,%s], minDistance:%f"%(lineA[0].name,lineA[1].name,otherLineA[0].name,otherLineA[1].name,minDistance)	
			return True
		if checkForCollisionEdge(lineA,otherLineB,minDistance):
			if debugPrint:
				print "Collision on 6: lineA:[%s,%s], otherLineB:[%s,%s], minDistance:%f"%(lineA[0].name,lineA[1].name,otherLineB[0].name,otherLineB[1].name,minDistance)	
			return True
		if checkForCollisionEdge(lineB,otherLineA,minDistance):
			if debugPrint:
				print "Collision on 7: lineB:[%s,%s], otherLineA:[%s,%s], minDistance:%f"%(lineB[0].name,lineB[1].name,otherLineA[0].name,otherLineA[1].name,minDistance)	
			return True
		if checkForCollisionEdge(lineB,otherLineB,minDistance):
			if debugPrint:
				print "Collision on 8: lineB:[%s,%s], otherLineB:[%s,%s], minDistance:%f"%(lineB[0].name,lineB[1].name,otherLineB[0].name,otherLineB[1],minDistance)	
			return True
	return False
#Plane = lineA, lineB
#Line = pointA, pointB
def checkForCollisionPlane(lineA,lineB,colLine,minDistance,debugPrint=False):
	if lineA == 'NULL' or lineB == 'NULL' or colLine == 'NULL':
		return False
	#STEP 1: Copy joints
	#STEP 2: Move so that plane orig is 0,0,0
	#STEP 3: Rotate around Y axis till plane pointA is in XY-plane
	#STEP 4: Rotate around Z axis till plane pointA in X-axis
	#STEP 5: Rotate around X axis till plane pointB is in XY-plane
	#STEP 6: Near edge: For each line end, check distance to Z, if less than min distance, check the point there
	#STEP 7: Clear cross: If the line begins and end on opposite sides of Z=0, solve for Z=0 and get the X,Y	
	#STEP 8: Check if the angle from origin to this new point is smaller than the angle to plane pointB
	#STEP 9: Check if the angle from planePointA to this new point is smaller than the angle from plane pointA to plane pointB

	#STEP 1
	plo,pla,plb,la,lb = jgh.copyPoints(lineA[0],lineA[1],lineB[1],colLine[0],colLine[1])
	allPoints = [plo,pla,plb,la,lb]	
	#STEP 2
	step2Inverse = jgh.moveToOrigin(plo,allPoints)
	if(debugPrint):
		print "step 2"	
		for pt in allPoints:
			print pt.toString()
	#STEP 3:
	step3Inverse = jgh.rotateYToXYPlane(pla,allPoints)	 
	if(debugPrint):
		print "step 3"	
		for pt in allPoints:
			print pt.toString()
	#STEP 4:
	step4Inverse = jgh.rotateZToXZPlane(pla,allPoints)
	if(debugPrint):
		print "step 4"	
		for pt in allPoints:
			print pt.toString()
	#STEP 5:
	step5Inverse = jgh.rotateXToXYPlane(plb,allPoints,yIsPos=True)
	if(debugPrint):
		print "step 5"	
		for pt in allPoints:
			print pt.toString()
	
	ptsToCheck = []
	#STEP 6:
	if (math.fabs(la.z)-minDistance) < 0.0: #No need to handle near-miss/hit with a fluff factor since we already have the standoff distance. 
		tmp = la.copy()
		tmp.z = 0.0	
		ptsToCheck.append(tmp)
		if debugPrint:
			print "end point was close to plane"
	if (math.fabs(lb.z)-minDistance) < 0.0: #No need to handle near-miss/hit with a fluff factor since we already have the standoff distance. 
		tmp = lb.copy()
		tmp.z = 0.0	
		ptsToCheck.append(tmp)
		if debugPrint:
			print "end point was close to plane"
	#STEP 7:
	if (la.z < 0.0 and lb.z > 0.0) or (la.z > 0.0 and lb.z < 0.0):
		#N(X1-X2)+X2 = X
		#N(Y1-Y2)+Y2 = Y
		#N(Z1-Z2)+Z2 = 0
		tmpX = lb.x + (-lb.z/(la.z-lb.z))*(la.x-lb.x)
		tmpY = lb.y + (-lb.z/(la.z-lb.z))*(la.y-lb.y)
		tmp = location(tmpX,tmpY,0.0)
		ptsToCheck.append(tmp)
		if debugPrint:
			print "line goes clear through the plane"
	#STEP 8,9:
	for pt in ptsToCheck:
		origAngleMax = math.atan2(plb.y,plb.x)
		origAngleFound = math.atan2(pt.y,pt.x)
		farAngleMax = math.atan2(plb.y,(pla.x-plb.x))	
		farAngleFound = math.atan2(pt.y,(pla.x-pt.x))
		if(origAngleFound > 0.0 and origAngleFound < origAngleMax and farAngleFound > 0.0 and farAngleFound < farAngleMax):
			if debugPrint:
				"line goes through the surface"	
			return True
		if debugPrint:
			print "STEP 8,9: Not a hit. point:%s, origAngleMax:%f, origAngleFound:%f, farAngleMax:%f, farAngleFound:%f"%(pt.toString(),origAngleMax,origAngleFound,farAngleMax,farAngleFound)
	return False
						
def checkForCollisionEdge(line,otherLine,minDistance,debugPrint=False):
		if line == 'NULL' or otherLine == 'NULL':
			return False
		#STEP 1: Check if params exist (for some dimensions they wont and we have no work to do
		#STEP 2: Check cylinder around the line for collisions with the other line
		if checkForCollisionEdgeCylinder(line,otherLine,minDistance,debugPrint=debugPrint):
			return True
		#STEP 3: Check end points for collisions with the other line
		if checkForCollisionEdgeEndpt(line[0],otherLine,minDistance,debugPrint=debugPrint):
			return True
		if checkForCollisionEdgeEndpt(line[1],otherLine,minDistance,debugPrint=debugPrint):
			return True
		if checkForCollisionEdgeEndpt(otherLine[0],line,minDistance,debugPrint=debugPrint):
			return True
		if checkForCollisionEdgeEndpt(otherLine[1],line,minDistance,debugPrint=debugPrint):
			return True
		return False
	
def checkForCollisionEdgeCylinder(line,otherLine,minDistance,debugPrint=False):
	#debugPrint = True
	#STEP 1: Copy joints
	#STEP 2: Move so that plane orig is 0,0,0
	#STEP 3: Rotate around Y axis till line is in XY-plane
	#STEP 4: Rotate around Z axis till line is the X-axis
	# -- Span/span collision -- (if the other line penetrates the cylinder around this line, it will be caught here. But it can still come in through the ends...)	
	#STEP 5: Check X1 and Y1 to assure it's square is not zero-zero. If it is, the quad formula we'll use wont work so we'll need to give it just a quick translation	
	#STEP 6: Find the two possible collision points (care for the 1-point case)
	#STEP 7: Check each point to see if it's actually on the other line
	#STEP 8: Check each point to see if it's actually on line
	la,lb,ola,olb = jgh.copyPoints(line[0],line[1],otherLine[0],otherLine[1])
	allPoints = [la,lb,ola,olb]	
	if(debugPrint):
		print "step 1"	
		for pt in allPoints:
			print pt.toString()
	#STEP 2
	step2Inverse = jgh.moveToOrigin(la,allPoints)
	if(debugPrint):
		print "step 2"	
		for pt in allPoints:
			print pt.toString()
	#STEP 3:
	step3Inverse = jgh.rotateYToXYPlane(lb,allPoints)	 
	if(debugPrint):
		print "step 3"	
		for pt in allPoints:
			print pt.toString()
	#STEP 4:
	step4Inverse = jgh.rotateZToXZPlane(lb,allPoints)
	if(debugPrint):
		print "step 4"	
		for pt in allPoints:
			print pt.toString()

	#STEP 5:
	if ola.z*ola.z+ola.y*ola.y == 0.0:
		jgh.movePoints(location(0,1,1),allPoints)
		if debugPrint:
			print "step 5: had to move points"
	#STEP 6:
	z1 = ola.z
	y1 = ola.y
	x1 = ola.x
	z2 = olb.z
	y2 = olb.y
	x2 = olb.x
	ye = la.y #could pick either A or B since they should now be equal
	ze = la.z
	#Move everything onto x=0 since we're not acting like line is a point
	ptA,ptB = solvePointToLine(0,ye,ze,0,y1,z1,0,y2,z2,minDistance,debugPrint=debugPrint)
	if ptA == 'NULL' and ptB == 'NULL':
		if debugPrint:
			print "step 6: there's no point to be found here"
		return False
	else:
		if debugPrint:
			print "step 6: found points: %s\t%s"%(ptA.toString(),ptB.toString())
	#	Fill in the X values we ignored earlier
	if y1 != y2:
		ptA.x = ((ptA.y-y2)/(y1-y2))*(x1-x2)+x2
		ptB.x = ((ptB.y-y2)/(y1-y2))*(x1-x2)+x2
	elif z1 != z2: #if y is parallel, use z
		ptA.x = ((ptA.z-z2)/(z1-z2))*(x1-x2)+x2
		ptB.x = ((ptB.z-z2)/(z1-z2))*(x1-x2)+x2
	else: #Only ever get here if it's a perfect hit on a parallel line, which will also get picked up by the end caps
		if debugPrint:
			print "step 6: no solution for x"
		return False	
	#STEP 7:
	if (ola.findLength(ptA) > ola.findLength(olb) or olb.findLength(ptA) > olb.findLength(ola)):
		ptA = 'NULL'
		if debugPrint:
			print "step 7: eliminating pta"
	if (ola.findLength(ptB) > ola.findLength(olb) or olb.findLength(ptB) > olb.findLength(ola)):
		ptB = 'NULL'
		if debugPrint:
			print "step 7: eliminating ptb"
	#STEP 8:
	if ptA != 'NULL':
		if (ptA.x < 0.0 or ptA.x > lb.x):
			if debugPrint:
				print "step 8: eliminating pta"
			ptA = 'NULL'
	if ptB != 'NULL':
		if (ptB.x < 0.0 or ptB.x > lb.x):
			if debugPrint:
				print "step 8: eliminating ptb"
			ptB = 'NULL'		
	#RETURN 
	if ptA != 'NULL' or ptB != 'NULL':
		if debugPrint:
			print "found an edge point that collides"
		return True
	return False		

def checkForCollisionEdgeEndpt(point,otherLine,minDistance,debugPrint=False):
	#STEP 1: Copy points
	#STEP 2: Check to assure we can use the quadratic and move the points if we can't	
	#STEP 3: Compute N in the quadratic solution
	#STEP 4: Find the actual point(s)
	#STEP 5: Check to assure the point is actually on the other line
	if debugPrint:
		print "Checking edge end points"
		print "Point:%s\totherLineA:%s\totherLineB:%s"%(point.toString(),otherLine[0].toString(),otherLine[1].toString())	
	#STEP 1	
	pt,ola,olb = jgh.copyPoints(point,otherLine[0],otherLine[1])
	allPoints = [pt,ola,olb]	
	#STEP 2 - We should not need this
	#if ola.x*ola.x+ola.y*ola.y+ola.z*ola.z == 0.0:
	#	jgh.movePoints(location(1,1,1),allPoints)
	#	if debugPrint:
	#		print "step 5: had to move points"
	#STEP 1: 
	# (X-Xe)^2 + (Y-Ye)^2 + (Z-Ze)^2 = R^2
	# N*(X1-X2) + X2 = X
	# N*(Y1-Y2) + Y2 = Y
	# N*(Z1-Z2) + Z2 = Z
	x1 = ola.x
	x2 = olb.x
	y1 = ola.y
	y2 = olb.y
	z1 = ola.z
	z2 = olb.z
	xe = pt.x
	ye = pt.y
	ze = pt.z
	r = minDistance
	ptA,ptB = solvePointToLine(xe,ye,ze,x1,y1,z1,x2,y2,z2,r,debugPrint=debugPrint)
	if ptA == 'NULL' and ptB == 'NULL':
		return False
	if debugPrint:
		print "New points:%s\t%s"%(ptA.toString(),ptB.toString())
	#STEP 3:
	if (ola.findLength(ptA) > ola.findLength(olb) or olb.findLength(ptA) > olb.findLength(ola)):
		ptA = 'NULL'
	if (ola.findLength(ptB) > ola.findLength(olb) or olb.findLength(ptB) > olb.findLength(ola)):
		ptB = 'NULL'
	#RETURN 
	if ptA != 'NULL' or ptB != 'NULL':
		if debugPrint:
			print "Collision detected"
		return True
	return False		
def solvePointToLine(xe,ye,ze,x1,y1,z1,x2,y2,z2,r,debugPrint=False):
	a = (x1*x1-2*x1*x2+x2*x2) + (y1*y1-2*y1*y2+y2*y2) + (z1*z1-2*z1*z2+z2*z2)
	b = 2.0*(x1*x2-x1*xe-x2*x2+x2*xe + y1*y2-y1*ye-y2*y2+y2*ye + z1*z2-z1*ze-z2*z2+z2*ze) 
	c = x2*x2-2*x2*xe+xe*xe + y2*y2-2*y2*ye+ye*ye + z2*z2-2*z2*ze+ze*ze - r*r
	if debugPrint:
		print 'x1:%f,x2:%f,y1:%f,y2:%f,z1:%f,z2:%f,xe:%f,ye:%f,ze:%f,r:%f,a:%f,b:%f,c:%f'%(x1,x2,y1,y2,z1,z1,xe,ye,ze,r,a,b,c)
	
	#It's possible for A to become nearly zero but not quite, giving totally bad solutions as things are divided by a very small number
	if jgh.isEssentiallyZero(a) or jgh.tolerantSqrt(b*b - 4.0*a*c,handleExceptions=True) == 'NULL':
		if debugPrint:
			print "Endpts: Unable to make ptA or ptB"
		return ['NULL','NULL']
	na = (-b + jgh.tolerantSqrt(b*b - 4.0*a*c))/(2.0*a)	
	nb = (-b - jgh.tolerantSqrt(b*b - 4.0*a*c))/(2.0*a)
	#STEP 2:	
	ptA = location(na*(x1-x2)+x2,na*(y1-y2)+y2,na*(z1-z2)+z2)
	ptB = location(nb*(x1-x2)+x2,nb*(y1-y2)+y2,nb*(z1-z2)+z2)
	return ptA,ptB
