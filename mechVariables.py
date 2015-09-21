from displayProperties import *
import math
class mechVariables:
	#mainSpanDensity = 4.9 #Pounds per linear foot. 3"x3"x0.25" angle grad 316 with cost of $40/linear foot or $8/lb
	#heavySupportSpanDensity = 3.19 # 2"x2"x0.25" angle grade 316 with cost of $25/linear foot or $8/lb
	#lightSupportSpanDensity = 1.49 # 1"x1"x0.25" angle grade 316 with cost of $10/linear foot or $6.7/lb 
	mainSpanDensity = 1.5 #3/4" round
	heavySupportSpanDensity = 1.5 #3/4" round
	lightSupportSpanDensity = .665 #0.5" round
	
	mainSpanDispProp = displayProperties([200,200,200],1)
	heavySupportSpanDispProp = displayProperties([150,150,150],1)
	lightSupportSpanDispProp = displayProperties([100,100,100],1)
	actuatorDispProp = displayProperties([255,255,100],3)
	engineDispProp = displayProperties([100,100,100],2)

	collisionMargin = 0.009 #in feet

	legBoneXWidth = 1.0
	legBoneZWidth = 0.5
	footLength = 8.0
	footWidth = 7.0
	footHeight = 1.0

	hipTrussWidth = 1.0
	hipTrussHeight = 1.0
	hipTrussLength = 8.0  - 2.0*math.sqrt(math.pow(hipTrussWidth,2.0)-math.pow(hipTrussWidth/2.0,2.0))
	hipActuatorMount = 0.5
	hipThickness = 0.5
	hipSideSupportLength = 0.25
	hipActuatorLegDistance = 1.0
	thighActuatorLegDistance = 1.0

	hipActuatorInit = 1.0

	thighLength = 4.0
	kneeThickness = 0.5
	kneeActuatorLegDistance = 1.0
	calfActuatorLegDistance = 1.0
	calfActuatorInit = 1.0
	calfLength = 4.0

	engineWidth = 4.0
	engineHeight = 3.0
	engineLength = 4.0 

