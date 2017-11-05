import pygame
import math
import random
from pylygon import Polygon 


generate = True
end = False
pygame.init
screen = pygame.display.set_mode((200,200))
met_list = []

met_positions = [[25,25],[75,25],[125,25],[175,25], [25,75], [75,75], [125,75], [175,75], [25,125],[75,125],[125,125],[175,125], [25,175], [75,175], [125,175], [175,175]]

clock = pygame.time.Clock()
while not end: 

	tick = clock.get_time()/1000.0
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			end = True
		if event.type == pygame.KEYDOWN:
			key = pygame.key.get_pressed()
			if key[pygame.K_ESCAPE]:
				end = True
			if key[pygame.K_SPACE]:
				generate = True
		
		
	
	screen.fill((0,0,0))

	# meteorite
	if generate:
		met_poly_list=[]
		for i in met_positions:
			met_radius = random.randrange(10,15)
			met_edgenum = random.randrange(5,10)
			met_point_angles = []
			for j in range(met_edgenum):
				met_point_angles.append(2 * math.pi/ float(met_edgenum) *	 j + math.radians(random.randrange(15)))
			met_point_list = []
			for j in met_point_angles:
				met_point_list.append([i[0] + math.cos(j) * met_radius, i[1] + math.sin(j) * met_radius])
			meteor = Polygon(met_point_list)
			met_poly_list.append(meteor)
		generate = False
	
	for i in met_poly_list:
		
		pygame.draw.lines(screen, (250,250,100), True, i.P)
		i.rotate_ip(math.pi/180)

		
	
	
	clock.tick(60)
	pygame.display.update()
pygame.quit

