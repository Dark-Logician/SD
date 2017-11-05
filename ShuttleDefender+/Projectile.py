from Vector import *
import math

class Projectile():
	def __init__(self, position, velocity, length, colour):
		self.velocity = velocity
		self.position = position
		self.length = length
		self.colour = colour
		
	def __str__(self):
		return str(self.position) + str(self.velocity)
		
	def update(self, delta_t):
		self.position.x = self.position.x+(self.velocity.x*delta_t)
		self.position.y = self.position.y+(self.velocity.y*delta_t)
		
	def check_bounds(self):
		if (self.position.x > 410) or (self.position.x < -10) or (self.position.y > 410) or (self.position.y < -10):
			return False
		else:
			return True