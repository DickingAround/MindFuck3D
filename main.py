from mass import *
from joint import *
import joint_test as jt
from structureDisplay import *
from mech import *
from mech_walkingSimulationV2_test import *
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
			disp = structureDisplay()	
			structure = test_structureSeed_pyramid()	
			structure.computeLocations()
			disp.displayLines_animate(structure,save=False)
			#disp.displayLines(structure.getLinesList())
		elif(ar == '-rs'): #RUN SIMULATION
			findOptimumMechWalk()		
		elif(ar == '-rf'):
			m = mech(part='foot')
			m.computeLocations()
			ma = m.struct.getCenterOfMass()
			print ma.toString()
			disp = structureDisplay()
			disp.displayLines_animate(m.struct,save=False)		
		elif(ar == '-rl'):
			m = mech(part='leg')
			m.computeLocations()
			ma = m.struct.getCenterOfMass()
			print ma.toString()
			disp = structureDisplay()
			disp.displayLines_animate(m.struct,save=False)		
		elif(ar == '-ra'):
			m = mech(part='all')
			m.computeLocations()
			ma = m.struct.getCenterOfMass()
			print ma.toString()
			disp = structureDisplay()
			disp.displayLines_animate(m.struct,save=False)		
		elif(ar == '-rh'):
			m = mech(part='hipandlegs')
			m.computeLocations()
			ma = m.struct.getCenterOfMass()
			print ma.toString()
			disp = structureDisplay()
			disp.displayLines_animate(m.struct,save=False)		
		elif(ar == '-rp'):
			m = mech(part='all')
			m.moveAllActuators(1.8,1.41,0.9,1.41)
			m.computeLocations()
			co = m.checkForCollisions()
			print "Collision status is: %s"%co
			disp = structureDisplay()
			disp.displayLines_animate(m.struct,save=False)		
		elif(ar == '-rw'):
			result = [0,{'vars':[]}]
			if(len(sys.argv) == 11): #file, modifier, 9 parameters of the simulation
				for i in range(9):
					result[1]['vars'].append(sys.argv[i+2])	
			else:
				t = result[1]['vars']
				t.append(1.8429)
				t.append(1.4172)
				t.append(1.1357)
				t.append(1.8517)
				t.append(1.8517) #lc1
				t.append(1.4)
				t.append(1.4)
				t.append(1.4)
				t.append(1.4)

			#	t.append(1.8)
			#	t.append(1.4333)
			#	t.append(1.031)
			#	t.append(1.744)
			#	t.append(1.8) #lc1
			#	t.append(1.433333)
			#	t.append(1.433333)
			#	t.append(1.433333)
			#	t.append(1.433333)
		#print "Displaying a walking mech"
			displayMech_walking(result)

	#else:
	#	disp= structureDisplay()
	#	mech = mech()
	#	mech.computeLocations()
		#disp.displayLines_animate(mech.struct.getLinesList(),save=False)	
	#	disp.displayLines(mech.struct.getLinesList())	
		foo = raw_input("Press enter to exit")
	print "done"

