from Entity import *


class Ship(Entity):

	def __init__(self, direction, position):
		shipBody = [(0,10),(0,-10*math.cos(2.0/9*math.pi)),(7.0/9*math.pi, 10), (-7.0/9*math.pi, 10)]
		Entity.__init__(self, direction, position, 0, 0, Vector(0,0), 1.0, 150, shipBody)
		
	def shoot(self):
		if self.mode == 0:
			laser = Projectile(Vector(self.position.x, self.position.y), Vector(math.cos(self.direction)*500,(math.sin(self.direction)*500)), 5.0, (255, 155, 155))
			return [laser]
			
		elif self.mode == 1:
			laser_1 = Projectile(Vector((self.position.x + 3 * (math.cos(self.direction + 90))), self.position.y + 3 * (math.sin(self.direction + 90))), Vector(math.cos(self.direction)*500,(math.sin(self.direction)*500)), 10.0, (0, 255, 255))
			
			laser_2 = Projectile((Vector(self.position.x + 3 * (math.cos((self.direction - 90))), self.position.y + 3 * math.sin(self.direction - 90))), Vector(math.cos(self.direction)*500,math.sin(self.direction)*500), 10.0, (0, 255, 255))
			
			return [laser_1, laser_2]
		