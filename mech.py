from mfStructure import *
from mechVariables import *
import sys
class mech():
	struct = 'NULL'
	leftThighActuator= 'NULL'
	rightThighActuator= 'NULL'
	leftCalfActuator= 'NULL'
	rightCalfActuator= 'NULL'
	leftAnkleActuator= 'NULL'
	rightAnkleActuator= 'NULL'
	leftHipActuator= 'NULL'
	rightHipActuator= 'NULL'

	leftFootReference ='NULL'
	rightFootReference = 'NULL'
	#taMax = 1.9
	#taMin = 0.5
	#caMax = 1.9
	#caMin = 0.5	  
	def moveAllActuators(self,rtinit,rcinit,ltinit,lcinit):
		d = 0.0
		d += self.moveActuator('rta',rtinit)
		d += self.moveActuator('rca',rcinit)
		d += self.moveActuator('lta',ltinit)
		d += self.moveActuator('lca',lcinit)	
		return d
	def moveActuator(self,act,l):
		if act == 'rta':
			tmp = self.rightThighActuator.l
			self.rightThighActuator.l = l
			return math.fabs(tmp-l)	
		if act == 'lta':
			tmp = self.leftThighActuator.l		
			self.leftThighActuator.l = l		
			return math.fabs(tmp-l)
		if act == 'rca':
			tmp = self.rightCalfActuator.l		
			self.rightCalfActuator.l = l		
			return math.fabs(tmp-l)
		if act == 'lca':
			tmp = self.leftCalfActuator.l		
			self.leftCalfActuator.l = l	
			return math.fabs(tmp-l)	
	def getActuatorPosition(self,act):
		if act == 'rta':
			return self.rightThighActuator.l
		if act == 'lta':
			return self.leftThighActuator.l		
		if act == 'rca':
			return self.rightCalfActuator.l		
		if act == 'lca':
			return self.leftCalfActuator.l		
	def getCockpitReferencePoint(self):
		return self.struct.getJoint('leftBodyActuatorPost')	
	def getFootReferencePoint(self,lOrR):
		if lOrR == 'l':
			return self.struct.getJoint('leftFootActuator')
		if lOrR == 'r':
			return self.struct.getJoint('rightFootActuator')
		else:
			return 'NULL'	
	def setDefaultDensityBasedOnAngleSteel(self,thicknessInInches,widthInInches):
		densityOfSteel = 490 #lb/cuft
		#Assumes distances in feet
		areaInInches = thicknessInInches*(widthInInches + (widthInInches-thicknessInInches))
		self.struct.defaultDensity = areaInInches/(12.0*12.0) * densityOfSteel
	def computeLocations(self):
		self.struct.computeLocations()
	def checkForCollisions(self):
		return self.struct.checkForCollisions()
	
	def __init__(self, part='all'):
		if part == 'all':
			self.internal_addMech()	
			#self.internal_addMech()
		elif part == 'foot':
			self.internal_addFootOnly() #legBoneXWidth, legBoneZWidth,footLength,footWidth,footHeight,footDispProp,actDispProp,isLeftFoot):
		elif part == 'leg':
			self.internal_addLegOnly()
		elif part == 'hipandlegs':
			self.internal_addHipAndLegs()

	def internal_addMech(self):
		self.internal_addHipAndLegs()
		self.internal_addEngine()
		s = self.struct
		self.leftHipActuator = s.getSpan('leftBodyActuatorPost','leftHipActuatorPost')
		self.rightHipActuator = s.getSpan('rightBodyActuatorPost','leftHipActuatorPost')
		self.leftThighActuator = s.getSpan('leftHipActuator','leftThighActuator')
		self.rightThighActuator = s.getSpan('rightHipActuator','rightThighActuator')
		self.leftCalfActuator = s.getSpan('leftKneeActuator','leftCalfActuator')
		self.rightCalfActuator = s.getSpan('rightKneeActuator','rightCalfActuator')
		self.leftAnkleActuator = s.getSpan('leftAnkleActuator','leftFootActuator')
		self.rightAnkleActuator = s.getSpan('rightAnkleActuator','rightFootActuator')
	
	def internal_addMechOld(self):
		#Leg attributes	
		actThighInit = 0.5
		actCalfInit = 0.5
		actRightThighInit = 0.5
		actRightCalfInit = 0.5
		actHipDis = 1.0
		actThighDis = 1.0
		actKneeDis = 1.0
		actCalfDis = 1.0
		thighLen = 4.0
		calfLen = 4.0
		legBoneDis = 2.0
		hipWidth = 8.0
		#DISPLAY PROPS
		leftLegDispProp = displayProperties([200,200,255],2)
		rightLegDispProp = leftLegDispProp
		rightFootDispProp = displayProperties([100,100,255],2)	
		leftFootDispProp = rightFootDispProp
		actDispProp = displayProperties([255,255,100],4)	
		hipDispProp = displayProperties([255,100,100],2)
		#BUILD IT!	
		self.struct = mfStructure('leftHipBack',[0,0,0],'leftHipActuator',[actHipDis,0,0])
		s = self.struct	
		s.collisionMargin = 0.5
		s.defaultDisplayProperties = leftLegDispProp
		self.setDefaultDensityBasedOnAngleSteel(0.25,2) 
		#LEFT LEG
		s.add2DJoint('leftThighActuator','leftHipBack',actThighDis,'leftHipActuator',actThighInit,[0,1,0],'f',dpB=actDispProp)
		self.leftThighActuator = s.getSpan('leftThighActuator','leftHipActuator')
		s.add1DJoint('leftKneeBack','leftHipBack',thighLen,'leftThighActuator')
		s.add1DJoint('leftHipFront','leftHipActuator',legBoneDis+actHipDis,'leftHipBack')
		s.add2DJoint('leftKneeFront','leftHipFront',thighLen,'leftKneeBack',legBoneDis,'leftHipBack','f')
		s.add2DJoint('leftKneeBrace','leftKneeBack',math.sqrt(1.0+legBoneDis*legBoneDis),'leftKneeFront',1.0,'leftHipBack','n')
		s.add2DJoint('leftKneeActuator','leftKneeBrace',math.sqrt(1.0+actKneeDis*actKneeDis),'leftKneeFront',actKneeDis,'leftKneeBack','f')
		s.add2DJoint('leftCalfActuator','leftKneeActuator',actCalfInit,'leftKneeFront',actCalfDis,'leftKneeBrace','f',dpA=actDispProp)
		self.leftCalfActuator = s.getSpan('leftCalfActuator','leftKneeActuator') 
		s.add1DJoint('leftAnkleFront','leftKneeFront',calfLen,'leftCalfActuator')
		s.add2DJoint('leftAnkleBack','leftAnkleFront',legBoneDis,'leftKneeBack',calfLen,'leftKneeActuator','f')	
		#LEFT FOOT
		footHeight = 1.0
		footThickness = 0.6	
		footPadWidth = 1.0
		footWidth = 6.0
		footLength = 8.0
		s.defaultDisplayProperties = leftFootDispProp
		s.add2DJoint('leftFootPivotBackTop','leftAnkleFront',sqrt(sq(legBoneDis)+sq(footHeight)),'leftAnkleBack',footHeight,'leftKneeFront','f',dpB=actDispProp)
		self.leftAnkleActuator = s.getSpan('leftAnkleBack','leftKneeFront')
		s.add2DJoint('leftFootPivotFrontTop','leftAnkleFront',sqrt(sq(legBoneDis)+sq(footHeight)),'leftFootPivotBackTop',legBoneDis*2,'leftAnkleBack','f')
		s.add2DJoint('leftFootPivotFrontBottom','leftFootPivotFrontTop',footThickness,'leftFootPivotBackTop',sqrt(sq(footThickness)+sq(legBoneDis*2)),'leftAnkleFront','f')
		s.add2DJoint('leftFootPivotBackBottom','leftFootPivotBackTop',footThickness,'leftFootPivotFrontTop',sqrt(sq(footThickness)+sq(legBoneDis*2)),'leftAnkleBack','f')
		s.add1DJoint('leftFootToeFrontTop','leftFootPivotBackTop',footLength/2.0+legBoneDis,'leftFootPivotFrontTop')
		s.add1DJoint('leftFootToeFrontBottom','leftFootPivotBackBottom',footLength/2.0+legBoneDis,'leftFootPivotFrontBottom')
		s.add1DJoint('leftFootToeFrontBottomNear','leftFootPivotBackBottom',footLength/2.0-footPadWidth+legBoneDis,'leftFootPivotFrontBottom')
		s.addJoint('leftFootPointyToeFront','leftFootToeFrontBottomNear',sqrt(sq(footPadWidth)+sq(footWidth)),'leftFootToeFrontBottom',footWidth,'leftFootToeFrontTop',sqrt(sq(footWidth)+sq(footThickness)),cd=True)
		s.add1DJoint('leftFootToeBackTop','leftFootPivotFrontTop',footLength/2.0+legBoneDis,'leftFootPivotBackTop')
		s.add1DJoint('leftFootToeBackBottom','leftFootPivotFrontBottom',footLength/2.0+legBoneDis,'leftFootPivotBackBottom')
		s.add1DJoint('leftFootToeBackBottomNear','leftFootPivotFrontBottom',footLength/2.0-footPadWidth+legBoneDis,'leftFootPivotBackBottom')
		s.addJoint('leftFootPointyToeBack','leftFootToeBackBottom',footWidth,'leftFootToeBackBottomNear',sqrt(sq(footPadWidth)+sq(footWidth)),'leftFootToeBackTop',sqrt(sq(footWidth)+sq(footThickness)),cd=True)	

		#HIP
		legHipSupportLen = 1.0
		legHipWingLen = 0.5
		hipPostLowerPoint = 0.1
		hipPostUpperPoint = 1.0
		hipCockpitDis = 1.0
		cockpitWidth = 6.0
		actHipInit = sqrt(sq(hipCockpitDis)+sq(actHipDis))
		# Main leg supports
		s.addJoint('leftHipSupportBack','leftHipBack',legHipSupportLen,'leftHipActuator', sqrt( sq(legHipSupportLen) + sq(actHipDis)),'leftThighActuator', sqrt(sq(actThighDis)+sq(legHipSupportLen)))
		s.add1DJoint('leftSupportAttachFront','leftHipFront',actThighDis,'leftKneeFront')	
		s.addJoint('leftHipSupportFront','leftHipFront',legHipSupportLen,'leftHipBack', sqrt(sq(legBoneDis)+sq(legHipSupportLen)),'leftSupportAttachFront', sqrt(sq(actThighDis)+sq(legHipSupportLen)))
		# Hip post 
		s.addJoint('leftHipWingBack','leftThighActuator',sqrt(sq(actThighDis)+sq(legHipWingLen)),'leftHipBack',legHipWingLen,'leftHipFront',sqrt(sq(legBoneDis)+sq(legHipWingLen)))
		s.addJoint('leftHipPostUpper','leftHipBack',hipPostUpperPoint,'leftHipFront',sqrt(sq(legBoneDis)+sq(hipPostUpperPoint)),'leftHipWingBack',sqrt(sq(legHipWingLen)+sq(hipPostUpperPoint)))
		s.addJoint('leftHipActuatorPost','leftHipBack',sqrt(sq(hipPostUpperPoint)+sq(actHipDis)),'leftHipActuator',hipPostUpperPoint,'leftHipPostUpper',actHipDis)
		# Hip center	
		s.defaultDisplayProperties = hipDispProp	
		s.addJoint('leftHipCockpitUpper','leftHipPostUpper',hipCockpitDis,'leftHipActuatorPost',actHipInit,'leftHipBack',sqrt(sq(hipCockpitDis)+sq(hipPostUpperPoint)),dpA=actDispProp)
		self.leftHipActuator = s.getSpan('leftHipCockpitUpper','leftHipPostUpper')	
		s.addJoint('leftHipCockpitLower','leftHipCockpitUpper',hipPostUpperPoint,'leftHipBack',hipCockpitDis,'leftHipPostUpper',sqrt(sq(hipCockpitDis)+sq(hipPostUpperPoint)))
		s.add1DJoint('rightHipCockpitUpper','leftHipPostUpper',cockpitWidth+hipCockpitDis,'leftHipCockpitUpper')
		s.add1DJoint('rightHipCockpitLower','leftHipBack',cockpitWidth+hipCockpitDis,'leftHipCockpitLower')
		s.add2DJoint('rightHipPostUpper','rightHipCockpitUpper',hipCockpitDis,'rightHipCockpitLower',sqrt(sq(hipCockpitDis)+sq(hipPostUpperPoint)),'leftHipCockpitLower','f')
		s.add2DJoint('rightHipBack','rightHipCockpitLower',hipCockpitDis,'rightHipCockpitUpper',sqrt(sq(hipCockpitDis)+sq(hipPostUpperPoint)),'leftHipCockpitUpper','f')
		# Hip post
		s.defaultDisplayProperties = rightLegDispProp
		s.addJoint('rightHipActuatorPost','rightHipBack',sqrt(sq(actHipDis)+sq(hipPostUpperPoint)),'rightHipPostUpper',actHipDis,'rightHipCockpitUpper',actHipInit,dpC=actDispProp)	
		self.rightHipActuator = s.getSpan('rightHipCockpitUpper','leftHipPostUpper')	
		s.addJoint('rightHipActuator','rightHipActuatorPost',hipPostUpperPoint,'rightHipBack',actHipDis,'rightHipPostUpper',sqrt(sq(hipPostUpperPoint)+sq(actHipDis)))
		#RIGHT LEG
		s.addJoint('rightHipWingBack','rightHipPostUpper',sqrt(sq(hipPostUpperPoint)+sq(legHipWingLen)),'rightHipActuator',sqrt(sq(legHipWingLen)+sq(actHipDis)),'rightHipBack',legHipWingLen)
		s.addJoint('rightThighActuator','rightHipActuator',actRightThighInit,'rightHipBack',actThighDis,'rightHipWingBack',sqrt(sq(legHipWingLen)+sq(actThighDis)),dpA=actDispProp)
		self.rightThighActuator = s.getSpan('rightThighActuator','rightHipActuator')
                s.add1DJoint('rightKneeBack','rightHipBack',thighLen,'rightThighActuator')
		s.add1DJoint('rightHipFront','rightHipActuator',legBoneDis+actHipDis,'rightHipBack')
                s.add2DJoint('rightKneeFront','rightHipFront',thighLen,'rightKneeBack',legBoneDis,'rightHipBack','f')
                s.add2DJoint('rightKneeBrace','rightKneeBack',math.sqrt(1.0+legBoneDis*legBoneDis),'rightKneeFront',1.0,'rightHipBack','n')
                s.add2DJoint('rightKneeActuator','rightKneeBrace',math.sqrt(1.0+actKneeDis*actKneeDis),'rightKneeFront',actKneeDis,'rightKneeBack','f')
                s.add2DJoint('rightCalfActuator','rightKneeActuator',actRightCalfInit,'rightKneeFront',actCalfDis,'rightKneeBrace','f',dpA=actDispProp)
		self.rightCalfActuator = s.getSpan('rightCalfActuator','rightKneeActuator')
                s.add1DJoint('rightAnkleFront','rightKneeFront',calfLen,'rightCalfActuator')
                s.add2DJoint('rightAnkleBack','rightAnkleFront',legBoneDis,'rightKneeBack',calfLen,'rightKneeActuator','f')	
		s.add1DJoint('rightSupportAttachFront','rightHipFront',actThighDis,'rightKneeFront')	
		s.addJoint('rightHipSupportFront','rightHipBack',sqrt(sq(legBoneDis)+sq(legHipSupportLen)),'rightHipFront',legHipSupportLen,'rightSupportAttachFront',sqrt(sq(actThighDis)+sq(legHipSupportLen)))
		s.addJoint('rightHipSupportBack','rightHipActuator',sqrt(sq(actHipDis)+sq(legHipSupportLen)),'rightHipBack',legHipSupportLen,'rightThighActuator',sqrt(sq(actThighDis)+sq(legHipSupportLen)))
		#RIGHT FOOT
		s.defaultDisplayProperties = rightFootDispProp
		s.add2DJoint('rightFootPivotBackTop','rightAnkleFront',sqrt(sq(legBoneDis)+sq(footHeight)),'rightAnkleBack',footHeight,'rightKneeFront','f',dpB=actDispProp)
		self.rightAnkleActuator = s.getSpan('rightFootPivotBackTop','rightAnkleBack')
		s.add2DJoint('rightFootPivotFrontTop','rightAnkleFront',sqrt(sq(legBoneDis)+sq(footHeight)),'rightFootPivotBackTop',legBoneDis*2,'rightAnkleBack','f')
		s.add2DJoint('rightFootPivotFrontBottom','rightFootPivotFrontTop',footThickness,'rightFootPivotBackTop',sqrt(sq(footThickness)+sq(legBoneDis*2)),'rightAnkleFront','f')
		s.add2DJoint('rightFootPivotBackBottom','rightFootPivotBackTop',footThickness,'rightFootPivotFrontTop',sqrt(sq(footThickness)+sq(legBoneDis*2)),'rightAnkleBack','f')
		s.add1DJoint('rightFootToeFrontTop','rightFootPivotBackTop',footLength/2.0+legBoneDis,'rightFootPivotFrontTop')
		s.add1DJoint('rightFootToeFrontBottom','rightFootPivotBackBottom',footLength/2.0+legBoneDis,'rightFootPivotFrontBottom')
		s.add1DJoint('rightFootToeFrontBottomNear','rightFootPivotBackBottom',footLength/2.0-footPadWidth+legBoneDis,'rightFootPivotFrontBottom')
		s.addJoint('rightFootPointyToeFront','rightFootToeFrontBottom',footWidth,'rightFootToeFrontBottomNear',sqrt(sq(footPadWidth)+sq(footWidth)),'rightFootToeFrontTop',sqrt(sq(footWidth)+sq(footThickness)),cd=True)
		s.add1DJoint('rightFootToeBackTop','rightFootPivotFrontTop',footLength/2.0+legBoneDis,'rightFootPivotBackTop')
		s.add1DJoint('rightFootToeBackBottom','rightFootPivotFrontBottom',footLength/2.0+legBoneDis,'rightFootPivotBackBottom')
		s.add1DJoint('rightFootToeBackBottomNear','rightFootPivotFrontBottom',footLength/2.0-footPadWidth+legBoneDis,'rightFootPivotBackBottom')
		s.addJoint('rightFootPointyToeBack','rightFootToeBackBottomNear',sqrt(sq(footPadWidth)+sq(footWidth)),'rightFootToeBackBottom',footWidth,'rightFootToeBackTop',sqrt(sq(footWidth)+sq(footThickness)),cd=True)			


	def internal_addHipAndLegs(self):
		self.internal_addLegOnly()
		mv = mechVariables()
		s = self.struct
		s.collisionMargin = mv.collisionMargin
		s.addJoint('rightUpperFrontHipTruss','leftUpperFrontHipTruss',mv.hipTrussLength,'leftUpperBackHipTruss',diag(mv.hipTrussLength,mv.hipTrussWidth),'leftLowerFrontHipTruss',diag(mv.hipTrussLength,mv.hipTrussHeight))
		s.addJoint('rightLowerBackHipTruss','leftUpperBackHipTruss',diag(mv.hipTrussLength,mv.hipTrussHeight),'leftLowerBackHipTruss',mv.hipTrussLength,'leftLowerFrontHipTruss',diag(mv.hipTrussLength,mv.hipTrussWidth))
		s.addJoint('rightUpperBackHipTruss','leftUpperBackHipTruss',mv.hipTrussLength,'rightLowerBackHipTruss',mv.hipTrussHeight,'rightUpperFrontHipTruss',mv.hipTrussWidth)
		s.addJoint('rightLowerFrontHipTruss','leftLowerFrontHipTruss',mv.hipTrussLength,'rightUpperFrontHipTruss',mv.hipTrussHeight,'rightLowerBackHipTruss',mv.hipTrussWidth)
		self.internal_addLeg(mv,False)

	#	
	def internal_addCockpit(self,mv):
		s = self.struct
				

	def internal_addEngine(self):
		s = self.struct
		mv = mechVariables()
		s.defaultDisplayProperties = mv.engineDispProp
		#TODO: Remove the weight of the mountings
		s.add1DJoint('leftFrontEngineMount','leftLowerFrontHipTruss',(mv.hipTrussLength-mv.engineWidth)/2.0,'rightLowerFrontHipTruss')
		s.add1DJoint('rightFrontEngineMount','rightLowerFrontHipTruss',(mv.hipTrussLength-mv.engineWidth)/2.0,'leftLowerFrontHipTruss')
		s.add1DJoint('leftBackEngineMount','leftLowerBackHipTruss',(mv.hipTrussLength-mv.engineWidth)/2.0,'rightLowerBackHipTruss')
		s.add1DJoint('rightBackEngineMount','rightLowerBackHipTruss',(mv.hipTrussLength-mv.engineWidth)/2.0,'leftLowerBackHipTruss')
		#Make the upper points on the engines
		s.add1DJoint('leftTopFrontEngine','leftBackEngineMount',(mv.hipTrussWidth/2.0 + mv.engineLength/2.0),'leftFrontEngineMount')
		s.add1DJoint('leftTopBackEngine','leftFrontEngineMount',(mv.hipTrussWidth/2.0 + mv.engineLength/2.0),'leftBackEngineMount')
		s.add1DJoint('rightTopFrontEngine','rightBackEngineMount',(mv.hipTrussWidth/2.0 + mv.engineLength/2.0),'rightFrontEngineMount')
		s.add1DJoint('rightTopBackEngine','rightFrontEngineMount',(mv.hipTrussWidth/2.0 + mv.engineLength/2.0),'rightBackEngineMount')
		#Make the lower points on the engines
		s.addJoint('rightBottomFrontEngine','rightTopFrontEngine',mv.engineHeight,'rightTopBackEngine',diag(mv.engineHeight,mv.engineLength),'leftTopFrontEngine',diag(mv.engineWidth,mv.engineHeight))
		s.addJoint('leftBottomFrontEngine','leftTopFrontEngine',mv.engineHeight,'rightTopFrontEngine',diag(mv.engineWidth,mv.engineHeight),'leftTopBackEngine',diag(mv.engineHeight,mv.engineLength))
		s.addJoint('leftBottomBackEngine','leftTopBackEngine',mv.engineHeight,'leftTopFrontEngine',diag(mv.engineHeight,mv.engineLength),'rightTopBackEngine',diag(mv.engineWidth,mv.engineHeight))
		s.addJoint('rightBottomBackEngine','rightTopBackEngine',mv.engineHeight,'leftTopBackEngine',diag(mv.engineHeight,mv.engineWidth),'rightTopFrontEngine',diag(mv.engineHeight,mv.engineLength))



	def internal_addLegOnly(self):
		mv = mechVariables()
		self.struct = mfStructure('leftUpperFrontHipTruss',[0,0,0],'leftUpperBackHipTruss',[mv.hipTrussWidth,0,0])
		s = self.struct
		s.defaultDisplayProperties = mv.mainSpanDispProp
		s.defaultDensity = mv.mainSpanDensity
		s.collisionMargin = mv.collisionMargin
		s.add1DJoint('leftLowerFrontHipTruss','leftUpperFrontHipTruss',mv.hipTrussHeight,[0.0,-1.0,0.0])
		s.add1DJoint('leftLowerBackHipTruss','leftUpperBackHipTruss',mv.hipTrussHeight,[mv.hipTrussWidth,-1.0,0.0])
		self.internal_addLeg(mv,True)
	#INPUTS
	# leftUpperFrontHipTruss
	# leftUpperBackHipTruss
	# leftLowerFrontHipTruss
	# leftLowerBackHipTruss
	#OUTPUTS	
	# leftOuterBackHip
	# leftOuterFrontHip
	# leftInnerBackHip
	# leftInnerFrontHip
	def internal_addLeg(self,mv,isLeft):
		self.internal_addHipJoint(mv,isLeft)
		self.internal_addThighAndCalf(mv,isLeft)

	def internal_addHipJoint(self,mv,isLeft):
		s = self.struct
		if isLeft:
			fs = 'left'
			isClockwise=False
		else:
			fs = 'right'
			isClockwise=True
		s.addJoint(fs+'UpperHipPost',fs+'UpperFrontHipTruss',mv.hipTrussWidth,fs+'UpperBackHipTruss',mv.hipTrussWidth,fs+'LowerFrontHipTruss',diag(mv.hipTrussWidth,mv.hipTrussHeight), isClockwise=isClockwise)
		s.addJoint(fs+'LowerHipPost',fs+'UpperFrontHipTruss',diag(mv.hipTrussWidth,mv.hipTrussHeight),fs+'LowerBackHipTruss',mv.hipTrussWidth,fs+'LowerFrontHipTruss',mv.hipTrussWidth, isClockwise=isClockwise)
		s.addJoint(fs+'BodyActuatorPost',fs+'LowerFrontHipTruss',diag(mv.hipTrussWidth,mv.hipTrussHeight/2.0),fs+'LowerBackHipTruss',mv.hipTrussHeight/2.0,fs+'LowerHipPost',diag(mv.hipTrussWidth,mv.hipTrussHeight/2.0),isClockwise=isClockwise)
		s.addJoint(fs+'HipActuatorPost',fs+'BodyActuatorPost',sqrt(sq(mv.hipTrussWidth)-sq(mv.hipActuatorMount)),fs+'LowerHipPost',diag(mv.hipTrussHeight/2.0,mv.hipActuatorMount),fs+'UpperHipPost',diag(mv.hipTrussHeight/2.0,mv.hipActuatorMount),isClockwise=isClockwise, dpA=mv.actuatorDispProp)
		s.add2DJoint(fs+'LowerHipActuatorPost',fs+'HipActuatorPost',mv.hipTrussHeight/2.0,fs+'LowerHipPost',mv.hipActuatorMount,fs+'UpperHipPost','f')
		s.add1DJoint(fs+'FrontHip',fs+'LowerHipActuatorPost',mv.hipActuatorMount+mv.legBoneXWidth,fs+'LowerHipPost')
		s.add1DJoint(fs+'OuterBackHip',fs+'UpperHipPost',mv.hipTrussHeight+mv.hipThickness,fs+'LowerHipPost')
		s.addJoint(fs+'OuterFrontHip',fs+'OuterBackHip',mv.legBoneXWidth,fs+'FrontHip',mv.hipThickness,fs+'LowerHipPost',diag(mv.legBoneXWidth,mv.hipThickness),isClockwise=isClockwise)
		s.addJoint(fs+'InnerFrontHip',fs+'FrontHip',diag(mv.hipThickness,mv.legBoneZWidth),fs+'OuterFrontHip',mv.legBoneZWidth,fs+'LowerHipPost',diag(mv.hipThickness,mv.legBoneZWidth,mv.legBoneXWidth),isClockwise=isClockwise)
		s.addJoint(fs+'InnerBackHip',fs+'InnerFrontHip',mv.legBoneXWidth,fs+'OuterBackHip',mv.legBoneZWidth,fs+'LowerHipPost',diag(mv.legBoneZWidth,mv.hipThickness),isClockwise=isClockwise)
		s.addJoint(fs+'HipSideSupport',fs+'OuterBackHip',mv.hipSideSupportLength,fs+'OuterFrontHip',diag(mv.hipSideSupportLength,mv.legBoneXWidth),fs+'UpperHipPost',diag(mv.hipSideSupportLength,mv.hipTrussHeight+mv.hipThickness),isClockwise=isClockwise)
		s.addJoint(fs+'HipActuator',fs+'LowerHipActuatorPost',diag(math.fabs(mv.hipActuatorLegDistance-mv.hipActuatorMount),mv.hipThickness),fs+'OuterBackHip',mv.hipActuatorLegDistance,fs+'HipSideSupport',diag(mv.hipSideSupportLength,mv.hipActuatorLegDistance),isClockwise=isClockwise)

	#INPUTES
	# leftOuterBackHip
	# leftOuterFrontHip
	# leftInnerBackHip
	# leftInnerFrontHip
	# leftHipActuator
	# leftLowerHipPost #for 2d reference
	#OUTPUTS
	# leftAnkleOuterFront
	# leftAnkleOuterBack
	# leftAnkleInnerFront
	# leftAnkleInnerBack
	def internal_addThighAndCalf(self,mv,isLeft):
		s = self.struct
		if isLeft:	
			fs = 'left'
			isClockwise = False
		else:
			fs = 'right'
			isClockwise = True
		s.add2DJoint(fs+'ThighActuator',fs+'HipActuator',mv.hipActuatorInit,fs+'OuterBackHip',mv.thighActuatorLegDistance,fs+'LowerHipPost','f',dpA=mv.actuatorDispProp)
		s.add1DJoint(fs+'OuterBackKnee',fs+'OuterBackHip',mv.thighLength,fs+'ThighActuator')
		s.add2DJoint(fs+'OuterFrontKnee',fs+'OuterBackKnee',mv.legBoneXWidth,fs+'OuterFrontHip',mv.thighLength,fs+'OuterBackHip','f')
		s.addJoint(fs+'InnerBackKnee',fs+'InnerBackHip',mv.thighLength,fs+'OuterFrontKnee',diag(mv.legBoneZWidth,mv.legBoneXWidth),fs+'OuterBackKnee',mv.legBoneZWidth,isClockwise=isClockwise)
		s.addJoint(fs+'InnerFrontKnee',fs+'InnerBackKnee',mv.legBoneXWidth,fs+'InnerFrontHip',mv.thighLength,fs+'OuterFrontKnee',mv.legBoneZWidth,isClockwise=isClockwise)
		#Now the knee structure and calf
		s.add1DJoint(fs+'KneeActuator',fs+'OuterBackKnee',mv.kneeActuatorLegDistance,fs+'OuterFrontKnee')
		s.add2DJoint(fs+'CalfActuator',fs+'OuterBackKnee',mv.calfActuatorLegDistance,fs+'KneeActuator',mv.calfActuatorInit,fs+'OuterBackHip','f',dpB=mv.actuatorDispProp)
		s.add1DJoint(fs+'AnkleOuterBack',fs+'OuterBackKnee',mv.calfLength,fs+'CalfActuator')
		s.add2DJoint(fs+'AnkleOuterFront',fs+'AnkleOuterBack',mv.legBoneXWidth,fs+'OuterFrontKnee',mv.calfLength,fs+'OuterBackKnee','f')
		s.addJoint(fs+'AnkleInnerBack',fs+'InnerBackKnee',mv.calfLength,fs+'AnkleOuterFront',diag(mv.legBoneZWidth,mv.legBoneXWidth),fs+'AnkleOuterBack',mv.legBoneZWidth,isClockwise=isClockwise)
		s.addJoint(fs+'AnkleInnerFront',fs+'AnkleInnerBack',mv.legBoneXWidth,fs+'InnerFrontKnee',mv.calfLength,fs+'AnkleOuterFront',mv.legBoneZWidth,isClockwise=isClockwise)
		self.internal_addFoot(mv,isLeft)

	def internal_addFootOnly(self):
		mv = mechVariables()
		self.struct = mfStructure('leftAnkleOuterFront',[0,0,0],'leftAnkleOuterBack',[1,0,0])
		s = self.struct
		s.defaultDisplayProperties = mv.mainSpanDispProp
		s.defaultDensity = mv.mainSpanDensity
		s.collisionMargin = mv.collisionMargin
		s.add1DJoint('leftAnkleInnerFront','leftAnkleOuterFront',0.5,[0,0,-0.5])
		s.add1DJoint('leftAnkleInnerBack','leftAnkleOuterBack',0.5,[1,0,-0.5])
		self.internal_addFoot( mv, 'left') #legBoneXWidth, legBoneZWidth,footLength,footWidth,footHeight,footDispProp,actDispProp,isLeftFoot):
		

	#Requires 4 interaction points:
	# leftAnkleOuterFront
	# leftAnkleOuterBack
	# leftAnkleInnerFront
	# leftAnkleInnerBack
	def internal_addFoot(self,mv,isLeft):
		if isLeft:
			fs = 'left'
			isClockwise = True
		else:
			fs = 'right'
			isClockwise = False
		actJY = 1.0
		actJX = 0.5
		actInit = 1.0
		s = self.struct
		tmpDispProp = s.defaultDisplayProperties
		s.defaultDisplayProperties = mv.mainSpanDispProp
		tmpDensity = s.defaultDensity
		s.defaultDensity = mv.mainSpanDensity
		#The actuator and beginning of the foot
		s.addJoint(fs+'AnkleActuator',fs+'AnkleOuterFront',diag(actJX+mv.legBoneXWidth,actJY,mv.legBoneZWidth/2.0),fs+'AnkleOuterBack',diag(actJX,actJY,mv.legBoneZWidth/2.0),fs+'AnkleInnerBack',diag(actJX,actJY,mv.legBoneZWidth/2.0),isClockwise=isClockwise)#Size oriented??
		s.addJoint(fs+'FootActuator',fs+'AnkleActuator',actInit,fs+'AnkleOuterBack',diag(actJX,mv.legBoneZWidth/2.0),fs+'AnkleInnerBack',diag(actJX,mv.legBoneZWidth/2.0),dpA=mv.actuatorDispProp,isClockwise=isClockwise)#Side oriented??
		s.add2DJoint(fs+'FootOuterBack',fs+'FootActuator',mv.legBoneZWidth/2.0,fs+'AnkleOuterBack',actJX,fs+'AnkleInnerBack','f')
		s.add2DJoint(fs+'FootInnerBack',fs+'FootActuator',mv.legBoneZWidth/2.0,fs+'AnkleInnerBack',actJX,fs+'AnkleOuterBack','f')
		#The front and back toes on ground level
		s.add1DJoint(fs+'FootOuterFrontToe',fs+'FootOuterBack',actJX+mv.footLength/2.0,fs+'AnkleOuterBack')
		s.add1DJoint(fs+'FootInnerFrontToe',fs+'FootInnerBack',actJX+mv.footLength/2.0,fs+'AnkleInnerBack')
		s.add1DJoint(fs+'FootOuterFrontToeSupport',fs+'FootOuterFrontToe',mv.footHeight,fs+'FootOuterBack')
		s.add1DJoint(fs+'FootInnerFrontToeSupport',fs+'FootInnerFrontToe',mv.footHeight,fs+'FootInnerBack')
		s.add1DJoint(fs+'FootOuterBackToe',fs+'AnkleOuterBack',actJX+mv.footLength/2.0,fs+'FootOuterBack')
		s.add1DJoint(fs+'FootInnerBackToe',fs+'AnkleInnerBack',actJX+mv.footLength/2.0,fs+'FootInnerBack')	
		s.add1DJoint(fs+'FootOuterBackToeSupport',fs+'FootOuterBackToe',mv.footHeight,fs+'FootOuterBack')
		s.add1DJoint(fs+'FootInnerBackToeSupport',fs+'FootInnerBackToe',mv.footHeight,fs+'FootInnerBack')
		#The front and back toes on upper level
		fs = fs+'Foot'
		s.addJoint(fs+'OuterBottomFrontToe',fs+'OuterFrontToeSupport',diag(mv.footHeight,mv.footHeight),fs+'OuterFrontToe',mv.footHeight,fs+'InnerFrontToe',diag(mv.footHeight,mv.legBoneZWidth),isClockwise=isClockwise)
		s.addJoint(fs+'InnerBottomFrontToe',fs+'InnerFrontToe',mv.footHeight,fs+'InnerFrontToeSupport',diag(mv.footHeight,mv.footHeight),fs+'OuterFrontToe',diag(mv.footHeight,mv.legBoneZWidth),isClockwise=isClockwise)
		s.addJoint(fs+'OuterBottomBackToe',fs+'OuterBackToe',mv.footHeight,fs+'OuterBackToeSupport',diag(mv.footHeight,mv.footHeight),fs+'InnerBackToe',diag(mv.footHeight,mv.legBoneZWidth),isClockwise=isClockwise)
		s.addJoint(fs+'InnerBottomBackToe',fs+'InnerBackToeSupport',diag(mv.footHeight,mv.footHeight),fs+'InnerBackToe',mv.footHeight,fs+'OuterBackToe',diag(mv.footHeight,mv.legBoneZWidth),isClockwise=isClockwise)
		#The top of the foot
		s.add1DJoint(fs+'OuterFrontBottomToeSupport',fs+'OuterBottomFrontToe',mv.footHeight,fs+'OuterBottomBackToe')
		s.add1DJoint(fs+'OuterBackBottomToeSupport',fs+'OuterBottomBackToe',mv.footHeight,fs+'OuterBottomFrontToe')
		s.add1DJoint(fs+'InnerFrontBottomToeSupport',fs+'InnerBottomFrontToe',mv.footHeight,fs+'InnerBottomBackToe')
		s.add1DJoint(fs+'InnerBackBottomToeSupport',fs+'InnerBottomBackToe',mv.footHeight,fs+'InnerBottomFrontToe')
		s.add1DJoint(fs+'Unused1',fs+'OuterBottomFrontToe',mv.footLength,fs+'OuterBottomBackToe')
		s.add1DJoint(fs+'Unused2',fs+'InnerBottomFrontToe',mv.footLength,fs+'InnerBottomBackToe')
		#The side supports on the foot
		self.internal_addFootSupport(mv.legBoneZWidth,mv.footWidth,mv.footHeight,fs,'Front','OuterFrontToe','InnerFrontToe','OuterFrontToeSupport','InnerFrontToeSupport','OuterBottomFrontToe','InnerBottomFrontToe','OuterFrontBottomToeSupport','InnerFrontBottomToeSupport',mv,isClockwise)
		self.internal_addFootSupport(mv.legBoneZWidth,mv.footWidth,mv.footHeight,fs,'Back','OuterBackToe','InnerBackToe','OuterBackToeSupport','InnerBackToeSupport','OuterBottomBackToe','InnerBottomBackToe','OuterBackBottomToeSupport','InnerBackBottomToeSupport',mv,isClockwise)
		#The supports on the feet
		self.internal_addCrossBracing(fs+'F',fs+'OuterFrontToe',fs+'InnerFrontToe',fs+'OuterBottomFrontToe',fs+'InnerBottomFrontToe',fs+'OuterBackToe',fs+'InnerBackToe',fs+'OuterBottomBackToe',fs+'InnerBottomBackToe',mv.legBoneZWidth,mv.footHeight,mv)
		self.internal_addCrossBracing(fs+'B',fs+'OuterBackToe',fs+'InnerBackToe',fs+'OuterBottomBackToe',fs+'InnerBottomBackToe',fs+'OuterFrontToe',fs+'InnerFrontToe',fs+'OuterBottomFrontToe',fs+'InnerBottomFrontToe',mv.legBoneZWidth,mv.footHeight,mv)
		s.defaultDisplayProperties = tmpDispProp
		s.defaultDensity = tmpDensity
	
	def internal_addCrossBracing(self,prefix,oft,ift,ofbt,ifbt,obt,ibt,obbt,ibbt,width,height,mv):
		s = self.struct	
		tmpDispProp = s.defaultDisplayProperties
		s.defaultDisplayProperties = mv.lightSupportSpanDispProp
		tmpDensity = s.defaultDensity
		s.defaultDensity = mv.lightSupportSpanDensity
		self.internal_addCrossBrace(prefix+'b1',ift,ibt,oft,obt,0.0*width,1.0*width,diag(width,width))#1
		self.internal_addCrossBrace(prefix+'b2',ift,ibt,oft,obt,2.0*width,1.0*width,diag(width,width))#2
		self.internal_addCrossBrace(prefix+'b3',ift,ibt,oft,obt,2.0*width,3.0*width,diag(width,width))#3
		self.internal_addCrossBrace(prefix+'b4',ift,ibt,oft,obt,4.0*width,3.0*width,diag(width,width))#4
		self.internal_addCrossBrace(prefix+'b5',ift,ibt,oft,obt,4.0*width,5.0*width,diag(width,width))#5
		self.internal_addCrossBrace(prefix+'b6',ift,ibt,oft,obt,6.0*width,5.0*width,diag(width,width))#6
		self.internal_addCrossBrace(prefix+'b7',ift,ibt,oft,obt,6.0*width,7.0*width,diag(width,width))#7
		self.internal_addCrossBrace(prefix+'b8',ift,ibt,oft,obt,8.0*width,7.0*width,diag(width,width))#8

		s.defaultDisplayProperties = mv.heavySupportSpanDispProp
		s.defaultDensity = mv.heavySupportSpanDensity
		self.internal_addCrossBrace(prefix+'b9' ,oft,obt,ofbt,obbt,width,width+height,diag(height,height))#1
		self.internal_addCrossBrace(prefix+'b10',oft,obt,ofbt,obbt,width*2.0,width*2+height,diag(height,height))#2

		s.defaultDisplayProperties = mv.lightSupportSpanDispProp
		s.defaultDensity = mv.lightSupportSpanDensity
		self.internal_addCrossBrace(prefix+'b11',ofbt,obbt,ifbt,ibbt,1.0*width,0.0*width,diag(width,width))#1
		self.internal_addCrossBrace(prefix+'b12',ofbt,obbt,ifbt,ibbt,1.0*width,2.0*width,diag(width,width))#2
		self.internal_addCrossBrace(prefix+'b13',ofbt,obbt,ifbt,ibbt,3.0*width,2.0*width,diag(width,width))#3
		self.internal_addCrossBrace(prefix+'b14',ofbt,obbt,ifbt,ibbt,3.0*width,4.0*width,diag(width,width))#4
		self.internal_addCrossBrace(prefix+'b15',ofbt,obbt,ifbt,ibbt,5.0*width,4.0*width,diag(width,width))#5
		self.internal_addCrossBrace(prefix+'b16',ofbt,obbt,ifbt,ibbt,5.0*width,6.0*width,diag(width,width))#6
		self.internal_addCrossBrace(prefix+'b17',ofbt,obbt,ifbt,ibbt,7.0*width,6.0*width,diag(width,width))#7
		self.internal_addCrossBrace(prefix+'b18',ofbt,obbt,ifbt,ibbt,7.0*width,8.0*width,diag(width,width))#8
	
		s.defaultDisplayProperties = mv.heavySupportSpanDispProp
		s.defaultDensity = mv.heavySupportSpanDensity
		self.internal_addCrossBrace(prefix+'b19',ifbt,ibbt,ift,ibt,width*4.0,width*4.0+height,diag(height,height))#1
		self.internal_addCrossBrace(prefix+'b20',ifbt,ibbt,ift,ibt,width*4.0+height,width*4.0+height*2.0,diag(height,height))#2
		s.defaultDisplayProperties = tmpDispProp
		s.defaultDensity = tmpDensity
	
	def internal_addCrossBrace(self,prefix,beginOne,endOne,beginTwo,endTwo,lengthOne,lengthTwo,distance):
		s = self.struct
		tmp = s.defaultDensity
		s.defaultDensity = 0.0
		s.add1DJoint(prefix+'Unused1',beginOne,lengthOne,endOne)
		s.add1DJoint(prefix+'Unused2',beginTwo,lengthTwo,endTwo)
		s.defaultDensity = tmp
		s.add1DJoint(prefix+'Unused3',prefix+'Unused1',distance,prefix+'Unused2')

	def internal_addFootSupport(self,legBoneZWidth,footWidth,footHeight,fs,fe,a,b,c,d,e,f,g,h,mv,isClockwise):
		s = self.struct
		tmpDispProp = s.defaultDisplayProperties
		s.defaultDisplayProperties = mv.mainSpanDispProp
		tmpDensity = s.defaultDensity
		s.defaultDensity = mv.mainSpanDensity
		
		#The side support main spans
		s.add1DJoint(fs+fe+'OuterSide',fs+a,footWidth,fs+b,cd=True)
		s.add1DJoint(fs+fe+'InnerSide',fs+c,footWidth,fs+d,cd=True)
		s.add1DJoint(fs+fe+'OuterBottomSide',fs+e,footWidth,fs+f,cd=True)
		s.add1DJoint(fs+fe+'InnerBottomSide',fs+g,footWidth,fs+h,cd=True)
		s.add1DJoint(fs+fe+'OuterSideSupport',fs+fe+'OuterSide',footHeight,fs+a)
		s.add1DJoint(fs+fe+'InnerSideSupport',fs+fe+'InnerSide',footHeight,fs+c)
		
		#Internal structure	
		s.add1DJoint(fs+fe+'Unused3',fs+fe+'OuterSide',footHeight,fs+fe+'InnerSide')
		s.add1DJoint(fs+fe+'Unused4',fs+fe+'OuterBottomSide',footHeight,fs+fe+'InnerBottomSide')
		if(fe == 'Front'):
		#	End bracing
			s.addJoint(fs+fe+'Unused5',fs+fe+'OuterSide',footHeight,fs+fe+'InnerSideSupport',diag(footHeight,footHeight,footHeight),fs+fe+'OuterSideSupport',diag(footHeight,footHeight),isClockwise=isClockwise)
			s.addJoint(fs+fe+'Unused6',fs+fe+'InnerSide',footHeight,fs+fe+'InnerSideSupport',diag(footHeight,footHeight),fs+fe+'OuterSideSupport',diag(footHeight,footHeight,footHeight),isClockwise=isClockwise)
		elif(fe == 'Back'):
		#	End bracing
			s.addJoint(fs+fe+'Unused5',fs+fe+'InnerSideSupport',diag(footHeight,footHeight,footHeight),fs+fe+'OuterSide',footHeight,fs+fe+'OuterSideSupport',diag(footHeight,footHeight),isClockwise=isClockwise)
			s.addJoint(fs+fe+'Unused6',fs+fe+'InnerSideSupport',diag(footHeight,footHeight),fs+fe+'InnerSide',footHeight,fs+fe+'OuterSideSupport',diag(footHeight,footHeight,footHeight),isClockwise=isClockwise)
		#		Long bracing	
		s.add1DJoint(fs+fe+'Unused7',fs+b,diag(footHeight,footWidth-legBoneZWidth),fs+fe+'OuterBottomSide')
		s.add1DJoint(fs+fe+'Unused8',fs+d,diag(footHeight,footWidth-legBoneZWidth),fs+fe+'InnerBottomSide')
		s.defaultDisplayProperties = tmpDispProp
		s.defaultDensity = tmpDensity

def diag(*args):
	t = 0.0
	for arg in args:
		t += sq(arg)
	return sqrt(t)		
def sqrt(x):
	return math.sqrt(x)

def sq(x):
	return math.pow(x,2.0) 
