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

s1 = Sphero("C9:93:8F:F1:91:E2")
s2 = Sphero("DA:06:00:55:3A:8D")
s3 = Sphero("DC:F3:09:7B:4D:BB")

class balls:
	
	def __init__(self,identifier,xy=[0,0],available = False):
		self.identifier = identifier
		self.xy = xy
		self.available = available
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


	


v1 = balls(s1)
v2 = balls(s2)
v3 = balls(s3)

#print(type(s1))
#print(type(v1))
#print(type(robots[0]))

variables = [v1,v2,v3]
initialized = False

def initialize():
	global blobs, robots, initialized
	print("Initialisation Sequence Initiated..")
	for variable in variables:
		updateBlob()
		oldBlob = blobs
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
		#variable.xy = list(x for x in blobs if x not in oldBlob)[0]
		#print(variable," is at ",variable.xy)
		for robot in robots:
			if (robot.available):
				robot.keepIdle()
	initialized = True

def robotMove(robot,speed,orientation):
	global robots
	print("Thread Starts with ", robot)
	robot.roll(int(speed),int(orientation))	
	time.sleep(2)


while True:

	if not initialized:
		initialize()
		print ("Initialisation Sequence Complete")

		for robot in robots:
			_thread.start_new_thread( robotMove, (robot, 20, 0, ) )
			#robotMove(robot,20,0)
			
		print("All Threads Done")

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