#The Swarming Project by CP Sridhar
#Reference https://docs.python.org/3/tutorial/classes.html
import numpy as np

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
		print("Edge1 is from robot "+str(self.frm.number)+" to robot "+str(self.to.number)+" and is of weight "+str(self.weight))


def incidence():
	the_incidence = np.zeros((len(vertices),len(edges)))
	for edge in range(len(vertices)):
		#print(the_incidence[:,edge])
		the_incidence[edges_name[edge].frm.number-1,edge] = -1* edges_name[edge].weight 
		the_incidence[edges_name[edge].to.number-1,edge] = edges_name[edge].weight 
	return the_incidence

def laplacian():
	the_incidence = incidence()
	return np.matmul(the_incidence,the_incidence.transpose())

def converge(T,dt):
	L = laplacian()
	for i in range(int(T//dt)):
		_x = []
		_y = []
		for vertex in vertices_name:
			 _x.append(vertex.x)
			 _y.append(vertex.y)
		_x -= (L.dot(_x)*dt)
		_y -= (L.dot(_y)*dt)
		for index in range(len(_x)):
			vertices_name[index].x =  _x[index]
			vertices_name[index].y =  _y[index]


# Robot_Name = bots(Robot_Number,X-coordinate,Y-coordinate,Orentation in degrees)
v1 = bots(1,0,10,0)
v2 = bots(2,10,10,0)
v3 = bots(3,10,0,0)
v4 = bots(4,0,0,0)

print("")
v1.description()
v2.description()
v3.description()
v4.description()

# Edge_Name = edge(Edge_Number,From,To,Weight)
e1 = edge(1,v1,v2,1)
e2 = edge(2,v2,v3,1)
e3 = edge(3,v4,v3,1)
e4 = edge(4,v1,v4,1)

print("")
e1.description()
e2.description()
e3.description()
e4.description()

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
	print i.position()

#print (incidence())
#print (incidence().transpose())
#print (laplacian())


dt = 0.01
T = 2.0

converge(T,dt)

print ("Lets see what is connected to what")
for i in vertices_name:
	print i.position()
print (i)

	


#CREATE AND DELETE INSTANCE OF OBJECTS
#v1.test = 100
#print(v1.test)
#del v1.test
#print(v1.test)
