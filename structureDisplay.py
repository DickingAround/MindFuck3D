import pygame
import os
import sys
from displayView import *
from displayProperties import *
from joint_generalHelperFunctions import *
import time
class structureDisplay():
	displayX = 640
	displayY = 480
	window = pygame.display.set_mode((displayX,displayY))
	imageResize = sys.float_info.min
	displayViewUL = 'NULL'
	displayViewUR = 'NULL'
	displayViewLL = 'NULL'
	displayViewLR = 'NULL'
	def __init__(self):
		window = pygame.display.set_mode((self.displayX,self.displayY))
		displayX = self.displayX
		displayY = self.displayY
		#X
		self.displayViewUL = displayView(0           ,0           ,displayX/2.0,displayY/2.0,[0,0.25,0])
		#Y	
		self.displayViewUR = displayView(displayX/2.0,0           ,displayX/2.0,displayY/2.0,[0.25,0,0])
		#Z	
		self.displayViewLL = displayView(0           ,displayY/2.0,displayX/2.0,displayY/2.0,[0,0,0])
		#Angle	
		self.displayViewLR = displayView(displayX/2.0,displayY/2.0,displayX/2.0,displayY/2.0,[0.2*0.25,0.2*.25,0])
		pygame.draw.line(self.window,(100,100,100),(displayX/2.0,-0),(displayX/2.0,displayY),1)
		pygame.draw.line(self.window,(100,100,100),(-0,displayY/2.0),(displayX,displayY/2.0),1)

	def saveScreen(self,name):
		pygame.image.save(self.window,"./images/%s.png"%name)
	def clearDisplay(self):
		self.window.fill((0,0,0))
		pygame.draw.line(self.window,(100,100,100),(self.displayX/2.0,-0),(self.displayX/2.0,self.displayY),1)
                pygame.draw.line(self.window,(100,100,100),(-0,self.displayY/2.0),(self.displayX,self.displayY/2.0),1)
		pygame.display.flip()
	#Duration is the number of seconds the sequence takes. Speeds for commands are specified and are relative.
	#Command: span,length,steps
	def displayLines_sequence(self,struct,commands,save=False,debugPrint=False):
		cont = True	
		saving = 0
		imgNumb = 0.0
		numbImgs = 0.0
		while cont:
			for command in commands:
				span = command[0]
				newLen = command[1]
				steps = command[2]
				if steps == 0:
					span.l = newLen #Don't do any saving, done do any waiting
				for incLen in frange(span.l,newLen,steps):
					span.l = incLen
					struct.computeLocations()
					lines = struct.getLinesList()
					if save and saving == 0:
						numbImgs += 1
					#self.displayViewLR.yRotate = (self.displayViewLR.yRotate+.001)%1.0
					self.displayLines(lines)	
					self.internal_drawCenterOfMass(struct)	
					if saving == 1:
						self.saveScreen("img_%f"%(imgNumb/numbImgs))
						imgNumb += 1
					else:
						time.sleep(0.050)
				if debugPrint:
					print "Just ran command: %s"%command
					#foo = raw_input("Press any yet to continue with next command")
			if saving == 0 and save:
				print "Begin saving..."
				os.system('bash clearImages')
				saving = 1
			elif saving == 1:
				saving = 2
				print "Compiling gif..."
				os.system('bash buildImages')
				print "Done saving."
	def displayLines_animate(self,struct,save=False,debugPrint=False):
		if debugPrint:
			print "beginning display"
		cont = True
		lines = struct.getLinesList()	
		if debugPrint:
			print "Lines list is %f lines"%len(lines)
		saving = 0
		self.displayViewLR.yRotate = 0.0
		while cont:
			self.displayViewLR.yRotate = (self.displayViewLR.yRotate+.01)%1.0
			self.displayLines(lines)
			self.internal_drawCenterOfMass(struct)	
			if save and self.displayViewLR.yRotate < 0.001:
				if saving == 0:
					print "Begin saving..."
					os.system('bash clearImages')
					saving = 1
				elif saving == 1:
					saving = 2
					print "Compiling gif..."	
					os.system('bash buildImages')
					print "Done saving."
			if saving == 1:
				self.saveScreen("img_%f"%self.displayViewLR.yRotate)
			if debugPrint:
				print "Ran a shot"
                        #for event in pygame.event.get():
                        #        if event.type == pygame.KEYDOWN:
                        #                cont = False	
			time.sleep(0.050)
	#Line = [pointA, pointB, span] NOTE: The span is only used for the display properties, we already know the length	
	def displayLines(self,lines,clearDisp=True):
		#Check min/max/sizes
		if clearDisp:
			self.internal_resetCenters()#Does not ever reset sizes
			for line in lines:
				self.internal_checkSizeAndCenter(line[0])
				self.internal_checkSizeAndCenter(line[1])
			self.internal_computeSizeAndCenters()
		#Display
		#if clearDisp:
			self.clearDisplay()
		for line in lines:
			self.displayLine(self.displayViewUL,line)
			self.displayLine(self.displayViewUR,line)
			self.displayLine(self.displayViewLL,line)
			self.displayLine(self.displayViewLR,line)
		pygame.display.flip()

	def displayLine(self,displayView,line):
		#print "Preparing line: %s -- %s"%(line[0].toString(),line[1].toString())
		locA = displayView.getDisplayCoordinates(self,line[0])
		locB = displayView.getDisplayCoordinates(self,line[1])
		#print "Drawing line: %s -- %s"%(locA.toString(), locB.toString())
		sp = line[2]	
		if(sp == 'NULL' or sp.displayProps == 'NULL'):
			pygame.draw.line(self.window,(255,255,255),(locA.x,locA.y),(locB.x,locB.y))
		else:
			t = sp.displayProps
			pygame.draw.line(self.window,(t.color[0],t.color[1],t.color[2]),(locA.x,locA.y),(locB.x,locB.y),t.thickness)
	def internal_drawCenterOfMass(self,struct,crossSize=1.0,displayProps=displayProperties([255,255,255],5),debugPrint=False):#TODO:Make cross size intelligent
		#We assume the structure's compute locations are up to date
		m = struct.getCenterOfMass()
		if debugPrint:
			print "x:%f,y:%f,z:%f,m:%f"%(m.x,m.y,m.z,m.m)
		lineXN = m.copy()
		lineXN.add(location(-crossSize,0,0))
		lineXP = m.copy()
		lineXP.add(location(crossSize,0,0))
		lineYN = m.copy()
		lineYN.add(location(0,-crossSize,0))
		lineYP = m.copy()
		lineYP.add(location(0,crossSize,0))
		lineZN = m.copy()
		lineZN.add(location(0,0,-crossSize))
		lineZP = m.copy()
		lineZP.add(location(0,0,crossSize))
		if debugPrint:
			print "lineXN: %s"%lineXN.toString()
			print "lineXP: %s"%lineXP.toString()
		self.displayLines([[lineXN,lineXP,span(crossSize,displayProps=displayProps)],[lineYN,lineYP,span(crossSize,displayProps=displayProps)],[lineZN,lineZP,span(crossSize,displayProps=displayProps)]],clearDisp=False)
	def internal_resetCenters(self):
		self.displayViewUL.resetCenters()
		self.displayViewUR.resetCenters()	
		self.displayViewLL.resetCenters()	
		self.displayViewLR.resetCenters()	
	def internal_checkSizeAndCenter(self,loc):
		s = self.displayViewUL.checkSizeAndCenter(loc)
		if(s > self.imageResize):
			self.imageResize = s 
		s = self.displayViewUR.checkSizeAndCenter(loc)
		if(s > self.imageResize):
			self.imageResize = s
		s = self.displayViewLL.checkSizeAndCenter(loc)
		if(s > self.imageResize):
			self.imageResize = s
		s = self.displayViewLR.checkSizeAndCenter(loc)
		if(s > self.imageResize):
			self.imageResize = s
	def internal_computeSizeAndCenters(self):
		self.displayViewUL.computeCenter()
		self.displayViewUR.computeCenter()
		self.displayViewLL.computeCenter()
		self.displayViewLR.computeCenter()
	 
