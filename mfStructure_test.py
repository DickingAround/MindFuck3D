import mfStructure as mfs
import displayProperties as dp
#import structureDisplay as sd
def test_mfStructure():
        p = True
	s = mfs.mfStructure('a',[0,0,0],'b',[1,0,0])
	s.defaultDensity = 2.0
	s.defaultDisplayProperties = dp.displayProperties([200,200,255],2)
	s.add1DJoint('c','a',0.5,[0,0,-0.5])
	s.defaultDensity = 8.0
	s.add1DJoint('d','b',0.5,[1,0,-0.5])
	s.computeLocations()
	m = s.getCenterOfMass()
	if m.x > 0.81 or m.x < 0.79 or m.y > 0.01 or m.y < -0.01 or m.z > -0.24 or m.z < -0.26 or m.m > 5.01 or m.m < 4.9:
		p = False
	#print m.toString()

###############################################################
	s = mfs.mfStructure('a',[0,0,0],'b',[10,0,0])
	s.defaultDensity = 2.0
	s.defaultDisplayProperties = dp.displayProperties([100,100,255],2)
	s.add1DJoint('c','a',5,[0,0,-5.0])
	s.add1DJoint('d','b',5,[10,0,-5.0])
	s.addJoint('e','a',10,'b',10,'c',10)
	s.computeLocations()
	m = s.getCenterOfMass()
	#print m.toString()
	#d = sd.structureDisplay() 
	#d.displayLines_animate(s)
###############################################################
	return p
