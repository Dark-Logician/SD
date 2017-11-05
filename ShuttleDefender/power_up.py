import pygame
import math
from pylygon import Polygon
import numpy

pygame.init
icon = pygame.image.load("C:\Users\Evan\Desktop\Code Projects\ShuttleDefender\SD - Sprites\Shuttle.PNG")
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((160,160))
end = False

#Automatic Fire
A_position = [10,10]
A_shape = Polygon([(A_position[0] - 3, A_position[1] - 6), (A_position[0] + 3, A_position[1] - 6), (A_position[0] - 3, A_position[1] + 6), (A_position[0] + 3, A_position[1] + 6)])
A_shape2 = Polygon([(A_position[0] - 3, A_position[1] - 2), (A_position[0] + 3, A_position[1] - 2),(A_position[0] + 3, A_position[1] + 2), (A_position[0] - 3, A_position[1] + 2)])




clock = pygame.time.Clock()
while not end:
	#events, keys, etc.
	
	tick = clock.get_time()/1000.0
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			end = True
	screen.fill((0,0,0))
	
	A_shape.rotate_ip(1/60.0)
	A_shape2.rotate_ip(1/60.0)
	
	pygame.draw.lines(screen, (0,255,255) ,True ,A_shape.P)
	pygame.draw.lines(screen, (0,255,255) ,True ,A_shape2.P)
	
	clock.tick(60)
	pygame.display.update()
pygame.quit()