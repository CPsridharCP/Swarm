#The Swarming Project by CP Sridhar
#Reference https://docs.python.org/3/tutorial/classes.html
import numpy as np
import matplotlib.pyplot as plt

vertices = []
vertices_name = []
edges = []
edges_name =[]

class bots:

	def __init__(self,number,x,y,orientation):
		self.number = number
		self.x = x
		self.y = y
		self.orientation = orientation #in degree
		self.adjacent = []

		vertices.append(self.number)
		vertices_name.append(self)

	def description(self):
		print ("The robot " + str(self.number) + " robot is at ("+ str(self.x) +","+ str(self.y) +") location in " + str(self.orientation) + " degree orientation" )

	def position(self):
		return [self.x,self.y]

	def orientation(self):
		return self.orientation

	def is_connected_to(self):
		print (self.adjacent)


class edge(bots):

	def __init__(self,number,botOne,botTwo,weight):
		self.number = number
		self.frm = botOne
		self.to = botTwo
		self.weight = weight

		edges.append(self.number)
		edges_name.append(self)

		self.frm.adjacent.append(self.to.number)

	def description(self):
		print("Edge is from robot "+str(self.frm.number)+" to robot "+str(self.to.number)+" and is of weight "+str(self.weight))


def incidence():
	the_incidence = np.zeros((len(vertices),len(edges)))
	for edge in range(len(edges_name)):
		#print(the_incidence[:,edge])
		the_incidence[edges_name[edge].frm.number-1,edge] = -1* edges_name[edge].weight 
		the_incidence[edges_name[edge].to.number-1,edge] = edges_name[edge].weight 
	return the_incidence

def laplacian():
	the_incidence = incidence()
	return np.matmul(the_incidence,the_incidence.transpose())

def get_currect_position():
	_x = []
	_y = []
	for vertex in vertices_name:
		_x.append(vertex.x)
		_y.append(vertex.y)
	return _x,_y 

def get_goal_position():
	_gx = []
	_gy = []
	for vertex in vertices_name:
		_gx.append(vertex.goal[0])
		_gy.append(vertex.goal[1])
	return _gx,_gy 

def update_position(_x,_y):
	for index in range(len(_x)):
		vertices_name[index].x =  _x[index]
		vertices_name[index].y =  _y[index]


def converge(T,dt):
	L = laplacian()
	for i in range(int(T//dt)):
		_x,_y = get_currect_position()
		# Consensus
		_x -= (L.dot(_x)*dt)
		_y -= (L.dot(_y)*dt)
		plot(_x,_y)
		update_position(_x,_y)

# WORK IN PROGRESS
def formation(T,dt,k):
	
	_gx,_gy = get_goal_position()
	for i in range(int(T//dt)):
		L = laplacian()
		_x ,_y  = get_currect_position()
		# Zref Method
		_x += (k*(L.dot(_gx))*dt) - (k*(L.dot(_x)*dt))
		_y += (k*(L.dot(_gy))*dt) - (k*(L.dot(_y)*dt))
		plot(_x,_y)
		update_position(_x,_y)

		

def plot(x,y):
	the_plot, = plt.plot(x,y,'bs')
	plt.axis([-8,9,-7,17])
	plt.xlabel('x')
	plt.ylabel('y')
	plt.pause(0.05)
	the_plot.remove()

	#plt.show()


#dt = 0.3
#T = 20.0
#k = 0.5

dt = 0.1
T = 7.0
k = 4


# Robot_Name = bots(Robot_Number,X-coordinate,Y-coordinate,Orentation in degrees)
v1 = bots(1,1,1,0)
v2 = bots(2,1,2,0)
v3 = bots(3,1,3,0)
v4 = bots(4,1,4,0)
v5 = bots(5,1,5,0)
v6 = bots(6,1,6,0)
v7 = bots(7,1,7,0)
v8 = bots(8,1,8,0)
v9 = bots(9,1,9,0)
v10 = bots(10,1,10,0)
v11 = bots(11,1,11,0)
v12 = bots(12,1,12,0)
v13 = bots(13,1,13,0)


print("")
v1.description()
v2.description()
v3.description()
#v4.description()

# Edge_Name = edge(Edge_Number,From,To,Weight)
e1 = edge(1,v1,v2,1)
e2 = edge(2,v2,v3,1)
e3 = edge(3,v3,v4,1)
e4 = edge(4,v4,v5,1)
e5 = edge(5,v5,v6,1)
e6 = edge(6,v6,v7,1)
e7 = edge(7,v7,v8,1)
e8 = edge(8,v8,v9,1)
e9 = edge(9,v9,v10,1)
e10 = edge(10,v10,v11,1)
e11 = edge(11,v11,v12,1)
e12 = edge(12,v12,v13,1)

#e4 = edge(4,v1,v4,1)
#e5 = edge(5,v1,v3,3)

print("")
e1.description()
e2.description()
e3.description()
#e4.description()

print("")
v1.is_connected_to()
v2.is_connected_to()
v3.is_connected_to()
v4.is_connected_to()

#print("")
#print (vertices)
#print (vertices_name)
#print (edges)
#print (edges_name)

print ("Lets see what is connected to what")
for i in vertices_name:
	print (i.position())
#print (incidence())
#print (incidence().transpose())
#print (laplacian())


#converge(T,dt)

print ("Lets see what is connected to what")
for i in vertices_name:
	print (i.position())
print (i)

while True:

	v1.goal = [12,3]
	v2.goal = [3,3]
	v3.goal = [12,6]
	v4.goal = [3,6]
	v5.goal = [12,9]
	v6.goal = [9.75,9]
	v7.goal = [7.5,9]
	v8.goal = [5.25,9]
	v9.goal = [3,9]
	v10.goal = [12,12]
	v11.goal = [12,15]
	v12.goal = [3,12]
	v13.goal = [3,15]

	formation(T,dt,k)

	v1.goal = [12,3]
	v2.goal = [3,3]
	v3.goal = [12,6]
	v4.goal = [3,6]
	v5.goal = [12,9]
	v6.goal = [9.75,12]
	v7.goal = [7.5,10]
	v8.goal = [5.25,12]
	v9.goal = [3,9]
	v10.goal = [12,12]
	v11.goal = [12,15]
	v12.goal = [3,12]
	v13.goal = [3,15]

	formation(T,dt,k)

	v1.goal = [12,3]#####
	v2.goal = [5,4.5]###
	v3.goal = [9.5,3]######
	v4.goal = [4,6]####
	v5.goal = [3,9]######
	v6.goal = [7,15]#####
	v7.goal = [7,3]#####
	v8.goal = [5.5,13.5]#####
	v9.goal = [3,7.5]######
	v10.goal = [9.5,15]#####
	v11.goal = [12,15]######
	v12.goal = [3,10.5]#####
	v13.goal = [4,12]#####

	formation(T,dt,k)

	v1.goal = [8,12]#####
	v2.goal = [3,3]######
	v3.goal = [6,10]#####
	v4.goal = [3,5]#####
	v5.goal = [3,9]######
	v6.goal = [4,15]#####
	v7.goal = [4,9]#####
	v8.goal = [3,15]####
	v9.goal = [3,7]####
	v10.goal = [6,14]
	v11.goal = [8,13]####
	v12.goal = [3,11]####
	v13.goal = [3,13]####

	formation(T,dt,k)



print ("Lets see what is connected to what")
for i in vertices_name:
	print (i.position())

#CREATE AND DELETE INSTANCE OF OBJECTS
#v1.test = 100
#print(v1.test)
#del v1.test
#print(v1.test)