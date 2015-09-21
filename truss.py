from mfStructure import *
from structureDisplay import *
import math
from displayProperties import *

def diag(*args):
        t = 0.0
        for arg in args:
                t += sq(arg)
        return sqrt(t)
def sqrt(x):
        return math.sqrt(x)

def sq(x):
        return math.pow(x,2.0)

if __name__ == '__main__':
	#The simple struct
	totalLen = 30.0
	mountLen = 10.0
	refPt = [-1.0,0.0,0.0]
	subLen = totalLen/3.0
	stretch = 1.001448
	struct = mfStructure('lowerMount',[0,0,0],'upperMount',[0,mountLen,0])
	struct.defaultDisplayProperties = displayProperties([255,100,255],2) 
	struct.add2DJoint('lowerLoad','upperMount',stretch*diag(totalLen,mountLen),'lowerMount',totalLen,refPt,'f')
	struct.add2DJoint('upperLoad','upperMount',stretch*totalLen,'lowerLoad',mountLen,refPt,'f')
	struct.computeLocations()
	print "structure 1: upperLoad: %s"%struct.getJoint('upperLoad').toString()
	print "structure 1: lowerLoad: %s"%struct.getJoint('lowerLoad').toString()

	struct.defaultDisplayProperties = displayProperties([255,255,100],2) 
	sectb = 3.0	
	struct.add2DJoint('lowerLoad1','upperMount',stretch*diag(totalLen/sectb,mountLen),'lowerMount',totalLen/sectb,refPt,'f')
	struct.add2DJoint('upperLoad1','upperMount',stretch*totalLen/sectb,'lowerLoad1',mountLen,refPt,'f')
	struct.add2DJoint('lowerLoad2','upperLoad1',stretch*diag(totalLen/sectb,mountLen),'lowerLoad1',totalLen/sectb,refPt,'f')
	struct.add2DJoint('upperLoad2','upperLoad1',stretch*totalLen/sectb,'lowerLoad2',mountLen,refPt,'f')
	struct.add2DJoint('lowerLoad3','upperLoad2',stretch*diag(totalLen/sectb,mountLen),'lowerLoad2',totalLen/sectb,refPt,'f')
	struct.add2DJoint('upperLoad3','upperLoad2',stretch*totalLen/sectb,'lowerLoad3',mountLen,refPt,'f')

	struct.computeLocations()
	print "structure 2: upperLoad: %s"%struct.getJoint('upperLoad3').toString()
	print "structure 2: lowerLoad: %s"%struct.getJoint('lowerLoad3').toString()

	struct.defaultDisplayProperties = displayProperties([100,255,255],2)
        sectc = 6.0
        struct.add2DJoint('lowerroad1','upperMount',stretch*diag(totalLen/sectc,mountLen),'lowerMount',totalLen/sectc,refPt,'f')
        struct.add2DJoint('upperroad1','upperMount',stretch*totalLen/sectc,'lowerroad1',mountLen,refPt,'f')
        struct.add2DJoint('lowerroad2','upperroad1',stretch*diag(totalLen/sectc,mountLen),'lowerroad1',totalLen/sectc,refPt,'f')
        struct.add2DJoint('upperroad2','upperroad1',stretch*totalLen/sectc,'lowerroad2',mountLen,refPt,'f')
        struct.add2DJoint('lowerroad3','upperroad2',stretch*diag(totalLen/sectc,mountLen),'lowerroad2',totalLen/sectc,refPt,'f')
        struct.add2DJoint('upperroad3','upperroad2',stretch*totalLen/sectc,'lowerroad3',mountLen,refPt,'f')

        struct.add2DJoint('lowerroad4','upperroad3',stretch*diag(totalLen/sectc,mountLen),'lowerroad3',totalLen/sectc,refPt,'f')
        struct.add2DJoint('upperroad4','upperroad3',stretch*totalLen/sectc,'lowerroad4',mountLen,refPt,'f')
        struct.add2DJoint('lowerroad5','upperroad4',stretch*diag(totalLen/sectc,mountLen),'lowerroad4',totalLen/sectc,refPt,'f')
        struct.add2DJoint('upperroad5','upperroad4',stretch*totalLen/sectc,'lowerroad5',mountLen,refPt,'f')
        struct.add2DJoint('lowerroad6','upperroad5',stretch*diag(totalLen/sectc,mountLen),'lowerroad5',totalLen/sectc,refPt,'f')
        struct.add2DJoint('upperroad6','upperroad5',stretch*totalLen/sectc,'lowerroad6',mountLen,refPt,'f')
        
	struct.computeLocations()
        print "structure 3: upperLoad: %s"%struct.getJoint('upperroad6').toString()
        print "structure 3: lowerLoad: %s"%struct.getJoint('lowerroad6').toString()


	disp = structureDisplay()
	disp.displayLines_animate(struct,save=True)


