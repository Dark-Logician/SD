from Vector import *
from Projectile import * 
from Entity import *
from Ship import Ship

import pygame
import math
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

# ship object
ship = Ship((3*math.pi/2), Vector(200,300))

movement = False
turnright = False
turnleft = False
holdingFire = False
firingDelay = 0



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
					ship_laser_list += ship.shoot()
				elif ship.mode == 1:
					holdingFire = True
			if key[pygame.K_x]:
				if ship.mode == 1:
					ship.mode = 0
					holdingFire = False
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
				holdingFire = False
	
	#responses to keys; i.e. movement and turning
	
	
	if movement:
		ship.move(100)
	if turnright:
		ship.turn(+math.pi*3/2.0,tick)
	if turnleft:
		ship.turn(-math.pi*3/2.0, tick)
	if holdingFire and firingDelay == 0:
		firingDelay = 10
		ship_laser_list += ship.shoot()
	ship.check_bounds()
	ship.update(tick)
	if firingDelay > 0:
		firingDelay -= 1
	
	
	
	screen.fill((0,0,0))
	
	#pygame.draw.rect(screen, (200,100,100), [200, 200, 3, 3])

		
	
	
	# Ship Graphics
	
	pygame.draw.lines(screen, (255,255,255),True,ship.body.P)
	#Holy shit was this complicated
	shipline = [pnt_proj(ship.position, ship.direction, 10), pnt_proj(ship.position, ship.direction, -(20*math.cos(7.0/9*math.pi)+10)/3 + 10*math.cos(7.0/9*math.pi))]
	pygame.draw.lines(screen, (255,255,255),False, shipline)

	# Laser Manipulation and Graphics
	
	# For projectile objects
	for laser in ship_laser_list:
		if laser.check_bounds():
			laser.update(tick)
			pygame.draw.lines(screen, laser.colour ,False ,[(laser.position.x, laser.position.y),(laser.position.x + laser.length*math.sin(laser.velocity.angle()), laser.position.y + laser.length*math.cos(laser.velocity.angle()))])
		else:
			ship_laser_list.remove(laser)
	
	clock.tick(60)
	pygame.display.update()
pygame.quit()

	