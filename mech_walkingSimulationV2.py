from mech import *
from structureDisplay import *
	
def findOptimumMechWalk():
	p = {}
	p['rtinit_grainularity'] = 40
	p['rcinit_grainularity'] = 20.0#15
	p['ltinit_grainularity'] = 40
	p['lcinit_grainularity'] = 20.0#15
	p['taMin'] = 0.5
	p['taMax'] = 1.9
	p['caMin'] = 0.5
	p['caMax'] = 1.9	
	p['lc1_grainularity'] = 30.0
	p['requiredHeight'] = 4.0#7
	p['footToFootProximity'] = 1.0/12.0 
	p['minStrideLength'] = 1.0
	p['maxStrideLength'] = 7.0
	p['moveGrainularity'] = 15.0
	m = mech(part='all')	
	res = findOptimumMechWalkFromSimParams(m,p,showProgress=True)
	displayResults(res)

def findOptimumMechWalkFromSimParams(m,p,showProgress=True,debugPrint=False,deepCheck=True):
	
	#VALUES TO VARY: All the walk parameters, calf and thigh length
	#GOALS: Optimize stride per actuator displacement while...
        # Maintain min height of 6' off the ground - CHECKABLE - simulation1
        # Keep center of balance over feet - NOT POSSIBLE YET
        # Avoid leg collisions at any point - CHECKABLE - simulation2
	# Do not exceed max/min of any joint - IMPLICIT
	# Both feet must be at about the same level (+/-3" for now let's say) - CHECKABLE - simulation 1
	m = mech(part='all')
	resultsList = []
	#PART 1: Find all the valid combinations
	for rtinit in frange(p['taMin'],p['taMax'],p['rtinit_grainularity']):
		#print "Completed a round out of %f"%grainularity
		if showProgress:	
			print "Trying configuration rtinit:%f within taMin:%f, taMax:%f"%(rtinit,p['taMin'],p['taMax'])
		for rcinit in frange(p['caMin'],p['caMax'],p['rcinit_grainularity']):
			for ltinit in frange(p['taMin'],p['taMax'],p['ltinit_grainularity']):
				for lcinit in frange(p['caMin'],p['caMax'],p['lcinit_grainularity']):
					if debugPrint:
						print "Trying configuration rtinit:%f, rcinit:%f, ltinit:%f, lcinit:%f"%(rtinit,rcinit,ltinit,lcinit)
					results = quickCheckStepEfficiency(m,p,rtinit,rcinit,ltinit,lcinit)
					if results != 'NULL':
						resultsList.append(results)
	#PART 2: For the most efficient walk, begin testing the combinations untill you have a match
	resultsList.sort(reverse=True)
	if not deepCheck:
		return resultsList[0]
	if showProgress:
		print "Found %f possible solutions"%len(resultsList)	
	if debugPrint:
		print "We now have %f possible solutions"%len(resultsList)	
		s = "results efficency list: "
		for i in resultsList:
			s = "%s,(%f,%f)"%(s,i[0],i[1]['moveDistance'])
		print s
	finalResultsList = []
	bestResult = 'NULL'
	for i in range(len(resultsList)):
		if showProgress:
			print "Checking solution #%f of %f. So far %f found."%(i,len(resultsList),len(finalResultsList))
		if findNoCollisionStateForStep(m,p,resultsList[i]):
			print "Found a no-collision result"
			finalResultsList.append(resultsList[i])#TODO: Actually check more, given this may not really be optimal
			if bestResult != 'NULL' and resultsList[i][0] > bestResult[0]:
				bestResult = resultsList[i]
			if bestResult == 'NULL':
				bestResult = resultsList[i]
		if bestResult != 'NULL':	
			print "Showing the best result so far"
			s = displayResults(bestResult,stringOnly=True)
			print s
			print "collision distance is"
			print m.struct.collisionMargin
		#	break
	finalResultsList.sort(reverse=True)
	if showProgress:
		print "Final results list has %f possible solutions"%len(finalResultsList)
	return finalResultsList[0]
											
#Return in the form ('efficency',[list of attributes])
def quickCheckStepEfficiency(m,p,rtinit,rcinit,ltinit,lcinit,debugPrint=False):
	#Do we need to do anything other than run the build and check the distanes here? I don't think so.
	#STEP 1: Run initial position
	#STEP 2: Check criteria
	#STEP 3: RUN final position
	#STEP 4: Check criteia
	#STEP 5: Compute efficency and results

	if rtinit == ltinit and rcinit == lcinit:
		if debugPrint:
			print "The leg positions are the same. This configuration is not consdered."
		return 'NULL'	
	m.moveAllActuators(rtinit,rcinit,ltinit,lcinit)
	m.computeLocations()
	if debugPrint:
		disp=structureDisplay()
		disp.displayLines(m.struct.getLinesList())
		foo = raw_input("Press enter to exit")
	if not checkCriteria(m,p,debugPrint=debugPrint):
		return 'NULL'
	actuatorDisplacement = m.moveAllActuators(ltinit,lcinit,rtinit,rcinit)
	m.computeLocations()
	if not checkCriteria(m,p):
		return 'NULL'
	moveDistance = math.fabs(m.getFootReferencePoint('l').x - m.getFootReferencePoint('r').x)
	minHeight = m.getCockpitReferencePoint().y - m.getFootReferencePoint('r').y
	resDict = {}
	resDict['moveDistance'] = moveDistance
	resDict['actuatorDisplacement'] = actuatorDisplacement
	resDict['efficency'] = moveDistance/actuatorDisplacement
	resDict['minHeight'] = minHeight
	resDict['vars'] = [rtinit,rcinit,ltinit,lcinit]  	
	return [resDict['efficency'],resDict]

def checkCriteria(m,p,debugPrint=False):
        # Maintain min height of 6' off the ground - CHECKABLE - simulation1
	# Both feet must be at about the same level (+/-3" for now let's say) - CHECKABLE - simulation 1
	#disp=structureDisplay()
	#disp.displayLines(m.struct.getLinesList())
	#foo = raw_input("Press enter to exit")
	#print "refL: %s, refR: %s"%(m.getFootReferencePoint('l').toString(),m.getFootReferencePoint('r').toString())
	maxFootHeightDifference = p['footToFootProximity']
	minCockpitHeight = p['requiredHeight']
	if math.fabs(m.getFootReferencePoint('l').y - m.getFootReferencePoint('r').y) > maxFootHeightDifference:
		if debugPrint:
			print "Feet don't land close enough to ground: l:%f, r:%f"%(m.getFootReferencePoint('l').y,m.getFootReferencePoint('r').y)
		return False	
	if m.getCockpitReferencePoint().y - m.getFootReferencePoint('r').y < minCockpitHeight: #Max
		if debugPrint:
			print "Cockpit is too low: cockpit: %f, foot: %f"%(m.getCockpitReferencePoint().y, m.getFootReferencePoint('r').y)
		return False
	if 'minStrideLength' in p and (math.fabs(m.getFootReferencePoint('r').x-m.getFootReferencePoint('l').x) < p['minStrideLength']):
		if debugPrint:
			print "The stride is too small: %f,%f"%(m.getFootReferencePoint('l').x,m.getFootReferencePoint('r').x)
		return False
	if ('maxStrideLength' in p) and (math.fabs(m.getFootReferencePoint('r').x-m.getFootReferencePoint('l').x) > p['maxStrideLength']):
		if debugPrint:
			print "The stride is too large"
		return False
	if m.checkForCollisions():
		if debugPrint:
			print "Rejected due to collision"
		return False
	return True
	
#Return True and modify results if you find one else return false
def findNoCollisionStateForStep(m,p,result,debugPrint=True):
	#Run through each movement with the collision checker and see if we hit home. Pick the smallest movement on the lc if in fact we do have a winner. 
	bestDisplacement = sys.float_info.max
	bestLc1 = -1.0
	bestrt2 = -1.0
	bestrc3 = -1.0
	bestlt4 = -1.0
	bestlc6 = -1.0	
	for lc1 in frange(p['caMin'],p['caMax'],p['lc1_grainularity']):
		#Returns 'NULL' if no solution. Returns total displacement used otherwise. This should entirely depend on lc1 for now, but may have a big to do with other positions given some joints intentionally go 'lax'.
		if debugPrint:
			print "Checking a lc1 value lc1:%f, res1: %s"%(lc1,result[1])
		tmp = runStepMovementToCheckForCollisions(m,p,result,lc1)
		if tmp != 'NULL':
			disp,rt2,rc3,lt4,lc6 = tmp	
			if disp < bestDisplacement:
				bestLc1 = lc1
				bestrt2 = rt2
				bestrc3 = rc3
				bestlt4 = lt4
				bestlc6 = lc6
				bestDisplacement = disp
	if bestLc1 >= 0.0:
		result[1]['actuatorDisplacement'] = bestDisplacement
		result[1]['efficency'] = result[1]['moveDistance']/result[1]['actuatorDisplacement']
		result[0] = result[1]['efficency']
		result[1]['vars'].append(bestLc1)
		result[1]['vars'].append(bestrt2)
		result[1]['vars'].append(bestrc3)
		result[1]['vars'].append(bestlt4)
		result[1]['vars'].append(bestlc6)
		return True	
	if debugPrint:
		print "No results found that don't have a colision state"
	return False	
def runStepMovementToCheckForCollisions(m,p,result,lc1,debugPrint=True):
	rtinit = result[1]['vars'][0]
	rcinit = result[1]['vars'][1]
	ltinit = result[1]['vars'][2]
	lcinit = result[1]['vars'][3]
	#For the steps that rely on knowing fully upright or fully down we have to do this empyrically. There's no point building a bunch of math just for this. That's why we have a model we can do empyrical experimentation with.
	#init: right foot forward, weight centered between feet (rtinit, rcinit, ltinit, lcinit)
        #1. left calf up and forward (lc1) -- TODO:Check to assure the calf is actually a foreward position on this one, we're using it for weight distribution
        #2. right thigh pushes the whole machine to fully upright (do a search for this value)
        #3. right calf also pushes to fully upright (do a search for this value)
       	#4. left thigh draws under the weight of gravity 
	#5. left thigh pushed the rest of the way forward (rtinit)
	#6. left calf is released and set to draw under the presence of gravity.(do a search for this value) (we do this because we don't want the weight too much forward)
        #7. left calf down (rcinit) -- we don't have to check the ground distance here because we know this will work.
	#8. right calf to landing position (lcinit)
	#9. right thigh continues to ltinit, making contact with the ground. 
	#10. (not drawn) the left leg is now able to take the weight	

	#INIT
	totalDisplacement = 0.0
	grainularity = p['moveGrainularity']
	m.moveAllActuators(rtinit,rcinit,ltinit,lcinit)
	m.computeLocations()
	#STEP 1
	tmp = runActuatorMoveToCheckForCollisions(m,'lca',lc1,grainularity)
	if tmp == 'NULL':
		if debugPrint:
			print "Colission on step 1, rtinit:%f, rcinit:%f, ltinit:%f, lcinit:%f"%(rtinit,rcinit,ltinit,lcinit)
		return 'NULL'
	if m.getFootReferencePoint('l').y <= m.getFootReferencePoint('r').y:
		print "Foot reference points don't align"
		return 'NULL' #The lc1 value found is actually pushing the foot below 0
	totalDisplacement += tmp
	
	#STEP 2
	#Search for reference point to have highest position
	rt2 = findActuatorPositionNeededToMakeJointVerticle(m,p,'rta',m.getCockpitReferencePoint(),m.getFootReferencePoint('r'),grainularity)
	#Now run that position
	tmp = runActuatorMoveToCheckForCollisions(m,'rta',rt2,grainularity)
	if tmp == 'NULL':
		if debugPrint:
			print "Colission on step 2"
		return 'NULL'
	totalDisplacement += tmp
	
	#STEP 3	
	#Search for reference point to have highest position
	rc3 = findActuatorPositionNeededToMakeJointVerticle(m,p,'rca',m.getCockpitReferencePoint(),m.getFootReferencePoint('r'),grainularity)
	#Now run that position
	tmp = runActuatorMoveToCheckForCollisions(m,'rca',rc3,grainularity)
	if tmp == 'NULL':
		if debugPrint:
			print "Colission on step 3"
		return 'NULL'
	totalDisplacement += tmp
	result[1]['maxHeight'] = m.getCockpitReferencePoint().y - m.getFootReferencePoint('r').y
	
	#STEP 4
	#Searh for lowest positing of left thigh	
	lt4 = findActuatorPositionNeededToMakeJointVerticle(m,p,'lta',m.getCockpitReferencePoint(),m.getFootReferencePoint('l'),grainularity)
	#Now run that position
	tmp = runActuatorMoveToCheckForCollisions(m,'lta',lt4,grainularity)
	if tmp == 'NULL':
		if debugPrint:
			print "Colission on step 4"
		return 'NULL'
	#totalDisplacement += tmp NOTICE: we're not recording this expendature since it's drawn under the weight of gravity. I expet the feet will be heavy enough to do this.

	#STEP 5
	tmp = runActuatorMoveToCheckForCollisions(m,'lta',rtinit,grainularity)
	if tmp == 'NULL':
		if debugPrint:
			print "Colission on step 5"
		return 'NULL'
	totalDisplacement += tmp
	
	#STEP 6
	#Searh for lowest positing of left calf	
	lc6 = findActuatorPositionNeededToMakeJointVerticle(m,p,'lca',m.getCockpitReferencePoint(),m.getFootReferencePoint('l'),grainularity)
	#Now run that position
	tmp = runActuatorMoveToCheckForCollisions(m,'lca',lc6,grainularity)
	if tmp == 'NULL':
		if debugPrint:
			print "Colission on step 6"
		return 'NULL'
	#totalDisplacement += tmp NOTICE: we're not recording this expendature since it's drawn under the weight of gravity. I expet the feet will be heavy enough to do this.
	
	#STEP 7
	tmp = runActuatorMoveToCheckForCollisions(m,'lca',rcinit,grainularity)
	if tmp == 'NULL':
		if debugPrint:
			print "Colission on step 7"
		return 'NULL'
	totalDisplacement += tmp 

	#STEP 8	
	tmp = runActuatorMoveToCheckForCollisions(m,'rca',lcinit,grainularity)
	if tmp == 'NULL':
		if debugPrint:
			print "Colission on step 8"
		return 'NULL'
	#totalDisplacement += tmp THIS IS UNDER WEIGHT OF GRAVITY

	#STEP 9
	tmp = runActuatorMoveToCheckForCollisions(m,'rta',ltinit,grainularity)
	if tmp == 'NULL':
		if debugPrint:
			print "Colission on step 9"
		return 'NULL'
	#totalDisplacement += tmp THIS IS UNDER WEIGHT OF GRAVITY
	return totalDisplacement,rt2,rc3,lt4,lc6
#Only works on heights, moves the object but returns it to the origional position, returns only the angle needed to max or min the resolut. 
def findActuatorPositionNeededToMakeJointVerticle(m,p,joint,refJointA,refJointB,grainularity,debugPrint=False):
	init = m.getActuatorPosition(joint)
	idealHeight = math.fabs(refJointA.y - refJointB.y)
	actPosition = m.getActuatorPosition(joint)
	if joint[1] == 'c':#Not sure if we need the thigh or calf
		mi = p['caMin']
		ma = p['caMax']
	elif joint[1] == 't':
		mi = p['taMin']
		ma = p['taMax']
	else:
		return 'NULL' #Bad input
	for d in frange(mi,ma,grainularity):
		m.moveActuator(joint,d)
		m.computeLocations()
		t = math.fabs(refJointA.y - refJointB.y)
		if debugPrint:
			print "For actLength %f, found distance of %f"%(d,t)
		if(t > idealHeight):
			idealHeight = t
			actPosition = d	
	m.moveActuator(joint,init) #Return the actuator to it's origional position
	return actPosition

def runActuatorMoveToCheckForCollisions(m,joint,newPosition,grainularity):
	displacement = 0.0
	init = m.getActuatorPosition(joint)	
	for d in frange(init,newPosition,grainularity):
		displacement += m.moveActuator(joint,d)
		m.computeLocations()
		if m.checkForCollisions():
			print "Rejected due to collision"
			return 'NULL'
	return displacement

#def checkAngleBeforeMechWouldFallOver(m,groundJointList):
#	ma = m.getCenterOfMass()
#	for j in groundJointList:
#		#Compute the angle assuming Y is up.	

def displayResults(result,stringOnly=False):
	s = "Efficency:%f"%result[0]
	for item in result[1].items():
		if( item[0] == 'vars'):
			s += "\nrtinit,rcinit,ltinit,lcinit,lc1,rt2,rc3,lt4,lc6"
		s += "\n%s:\t%s"%(item[0],item[1])
	if stringOnly:
		return s
	else:
		print s
	if len(result[1]['vars']) > 5:
		displayMech_walking(result)
	else:
		#print "Display mech basic"
		displayMech_basic(result)
def displayMech_basic(result):
	m = mech()
	rtinit = result[1]['vars'][0]
	rcinit = result[1]['vars'][1]
	ltinit = result[1]['vars'][2]
	lcinit = result[1]['vars'][3]
	m.moveAllActuators(rtinit,rcinit,ltinit,lcinit)
	m.computeLocations()
	disp=structureDisplay()
	disp.displayLines_animate(m.struct)		
def displayMech_walking(result):
	m = mech()
	rtinit = result[1]['vars'][0]
	rcinit = result[1]['vars'][1]
	ltinit = result[1]['vars'][2]
	lcinit = result[1]['vars'][3]
	lc1 = result[1]['vars'][4]
	rt2 = result[1]['vars'][5]
	rc3 = result[1]['vars'][6]
	lt4 = result[1]['vars'][7]
	lc6 = result[1]['vars'][8]	
	lta = m.leftThighActuator
	rta = m.rightThighActuator
	lca = m.leftCalfActuator
	rca = m.rightCalfActuator
	#m.moveAllActuators(result[1]['vars'][0],result[1]['vars'][1],result[1]['vars'][2],result[1]['vars'][3])
	#m.computeLocations()
	disp=structureDisplay()
	commands = []
	commands.append([lta,ltinit,0])
	commands.append([rta,rtinit,0])
	commands.append([lca,lcinit,0])
	commands.append([rca,rcinit,0])
	commands.append([lca,lc1,10])
	commands.append([rta,rt2,10])
	commands.append([rca,rc3,10])
	commands.append([lta,lt4,10])
	commands.append([lta,rtinit,10])
	commands.append([lca,lc6,10])
	commands.append([lca,rcinit,10])
	commands.append([rca,lcinit,10])
	commands.append([rta,ltinit,10])
	#New step
	commands.append([rca,lc1,10])
	commands.append([lta,rt2,10])
	commands.append([lca,rc3,10])
	commands.append([rta,lt4,10])
	commands.append([rta,rtinit,10])
	commands.append([rca,lc6,10])
	commands.append([rca,rcinit,10])
	commands.append([lca,lcinit,10])
	commands.append([lta,ltinit,10])
	disp.displayLines_sequence(m.struct,commands,save=True)	
	#disp.displayLines_animate(m.struct.getLinesList())
	foo = raw_input("Press enter to exit")
