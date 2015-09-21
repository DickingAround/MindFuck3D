from mech_usedForTesting import *
from structureDisplay import *
from mech_walkingSimulation import *
from joint_generalHelperFunctions import *
def test_findOptimumMechWalk(short=False):
	r = True
	#Test frange	
	a = frange(1,4,4) 
	if a != [1,2,3,4]:
		print "ERROR: frange does not work correctly:%s"%a
		r = False

	#Test the maximizing function
	m = mech_usedForTesting()
	p = {}
	p['taMin'] = 0.5
	p['taMax'] = 1.9
	j = 'rta'
	refJA = m.getCockpitReferencePoint()
	refJB = m.getFootReferencePoint('r')
	grain = 100
	lengthFound = findActuatorPositionNeededToMakeJointVerticle(m,p,j,refJA,refJB,grain)
	if (lengthFound < 1.4 or lengthFound > 1.43):
		print "ERROR: Length finder did not pass it's tests"
		r = False	

	if short:
		return r
	p = {}
	p['rtinit_grainularity'] = 10.0
	p['rcinit_grainularity'] = 5.0
	p['ltinit_grainularity'] = 20.0
	p['lcinit_grainularity'] = 5.0
	p['taMin'] = 0.5
	p['taMax'] = 1.9
	p['caMin'] = 0.5
	p['caMax'] = 1.9
	p['lc1_grainularity'] = 10.0
	p['requiredHeight'] = 7.0
	p['footToFootProximity'] = 3.0/12.0
	p['maxStrideLength'] = 7.0
	p['minStrideLength'] = 3.0
	p['moveGrainularity'] = 4.0
	m = mech_usedForTesting()
	result = findOptimumMechWalkFromSimParams(m,p)
	#displayResults(result)
	
	if result[0] < 5.13 or result[0] > 5.14:
		print "ERROR: simulation efficency is incorrect: %f"%result[0]
		r = False
	if result[1]['moveDistance'] < 5.38 or result[1]['moveDistance'] > 5.39:
		print "ERROR: simulation move distance is incorrect: %f"%result[1]['moveDistance']
		r = False
	return r
