import pygame
import math
from sd_classes import * 
from pylygon import Polygon
import numpy

wall_l = Polygon([(0,0), (0,400)])
wall_t = Polygon([(0,0), (400,0)])
wall_b = Polygon([(0,400), (400,400)])
wall_r = Polygon([(400,0), (400,400)])

pygame.init

screen = pygame.display.set_mode((400,400))
end = False
ship_laser_list = []

def pnt_proj(position, angle, magnitude):
	pnt_x = position.x + magnitude*math.cos(angle)
	pnt_y = position.y + magnitude*math.sin(angle)
	return (pnt_x,pnt_y)

def pnt_move(position, x_d, y_d):
	pnt_x = position.x + x_d
	pnt_y = position.y + y_d
	return (pnt_x, pnt_y)


	

			
class PlayerEnt(Entity):
	def __init__(self, direction, position, health, mode, velocity, friction, maxspeed):
		Entity.__init__(self, direction, position, health, mode, velocity, friction, maxspeed)
	
		
			
# hit boxes, boundaries, etc.
	
		

# ship object
ship = Entity((3*math.pi/2), Vector(200,300), 0, 0, Vector(0,0), 1.0, 150)

movement = False
turnright = False
turnleft = False
const_fire = [0, False]


# main

clock = pygame.time.Clock()
while not end:
	#events, keys, etc.
	
	tick = clock.get_time()/1000.0
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			end = True
		if event.type == pygame.KEYDOWN:
			key = pygame.key.get_pressed()
			if key[pygame.K_UP]: 
				movement = True
			if key[pygame.K_RIGHT]:
				turnright = True
			if key[pygame.K_LEFT]:
				turnleft = True
			if key[pygame.K_z]:
				if ship.mode == 0:
					ship_laser_list.append(ship.shoot())
				elif ship.mode == 1:
					const_fire[1] = True
			if key[pygame.K_x]:
				if ship.mode == 1:
					ship.mode = 0
					const_fire[1] = False
				elif ship.mode == 0:
					ship.mode = 1
						
		if event.type == pygame.KEYUP:
			key = event.key
			if key == pygame.K_RIGHT:
				turnright = False
			if key == pygame.K_LEFT:
				turnleft = False 
			if key == pygame.K_UP:
				movement = False
			if key == pygame.K_z and ship.mode == 1:
				const_fire[1] = False
	
	#responses to keys; i.e. movement and turning
	
	if movement:
		ship.move(100)
	if turnright:
		ship.turn(+math.pi*3/2.0,tick)
	if turnleft:
		ship.turn(-math.pi*3/2.0, tick)
	ship.check_bounds()
	ship.update(tick)
	if const_fire[1] == True:
		const_fire[0] += 1
		if const_fire[0] == 10:
			for i in ship.shoot():
				ship_laser_list.append(i)
			const_fire[0] = 0
	elif const_fire[0] == False:
                const_fire[0] = 9
	
	
	
	screen.fill((0,0,0))
	
	#Powerup Graphics
	
	pow_pos = Vector(200,100)
	pow_rgt = (pow_pos.x + 5, pow_pos.y)
	pow_bot = (pow_pos.x, pow_pos.y + 5)
	pow_lft = (pow_pos.x - 5, pow_pos.y)
	pow_top = (pow_pos.x, pow_pos.y - 5)
	pow_body = Polygon([pow_rgt, pow_bot, pow_lft, pow_top])
	pow_geom_list = [[pow_top, pow_bot], [pow_rgt, pow_lft], [pow_top, pow_rgt], [pow_top, pow_lft], [pow_bot, pow_lft], [pow_bot, pow_rgt]]
	for i in pow_geom_list:
		pygame.draw.lines(screen, (150,255,255),True,i)

		
	
	
	# Ship Graphics
	
	pygame.draw.lines(screen, (255,255,255),True,ship.body.P)
	pygame.draw.lines(screen, (255,255,255),False, [pnt_proj(ship.position, ship.direction, 10), pnt_proj(ship.position, ship.direction, -10*math.sin(2.0/9*math.pi))])
	shipline = ship.body.project((0,1))

	# Laser Manipulation and Graphics
	
	# For projectile objects
	for laser in ship_laser_list:
		if laser.check_bounds():
			laser.update(tick)
			pygame.draw.lines(screen, laser.colour ,False ,[(laser.position.x, laser.position.y),(laser.position.x + laser.length*math.cos(laser.velocity.angle()), laser.position.y + laser.length*math.sin(laser.velocity.angle()))])
		else:
			ship_laser_list.remove(laser)
	
	clock.tick(60)
	pygame.display.update()
pygame.quit()

	
	
	
	
	
	
