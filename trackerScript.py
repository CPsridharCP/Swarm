from collections import deque
import numpy as np
import argparse
import imutils
import cv2

from sphero_sprk import Sphero 
import time

greenLower = (100,0, 0)
greenUpper = (255,255,255)

blob_xy_pix = [[0,0]]
blob_xy_real = [[0,0]]
heading = [False]
goal = [0,0]

speed = 15

#heading_gain = 0.1

camera = cv2.VideoCapture(1)

speed_min = 30
speed_max = 40
angle_step_max = 18
error_old = 0
error_new = 0
robot_xy_new = [0,0]
robot_xy_old = [0,0]

heading = 0

def map_to_pix(x,y):
	x = x*7
	y = (50 + (50-y))*7
	return x,y

def map_to_xy(x,y):
	x = int(x//7)
	y = 50 + (50-(int(y//7)))
	return x,y

def get_goal(event, x, y, flags, param):
	global goal,goal_set
	if event == cv2.EVENT_LBUTTONDOWN:
		buff = map_to_xy(x,y)
		goal = [int(buff[0]), int(buff[1])]
		goal_set = True
		print("mouse click event")

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", get_goal)
goal_set = False

orb = Sphero("C9:93:8F:F1:91:E2")
orb.connect()
print ("Connection 1 Established")
print(orb.ping())
time.sleep(2)



while True:

	(grabbed, frame) = camera.read()

	frame = imutils.resize(frame, width=1200)
	height = np.size(frame,0)
	width = np.size(frame,1)
	frame = frame[int(1.3*height/10):int(9.1*height/10), int(1.75*width/10):int(7.6*width/10)]
	blurred = cv2.GaussianBlur(frame, (15, 15), 0)
	#hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	kernel = np.ones((10,10),np.uint8)
	mask = cv2.inRange(blurred, greenLower, greenUpper)
	#cv2.imshow("mask",mask)
	mask = cv2.erode(mask, kernel, iterations=2)
	#cv2.imshow("erode",mask)
	mask = cv2.dilate(mask, kernel, iterations=2)
	cv2.imshow("dilate",mask)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	#print ("cnts length", len(cnts))
	center = None

	if goal_set:
		buff = map_to_pix(goal[0], goal[1])
		cv2.circle(frame, (buff[0],buff[1]), 30,(0, 255, 255), -1)


	if len(cnts) > 0:
		#for c in cnts:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 3:
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			blob_xy_pix[0] = [int(x),int(y)]
			buff = map_to_xy(x,y)
			blob_xy_real[0] = [int(buff[0]),int(buff[1])]
	#print (blob_xy_real)
	
	cv2.imshow("Frame", frame)
	#print (goal)

	error = np.linalg.norm(np.array(blob_xy_real)-np.array(goal))
	#print(error)

	
	angle_step = 5

	if goal_set and error>5:
		
		error_new = error
		chg_in_error = error_old - error_new
		
		# compare robot position in two time steps to find robot heading
		# calculate angle to goal using current robot position and goal position
		# Use both to decide next heading command
		# CONTROLS
		
		
		if error < 10:
			speed = 0

		robot_xy_new = blob_xy_real[0]

		orb.roll(int(speed),int(heading))

		for i in range(100000):
			pass

		heading_vec = np.array(robot_xy_new)-np.array(robot_xy_old)
		current_heading = np.arctan2(heading_vec[1],heading_vec[0]) * 180 / np.pi

		if current_heading<0:
			current_heading += 360

		goal_vec = np.array(goal)-np.array(robot_xy_new)
		ang_to_goal = np.arctan2(goal_vec[1],goal_vec[0]) * 180 / np.pi

		if ang_to_goal<0:
			ang_to_goal +=360

		# Angle step Controller
		ang_error = ang_to_goal - current_heading
		if ang_error <0:
			ang_error = ang_error * -1

		if ang_error >= 90:
			angle_step = 8

		elif ang_error > 50 and ang_error < 90 :
			angle_step = 5

		else:
			angle_step = 3

		#angle_step = (ang_error/24)
		print (ang_error)

		if angle_step > angle_step_max:
			angle_step = angle_step_max


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

		heading = heading % 360

		#Speed Controller 
		speed = (int(error)/100)*speed_max
		if speed > speed_max:
			speed = speed_max
		elif speed < speed_min:
			speed = speed_min
		#print (speed)


		#print (current_heading, " >>> ", heading_gain* (ang_to_goal -current_heading) )
		#print (heading)

		robot_xy_old = robot_xy_new

	
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()