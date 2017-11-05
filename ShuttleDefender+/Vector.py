import math
import numpy as np

class Vector:
	def __init__(self, x, y):
		self.a = np.array([x, y])
		self.x = self.a[0]
		self.y = self.a[1]
		
	def set_x(self, x):
		self.a[0] = x
		
	def set_y(self, y):
		self.a[1] = y
	
	def __str__(self):
		return str(self.a)
		
	def angle(self):
		return math.atan2(self.a[0],self.a[1])
		
	def magnitude(self):
		magnitude = sqrt(self.a[0]**2 + self.a[1]**2)
		return magnitude
		
	def mult(self, c):
		v2 = Vector(self.a[0]*c , self.a[1]*c)
		return v2
		
	def add(self, v2):
		v3 = Vector(self.a[0] + v2.a[0], self.a[1] + v2.a[1])
		return v3
	
	def arr(self):
                return self.a
	
