from mass import *
from joint import *
import joint_test as jt
from mech import *
from mech_walkingSimulationV3_test import *
from mfStructure_test import *
import time
def test_software(short=False):
	#Mass calculation testing
	p = True
	if not jt.test_joint():
		p = False 
	if not test_mass():
		p = False
	if not test_findOptimumMechWalk(short=short):
		p = False	
	if not test_mfStructure():
		p = False
	if p:	
		print "Passed tests"

if __name__ == '__main__':
	import sys
	if(len(sys.argv) > 1):
		ar = sys.argv[1]
		if(ar == '-t'):
			test_software()
			sys.exit()
		elif(ar == '-ts'):
			test_software(short=True)
			sys.exit()
		elif(ar == '-td'):
			structure = test_structureSeed_pyramid()	
			structure.computeLocations()
		elif(ar == '-rs'): #RUN SIMULATION
			findOptimumMechWalk()		
		elif(ar == '-rf'):
			m = mech(part='foot')
			m.computeLocations()
			ma = m.struct.getCenterOfMass()
			print ma.toString()
		elif(ar == '-rl'):
			m = mech(part='leg')
			m.computeLocations()
			ma = m.struct.getCenterOfMass()
			print ma.toString()
		elif(ar == '-ra'):
			m = mech(part='all')
			m.computeLocations()
			ma = m.struct.getCenterOfMass()
			print ma.toString()
		elif(ar == '-rh'):
			m = mech(part='hipandlegs')
			m.computeLocations()
			ma = m.struct.getCenterOfMass()
			print ma.toString()
		elif(ar == '-rp'):
			m = mech(part='all')
			m.moveAllActuators(1.8,1.41,0.9,1.41)
			m.computeLocations()
			co = m.checkForCollisions()
			print "Collision status is: %s"%co

	#else:
	#	disp= structureDisplay()
	#	mech = mech()
	#	mech.computeLocations()
		#disp.displayLines_animate(mech.struct.getLinesList(),save=False)	
	#	disp.displayLines(mech.struct.getLinesList())	
	print "done"

