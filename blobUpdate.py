from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import pickle

greenLower = (100,0, 0)
greenUpper = (255,255,255)

blob_xy_pix = [[0,0]]
blob_xy_real = [[0,0]]

robot_positions = []

camera = cv2.VideoCapture(1)

def map_to_pix(x,y):
	x = x*7
	y = (50 + (50-y))*7
	return x,y

def map_to_xy(x,y):
	x = int(x//7)
	y = 50 + (50-(int(y//7)))
	return x,y

while True:
#def blobUpdate():

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

	outbuff =[]
	if len(cnts) > 0:
		for c in cnts:
			#c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			if radius > 3:
				cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
				#blob_xy_pix[0] = [int(x),int(y)]
				buff = map_to_xy(x,y)
				blob_xy_real[0] = [int(buff[0]),int(buff[1])]
				outbuff.append([int(buff[0]),int(buff[1])])
				robot_positions = outbuff
	with open("blobLocations", 'wb') as f:
		if len(cnts) <= 0:
			robot_positions =[]
		pickle.dump(robot_positions, f)
		print(robot_positions)

		#print (blob_xy_real)
	#print(robot_positions)
	cv2.imshow("Frame", frame)

	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()