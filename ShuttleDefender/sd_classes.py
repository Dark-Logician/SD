class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __str__(self):
		return '[' + str(self.x) + ',' + str(self.y) + ']'
		
	def add(self, v2):
		v3 = Vector(self.x + v2.x, self.y + v2.y)
		return v3
		
	def magnitude(self):
		magnitude = sqrt(self.x**2 + self.y**2)
		return magnitude
		
	def mult(self, c):
		v2 = Vector(self.x*c , self.y*c)
		return v2
		
	def angle(self):
		return math.atan2(self.y,self.x)

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

class Entity:
	def __init__(self, direction, position, health, mode, velocity, friction, maxspeed):
		self.direction = direction
		self.position = position
		self.health = health
		self.mode = mode
		self.velocity = velocity
		self.friction = friction
		self.maxspeed = maxspeed
	
	def __str__(self):
		return str(self.direction) + str(self.position) + str(self.velocity)
		
	def update(self,delta_t):
		self.position = self.position.add(self.velocity.mult(delta_t))
		self.velocity = self.velocity.mult(1-self.friction*delta_t)
		
	def turn(self, angle, delta_t):
		self.direction = self.direction + angle*delta_t
		if self.direction > 2*math.pi:
			self.direction = self.direction-2*math.pi
		if self.direction < 0:
			self.direction = self.direction+2*math.pi
	
	def  move(self, speed):
		delta_v = Vector(math.cos(self.direction)*speed, math.sin(self.direction)*speed)
		self.velocity = self.velocity.add(delta_v)
		if self.velocity.magnitude > self.maxspeed:
			self.velocity.x = self.maxspeed*math.cos(self.direction)
			self.velocity.y = self.maxspeed*math.sin(self.direction)
	
	def shoot(self):
		if self.mode == 0:
			laser = Projectile(Vector(self.position.x, self.position.y), Vector(math.cos(self.direction)*500,(math.sin(self.direction)*500)), 5.0, (255, 155, 155))
			return laser
			print True
			
		elif self.mode == 1:
			laser_1 = Projectile(Vector((self.position.x + 3 * (math.cos(ship.direction + 90))), self.position.y + 3 * (math.sin(ship.direction + 90))), Vector(math.cos(self.direction)*500,(math.sin(self.direction)*500)), 10.0, (0, 255, 255))
			
			laser_2 = Projectile((Vector(self.position.x + 3 * (math.cos((ship.direction - 90))), self.position.y + 3 * math.sin(ship.direction - 90))), Vector(math.cos(self.direction)*500,math.sin(self.direction)*500), 10.0, (0, 255, 255))
			
			return [laser_1, laser_2]