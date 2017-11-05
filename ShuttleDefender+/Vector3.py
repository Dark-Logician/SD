import math

class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __str__(self):
		return '[' + str(self.x) + ',' + str(self.y) + ']'
		
	def angle(self):
		return math.atan2(self.y,self.x)
		
	def magnitude(self):
		magnitude = sqrt(self.x**2 + self.y**2)
		return magnitude
		
	def mult(self, c):
		v2 = Vector(self.x*c , self.y*c)
		return v2
		
	def add(self, v2):
		v3 = Vector(self.x + v2.x, self.y + v2.y)
		return v3
		
