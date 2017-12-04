from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from sphero_sprk import Sphero 
import time
import _thread
import pickle
import matplotlib.pyplot as plt

robots = []
blobs = []
goals= [[20,80],[50,60],[80,80]]
counter = 0
costMatrix = np.empty([len(goals),len(robots)])

motionEnabled = True
speed_min = 20
speed_max = 35
angle_step_max = 18

s1 = Sphero("C9:93:8F:F1:91:E2")
s2 = Sphero("DA:06:00:55:3A:8D")
s3 = Sphero("DC:F3:09:7B:4D:BB")
#s4 = Sphero("F5:8F:A1:93:56:40")

class balls:
	
	def __init__(self,identifier,xy=[0,0],available = False, isMoving = False, currentGoal = [0,0], old_xy = [0,0], speed = 0, heading = 0):
		self.identifier = identifier
		self.xy = xy
		self.available = available
		self.isMoving = isMoving
		self.currentGoal = currentGoal
		self.old_xy = old_xy
		self.speed = speed
		self.heading = heading

		# We need the next line to iterate through all the class objects
		robots.append(self)

	def connect(self):
		self.identifier.connect()

	# Not Required	
	def location(self):
		print (self.xy)

	def keepIdle(self):
		self.identifier.roll(int(0),int(0))

	def roll(self,speed,orientation):
		self.identifier.roll(speed,orientation)

v1 = balls(s1)
v2 = balls(s2)
v3 = balls(s3)
#v4 = balls(s4)

# Variables and Robots are same
variables = [v1,v2,v3]
initialized = False


def updateBlob():
	fetch = None
	global blobs
	while fetch is None:
		try:
			with open("blobLocations", 'rb') as f:
				blobs = pickle.load(f)
				fetch = True
		except:
			pass

#print(type(s1))
#print(type(v1))
#print(type(robots[0]))

def initialize():
	global blobs, robots, initialized
	print("Initialisation Sequence Initiated..")
	assigned = []
	for variable in variables:
		updateBlob()
		oldBlobs = blobs
		# Sometime connection fails, we reattemp connections in these cases
		connected = False
		while not connected:
			try:
				variable.connect()
				connected = True
			except:
				time.sleep(1)
		variable.available = True
		time.sleep(2)
		updateBlob()

		if len(oldBlobs):
			for blob in blobs:
				NewBlob = True
				for oldBlob in oldBlobs:
					if (np.linalg.norm(np.array(blob)-np.array(oldBlob))<5):
						NewBlob = False
				if NewBlob:
					variable.xy = blob

		else:
			variable.xy = list(x for x in blobs if x not in oldBlobs)[0]
		
		print(variable," is at ",variable.xy)
		for robot in robots:
			if (robot.available):
				robot.keepIdle()
	initialized = True


def updatePosition(blob):
	global robots
	rob      = []
	distance = []
	for robot in robots:
		if (robot.available):
			dist = np.linalg.norm(np.array(robot.xy)-np.array(blob))
			rob.append(robot)
			distance.append(dist)

	bot = rob[distance.index(min(distance))]
	if (bot.xy == blob):
		bot.isMoving = False
		bot.keepIdle()
		#print("Idle")
	else:
		bot.xy = blob
		bot.isMoving = True
		#print("Moving")

	#printStatement = ""
	#for i,robot in enumerate(robots):
	#	printStatement+= "Robot "+str(i)+" at "+str(robot.xy) + " ; "


def robotMove(robot,speed,orientation):
	global robots
	robot.roll(int(speed),int(orientation))	

def allocateGoal(robot,i):
	global counter,goals, costMatrix
	for j,goal in enumerate(goals):
		costMatrix[j,i] = (np.linalg.norm(np.array(robot.xy)-np.array(goal)))
		counter+=1

def getGoals():
	global goals
	goals= [[20,80],[50,60],[80,80]]#,[80,60]]

def moveToGoal(robot):
	global robots
	
	while motionEnabled:
		
		if (robot.available and robot.currentGoal != [0,0]):
			
			#print ("1 speed  ", robot.speed)
			#print ("1 heading", robot.heading)
			#print ("1 old_xy ", robot.old_xy)
			#print ("1 XY     ", robot.xy)

			current_position = robot.xy
			error = np.linalg.norm(np.array(robot.xy)-np.array(robot.currentGoal))

			if error < 5:
				robot.speed = 0
				robot.isMoving = False
				robot.currentGoal = [0,0];
				robot.keepIdle()
			else:
				robot.isMoving = True

			robot.roll(int(robot.speed),int(robot.heading))

			while (robot.xy == robot.old_xy):
				pass

			heading_vec = np.array(robot.xy)-np.array(robot.old_xy)
			current_heading = int(np.arctan2(heading_vec[1],heading_vec[0]) * 180 / np.pi)

			if current_heading<0:
				current_heading += 360
			current_heading = current_heading % 360

			goal_vec = np.array(robot.currentGoal)-np.array(robot.xy)
			ang_to_goal = int(np.arctan2(goal_vec[1],goal_vec[0]) * 180 / np.pi)

			if ang_to_goal<0:
				ang_to_goal +=360
			ang_to_goal = ang_to_goal % 360
			ang_error = ang_to_goal - current_heading
			ang_error =  ((ang_error-180)%360) + 180
			ang_error = ang_error % 360

			if ang_error <0:
				ang_error = ang_error * -1

			if ang_error >= 90:
				angle_step = 8

			elif ang_error <= 5:
				angle_step = 0

			else:
				angle_step = int(str(ang_error)[-1*len(str(ang_error))])

			angle_step = min(angle_step_max, angle_step)

			heading = robot.heading

			if ang_to_goal >= current_heading:
				if ang_to_goal - current_heading >=180:
					heading += angle_step

				else:
					heading -= angle_step
			else:
				if current_heading - ang_to_goal > 180: 
					heading -= angle_step
				else:
					heading += angle_step
			robot.heading = heading % 360

			#Speed Controller 
			speed = (int(error)/100)*speed_max - angle_step
			
			if speed > speed_max:
				speed = speed_max
			elif speed < speed_min:
				speed = speed_min

			robot.speed = speed
			robot.old_xy = current_position
			

		else:
			robot.keepIdle()
			pass

while True:

	if not initialized:
		initialize()
		print ("Initialisation Sequence Complete")
		time.sleep(1)

		

		for robot in robots:
			_thread.start_new_thread( moveToGoal, (robot,))

	updateBlob()
	for blob in blobs:
		_thread.start_new_thread( updatePosition, (blob,))

	getGoals()
	costMatrix = np.empty([len(goals),len(robots)])
	counter = 0
	for i,robot in enumerate(robots):
		_thread.start_new_thread( allocateGoal, (robot,i))

	while counter< len(robots)*len(goals):
		pass

	for i in range(len(robots)):
		theIndex = np.where(costMatrix[:,i] == np.min(costMatrix[:,i]))[0][0]
		robots[i].currentGoal = goals[theIndex]
		goals.pop(theIndex)
		costMatrix = np.delete(costMatrix,(theIndex),axis=0)
		
	printStatement = ""
	for i,robot in enumerate(robots):
		printStatement+= "Robot "+str(i)+" at "+ str(robot.xy) + "has goal "+str(robot.currentGoal) + " ; "
	print(printStatement)


		#for robot in robots:
		#	_thread.start_new_thread( robotMove, (robot, 20, 0, ))		
		#print("All Threads Done")
	time.sleep(0.1)
	
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break




# EXPERIMENTAL ROUGH WORK BELOW THIS


#v2 = balls(s2)



"""

try:
			_thread.start_new_thread(robotMove,(robot[0], 20,))
			_thread.start_new_thread(robotMove,(robot[1], 20,))
			_thread.start_new_thread(robotMove,(robot[2], 20,))
			time.sleep(3)
		except:
			print ("Error: unable to start thread")


for robot in robots:
		robot.roll(20,0)
		time.sleep(2)


while True:

		updateBlob()
		print(blobs)

		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

#v1.connect()

 

#v2.connect()

#t1 = Thread(target = updateBlob())
#t1.start()

#t2 = Thread(target)

# Initialisation Sequence Rough
updateBlob()			
oldBlob = blobs			
v1 = balls(s1)
v1.connect()
print("oldBlob ", oldBlob )
print("connect and 1s sleep starts")
time.sleep(1)
updateBlob()
print("new blob ", blobs)
print ("v1 location update ", list(x for x in blobs if x not in oldBlob))
v1.xy = list(x for x in blobs if x not in oldBlob)[0]
print (v1.xy)

updateBlob()			
oldBlob = blobs			
v2 = balls(s2)
v2.connect()
print("oldBlob ", oldBlob )
print("connect and 1s sleep starts")
time.sleep(1)
updateBlob()
print("new blob ", blobs)
print ("v2 location update ", list(x for x in blobs if x not in oldBlob))
v2.xy = list(x for x in blobs if x not in oldBlob)[0]
print (v2.xy)

"""