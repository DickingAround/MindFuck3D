from mfStructure import *
import sys
class mech_usedForTesting():
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
		return self.struct.getJoint('leftHipActuator')	
	def getFootReferencePoint(self,lOrR):
		if lOrR == 'l':
			return self.struct.getJoint('leftAnkleFront')
		if lOrR == 'r':
			return self.struct.getJoint('rightAnkleFront')
		else:
			return 'NULL'	
	def computeLocations(self):
		self.struct.computeLocations()
	def checkForCollisions(self):
		self.struct.checkForCollisions()
	
	def __init__(self):
		#Leg attributes	
		actThighInit = 0.5
		actCalfInit = 0.5
		actRightThighInit = 0.5
		actRightCalfInit = 0.5
		actHipDis = 1.0
		actThighDis = 1.0
		actKneeDis = 1.0
		actCalfDis = 1.0
		thighLen = 5.0
		calfLen = 5.0
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
		#LEFT LEG
		s.add2DJoint('leftThighActuator','leftHipBack',actThighDis,'leftHipActuator',actThighInit,[0,1,0],'f',dpA=leftLegDispProp,dpB=actDispProp)
		self.leftThighActuator = s.getSpan('leftThighActuator','leftHipActuator')
		s.add1DJoint('leftKneeBack','leftHipBack',thighLen,'leftThighActuator',dpA=leftLegDispProp)
		s.add1DJoint('leftHipFront','leftHipActuator',legBoneDis+actHipDis,'leftHipBack',dpA=leftLegDispProp)
		s.add2DJoint('leftKneeFront','leftHipFront',thighLen,'leftKneeBack',legBoneDis,'leftHipBack','f',dp=leftLegDispProp)
		s.add2DJoint('leftKneeBrace','leftKneeBack',math.sqrt(1.0+legBoneDis*legBoneDis),'leftKneeFront',1.0,'leftHipBack','n',dp=leftLegDispProp)
		s.add2DJoint('leftKneeActuator','leftKneeBrace',math.sqrt(1.0+actKneeDis*actKneeDis),'leftKneeFront',actKneeDis,'leftKneeBack','f',dp=leftLegDispProp)
		s.add2DJoint('leftCalfActuator','leftKneeActuator',actCalfInit,'leftKneeFront',actCalfDis,'leftKneeBrace','f',dpA=actDispProp,dpB=leftLegDispProp)
		self.leftCalfActuator = s.getSpan('leftCalfActuator','leftKneeActuator') 
		s.add1DJoint('leftAnkleFront','leftKneeFront',calfLen,'leftCalfActuator',dp=leftLegDispProp)
		s.add2DJoint('leftAnkleBack','leftAnkleFront',legBoneDis,'leftKneeBack',calfLen,'leftKneeActuator','f',dp=leftLegDispProp)	
		#LEFT FOOT
		footHeight = 1.0
		footThickness = 0.6	
		footPadWidth = 1.0
		footWidth = 6.0
		footLength = 8.0
		s.add2DJoint('leftFootPivotBackTop','leftAnkleFront',sqrt(sq(legBoneDis)+sq(footHeight)),'leftAnkleBack',footHeight,'leftKneeFront','f',dpA=leftFootDispProp,dpB=actDispProp)
		self.leftAnkleActuator = s.getSpan('leftAnkleBack','leftKneeFront')
		s.add2DJoint('leftFootPivotFrontTop','leftAnkleFront',sqrt(sq(legBoneDis)+sq(footHeight)),'leftFootPivotBackTop',legBoneDis*2,'leftAnkleBack','f',dp=leftFootDispProp)
		s.add2DJoint('leftFootPivotFrontBottom','leftFootPivotFrontTop',footThickness,'leftFootPivotBackTop',sqrt(sq(footThickness)+sq(legBoneDis*2)),'leftAnkleFront','f',dp=leftFootDispProp)
		s.add2DJoint('leftFootPivotBackBottom','leftFootPivotBackTop',footThickness,'leftFootPivotFrontTop',sqrt(sq(footThickness)+sq(legBoneDis*2)),'leftAnkleBack','f',dp=leftFootDispProp)
		s.add1DJoint('leftFootToeFrontTop','leftFootPivotBackTop',footLength/2.0+legBoneDis,'leftFootPivotFrontTop',dp=leftFootDispProp)
		s.add1DJoint('leftFootToeFrontBottom','leftFootPivotBackBottom',footLength/2.0+legBoneDis,'leftFootPivotFrontBottom',dp=leftFootDispProp)
		s.add1DJoint('leftFootToeFrontBottomNear','leftFootPivotBackBottom',footLength/2.0-footPadWidth+legBoneDis,'leftFootPivotFrontBottom',dp=leftFootDispProp)
		s.addJoint('leftFootPointyToeFront','leftFootToeFrontBottomNear',sqrt(sq(footPadWidth)+sq(footWidth)),'leftFootToeFrontBottom',footWidth,'leftFootToeFrontTop',sqrt(sq(footWidth)+sq(footThickness)),dp=leftFootDispProp)
		s.add1DJoint('leftFootToeBackTop','leftFootPivotFrontTop',footLength/2.0+legBoneDis,'leftFootPivotBackTop',dp=leftFootDispProp)
		s.add1DJoint('leftFootToeBackBottom','leftFootPivotFrontBottom',footLength/2.0+legBoneDis,'leftFootPivotBackBottom',dp=leftFootDispProp)
		s.add1DJoint('leftFootToeBackBottomNear','leftFootPivotFrontBottom',footLength/2.0-footPadWidth+legBoneDis,'leftFootPivotBackBottom',dp=leftFootDispProp)
		s.addJoint('leftFootPointyToeBack','leftFootToeBackBottom',footWidth,'leftFootToeBackBottomNear',sqrt(sq(footPadWidth)+sq(footWidth)),'leftFootToeBackTop',sqrt(sq(footWidth)+sq(footThickness)),dp=leftFootDispProp)	

		#HIP
		legHipSupportLen = 1.0
		legHipWingLen = 0.5
		hipPostLowerPoint = 0.1
		hipPostUpperPoint = 1.0
		hipCockpitDis = 1.0
		cockpitWidth = 6.0
		actHipInit = sqrt(sq(hipCockpitDis)+sq(actHipDis))
		# Main leg supports
		s.computeLocations()
		s.addJoint('leftHipSupportBack','leftHipBack',legHipSupportLen,'leftHipActuator', sqrt( sq(legHipSupportLen) + sq(actHipDis)),'leftThighActuator', sqrt(sq(actThighDis)+sq(legHipSupportLen)),dp=leftLegDispProp)
		s.add1DJoint('leftSupportAttachFront','leftHipFront',actThighDis,'leftKneeFront',dp=leftLegDispProp)	
		s.addJoint('leftHipSupportFront','leftHipFront',legHipSupportLen,'leftHipBack', sqrt(sq(legBoneDis)+sq(legHipSupportLen)),'leftSupportAttachFront', sqrt(sq(actThighDis)+sq(legHipSupportLen)),dp=leftLegDispProp)
		# Hip post 
		s.addJoint('leftHipWingBack','leftThighActuator',sqrt(sq(actThighDis)+sq(legHipWingLen)),'leftHipBack',legHipWingLen,'leftHipFront',sqrt(sq(legBoneDis)+sq(legHipWingLen)),dp=leftLegDispProp)
		s.addJoint('leftHipPostUpper','leftHipBack',hipPostUpperPoint,'leftHipFront',sqrt(sq(legBoneDis)+sq(hipPostUpperPoint)),'leftHipWingBack',sqrt(sq(legHipWingLen)+sq(hipPostUpperPoint)),dp=leftLegDispProp)
		s.addJoint('leftHipActuatorPost','leftHipBack',sqrt(sq(hipPostUpperPoint)+sq(actHipDis)),'leftHipActuator',hipPostUpperPoint,'leftHipPostUpper',actHipDis,dp=leftLegDispProp)
		# Hip center		
		s.addJoint('leftHipCockpitUpper','leftHipPostUpper',hipCockpitDis,'leftHipActuatorPost',actHipInit,'leftHipBack',sqrt(sq(hipCockpitDis)+sq(hipPostUpperPoint)),dpA=actDispProp,dpB=hipDispProp,dpC=hipDispProp)
		self.leftHipActuator = s.getSpan('leftHipCockpitUpper','leftHipPostUpper')	
		s.addJoint('leftHipCockpitLower','leftHipCockpitUpper',hipPostUpperPoint,'leftHipBack',hipCockpitDis,'leftHipPostUpper',sqrt(sq(hipCockpitDis)+sq(hipPostUpperPoint)),dp=hipDispProp)
		s.add1DJoint('rightHipCockpitUpper','leftHipPostUpper',cockpitWidth+hipCockpitDis,'leftHipCockpitUpper',dp=hipDispProp)
		s.add1DJoint('rightHipCockpitLower','leftHipBack',cockpitWidth+hipCockpitDis,'leftHipCockpitLower',dp=hipDispProp)
		s.add2DJoint('rightHipPostUpper','rightHipCockpitUpper',hipCockpitDis,'rightHipCockpitLower',sqrt(sq(hipCockpitDis)+sq(hipPostUpperPoint)),'leftHipCockpitLower','f',dp=hipDispProp)
		s.add2DJoint('rightHipBack','rightHipCockpitLower',hipCockpitDis,'rightHipCockpitUpper',sqrt(sq(hipCockpitDis)+sq(hipPostUpperPoint)),'leftHipCockpitUpper','f',dp=hipDispProp)
		# Hip post
		s.addJoint('rightHipActuatorPost','rightHipBack',sqrt(sq(actHipDis)+sq(hipPostUpperPoint)),'rightHipPostUpper',actHipDis,'rightHipCockpitUpper',actHipInit,dpA=rightLegDispProp,dpB=rightLegDispProp,dpC=actDispProp)	
		self.rightHipActuator = s.getSpan('rightHipCockpitUpper','leftHipPostUpper')	
		s.addJoint('rightHipActuator','rightHipActuatorPost',hipPostUpperPoint,'rightHipBack',actHipDis,'rightHipPostUpper',sqrt(sq(hipPostUpperPoint)+sq(actHipDis)),dp=rightLegDispProp)
		#RIGHT LEG
		s.addJoint('rightHipWingBack','rightHipPostUpper',sqrt(sq(hipPostUpperPoint)+sq(legHipWingLen)),'rightHipActuator',sqrt(sq(legHipWingLen)+sq(actHipDis)),'rightHipBack',legHipWingLen,dp=rightLegDispProp)
		s.addJoint('rightThighActuator','rightHipActuator',actRightThighInit,'rightHipBack',actThighDis,'rightHipWingBack',sqrt(sq(legHipWingLen)+sq(actThighDis)),dpB=rightLegDispProp,dpA=actDispProp,dpC=rightLegDispProp)
		self.rightThighActuator = s.getSpan('rightThighActuator','rightHipActuator')
                s.add1DJoint('rightKneeBack','rightHipBack',thighLen,'rightThighActuator',dpA=rightLegDispProp)
		s.add1DJoint('rightHipFront','rightHipActuator',legBoneDis+actHipDis,'rightHipBack',dpA=rightLegDispProp)
                s.add2DJoint('rightKneeFront','rightHipFront',thighLen,'rightKneeBack',legBoneDis,'rightHipBack','f',dp=rightLegDispProp)
                s.add2DJoint('rightKneeBrace','rightKneeBack',math.sqrt(1.0+legBoneDis*legBoneDis),'rightKneeFront',1.0,'rightHipBack','n',dp=rightLegDispProp)
                s.add2DJoint('rightKneeActuator','rightKneeBrace',math.sqrt(1.0+actKneeDis*actKneeDis),'rightKneeFront',actKneeDis,'rightKneeBack','f',dp=rightLegDispProp)
                s.add2DJoint('rightCalfActuator','rightKneeActuator',actRightCalfInit,'rightKneeFront',actCalfDis,'rightKneeBrace','f',dpA=actDispProp,dpB=rightLegDispProp)
		self.rightCalfActuator = s.getSpan('rightCalfActuator','rightKneeActuator')
                s.add1DJoint('rightAnkleFront','rightKneeFront',calfLen,'rightCalfActuator',dp=rightLegDispProp)
                s.add2DJoint('rightAnkleBack','rightAnkleFront',legBoneDis,'rightKneeBack',calfLen,'rightKneeActuator','f',dp=rightLegDispProp)	
		s.add1DJoint('rightSupportAttachFront','rightHipFront',actThighDis,'rightKneeFront',dp=rightLegDispProp)	
		s.addJoint('rightHipSupportFront','rightHipBack',sqrt(sq(legBoneDis)+sq(legHipSupportLen)),'rightHipFront',legHipSupportLen,'rightSupportAttachFront',sqrt(sq(actThighDis)+sq(legHipSupportLen)),dp=rightLegDispProp)
		s.addJoint('rightHipSupportBack','rightHipActuator',sqrt(sq(actHipDis)+sq(legHipSupportLen)),'rightHipBack',legHipSupportLen,'rightThighActuator',sqrt(sq(actThighDis)+sq(legHipSupportLen)),dp=rightLegDispProp)
		#RIGHT FOOT
		s.add2DJoint('rightFootPivotBackTop','rightAnkleFront',sqrt(sq(legBoneDis)+sq(footHeight)),'rightAnkleBack',footHeight,'rightKneeFront','f',dpA=rightFootDispProp,dpB=actDispProp)
		self.rightAnkleActuator = s.getSpan('rightFootPivotBackTop','rightAnkleBack')
		s.add2DJoint('rightFootPivotFrontTop','rightAnkleFront',sqrt(sq(legBoneDis)+sq(footHeight)),'rightFootPivotBackTop',legBoneDis*2,'rightAnkleBack','f',dp=rightFootDispProp)
		s.add2DJoint('rightFootPivotFrontBottom','rightFootPivotFrontTop',footThickness,'rightFootPivotBackTop',sqrt(sq(footThickness)+sq(legBoneDis*2)),'rightAnkleFront','f',dp=rightFootDispProp)
		s.add2DJoint('rightFootPivotBackBottom','rightFootPivotBackTop',footThickness,'rightFootPivotFrontTop',sqrt(sq(footThickness)+sq(legBoneDis*2)),'rightAnkleBack','f',dp=rightFootDispProp)
		s.add1DJoint('rightFootToeFrontTop','rightFootPivotBackTop',footLength/2.0+legBoneDis,'rightFootPivotFrontTop',dp=rightFootDispProp)
		s.add1DJoint('rightFootToeFrontBottom','rightFootPivotBackBottom',footLength/2.0+legBoneDis,'rightFootPivotFrontBottom',dp=rightFootDispProp)
		s.add1DJoint('rightFootToeFrontBottomNear','rightFootPivotBackBottom',footLength/2.0-footPadWidth+legBoneDis,'rightFootPivotFrontBottom',dp=rightFootDispProp)
		s.addJoint('rightFootPointyToeFront','rightFootToeFrontBottom',footWidth,'rightFootToeFrontBottomNear',sqrt(sq(footPadWidth)+sq(footWidth)),'rightFootToeFrontTop',sqrt(sq(footWidth)+sq(footThickness)),dp=rightFootDispProp)
		s.add1DJoint('rightFootToeBackTop','rightFootPivotFrontTop',footLength/2.0+legBoneDis,'rightFootPivotBackTop',dp=rightFootDispProp)
		s.add1DJoint('rightFootToeBackBottom','rightFootPivotFrontBottom',footLength/2.0+legBoneDis,'rightFootPivotBackBottom',dp=rightFootDispProp)
		s.add1DJoint('rightFootToeBackBottomNear','rightFootPivotFrontBottom',footLength/2.0-footPadWidth+legBoneDis,'rightFootPivotBackBottom',dp=rightFootDispProp)
		s.addJoint('rightFootPointyToeBack','rightFootToeBackBottomNear',sqrt(sq(footPadWidth)+sq(footWidth)),'rightFootToeBackBottom',footWidth,'rightFootToeBackTop',sqrt(sq(footWidth)+sq(footThickness)),dp=rightFootDispProp)			

def sqrt(x):
	return math.sqrt(x)

def sq(x):
	return math.pow(x,2.0) 
