from Vector import *
from Projectile import * 
import math
from pylygon import Polygon

class Entity:

	def __init__(self, direction, position, health, mode, velocity, friction, maxspeed, points):
		self.direction = direction
		self.position = position
		self.health = health
		self.mode = mode
		self.velocity = velocity
		self.friction = friction
		self.maxspeed = maxspeed
		pnts_list = []
		for i in points:
			pnts_list.append(pnt_proj(self.position, self.direction+i[0], i[1]))
		self.body = Polygon(pnts_list)
	
	def __str__(self):
		return str(self.direction) + str(self.position) + str(self.velocity)
		
	def _rect(self):
		return self.body.get_rect()
		
	def update(self,delta_t):
		#self.body.move_ip(self.velocity.x*(delta_t), self.velocity.y*(delta_t))
		self.position = self.position.add(self.velocity.mult(delta_t))
		self.velocity = self.velocity.mult(1-self.friction*delta_t)
		if abs(self.velocity.x) < 0.8: self.velocity.set_x(0)
		if abs(self.velocity.y) < 0.8: self.velocity.set_y(0)
		self.body.C = (self.position.x, self.position.y)
		
	def turn(self, angle, delta_t):
		self.direction = self.direction + angle*delta_t
		self.body.rotate_ip(angle*delta_t)
		if self.direction > 2*math.pi:
			self.direction = self.direction-2*math.pi
		if self.direction < 0:
			self.direction = self.direction+2*math.pi
	
	def  move(self, speed):
		delta_v = Vector(math.cos(self.direction)*speed, math.sin(self.direction)*speed)
		self.velocity = self.velocity.add(delta_v)
		if self.velocity.magnitude > self.maxspeed:
			self.velocity.set_x(self.maxspeed*math.cos(self.direction))
			self.velocity.set_y(self.maxspeed*math.sin(self.direction))
			
	def check_bounds(self):
		rect =  self.body.get_rect()
	
		#checks if ship is leaving the screen and stops the ship from leaving the screen
		#Right, Left, Top, and then Bottom 
	
		if rect.right >= 400 and self.velocity.x > -1:
			self.position.set_x(400 - abs(rect.right - self.position.x))
			self.velocity.set_x(0)
			
		if rect.left <= 0 and self.velocity.x < 1:
			self.position.set_x(0 + abs(rect.left - self.position.x))
			self.velocity.set_x(0)
		
		if rect.top <= 0 and self.velocity.y < 1:
			self.position.set_y(0 + abs(rect.top - self.position.y))
			self.velocity.set_y(0)
			
		if rect.bottom >= 400 and self.velocity.y > -1:
			self.position.set_y(400 - abs(rect.bottom - self.position.y))
			self.velocity.set_y(0)
			
# additional Functions:
			
def pnt_proj(position, angle, magnitude):
	pnt_x = position.x + magnitude*math.cos(angle)
	pnt_y = position.y + magnitude*math.sin(angle)
	return (pnt_x,pnt_y)